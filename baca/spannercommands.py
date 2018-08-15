import abjad
import typing
from . import classes
from . import scoping
from . import typings


### CLASSES ###

class SpannerCommand(scoping.Command):
    r"""
    Spanner command.

    ..  container:: example

        With music-maker:

        >>> music_maker = baca.MusicMaker(
        ...     baca.SpannerCommand(
        ...         selector=baca.tuplet(1),
        ...         spanner=abjad.Slur(),
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
                            c'16
                            [
                            d'16
                            bf'16
                            ]
                        }
                        \scaleDurations #'(1 . 1) {
                            fs''16
                            [
                            (                                                                        %! SpannerCommand
                            e''16
                            ef''16
                            af''16
                            g''16
                            ]
                            )                                                                        %! SpannerCommand
                        }
                        \scaleDurations #'(1 . 1) {
                            a'16
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
        ...     baca.SpannerCommand(
        ...         selector=baca.leaves()[4:7],
        ...         spanner=abjad.Slur(),
        ...         ),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
                            (                                                                        %! SpannerCommand
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
                            )                                                                        %! SpannerCommand
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        >>> baca.SpannerCommand()
        SpannerCommand(selector=baca.leaves(), tags=[])

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_detach_first',
        '_left_broken',
        '_right_broken',
        '_spanner',
        '_tags',
        '_tweaks',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        deactivate: bool = None,
        detach_first: bool = None,
        left_broken: bool = None,
        map: typings.Selector = None,
        match: typings.Indices = None,
        measures: typings.Slice = None,
        right_broken: bool = None,
        scope: scoping.scope_typing = None,
        selector: typings.Selector = 'baca.leaves()',
        spanner: abjad.Spanner = None,
        tags: typing.List[typing.Union[str, abjad.Tag, None]] = None,
        tweaks: typing.Tuple[abjad.LilyPondTweakManager, ...] = None,
        ) -> None:
        scoping.Command.__init__(
            self,
            deactivate=deactivate,
            map=map,
            match=match,
            measures=measures,
            scope=scope,
            selector=selector,
            tags=tags,
            )
        if detach_first is not None:
            detach_first = bool(detach_first)
        self._detach_first = detach_first
        if left_broken is not None:
            left_broken = bool(left_broken)
        self._left_broken = left_broken
        if right_broken is not None:
            right_broken = bool(right_broken)
        self._right_broken = right_broken
        self._spanner = spanner
        self._validate_tweaks(tweaks)
        self._tweaks = tweaks

    ### SPECIAL METHODS ###

    def _call(self, argument=None):
        """
        Calls command on ``argument``.

        Returns spanner (for handoff to piecewise command).
        """
        if argument is None:
            return
        if self.spanner is None:
            return
        if self.selector:
            argument = self.selector(argument)
        leaves = abjad.select(argument).leaves()
        spanner = abjad.new(self.spanner)
        if self.left_broken:
            spanner = abjad.new(spanner, left_broken=self.left_broken)
        if self.right_broken:
            spanner = abjad.new(spanner, right_broken=self.right_broken)
        self._apply_tweaks(spanner, self.tweaks)
        if self.detach_first:
            abjad.detach(
                type(spanner),
                leaves,
                )
        abjad.attach(
            spanner,
            leaves,
            deactivate=self.deactivate,
            tag=self.tag.append('SpannerCommand'),
            )
        return spanner

    ### PUBLIC PROPERTIES ###

    @property
    def detach_first(self) -> typing.Optional[bool]:
        """
        Is true when command detaches existing spanners before attaching new
        ones.
        """
        return self._detach_first

    @property
    def left_broken(self) -> typing.Optional[bool]:
        """
        Is true when spanner is left-broken.
        """
        return self._left_broken

    @property
    def right_broken(self) -> typing.Optional[bool]:
        """
        Is true when spanner is right-broken.
        """
        return self._right_broken

    @property
    def selector(self) -> typing.Optional[abjad.Expression]:
        r"""
        Gets selector.

        ..  container:: example

            Selects trimmed leaves by default:

            >>> music_maker = baca.MusicMaker(baca.slur())

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
                                c'16
                                [
                                (                                                                        %! baca_slur:SpannerCommand
                                d'16
                                bf'16
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
                                )                                                                        %! baca_slur:SpannerCommand
                            }
                        }
                    }
                >>

        Set to selector or none.

        Returns selector or none.
        """
        return self._selector

    @property
    def spanner(self) -> typing.Optional[abjad.Spanner]:
        r"""
        Gets spanner.

        ..  container:: example

            Ties are smart enough to remove existing ties prior to attach:

            >>> music_maker = baca.MusicMaker()

            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[14, 14, 14]],
            ...     counts=[5],
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
                                d''4
                                ~
                                d''16
                                d''4
                                ~
                                d''16
                                d''4
                                ~
                                d''16
                            }
                        }
                    }
                >>

            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[14, 14, 14]],
            ...     baca.SpannerCommand(spanner=abjad.Tie()),
            ...     counts=[5],
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
                                d''4
                                ~                                                                        %! SpannerCommand
                                d''16
                                ~                                                                        %! SpannerCommand
                                d''4
                                ~                                                                        %! SpannerCommand
                                d''16
                                ~                                                                        %! SpannerCommand
                                d''4
                                ~                                                                        %! SpannerCommand
                                d''16
                            }
                        }
                    }
                >>

        Set to spanner or none.

        Returns spanner or none.
        """
        return self._spanner

    @property
    def tweaks(self) -> typing.Optional[
        typing.Tuple[abjad.LilyPondTweakManager, ...]]:
        """
        Gets tweaks.
        """
        return self._tweaks

### FACTORY FUNCTIONS ###

def beam(
    *tweaks: abjad.LilyPondTweakManager,
    selector: typings.Selector = 'baca.tleaves()',
    tag: typing.Optional[str] = 'baca_beam',
    ) -> SpannerCommand:
    r"""
    Attaches beam.

    ..  container:: example

        Beams everything:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.beam(),
        ...     baca.make_even_divisions(),
        ...     baca.pitch('C4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            c'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_beam:SpannerCommand
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_beam:SpannerCommand
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    """
    return SpannerCommand(
        detach_first=True,
        selector=selector,
        spanner=abjad.Beam(),
        tags=[tag],
        tweaks=tweaks,
        )

def finger_pressure_transition(
    *,
    selector: typings.Selector = 'baca.tleaves()',
    right_broken: bool = None,
    tag: typing.Optional[str] = 'baca_finger_pressure_transition',
    ) -> SpannerCommand:
    r"""
    Makes finger pressure transition glissando.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.finger_pressure_transition(selector=baca.notes()[:2]),
        ...     baca.finger_pressure_transition(selector=baca.notes()[2:]),
        ...     baca.make_notes(),
        ...     baca.note_head_style_harmonic(selector=baca.note(0)),
        ...     baca.note_head_style_harmonic(selector=baca.note(2)),
        ...     baca.pitch('C5'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            \once \override NoteHead.style = #'harmonic                              %! baca_note_head_style_harmonic:OverrideCommand(1)
                            c''2                                                                     %! baca_make_notes
                            - \tweak arrow-length #2                                                 %! baca_finger_pressure_transition:SpannerCommand
                            - \tweak arrow-width #0.5                                                %! baca_finger_pressure_transition:SpannerCommand
                            - \tweak bound-details.right.arrow ##t                                   %! baca_finger_pressure_transition:SpannerCommand
                            - \tweak thickness #3                                                    %! baca_finger_pressure_transition:SpannerCommand
                            \glissando                                                               %! baca_finger_pressure_transition:SpannerCommand
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            c''4.                                                                    %! baca_make_notes
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            \once \override NoteHead.style = #'harmonic                              %! baca_note_head_style_harmonic:OverrideCommand(1)
                            c''2                                                                     %! baca_make_notes
                            - \tweak arrow-length #2                                                 %! baca_finger_pressure_transition:SpannerCommand
                            - \tweak arrow-width #0.5                                                %! baca_finger_pressure_transition:SpannerCommand
                            - \tweak bound-details.right.arrow ##t                                   %! baca_finger_pressure_transition:SpannerCommand
                            - \tweak thickness #3                                                    %! baca_finger_pressure_transition:SpannerCommand
                            \glissando                                                               %! baca_finger_pressure_transition:SpannerCommand
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            c''4.                                                                    %! baca_make_notes
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    """
    return SpannerCommand(
        right_broken=right_broken,
        selector=selector,
        spanner=abjad.Glissando(allow_repeats=True),
        tags=[tag],
        tweaks=(
            abjad.tweak(2).arrow_length,
            abjad.tweak(0.5).arrow_width,
            abjad.tweak(True).bound_details__right__arrow,
            abjad.tweak(3).thickness,
            ),
        )

def glissando(
    *,
    allow_repeats: bool = None,
    allow_ties: bool = None,
    right_broken: bool = None,
    selector: typings.Selector = 'baca.tleaves()',
    stems: bool = None,
    style: str = None,
    tag: typing.Optional[str] = 'baca_glissando',
    ) -> SpannerCommand:
    r"""
    Attaches glissando.

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
        ...     baca.glissando()
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
                            \glissando                                                               %! baca_glissando:SpannerCommand
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            \glissando                                                               %! baca_glissando:SpannerCommand
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            \glissando                                                               %! baca_glissando:SpannerCommand
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
                            \glissando                                                               %! baca_glissando:SpannerCommand
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
                            \glissando                                                               %! baca_glissando:SpannerCommand
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
                            \glissando                                                               %! baca_glissando:SpannerCommand
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
                            \glissando                                                               %! baca_glissando:SpannerCommand
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
                            \glissando                                                               %! baca_glissando:SpannerCommand
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
                            \glissando                                                               %! baca_glissando:SpannerCommand
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            \glissando                                                               %! baca_glissando:SpannerCommand
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
                            \glissando                                                               %! baca_glissando:SpannerCommand
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
                            \glissando                                                               %! baca_glissando:SpannerCommand
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            \glissando                                                               %! baca_glissando:SpannerCommand
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        First and last PLTs:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.make_even_divisions(),
        ...     baca.glissando(selector=baca.plts()[:2]),
        ...     baca.glissando(selector=baca.plts()[-2:]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! SingleStaffScoreTemplate
            <<                                                                                       %! SingleStaffScoreTemplate
            <BLANKLINE>
                \context GlobalContext = "GlobalContext"                                             %! _make_global_context
                <<                                                                                   %! _make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "GlobalSkips"                                             %! _make_global_context
                    {                                                                                %! _make_global_context
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                    }                                                                                %! _make_global_context
            <BLANKLINE>
                >>                                                                                   %! _make_global_context
            <BLANKLINE>
                \context MusicContext = "MusicContext"                                               %! SingleStaffScoreTemplate
                <<                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
                    \context Staff = "MusicStaff"                                                    %! SingleStaffScoreTemplate
                    {                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                        \context Voice = "MusicVoice"                                                %! SingleStaffScoreTemplate
                        {                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! _comment_measure_numbers
                            e'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
                            \glissando                                                               %! baca_glissando:SpannerCommand
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! _comment_measure_numbers
                            g'8                                                                      %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! _comment_measure_numbers
                            d''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            f'8                                                                      %! baca_make_even_divisions
            <BLANKLINE>
                            e''8                                                                     %! baca_make_even_divisions
            <BLANKLINE>
                            g'8                                                                      %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! _comment_measure_numbers
                            f''8                                                                     %! baca_make_even_divisions
                            [                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                            e'8                                                                      %! baca_make_even_divisions
                            \glissando                                                               %! baca_glissando:SpannerCommand
            <BLANKLINE>
                            d''8                                                                     %! baca_make_even_divisions
                            ]                                                                        %! baca_make_even_divisions
            <BLANKLINE>
                        }                                                                            %! SingleStaffScoreTemplate
            <BLANKLINE>
                    }                                                                                %! SingleStaffScoreTemplate
            <BLANKLINE>
                >>                                                                                   %! SingleStaffScoreTemplate
            <BLANKLINE>
            >>                                                                                       %! SingleStaffScoreTemplate

    ..  container:: example

        With music-maker:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.new(
        ...         baca.glissando(),
        ...         map=baca.tuplets()[1:2].runs(),
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
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
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
                            [
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            e''16
                            ]
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            \glissando                                                               %! baca_glissando:SpannerCommand
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    glissando = abjad.Glissando(
        allow_repeats=allow_repeats,
        allow_ties=allow_ties,
        stems=stems,
        style=style,
        )
    return SpannerCommand(
        right_broken=right_broken,
        selector=selector,
        spanner=glissando,
        tags=[tag],
        )

def ottava(
    *,
    selector: typings.Selector = 'baca.tleaves()',
    tag: typing.Optional[str] = 'baca_ottava',
    ) -> SpannerCommand:
    r"""
    Attaches ottava spanner.

    ..  container:: example

        Attaches ottava spanner to trimmed leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.ottava(),
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
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            \ottava #1                                                               %! baca_ottava:SpannerCommand
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
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            \ottava #0                                                               %! baca_ottava:SpannerCommand
                            r4
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return SpannerCommand(
        selector=selector,
        spanner=abjad.OctavationSpanner(start=1, stop=0),
        tags=[tag],
        )

def ottava_bassa(
    *,
    selector: typings.Selector = 'baca.tleaves()',
    tag: typing.Optional[str] = 'baca_ottava_bassa',
    ) -> SpannerCommand:
    r"""
    Attaches ottava bassa spanner.

    ..  container:: example

        Attaches ottava bassa spanner to trimmed leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.ottava_bassa(),
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
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            \ottava #-1                                                              %! baca_ottava_bassa:SpannerCommand
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
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            \ottava #0                                                               %! baca_ottava_bassa:SpannerCommand
                            r4
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return SpannerCommand(
        selector=selector,
        spanner=abjad.OctavationSpanner(start=-1, stop=0),
        tags=[tag],
        )

def repeat_tie(
    *,
    selector: typings.Selector = 'baca.qrun(0)',
    tag: typing.Optional[str] = 'baca_repeat_tie',
    ) -> SpannerCommand:
    r"""
    Attaches repeat tie.

    ..  container:: example

        Attaches repeat tie to each equipitch run:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
        ...     baca.new(
        ...         baca.repeat_tie(),
        ...         map=baca.qruns(),
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
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            [
                            c'16
                            \repeatTie                                                               %! baca_repeat_tie:SpannerCommand
                            ]
                            bf'4
                            bf'16
                            \repeatTie                                                               %! baca_repeat_tie:SpannerCommand
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            bf'16
                            [
                            e''16
                            ]
                            e''4
                            \repeatTie                                                               %! baca_repeat_tie:SpannerCommand
                            e''16
                            \repeatTie                                                               %! baca_repeat_tie:SpannerCommand
                            r16
                            fs''16
                            [
                            af''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return SpannerCommand(
        selector=selector,
        spanner=abjad.Tie(repeat=True),
        tags=[tag],
        )

def repeat_tie_repeat_pitches(
    *,
    tag: typing.Optional[str] = 'baca_repeat_tie_repeat_pitches',
    ) -> SpannerCommand:
    """
    Repeat-ties repeat pitches.
    """
    return SpannerCommand(
        map=classes.selector().ltqruns().nontrivial(),
        selector='baca.qrun(0)',
        spanner=abjad.Tie(repeat=True),
        tags=[tag],
        )

def slur(
    *tweaks: abjad.LilyPondTweakManager,
    selector: typings.Selector = 'baca.tleaves()',
    tag: typing.Optional[str] = 'baca_slur',
    ) -> SpannerCommand:
    r"""
    Attaches slur.

    ..  container:: example

        Attaches slur to trimmed leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.slur(),
        ...     baca.slur_down(),
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
                            \override Slur.direction = #down                                         %! baca_slur_down:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            [
                            (                                                                        %! baca_slur:SpannerCommand
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
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            )                                                                        %! baca_slur:SpannerCommand
                            r4
                            \revert Slur.direction                                                   %! baca_slur_down:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches slur to trimmed leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.new(
        ...         baca.slur(),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.slur_down(),
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
                            \override Slur.direction = #down                                         %! baca_slur_down:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
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
                            [
                            (                                                                        %! baca_slur:SpannerCommand
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            )                                                                        %! baca_slur:SpannerCommand
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert Slur.direction                                                   %! baca_slur_down:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return SpannerCommand(
        selector=selector,
        spanner=abjad.Slur(),
        tags=[tag],
        tweaks=tweaks,
        )

def sustain_pedal(
    *,
    selector: typings.Selector = 'baca.leaves()',
    tag: typing.Optional[str] = 'baca_sustain_pedal',
    ) -> SpannerCommand:
    r"""
    Attaches sustain pedal.

    ..  container:: example

        Pedals leaves:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.sustain_pedal(),
        ...     baca.sustain_pedal_staff_padding(4),
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
                            \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! baca_sustain_pedal_staff_padding:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            r8
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
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
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            \revert Staff.SustainPedalLineSpanner.staff-padding                      %! baca_sustain_pedal_staff_padding:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Pedals leaves in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.new(
        ...         baca.sustain_pedal(),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.sustain_pedal_staff_padding(4),
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
                            \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! baca_sustain_pedal_staff_padding:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
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
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            fs''16
                            [
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert Staff.SustainPedalLineSpanner.staff-padding                      %! baca_sustain_pedal_staff_padding:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Pedals leaves in tuplet 1 (leaked to the left):

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.new(
        ...         baca.sustain_pedal(selector=baca.lleaves()),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.sustain_pedal_staff_padding(4),
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
                            \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! baca_sustain_pedal_staff_padding:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            r16
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert Staff.SustainPedalLineSpanner.staff-padding                      %! baca_sustain_pedal_staff_padding:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Pedals leaves in tuplet 1 (leaked to the right):

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.new(
        ...         baca.sustain_pedal(selector=baca.rleaves()),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.sustain_pedal_staff_padding(4),
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
                            \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! baca_sustain_pedal_staff_padding:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
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
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            fs''16
                            [
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            r4
                            \revert Staff.SustainPedalLineSpanner.staff-padding                      %! baca_sustain_pedal_staff_padding:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Pedals leaves in tuplet 1 (leaked wide):

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.new(
        ...         baca.sustain_pedal(selector=baca.wleaves()),
        ...         map=baca.tuplet(1),
        ...         ),
        ...     baca.sustain_pedal_staff_padding(4),
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
                            \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! baca_sustain_pedal_staff_padding:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            r16
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            r4
                            \revert Staff.SustainPedalLineSpanner.staff-padding                      %! baca_sustain_pedal_staff_padding:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Pedals leaves in tuplets:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.new(
        ...         baca.sustain_pedal(),
        ...         map=baca.tuplets(),
        ...         ),
        ...     baca.sustain_pedal_staff_padding(4),
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
                            \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! baca_sustain_pedal_staff_padding:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            r8
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            fs''16
                            [
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                        }
                        \times 4/5 {
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            a'16
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
                            r4
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            \revert Staff.SustainPedalLineSpanner.staff-padding                      %! baca_sustain_pedal_staff_padding:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Pedals leaves in tuplets (leaked to the left):

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.new(
        ...         baca.sustain_pedal(selector=baca.lleaves()),
        ...         map=baca.tuplets(),
        ...         ),
        ...     baca.sustain_pedal_staff_padding(4),
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
                            \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! baca_sustain_pedal_staff_padding:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            r8
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
                            c'16
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            r16
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            g''16
                            ]
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            \revert Staff.SustainPedalLineSpanner.staff-padding                      %! baca_sustain_pedal_staff_padding:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Pedals leaves in tuplets (leaked to the right):

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.new(
        ...         baca.sustain_pedal(selector=baca.rleaves()),
        ...         map=baca.tuplets(),
        ...         ),
        ...     baca.sustain_pedal_staff_padding(4),
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
                            \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! baca_sustain_pedal_staff_padding:OverrideCommand(1)
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            r8
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
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
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            fs''16
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            [
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            \set Staff.pedalSustainStyle = #'bracket                                 %! baca_sustain_pedal:SpannerCommand
                            a'16
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            \sustainOn                                                               %! baca_sustain_pedal:SpannerCommand
                            r4
                            \sustainOff                                                              %! baca_sustain_pedal:SpannerCommand
                            \revert Staff.SustainPedalLineSpanner.staff-padding                      %! baca_sustain_pedal_staff_padding:OverrideCommand(2)
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    return SpannerCommand(
        selector=selector,
        spanner=abjad.PianoPedalSpanner(style='bracket'),
        tags=[tag],
        )

def tie(
    *,
    repeat: typing.Union[
        bool,
        typings.IntegerPair,
        abjad.DurationInequality,
        ] = None,
    selector: typings.Selector = 'baca.qrun(0)',
    tag: typing.Optional[str] = 'baca_tie',
    ) -> SpannerCommand:
    r"""
    Attaches tie.

    ..  container:: example

        Attaches ties to equipitch runs:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
        ...     baca.new(
        ...         baca.tie(),
        ...         map=baca.qruns(),
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
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            ~                                                                        %! baca_tie:SpannerCommand
                            [
                            c'16
                            ]
                            bf'4
                            ~                                                                        %! baca_tie:SpannerCommand
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            bf'16
                            [
                            e''16
                            ~                                                                        %! baca_tie:SpannerCommand
                            ]
                            e''4
                            ~                                                                        %! baca_tie:SpannerCommand
                            e''16
                            r16
                            fs''16
                            [
                            af''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches repeat-threshold ties to equipitch runs:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
        ...     baca.new(
        ...         baca.tie(repeat=(1, 8)),
        ...         map=baca.qruns(),
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
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            ~                                                                        %! baca_tie:SpannerCommand
                            [
                            c'16
                            ]
                            bf'4
                            bf'16
                            \repeatTie                                                               %! baca_tie:SpannerCommand
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            bf'16
                            [
                            e''16
                            ~                                                                        %! baca_tie:SpannerCommand
                            ]
                            e''4
                            e''16
                            \repeatTie                                                               %! baca_tie:SpannerCommand
                            r16
                            fs''16
                            [
                            af''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    tie = abjad.Tie(
        repeat=repeat,
        )
    return SpannerCommand(
        selector=selector,
        spanner=tie,
        tags=[tag],
        )

def tie_repeat_pitches(
    *,
    tag: typing.Optional[str] = 'baca_tie_repeat_pitches',
    ) -> SpannerCommand:
    """
    Ties repeat pitches.
    """
    command = tie(tag=tag)
    command.map = classes.selector().ltqruns().nontrivial()
    return command

def trill_spanner(
    string: str = None,
    *,
    harmonic: bool = None,
    left_broken: bool = None,
    right_broken: bool = None,
    selector: typings.Selector = 'baca.tleaves().with_next_leaf()',
    tag: typing.Optional[str] = 'baca_trill_spanner',
    ) -> SpannerCommand:
    r"""
    Attaches trill spanner.

    ..  container:: example

        Attaches trill spanner to trimmed leaves (leaked to the right):

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.trill_spanner(),
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
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            [
                            \startTrillSpan
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
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches trill spanner to trimmed leaves (leaked to the right) in
        every equipitch run:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.new(
        ...         baca.trill_spanner(),
        ...         map=baca.qruns(),
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
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            [
                            \startTrillSpan
                            d'16
                            ]
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan
                            bf'4
                            ~
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan
                            bf'16
                            r16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            \startTrillSpan
                            e''16
                            ]
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan
                            ef''4
                            ~
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan
                            ef''16
                            r16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            af''16
                            [
                            \startTrillSpan
                            g''16
                            ]
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan
                        }
                        \times 4/5 {
                            a'16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan
                            r4
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches trill to trimmed leaves (leaked to the right) in every
        run:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.new(
        ...         baca.trill_spanner(),
        ...         map=baca.runs(),
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
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            c'16
                            [
                            \startTrillSpan
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            \startTrillSpan
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            af''16
                            [
                            \startTrillSpan
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches pitched trill to trimmed leaves (leaked to the right) in
        equipitch run 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.rests_around([2], [4]),
        ...     baca.new(
        ...         baca.trill_spanner(string='Eb4'),
        ...         map=baca.qrun(0),
        ...         ),
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
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            c'16
                            [
                            \startTrillSpan ef'
                            d'16
                            ]
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            [
                            e''16
                            ]
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches pitched trill to trimmed leaves (leaked to the right) in
        every equipitch run:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.new(
        ...         baca.trill_spanner(string='Eb4'),
        ...         map=baca.qruns(),
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
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            c'16
                            [
                            \startTrillSpan ef'
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            d'16
                            ]
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan ef'
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            bf'4
                            ~
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan ef'
                            bf'16
                            r16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            fs''16
                            [
                            \startTrillSpan ef'
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            e''16
                            ]
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan ef'
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            ef''4
                            ~
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan ef'
                            ef''16
                            r16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            af''16
                            [
                            \startTrillSpan ef'
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            g''16
                            ]
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan ef'
                        }
                        \times 4/5 {
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            a'16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan ef'
                            r4
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches pitched trill (specified by interval) to trimmed leaves
        (leaked to the right) in every equipitch run:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.new(
        ...         baca.trill_spanner(string='M2'),
        ...         map=baca.qruns(),
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
                            \override TupletBracket.staff-padding = #5                               %! baca_tuplet_bracket_staff_padding:OverrideCommand(1)
                            r8
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            c'16
                            [
                            \startTrillSpan d'
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            d'16
                            ]
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan e'
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            bf'4
                            ~
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan c''
                            bf'16
                            r16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            fs''16
                            [
                            \startTrillSpan gs''
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            e''16
                            ]
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan fs''
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            ef''4
                            ~
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan f''
                            ef''16
                            r16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            af''16
                            [
                            \startTrillSpan bf''
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            g''16
                            ]
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan a''
                        }
                        \times 4/5 {
                            \pitchedTrill                                                            %! baca_trill_spanner:SpannerCommand
                            a'16
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \startTrillSpan b'
                            r4
                            \stopTrillSpan                                                           %! baca_trill_spanner:SpannerCommand
                            \revert TupletBracket.staff-padding                                      %! baca_tuplet_bracket_staff_padding:OverrideCommand(2)
                        }
                    }
                }
            >>

    """
    if string is None:
        interval = None
        pitch = None
    else:
        try:
            interval = None
            pitch = abjad.NamedPitch(string)
        except ValueError:
            interval = abjad.NamedInterval(string)
            pitch = None
    return SpannerCommand(
        left_broken=left_broken,
        right_broken=right_broken,
        spanner=abjad.TrillSpanner(
            interval=interval,
            is_harmonic=harmonic,
            pitch=pitch,
            ),
        selector=selector,
        tags=[tag],
        )
