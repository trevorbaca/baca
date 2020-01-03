import inspect
import typing

import abjad

from . import classes, scoping, typings


def _site(frame):
    prefix = "baca"
    return scoping.site(frame, prefix)


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
        map: abjad.Expression = None,
        match: typings.Indices = None,
        measures: typings.SliceTyping = None,
        right_broken: bool = None,
        scope: scoping.ScopeTyping = None,
        selector: abjad.Expression = classes.Expression().select().leaves(),
        start_indicator: typing.Any = None,
        stop_indicator: typing.Any = None,
        tags: typing.List[typing.Optional[abjad.Tag]] = None,
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
                for leaf in abjad.iterate(argument).leaves(grace=False):
                    abjad.detach(type(start_indicator), leaf)
            self._apply_tweaks(start_indicator, self.tweaks)
            first_leaf = abjad.select(argument).leaf(0)
            if self.left_broken:
                self._attach_indicator(
                    start_indicator,
                    first_leaf,
                    deactivate=self.deactivate,
                    tag=abjad.Tag("baca.SpannerIndicatorCommand._call(1)")
                    .append(abjad.tags.SPANNER_START)
                    .append(abjad.tags.LEFT_BROKEN),
                )
            else:
                self._attach_indicator(
                    start_indicator,
                    first_leaf,
                    deactivate=self.deactivate,
                    tag=abjad.Tag("baca.SpannerIndicatorCommand._call(2)").append(
                        abjad.tags.SPANNER_START
                    ),
                )
        if self.stop_indicator is not None:
            stop_indicator = self.stop_indicator
            if self.detach_first:
                for leaf in abjad.iterate(argument).leaves(grace=False):
                    abjad.detach(type(stop_indicator), leaf)
            final_leaf = abjad.select(argument).leaf(-1)
            if self.right_broken:
                self._attach_indicator(
                    stop_indicator,
                    final_leaf,
                    deactivate=self.deactivate,
                    tag=abjad.Tag("baca.SpannerIndicatorCommand._call(3)")
                    .append(abjad.tags.SPANNER_STOP)
                    .append(abjad.tags.RIGHT_BROKEN),
                )
            else:
                self._attach_indicator(
                    stop_indicator,
                    final_leaf,
                    deactivate=self.deactivate,
                    tag=abjad.Tag("baca.SpannerIndicatorCommand._call(4)").append(
                        abjad.tags.SPANNER_STOP
                    ),
                )

    ### PRIVATE METHODS ###

    def _attach_indicator(self, indicator, leaf, deactivate=None, tag=None):
        # TODO: factor out late import
        from .segmentmaker import SegmentMaker

        assert isinstance(tag, abjad.Tag), repr(tag)
        reapplied = scoping.Command._remove_reapplied_wrappers(leaf, indicator)
        tag_ = self.tag.append(tag)
        wrapper = abjad.attach(
            indicator, leaf, deactivate=deactivate, tag=tag_, wrapper=True
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
    selector: abjad.Expression = classes.Expression().select().tleaves(),
    start_beam: abjad.StartBeam = None,
    stop_beam: abjad.StopBeam = None,
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
            \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__()
            <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #12                                             %! SPACING_COMMAND:baca.HorizontalSpacingSpecifier.__call__(1)
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #12                                             %! SPACING_COMMAND:baca.HorizontalSpacingSpecifier.__call__(1)
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #12                                             %! SPACING_COMMAND:baca.HorizontalSpacingSpecifier.__call__(1)
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #12                                             %! SPACING_COMMAND:baca.HorizontalSpacingSpecifier.__call__(1)
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                        \baca-new-spacing-section #1 #4                                              %! SPACING_COMMAND:baca.HorizontalSpacingSpecifier.__call__(1):baca.SegmentMaker._style_phantom_measures(1):PHANTOM
                        \time 1/4                                                                    %! baca.SegmentMaker._make_global_skips(3):PHANTOM:baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE:baca.SegmentMaker._style_phantom_measures(1)
                        \baca-time-signature-transparent                                             %! baca.SegmentMaker._style_phantom_measures(2):PHANTOM
                        s1 * 1/4                                                                     %! baca.SegmentMaker._make_global_skips(3):PHANTOM
                        \once \override Score.BarLine.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
                        \once \override Score.SpanBar.transparent = ##t                              %! baca.SegmentMaker._style_phantom_measures(3):PHANTOM
            <BLANKLINE>
                    }                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                >>                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                \context MusicContext = "Music_Context"                                              %! baca.SingleStaffScoreTemplate.__call__()
                <<                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    \context Staff = "Music_Staff"                                                   %! baca.SingleStaffScoreTemplate.__call__()
                    {                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                        \context Voice = "Music_Voice"                                               %! baca.SingleStaffScoreTemplate.__call__()
                        {                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                            % [Music_Voice measure 1]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            c'8                                                                      %! baca.make_even_divisions()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_even_divisions()"                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            _ [                                                                      %! baca.beam():baca.SpannerIndicatorCommand._call(2):SPANNER_START
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            c'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            c'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            c'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions()
                            ]                                                                        %! baca.beam():baca.SpannerIndicatorCommand._call(4):SPANNER_STOP
                            <> \bacaStopTextSpanRhythmAnnotation                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
            <BLANKLINE>
                            <<                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                                \context Voice = "Music_Voice"                                       %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                    % [Music_Voice measure 5]                                        %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \abjad-invisible-music-coloring                                  %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                %@% \abjad-invisible-music                                           %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                    \baca-not-yet-pitched-coloring                                   %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    b'1 * 1/4                                                        %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                \context Voice = "Rest_Voice"                                        %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                {                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                    % [Rest_Voice measure 5]                                         %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \once \override Score.TimeSignature.X-extent = ##f               %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                    \once \override MultiMeasureRest.transparent = ##t               %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                    \stopStaff                                                       %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \once \override Staff.StaffSymbol.transparent = ##t              %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \startStaff                                                      %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    R1 * 1/4                                                         %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                     %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                }                                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                            >>                                                                       %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                        }                                                                            %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                    }                                                                                %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.SingleStaffScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.SingleStaffScoreTemplate.__call__()

    """
    start_beam = start_beam or abjad.StartBeam(direction=direction)
    stop_beam = stop_beam or abjad.StopBeam()
    return SpannerIndicatorCommand(
        detach_first=True,
        selector=selector,
        start_indicator=start_beam,
        stop_indicator=stop_beam,
        tags=[_site(inspect.currentframe())],
        tweaks=tweaks,
    )


def ottava(
    start_ottava: abjad.Ottava = abjad.Ottava(n=1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, format_slot="after"),
    *,
    right_broken: bool = None,
    selector: abjad.Expression = classes.Expression().select().tleaves(),
) -> SpannerIndicatorCommand:
    r"""
    Attaches ottava indicators.

    ..  container:: example

        Attaches ottava indicators to trimmed leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(1)
                        r8
                        \ottava 1                                                                    %! baca.ottava():baca.SpannerIndicatorCommand._call(2):SPANNER_START
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
                        \ottava 0                                                                    %! baca.ottava():baca.SpannerIndicatorCommand._call(4):SPANNER_STOP
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(2)
                    }
                }
            >>

    """
    return SpannerIndicatorCommand(
        right_broken=right_broken,
        selector=selector,
        start_indicator=start_ottava,
        stop_indicator=stop_ottava,
        tags=[_site(inspect.currentframe())],
    )


def ottava_bassa(
    start_ottava: abjad.Ottava = abjad.Ottava(n=-1),
    stop_ottava: abjad.Ottava = abjad.Ottava(n=0, format_slot="after"),
    *,
    selector: abjad.Expression = classes.Expression().select().tleaves(),
) -> SpannerIndicatorCommand:
    r"""
    Attaches ottava bassa indicators.

    ..  container:: example

        Attaches ottava bassa indicators to trimmed leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(1)
                        r8
                        \ottava -1                                                                   %! baca.ottava_bassa():baca.SpannerIndicatorCommand._call(2):SPANNER_START
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
                        \ottava 0                                                                    %! baca.ottava_bassa():baca.SpannerIndicatorCommand._call(4):SPANNER_STOP
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(2)
                    }
                }
            >>

    """
    return SpannerIndicatorCommand(
        selector=selector,
        start_indicator=start_ottava,
        stop_indicator=stop_ottava,
        tags=[_site(inspect.currentframe())],
    )


def slur(
    *tweaks: abjad.LilyPondTweakManager,
    map: abjad.Expression = None,
    selector: abjad.Expression = classes.Expression().select().tleaves(),
    start_slur: abjad.StartSlur = None,
    stop_slur: abjad.StopSlur = None,
) -> SpannerIndicatorCommand:
    r"""
    Attaches slur.

    ..  container:: example

        Attaches slur to trimmed leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
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
                        \override Slur.direction = #down                                             %! baca.slur_down():baca.OverrideCommand._call(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(1)
                        r8
                        c'16
                        [
                        (                                                                            %! baca.slur():baca.SpannerIndicatorCommand._call(2):SPANNER_START
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
                        )                                                                            %! baca.slur():baca.SpannerIndicatorCommand._call(4):SPANNER_STOP
                        r4
                        \revert Slur.direction                                                       %! baca.slur_down():baca.OverrideCommand._call(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(2)
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
        tags=[_site(inspect.currentframe())],
        tweaks=tweaks,
    )


def sustain_pedal(
    *,
    selector: abjad.Expression = classes.Expression().select().leaves(),
    start_piano_pedal: abjad.StartPianoPedal = None,
    stop_piano_pedal: abjad.StopPianoPedal = None,
) -> SpannerIndicatorCommand:
    r"""
    Attaches sustain pedal indicators.

    ..  container:: example

        Pedals leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
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
                        \override Staff.SustainPedalLineSpanner.staff-padding = #4                   %! baca.sustain_pedal_staff_padding():baca.OverrideCommand._call(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(1)
                        r8
                        \sustainOn                                                                   %! baca.sustain_pedal():baca.SpannerIndicatorCommand._call(2):SPANNER_START
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
                        \sustainOff                                                                  %! baca.sustain_pedal():baca.SpannerIndicatorCommand._call(4):SPANNER_STOP
                        \revert Staff.SustainPedalLineSpanner.staff-padding                          %! baca.sustain_pedal_staff_padding():baca.OverrideCommand._call(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(2)
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
        tags=[_site(inspect.currentframe())],
    )


def trill_spanner(
    *tweaks: abjad.LilyPondTweakManager,
    alteration: str = None,
    harmonic: bool = None,
    left_broken: bool = None,
    map: abjad.Expression = None,
    right_broken: bool = None,
    selector: abjad.Expression = classes.Expression().select().tleaves().rleak(),
    start_trill_span: abjad.StartTrillSpan = None,
    stop_trill_span: abjad.StopTrillSpan = None,
) -> SpannerIndicatorCommand:
    r"""
    Attaches trill spanner indicators.

    ..  container:: example

        Attaches trill spanner to trimmed leaves (leaked to the right):

        >>> stack = baca.stack(
        ...     baca.figure(
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(1)
                        r8
                        c'16
                        [
                        \startTrillSpan                                                              %! baca.trill_spanner():baca.SpannerIndicatorCommand._call(2):SPANNER_START
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
                        \stopTrillSpan                                                               %! baca.trill_spanner():baca.SpannerIndicatorCommand._call(4):SPANNER_STOP
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(2)
                    }
                }
            >>

    ..  container:: example

        Attaches trill to trimmed leaves (leaked to the right) in every
        run:

        >>> stack = baca.stack(
        ...     baca.figure(
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(1)
                        r8
                        c'16
                        [
                        \startTrillSpan                                                              %! baca.trill_spanner():baca.SpannerIndicatorCommand._call(2):SPANNER_START
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                        \stopTrillSpan                                                               %! baca.trill_spanner():baca.SpannerIndicatorCommand._call(4):SPANNER_STOP
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        [
                        \startTrillSpan                                                              %! baca.trill_spanner():baca.SpannerIndicatorCommand._call(2):SPANNER_START
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        \stopTrillSpan                                                               %! baca.trill_spanner():baca.SpannerIndicatorCommand._call(4):SPANNER_STOP
                        af''16
                        [
                        \startTrillSpan                                                              %! baca.trill_spanner():baca.SpannerIndicatorCommand._call(2):SPANNER_START
                        g''16
                        \stopTrillSpan                                                               %! baca.trill_spanner():baca.SpannerIndicatorCommand._call(4):SPANNER_STOP
                        ]
                    }
                    \times 4/5 {
                        a'16
                        \startTrillSpan                                                              %! baca.trill_spanner():baca.SpannerIndicatorCommand._call(2):SPANNER_START
                        r4
                        \stopTrillSpan                                                               %! baca.trill_spanner():baca.SpannerIndicatorCommand._call(4):SPANNER_STOP
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(2)
                    }
                }
            >>

    ..  container:: example

        Tweaks trill spanner:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.new(
        ...         baca.trill_spanner(
        ...             abjad.tweak('red').color,
        ...             alteration='M2',
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
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(1)
                        r8
                        \pitchedTrill                                                                %! baca.trill_spanner():baca.SpannerIndicatorCommand._call(2):SPANNER_START
                        c'16
                        [
                        - \tweak color #red                                                          %! baca.trill_spanner():baca.SpannerIndicatorCommand._call(2):SPANNER_START
                        \startTrillSpan d'                                                           %! baca.trill_spanner():baca.SpannerIndicatorCommand._call(2):SPANNER_START
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
                        \stopTrillSpan                                                               %! baca.trill_spanner():baca.SpannerIndicatorCommand._call(4):SPANNER_STOP
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(2)
                    }
                }
            >>

    """
    if alteration is not None:
        prototype = (abjad.NamedPitch, abjad.NamedInterval, str)
        if not isinstance(alteration, prototype):
            message = f"trill spanner 'alteration' must be pitch, interval, str:"
            message += f"\n   {alteration}"
            raise Exception(message)
    interval = pitch = None
    if alteration is not None:
        try:
            pitch = abjad.NamedPitch(alteration)
        except:
            try:
                interval = abjad.NamedInterval(alteration)
            except:
                pass
    start_trill_span = start_trill_span or abjad.StartTrillSpan()
    if pitch is not None or interval is not None:
        start_trill_span = abjad.new(start_trill_span, interval=interval, pitch=pitch)
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
        tags=[_site(inspect.currentframe())],
        tweaks=tweaks,
    )
