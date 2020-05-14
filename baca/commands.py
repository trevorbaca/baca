import inspect
import typing

import abjad

from . import (
    classes,
    commandclasses,
    indicatorcommands,
    indicators,
    overrides,
    pitchcommands,
    scoping,
    typings,
)


def _site(frame, n=None):
    prefix = "baca"
    return scoping.site(frame, prefix, n=n)


### FACTORY FUNCTIONS ###


def allow_octaves(
    *, selector: abjad.Expression = classes.Expression().select().leaves()
) -> commandclasses.IndicatorCommand:
    """
    Attaches ALLOW_OCTAVE constant.
    """
    return commandclasses.IndicatorCommand(
        indicators=[abjad.const.ALLOW_OCTAVE], selector=selector
    )


def bcps(
    bcps,
    *tweaks: abjad.IndexedTweakManager,
    bow_change_tweaks: abjad.IndexedTweakManagers = None,
    final_spanner: bool = None,
    helper: typing.Callable = None,
    selector: abjad.Expression = classes.Expression().select().leaves(),
) -> commandclasses.BCPCommand:
    r"""
    Makes bow contact point command.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 16)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.make_even_divisions(),
            ...     baca.bcps(
            ...         [(1, 5), (3, 5), (2, 5), (4, 5), (5, 5)],
            ...         ),
            ...     baca.pitches('E4 F4'),
            ...     baca.script_staff_padding(5.5),
            ...     baca.text_spanner_staff_padding(2.5),
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
                            \baca-new-spacing-section #1 #16                                             %! SPACING_COMMAND:baca.HorizontalSpacingSpecifier.__call__(1)
                            \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-new-spacing-section #1 #16                                             %! SPACING_COMMAND:baca.HorizontalSpacingSpecifier.__call__(1)
                            \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-new-spacing-section #1 #16                                             %! SPACING_COMMAND:baca.HorizontalSpacingSpecifier.__call__(1)
                            \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                            \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                            s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                            \baca-new-spacing-section #1 #16                                             %! SPACING_COMMAND:baca.HorizontalSpacingSpecifier.__call__(1)
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
                                \override Script.staff-padding = #5.5                                    %! baca.script_staff_padding():baca.OverrideCommand._call(1)
                                \override TextSpanner.staff-padding = #2.5                               %! baca.text_spanner_staff_padding():baca.OverrideCommand._call(1)
                                e'8                                                                      %! baca.make_even_divisions()
                                - \downbow                                                               %! baca.bcps():baca.BCPCommand._call(6)
                                [                                                                        %! baca.make_even_divisions()
                                - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \baca-text-spanner-left-text "make_even_divisions()"                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                                - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps():baca.BCPCommand._call(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! baca.bcps():baca.BCPCommand._call(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps():baca.BCPCommand._call(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions()
                                - \upbow                                                                 %! baca.bcps():baca.BCPCommand._call(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps():baca.BCPCommand._call(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps():baca.BCPCommand._call(2)
                                - \baca-bcp-spanner-left-text #3 #5                                      %! baca.bcps():baca.BCPCommand._call(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps():baca.BCPCommand._call(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions()
                                - \downbow                                                               %! baca.bcps():baca.BCPCommand._call(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps():baca.BCPCommand._call(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps():baca.BCPCommand._call(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! baca.bcps():baca.BCPCommand._call(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps():baca.BCPCommand._call(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions()
                                \bacaStopTextSpanBCP                                                     %! baca.bcps():baca.BCPCommand._call(3)
                                ]                                                                        %! baca.make_even_divisions()
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps():baca.BCPCommand._call(2)
                                - \baca-bcp-spanner-left-text #4 #5                                      %! baca.bcps():baca.BCPCommand._call(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps():baca.BCPCommand._call(2)
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                e'8                                                                      %! baca.make_even_divisions()
                                - \upbow                                                                 %! baca.bcps():baca.BCPCommand._call(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps():baca.BCPCommand._call(3)
                                [                                                                        %! baca.make_even_divisions()
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps():baca.BCPCommand._call(2)
                                - \baca-bcp-spanner-left-text #5 #5                                      %! baca.bcps():baca.BCPCommand._call(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps():baca.BCPCommand._call(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions()
                                - \downbow                                                               %! baca.bcps():baca.BCPCommand._call(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps():baca.BCPCommand._call(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps():baca.BCPCommand._call(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! baca.bcps():baca.BCPCommand._call(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps():baca.BCPCommand._call(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions()
                                - \upbow                                                                 %! baca.bcps():baca.BCPCommand._call(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps():baca.BCPCommand._call(3)
                                ]                                                                        %! baca.make_even_divisions()
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps():baca.BCPCommand._call(2)
                                - \baca-bcp-spanner-left-text #3 #5                                      %! baca.bcps():baca.BCPCommand._call(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps():baca.BCPCommand._call(2)
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                f'8                                                                      %! baca.make_even_divisions()
                                - \downbow                                                               %! baca.bcps():baca.BCPCommand._call(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps():baca.BCPCommand._call(3)
                                [                                                                        %! baca.make_even_divisions()
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps():baca.BCPCommand._call(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! baca.bcps():baca.BCPCommand._call(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps():baca.BCPCommand._call(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions()
                                \bacaStopTextSpanBCP                                                     %! baca.bcps():baca.BCPCommand._call(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps():baca.BCPCommand._call(2)
                                - \baca-bcp-spanner-left-text #4 #5                                      %! baca.bcps():baca.BCPCommand._call(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps():baca.BCPCommand._call(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions()
                                - \upbow                                                                 %! baca.bcps():baca.BCPCommand._call(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps():baca.BCPCommand._call(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps():baca.BCPCommand._call(2)
                                - \baca-bcp-spanner-left-text #5 #5                                      %! baca.bcps():baca.BCPCommand._call(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps():baca.BCPCommand._call(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions()
                                - \downbow                                                               %! baca.bcps():baca.BCPCommand._call(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps():baca.BCPCommand._call(3)
                                ]                                                                        %! baca.make_even_divisions()
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps():baca.BCPCommand._call(2)
                                - \baca-bcp-spanner-left-text #1 #5                                      %! baca.bcps():baca.BCPCommand._call(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps():baca.BCPCommand._call(2)
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                                f'8                                                                      %! baca.make_even_divisions()
                                - \upbow                                                                 %! baca.bcps():baca.BCPCommand._call(7)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps():baca.BCPCommand._call(3)
                                [                                                                        %! baca.make_even_divisions()
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps():baca.BCPCommand._call(2)
                                - \baca-bcp-spanner-left-text #3 #5                                      %! baca.bcps():baca.BCPCommand._call(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps():baca.BCPCommand._call(2)
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions()
                                - \downbow                                                               %! baca.bcps():baca.BCPCommand._call(8)
                                \bacaStopTextSpanBCP                                                     %! baca.bcps():baca.BCPCommand._call(3)
                                - \abjad-solid-line-with-arrow                                           %! baca.bcps():baca.BCPCommand._call(2)
                                - \baca-bcp-spanner-left-text #2 #5                                      %! baca.bcps():baca.BCPCommand._call(2)
                                - \baca-bcp-spanner-right-text #4 #5                                     %! baca.bcps():baca.BCPCommand._call(2)
                                \bacaStartTextSpanBCP                                                    %! baca.bcps():baca.BCPCommand._call(2)
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions()
                                \bacaStopTextSpanBCP                                                     %! baca.bcps():baca.BCPCommand._call(1)
                                ]                                                                        %! baca.make_even_divisions()
                                \revert Script.staff-padding                                             %! baca.script_staff_padding():baca.OverrideCommand._call(2)
                                \revert TextSpanner.staff-padding                                        %! baca.text_spanner_staff_padding():baca.OverrideCommand._call(2)
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
    if final_spanner is not None:
        final_spanner = bool(final_spanner)
    return commandclasses.BCPCommand(
        bcps=bcps,
        bow_change_tweaks=bow_change_tweaks,
        final_spanner=final_spanner,
        helper=helper,
        selector=selector,
        tags=[_site(inspect.currentframe())],
        tweaks=tweaks,
    )


def close_volta(
    selector: abjad.Expression = classes.Expression().select().leaf(0),
    *,
    format_slot: str = "before",
) -> scoping.Suite:
    """
    Attaches bar line and overrides bar line X-extent.
    """
    assert format_slot in ("after", "before"), repr(format_slot)
    after = format_slot == "after"
    # does not require not_mol() tagging, just only_mol() tagging:
    return scoping.suite(
        indicatorcommands.bar_line(":|.", selector, format_slot=format_slot),
        scoping.only_mol(overrides.bar_line_x_extent((0, 1.5), selector, after=after)),
    )


def color(
    selector: abjad.Expression = classes.Expression().select().leaves(),
) -> commandclasses.ColorCommand:
    r"""
    Makes color command.

    :param selector: selector.

    ..  container:: example

        Colors leaves:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.color(),
        ...     rmakers.unbeam(),
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
                        \abjad-color-music #'red
                        r8
                        \abjad-color-music #'blue
                        c'16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        bf'4
                        ~
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \abjad-color-music #'red
                        fs''16
                        \abjad-color-music #'blue
                        e''16
                        \abjad-color-music #'red
                        ef''4
                        ~
                        \abjad-color-music #'blue
                        ef''16
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'blue
                        af''16
                        \abjad-color-music #'red
                        g''16
                    }
                    \times 4/5 {
                        \abjad-color-music #'blue
                        a'16
                        \abjad-color-music #'red
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(2)
                    }
                }
            >>

    ..  container:: example

        Colors leaves in tuplet 1:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.color(baca.tuplets()[1:2].leaves()),
        ...     rmakers.unbeam(),
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
                        d'16
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \abjad-color-music #'red
                        fs''16
                        \abjad-color-music #'blue
                        e''16
                        \abjad-color-music #'red
                        ef''4
                        ~
                        \abjad-color-music #'blue
                        ef''16
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'blue
                        af''16
                        \abjad-color-music #'red
                        g''16
                    }
                    \times 4/5 {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(2)
                    }
                }
            >>

    """
    return commandclasses.ColorCommand(selector=selector)


def container(
    identifier: str = None,
    *,
    selector: abjad.Expression = classes.Expression().select().leaves(),
) -> commandclasses.ContainerCommand:
    r"""
    Makes container with ``identifier`` and extends container with
    ``selector`` output.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.container('ViolinI', selector=baca.leaves()[:2]),
        ...     baca.container('ViolinII', selector=baca.leaves()[2:]),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')

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
                    \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                    \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                    s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
        <BLANKLINE>
                    % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                    \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                    \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                    s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
        <BLANKLINE>
                    % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                    \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                    \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                    s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
        <BLANKLINE>
                    % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                    \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                    \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                    s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
        <BLANKLINE>
                    % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
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
                        {   %*% ViolinI
        <BLANKLINE>
                            % [Music_Voice measure 1]                                            %! baca.SegmentMaker._comment_measure_numbers()
                            e'2                                                                  %! baca.make_notes()
                            - \abjad-dashed-line-with-hook                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_notes(repeat_ties=True)"        %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                             %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                            %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
        <BLANKLINE>
                            % [Music_Voice measure 2]                                            %! baca.SegmentMaker._comment_measure_numbers()
                            f'4.                                                                 %! baca.make_notes()
        <BLANKLINE>
                        }   %*% ViolinI
        <BLANKLINE>
                        {   %*% ViolinII
        <BLANKLINE>
                            % [Music_Voice measure 3]                                            %! baca.SegmentMaker._comment_measure_numbers()
                            e'2                                                                  %! baca.make_notes()
        <BLANKLINE>
                            % [Music_Voice measure 4]                                            %! baca.SegmentMaker._comment_measure_numbers()
                            f'4.                                                                 %! baca.make_notes()
                            <> \bacaStopTextSpanRhythmAnnotation                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
        <BLANKLINE>
                        }   %*% ViolinII
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
    if identifier is not None:
        if not isinstance(identifier, str):
            message = f"identifier must be string (not {identifier!r})."
            raise Exception(message)
    return commandclasses.ContainerCommand(identifier=identifier, selector=selector)


def cross_staff(
    *, selector: abjad.Expression = classes.Expression().select().phead(0)
) -> commandclasses.IndicatorCommand:
    r"""
    Attaches cross-staff command.

    ..  container:: example

        Attaches cross-staff command to last two pitched leaves:

        >>> score_template = baca.StringTrioScoreTemplate()
        >>> accumulator = baca.Accumulator(score_template=score_template)
        >>> commands = [
        ...     baca.figure([1], 8, signature=8),
        ...     rmakers.beam(),
        ... ]
        >>> accumulator(
        ...     'Violin_Music_Voice',
        ...     [[9, 11, 12, 14, 16]],
        ...     *commands,
        ...     rmakers.unbeam(),
        ...     baca.stem_up(),
        ...     figure_name='vn.1',
        ... )
        >>> accumulator(
        ...     'Viola_Music_Voice',
        ...     [[0, 2, 4, 5, 7]],
        ...     *commands,
        ...     baca.cross_staff(selector=baca.pleaves()[-2:]),
        ...     rmakers.unbeam(),
        ...     baca.stem_up(),
        ...     anchor=baca.anchor('Violin_Music_Voice'),
        ...     figure_name='va.1',
        ... )
        >>> accumulator(
        ...     'Violin_Music_Voice',
        ...     [[15]],
        ...     *commands,
        ...     rmakers.unbeam(),
        ...     figure_name='vn.2',
        ... )

        >>> maker = baca.SegmentMaker(
        ...     ignore_repeat_pitch_classes=True,
        ...     score_template=accumulator.score_template,
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=accumulator.time_signatures,
        ...     )
        >>> accumulator.populate_segment_maker(maker)
        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            <BLANKLINE>
            \context Score = "Score"                                                                 %! baca.StringTrioScoreTemplate.__call__()
            <<                                                                                       %! baca.StringTrioScoreTemplate.__call__()
            <BLANKLINE>
                \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
                <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                    {                                                                                %! abjad.ScoreTemplate._make_global_context()
            <BLANKLINE>
                        % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #12                                             %! SPACING_COMMAND:baca.HorizontalSpacingSpecifier.__call__(1)
                        \time 5/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 5/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \baca-new-spacing-section #1 #12                                             %! SPACING_COMMAND:baca.HorizontalSpacingSpecifier.__call__(1)
                        \time 1/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
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
                \context MusicContext = "Music_Context"                                              %! baca.StringTrioScoreTemplate.__call__()
                <<                                                                                   %! baca.StringTrioScoreTemplate.__call__()
            <BLANKLINE>
                    \context StringSectionStaffGroup = "String_Section_Staff_Group"                  %! baca.StringTrioScoreTemplate.__call__()
                    <<                                                                               %! baca.StringTrioScoreTemplate.__call__()
            <BLANKLINE>
                        \tag Violin                                                                  %! baca.ScoreTemplate._attach_liypond_tag()
                        \context ViolinMusicStaff = "Violin_Music_Staff"                             %! baca.StringTrioScoreTemplate.__call__()
                        {                                                                            %! baca.StringTrioScoreTemplate.__call__()
            <BLANKLINE>
                            \context ViolinMusicVoice = "Violin_Music_Voice"                         %! baca.StringTrioScoreTemplate.__call__()
                            {                                                                        %! baca.StringTrioScoreTemplate.__call__()
            <BLANKLINE>
                                {
            <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                        % [Violin_Music_Voice measure 1]                             %! baca.SegmentMaker._comment_measure_numbers()
                                        \override Stem.direction = #up                               %! baca.stem_up():baca.OverrideCommand._call(1)
                                        \clef "treble"                                               %! abjad.ScoreTemplate.attach_defaults(3):baca.SegmentMaker._set_status_tag():DEFAULT_CLEF
                                        \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! baca.SegmentMaker._attach_color_literal(2):DEFAULT_CLEF_COLOR
                                    %@% \override ViolinMusicStaff.Clef.color = ##f                  %! baca.SegmentMaker._attach_color_literal(1):DEFAULT_CLEF_COLOR_CANCELLATION
                                        \set ViolinMusicStaff.forceClef = ##t                        %! abjad.ScoreTemplate.attach_defaults(3):baca.SegmentMaker._treat_persistent_wrapper(2):baca.SegmentMaker._set_status_tag():DEFAULT_CLEF
                                        a'8
                                        ^ \baca-default-indicator-markup "(Violin)"                  %! DEFAULT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                                        - \abjad-dashed-line-with-hook                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                        - \baca-text-spanner-left-text "baca.music()"                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                        - \tweak bound-details.right.padding #2.75                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                                        - \tweak color #darkcyan                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                        - \tweak staff-padding #8                                    %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                        \bacaStartTextSpanRhythmAnnotation                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                        \override ViolinMusicStaff.Clef.color = #(x11-color 'violet) %! baca.SegmentMaker._attach_color_literal(2):DEFAULT_CLEF_REDRAW_COLOR
            <BLANKLINE>
                                        b'8
            <BLANKLINE>
                                        c''8
            <BLANKLINE>
                                        d''8
            <BLANKLINE>
                                        e''8
                                        \revert Stem.direction                                       %! baca.stem_up():baca.OverrideCommand._call(2)
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                }
            <BLANKLINE>
                                {
            <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                        % [Violin_Music_Voice measure 2]                             %! baca.SegmentMaker._comment_measure_numbers()
                                        ef''!8
                                        <> \bacaStopTextSpanRhythmAnnotation                         %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                }
            <BLANKLINE>
                                <<                                                                   %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                                    \context Voice = "Violin_Music_Voice"                            %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                    {                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                        % [Violin_Music_Voice measure 3]                             %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        \abjad-invisible-music-coloring                              %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                    %@% \abjad-invisible-music                                       %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                        \baca-not-yet-pitched-coloring                               %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        b'1 * 1/4                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                 %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                    }                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                    \context Voice = "Violin_Rest_Voice"                             %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                    {                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                        % [Violin_Rest_Voice measure 3]                              %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        \once \override Score.TimeSignature.X-extent = ##f           %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                        \once \override MultiMeasureRest.transparent = ##t           %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                        \stopStaff                                                   %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        \once \override Staff.StaffSymbol.transparent = ##t          %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        \startStaff                                                  %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        R1 * 1/4                                                     %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                 %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                    }                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                >>                                                                   %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                            }                                                                        %! baca.StringTrioScoreTemplate.__call__()
            <BLANKLINE>
                        }                                                                            %! baca.StringTrioScoreTemplate.__call__()
            <BLANKLINE>
                        \tag Viola                                                                   %! baca.ScoreTemplate._attach_liypond_tag()
                        \context ViolaMusicStaff = "Viola_Music_Staff"                               %! baca.StringTrioScoreTemplate.__call__()
                        {                                                                            %! baca.StringTrioScoreTemplate.__call__()
            <BLANKLINE>
                            \context ViolaMusicVoice = "Viola_Music_Voice"                           %! baca.StringTrioScoreTemplate.__call__()
                            {                                                                        %! baca.StringTrioScoreTemplate.__call__()
            <BLANKLINE>
                                {
            <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {
            <BLANKLINE>
                                        % [Viola_Music_Voice measure 1]                              %! baca.SegmentMaker._comment_measure_numbers()
                                        \override Stem.direction = #up                               %! baca.stem_up():baca.OverrideCommand._call(1)
                                        \clef "alto"                                                 %! abjad.ScoreTemplate.attach_defaults(3):baca.SegmentMaker._set_status_tag():DEFAULT_CLEF
                                        \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! baca.SegmentMaker._attach_color_literal(2):DEFAULT_CLEF_COLOR
                                    %@% \override ViolaMusicStaff.Clef.color = ##f                   %! baca.SegmentMaker._attach_color_literal(1):DEFAULT_CLEF_COLOR_CANCELLATION
                                        \set ViolaMusicStaff.forceClef = ##t                         %! abjad.ScoreTemplate.attach_defaults(3):baca.SegmentMaker._treat_persistent_wrapper(2):baca.SegmentMaker._set_status_tag():DEFAULT_CLEF
                                        c'8
                                        ^ \baca-default-indicator-markup "(Viola)"                   %! DEFAULT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                                        - \abjad-dashed-line-with-hook                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                        - \baca-text-spanner-left-text "baca.music()"                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                        - \tweak bound-details.right.padding #2.75                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                                        - \tweak color #darkcyan                                     %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                        - \tweak staff-padding #8                                    %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                        \bacaStartTextSpanRhythmAnnotation                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                        \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)  %! baca.SegmentMaker._attach_color_literal(2):DEFAULT_CLEF_REDRAW_COLOR
            <BLANKLINE>
                                        d'8
            <BLANKLINE>
                                        e'8
            <BLANKLINE>
                                        \crossStaff                                                  %! baca.cross_staff():baca.IndicatorCommand._call()
                                        f'8
            <BLANKLINE>
                                        \crossStaff                                                  %! baca.cross_staff():baca.IndicatorCommand._call()
                                        g'8
                                        \revert Stem.direction                                       %! baca.stem_up():baca.OverrideCommand._call(2)
                                        <> \bacaStopTextSpanRhythmAnnotation                         %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
            <BLANKLINE>
                                    }
            <BLANKLINE>
                                }
            <BLANKLINE>
                                <<                                                                   %! baca.SegmentMaker._make_multimeasure_rest_container(7)
            <BLANKLINE>
                                    \context Voice = "Viola_Music_Voice"                             %! baca.SegmentMaker._make_multimeasure_rest_container(4)
                                    {                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(4)
            <BLANKLINE>
                                        % [Viola_Music_Voice measure 2]                              %! baca.SegmentMaker._comment_measure_numbers()
                                        \abjad-invisible-music-coloring                              %! baca.SegmentMaker._make_multimeasure_rest_container(2):NOTE:INVISIBLE_MUSIC_COLORING
                                    %@% \abjad-invisible-music                                       %! baca.SegmentMaker._make_multimeasure_rest_container(3):NOTE:INVISIBLE_MUSIC_COMMAND
                                        \baca-not-yet-pitched-coloring                               %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE
                                        c'1 * 1/8                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(1):HIDDEN:NOTE
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"8"                 %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE
            <BLANKLINE>
                                    }                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(4)
            <BLANKLINE>
                                    \context Voice = "Viola_Rest_Voice"                              %! baca.SegmentMaker._make_multimeasure_rest_container(6)
                                    {                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(6)
            <BLANKLINE>
                                        % [Viola_Rest_Voice measure 2]                               %! baca.SegmentMaker._comment_measure_numbers()
                                        R1 * 1/8                                                     %! baca.SegmentMaker._make_multimeasure_rest_container(5):REST_VOICE:MULTIMEASURE_REST
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"8"                 %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:REST_VOICE
            <BLANKLINE>
                                    }                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(6)
            <BLANKLINE>
                                >>                                                                   %! baca.SegmentMaker._make_multimeasure_rest_container(7)
            <BLANKLINE>
                                <<                                                                   %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                                    \context Voice = "Viola_Music_Voice"                             %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                    {                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                        % [Viola_Music_Voice measure 3]                              %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        \abjad-invisible-music-coloring                              %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:MULTIMEASURE_REST:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                    %@% \abjad-invisible-music                                       %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:MULTIMEASURE_REST:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                        R1 * 1/4                                                     %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:MULTIMEASURE_REST
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                 %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:MULTIMEASURE_REST:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                    }                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                    \context Voice = "Viola_Rest_Voice"                              %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                    {                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                        % [Viola_Rest_Voice measure 3]                               %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        \once \override Score.TimeSignature.X-extent = ##f           %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                        \once \override MultiMeasureRest.transparent = ##t           %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                        \stopStaff                                                   %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        \once \override Staff.StaffSymbol.transparent = ##t          %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        \startStaff                                                  %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        R1 * 1/4                                                     %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                 %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                    }                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                >>                                                                   %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                            }                                                                        %! baca.StringTrioScoreTemplate.__call__()
            <BLANKLINE>
                        }                                                                            %! baca.StringTrioScoreTemplate.__call__()
            <BLANKLINE>
                        \tag Cello                                                                   %! baca.ScoreTemplate._attach_liypond_tag()
                        \context CelloMusicStaff = "Cello_Music_Staff"                               %! baca.StringTrioScoreTemplate.__call__()
                        {                                                                            %! baca.StringTrioScoreTemplate.__call__()
            <BLANKLINE>
                            \context CelloMusicVoice = "Cello_Music_Voice"                           %! baca.StringTrioScoreTemplate.__call__()
                            {                                                                        %! baca.StringTrioScoreTemplate.__call__()
            <BLANKLINE>
                                % [Cello_Music_Voice measure 1]                                      %! baca.SegmentMaker._comment_measure_numbers()
                                \clef "bass"                                                         %! abjad.ScoreTemplate.attach_defaults(3):baca.SegmentMaker._set_status_tag():DEFAULT_CLEF
                                \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! baca.SegmentMaker._attach_color_literal(2):DEFAULT_CLEF_COLOR
                            %@% \override CelloMusicStaff.Clef.color = ##f                           %! baca.SegmentMaker._attach_color_literal(1):DEFAULT_CLEF_COLOR_CANCELLATION
                                \set CelloMusicStaff.forceClef = ##t                                 %! abjad.ScoreTemplate.attach_defaults(3):baca.SegmentMaker._treat_persistent_wrapper(2):baca.SegmentMaker._set_status_tag():DEFAULT_CLEF
                                R1 * 5/8                                                             %! baca.SegmentMaker._call_rhythm_commands()
                                ^ \baca-default-indicator-markup "(Cello)"                           %! DEFAULT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                            %@% ^ \baca-duration-multiplier-markup #"5" #"8"                         %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER
                                \override CelloMusicStaff.Clef.color = #(x11-color 'violet)          %! baca.SegmentMaker._attach_color_literal(2):DEFAULT_CLEF_REDRAW_COLOR
            <BLANKLINE>
                                % [Cello_Music_Voice measure 2]                                      %! baca.SegmentMaker._comment_measure_numbers()
                                R1 * 1/8                                                             %! baca.SegmentMaker._call_rhythm_commands()
                            %@% ^ \baca-duration-multiplier-markup #"1" #"8"                         %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER
            <BLANKLINE>
                                <<                                                                   %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                                    \context Voice = "Cello_Music_Voice"                             %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                    {                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                        % [Cello_Music_Voice measure 3]                              %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        \abjad-invisible-music-coloring                              %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:MULTIMEASURE_REST:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                    %@% \abjad-invisible-music                                       %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:MULTIMEASURE_REST:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                        R1 * 1/4                                                     %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:MULTIMEASURE_REST
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                 %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:MULTIMEASURE_REST:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                    }                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
            <BLANKLINE>
                                    \context Voice = "Cello_Rest_Voice"                              %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                    {                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                        % [Cello_Rest_Voice measure 3]                               %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                        \once \override Score.TimeSignature.X-extent = ##f           %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                        \once \override MultiMeasureRest.transparent = ##t           %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                        \stopStaff                                                   %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        \once \override Staff.StaffSymbol.transparent = ##t          %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        \startStaff                                                  %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                        R1 * 1/4                                                     %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"                 %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
            <BLANKLINE>
                                    }                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
            <BLANKLINE>
                                >>                                                                   %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
            <BLANKLINE>
                            }                                                                        %! baca.StringTrioScoreTemplate.__call__()
            <BLANKLINE>
                        }                                                                            %! baca.StringTrioScoreTemplate.__call__()
            <BLANKLINE>
                    >>                                                                               %! baca.StringTrioScoreTemplate.__call__()
            <BLANKLINE>
                >>                                                                                   %! baca.StringTrioScoreTemplate.__call__()
            <BLANKLINE>
            >>                                                                                       %! baca.StringTrioScoreTemplate.__call__()

    """
    return commandclasses.IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\crossStaff")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def double_volta(
    selector: abjad.Expression = classes.Expression().select().leaf(0),
) -> scoping.Suite:
    """
    Attaches bar line and overrides bar line X-extent.
    """
    return scoping.suite(
        indicatorcommands.bar_line(":.|.:", selector, format_slot="before"),
        scoping.not_mol(overrides.bar_line_x_extent((0, 3), selector)),
        scoping.only_mol(overrides.bar_line_x_extent((0, 4), selector)),
    )


def dynamic_down(
    *, selector: abjad.Expression = classes.Expression().select().leaf(0)
) -> commandclasses.IndicatorCommand:
    r"""
    Attaches dynamic-down command.

    ..  container:: example

        Attaches dynamic-down command to leaf 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.dynamic('p'),
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].phead(0)),
        ...     baca.dynamic_down(),
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
                        \dynamicDown                                                                 %! baca.dynamic_down():baca.IndicatorCommand._call()
                        r8
                        c'16
                        \p                                                                           %! baca.dynamic():baca.IndicatorCommand._call()
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
                        \f                                                                           %! baca.dynamic():baca.IndicatorCommand._call()
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
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(2)
                    }
                }
            >>

    """
    return commandclasses.IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\dynamicDown")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def dynamic_up(
    *, selector: abjad.Expression = classes.Expression().select().leaf(0)
) -> commandclasses.IndicatorCommand:
    r"""
    Attaches dynamic-up command.

    ..  container:: example

        Attaches dynamic-up command to leaf 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.dynamic('p'),
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].phead(0)),
        ...     baca.dynamic_up(),
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
                        \dynamicUp                                                                   %! baca.dynamic_up():baca.IndicatorCommand._call()
                        r8
                        c'16
                        \p                                                                           %! baca.dynamic():baca.IndicatorCommand._call()
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
                        \f                                                                           %! baca.dynamic():baca.IndicatorCommand._call()
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
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(2)
                    }
                }
            >>

    """
    return commandclasses.IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\dynamicUp")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def edition(
    not_parts: typing.Union[str, abjad.Markup, commandclasses.IndicatorCommand],
    only_parts: typing.Union[str, abjad.Markup, commandclasses.IndicatorCommand],
) -> scoping.Suite:
    """
    Makes not-parts / only-parts markup suite.
    """
    if isinstance(not_parts, (str, abjad.Markup)):
        not_parts = markup(not_parts)
    assert isinstance(not_parts, commandclasses.IndicatorCommand)
    not_parts_ = scoping.not_parts(not_parts)
    if isinstance(only_parts, (str, abjad.Markup)):
        only_parts = markup(only_parts)
    assert isinstance(only_parts, commandclasses.IndicatorCommand)
    only_parts_ = scoping.only_parts(only_parts)
    return scoping.suite(not_parts_, only_parts_)


def finger_pressure_transition(
    *,
    selector: abjad.Expression = classes.Expression().select().tleaves(),
    right_broken: bool = None,
) -> commandclasses.GlissandoCommand:
    r"""
    Makes finger pressure transition glissando.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
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
                            \once \override NoteHead.style = #'harmonic                              %! baca.note_head_style_harmonic():baca.OverrideCommand._call(1)
                            c''2                                                                     %! baca.make_notes()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_notes()"                            %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak arrow-length #2                                                 %! baca.finger_pressure_transition():abjad.glissando(7)
                            - \tweak arrow-width #0.5                                                %! baca.finger_pressure_transition():abjad.glissando(7)
                            - \tweak bound-details.right.arrow ##t                                   %! baca.finger_pressure_transition():abjad.glissando(7)
                            - \tweak thickness #3                                                    %! baca.finger_pressure_transition():abjad.glissando(7)
                            \glissando                                                               %! baca.finger_pressure_transition():abjad.glissando(7)
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            c''4.                                                                    %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            \once \override NoteHead.style = #'harmonic                              %! baca.note_head_style_harmonic():baca.OverrideCommand._call(1)
                            c''2                                                                     %! baca.make_notes()
                            - \tweak arrow-length #2                                                 %! baca.finger_pressure_transition():abjad.glissando(7)
                            - \tweak arrow-width #0.5                                                %! baca.finger_pressure_transition():abjad.glissando(7)
                            - \tweak bound-details.right.arrow ##t                                   %! baca.finger_pressure_transition():abjad.glissando(7)
                            - \tweak thickness #3                                                    %! baca.finger_pressure_transition():abjad.glissando(7)
                            \glissando                                                               %! baca.finger_pressure_transition():abjad.glissando(7)
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            c''4.                                                                    %! baca.make_notes()
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
    return commandclasses.GlissandoCommand(
        allow_repeats=True,
        right_broken=right_broken,
        selector=selector,
        tags=[_site(inspect.currentframe())],
        tweaks=(
            abjad.tweak(2).arrow_length,
            abjad.tweak(0.5).arrow_width,
            abjad.tweak(True).bound_details__right__arrow,
            abjad.tweak(3).thickness,
        ),
    )


def flat_glissando(
    pitch: typing.Union[
        str, abjad.NamedPitch, abjad.StaffPosition, typing.List[abjad.StaffPosition],
    ] = None,
    *tweaks,
    allow_repitch: bool = None,
    do_not_hide_middle_note_heads: bool = None,
    mock: bool = None,
    hide_middle_stems: bool = None,
    hide_stem_selector: abjad.Expression = None,
    left_broken: bool = None,
    right_broken: bool = None,
    right_broken_show_next: bool = None,
    rleak: bool = None,
    selector: abjad.Expression = classes.Expression().select().pleaves(),
    stop_pitch: typing.Union[str, abjad.NamedPitch, abjad.StaffPosition] = None,
) -> scoping.Suite:
    """
    Makes flat glissando.
    """
    prototype = (list, str, abjad.NamedPitch, abjad.StaffPosition)
    if pitch is not None:
        assert isinstance(pitch, prototype), repr(pitch)
    if stop_pitch is not None:
        assert type(pitch) is type(stop_pitch), repr((pitch, stop_pitch))
    if rleak:
        selector = selector.rleak()
    commands: typing.List[scoping.Command] = []
    command = glissando(
        *tweaks,
        allow_repeats=True,
        allow_ties=True,
        hide_middle_note_heads=not do_not_hide_middle_note_heads,
        hide_middle_stems=hide_middle_stems,
        hide_stem_selector=hide_stem_selector,
        left_broken=left_broken,
        right_broken=right_broken,
        right_broken_show_next=right_broken_show_next,
        selector=selector,
    )
    commands.append(command)
    untie_command = untie(selector.leaves())
    commands.append(untie_command)
    if pitch is not None and stop_pitch is None:
        if isinstance(pitch, abjad.StaffPosition) or (
            isinstance(pitch, list) and isinstance(pitch[0], abjad.StaffPosition)
        ):
            staff_position_command = pitchcommands.staff_position(
                pitch, allow_repitch=allow_repitch, mock=mock, selector=selector,
            )
            commands.append(staff_position_command)
        else:
            pitch_command = pitchcommands.pitch(
                pitch, allow_repitch=allow_repitch, mock=mock, selector=selector,
            )
            commands.append(pitch_command)
    elif pitch is not None and stop_pitch is not None:
        if isinstance(pitch, abjad.StaffPosition):
            assert isinstance(stop_pitch, abjad.StaffPosition)
            interpolation_command = pitchcommands.interpolate_staff_positions(
                pitch, stop_pitch, mock=mock, selector=selector
            )
        else:
            assert isinstance(pitch, (str, abjad.NamedPitch))
            assert isinstance(stop_pitch, (str, abjad.NamedPitch))
            interpolation_command = pitchcommands.interpolate_pitches(
                pitch, stop_pitch, mock=mock, selector=selector
            )
        commands.append(interpolation_command)
    return scoping.suite(*commands)


def fractions(items):
    """
    Makes fractions.
    """
    result = []
    for item in items:
        item_ = abjad.NonreducedFraction(item)
        result.append(item_)
    return result


def glissando(
    *tweaks: abjad.IndexedTweakManager,
    allow_repeats: bool = None,
    allow_ties: bool = None,
    hide_middle_note_heads: bool = None,
    hide_middle_stems: bool = None,
    hide_stem_selector: abjad.Expression = None,
    left_broken: bool = None,
    map: abjad.Expression = None,
    right_broken: bool = None,
    right_broken_show_next: bool = None,
    selector: abjad.Expression = classes.Expression().select().tleaves(),
    style: str = None,
    zero_padding: bool = None,
) -> commandclasses.GlissandoCommand:
    r"""
    Attaches glissando.

    ..  container:: example

        With segment-maker:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.glissando()
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
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
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
                            e'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_even_divisions()"                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            g'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            f''8                                                                     %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            d''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            g'8                                                                      %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            f''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
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

    ..  container:: example

        First and last PLTs:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
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
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
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
                            e'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_even_divisions()"                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            g'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            f''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            d''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions()
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions()
            <BLANKLINE>
                            g'8                                                                      %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            f''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
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

    ..  container:: example

        Works with tweaks:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.glissando(
        ...         abjad.tweak('red').color,
        ...         ),
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
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
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
                            e'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_even_divisions()"                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak color #red                                                      %! baca.glissando():abjad.glissando(7)
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions()
                            - \tweak color #red                                                      %! baca.glissando():abjad.glissando(7)
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions()
                            - \tweak color #red                                                      %! baca.glissando():abjad.glissando(7)
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
                            - \tweak color #red                                                      %! baca.glissando():abjad.glissando(7)
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            g'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            - \tweak color #red                                                      %! baca.glissando():abjad.glissando(7)
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            f''8                                                                     %! baca.make_even_divisions()
                            - \tweak color #red                                                      %! baca.glissando():abjad.glissando(7)
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
                            - \tweak color #red                                                      %! baca.glissando():abjad.glissando(7)
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            d''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            - \tweak color #red                                                      %! baca.glissando():abjad.glissando(7)
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions()
                            - \tweak color #red                                                      %! baca.glissando():abjad.glissando(7)
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions()
                            - \tweak color #red                                                      %! baca.glissando():abjad.glissando(7)
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            g'8                                                                      %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
                            - \tweak color #red                                                      %! baca.glissando():abjad.glissando(7)
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            f''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            - \tweak color #red                                                      %! baca.glissando():abjad.glissando(7)
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions()
                            - \tweak color #red                                                      %! baca.glissando():abjad.glissando(7)
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
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

    ..  container:: example

        Works with indexed tweaks:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.glissando(
        ...         (abjad.tweak('red').color, 0),
        ...         (abjad.tweak('red').color, -1),
        ...         ),
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
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                        \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                        \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                        s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
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
                            e'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_even_divisions()"                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak color #red                                                      %! baca.glissando():abjad.glissando(7)
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            g'8                                                                      %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            f''8                                                                     %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            d''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            f'8                                                                      %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            e''8                                                                     %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            g'8                                                                      %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            f''8                                                                     %! baca.make_even_divisions()
                            [                                                                        %! baca.make_even_divisions()
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            e'8                                                                      %! baca.make_even_divisions()
                            - \tweak color #red                                                      %! baca.glissando():abjad.glissando(7)
                            \glissando                                                               %! baca.glissando():abjad.glissando(7)
            <BLANKLINE>
                            d''8                                                                     %! baca.make_even_divisions()
                            ]                                                                        %! baca.make_even_divisions()
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
    return commandclasses.GlissandoCommand(
        allow_repeats=allow_repeats,
        allow_ties=allow_ties,
        hide_middle_note_heads=hide_middle_note_heads,
        hide_middle_stems=hide_middle_stems,
        hide_stem_selector=hide_stem_selector,
        left_broken=left_broken,
        map=map,
        right_broken=right_broken,
        right_broken_show_next=right_broken_show_next,
        selector=selector,
        tags=[_site(inspect.currentframe())],
        tweaks=tweaks,
        zero_padding=zero_padding,
    )


def global_fermata(
    description: str = "fermata",
    selector: abjad.Expression = classes.Expression().select().leaf(0),
) -> commandclasses.GlobalFermataCommand:
    """
    Attaches global fermata.
    """
    fermatas = commandclasses.GlobalFermataCommand.description_to_command.keys()
    if description not in fermatas:
        message = f"must be in {repr(', '.join(fermatas))}:\n"
        message += f"   {repr(description)}"
        raise Exception(message)
    return commandclasses.GlobalFermataCommand(
        description=description,
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def instrument(
    instrument: abjad.Instrument,
    selector: abjad.Expression = classes.Expression().select().leaf(0),
) -> commandclasses.InstrumentChangeCommand:
    """
    Makes instrument change command.
    """
    if not isinstance(instrument, abjad.Instrument):
        message = f"instrument must be instrument (not {instrument!r})."
        raise Exception(message)
    return commandclasses.InstrumentChangeCommand(
        indicators=[instrument],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def invisible_music(
    selector: abjad.Expression = classes.Expression().select().leaf(0),
    *,
    map: abjad.Expression = None,
) -> scoping.Suite:
    r"""
    Attaches ``\baca-invisible-music`` literal.

    ..  container:: example

        Attaches ``\baca-invisible-music`` literal to middle leaves:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.invisible_music(
        ...         selector=baca.leaves()[1:-1],
        ...         ),
        ...     baca.make_notes(),
        ...     baca.pitch('C5'),
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
                            c''2                                                                     %! baca.make_notes()
                            - \abjad-dashed-line-with-hook                                           %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \baca-text-spanner-left-text "make_notes()"                            %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak bound-details.right.padding #2.75                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                            - \tweak color #darkcyan                                                 %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            - \tweak staff-padding #8                                                %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                            \bacaStartTextSpanRhythmAnnotation                                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \abjad-invisible-music                                                   %! baca.invisible_music(1):INVISIBLE_MUSIC_COMMAND:baca.IndicatorCommand._call()
                            \abjad-invisible-music-coloring                                          %! baca.invisible_music(2):INVISIBLE_MUSIC_COLORING:baca.IndicatorCommand._call()
                            c''4.                                                                    %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! baca.SegmentMaker._comment_measure_numbers()
                        %@% \abjad-invisible-music                                                   %! baca.invisible_music(1):INVISIBLE_MUSIC_COMMAND:baca.IndicatorCommand._call()
                            \abjad-invisible-music-coloring                                          %! baca.invisible_music(2):INVISIBLE_MUSIC_COLORING:baca.IndicatorCommand._call()
                            c''2                                                                     %! baca.make_notes()
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! baca.SegmentMaker._comment_measure_numbers()
                            c''4.                                                                    %! baca.make_notes()
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
    tag = _site(inspect.currentframe(), 1)
    tag = tag.append(abjad.tags.INVISIBLE_MUSIC_COMMAND)
    command_1 = commandclasses.IndicatorCommand(
        [abjad.LilyPondLiteral(r"\abjad-invisible-music")],
        deactivate=True,
        map=map,
        selector=selector,
        tags=[tag],
    )
    tag = _site(inspect.currentframe(), 2)
    tag = tag.append(abjad.tags.INVISIBLE_MUSIC_COLORING)
    command_2 = commandclasses.IndicatorCommand(
        [abjad.LilyPondLiteral(r"\abjad-invisible-music-coloring")],
        map=map,
        selector=selector,
        tags=[tag],
    )
    return scoping.suite(command_1, command_2)


def label(
    expression: abjad.Expression,
    selector: abjad.Expression = classes.Expression().select().leaves(),
) -> commandclasses.LabelCommand:
    r"""
    Labels ``selector`` output with label ``expression``.

    ..  container:: example

        Labels pitch names:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.label(abjad.label().with_pitches(locale='us')),
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
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(2)
                    }
                }
            >>

    """
    return commandclasses.LabelCommand(expression=expression, selector=selector)


def markup(
    argument: typing.Union[str, abjad.Markup],
    *tweaks: abjad.LilyPondTweakManager,
    boxed: bool = None,
    # typehinting is weird for some reason
    direction=abjad.Up,
    literal: bool = False,
    map: abjad.Expression = None,
    match: typings.Indices = None,
    measures: typings.SliceTyping = None,
    selector: abjad.Expression = classes.Expression().select().pleaf(0),
) -> commandclasses.IndicatorCommand:
    r"""
    Makes markup and inserts into indicator command.

    ..  container:: example

        Attaches markup to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.markup('più mosso'),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
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
                        \override TupletBracket.outside-staff-priority = #1000                       %! baca.tuplet_bracket_outside_staff_priority():baca.OverrideCommand._call(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(1)
                        r8
                        c'16
                        ^ \markup { "più mosso" }                                                    %! baca.markup():baca.IndicatorCommand._call()
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
                        \revert TupletBracket.outside-staff-priority                                 %! baca.tuplet_bracket_outside_staff_priority():baca.OverrideCommand._call(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(2)
                    }
                }
            >>

    ..  container:: example

        Set ``literal=True`` to pass predefined markup commands:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.markup(
        ...         r'\markup { \baca-triple-diamond-markup }',
        ...         literal=True,
        ...         ),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
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
                        \override TupletBracket.outside-staff-priority = #1000                       %! baca.tuplet_bracket_outside_staff_priority():baca.OverrideCommand._call(1)
                        \override TupletBracket.staff-padding = #2                                   %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(1)
                        r8
                        c'16
                        ^ \markup { \baca-triple-diamond-markup }                                    %! baca.markup():baca.IndicatorCommand._call()
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
                        \revert TupletBracket.outside-staff-priority                                 %! baca.tuplet_bracket_outside_staff_priority():baca.OverrideCommand._call(2)
                        \revert TupletBracket.staff-padding                                          %! baca.tuplet_bracket_staff_padding():baca.OverrideCommand._call(2)
                    }
                }
            >>

    ..  container:: example exception

        Raises exception on nonstring, nonmarkup ``argument``:

        >>> baca.markup(['Allegro', 'ma non troppo'])
        Traceback (most recent call last):
            ...
        Exception: MarkupLibary.__call__():
            Value of 'argument' must be str or markup.
            Not ['Allegro', 'ma non troppo'].

    """
    if direction not in (abjad.Down, abjad.Up):
        message = f"direction must be up or down (not {direction!r})."
        raise Exception(message)
    if isinstance(argument, str):
        if literal:
            markup = abjad.Markup(argument, direction=direction, literal=True)
        else:
            markup = abjad.Markup(argument, direction=direction)
    elif isinstance(argument, abjad.Markup):
        markup = abjad.new(argument, direction=direction)
    else:
        message = "MarkupLibary.__call__():\n"
        message += "  Value of 'argument' must be str or markup.\n"
        message += f"  Not {argument!r}."
        raise Exception(message)
    if boxed:
        markup = markup.box().override(("box-padding", 0.5))
    prototype = (str, abjad.Expression)
    if selector is not None and not isinstance(selector, prototype):
        message = "selector must be string or expression"
        message += f" (not {selector!r})."
        raise Exception(message)
    selector = selector or classes.Expression().select().phead(0)
    return commandclasses.IndicatorCommand(
        indicators=[markup],
        map=map,
        match=match,
        measures=measures,
        selector=selector,
        tags=[_site(inspect.currentframe())],
        tweaks=tweaks,
    )


def metronome_mark(
    key: typing.Union[str, indicators.Accelerando, indicators.Ritardando],
    selector: abjad.Expression = classes.Expression().select().leaf(0),
    *,
    redundant: bool = None,
) -> typing.Optional[commandclasses.MetronomeMarkCommand]:
    """
    Attaches metronome mark matching ``key`` metronome mark manifest.
    """
    if redundant is True:
        return None
    return commandclasses.MetronomeMarkCommand(
        key=key, redundant=redundant, selector=selector
    )


def parts(
    part_assignment: abjad.PartAssignment,
    *,
    selector: abjad.Expression = classes.Expression().select().leaves(),
) -> commandclasses.PartAssignmentCommand:
    r"""
    Inserts ``selector`` output in container and sets part assignment.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Violin_Music_Voice',
        ...     baca.make_notes(),
        ...     baca.parts(abjad.PartAssignment('Violin')),
        ...     baca.pitch('E4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        >>> abjad.f(lilypond_file[abjad.Score], strict=89)
        <BLANKLINE>
        \context Score = "Score"                                                                 %! baca.StringTrioScoreTemplate.__call__()
        <<                                                                                       %! baca.StringTrioScoreTemplate.__call__()
        <BLANKLINE>
            \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context()
            <<                                                                                   %! abjad.ScoreTemplate._make_global_context()
        <BLANKLINE>
                \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context()
                {                                                                                %! abjad.ScoreTemplate._make_global_context()
        <BLANKLINE>
                    % [Global_Skips measure 1]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                    \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                    \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                    s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
        <BLANKLINE>
                    % [Global_Skips measure 2]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                    \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                    \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                    s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
        <BLANKLINE>
                    % [Global_Skips measure 3]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                    \time 4/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                    \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                    s1 * 1/2                                                                     %! baca.SegmentMaker._make_global_skips(1)
        <BLANKLINE>
                    % [Global_Skips measure 4]                                                   %! baca.SegmentMaker._comment_measure_numbers()
                    \time 3/8                                                                    %! baca.SegmentMaker._make_global_skips(2):baca.SegmentMaker._set_status_tag():EXPLICIT_TIME_SIGNATURE
                    \baca-time-signature-color #'blue                                            %! baca.SegmentMaker._attach_color_literal(2):EXPLICIT_TIME_SIGNATURE_COLOR
                    s1 * 3/8                                                                     %! baca.SegmentMaker._make_global_skips(1)
        <BLANKLINE>
                    % [Global_Skips measure 5]                                                   %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(1):PHANTOM
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
            \context MusicContext = "Music_Context"                                              %! baca.StringTrioScoreTemplate.__call__()
            <<                                                                                   %! baca.StringTrioScoreTemplate.__call__()
        <BLANKLINE>
                \context StringSectionStaffGroup = "String_Section_Staff_Group"                  %! baca.StringTrioScoreTemplate.__call__()
                <<                                                                               %! baca.StringTrioScoreTemplate.__call__()
        <BLANKLINE>
                    \tag Violin                                                                  %! baca.ScoreTemplate._attach_liypond_tag()
                    \context ViolinMusicStaff = "Violin_Music_Staff"                             %! baca.StringTrioScoreTemplate.__call__()
                    {                                                                            %! baca.StringTrioScoreTemplate.__call__()
        <BLANKLINE>
                        \context ViolinMusicVoice = "Violin_Music_Voice"                         %! baca.StringTrioScoreTemplate.__call__()
                        {                                                                        %! baca.StringTrioScoreTemplate.__call__()
        <BLANKLINE>
                            {   %*% PartAssignment('Violin')
        <BLANKLINE>
                                % [Violin_Music_Voice measure 1]                                 %! baca.SegmentMaker._comment_measure_numbers()
                                \clef "treble"                                                   %! abjad.ScoreTemplate.attach_defaults(3):baca.SegmentMaker._set_status_tag():DEFAULT_CLEF
                                \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! baca.SegmentMaker._attach_color_literal(2):DEFAULT_CLEF_COLOR
                            %@% \override ViolinMusicStaff.Clef.color = ##f                      %! baca.SegmentMaker._attach_color_literal(1):DEFAULT_CLEF_COLOR_CANCELLATION
                                \set ViolinMusicStaff.forceClef = ##t                            %! abjad.ScoreTemplate.attach_defaults(3):baca.SegmentMaker._treat_persistent_wrapper(2):baca.SegmentMaker._set_status_tag():DEFAULT_CLEF
                                e'2                                                              %! baca.make_notes()
                                ^ \baca-default-indicator-markup "(Violin)"                      %! DEFAULT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                                - \abjad-dashed-line-with-hook                                   %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \baca-text-spanner-left-text "make_notes()"                    %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \tweak bound-details.right.padding #2.75                       %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):AUTODETECT:SPANNER_START
                                - \tweak color #darkcyan                                         %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                - \tweak staff-padding #8                                        %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                \bacaStartTextSpanRhythmAnnotation                               %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(2):SPANNER_START
                                \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)     %! baca.SegmentMaker._attach_color_literal(2):DEFAULT_CLEF_REDRAW_COLOR
        <BLANKLINE>
                                % [Violin_Music_Voice measure 2]                                 %! baca.SegmentMaker._comment_measure_numbers()
                                e'4.                                                             %! baca.make_notes()
        <BLANKLINE>
                                % [Violin_Music_Voice measure 3]                                 %! baca.SegmentMaker._comment_measure_numbers()
                                e'2                                                              %! baca.make_notes()
        <BLANKLINE>
                                % [Violin_Music_Voice measure 4]                                 %! baca.SegmentMaker._comment_measure_numbers()
                                e'4.                                                             %! baca.make_notes()
                                <> \bacaStopTextSpanRhythmAnnotation                             %! baca.rhythm_annotation_spanner():RHYTHM_ANNOTATION_SPANNER:baca.PiecewiseCommand._call(4):SPANNER_STOP
        <BLANKLINE>
                            }   %*% PartAssignment('Violin')
        <BLANKLINE>
                            <<                                                                   %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
        <BLANKLINE>
                                \context Voice = "Violin_Music_Voice"                            %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                {                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
        <BLANKLINE>
                                    % [Violin_Music_Voice measure 5]                             %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \abjad-invisible-music-coloring                              %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:NOTE:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                %@% \abjad-invisible-music                                       %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:NOTE:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                    \baca-not-yet-pitched-coloring                               %! baca.SegmentMaker._color_not_yet_pitched():NOT_YET_PITCHED_COLORING:HIDDEN:NOTE:baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    b'1 * 1/4                                                    %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:NOTE
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                 %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:NOTE:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
        <BLANKLINE>
                                }                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
        <BLANKLINE>
                                \context Voice = "Violin_Rest_Voice"                             %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                {                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
        <BLANKLINE>
                                    % [Violin_Rest_Voice measure 5]                              %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \once \override Score.TimeSignature.X-extent = ##f           %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                    \once \override MultiMeasureRest.transparent = ##t           %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                    \stopStaff                                                   %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \once \override Staff.StaffSymbol.transparent = ##t          %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \startStaff                                                  %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    R1 * 1/4                                                     %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                 %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
        <BLANKLINE>
                                }                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
        <BLANKLINE>
                            >>                                                                   %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
        <BLANKLINE>
                        }                                                                        %! baca.StringTrioScoreTemplate.__call__()
        <BLANKLINE>
                    }                                                                            %! baca.StringTrioScoreTemplate.__call__()
        <BLANKLINE>
                    \tag Viola                                                                   %! baca.ScoreTemplate._attach_liypond_tag()
                    \context ViolaMusicStaff = "Viola_Music_Staff"                               %! baca.StringTrioScoreTemplate.__call__()
                    {                                                                            %! baca.StringTrioScoreTemplate.__call__()
        <BLANKLINE>
                        \context ViolaMusicVoice = "Viola_Music_Voice"                           %! baca.StringTrioScoreTemplate.__call__()
                        {                                                                        %! baca.StringTrioScoreTemplate.__call__()
        <BLANKLINE>
                            % [Viola_Music_Voice measure 1]                                      %! baca.SegmentMaker._comment_measure_numbers()
                            \clef "alto"                                                         %! abjad.ScoreTemplate.attach_defaults(3):baca.SegmentMaker._set_status_tag():DEFAULT_CLEF
                            \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! baca.SegmentMaker._attach_color_literal(2):DEFAULT_CLEF_COLOR
                        %@% \override ViolaMusicStaff.Clef.color = ##f                           %! baca.SegmentMaker._attach_color_literal(1):DEFAULT_CLEF_COLOR_CANCELLATION
                            \set ViolaMusicStaff.forceClef = ##t                                 %! abjad.ScoreTemplate.attach_defaults(3):baca.SegmentMaker._treat_persistent_wrapper(2):baca.SegmentMaker._set_status_tag():DEFAULT_CLEF
                            R1 * 4/8                                                             %! baca.SegmentMaker._call_rhythm_commands()
                            ^ \baca-default-indicator-markup "(Viola)"                           %! DEFAULT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                        %@% ^ \baca-duration-multiplier-markup #"4" #"8"                         %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER
                            \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)          %! baca.SegmentMaker._attach_color_literal(2):DEFAULT_CLEF_REDRAW_COLOR
        <BLANKLINE>
                            % [Viola_Music_Voice measure 2]                                      %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                             %! baca.SegmentMaker._call_rhythm_commands()
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"                         %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER
        <BLANKLINE>
                            % [Viola_Music_Voice measure 3]                                      %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 4/8                                                             %! baca.SegmentMaker._call_rhythm_commands()
                        %@% ^ \baca-duration-multiplier-markup #"4" #"8"                         %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER
        <BLANKLINE>
                            % [Viola_Music_Voice measure 4]                                      %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                             %! baca.SegmentMaker._call_rhythm_commands()
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"                         %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER
        <BLANKLINE>
                            <<                                                                   %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
        <BLANKLINE>
                                \context Voice = "Viola_Music_Voice"                             %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                {                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
        <BLANKLINE>
                                    % [Viola_Music_Voice measure 5]                              %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \abjad-invisible-music-coloring                              %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:MULTIMEASURE_REST:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                %@% \abjad-invisible-music                                       %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:MULTIMEASURE_REST:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                    R1 * 1/4                                                     %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                 %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:MULTIMEASURE_REST:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
        <BLANKLINE>
                                }                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
        <BLANKLINE>
                                \context Voice = "Viola_Rest_Voice"                              %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                {                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
        <BLANKLINE>
                                    % [Viola_Rest_Voice measure 5]                               %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \once \override Score.TimeSignature.X-extent = ##f           %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                    \once \override MultiMeasureRest.transparent = ##t           %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                    \stopStaff                                                   %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \once \override Staff.StaffSymbol.transparent = ##t          %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \startStaff                                                  %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    R1 * 1/4                                                     %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                 %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
        <BLANKLINE>
                                }                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
        <BLANKLINE>
                            >>                                                                   %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
        <BLANKLINE>
                        }                                                                        %! baca.StringTrioScoreTemplate.__call__()
        <BLANKLINE>
                    }                                                                            %! baca.StringTrioScoreTemplate.__call__()
        <BLANKLINE>
                    \tag Cello                                                                   %! baca.ScoreTemplate._attach_liypond_tag()
                    \context CelloMusicStaff = "Cello_Music_Staff"                               %! baca.StringTrioScoreTemplate.__call__()
                    {                                                                            %! baca.StringTrioScoreTemplate.__call__()
        <BLANKLINE>
                        \context CelloMusicVoice = "Cello_Music_Voice"                           %! baca.StringTrioScoreTemplate.__call__()
                        {                                                                        %! baca.StringTrioScoreTemplate.__call__()
        <BLANKLINE>
                            % [Cello_Music_Voice measure 1]                                      %! baca.SegmentMaker._comment_measure_numbers()
                            \clef "bass"                                                         %! abjad.ScoreTemplate.attach_defaults(3):baca.SegmentMaker._set_status_tag():DEFAULT_CLEF
                            \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! baca.SegmentMaker._attach_color_literal(2):DEFAULT_CLEF_COLOR
                        %@% \override CelloMusicStaff.Clef.color = ##f                           %! baca.SegmentMaker._attach_color_literal(1):DEFAULT_CLEF_COLOR_CANCELLATION
                            \set CelloMusicStaff.forceClef = ##t                                 %! abjad.ScoreTemplate.attach_defaults(3):baca.SegmentMaker._treat_persistent_wrapper(2):baca.SegmentMaker._set_status_tag():DEFAULT_CLEF
                            R1 * 4/8                                                             %! baca.SegmentMaker._call_rhythm_commands()
                            ^ \baca-default-indicator-markup "(Cello)"                           %! DEFAULT_INSTRUMENT_ALERT:baca.SegmentMaker._attach_latent_indicator_alert()
                        %@% ^ \baca-duration-multiplier-markup #"4" #"8"                         %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER
                            \override CelloMusicStaff.Clef.color = #(x11-color 'violet)          %! baca.SegmentMaker._attach_color_literal(2):DEFAULT_CLEF_REDRAW_COLOR
        <BLANKLINE>
                            % [Cello_Music_Voice measure 2]                                      %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                             %! baca.SegmentMaker._call_rhythm_commands()
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"                         %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER
        <BLANKLINE>
                            % [Cello_Music_Voice measure 3]                                      %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 4/8                                                             %! baca.SegmentMaker._call_rhythm_commands()
                        %@% ^ \baca-duration-multiplier-markup #"4" #"8"                         %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER
        <BLANKLINE>
                            % [Cello_Music_Voice measure 4]                                      %! baca.SegmentMaker._comment_measure_numbers()
                            R1 * 3/8                                                             %! baca.SegmentMaker._call_rhythm_commands()
                        %@% ^ \baca-duration-multiplier-markup #"3" #"8"                         %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER
        <BLANKLINE>
                            <<                                                                   %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
        <BLANKLINE>
                                \context Voice = "Cello_Music_Voice"                             %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
                                {                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
        <BLANKLINE>
                                    % [Cello_Music_Voice measure 5]                              %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \abjad-invisible-music-coloring                              %! baca.SegmentMaker._make_multimeasure_rest_container(2):PHANTOM:MULTIMEASURE_REST:INVISIBLE_MUSIC_COLORING:baca.SegmentMaker._style_phantom_measures(5)
                                %@% \abjad-invisible-music                                       %! baca.SegmentMaker._make_multimeasure_rest_container(3):PHANTOM:MULTIMEASURE_REST:INVISIBLE_MUSIC_COMMAND:baca.SegmentMaker._style_phantom_measures(5)
                                    R1 * 1/4                                                     %! baca.SegmentMaker._make_multimeasure_rest_container(1):PHANTOM:HIDDEN:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                 %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:HIDDEN:MULTIMEASURE_REST:PHANTOM:baca.SegmentMaker._style_phantom_measures(5)
        <BLANKLINE>
                                }                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(4):PHANTOM
        <BLANKLINE>
                                \context Voice = "Cello_Rest_Voice"                              %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
                                {                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
        <BLANKLINE>
                                    % [Cello_Rest_Voice measure 5]                               %! baca.SegmentMaker._comment_measure_numbers():baca.SegmentMaker._style_phantom_measures(5):PHANTOM
                                    \once \override Score.TimeSignature.X-extent = ##f           %! baca.SegmentMaker._style_phantom_measures(6):PHANTOM
                                    \once \override MultiMeasureRest.transparent = ##t           %! baca.SegmentMaker._style_phantom_measures(7):PHANTOM
                                    \stopStaff                                                   %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \once \override Staff.StaffSymbol.transparent = ##t          %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    \startStaff                                                  %! baca.SegmentMaker._style_phantom_measures(8):PHANTOM
                                    R1 * 1/4                                                     %! baca.SegmentMaker._make_multimeasure_rest_container(5):PHANTOM:REST_VOICE:MULTIMEASURE_REST
                                %@% ^ \baca-duration-multiplier-markup #"1" #"4"                 %! baca.SegmentMaker._label_duration_multipliers():DURATION_MULTIPLIER:MULTIMEASURE_REST:PHANTOM:REST_VOICE:baca.SegmentMaker._style_phantom_measures(5)
        <BLANKLINE>
                                }                                                                %! baca.SegmentMaker._make_multimeasure_rest_container(6):PHANTOM
        <BLANKLINE>
                            >>                                                                   %! baca.SegmentMaker._make_multimeasure_rest_container(7):PHANTOM
        <BLANKLINE>
                        }                                                                        %! baca.StringTrioScoreTemplate.__call__()
        <BLANKLINE>
                    }                                                                            %! baca.StringTrioScoreTemplate.__call__()
        <BLANKLINE>
                >>                                                                               %! baca.StringTrioScoreTemplate.__call__()
        <BLANKLINE>
            >>                                                                                   %! baca.StringTrioScoreTemplate.__call__()
        <BLANKLINE>
        >>                                                                                       %! baca.StringTrioScoreTemplate.__call__()

    ..  container:: example exception

        Raises exception when voice does not allow part assignment:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     test_container_identifiers=True,
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> part_assignment = abjad.PartAssignment('Flute')

        >>> maker(
        ...     'Violin_Music_Voice',
        ...     baca.make_notes(),
        ...     baca.parts(part_assignment),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        Traceback (most recent call last):
            ...
        Exception: Violin_Music_Voice does not allow Flute part assignment:
            abjad.PartAssignment('Flute')

    """
    if not isinstance(part_assignment, abjad.PartAssignment):
        message = "part_assignment must be part assignment"
        message += f" (not {part_assignment!r})."
        raise Exception(message)
    return commandclasses.PartAssignmentCommand(
        part_assignment=part_assignment, selector=selector
    )


def one_voice(
    selector: abjad.Expression = classes.Expression().select().leaf(0),
) -> commandclasses.IndicatorCommand:
    r"""
    Makes LilyPond ``\oneVoice`` command.
    """
    literal = abjad.LilyPondLiteral(r"\oneVoice")
    return commandclasses.IndicatorCommand(
        indicators=[literal], selector=selector, tags=[_site(inspect.currentframe())],
    )


def open_volta(
    selector: abjad.Expression = classes.Expression().select().leaf(0),
) -> scoping.Suite:
    """
    Attaches bar line and overrides bar line X-extent.
    """
    return scoping.suite(
        indicatorcommands.bar_line(".|:", selector, format_slot="before"),
        scoping.not_mol(overrides.bar_line_x_extent((0, 2), selector)),
        scoping.only_mol(overrides.bar_line_x_extent((0, 3), selector)),
    )


def previous_metadata(path: str) -> abjad.OrderedDict:
    """
    Gets previous segment metadata before ``path``.
    """
    # reproduces abjad.Path.get_previous_path()
    # because Travis isn't configured for scores-directory calculations
    definition_py = abjad.Path(path)
    segment = abjad.Path(definition_py).parent
    assert segment.is_segment(), repr(segment)
    segments = segment.parent
    assert segments.is_segments(), repr(segments)
    paths = segments.list_paths()
    paths = [_ for _ in paths if not _.name.startswith(".")]
    assert all(_.is_dir() for _ in paths), repr(paths)
    index = paths.index(segment)
    if index == 0:
        return abjad.OrderedDict()
    previous_index = index - 1
    previous_segment = paths[previous_index]
    previous_metadata = previous_segment.get_metadata()
    return previous_metadata


def select(items=None):
    if items is None:
        return classes.Expression().select()
    return classes.Selection(items=items)


def sequence(items=None, **keywords):
    if items is None:
        return classes.Expression().sequence(**keywords)
    return classes.Sequence(items=items, **keywords)


def untie(selector: abjad.Expression) -> commandclasses.DetachCommand:
    """
    Makes (repeat-)tie detach command.
    """
    return commandclasses.DetachCommand([abjad.Tie, abjad.RepeatTie], selector=selector)


def voice_four(
    selector: abjad.Expression = classes.Expression().select().leaf(0),
) -> commandclasses.IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceFour`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceFour")
    return commandclasses.IndicatorCommand(
        indicators=[literal], selector=selector, tags=[_site(inspect.currentframe())],
    )


def voice_one(
    selector: abjad.Expression = classes.Expression().select().leaf(0),
) -> commandclasses.IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceOne`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceOne")
    return commandclasses.IndicatorCommand(
        indicators=[literal], selector=selector, tags=[_site(inspect.currentframe())],
    )


def voice_three(
    selector: abjad.Expression = classes.Expression().select().leaf(0),
) -> commandclasses.IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceThree`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceThree")
    return commandclasses.IndicatorCommand(
        indicators=[literal], selector=selector, tags=[_site(inspect.currentframe())],
    )


def voice_two(
    selector: abjad.Expression = classes.Expression().select().leaf(0),
) -> commandclasses.IndicatorCommand:
    r"""
    Makes LilyPond ``\voiceTwo`` command.
    """
    literal = abjad.LilyPondLiteral(r"\voiceTwo")
    return commandclasses.IndicatorCommand(
        indicators=[literal], selector=selector, tags=[_site(inspect.currentframe())],
    )
