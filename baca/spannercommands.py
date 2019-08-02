import abjad
import typing
from . import classes
from . import commands
from . import scoping
from . import typings


### CLASSES ###


class SpannerIndicatorCommand(scoping.Command):
    """
    Spanner indicator command.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_detach_first",
        "_left_broken",
        "_right_broken",
        "_start_indicator",
        "_stop_indicator",
        "_tags",
        "_tweaks",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        deactivate: bool = None,
        detach_first: bool = None,
        left_broken: bool = None,
        map: abjad.SelectorTyping = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        right_broken: bool = None,
        scope: scoping.ScopeTyping = None,
        selector: abjad.SelectorTyping = "baca.leaves()",
        start_indicator: typing.Any = None,
        stop_indicator: typing.Any = None,
        tags: typing.List[typing.Union[str, abjad.Tag, None]] = None,
        tweaks: abjad.IndexedTweakManagers = None,
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
        self._start_indicator = start_indicator
        self._stop_indicator = stop_indicator
        self._validate_indexed_tweaks(tweaks)
        self._tweaks = tweaks

    ### SPECIAL METHODS ###

    def _call(self, argument=None):
        """
        Calls command on ``argument``.
        """
        if argument is None:
            return
        if self.start_indicator is None and self.stop_indicator is None:
            return
        if self.selector:
            argument = self.selector(argument)
        if self.start_indicator is not None:
            start_indicator = self.start_indicator
            if self.detach_first:
                for leaf in abjad.iterate(argument).leaves(grace_notes=False):
                    abjad.detach(type(start_indicator), leaf)
            if self.left_broken:
                start_indicator = abjad.new(
                    start_indicator, left_broken=self.left_broken
                )
            self._apply_tweaks(start_indicator, self.tweaks)
            first_leaf = abjad.select(argument).leaf(0)
            self._attach_indicator(
                start_indicator,
                first_leaf,
                deactivate=self.deactivate,
                tag="SpannerIndicatorCommand(1)",
            )
        if self.stop_indicator is not None:
            stop_indicator = self.stop_indicator
            if self.detach_first:
                for leaf in abjad.iterate(argument).leaves(grace_notes=False):
                    abjad.detach(type(stop_indicator), leaf)
            if self.right_broken:
                stop_indicator = abjad.new(
                    stop_indicator, right_broken=self.right_broken
                )
            final_leaf = abjad.select(argument).leaf(-1)
            self._attach_indicator(
                stop_indicator,
                final_leaf,
                deactivate=self.deactivate,
                tag="SpannerIndicatorCommand(2)",
            )

    ### PRIVATE METHODS ###

    def _attach_indicator(self, indicator, leaf, deactivate=None, tag=None):
        # TODO: factor out late import
        from .segmentmaker import SegmentMaker

        assert isinstance(tag, str), repr(tag)
        reapplied = scoping.Command._remove_reapplied_wrappers(leaf, indicator)
        wrapper = abjad.attach(
            indicator,
            leaf,
            deactivate=deactivate,
            tag=self.tag.append(tag),
            wrapper=True,
        )
        if scoping.compare_persistent_indicators(indicator, reapplied):
            status = "redundant"
            SegmentMaker._treat_persistent_wrapper(
                self.runtime["manifests"], wrapper, status
            )

    ### PUBLIC PROPERTIES ###

    @property
    def detach_first(self) -> typing.Optional[bool]:
        """
        Is true when command detaches existing indicator first.
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
        """
        return self._selector

    @property
    def start_indicator(self) -> typing.Optional[typing.Any]:
        """
        Gets start indicator.
        """
        return self._start_indicator

    @property
    def stop_indicator(self) -> typing.Optional[typing.Any]:
        """
        Gets stop indicator.
        """
        return self._stop_indicator

    @property
    def tweaks(self) -> typing.Optional[abjad.IndexedTweakManagers]:
        """
        Gets tweaks.
        """
        return self._tweaks


### FACTORY FUNCTIONS ###


def beam(
    *tweaks: abjad.LilyPondTweakManager,
    direction: abjad.VerticalAlignment = None,
    selector: abjad.SelectorTyping = "baca.tleaves()",
    start_beam: abjad.StartBeam = None,
    stop_beam: abjad.StopBeam = None,
    tag: typing.Optional[str] = "baca.beam",
) -> SpannerIndicatorCommand:
    r"""
    Attaches beam.

    ..  container:: example

        Beams everything and sets beam direction down:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.beam(
        ...         direction=abjad.Down,
        ...         ),
        ...     baca.make_even_divisions(),
        ...     baca.pitch('C4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                    {                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \baca-new-spacing-section #1 #12                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
                        \baca-new-spacing-section #1 #4                                              %! PHANTOM:_style_phantom_measures(1):HorizontalSpacingSpecifier(1):SPACING_COMMAND
                        \time 1/4                                                                    %! PHANTOM:_style_phantom_measures(1):EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(3)
                        \baca-time-signature-transparent                                             %! PHANTOM:_style_phantom_measures(2)
                        s1 * 1/4                                                                     %! PHANTOM:_make_global_skips(3)
                        \once \override Score.BarLine.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
                        \once \override Score.SpanBar.transparent = ##t                              %! PHANTOM:_style_phantom_measures(3)
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! _comment_measure_numbers
                            c'8                                                                      %! baca.make_even_divisions
                            _ [                                                                      %! baca.beam:SpannerIndicatorCommand(1)
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            c'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            c'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            c'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
                            ]                                                                        %! baca.beam:SpannerIndicatorCommand(2)
            <BLANKLINE>
                            <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                    c'1 * 1/4                                                        %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! PHANTOM:_make_multimeasure_rest_container
                                {                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                    \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:_style_phantom_measures(6)
                                    \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:_style_phantom_measures(7)
                                    \stopStaff                                                       %! PHANTOM:_style_phantom_measures(8)
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:_style_phantom_measures(8)
                                    \startStaff                                                      %! PHANTOM:_style_phantom_measures(8)
                                    R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                                }                                                                    %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                            >>                                                                       %! PHANTOM:_make_multimeasure_rest_container
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__

    """
    start_beam = start_beam or abjad.StartBeam(direction=direction)
    stop_beam = stop_beam or abjad.StopBeam()
    return SpannerIndicatorCommand(
        detach_first=True,
        selector=selector,
        start_indicator=start_beam,
        stop_indicator=stop_beam,
        tags=[tag],
        tweaks=tweaks,
    )


def ottava(
    start_ottava: abjad.Ottava = abjad.Ottava(n=1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, format_slot="after"),
    *,
    right_broken: bool = None,
    selector: abjad.SelectorTyping = "baca.tleaves()",
    tag: typing.Optional[str] = "baca.ottava",
) -> SpannerIndicatorCommand:
    r"""
    Attaches ottava indicators.

    ..  container:: example

        Attaches ottava indicators to trimmed leaves:

        >>> stack = baca.stack(
        ...     baca.pfmaker(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...         ),
        ...     rmakers.beam(),
        ...     baca.ottava(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        \ottava 1                                                                    %! baca.ottava:SpannerIndicatorCommand(1)
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
                        \ottava 0                                                                    %! baca.ottava:SpannerIndicatorCommand(2)
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return SpannerIndicatorCommand(
        right_broken=right_broken,
        selector=selector,
        start_indicator=start_ottava,
        stop_indicator=stop_ottava,
        tags=[tag],
    )


def ottava_bassa(
    start_ottava: abjad.Ottava = abjad.Ottava(n=-1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, format_slot="after"),
    *,
    selector: abjad.SelectorTyping = "baca.tleaves()",
    tag: typing.Optional[str] = "baca.ottava_bassa",
) -> SpannerIndicatorCommand:
    r"""
    Attaches ottava bassa indicators.

    ..  container:: example

        Attaches ottava bassa indicators to trimmed leaves:

        >>> stack = baca.stack(
        ...     baca.pfmaker(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...         ),
        ...     rmakers.beam(),
        ...     baca.ottava_bassa(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        \ottava -1                                                                   %! baca.ottava_bassa:SpannerIndicatorCommand(1)
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
                        \ottava 0                                                                    %! baca.ottava_bassa:SpannerIndicatorCommand(2)
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    return SpannerIndicatorCommand(
        selector=selector,
        start_indicator=start_ottava,
        stop_indicator=stop_ottava,
        tags=[tag],
    )


def slur(
    *tweaks: abjad.LilyPondTweakManager,
    map: abjad.SelectorTyping = None,
    selector: abjad.SelectorTyping = "baca.tleaves()",
    start_slur: abjad.StartSlur = None,
    stop_slur: abjad.StopSlur = None,
    tag: typing.Optional[str] = "baca.slur",
) -> SpannerIndicatorCommand:
    r"""
    Attaches slur.

    ..  container:: example

        Attaches slur to trimmed leaves:

        >>> stack = baca.stack(
        ...     baca.pfmaker(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...         ),
        ...     rmakers.beam(),
        ...     baca.slur(),
        ...     baca.slur_down(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override Slur.direction = #down                                             %! baca.slur_down:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        c'16
                        [
                        (                                                                            %! baca.slur:SpannerIndicatorCommand(1)
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
                        )                                                                            %! baca.slur:SpannerIndicatorCommand(2)
                        r4
                        \revert Slur.direction                                                       %! baca.slur_down:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    start_slur = start_slur or abjad.StartSlur()
    stop_slur = stop_slur or abjad.StopSlur()
    return SpannerIndicatorCommand(
        map=map,
        selector=selector,
        start_indicator=start_slur,
        stop_indicator=stop_slur,
        tags=[tag],
        tweaks=tweaks,
    )


def sustain_pedal(
    *,
    selector: abjad.SelectorTyping = "baca.leaves()",
    start_piano_pedal: abjad.StartPianoPedal = None,
    stop_piano_pedal: abjad.StopPianoPedal = None,
    tag: typing.Optional[str] = "baca.sustain_pedal",
) -> SpannerIndicatorCommand:
    r"""
    Attaches sustain pedal indicators.

    ..  container:: example

        Pedals leaves:

        >>> stack = baca.stack(
        ...     baca.pfmaker(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...         ),
        ...     rmakers.beam(),
        ...     baca.sustain_pedal(),
        ...     baca.sustain_pedal_staff_padding(4),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override Staff.SustainPedalLineSpanner.staff-padding = #4                   %! baca.sustain_pedal_staff_padding:OverrideCommand(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        \sustainOn                                                                   %! baca.sustain_pedal:SpannerIndicatorCommand(1)
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
                        \sustainOff                                                                  %! baca.sustain_pedal:SpannerIndicatorCommand(2)
                        \revert Staff.SustainPedalLineSpanner.staff-padding                          %! baca.sustain_pedal_staff_padding:OverrideCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    start_piano_pedal = start_piano_pedal or abjad.StartPianoPedal()
    stop_piano_pedal = stop_piano_pedal or abjad.StopPianoPedal()
    return SpannerIndicatorCommand(
        selector=selector,
        start_indicator=start_piano_pedal,
        stop_indicator=stop_piano_pedal,
        tags=[tag],
    )


def trill_spanner(
    argument: str = None,
    *tweaks: abjad.LilyPondTweakManager,
    harmonic: bool = None,
    left_broken: bool = None,
    map: abjad.SelectorTyping = None,
    right_broken: bool = None,
    selector: abjad.SelectorTyping = "baca.tleaves().rleak()",
    start_trill_span: abjad.StartTrillSpan = None,
    stop_trill_span: abjad.StopTrillSpan = None,
    tag: typing.Optional[str] = "baca.trill_spanner",
) -> SpannerIndicatorCommand:
    r"""
    Attaches trill spanner indicators.

    ..  container:: example

        Attaches trill spanner to trimmed leaves (leaked to the right):

        >>> stack = baca.stack(
        ...     baca.pfmaker(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.trill_spanner(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        c'16
                        [
                        \startTrillSpan                                                              %! baca.trill_spanner:SpannerIndicatorCommand(1)
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
                        \stopTrillSpan                                                               %! baca.trill_spanner:SpannerIndicatorCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    ..  container:: example

        Attaches trill to trimmed leaves (leaked to the right) in every
        run:

        >>> stack = baca.stack(
        ...     baca.pfmaker(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.trill_spanner(),
        ...         map=baca.runs(),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        c'16
                        [
                        \startTrillSpan                                                              %! baca.trill_spanner:SpannerIndicatorCommand(1)
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                        \stopTrillSpan                                                               %! baca.trill_spanner:SpannerIndicatorCommand(2)
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        [
                        \startTrillSpan                                                              %! baca.trill_spanner:SpannerIndicatorCommand(1)
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        \stopTrillSpan                                                               %! baca.trill_spanner:SpannerIndicatorCommand(2)
                        af''16
                        [
                        \startTrillSpan                                                              %! baca.trill_spanner:SpannerIndicatorCommand(1)
                        g''16
                        \stopTrillSpan                                                               %! baca.trill_spanner:SpannerIndicatorCommand(2)
                        ]
                    }
                    \times 4/5 {
                        a'16
                        \startTrillSpan                                                              %! baca.trill_spanner:SpannerIndicatorCommand(1)
                        r4
                        \stopTrillSpan                                                               %! baca.trill_spanner:SpannerIndicatorCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    ..  container:: example
 
        Tweaks trill spanner:
 
        >>> stack = baca.stack(
        ...     baca.pfmaker(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.trill_spanner(
        ...             'M2',
        ...             abjad.tweak('red').color,
        ...             ),
        ...         ),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])
        >>> lilypond_file = abjad.LilyPondFile.rhythm(selection)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP
 
        ..  docs::
 
            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \new Score
            <<
                \new GlobalContext
                {
                    \time 11/8
                    s1 * 11/8
                }
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding:OverrideCommand(1)
                        r8
                        \pitchedTrill                                                                %! baca.trill_spanner:SpannerIndicatorCommand(1)
                        c'16
                        [
                        - \tweak color #red                                                          %! baca.trill_spanner:SpannerIndicatorCommand(1)
                        \startTrillSpan d'                                                           %! baca.trill_spanner:SpannerIndicatorCommand(1)
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
                        \stopTrillSpan                                                               %! baca.trill_spanner:SpannerIndicatorCommand(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding:OverrideCommand(2)
                    }
                }
            >>

    """
    if argument is not None:
        prototype = (abjad.NamedPitch, abjad.NamedInterval, str)
        if not isinstance(argument, prototype):
            message = f"trill spanner argument must be pitch, interval, str:"
            message += f"\n   {argument}"
            raise Exception(message)
    interval = pitch = None
    if argument is not None:
        try:
            pitch = abjad.NamedPitch(argument)
        except:
            try:
                interval = abjad.NamedInterval(argument)
            except:
                pass
    start_trill_span = start_trill_span or abjad.StartTrillSpan()
    if pitch is not None or interval is not None:
        start_trill_span = abjad.new(
            start_trill_span, interval=interval, pitch=pitch
        )
    if harmonic is True:
        string = "#(lambda (grob) (grob-interpret-markup grob"
        string += r' #{ \markup \musicglyph #"noteheads.s0harmonic" #}))'
        abjad.tweak(start_trill_span).TrillPitchHead.stencil = string
    stop_trill_span = stop_trill_span or abjad.StopTrillSpan()
    return SpannerIndicatorCommand(
        left_broken=left_broken,
        map=map,
        right_broken=right_broken,
        selector=selector,
        start_indicator=start_trill_span,
        stop_indicator=stop_trill_span,
        tags=[tag],
        tweaks=tweaks,
    )
