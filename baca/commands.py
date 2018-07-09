import abjad
import collections
import typing
from . import indicators
from . import library
from . import scoping
from . import typings
from .Selection import Selection
from .Selection import _select
from .Sequence import Sequence


### CLASSES ###

class BCPCommand(scoping.Command):
    """
    Bow contact point command.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bow_contact_points',
        '_final_spanner',
        '_helper',
        '_tweaks',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *tweaks: abjad.LilyPondTweakManager,
        bcps: typing.Iterable[typing.Tuple[int, int]] = None,
        final_spanner: bool = None,
        helper: typing.Callable = None,
        selector: typings.Selector = None,
        ) -> None:
        scoping.Command.__init__(self, selector=selector)
        if bcps is None:
            self._validate_bcps(bcps)
        self._bow_contact_points = bcps
        if final_spanner is not None:
            final_spanner = bool(final_spanner)
        self._final_spanner = final_spanner
        if helper is not None:
            assert callable(helper), repr(helper)
        self._helper = helper
        self._validate_tweaks(tweaks)
        self._tags = [abjad.Tag('BACA_BCP_COMMAND')]
        self._tweaks = tweaks

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if self.bow_contact_points is None:
            return
        if self.selector:
            argument = self.selector(argument)
        leaves = Selection(argument).leaves()
        bcps_ = Sequence(self.bow_contact_points)
        if self.helper:
            bcps_ = self.helper(bcps_, argument)
        bcps = abjad.CyclicTuple(bcps_)
        lts = Selection(argument).lts()
        total = len(lts)
        add_right_text_to_me = None
        if not self.final_spanner:
            rest_count, nonrest_count = 0, 0
            for lt in reversed(lts):
                if self._is_rest(lt.head):
                    rest_count += 1
                else:
                    if 0 < rest_count and nonrest_count == 0:
                        add_right_text_to_me = lt.head
                        break
                    if 0 < nonrest_count and rest_count == 0:
                        add_right_text_to_me = lt.head
                        break
                    nonrest_count += 1
        if (self.final_spanner and
            not self._is_rest(lts[-1]) and
            len(lts[-1]) == 1):
            next_leaf_after_argument = abjad.inspect(lts[-1][-1]).get_leaf(1)
            if next_leaf_after_argument is None:
                raise Exception(
                    'can not attach final spanner:'
                    ' argument includes end of score.'
                    )
        previous_bcp = None
        i = 0
        for lt in lts:
            stop_text_span = abjad.StopTextSpan(
                command=self.stop_command,
                )
            if (not self.final_spanner and
                lt is lts[-1] and
                not self._is_rest(lt.head)):
                abjad.attach(
                    stop_text_span,
                    lt.head,
                    tag=self.tag,
                    )
                break
            previous_leaf = abjad.inspect(lt.head).get_leaf(-1)
            if (self._is_rest(lt.head) and
                (self._is_rest(previous_leaf) or previous_leaf is None)):
                continue
            if (isinstance(lt.head, abjad.Note) and
                self._is_rest(previous_leaf) and
                previous_bcp is not None):
                numerator, denominator = previous_bcp
            else:
                bcp = bcps[i]
                numerator, denominator = bcp
                i += 1
                next_bcp = bcps[i]
            string = rf'\markup \baca-bcp-left #{numerator} #{denominator}'
            left_literal = abjad.LilyPondLiteral(string)
            if lt is lts[-1]:
                if self.final_spanner:
                    style = 'solid_line_with_arrow'
                else:
                    style = 'invisible_line'
            elif not self._is_rest(lt.head):
                style = 'solid_line_with_arrow'
            else:
                style = 'invisible_line'
            right_literal = None
            if lt.head is add_right_text_to_me:
                numerator, denominator = next_bcp
                string = rf'\markup \baca-bcp-right #{numerator} #{denominator}'
                right_literal = abjad.LilyPondLiteral(string)
            start_text_span = abjad.StartTextSpan(
                command=self.start_command,
                left_text=left_literal,
                right_text=right_literal,
                style=style,
                )
            abjad.attach(
                start_text_span,
                lt.head,
                tag=self.tag,
                )
            if 0 < i:
                abjad.attach(
                    stop_text_span,
                    lt.head,
                    tag=self.tag,
                    )
            if lt is lts[-1] and self.final_spanner:
                abjad.attach(
                    stop_text_span,
                    next_leaf_after_argument,
                    tag=self.tag,
                    )
            bcp_fraction = abjad.Fraction(*bcp)
            next_bcp_fraction = abjad.Fraction(*bcps[i])
            if self._is_rest(lt.head):
                pass
            elif self._is_rest(previous_leaf) or previous_bcp is None:
                if bcp_fraction > next_bcp_fraction:
                    abjad.attach(
                        abjad.Articulation('upbow'),
                        lt.head,
                        tag=self.tag,
                        )
                elif bcp_fraction < next_bcp_fraction:
                    abjad.attach(
                        abjad.Articulation('downbow'),
                        lt.head,
                        tag=self.tag,
                        )
            else:
                previous_bcp_fraction = abjad.Fraction(*previous_bcp)
                if previous_bcp_fraction < bcp_fraction > next_bcp_fraction:
                    abjad.attach(
                        abjad.Articulation('upbow'),
                        lt.head,
                        tag=self.tag,
                        )
                elif previous_bcp_fraction > bcp_fraction < next_bcp_fraction:
                    abjad.attach(
                        abjad.Articulation('downbow'),
                        lt.head,
                        tag=self.tag,
                        )
            previous_bcp = bcp

    ### PRIVATE METHODS ###

    @staticmethod
    def _is_rest(argument):
        prototype = (abjad.Rest, abjad.MultimeasureRest, abjad.Skip)
        if isinstance(argument, prototype):
            return True
        annotation = abjad.inspect(argument).get_annotation('is_sounding')
        if annotation is False:
            return True
        return False

    @staticmethod
    def _validate_bcps(bcps):
        if bcps is None:
            return
        for bcp in bcps:
            assert isinstance(bcp, tuple), repr(bcp)
            assert len(bcp) == 2, repr(bcp)

    ### PUBLIC PROPERTIES ###

    @property
    def bow_contact_points(self) -> typing.Optional[
        typing.Iterable[typing.Tuple[int, int]]
        ]:
        r"""
        Gets bow contact points.

        ..  container:: example

            PATTERN. Define chunkwise spanners like this:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 16)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.bcps(abjad.tweak(5).staff_padding),
            ...     baca.make_even_divisions(),
            ...     baca.pitches('E4 F4'),
            ...     baca.measures(
            ...         (1, 2),
            ...         baca.bcps(bcps=[(1, 5), (2, 5)]),
            ...         ),
            ...     baca.measures(
            ...         (3, 4),
            ...         baca.bcps(bcps=[(3, 5), (4, 5)]),
            ...         ),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \baca_bar_line_visible                                                       %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                e'8
                                -\downbow                                                                %! BACA_BCP_COMMAND
                                \bacaStopTextSpanBCP                                                     %! BACA_BCP_COMMAND
                                - \abjad_solid_line_with_arrow                                           %! BACA_BCP_COMMAND
                                - \tweak bound-details.left.text \markup \baca-bcp-left #1 #5            %! BACA_BCP_COMMAND
                                \bacaStartTextSpanBCP                                                    %! BACA_BCP_COMMAND
                                [
                <BLANKLINE>
                                f'8
                                -\upbow                                                                  %! BACA_BCP_COMMAND
                                \bacaStopTextSpanBCP                                                     %! BACA_BCP_COMMAND
                                - \abjad_solid_line_with_arrow                                           %! BACA_BCP_COMMAND
                                - \tweak bound-details.left.text \markup \baca-bcp-left #2 #5            %! BACA_BCP_COMMAND
                                \bacaStartTextSpanBCP                                                    %! BACA_BCP_COMMAND
                <BLANKLINE>
                                e'8
                                -\downbow                                                                %! BACA_BCP_COMMAND
                                \bacaStopTextSpanBCP                                                     %! BACA_BCP_COMMAND
                                - \abjad_solid_line_with_arrow                                           %! BACA_BCP_COMMAND
                                - \tweak bound-details.left.text \markup \baca-bcp-left #1 #5            %! BACA_BCP_COMMAND
                                \bacaStartTextSpanBCP                                                    %! BACA_BCP_COMMAND
                <BLANKLINE>
                                f'8
                                -\upbow                                                                  %! BACA_BCP_COMMAND
                                \bacaStopTextSpanBCP                                                     %! BACA_BCP_COMMAND
                                ]
                                - \abjad_solid_line_with_arrow                                           %! BACA_BCP_COMMAND
                                - \tweak bound-details.left.text \markup \baca-bcp-left #2 #5            %! BACA_BCP_COMMAND
                                \bacaStartTextSpanBCP                                                    %! BACA_BCP_COMMAND
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                e'8
                                -\downbow                                                                %! BACA_BCP_COMMAND
                                \bacaStopTextSpanBCP                                                     %! BACA_BCP_COMMAND
                                - \abjad_solid_line_with_arrow                                           %! BACA_BCP_COMMAND
                                - \tweak bound-details.left.text \markup \baca-bcp-left #1 #5            %! BACA_BCP_COMMAND
                                \bacaStartTextSpanBCP                                                    %! BACA_BCP_COMMAND
                                [
                <BLANKLINE>
                                f'8
                                -\upbow                                                                  %! BACA_BCP_COMMAND
                                \bacaStopTextSpanBCP                                                     %! BACA_BCP_COMMAND
                                - \abjad_solid_line_with_arrow                                           %! BACA_BCP_COMMAND
                                - \tweak bound-details.left.text \markup \baca-bcp-left #2 #5            %! BACA_BCP_COMMAND
                                - \tweak bound-details.right.text \markup \baca-bcp-right #1 #5          %! BACA_BCP_COMMAND
                                \bacaStartTextSpanBCP                                                    %! BACA_BCP_COMMAND
                <BLANKLINE>
                                e'8
                                \bacaStopTextSpanBCP                                                     %! BACA_BCP_COMMAND
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                f'8
                                -\downbow                                                                %! BACA_BCP_COMMAND
                                \bacaStopTextSpanBCP                                                     %! BACA_BCP_COMMAND
                                - \abjad_solid_line_with_arrow                                           %! BACA_BCP_COMMAND
                                - \tweak bound-details.left.text \markup \baca-bcp-left #3 #5            %! BACA_BCP_COMMAND
                                \bacaStartTextSpanBCP                                                    %! BACA_BCP_COMMAND
                                [
                <BLANKLINE>
                                e'8
                                -\upbow                                                                  %! BACA_BCP_COMMAND
                                \bacaStopTextSpanBCP                                                     %! BACA_BCP_COMMAND
                                - \abjad_solid_line_with_arrow                                           %! BACA_BCP_COMMAND
                                - \tweak bound-details.left.text \markup \baca-bcp-left #4 #5            %! BACA_BCP_COMMAND
                                \bacaStartTextSpanBCP                                                    %! BACA_BCP_COMMAND
                <BLANKLINE>
                                f'8
                                -\downbow                                                                %! BACA_BCP_COMMAND
                                \bacaStopTextSpanBCP                                                     %! BACA_BCP_COMMAND
                                - \abjad_solid_line_with_arrow                                           %! BACA_BCP_COMMAND
                                - \tweak bound-details.left.text \markup \baca-bcp-left #3 #5            %! BACA_BCP_COMMAND
                                \bacaStartTextSpanBCP                                                    %! BACA_BCP_COMMAND
                <BLANKLINE>
                                e'8
                                -\upbow                                                                  %! BACA_BCP_COMMAND
                                \bacaStopTextSpanBCP                                                     %! BACA_BCP_COMMAND
                                ]
                                - \abjad_solid_line_with_arrow                                           %! BACA_BCP_COMMAND
                                - \tweak bound-details.left.text \markup \baca-bcp-left #4 #5            %! BACA_BCP_COMMAND
                                \bacaStartTextSpanBCP                                                    %! BACA_BCP_COMMAND
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                f'8
                                -\downbow                                                                %! BACA_BCP_COMMAND
                                \bacaStopTextSpanBCP                                                     %! BACA_BCP_COMMAND
                                - \abjad_solid_line_with_arrow                                           %! BACA_BCP_COMMAND
                                - \tweak bound-details.left.text \markup \baca-bcp-left #3 #5            %! BACA_BCP_COMMAND
                                \bacaStartTextSpanBCP                                                    %! BACA_BCP_COMMAND
                                [
                <BLANKLINE>
                                e'8
                                -\upbow                                                                  %! BACA_BCP_COMMAND
                                \bacaStopTextSpanBCP                                                     %! BACA_BCP_COMMAND
                                - \abjad_solid_line_with_arrow                                           %! BACA_BCP_COMMAND
                                - \tweak bound-details.left.text \markup \baca-bcp-left #4 #5            %! BACA_BCP_COMMAND
                                - \tweak bound-details.right.text \markup \baca-bcp-right #3 #5          %! BACA_BCP_COMMAND
                                \bacaStartTextSpanBCP                                                    %! BACA_BCP_COMMAND
                <BLANKLINE>
                                f'8
                                \bacaStopTextSpanBCP                                                     %! BACA_BCP_COMMAND
                                ]
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return self._bow_contact_points

    @property
    def final_spanner(self) -> typing.Optional[bool]:
        """
        Is true when command outputs dangling final spanner.
        """
        return self._final_spanner

    @property
    def helper(self) -> typing.Optional[typing.Callable]:
        """
        Gets BCP helper.
        """
        return self._helper

    @property
    def start_command(self) -> str:
        r"""
        Gets ``'\bacaStartTextSpanBCP'``.
        """
        return r'\bacaStartTextSpanBCP'

    @property
    def stop_command(self) -> str:
        r"""
        Gets ``'\bacaStopTextSpanBCP'``.
        """
        return r'\bacaStopTextSpanBCP'

    @property
    def tag(self) -> abjad.Tag:
        """
        Gets tag.

        ..  container:: example

            >>> baca.BCPCommand().tag
            Tag('BACA_BCP_COMMAND')

        """
        return super().tag

    @property
    def tweaks(self) -> typing.Tuple[abjad.LilyPondTweakManager, ...]:
        """
        Gets tweaks.
        """
        return self._tweaks

class ColorCommand(scoping.Command):
    r"""
    Color command.

    >>> from abjadext import rmakers

    ..  container:: example

        With music-maker:

        Colors leaves by default:

        >>> music_maker = baca.MusicMaker(
        ...     baca.color(),
        ...     baca.PitchFirstRhythmCommand(
        ...         rhythm_maker=baca.PitchFirstRhythmMaker(
        ...             talea=rmakers.Talea(
        ...                 counts=[5, 4, 4, 5, 4, 4, 4],
        ...                 denominator=32,
        ...                 ),
        ...             ),
        ...         ),
        ...     )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker('Voice 1', collections)
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            c'8
                            ~
                            [
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            c'32
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            d'8
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            bf'8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            fs''8
                            ~
                            [
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            fs''32
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e''8
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            ef''8
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            af''8
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            af''32
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            g''8
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            a'8
                            ~
                            [
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            a'32
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        With segment-maker:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.color(),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'8
                            [
            <BLANKLINE>
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            d''8
            <BLANKLINE>
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            f'8
            <BLANKLINE>
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            g'8
                            [
            <BLANKLINE>
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            f''8
            <BLANKLINE>
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            d''8
                            [
            <BLANKLINE>
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            f'8
            <BLANKLINE>
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            e''8
            <BLANKLINE>
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            f''8
                            [
            <BLANKLINE>
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'8
            <BLANKLINE>
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            d''8
                            ]
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        selector='baca.leaves()',
        ):
        assert selector is not None
        scoping.Command.__init__(self, selector=selector)

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        """
        Calls command on ``argument``.

        Returns colored selector result.
        """
        if argument is None:
            return
        argument = self.selector(argument)
        self.selector.color(argument)
        return argument

class ContainerCommand(scoping.Command):
    r"""
    Container command.

    ..  container:: example

        >>> baca.ContainerCommand()
        ContainerCommand(selector=baca.leaves())

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.container('ViolinI', selector=baca.leaves()[:2]),
        ...     baca.container('ViolinII', selector=baca.leaves()[2:]),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')

        >>> abjad.f(lilypond_file[abjad.Score], strict=89)
        \context Score = "Score"
        <<
            \context GlobalContext = "GlobalContext"
            <<
                \context GlobalSkips = "GlobalSkips"
                {
        <BLANKLINE>
                    % [GlobalSkips measure 1]                                                    %! SM4
                    \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                    \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                    s1 * 1/2
        <BLANKLINE>
                    % [GlobalSkips measure 2]                                                    %! SM4
                    \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                    \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                    s1 * 3/8
        <BLANKLINE>
                    % [GlobalSkips measure 3]                                                    %! SM4
                    \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                    \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                    s1 * 1/2
        <BLANKLINE>
                    % [GlobalSkips measure 4]                                                    %! SM4
                    \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                    \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                    s1 * 3/8
                    \baca_bar_line_visible                                                       %! SM5
                    \bar "|"                                                                     %! SM5
        <BLANKLINE>
                }
            >>
            \context MusicContext = "MusicContext"
            <<
                \context Staff = "MusicStaff"
                {
                    \context Voice = "MusicVoice"
                    {
                        {   %*% ViolinI
        <BLANKLINE>
                            % [MusicVoice measure 1]                                             %! SM4
                            e'2
        <BLANKLINE>
                            % [MusicVoice measure 2]                                             %! SM4
                            f'4.
                        }   %*% ViolinI
                        {   %*% ViolinII
        <BLANKLINE>
                            % [MusicVoice measure 3]                                             %! SM4
                            e'2
        <BLANKLINE>
                            % [MusicVoice measure 4]                                             %! SM4
                            f'4.
        <BLANKLINE>
                        }   %*% ViolinII
                    }
                }
            >>
        >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_identifier',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        identifier: str = None,
        selector: typings.Selector = 'baca.leaves()',
        ) -> None:
        scoping.Command.__init__(self, selector=selector)
        if identifier is not None:
            if not isinstance(identifier, str):
                message = f'identifier must be string (not {identifier!r}).'
                raise Exception(message)
        self._identifier = identifier
        self._tags: typing.List[abjad.Tag] = []

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Inserts ``selector`` output in container.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if not self.identifier:
            identifier = None
        elif self.identifier.startswith('%*%'):
            identifier = self.identifier
        else:
            identifier = f'%*% {self.identifier}'
        container = abjad.Container(identifier=identifier)
        components = Selection(argument).leaves().top()
        abjad.mutate(components).wrap(container)

    ### PUBLIC PROPERTIES ###

    @property
    def identifier(self) -> typing.Optional[str]:
        """
        Gets identifier.
        """
        return self._identifier

class GlobalFermataCommand(scoping.Command):
    """
    Global fermata command.

    ..  container:: example

        >>> baca.GlobalFermataCommand()
        GlobalFermataCommand(selector=baca.leaf(0))

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_description',
        )

    description_to_command = {
        'short': 'shortfermata',
        'fermata': 'fermata',
        'long': 'longfermata',
        'very_long': 'verylongfermata',
        }

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        description: str = None,
        selector: typings.Selector = 'baca.leaf(0)',
        ) -> None:
        scoping.Command.__init__(self, selector=selector)
        if description is not None:
            assert description in GlobalFermataCommand.description_to_command
        self._description = description

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Applies command to ``argument`` selector output.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if isinstance(self.description, str):
            command = self.description_to_command.get(self.description)
        else:
            command = 'fermata'
        for leaf in abjad.iterate(argument).leaves():
            assert isinstance(leaf, abjad.MultimeasureRest)
            string = f'scripts.u{command}'
            directive = abjad.Markup.musicglyph(string)
            directive = abjad.new(directive, direction=abjad.Up)
            abjad.attach(directive, leaf, tag='GFC1')
            strings = []
            string = r'\once \override'
            string += ' Score.MultiMeasureRest.transparent = ##t'
            strings.append(string)
            string = r'\once \override Score.TimeSignature.stencil = ##f'
            strings.append(string)
            literal = abjad.LilyPondLiteral(strings)
            abjad.attach(literal, leaf, tag='GFC2')
            abjad.attach(
                abjad.tags.FERMATA_MEASURE,
                leaf,
                tag=abjad.tags.FERMATA_MEASURE,
                )

    ### PUBLIC PROPERTIES ###

    @property
    def description(self) -> typing.Optional[str]:
        """
        Gets description.
        """
        return self._description

class IndicatorBundle(abjad.AbjadObject):
    """
    IndicatorBundle.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bookended_spanner_start',
        '_enchained',
        '_indicator',
        '_spanner_start',
        '_spanner_stop',
        )

    _publish_storage_format=True

    ### INITIALIZER ###

    def __init__(
        self,
        *arguments: typing.Any,
        bookended_spanner_start: typing.Any = None,
        enchained: bool = None,
        ) -> None:
        assert len(arguments) <= 3, repr(arguments)
        self._indicator = None
        self._spanner_start = None
        self._spanner_stop = None
        for argument in arguments:
            if argument is None:
                continue
            elif getattr(argument, 'spanner_start', False) is True:
                self._spanner_start = argument
            elif getattr(argument, 'spanner_stop', False) is True:
                self._spanner_stop = argument
            else:
                self._indicator = argument
        self._bookended_spanner_start = bookended_spanner_start
        if enchained is not None:
            enchained = bool(enchained)
        self._enchained = enchained

    ### SPECIAL METHODS ###

    def __iter__(self) -> typing.Iterator:
        """
        Iterates bundle.
        """
        return iter(self.indicators)

    def __len__(self) -> int:
        """
        Gets length.
        """
        return len(self.indicators)

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        class_ = type(self).__name__
        string = ', '.join([repr(_) for _ in self.indicators])
        return f'{class_}({string})'

    ### PUBLIC PROPERTIES ###

    @property
    def bookended_spanner_start(self) -> typing.Optional[typing.Any]:
        """
        Gets bookended start text span indicator.
        """
        return self._bookended_spanner_start

    @property
    def enchained(self) -> typing.Optional[bool]:
        """
        Is true when bundle contributes to enchained spanner.
        """
        return self._enchained

    @property
    def indicator(self) -> typing.Optional[typing.Any]:
        """
        Gets indicator.
        """
        return self._indicator

    @property
    def indicators(self) -> typing.List:
        """
        Gets indicators.
        """
        result: typing.List = []
        if self.spanner_stop:
            result.append(self.spanner_stop)
        if self.indicator:
            result.append(self.indicator)
        if self.spanner_start:
            result.append(self.spanner_start)
        return result

    @property
    def spanner_start(self) -> typing.Optional[typing.Any]:
        """
        Gets spanner start.
        """
        return self._spanner_start

    @property
    def spanner_stop(self) -> typing.Optional[typing.Any]:
        """
        Gets spanner stop.
        """
        return self._spanner_stop

    ### PUBLIC METHODS ###

    def compound(self) -> bool:
        """
        Is true when bundle has both indicator and spanner_start.
        """
        return bool(self.indicator) and bool(self.spanner_start)

    def indicator_only(self) -> bool:
        """
        Is true when bundle has indicator only.
        """
        if self.indicator and not self.spanner_start:
            return True
        return False

    def simple(self) -> bool:
        """
        Is true when bundle has indicator or spanner start but not both.
        """
        return len(self) == 1

    def spanner_start_only(self) -> bool:
        """
        Is true when bundle has spanner start only.
        """
        if not self.indicator and self.spanner_start:
            return True
        return False

    def with_indicator(self, indicator) -> 'IndicatorBundle':
        """
        Makes new bundle with indicator.

        ..  container:: example

            >>> bundle = baca.IndicatorBundle(
            ...     abjad.Dynamic('p'),
            ...     abjad.DynamicTrend('<'),
            ...     )

            >>> bundle.with_indicator(abjad.Dynamic('f'))
            IndicatorBundle(Dynamic('f'), DynamicTrend(shape='<'))

            >>> bundle.with_indicator(None)
            IndicatorBundle(DynamicTrend(shape='<'))

        """
        if indicator is None:
            return type(self)(self.spanner_start)
        return type(self)(
            self.spanner_stop,
            indicator,
            self.spanner_start,
            bookended_spanner_start=self.bookended_spanner_start,
            enchained=self.enchained,
            )

    def with_spanner_start(self, spanner_start) -> 'IndicatorBundle':
        """
        Makes new bundle with spanner start.

        ..  container:: example

            >>> bundle = baca.IndicatorBundle(
            ...     abjad.Dynamic('p'),
            ...     abjad.DynamicTrend('<'),
            ...     )

            >>> bundle.with_spanner_start(abjad.DynamicTrend('>'))
            IndicatorBundle(Dynamic('p'), DynamicTrend(shape='>'))

            >>> bundle.with_spanner_start(None)
            IndicatorBundle(Dynamic('p'))

        ..  container:: example

            >>> bundle = baca.IndicatorBundle(
            ...     abjad.StopTextSpan(),
            ...     abjad.StartTextSpan(left_text=abjad.Markup('pont.')),
            ...     )

            >>> bundle.with_spanner_start(
            ...     abjad.StartTextSpan(command=r'\startTextSpanOne')
            ...     )
            IndicatorBundle(StopTextSpan(command='\\stopTextSpan'), StartTextSpan(command='\\startTextSpanOne', concat_hspace_left=0.5))

            >>> bundle.with_spanner_start(None)
            IndicatorBundle(StopTextSpan(command='\\stopTextSpan'))

        """
        if (spanner_start is not None and
            getattr(spanner_start, 'spanner_start', False) is not True):
            raise Exception(spanner_start)
        return type(self)(
            self.spanner_stop,
            self.indicator,
            spanner_start,
            bookended_spanner_start=self.bookended_spanner_start,
            enchained=self.enchained,
            )

    def with_spanner_stop(self, spanner_stop) -> 'IndicatorBundle':
        """
        Makes new bundle with spanner stop.

        ..  container:: example

            >>> bundle = baca.IndicatorBundle(
            ...     abjad.StopTextSpan(),
            ...     abjad.StartTextSpan(left_text=abjad.Markup('pont.')),
            ...     )

            >>> string = r'\stopTextSpanOne'
            >>> bundle.with_spanner_stop(abjad.StopTextSpan(command=string))
            IndicatorBundle(StopTextSpan(command='\\stopTextSpanOne'), StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5, left_text=Markup(contents=['pont.'])))

            >>> bundle.with_spanner_stop(None)
            IndicatorBundle(StartTextSpan(command='\\startTextSpan', concat_hspace_left=0.5, left_text=Markup(contents=['pont.'])))

        """
        if (spanner_stop is not None and
            getattr(spanner_stop, 'spanner_stop', False) is not True):
            raise Exception(spanner_stop)
        return type(self)(
            spanner_stop,
            self.indicator,
            self.spanner_start,
            bookended_spanner_start=self.bookended_spanner_start,
            enchained=self.enchained,
            )

class IndicatorCommand(scoping.Command):
    r"""
    Indicator command.

    >>> from abjadext import rmakers

    ..  container:: example

        With music-maker:

        >>> music_maker = baca.MusicMaker(
        ...     baca.IndicatorCommand(indicators=[abjad.Fermata()]),
        ...     baca.PitchFirstRhythmCommand(
        ...         rhythm_maker=baca.PitchFirstRhythmMaker(
        ...             talea=rmakers.Talea(
        ...                 counts=[5, 4, 4, 5, 4, 4, 4],
        ...                 denominator=32,
        ...                 ),
        ...             ),
        ...         ),
        ...     )

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker('Voice 1', collections)
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            c'8
                            \fermata                                                                 %! IC
                            ~
                            [
                            c'32
                            d'8
                            \fermata                                                                 %! IC
                            bf'8
                            \fermata                                                                 %! IC
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''8
                            \fermata                                                                 %! IC
                            ~
                            [
                            fs''32
                            e''8
                            \fermata                                                                 %! IC
                            ef''8
                            \fermata                                                                 %! IC
                            af''8
                            \fermata                                                                 %! IC
                            ~
                            af''32
                            g''8
                            \fermata                                                                 %! IC
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'8
                            \fermata                                                                 %! IC
                            ~
                            [
                            a'32
                            ]
                        }
                    }
                }
            >>

    ..  container:: example

        With segment-maker:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.IndicatorCommand(indicators=[abjad.Fermata()]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            e'8
                            \fermata                                                                 %! IC
                            [
            <BLANKLINE>
                            d''8
                            \fermata                                                                 %! IC
            <BLANKLINE>
                            f'8
                            \fermata                                                                 %! IC
            <BLANKLINE>
                            e''8
                            \fermata                                                                 %! IC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            \fermata                                                                 %! IC
                            [
            <BLANKLINE>
                            f''8
                            \fermata                                                                 %! IC
            <BLANKLINE>
                            e'8
                            \fermata                                                                 %! IC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            \fermata                                                                 %! IC
                            [
            <BLANKLINE>
                            f'8
                            \fermata                                                                 %! IC
            <BLANKLINE>
                            e''8
                            \fermata                                                                 %! IC
            <BLANKLINE>
                            g'8
                            \fermata                                                                 %! IC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            \fermata                                                                 %! IC
                            [
            <BLANKLINE>
                            e'8
                            \fermata                                                                 %! IC
            <BLANKLINE>
                            d''8
                            \fermata                                                                 %! IC
                            ]
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context',
        '_indicators',
        '_redundant',
        '_tags',
        '_tweaks',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *tweaks: abjad.LilyPondTweakManager,
        context: str = None,
        deactivate: bool = None,
        indicators: typing.List[typing.Any] = None,
        redundant: bool = None,
        selector: typings.Selector = 'baca.pheads()',
        tags: typing.List[abjad.Tag] = None,
        ) -> None:
        scoping.Command.__init__(
            self,
            deactivate=deactivate,
            selector=selector,
            )
        if context is not None:
            assert isinstance(context, str), repr(context)
        self._context = context
        indicators_ = None
        if indicators is not None:
            if isinstance(indicators, collections.Iterable):
                indicators_ = abjad.CyclicTuple(indicators)
            else:
                indicators_ = abjad.CyclicTuple([indicators])
        self._indicators = indicators_
        if redundant is not None:
            redundant = bool(redundant)
        self._redundant = redundant
        self._validate_tweaks(tweaks)
        self._tweaks = tweaks
        tags = tags or []
        assert self._validate_tags(tags), repr(tags)
        self._tags = tags

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        # TODO: externalize late import
        from .SegmentMaker import SegmentMaker
        if argument is None:
            return
        if self.indicators is None:
            return
        if self.redundant is True:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        for i, leaf in enumerate(_select(argument).leaves()):
            indicators = self.indicators[i]
            indicators = self._token_to_indicators(indicators)
            for indicator in indicators:
                self._apply_tweaks(indicator)
                reapplied = self._remove_reapplied_wrappers(leaf, indicator)
                wrapper = abjad.attach(
                    indicator,
                    leaf,
                    context=self.context,
                    deactivate=self.deactivate,
                    tag=self.tag.prepend('IC'),
                    wrapper=True,
                    )
                if indicator == reapplied:
                    if (isinstance(indicator, abjad.Dynamic) and
                        indicator.sforzando):
                        status = 'explicit'
                    else:
                        status = 'redundant'
                    SegmentMaker._treat_persistent_wrapper(
                        self.runtime['manifests'],
                        wrapper,
                        status,
                        )

    ### PRIVATE METHODS ###

    @staticmethod
    def _token_to_indicators(token):
        result = []
        if not isinstance(token, (tuple, list)):
            token = [token]
        for item in token:
            if item is None:
                continue
            result.append(item)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> typing.Optional[str]:
        """
        Gets context name.
        """
        return self._context

    @property
    def indicators(self) -> typing.Optional[abjad.CyclicTuple]:
        r"""
        Gets indicators.

        ..  container:: example

            Attaches fermata to head of every pitched logical tie:

            >>> music_maker = baca.MusicMaker(
            ...     baca.IndicatorCommand(indicators=[abjad.Fermata()]),
            ...     baca.PitchFirstRhythmCommand(
            ...         rhythm_maker=baca.PitchFirstRhythmMaker(
            ...             talea=rmakers.Talea(
            ...                 counts=[5, 4, 4, 5, 4, 4, 4],
            ...                 denominator=32,
            ...                 ),
            ...             ),
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'8
                                \fermata                                                                 %! IC
                                ~
                                [
                                c'32
                                d'8
                                \fermata                                                                 %! IC
                                bf'8
                                \fermata                                                                 %! IC
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''8
                                \fermata                                                                 %! IC
                                ~
                                [
                                fs''32
                                e''8
                                \fermata                                                                 %! IC
                                ef''8
                                \fermata                                                                 %! IC
                                af''8
                                \fermata                                                                 %! IC
                                ~
                                af''32
                                g''8
                                \fermata                                                                 %! IC
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'8
                                \fermata                                                                 %! IC
                                ~
                                [
                                a'32
                                ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Patterns fermatas:

            >>> music_maker = baca.MusicMaker(
            ...     baca.IndicatorCommand(
            ...         indicators=[
            ...             abjad.Fermata(), None, None,
            ...             abjad.Fermata(), None, None,
            ...             abjad.Fermata(), None,
            ...             ],
            ...         ),
            ...     baca.PitchFirstRhythmCommand(
            ...         rhythm_maker=baca.PitchFirstRhythmMaker(
            ...             talea=rmakers.Talea(
            ...                 counts=[5, 4, 4, 5, 4, 4, 4],
            ...                 denominator=32,
            ...                 ),
            ...             ),
            ...         ),
            ...     )

            >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
            >>> contribution = music_maker('Voice 1', collections)
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff
                <<
                    \context Voice = "Voice 1"
                    {
                        \voiceOne
                        {
                            \scaleDurations #'(1 . 1) {
                                c'8
                                \fermata                                                                 %! IC
                                ~
                                [
                                c'32
                                d'8
                                bf'8
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''8
                                \fermata                                                                 %! IC
                                ~
                                [
                                fs''32
                                e''8
                                ef''8
                                af''8
                                \fermata                                                                 %! IC
                                ~
                                af''32
                                g''8
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'8
                                \fermata                                                                 %! IC
                                ~
                                [
                                a'32
                                ]
                            }
                        }
                    }
                >>

        """
        return self._indicators

    @property
    def redundant(self) -> typing.Optional[bool]:
        """
        Is true when command is redundant.
        """
        return self._redundant

    @property
    def tweaks(self) -> typing.Tuple[abjad.LilyPondTweakManager, ...]:
        """
        Gets tweaks.
        """
        return self._tweaks

class InstrumentChangeCommand(IndicatorCommand):
    """
    Instrument change command.
    """

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Inserts ``selector`` output in container and sets part assignment.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        if self.indicators is None:
            return
        first_leaf = abjad.inspect(argument).get_leaf(0)
        if first_leaf is not None:
            parentage = abjad.inspect(first_leaf).get_parentage()
            staff = parentage.get_first(abjad.Staff)
            instrument = self.indicators[0]
            assert isinstance(instrument, abjad.Instrument), repr(instrument)
            if not self.runtime['score_template'].allows_instrument(
                staff.name,
                instrument,
                ):
                message = f'{staff.name} does not allow instrument:\n'
                message += f'  {instrument}'
                raise Exception(message)
        super(InstrumentChangeCommand, self).__call__(argument)

class LabelCommand(scoping.Command):
    r"""
    Label command.

    ..  container:: example

        Labels pitch names:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.label(abjad.label().with_pitches(locale='us')),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            e'8
                            ^ \markup { E4 }
                            [
            <BLANKLINE>
                            d''8
                            ^ \markup { D5 }
            <BLANKLINE>
                            f'8
                            ^ \markup { F4 }
            <BLANKLINE>
                            e''8
                            ^ \markup { E5 }
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            ^ \markup { G4 }
                            [
            <BLANKLINE>
                            f''8
                            ^ \markup { F5 }
            <BLANKLINE>
                            e'8
                            ^ \markup { E4 }
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            ^ \markup { D5 }
                            [
            <BLANKLINE>
                            f'8
                            ^ \markup { F4 }
            <BLANKLINE>
                            e''8
                            ^ \markup { E5 }
            <BLANKLINE>
                            g'8
                            ^ \markup { G4 }
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            ^ \markup { F5 }
                            [
            <BLANKLINE>
                            e'8
                            ^ \markup { E4 }
            <BLANKLINE>
                            d''8
                            ^ \markup { D5 }
                            ]
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Labels pitch names in tuplet 0:

        >>> music_maker = baca.MusicMaker()

        >>> collections = [[0, 2, 10], [18, 16, 15, 20, 19], [9]]
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     collections,
        ...     baca.label(
        ...         abjad.label().with_pitches(locale='us'),
        ...         selector=baca.tuplet(0),
        ...         ),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \scaleDurations #'(1 . 1) {
                            c'16
                            ^ \markup { C4 }
                            [
                            d'16
                            ^ \markup { D4 }
                            bf'16
                            ^ \markup { Bb4 }
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            e''16
                            ef''16
                            af''16
                            g''16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
                        }
                    }
                }
            >>

    """

    ### CLASS VARIABLES ##

    __slots__ = (
        '_expression',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        expression=None,
        selector='baca.leaves()',
        ):
        scoping.Command.__init__(self, selector=selector)
        if expression is not None:
            assert isinstance(expression, abjad.Expression)
        self._expression = expression

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        """
        Calls command on ``argument``.

        Returns none.
        """
        if argument is None:
            return
        if self.expression is None:
            return
        if self.selector:
            argument = self.selector(argument)
        self.expression(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def expression(self):
        """
        Gets expression.

        Defaults to none.

        Set to label expression or none.

        Returns label expression or none.
        """
        return self._expression

class MetronomeMarkCommand(scoping.Command):
    """
    Metronome mark command.

    ..  container:: example

        >>> baca.MetronomeMarkCommand()
        MetronomeMarkCommand(selector=baca.leaf(0), tags=[])

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_key',
        '_redundant',
        '_tags',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        deactivate: bool = None,
        key: typing.Union[
            str,
            indicators.Accelerando,
            indicators.Ritardando] = None,
        redundant: bool = None,
        selector: typings.Selector = 'baca.leaf(0)',
        tags: typing.List[abjad.Tag] = None,
        ) -> None:
        scoping.Command.__init__(
            self,
            deactivate=deactivate,
            selector=selector,
            )
        prototype = (str, indicators.Accelerando, indicators.Ritardando)
        if key is not None:
            assert isinstance(key, prototype), repr(key)
        self._key = key
        if redundant is not None:
            redundant = bool(redundant)
        self._redundant = redundant
        tags = tags or []
        assert self._validate_tags(tags), repr(tags)
        self._tags = tags

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Applies command to result of selector called on ``argument``.
        """
        from .SegmentMaker import SegmentMaker
        if argument is None:
            return
        if self.key is None:
            return
        if self.redundant is True:
            return
        if isinstance(self.key, str) and self.runtime['manifests'] is not None:
            metronome_marks = self.runtime['manifests']['abjad.MetronomeMark']
            indicator = metronome_marks.get(self.key)
            if indicator is None:
                raise Exception(f'can not find metronome mark {self.key!r}.')
        else:
            indicator = self.key
        if self.selector is not None:
            argument = self.selector(argument)
        if not argument:
            return
        leaf = Selection(argument).leaf(0)
        reapplied = self._remove_reapplied_wrappers(leaf, indicator)
        wrapper = abjad.attach(
            indicator,
            leaf,
            deactivate=self.deactivate,
            tag=self.tag,
            wrapper=True,
            )
        if indicator == reapplied:
            SegmentMaker._treat_persistent_wrapper(
                self.runtime['manifests'],
                wrapper,
                'redundant',
                )

    ### PUBLIC PROPERTIES ###

    @property
    def key(self) -> typing.Optional[typing.Union[str,
    indicators.Accelerando, indicators.Ritardando]]:
        """
        Gets metronome mark key.
        """
        return self._key

    @property
    def redundant(self) -> typing.Optional[bool]:
        """
        Is true when command is redundant.
        """
        return self._redundant

class PartAssignmentCommand(scoping.Command):
    """
    Part assignment command.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_part_assignment',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        part_assignment: abjad.PartAssignment = None,
        selector: typings.Selector = 'baca.leaves()',
        ) -> None:
        scoping.Command.__init__(self, selector=selector)
        if part_assignment is not None:
            if not isinstance(part_assignment, abjad.PartAssignment):
                message = 'part_assignment must be part assignment'
                message += f' (not {part_assignment!r}).'
                raise Exception(message)
        self._part_assignment = part_assignment

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Inserts ``selector`` output in container and sets part assignment.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        first_leaf = abjad.inspect(argument).get_leaf(0)
        if first_leaf is None:
            return
        parentage = abjad.inspect(first_leaf).get_parentage()
        voice = parentage.get_first(abjad.Voice)
        if voice is not None and self.part_assignment is not None:
            if not self.runtime['score_template'].allows_part_assignment(
                voice.name,
                self.part_assignment,
                ):
                message = f'{voice.name} does not allow'
                message += f' {self.part_assignment.section} part assignment:'
                message += f'\n  {self.part_assignment}'
                raise Exception(message)
        identifier = f'%*% {self.part_assignment!s}'
        container = abjad.Container(identifier=identifier)
        components = Selection(argument).leaves().top()
        abjad.mutate(components).wrap(container)

    ### PUBLIC PROPERTIES ###

    @property
    def part_assignment(self) -> typing.Optional[abjad.PartAssignment]:
        """
        Gets part assignment.
        """
        return self._part_assignment

class PiecewiseIndicatorCommand(scoping.Command):
    """
    Piecewise indicator command.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_bookend',
        '_bundles',
        '_final_piece_spanner',
        '_leak',
        '_piece_selector',
        '_remove_length_1_spanner_start',
        '_right_broken',
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        bookend: typing.Union[bool, int] = None,
        bundles: typing.List[IndicatorBundle] = None,
        final_piece_spanner: typing.Any = None,
        leak: bool = None,
        piece_selector: typings.Selector = 'baca.leaves()',
        remove_length_1_spanner_start: bool = None,
        right_broken: typing.Any = None,
        selector: typings.Selector = 'baca.leaves()',
        ) -> None:
        # for selector evaluation
        import baca
        scoping.Command.__init__(self, selector=selector)
        if bookend is not None:
            assert isinstance(bookend, (int, bool)), repr(bookend)
        self._bookend = bookend
        bundles_ = None
        if bundles is not None:
            bundles_ = abjad.CyclicTuple(bundles)
        self._bundles = bundles_
        if final_piece_spanner not in (None, False):
            assert getattr(final_piece_spanner, 'spanner_start', False)
        self._final_piece_spanner = final_piece_spanner
        if leak is not None:
            leak = bool(leak)
        self._leak = leak
        if isinstance(piece_selector, str):
            piece_selector = eval(piece_selector)
        if piece_selector is not None:
            assert isinstance(piece_selector, abjad.Expression), repr(
                piece_selector)
        self._piece_selector = piece_selector
        if remove_length_1_spanner_start is not None:
            remove_length_1_spanner_start = bool(remove_length_1_spanner_start)
        self._remove_length_1_spanner_start = remove_length_1_spanner_start
        self._right_broken = right_broken
        self._tags: typing.List[abjad.Tag] = []

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if not self.bundles:
            return
        if self.selector is not None:
            assert not isinstance(self.selector, str)
            argument = self.selector(argument)
        if self.piece_selector is not None:
            assert not isinstance(self.piece_selector, str)
            pieces = self.piece_selector(argument)
        else:
            pieces = argument
        assert pieces is not None
        piece_count = len(pieces)
        assert 0 < piece_count, repr(piece_count)
        if self.bookend in (False, None):
            bookend_pattern = abjad.Pattern()
        elif self.bookend is True:
            bookend_pattern = abjad.index([0], 1)
        else:
            assert isinstance(self.bookend, int), repr(self.bookend)
            bookend_pattern = abjad.index([self.bookend], period=piece_count)
        for i, piece in enumerate(pieces):
            start_leaf = Selection(piece).leaf(0)
            stop_leaf = Selection(piece).leaf(-1)
            if i == 0:
                is_first_piece = True
            else:
                is_first_piece = False
            if i == piece_count - 1:
                is_final_piece = True
            else:
                is_final_piece = False
            if is_final_piece and self.right_broken:
                bundle = IndicatorBundle(self.right_broken)
                self._attach_indicators(
                    bundle,
                    stop_leaf,
                    tag=str(abjad.tags.HIDE_TO_JOIN_BROKEN_SPANNERS),
                    )
            if (bookend_pattern.matches_index(i, piece_count) and
                1 < len(piece)):
                should_bookend = True
            else:
                should_bookend = False
            if is_final_piece and self.right_broken:
                should_bookend = False
            bundle = self.bundles[i]
            if should_bookend and bundle.bookended_spanner_start:
                bundle = bundle.with_spanner_start(
                    bundle.bookended_spanner_start
                    )
            if (len(piece) == 1 and
                bundle.compound() and
                self.remove_length_1_spanner_start):
                bundle = bundle.with_spanner_start(None)
            if is_final_piece and bundle.compound():
                if self.final_piece_spanner:
                    bundle = bundle.with_spanner_start(
                        self.final_piece_spanner)
                elif self.final_piece_spanner is False:
                    bundle = bundle.with_spanner_start(None)
            if is_first_piece:
                bundle = bundle.with_spanner_stop(None)
            self._attach_indicators(
                bundle,
                start_leaf,
                tag='PIC',
                )
            next_bundle = self.bundles[i + 1]
            if should_bookend:
                if bundle.bookended_spanner_start is not None:
                    next_bundle = next_bundle.with_spanner_start(None)
                if next_bundle.compound():
                    next_bundle = next_bundle.with_spanner_start(None)
                self._attach_indicators(
                    next_bundle,
                    stop_leaf,
                    tag='PIC',
                    )
            elif is_final_piece and next_bundle.spanner_stop:
                spanner_stop = next_bundle.spanner_stop
                if self.leak:
                    spanner_stop = abjad.new(spanner_stop, leak=True)
                bundle = IndicatorBundle(spanner_stop)
                self._attach_indicators(
                    bundle,
                    stop_leaf,
                    tag='PIC',
                    )

    ### PRIVATE METHODS ###

    def _attach_indicators(
        self,
        bundle,
        leaf,
        tag=None,
        ):
        # TODO: factor out late import
        from .SegmentMaker import SegmentMaker
        assert isinstance(tag, str), repr(tag)
        for indicator in bundle:
            reapplied = scoping.Command._remove_reapplied_wrappers(
                leaf,
                indicator,
                )
            wrapper = abjad.attach(
                indicator,
                leaf,
                tag=self.tag.prepend(tag),
                wrapper=True,
                )
            if indicator == reapplied:
                if (isinstance(indicator, abjad.Dynamic) and
                    indicator.sforzando):
                    status = 'explicit'
                else:
                    status = 'redundant'
                SegmentMaker._treat_persistent_wrapper(
                    self.runtime['manifests'],
                    wrapper,
                    status,
                    )

    ### PUBLIC PROPERTIES ###

    @property
    def bookend(self) -> typing.Optional[typing.Union[bool, int]]:
        """
        Gets bookend token.

        Command attaches indicator to first leaf in each group of
        selector output when ``bookend`` is false.

        Command attaches indicator to both first leaf and last
        leaf in each group of selector output when ``bookend`` is true.

        When ``bookend`` equals integer ``n``, command attaches indicator to
        first leaf and last leaf in group ``n`` of selector output and attaches
        indicator to only first leaf in other groups of selector output.
        """
        return self._bookend

    @property
    def bundles(self) -> typing.Optional[abjad.CyclicTuple]:
        """
        Gets bundles.
        """
        return self._bundles

    @property
    def final_piece_spanner(self) -> typing.Optional[typing.Any]:
        """
        Gets last piece spanner start.
        """
        return self._final_piece_spanner

    @property
    def leak(self) -> typing.Optional[bool]:
        """
        Is true when command leaks final spanner stop.
        """
        return self._leak

    @property
    def piece_selector(self) -> typing.Optional[abjad.Expression]:
        """
        Gets piece selector.
        """
        return self._piece_selector

    @property
    def remove_length_1_spanner_start(self) -> typing.Optional[bool]:
        """
        Is true when command removes spanner start from length-1 pieces.
        """
        return self._remove_length_1_spanner_start

    @property
    def right_broken(self) -> typing.Optional[typing.Any]:
        """
        Gets right-broken indicator.
        """
        return self._right_broken

    @property
    def selector(self) -> typing.Optional[abjad.Expression]:
        """
        Gets (first-order) selector.
        """
        return self._selector

class VoltaCommand(scoping.Command):
    """
    Volta command.

    ..  container:: example

        >>> baca.VoltaCommand()
        VoltaCommand()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Applies command to result of selector called on ``argument``.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        leaves = Selection(argument).leaves()
        container = abjad.Container()
        abjad.mutate(leaves).wrap(container)
        abjad.attach(abjad.Repeat(), container)

### FACTORY FUNCTIONS ###

def bcps(
    *tweaks: abjad.LilyPondTweakManager,
    bcps: typing.Iterable[typing.Tuple[int, int]] = None,
    final_spanner: bool = None,
    helper: typing.Callable = None,
    selector: typings.Selector = 'baca.leaves()',
    ) -> BCPCommand:
    """
    Makes bow contact points.
    """
    if final_spanner is not None:
        final_spanner = bool(final_spanner)
    return BCPCommand(
        *tweaks,
        bcps=bcps,
        final_spanner=final_spanner,
        helper=helper,
        selector=selector,
        )

def volta(
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> VoltaCommand:
    r"""
    Makes volta container and extends container with ``selector`` output.

    ..  container:: example

        Wraps stage 1 (global skips 1 and 2) in volta container:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.RhythmCommand(
        ...         rhythm_maker=rmakers.TaleaRhythmMaker(
        ...             talea=rmakers.Talea(
        ...                 counts=[1, 1, 1, -1],
        ...                 denominator=8,
        ...                 ),
        ...             ),
        ...         ),
        ...     )

        >>> maker(
        ...     'GlobalSkips',
        ...     baca.volta(selector=baca.skips()[1:3]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
                        \repeat volta 2
                        {
            <BLANKLINE>
                            % [GlobalSkips measure 2]                                                %! SM4
                            \time 3/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color #'blue                                        %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
            <BLANKLINE>
                            % [GlobalSkips measure 3]                                                %! SM4
                            \time 4/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color #'blue                                        %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                        }
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            r8
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            e''8
                            [
            <BLANKLINE>
                            g'8
            <BLANKLINE>
                            f''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            r8
            <BLANKLINE>
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            r8
            <BLANKLINE>
                            e''8
                            [
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Wraps stage 2 global skips in volta container:

        >>> maker = baca.SegmentMaker(
        ...     measures_per_stage=[1, 2, 1],
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     ('MusicVoice', (1, 3)),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.RhythmCommand(
        ...         rhythm_maker=rmakers.TaleaRhythmMaker(
        ...             talea=rmakers.Talea(
        ...                 counts=[1, 1, 1, -1],
        ...                 denominator=8,
        ...                 ),
        ...             ),
        ...         ),
        ...     )

        >>> maker(
        ...     ('GlobalSkips', 2),
        ...     baca.volta(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
                        \repeat volta 2
                        {
            <BLANKLINE>
                            % [GlobalSkips measure 2]                                                %! SM4
                            \time 3/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color #'blue                                        %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
            <BLANKLINE>
                            % [GlobalSkips measure 3]                                                %! SM4
                            \time 4/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \baca_time_signature_color #'blue                                        %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                        }
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            r8
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            e''8
                            [
            <BLANKLINE>
                            g'8
            <BLANKLINE>
                            f''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            r8
            <BLANKLINE>
                            e'8
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            r8
            <BLANKLINE>
                            e''8
                            [
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    return VoltaCommand(selector=selector)

### FACTORY FUNCTIONS ###

def color(*, selector: typings.Selector = 'baca.leaves()') -> ColorCommand:
    r"""
    Colors leaves.

    ..  container:: example

        Colors all leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.color(),
        ...     baca.flags(),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            \once \override Dots.color = #red
                            \once \override Rest.color = #red
                            r8
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            c'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            d'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            bf'4
                            ~
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            bf'16
                            \once \override Dots.color = #blue
                            \once \override Rest.color = #blue
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            fs''16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            e''16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            ef''4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            ef''16
                            \once \override Dots.color = #red
                            \once \override Rest.color = #red
                            r16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            af''16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            g''16
                        }
                        \times 4/5 {
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            a'16
                            \once \override Dots.color = #red
                            \once \override Rest.color = #red
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Colors leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.color(selector=baca.tuplets()[1:2].leaves()),
        ...     baca.flags(),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            d'16
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            fs''16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            e''16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            ef''4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            ef''16
                            \once \override Dots.color = #red
                            \once \override Rest.color = #red
                            r16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            af''16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            g''16
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    """
    return ColorCommand(selector=selector)

def container(
    identifier: str = None,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> ContainerCommand:
    r"""
    Makes container with ``identifier`` and extends container with
    ``selector`` output.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.container('ViolinI', selector=baca.leaves()[:2]),
        ...     baca.container('ViolinII', selector=baca.leaves()[2:]),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')

        >>> abjad.f(lilypond_file[abjad.Score], strict=89)
        \context Score = "Score"
        <<
            \context GlobalContext = "GlobalContext"
            <<
                \context GlobalSkips = "GlobalSkips"
                {
        <BLANKLINE>
                    % [GlobalSkips measure 1]                                                    %! SM4
                    \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                    \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                    s1 * 1/2
        <BLANKLINE>
                    % [GlobalSkips measure 2]                                                    %! SM4
                    \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                    \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                    s1 * 3/8
        <BLANKLINE>
                    % [GlobalSkips measure 3]                                                    %! SM4
                    \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                    \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                    s1 * 1/2
        <BLANKLINE>
                    % [GlobalSkips measure 4]                                                    %! SM4
                    \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                    \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                    s1 * 3/8
                    \baca_bar_line_visible                                                       %! SM5
                    \bar "|"                                                                     %! SM5
        <BLANKLINE>
                }
            >>
            \context MusicContext = "MusicContext"
            <<
                \context Staff = "MusicStaff"
                {
                    \context Voice = "MusicVoice"
                    {
                        {   %*% ViolinI
        <BLANKLINE>
                            % [MusicVoice measure 1]                                             %! SM4
                            e'2
        <BLANKLINE>
                            % [MusicVoice measure 2]                                             %! SM4
                            f'4.
                        }   %*% ViolinI
                        {   %*% ViolinII
        <BLANKLINE>
                            % [MusicVoice measure 3]                                             %! SM4
                            e'2
        <BLANKLINE>
                            % [MusicVoice measure 4]                                             %! SM4
                            f'4.
        <BLANKLINE>
                        }   %*% ViolinII
                    }
                }
            >>
        >>

    """
    if identifier is not None:
        if not isinstance(identifier, str):
            message = f'identifier must be string (not {identifier!r}).'
            raise Exception(message)
    return ContainerCommand(
        identifier=identifier,
        selector=selector,
        )

def global_fermata(
    description: str = None,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> GlobalFermataCommand:
    """
    Attaches global fermata.
    """
    return GlobalFermataCommand(
        description=description,
        selector=selector,
        )

def instrument(
    instrument: abjad.Instrument,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> InstrumentChangeCommand:
    """
    Makes instrument change command.
    """
    if not isinstance(instrument, abjad.Instrument):
        message = f'instrument must be instrument (not {instrument!r}).'
        raise Exception(message)
    return InstrumentChangeCommand(
        indicators=[instrument],
        selector=selector,
        )

def label(
    expression: abjad.Expression,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> LabelCommand:
    r"""
    Labels ``selector`` output with label ``expression``.

    ..  container:: example

        Labels pitch names:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.label(abjad.label().with_pitches(locale='us')),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            ^ \markup { C4 }
                            [
                            d'16
                            ^ \markup { D4 }
                            ]
                            bf'4
                            ^ \markup { Bb4 }
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            ^ \markup { "F#5" }
                            [
                            e''16
                            ^ \markup { E5 }
                            ]
                            ef''4
                            ^ \markup { Eb5 }
                            ~
                            ef''16
                            r16
                            af''16
                            ^ \markup { Ab5 }
                            [
                            g''16
                            ^ \markup { G5 }
                            ]
                        }
                        \times 4/5 {
                            a'16
                            ^ \markup { A4 }
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Labels pitch names in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.label(
        ...         abjad.label().with_pitches(locale='us'),
        ...         selector=baca.tuplet(1),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            ^ \markup { "F#5" }
                            [
                            e''16
                            ^ \markup { E5 }
                            ]
                            ef''4
                            ^ \markup { Eb5 }
                            ~
                            ef''16
                            r16
                            af''16
                            ^ \markup { Ab5 }
                            [
                            g''16
                            ^ \markup { G5 }
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    """
    return LabelCommand(expression=expression, selector=selector)

def metronome_mark(
    key: str,
    *,
    redundant: bool = None,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> typing.Optional[MetronomeMarkCommand]:
    """
    Attaches metronome mark matching ``key`` metronome mark manifest.
    """
    if redundant is True:
        return None
    return MetronomeMarkCommand(
        key=key,
        redundant=redundant,
        selector=selector,
        )

def parts(
    part_assignment: abjad.PartAssignment,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> PartAssignmentCommand:
    r"""
    Inserts ``selector`` output in container and sets part assignment.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'ViolinMusicVoice',
        ...     baca.make_notes(),
        ...     baca.parts(abjad.PartAssignment('Violin')),
        ...     baca.pitch('E4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        >>> abjad.f(lilypond_file[abjad.Score], strict=89)
        \context Score = "Score"
        <<
            \context GlobalContext = "GlobalContext"
            <<
                \context GlobalSkips = "GlobalSkips"
                {
        <BLANKLINE>
                    % [GlobalSkips measure 1]                                                    %! SM4
                    \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                    \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                    s1 * 1/2
        <BLANKLINE>
                    % [GlobalSkips measure 2]                                                    %! SM4
                    \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                    \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                    s1 * 3/8
        <BLANKLINE>
                    % [GlobalSkips measure 3]                                                    %! SM4
                    \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                    \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                    s1 * 1/2
        <BLANKLINE>
                    % [GlobalSkips measure 4]                                                    %! SM4
                    \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                    \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                    s1 * 3/8
                    \baca_bar_line_visible                                                       %! SM5
                    \bar "|"                                                                     %! SM5
        <BLANKLINE>
                }
            >>
            \context MusicContext = "MusicContext"
            <<
                \context StringSectionStaffGroup = "String Section Staff Group"
                <<
                    \tag Violin                                                                  %! ST4
                    \context ViolinMusicStaff = "ViolinMusicStaff"
                    {
                        \context ViolinMusicVoice = "ViolinMusicVoice"
                        {
                            {   %*% PartAssignment('Violin')
        <BLANKLINE>
                                % [ViolinMusicVoice measure 1]                                   %! SM4
                                \clef "treble"                                                   %! SM8:DEFAULT_CLEF:ST3
                                \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                            %@% \override ViolinMusicStaff.Clef.color = ##f                      %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                \set ViolinMusicStaff.forceClef = ##t                            %! SM8:DEFAULT_CLEF:SM33:ST3
                                e'2
                                ^ \markup {                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \with-color                                                  %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        #(x11-color 'DarkViolet)                                 %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        (Violin)                                                 %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    }                                                            %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)     %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
        <BLANKLINE>
                                % [ViolinMusicVoice measure 2]                                   %! SM4
                                e'4.
        <BLANKLINE>
                                % [ViolinMusicVoice measure 3]                                   %! SM4
                                e'2
        <BLANKLINE>
                                % [ViolinMusicVoice measure 4]                                   %! SM4
                                e'4.
        <BLANKLINE>
                            }   %*% PartAssignment('Violin')
                        }
                    }
                    \tag Viola                                                                   %! ST4
                    \context ViolaMusicStaff = "ViolaMusicStaff"
                    {
                        \context ViolaMusicVoice = "ViolaMusicVoice"
                        {
        <BLANKLINE>
                            % [ViolaMusicVoice measure 1]                                        %! SM4
                            \clef "alto"                                                         %! SM8:DEFAULT_CLEF:ST3
                            \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                        %@% \override ViolaMusicStaff.Clef.color = ##f                           %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                            \set ViolaMusicStaff.forceClef = ##t                                 %! SM8:DEFAULT_CLEF:SM33:ST3
                            R1 * 1/2
                            ^ \markup {                                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                \with-color                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    #(x11-color 'DarkViolet)                                     %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    (Viola)                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                }                                                                %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                            \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)          %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
        <BLANKLINE>
                            % [ViolaMusicVoice measure 2]                                        %! SM4
                            R1 * 3/8
        <BLANKLINE>
                            % [ViolaMusicVoice measure 3]                                        %! SM4
                            R1 * 1/2
        <BLANKLINE>
                            % [ViolaMusicVoice measure 4]                                        %! SM4
                            R1 * 3/8
        <BLANKLINE>
                        }
                    }
                    \tag Cello                                                                   %! ST4
                    \context CelloMusicStaff = "CelloMusicStaff"
                    {
                        \context CelloMusicVoice = "CelloMusicVoice"
                        {
        <BLANKLINE>
                            % [CelloMusicVoice measure 1]                                        %! SM4
                            \clef "bass"                                                         %! SM8:DEFAULT_CLEF:ST3
                            \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                        %@% \override CelloMusicStaff.Clef.color = ##f                           %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                            \set CelloMusicStaff.forceClef = ##t                                 %! SM8:DEFAULT_CLEF:SM33:ST3
                            R1 * 1/2
                            ^ \markup {                                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                \with-color                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    #(x11-color 'DarkViolet)                                     %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    (Cello)                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                }                                                                %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                            \override CelloMusicStaff.Clef.color = #(x11-color 'violet)          %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
        <BLANKLINE>
                            % [CelloMusicVoice measure 2]                                        %! SM4
                            R1 * 3/8
        <BLANKLINE>
                            % [CelloMusicVoice measure 3]                                        %! SM4
                            R1 * 1/2
        <BLANKLINE>
                            % [CelloMusicVoice measure 4]                                        %! SM4
                            R1 * 3/8
        <BLANKLINE>
                        }
                    }
                >>
            >>
        >>

    ..  container:: example

        Raises exception when voice does not allow part assignment:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     test_container_identifiers=True,
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> part_assignment = abjad.PartAssignment('Flute')

        >>> maker(
        ...     'ViolinMusicVoice',
        ...     baca.make_notes(),
        ...     baca.parts(part_assignment),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: ViolinMusicVoice does not allow Flute part assignment:
            abjad.PartAssignment('Flute')

    """
    if not isinstance(part_assignment, abjad.PartAssignment):
        message = 'part_assignment must be part assignment'
        message += f' (not {part_assignment!r}).'
        raise Exception(message)
    return PartAssignmentCommand(
        part_assignment=part_assignment,
        )

def text_spanner(
    items: typing.Union[str, typing.List],
    *,
    bookend: typing.Union[bool, int] = -1,
    leak: bool = None,
    lilypond_id: int = None,
    piece_selector: typings.Selector = 'baca.group()',
    selector: typings.Selector = 'baca.tleaves()',
    tweaks: typing.List[abjad.LilyPondTweakManager] = None,
    ) -> PiecewiseIndicatorCommand:
    r"""
    Attaches text span indicators.

    ..  container:: example

        Single-segment spanners.

        Dashed line with arrow:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.text_spanner('pont. => ord.'),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_dashed_line_with_arrow                                          %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "pont."              %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "ord."             %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Dashed line with hook:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.text_spanner('pont. =| ord.'),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_dashed_line_with_hook                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "pont."              %! PIC
                            - \tweak bound-details.right.text \markup {                              %! PIC
                                \concat                                                              %! PIC
                                    {                                                                %! PIC
                                        \raise                                                       %! PIC
                                            #-1                                                      %! PIC
                                            \draw-line                                               %! PIC
                                                #'(0 . -1)                                           %! PIC
                                        \hspace                                                      %! PIC
                                            #0.75                                                    %! PIC
                                        \general-align                                               %! PIC
                                            #Y                                                       %! PIC
                                            #1                                                       %! PIC
                                            \upright                                                 %! PIC
                                                ord.                                                 %! PIC
                                    }                                                                %! PIC
                                }                                                                    %! PIC
                            - \tweak bound-details.right.padding #1.25                               %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Solid line with arrow:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.text_spanner('pont. -> ord.'),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_solid_line_with_arrow                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "pont."              %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "ord."             %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Solid line with hook:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.text_spanner('pont. -| ord.'),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_solid_line_with_hook                                            %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "pont."              %! PIC
                            - \tweak bound-details.right.text \markup {                              %! PIC
                                \concat                                                              %! PIC
                                    {                                                                %! PIC
                                        \raise                                                       %! PIC
                                            #-1                                                      %! PIC
                                            \draw-line                                               %! PIC
                                                #'(0 . -1)                                           %! PIC
                                        \hspace                                                      %! PIC
                                            #0.75                                                    %! PIC
                                        \general-align                                               %! PIC
                                            #Y                                                       %! PIC
                                            #1                                                       %! PIC
                                            \upright                                                 %! PIC
                                                ord.                                                 %! PIC
                                    }                                                                %! PIC
                                }                                                                    %! PIC
                            - \tweak bound-details.right.padding #1.25                               %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Invisible lines:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.text_spanner('pont. || ord.'),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_invisible_line                                                  %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "pont."              %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "ord."             %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Piece selector groups leaves by measures:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.text_spanner(
        ...         'A || B',
        ...         piece_selector=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_invisible_line                                                  %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_invisible_line                                                  %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_invisible_line                                                  %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_invisible_line                                                  %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "A"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        With spanners:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.text_spanner(
        ...         'A -> B ->',
        ...         piece_selector=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_solid_line_with_arrow                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_solid_line_with_arrow                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_solid_line_with_arrow                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_solid_line_with_arrow                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "A"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Bookends each piece:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.text_spanner(
        ...         'A || B',
        ...         bookend=True,
        ...         piece_selector=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_invisible_line                                                  %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "B"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            \stopTextSpan                                                            %! PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_invisible_line                                                  %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "A"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            \stopTextSpan                                                            %! PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_invisible_line                                                  %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "B"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            \stopTextSpan                                                            %! PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_invisible_line                                                  %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "A"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        With spanners:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.text_spanner(
        ...         'A -> B ->',
        ...         bookend=True,
        ...         piece_selector=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_solid_line_with_arrow                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "B"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            \stopTextSpan                                                            %! PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_solid_line_with_arrow                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "A"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            \stopTextSpan                                                            %! PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_solid_line_with_arrow                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "B"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            \stopTextSpan                                                            %! PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_solid_line_with_arrow                                           %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            - \tweak bound-details.right.text \markup \baca-right "A"                %! PIC
                            - \tweak bound-details.right.padding #0.5                                %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        REGRESSION. Bookended hooks are kerned:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.text_spanner(
        ...         'A -| B -|',
        ...         piece_selector=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.text_spanner_staff_padding(4.5),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \override TextSpanner.staff-padding = #4.5                               %! OC1
                            e'8
                            - \abjad_solid_line_with_hook                                            %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_solid_line_with_hook                                            %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_solid_line_with_hook                                            %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "A"                  %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            \stopTextSpan                                                            %! PIC
                            - \abjad_solid_line_with_hook                                            %! PIC
                            - \tweak bound-details.left.text \markup \baca-left "B"                  %! PIC
                            - \tweak bound-details.right.text \markup {                              %! PIC
                                \concat                                                              %! PIC
                                    {                                                                %! PIC
                                        \raise                                                       %! PIC
                                            #-1                                                      %! PIC
                                            \draw-line                                               %! PIC
                                                #'(0 . -1)                                           %! PIC
                                        \hspace                                                      %! PIC
                                            #0.75                                                    %! PIC
                                        \general-align                                               %! PIC
                                            #Y                                                       %! PIC
                                            #1                                                       %! PIC
                                            \upright                                                 %! PIC
                                                A                                                    %! PIC
                                    }                                                                %! PIC
                                }                                                                    %! PIC
                            - \tweak bound-details.right.padding #1.25                               %! PIC
                            - \tweak bound-details.right.stencil-align-dir-y #center                 %! PIC
                            \startTextSpan                                                           %! PIC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            \stopTextSpan                                                            %! PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
                            \revert TextSpanner.staff-padding                                        %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    shape_to_style = {
        '=>': 'dashed_line_with_arrow',
        '=|': 'dashed_line_with_hook',
        '||': 'invisible_line',
        '->': 'solid_line_with_arrow',
        '-|': 'solid_line_with_hook',
        }
    if isinstance(items, str):
        items_ = []
        current_item: typing.List[str] = []
        for word in items.split():
            if word in shape_to_style:
                if current_item:
                    item_ = ' '.join(current_item)
                    items_.append(item_)
                    current_item = []
                items_.append(word)
            else:
                current_item.append(word)
        if current_item:
            item_ = ' '.join(current_item)
            items_.append(item_)
        items = items_
    bundles = []
    if len(items) == 1:
        raise NotImplementedError('implement lone item')
    if lilypond_id is None:
        command = r'\stopTextSpan'
    elif lilypond_id == 1:
        command = r'\stopTextSpanOne'
    elif lilypond_id == 2:
        command = r'\stopTextSpanTwo'
    elif lilypond_id == 3:
        command = r'\stopTextSpanThree'
    else:
        raise ValueError(lilypond_id)
    stop_text_span = abjad.StopTextSpan(command=command)
    cyclic_items = abjad.CyclicTuple(items)
    for i, item in enumerate(cyclic_items):
        if item in shape_to_style:
            continue
        if isinstance(item, str):
            string = rf'\markup \baca-left "{item}"'
            item_markup = abjad.LilyPondLiteral(string)
        else:
            item_markup = item
            assert isinstance(item_markup, abjad.Markup)
            item_markup = item_markup.upright()
        prototype = (abjad.LilyPondLiteral, abjad.Markup)
        assert isinstance(item_markup, prototype)
        style = 'invisible_line'
        if cyclic_items[i + 1] in shape_to_style:
            style = shape_to_style[cyclic_items[i + 1]]
            right_text = cyclic_items[i + 2]
        else:
            right_text = cyclic_items[i + 1]
        right_markup: typing.Union[abjad.LilyPondLiteral, abjad.Markup]
        if isinstance(right_text, str):
            if 'hook' not in style:
                string = rf'\markup \baca-right "{right_text}"'
                right_markup = abjad.LilyPondLiteral(string)
            else:
                right_markup = abjad.Markup.from_literal(right_text)
                assert isinstance(right_markup, abjad.Markup)
                right_markup = right_markup.upright()
        else:
            assert isinstance(right_text, abjad.Markup)
            right_markup = right_text.upright()
        if lilypond_id is None:
            command = r'\startTextSpan'
        elif lilypond_id == 1:
            command = r'\startTextSpanOne'
        elif lilypond_id == 2:
            command = r'\startTextSpanTwo'
        elif lilypond_id == 3:
            command = r'\startTextSpanThree'
        else:
            raise ValueError(lilypond_id)
        start_text_span = abjad.StartTextSpan(
            command=command,
            left_text=item_markup,
            style=style,
            )
        if tweaks:
            library.apply_tweaks(start_text_span, tweaks)
        # kerns bookended hook
        if 'hook' in style:
            assert isinstance(right_markup, abjad.Markup)
            line = abjad.Markup.draw_line(0, -1)
            line = line.raise_(-1)
            hspace = abjad.Markup.hspace(0.75)
            right_markup = right_markup.general_align('Y', 1)
            right_markup = abjad.Markup.concat([line, hspace, right_markup])
        bookended_spanner_start = abjad.new(
            start_text_span,
            right_text=right_markup,
            )
        # TODO: find some way to make these tweaks explicit to composer
        manager = abjad.tweak(bookended_spanner_start)
        manager.bound_details__right__stencil_align_dir_y = abjad.Center
        if 'hook' in style:
            manager.bound_details__right__padding = 1.25
        else:
            manager.bound_details__right__padding = 0.5
        bundle = IndicatorBundle(
            stop_text_span,
            start_text_span,
            bookended_spanner_start=bookended_spanner_start,
            enchained=True,
            )
        bundles.append(bundle)
    return PiecewiseIndicatorCommand(
        bookend=bookend,
        bundles=bundles,
        leak=leak,
        piece_selector=piece_selector,
        selector=selector,
        )

