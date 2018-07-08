import abjad
import typing
from . import typings
from .Command import Command
from .Selection import Selection
from .Sequence import Sequence


class BCPCommand(Command):
    """
    Bow contact point command.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(4) Commands'
    
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
        Command.__init__(self, selector=selector)
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
