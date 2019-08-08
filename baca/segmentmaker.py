import abjad
import copy
import os
import pathlib
import sys
import traceback
import typing
from abjadext import rmakers
from . import classes
from . import commands as baca_commands
from . import const
from . import indicators
from . import markups
from . import overrides as baca_overrides
from . import pitchclasses
from . import rhythmcommands
from . import scoping
from . import segmentclasses
from . import templates
from . import typings


class SegmentMaker(abjad.SegmentMaker):
    r"""
    Segment-maker.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     do_not_color_unpitched_music=True,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_even_divisions(),
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
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 1/2                                                                     %! _make_global_skips(1)
            <BLANKLINE>
                        % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                        \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                        s1 * 3/8                                                                     %! _make_global_skips(1)
                        \baca-bar-line-visible                                                       %! _attach_final_bar_line
                        \bar "|"                                                                     %! _attach_final_bar_line
            <BLANKLINE>
                        % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                            [                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                            c'8                                                                      %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                            c'8                                                                      %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                            c'8                                                                      %! baca.make_even_divisions
                            [                                                                        %! baca.make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
            <BLANKLINE>
                            c'8                                                                      %! baca.make_even_divisions
                            ]                                                                        %! baca.make_even_divisions
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

    __documentation_section__ = "Classes"

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        "_activate",
        "_allow_empty_selections",
        "_breaks",
        "_cache",
        "_cached_time_signatures",
        "_clock_time_extra_offset",
        "_clock_time_override",
        "_color_octaves",
        "_commands",
        "_deactivate",
        "_do_not_check_out_of_range_pitches",
        "_do_not_check_persistence",
        "_do_not_check_wellformedness",
        "_do_not_color_out_of_range_pitches",
        "_do_not_color_repeat_pitch_classes",
        "_do_not_color_unpitched_music",
        "_do_not_color_unregistered_pitches",
        "_do_not_include_layout_ly",
        "_do_not_force_nonnatural_accidentals",
        "_duration",
        "_environment",
        "_fermata_measure_empty_overrides",
        "_fermata_measure_numbers",
        "_fermata_measure_staff_line_count",
        "_fermata_start_offsets",
        "_fermata_stop_offsets",
        "_final_bar_line",
        "_final_markup",
        "_final_markup_extra_offset",
        "_final_measure_is_fermata",
        "_first_measure_number",
        "_final_segment",
        "_first_segment",
        "_ignore_repeat_pitch_classes",
        "_includes",
        "_instruments",
        "_local_measure_number_extra_offset",
        "_magnify_staves",
        "_margin_markups",
        "_measure_number_extra_offset",
        "_metronome_marks",
        "_midi",
        "_nonfirst_segment_lilypond_include",
        "_offset_to_measure_number",
        "_previously_alive_contexts",
        "_remove_phantom_measure",
        "_score",
        "_score_template",
        "_segment_bol_measure_numbers",
        "_segment_directory",
        "_segment_duration",
        "_skips_instead_of_rests",
        "_sounds_during_segment",
        "_spacing",
        "_spacing_extra_offset",
        "_stage_markup",
        "_stage_number_extra_offset",
        "_start_clock_time",
        "_stop_clock_time",
        "_test_container_identifiers",
        "_time_signatures",
        "_transpose_score",
        "_validate_measure_count",
        "_voice_metadata",
        "_voice_names",
    )

    _absolute_string_trio_stylesheet_path = pathlib.Path(
        "/",
        "Users",
        "trevorbaca",
        "baca",
        "docs",
        "source",
        "_stylesheets",
        "string-trio.ily",
    )

    _absolute_two_voice_staff_stylesheet_path = pathlib.Path(
        "/",
        "Users",
        "trevorbaca",
        "baca",
        "docs",
        "source",
        "_stylesheets",
        "two-voice-staff.ily",
    )

    _prototype_to_manifest_name = {
        "abjad.Instrument": "instruments",
        "abjad.MetronomeMark": "metronome_marks",
        "abjad.MarginMarkup": "margin_markups",
    }

    _publish_storage_format = True

    _status_to_color = {
        "default": "DarkViolet",
        "explicit": "blue",
        "reapplied": "green4",
        "redundant": "DeepPink1",
    }

    _status_to_markup_function = {
        "default": "baca-default-indicator-markup",
        "explicit": "baca-explicit-indicator-markup",
        "reapplied": "baca-reapplied-indicator-markup",
        "redundant": "baca-redundant-indicator-markup",
    }

    _status_to_redraw_color = {
        "default": "violet",
        "explicit": "DeepSkyBlue2",
        "reapplied": "OliveDrab",
        "redundant": "DeepPink4",
    }

    _score_package_stylesheet_path = pathlib.Path(
        "..", "..", "stylesheets", "stylesheet.ily"
    )

    _score_package_nonfirst_segment_path = pathlib.Path(
        "..", "..", "stylesheets", "nonfirst-segment.ily"
    )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        activate: typing.List[str] = None,
        allow_empty_selections: bool = None,
        breaks: segmentclasses.BreakMeasureMap = None,
        clock_time_extra_offset: typing.Union[bool, typings.Pair] = None,
        clock_time_override: abjad.MetronomeMark = None,
        color_octaves: bool = None,
        deactivate: typing.List[str] = None,
        do_not_check_out_of_range_pitches: bool = None,
        do_not_check_persistence: bool = None,
        do_not_check_wellformedness: bool = None,
        do_not_color_out_of_range_pitches: bool = None,
        do_not_color_repeat_pitch_classes: bool = None,
        do_not_color_unpitched_music: bool = None,
        do_not_color_unregistered_pitches: bool = None,
        do_not_force_nonnatural_accidentals: bool = None,
        do_not_include_layout_ly: bool = None,
        fermata_measure_empty_overrides: typing.Sequence[int] = None,
        fermata_measure_staff_line_count: int = None,
        final_bar_line: typing.Union[bool, str] = None,
        final_markup: tuple = None,
        final_markup_extra_offset: abjad.NumberPair = None,
        final_segment: bool = None,
        first_measure_number: int = None,
        first_segment: bool = None,
        ignore_repeat_pitch_classes: bool = None,
        includes: typing.Sequence[str] = None,
        instruments: abjad.OrderedDict = None,
        local_measure_number_extra_offset: typing.Union[
            bool, typings.Pair
        ] = None,
        magnify_staves: typing.Union[
            abjad.Multiplier, typing.Tuple[abjad.Multiplier, str]
        ] = None,
        margin_markups: abjad.OrderedDict = None,
        measure_number_extra_offset: typing.Union[bool, typings.Pair] = None,
        metronome_marks: abjad.OrderedDict = None,
        nonfirst_segment_lilypond_include: bool = None,
        phantom: bool = None,
        remove_phantom_measure: bool = None,
        score_template: templates.ScoreTemplate = None,
        segment_directory: abjad.Path = None,
        skips_instead_of_rests: bool = None,
        spacing: segmentclasses.HorizontalSpacingSpecifier = None,
        spacing_extra_offset: typing.Union[bool, typings.Pair] = None,
        stage_markup: typing.Sequence[typing.Tuple] = None,
        stage_number_extra_offset: typing.Union[bool, typings.Pair] = None,
        test_container_identifiers: bool = None,
        time_signatures: typing.Sequence[
            typing.Union[
                abjad.NonreducedFraction,
                abjad.TimeSignature,
                abjad.IntegerPair,
            ]
        ] = None,
        transpose_score: bool = None,
        validate_measure_count: int = None,
    ) -> None:
        super().__init__()
        self._activate = activate
        self._allow_empty_selections = allow_empty_selections
        self._breaks = breaks
        if clock_time_extra_offset not in (False, None):
            assert isinstance(clock_time_extra_offset, tuple)
            assert len(clock_time_extra_offset) == 2
        self._clock_time_extra_offset = clock_time_extra_offset
        if clock_time_override is not None:
            assert isinstance(clock_time_override, abjad.MetronomeMark)
        self._clock_time_override = clock_time_override
        self._color_octaves = color_octaves
        self._cache = None
        self._cached_time_signatures: typing.List[abjad.TimeSignature] = []
        self._deactivate = deactivate
        if do_not_check_out_of_range_pitches is not None:
            do_not_check_out_of_range_pitches = bool(
                do_not_check_out_of_range_pitches
            )
        self._do_not_check_out_of_range_pitches = (
            do_not_check_out_of_range_pitches
        )
        self._do_not_check_persistence = do_not_check_persistence
        self._do_not_check_wellformedness = do_not_check_wellformedness
        self._do_not_color_out_of_range_pitches = (
            do_not_color_out_of_range_pitches
        )
        self._do_not_color_repeat_pitch_classes = (
            do_not_color_repeat_pitch_classes
        )
        self._do_not_color_unpitched_music = do_not_color_unpitched_music
        self._do_not_color_unregistered_pitches = (
            do_not_color_unregistered_pitches
        )
        self._do_not_force_nonnatural_accidentals = (
            do_not_force_nonnatural_accidentals
        )
        self._do_not_include_layout_ly = do_not_include_layout_ly
        self._duration: typing.Optional[abjad.DurationTyping] = None
        self._fermata_measure_empty_overrides = fermata_measure_empty_overrides
        self._fermata_measure_numbers: typing.List = []
        self._fermata_measure_staff_line_count = (
            fermata_measure_staff_line_count
        )
        self._fermata_start_offsets: typing.List[abjad.Offset] = []
        self._fermata_stop_offsets: typing.List[abjad.Offset] = []
        if final_bar_line is not None:
            assert isinstance(final_bar_line, (bool, str))
        self._final_bar_line = final_bar_line
        self._final_markup = final_markup
        self._final_markup_extra_offset = final_markup_extra_offset
        self._first_measure_number = first_measure_number
        if first_segment is not None:
            first_segment = bool(first_segment)
        self._first_segment = first_segment
        self._ignore_repeat_pitch_classes = ignore_repeat_pitch_classes
        self._nonfirst_segment_lilypond_include = (
            nonfirst_segment_lilypond_include
        )
        self._instruments = instruments
        self._final_measure_is_fermata = False
        self._final_segment = final_segment
        self._includes = includes
        self._local_measure_number_extra_offset = (
            local_measure_number_extra_offset
        )
        self._magnify_staves = magnify_staves
        self._margin_markups = margin_markups
        self._measure_number_extra_offset = measure_number_extra_offset
        self._metronome_marks = metronome_marks
        self._midi: typing.Optional[bool] = None
        self._offset_to_measure_number: typing.Dict[abjad.Offset, int] = {}
        self._previously_alive_contexts: typing.List[str] = []
        if remove_phantom_measure is not None:
            remove_phantom_measure = bool(remove_phantom_measure)
        self._remove_phantom_measure = remove_phantom_measure
        self._score_template = score_template
        self._segment_bol_measure_numbers: typing.List[int] = []
        if segment_directory is not None:
            segment_directory = abjad.Path(
                segment_directory,
                scores=segment_directory.parent.parent.parent.parent,
            )
        self._segment_directory: typing.Optional[
            abjad.Path
        ] = segment_directory
        self._segment_duration: typing.Optional[abjad.DurationTyping] = None
        self._skips_instead_of_rests = skips_instead_of_rests
        self._sounds_during_segment: abjad.OrderedDict = abjad.OrderedDict()
        self._spacing = spacing
        self._spacing_extra_offset = spacing_extra_offset
        self._stage_markup = stage_markup
        self._stage_number_extra_offset = stage_number_extra_offset
        self._start_clock_time: typing.Optional[str] = None
        self._stop_clock_time: typing.Optional[str] = None
        if test_container_identifiers is not None:
            test_container_identifiers = bool(test_container_identifiers)
        self._test_container_identifiers = test_container_identifiers
        self._transpose_score = transpose_score
        self._validate_measure_count = validate_measure_count
        self._voice_metadata: abjad.OrderedDict = abjad.OrderedDict()
        self._voice_names: typing.Optional[typing.Tuple[str, ...]] = None
        self._commands: typing.List[scoping.Command] = []
        self._import_manifests()
        self._initialize_time_signatures(time_signatures)
        self._validate_measure_count_()

    ### SPECIAL METHODS ###

    def __call__(
        self,
        scopes: typing.Union[
            scoping.Scope, scoping.TimelineScope, typings.ScopeTyping
        ],
        *commands: typing.Union[scoping.Command, scoping.Suite, None],
    ) -> None:
        r"""
        Wraps each command in ``commands`` with each scope in ``scopes``.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.make_even_divisions(),
            ...     baca.label(abjad.label().with_indices()),
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
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 0 }
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 1 }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 2 }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 3 }
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 4 }
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 5 }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 6 }
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 7 }
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 8 }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 9 }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 10 }
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 11 }
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 12 }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 13 }
                                ]                                                                        %! baca.make_even_divisions
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

        ..  container:: example

            Commands may be grouped into lists:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> commands = []
            >>> commands.append(baca.make_even_divisions())
            >>> commands.append(baca.label(abjad.label().with_indices()))

            >>> maker(
            ...     'Music_Voice',
            ...     commands,
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
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 0 }
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 1 }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 2 }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 3 }
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 4 }
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 5 }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 6 }
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 7 }
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 8 }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 9 }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 10 }
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 11 }
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 12 }
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ^ \markup { 13 }
                                ]                                                                        %! baca.make_even_divisions
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

        ..  container:: example exception

            Raises exception on noncommand input:

            >>> maker(
            ...     'Music_Voice',
            ...     'text',
            ...     )
            Traceback (most recent call last):
                ...
            Exception: 
            <BLANKLINE>
            Must be command:
            <BLANKLINE>
            text

        ..  container:: example exception

            Raises exception on unknown voice name:

            >>> maker(
            ...     'Percussion_Voice',
            ...     baca.make_repeated_duration_notes([(1, 4)]),
            ...     )
            Traceback (most recent call last):
                ...
            Exception: unknown voice name 'Percussion_Voice'.

        """
        commands_ = classes.Sequence(commands).flatten(
            classes=(list, scoping.Suite), depth=-1
        )
        commands = tuple(commands_)
        if self.score_template is not None:
            self._cache_voice_names()
            abbreviations = self.score_template.voice_abbreviations
        else:
            abbreviations = abjad.OrderedDict()
        abbreviations = abbreviations or abjad.OrderedDict()
        scopes_ = self._unpack_scopes(scopes, abbreviations)
        scope_type = (scoping.Scope, scoping.TimelineScope)
        assert all(isinstance(_, scope_type) for _ in scopes_), repr(scopes_)
        for command in commands:
            if command is None:
                continue
            if isinstance(command, list):
                raise Exception("use baca.suite().")
            if not isinstance(command, scoping.Command):
                message = "\n\nMust be command:"
                message += f"\n\n{format(command)}"
                raise Exception(message)
        scope_count = len(scopes_)
        for i, current_scope in enumerate(scopes_):
            if (
                self._voice_names
                and current_scope.voice_name not in self._voice_names
            ):
                message = f"unknown voice name {current_scope.voice_name!r}."
                raise Exception(message)
            if isinstance(current_scope, scoping.TimelineScope):
                for scope_ in current_scope.scopes:
                    if scope_.voice_name in abbreviations:
                        voice_name = abbreviations[scope_.voice_name]
                        scope_._voice_name = voice_name
            for command in commands:
                if command is None:
                    continue
                assert isinstance(command, scoping.Command), repr(command)
                if not command._matches_scope_index(scope_count, i):
                    continue
                if isinstance(command, scoping.Command):
                    commands_ = [command]
                else:
                    commands_ = command
                for command_ in commands_:
                    assert isinstance(command_, scoping.Command), repr(
                        command_
                    )
                    measures = command_.measures
                    if isinstance(measures, int):
                        measures = (measures, measures)
                    if measures is not None:
                        scope_ = abjad.new(current_scope, measures=measures)
                    else:
                        scope_ = abjad.new(current_scope)
                    command_ = abjad.new(command_, scope=scope_)
                    self.commands.append(command_)

    ### PRIVATE METHODS ###

    def _activate_tags(self, tags):
        tags = tags or []
        tags = set(tags)
        tags.update(self.activate or [])
        if not tags:
            return
        for leaf in abjad.iterate(self.score).leaves():
            if not isinstance(leaf, abjad.Skip):
                continue
            wrappers = abjad.inspect(leaf).wrappers()
            for wrapper in wrappers:
                if wrapper.tag is None:
                    continue
                for tag in tags:
                    if tag in wrapper.tag:
                        wrapper.deactivate = False
                        break

    def _add_final_markup(self):
        if self.final_markup is None:
            return
        if isinstance(self.final_markup, abjad.Markup):
            final_markup = self.final_markup
        else:
            final_markup = markups.final_markup(*self.final_markup)
        assert isinstance(final_markup, abjad.Markup)
        command = baca_commands.markup(
            final_markup, selector="baca.leaf(-1)", direction=abjad.Down
        )
        self.score.add_final_markup(
            command.indicators[0], extra_offset=self.final_markup_extra_offset
        )

    def _alive_during_any_previous_segment(self, context) -> bool:
        assert isinstance(context, abjad.Context), repr(context)
        assert self.previous_persist is not None
        names: typing.List = self.previous_persist.get(
            "alive_during_segment", []
        )
        return context.name in names

    def _alive_during_previous_segment(self, context) -> bool:
        assert isinstance(context, abjad.Context), repr(context)
        assert self.previous_persist is not None
        names: typing.List = self.previous_persist.get(
            "alive_during_segment", []
        )
        return context.name in names

    def _analyze_momento(self, context, momento):
        previous_indicator = self._momento_to_indicator(momento)
        if previous_indicator is None:
            return
        if isinstance(previous_indicator, indicators.SpacingSection):
            return
        if momento.context in self.score:
            # momento_context = self.score[momento.context]
            for context in abjad.iterate(self.score).components(abjad.Context):
                if context.name == momento.context:
                    momento_context = context
                    break
        else:
            # context alive in previous segment doesn't exist in this segment
            return
        leaf = abjad.inspect(momento_context).leaf(0)
        if isinstance(previous_indicator, abjad.Instrument):
            prototype = abjad.Instrument
        else:
            prototype = type(previous_indicator)
        indicator = abjad.inspect(leaf).indicator(prototype)
        status = None
        if indicator is None:
            status = "reapplied"
        elif not scoping.compare_persistent_indicators(
            previous_indicator, indicator
        ):
            status = "explicit"
        elif isinstance(previous_indicator, abjad.TimeSignature):
            status = "reapplied"
        else:
            status = "redundant"
        edition = momento.edition or abjad.Tag()
        return leaf, previous_indicator, status, edition

    def _annotate_sounds_during(self):
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            pleaves = []
            for pleaf in classes.Selection(voice).pleaves():
                if abjad.inspect(pleaf).annotation(const.PHANTOM):
                    continue
                pleaves.append(pleaf)
            value = bool(pleaves)
            abjad.annotate(voice, const.SOUNDS_DURING_SEGMENT, value)

    def _apply_breaks(self):
        if self.breaks is None:
            return
        self.breaks(self.score["Global_Skips"])
        if self.breaks.local_measure_numbers:
            abjad.setting(self.score).current_bar_number = 1

    def _apply_spacing(self):
        if self.spacing is None:
            return
        with abjad.Timer() as timer:
            self.spacing(self)
        if os.getenv("TRAVIS"):
            return
        count = int(timer.elapsed_time)
        if False:
            seconds = abjad.String("second").pluralize(count)
            message = f" Spacing application {count} {seconds} ..."
            raise Exception(f"spacing application {count} {seconds}!")
        return count

    def _assert_nonoverlapping_rhythms(self, rhythms, voice):
        previous_stop_offset = 0
        for rhythm in rhythms:
            start_offset = rhythm.start_offset
            if start_offset < previous_stop_offset:
                raise Exception(f"{voice} has overlapping rhythms.")
            duration = abjad.inspect(rhythm.annotation).duration()
            stop_offset = start_offset + duration
            previous_stop_offset = stop_offset

    @staticmethod
    def _attach_color_cancelation_literal(
        wrapper, status, existing_deactivate=None, existing_tag=None
    ):
        if getattr(wrapper.indicator, "latent", False):
            return
        if getattr(wrapper.indicator, "hide", False):
            return
        if not getattr(wrapper.indicator, "redraw", False):
            return
        SegmentMaker._attach_color_literal(
            wrapper,
            status,
            existing_deactivate=wrapper.deactivate,
            cancelation=True,
        )

    @staticmethod
    def _attach_color_literal(
        wrapper,
        status,
        existing_deactivate=None,
        redraw=False,
        cancelation=False,
    ):
        assert isinstance(wrapper, abjad.Wrapper), repr(wrapper)
        if getattr(wrapper.indicator, "hide", False) is True:
            return
        if isinstance(wrapper.indicator, abjad.Instrument):
            return
        if not getattr(wrapper.indicator, "persistent", False):
            return
        if getattr(wrapper.indicator, "parameter", None) == "METRONOME_MARK":
            return
        if isinstance(wrapper.indicator, abjad.PersistentOverride):
            return
        stem = abjad.String.to_indicator_stem(wrapper.indicator)
        grob = SegmentMaker._indicator_to_grob(wrapper.indicator)
        context = wrapper._find_correct_effective_context()
        assert isinstance(context, abjad.Context), repr(context)
        string = rf"\override {context.lilypond_type}.{grob}.color ="
        if cancelation is True:
            string += " ##f"
        elif redraw is True:
            color = SegmentMaker._status_to_redraw_color[status]
            string += f" #(x11-color '{color})"
        else:
            string = rf"\once {string}"
            color = SegmentMaker._status_to_color[status]
            string += f" #(x11-color '{color})"
        if redraw:
            literal = abjad.LilyPondLiteral(string, "after")
        else:
            literal = abjad.LilyPondLiteral(string)
        if getattr(wrapper.indicator, "latent", False):
            if redraw:
                prefix = "redrawn"
            else:
                prefix = None
            if cancelation:
                suffix = "color_cancellation"
            else:
                suffix = "color"
        else:
            prefix = None
            if redraw:
                suffix = "redraw_color"
            elif cancelation:
                suffix = "color_cancellation"
            else:
                suffix = "color"
        status_tag = SegmentMaker._get_tag(
            status, stem, prefix=prefix, suffix=suffix
        )
        if isinstance(wrapper.indicator, abjad.TimeSignature):
            string = rf"\baca-time-signature-color #'{color}"
            literal = abjad.LilyPondLiteral(string)
        if cancelation is True:
            tag = abjad.Tag("_attach_color_literal(1)")
            tag = tag.prepend(status_tag)
            abjad.attach(literal, wrapper.component, deactivate=True, tag=tag)
        else:
            tag = abjad.Tag("_attach_color_literal(2)")
            tag = tag.prepend(status_tag)
            abjad.attach(
                literal,
                wrapper.component,
                deactivate=existing_deactivate,
                tag=tag,
            )

    @staticmethod
    def _attach_color_redraw_literal(
        wrapper, status, existing_deactivate=None, existing_tag=None
    ):
        if not getattr(wrapper.indicator, "redraw", False):
            return
        if getattr(wrapper.indicator, "hide", False):
            return
        SegmentMaker._attach_color_literal(
            wrapper,
            status,
            existing_deactivate=wrapper.deactivate,
            redraw=True,
        )

    def _attach_fermatas(self):
        always_make_global_rests = self.score_template.always_make_global_rests
        if not always_make_global_rests:
            del self.score["Global_Rests"]
            return
        has_fermata = False
        if not has_fermata and not always_make_global_rests:
            del self.score["Global_Rests"]
            return
        context = self.score["Global_Rests"]
        rests = self._make_global_rests()
        context.extend(rests)

    def _attach_final_bar_line(self):
        if self.final_bar_line is False:
            return
        strings = []
        abbreviation = "|"
        if self.final_segment:
            abbreviation = "|."
        if isinstance(self.final_bar_line, str):
            abbreviation = self.final_bar_line
        strings.append(r"\baca-bar-line-visible")
        strings.append(rf'\bar "{abbreviation}"')
        literal = abjad.LilyPondLiteral(strings, "after")
        skips = classes.Selection(self.score["Global_Skips"]).skips()
        if self.remove_phantom_measure:
            skip = skips[-1]
        else:
            skip = skips[-2]
        abjad.attach(literal, skip, tag="_attach_final_bar_line")

    def _attach_first_appearance_score_template_defaults(self):
        if self.first_segment:
            return
        staff__group = (abjad.Staff, abjad.StaffGroup)
        dictionary = self.previous_persist["persistent_indicators"]
        for staff__group in abjad.iterate(self.score).components(staff__group):
            if staff__group.name in dictionary:
                continue
            for wrapper in self.score_template.attach_defaults(staff__group):
                self._treat_persistent_wrapper(
                    self.manifests, wrapper, "default"
                )

    def _attach_first_segment_score_template_defaults(self):
        if not self.first_segment:
            return
        for wrapper in self.score_template.attach_defaults(self.score):
            self._treat_persistent_wrapper(self.manifests, wrapper, "default")

    @staticmethod
    def _attach_latent_indicator_alert(
        manifests, wrapper, status, existing_deactivate=None
    ):
        if not getattr(wrapper.indicator, "latent", False):
            return
        leaf = wrapper.component
        indicator = wrapper.indicator
        assert indicator.latent, repr(indicator)
        if isinstance(indicator, abjad.Clef):
            return
        key = SegmentMaker._indicator_to_key(indicator, manifests)
        if key is not None:
            key = f"“{key}”"
        else:
            key = type(indicator).__name__
        if isinstance(indicator, abjad.Instrument):
            if status == "default":
                tag = abjad.tags.DEFAULT_INSTRUMENT_ALERT
            elif status == "explicit":
                tag = abjad.tags.EXPLICIT_INSTRUMENT_ALERT
            elif status == "reapplied":
                tag = abjad.tags.REAPPLIED_INSTRUMENT_ALERT
            else:
                assert status == "redundant", repr(status)
                tag = abjad.tags.REDUNDANT_INSTRUMENT_ALERT
            left, right = "(", ")"
        else:
            assert isinstance(indicator, abjad.MarginMarkup)
            if status == "default":
                tag = abjad.tags.DEFAULT_MARGIN_MARKUP_ALERT
            elif status == "explicit":
                tag = abjad.tags.EXPLICIT_MARGIN_MARKUP_ALERT
            elif status == "reapplied":
                tag = abjad.tags.REAPPLIED_MARGIN_MARKUP_ALERT
            else:
                assert status == "redundant", repr(status)
                tag = abjad.tags.REDUNDANT_MARGIN_MARKUP_ALERT
            left, right = "[", "]"
        tag = abjad.Tag(tag)
        string = f"{left}{key}{right}"
        markup_function = SegmentMaker._status_to_markup_function[status]
        string = fr'\{markup_function} "{string}"'
        markup = abjad.Markup(string, direction=abjad.Up, literal=True)
        tag = tag.append("_attach_latent_indicator_alert")
        abjad.attach(markup, leaf, deactivate=existing_deactivate, tag=tag)

    def _attach_metronome_marks(self):
        indicator_count = 0
        skips = classes.Selection(self.score["Global_Skips"]).skips()
        final_leaf_metronome_mark = abjad.inspect(skips[-1]).indicator(
            abjad.MetronomeMark
        )
        add_right_text_to_me = None
        if final_leaf_metronome_mark:
            tempo_prototype = (
                abjad.MetronomeMark,
                indicators.Accelerando,
                indicators.Ritardando,
            )
            for skip in reversed(skips[:-1]):
                if abjad.inspect(skip).has_indicator(tempo_prototype):
                    add_right_text_to_me = skip
                    break
        for i, skip in enumerate(skips):
            inspection = abjad.inspect(skip)
            metronome_mark = inspection.indicator(abjad.MetronomeMark)
            metric_modulation = inspection.indicator(abjad.MetricModulation)
            accelerando = inspection.indicator(indicators.Accelerando)
            ritardando = inspection.indicator(indicators.Ritardando)
            if (
                metronome_mark is None
                and metric_modulation is None
                and accelerando is None
                and ritardando is None
            ):
                continue
            if metronome_mark is not None:
                metronome_mark._hide = True
                wrapper = inspection.wrapper(abjad.MetronomeMark)
            if metric_modulation is not None:
                metric_modulation._hide = True
            if accelerando is not None:
                accelerando._hide = True
            if ritardando is not None:
                ritardando._hide = True
            if skip is skips[-1]:
                break
            if metronome_mark is None and metric_modulation is not None:
                wrapper = inspection.wrapper(abjad.MetricModulation)
            if metronome_mark is None and accelerando is not None:
                wrapper = inspection.wrapper(indicators.Accelerando)
            if metronome_mark is None and ritardando is not None:
                wrapper = inspection.wrapper(indicators.Ritardando)
            has_trend = accelerando is not None or ritardando is not None
            indicator_count += 1
            tag = wrapper.tag
            if metronome_mark is not None:
                if metric_modulation is not None:
                    if metronome_mark.custom_markup is not None:
                        left_text = metronome_mark._get_markup()
                        markups = []
                        markups.append(left_text)
                        markups.append(abjad.Markup.hspace(2))
                        markups.append(abjad.Markup("[").upright())
                        modulation = metric_modulation._get_markup()
                        if modulation.contents[0].startswith(r"\markup"):
                            string = modulation.contents[0][8:]
                            modulation = abjad.Markup(string, literal=True)
                        modulation = abjad.Markup.line([modulation])
                        markups.append(modulation)
                        markups.append(abjad.Markup.hspace(0.5))
                        markups.append(abjad.Markup("]").upright())
                        left_text = abjad.Markup.concat(markups)
                    else:
                        left_text = self._bracket_metric_modulation(
                            metronome_mark, metric_modulation
                        )
                elif metronome_mark.custom_markup is not None:
                    assert metronome_mark.custom_markup.literal
                    left_text = r"- \baca-metronome-mark-spanner-left-markup"
                    string = format(metronome_mark.custom_markup)
                    assert string.startswith("\\")
                    left_text += f" {string}"
                # mixed number
                elif metronome_mark.decimal is True:
                    arguments = metronome_mark._get_markup_arguments()
                    log, dots, stem, base, n, d = arguments
                    left_text = r"- \baca-metronome-mark-spanner-left-text-mixed-number"
                    left_text += f' {log} {dots} {stem} "{base}" "{n}" "{d}"'
                else:
                    arguments = metronome_mark._get_markup_arguments()
                    log, dots, stem, value = arguments
                    left_text = r"- \baca-metronome-mark-spanner-left-text"
                    left_text += f' {log} {dots} {stem} "{value}"'
            elif accelerando is not None:
                left_text = accelerando._get_markup()
            elif ritardando is not None:
                left_text = ritardando._get_markup()
            if has_trend:
                style = "dashed-line-with-arrow"
            else:
                style = "invisible-line"
            if 0 < i:
                stop_text_span = abjad.StopTextSpan(
                    command=r"\bacaStopTextSpanMM"
                )
                abjad.attach(
                    stop_text_span, skip, tag="_attach_metronome_marks(1)"
                )
            if add_right_text_to_me is skip:
                right_text = final_leaf_metronome_mark._get_markup()
            else:
                right_text = None
            start_text_span = abjad.StartTextSpan(
                command=r"\bacaStartTextSpanMM",
                left_text=left_text,
                right_text=right_text,
                style=style,
            )
            assert "METRONOME_MARK" in str(tag), repr(tag)
            if (
                isinstance(wrapper.indicator, abjad.MetronomeMark)
                and has_trend
                and "EXPLICIT" not in str(tag)
            ):
                words = []
                for word in str(tag).split(":"):
                    if "METRONOME_MARK" in word:
                        word = word.replace("DEFAULT", "EXPLICIT")
                        word = word.replace("REAPPLIED", "EXPLICIT")
                        word = word.replace("REDUNDANT", "EXPLICIT")
                    words.append(word)
                new_tag = abjad.Tag.from_words(words)
                indicator = wrapper.indicator
                abjad.detach(wrapper, skip)
                abjad.attach(
                    indicator,
                    skip,
                    tag=new_tag.append("_attach_metronome_marks(5)"),
                )
                tag = new_tag
            abjad.attach(
                start_text_span,
                skip,
                deactivate=True,
                tag=tag.append("_attach_metronome_marks(2)"),
            )
            string = str(tag)
            if "DEFAULT" in string:
                status = "default"
            elif "EXPLICIT" in string:
                status = "explicit"
            elif "REAPPLIED" in string:
                status = "reapplied"
            elif "REDUNDANT" in string:
                status = "redundant"
            else:
                status = None
            assert status is not None
            color = self._status_to_color[status]
            tag = f"{status.upper()}_METRONOME_MARK_WITH_COLOR"
            tag = abjad.Tag(tag)
            if isinstance(left_text, str):
                string = left_text.replace(
                    "baca-metronome-mark-spanner-left-markup",
                    "baca-metronome-mark-spanner-colored-left-markup",
                )
                string = string.replace(
                    "baca-metronome-mark-spanner-left-text",
                    "baca-metronome-mark-spanner-colored-left-text",
                )
                string = string.replace(
                    "baca-bracketed-metric-modulation",
                    "baca-colored-bracketed-metric-modulation",
                )
                string = string.replace(
                    "baca-bracketed-mixed-number-metric-modulation",
                    "baca-colored-bracketed-mixed-number-metric-modulation",
                )
                left_text_with_color = f"{string} #'{color}"
            else:
                color = abjad.SchemeColor(color)
                left_text_with_color = left_text.with_color(color)
            if right_text:
                wrapper = abjad.inspect(skips[-1]).wrapper(abjad.MetronomeMark)
                tag = wrapper.tag
                string = str(tag)
                if "DEFAULT" in string:
                    status = "default"
                elif "EXPLICIT" in string:
                    status = "explicit"
                elif "REAPPLIED" in str(tag):
                    status = "reapplied"
                elif "REDUNDANT" in str(tag):
                    status = "redundant"
                else:
                    status = None
                assert status is not None
                color = self._status_to_color[status]
                color = abjad.SchemeColor(color)
                right_text_with_color = right_text.with_color(color)
            else:
                right_text_with_color = None
            start_text_span = abjad.StartTextSpan(
                command=r"\bacaStartTextSpanMM",
                left_text=left_text_with_color,
                right_text=right_text_with_color,
                style=style,
            )
            abjad.attach(
                start_text_span,
                skip,
                deactivate=False,
                tag=tag.append("_attach_metronome_marks(3)"),
            )
        if indicator_count:
            final_skip = skip
            stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanMM")
            abjad.attach(
                stop_text_span,
                final_skip,
                tag="SEGMENT_FINAL_STOP_MM_SPANNER:_attach_metronome_marks(4)",
            )

    def _born_this_segment(self, component):
        prototype = (abjad.Staff, abjad.StaffGroup)
        assert isinstance(component, prototype), repr(component)
        return not self._alive_during_previous_segment(component)

    @staticmethod
    def _bracket_metric_modulation(metronome_mark, metric_modulation):
        if metronome_mark.decimal is not True:
            # TODO: refactor _get_markup_arguments() to return dict
            arguments = metronome_mark._get_markup_arguments()
            mm_length, mm_dots, mm_stem, mm_value = arguments
            arguments = metric_modulation._get_markup_arguments()
            if metric_modulation._note_to_note():
                command = r"- \baca-bracketed-metric-modulation"
                lhs_length, lhs_dots, rhs_length, rhs_dots = arguments
                command += f' #{mm_length} #{mm_dots} #{mm_stem} #"{mm_value}"'
                command += f" #{lhs_length} #{lhs_dots}"
                command += f" #{rhs_length} #{rhs_dots}"
            elif metric_modulation._lhs_tuplet():
                command = r"- \baca-bracketed-metric-modulation-tuplet-lhs"
                tuplet_length, tuplet_dots, tuplet_n, tuplet_d = arguments[:4]
                note_length, note_dots = arguments[4:]
                command += f' #{mm_length} #{mm_dots} #{mm_stem} #"{mm_value}"'
                command += f" #{tuplet_length} #{tuplet_dots}"
                command += f" #{tuplet_n} #{tuplet_d}"
                command += f" #{note_length} #{note_dots}"
            elif metric_modulation._rhs_tuplet():
                command = r"- \baca-bracketed-metric-modulation-tuplet-rhs"
                note_length, note_dots = arguments[:2]
                tuplet_length, tuplet_dots, tuplet_n, tuplet_d = arguments[2:]
                command += f' #{mm_length} #{mm_dots} #{mm_stem} #"{mm_value}"'
                command += f" #{note_length} #{note_dots}"
                command += f" #{tuplet_length} #{tuplet_dots}"
                command += f" #{tuplet_n} #{tuplet_d}"
            else:
                raise Exception(
                    "implement tied note values in metric modulation."
                )
        else:
            arguments = metronome_mark._get_markup_arguments()
            mm_length, mm_dots, mm_stem, mm_base, mm_n, mm_d = arguments
            # TODO: refactor _get_markup_arguments() to return dict
            arguments = metric_modulation._get_markup_arguments()
            if metric_modulation._note_to_note():
                command = r"- \baca-bracketed-mixed-number-metric-modulation"
                lhs_length, lhs_dots, rhs_length, rhs_dots = arguments
                command += f" #{mm_length} #{mm_dots} #{mm_stem}"
                command += f' #"{mm_base}" #"{mm_n}" #"{mm_d}"'
                command += f" #{lhs_length} #{lhs_dots}"
                command += f" #{rhs_length} #{rhs_dots}"
            elif metric_modulation._lhs_tuplet():
                command = r"- \baca-bracketed-mixed-number-metric-modulation-tuplet-lhs"
                tuplet_length, tuplet_dots, tuplet_n, tuplet_d = arguments[:4]
                note_length, note_dots = arguments[4:]
                command += f" #{mm_length} #{mm_dots} #{mm_stem}"
                command += f' #"{mm_base}" #"{mm_n}" #"{mm_d}"'
                command += f" #{tuplet_length} #{tuplet_dots}"
                command += f" #{tuplet_n} #{tuplet_d}"
                command += f" #{note_length} #{note_dots}"
            elif metric_modulation._rhs_tuplet():
                command = r"- \baca-bracketed-mixed-number-metric-modulation-tuplet-rhs"
                note_length, note_dots = arguments[:2]
                tuplet_length, tuplet_dots, tuplet_n, tuplet_d = arguments[2:]
                command += f" #{mm_length} #{mm_dots} #{mm_stem}"
                command += f' #"{mm_base}" #"{mm_n}" #"{mm_d}"'
                command += f" #{note_length} #{note_dots}"
                command += f" #{tuplet_length} #{tuplet_dots}"
                command += f" #{tuplet_n} #{tuplet_d}"
            else:
                raise Exception(
                    "implement tied note values in metric modulation."
                )

        scale = metric_modulation.scale
        command += f" #'({scale[0]} . {scale[1]})"
        return command

    def _bundle_manifests(self, voice_name=None):
        manifests = abjad.OrderedDict()
        previous_segment_voice_metadata = self._get_previous_segment_voice_metadata(
            voice_name
        )
        manifests["manifests"] = self.manifests
        manifests["offset_to_measure_number"] = self._offset_to_measure_number
        manifests[
            "previous_segment_voice_metadata"
        ] = previous_segment_voice_metadata
        manifests["score_template"] = self.score_template
        return manifests

    def _cache_fermata_measure_numbers(self):
        if "Global_Rests" not in self.score:
            return
        context = self.score["Global_Rests"]
        rests = abjad.select(context).leaves(abjad.MultimeasureRest)
        final_measure_index = len(rests) - 1
        final_measure_index -= 1
        first_measure_number = self._get_first_measure_number()
        tag = abjad.tags.FERMATA_MEASURE
        for measure_index, rest in enumerate(rests):
            if not abjad.inspect(rest).has_indicator(tag):
                continue
            if measure_index == final_measure_index:
                self._final_measure_is_fermata = True
            measure_number = first_measure_number + measure_index
            timespan = abjad.inspect(rest).timespan()
            self._fermata_start_offsets.append(timespan.start_offset)
            self._fermata_stop_offsets.append(timespan.stop_offset)
            self._fermata_measure_numbers.append(measure_number)

    def _cache_leaves(self):
        measure_timespans = []
        for measure_index in range(self.measure_count):
            measure_number = measure_index + 1
            measure_timespan = self._get_measure_timespan(measure_number)
            measure_timespans.append(measure_timespan)
        self._cache = abjad.OrderedDict()
        for leaf in abjad.select(self.score).leaves():
            parentage = abjad.inspect(leaf).parentage(grace=True)
            context = parentage.get(abjad.Context)
            leaves_by_measure_number = self._cache.setdefault(
                context.name, abjad.OrderedDict()
            )
            leaf_timespan = abjad.inspect(leaf).timespan()
            # TODO: replace loop with bisection:
            for i, measure_timespan in enumerate(measure_timespans):
                measure_number = i + 1
                if leaf_timespan.starts_during_timespan(measure_timespan):
                    cached_leaves = leaves_by_measure_number.setdefault(
                        measure_number, []
                    )
                    cached_leaves.append(leaf)

    def _cache_previously_alive_contexts(self) -> None:
        if self.segment_directory is None:
            return
        contexts: typing.Set[str] = set()
        string = "alive_during_segment"
        for segment in self.segment_directory.parent.list_paths():
            if segment == self.segment_directory:
                break
            contexts_ = segment.get_metadatum(
                string, file_name="__persist__.py"
            )
            contexts.update(contexts_)
        self._previously_alive_contexts.extend(sorted(contexts))

    def _cache_voice_names(self):
        if self._voice_names is not None:
            return
        if self.score_template is None:
            return
        voice_names = ["Global_Skips", "Global_Rests", "Timeline_Scope"]
        score = self.score_template()
        for voice in abjad.iterate(score).components(abjad.Voice):
            if voice.name is not None:
                voice_names.append(voice.name)
                if "Music_Voice" in voice.name:
                    name = voice.name.replace("Music_Voice", "Rest_Voice")
                else:
                    name = voice.name.replace("Voice", "Rest_Voice")
                voice_names.append(name)
        voice_names_ = tuple(voice_names)
        self._voice_names = voice_names_

    def _calculate_clock_times(self):
        skips = classes.Selection(self.score["Global_Skips"]).skips()
        if "Global_Rests" not in self.score:
            return
        rests = classes.Selection(self.score["Global_Rests"]).rests()
        assert len(skips) == len(rests)
        start_clock_time = self._get_previous_stop_clock_time()
        start_clock_time = start_clock_time or "0'00''"
        self._start_clock_time = start_clock_time
        start_offset = abjad.Duration.from_clock_string(start_clock_time)
        if self.clock_time_override:
            metronome_mark = self.clock_time_override
            abjad.attach(metronome_mark, skips[0])
        if abjad.inspect(skips[0]).effective(abjad.MetronomeMark) is None:
            return
        first_measure_number = self._get_first_measure_number()
        clock_times = []
        for local_measure_index, skip in enumerate(skips):
            measure_number = first_measure_number + local_measure_index
            if measure_number not in self._fermata_measure_numbers:
                clock_times.append(start_offset)
                duration = abjad.inspect(skip).duration(in_seconds=True)
            else:
                rest = rests[local_measure_index]
                fermata_duration = abjad.inspect(rest).annotation(
                    const.FERMATA_DURATION
                )
                duration = abjad.Duration(fermata_duration)
                clock_times.append(duration)
            start_offset += duration
        clock_times.append(start_offset)
        assert len(skips) == len(clock_times) - 1
        if self.clock_time_override:
            metronome_mark = self.clock_time_override
            abjad.detach(metronome_mark, skips[0])
        stop_clock_time = clock_times[-1].to_clock_string()
        self._stop_clock_time = stop_clock_time
        duration = clock_times[-1] - clock_times[0]
        duration_clock_string = duration.to_clock_string()
        self._duration = duration_clock_string
        return clock_times

    def _call_commands(self):
        command_count = 0
        for command in self.commands:
            assert isinstance(command, scoping.Command)
            if isinstance(command, rhythmcommands.RhythmCommand):
                continue
            command_count += 1
            selection = self._scope_to_leaf_selection(command)
            voice_name = command.scope.voice_name
            runtime = self._bundle_manifests(voice_name)
            try:
                command(selection, runtime)
            except:
                print(f"Interpreting ...\n\n{format(command)}\n")
                raise
            self._handle_mutator(command)
            if getattr(command, "persist", None):
                parameter = command.parameter
                state = command.state
                assert "name" not in state
                state["name"] = command.persist
                if voice_name not in self.voice_metadata:
                    self.voice_metadata[voice_name] = abjad.OrderedDict()
                self.voice_metadata[voice_name][parameter] = state
        return command_count

    def _call_rhythm_commands(self):
        self._attach_fermatas()
        command_count = 0
        tag = "_call_rhythm_commands"
        silence_maker = rhythmcommands.SkipRhythmMaker(
            tag=tag, use_multimeasure_rests=not (self.skips_instead_of_rests)
        )
        for voice in abjad.select(self.score).components(abjad.Voice):
            assert not len(voice), repr(voice)
            voice_metadata = self._voice_metadata.get(
                voice.name, abjad.OrderedDict()
            )
            commands = self._voice_to_rhythm_commands(voice)
            if not commands:
                selection = silence_maker(self.time_signatures)
                assert isinstance(selection, abjad.Selection), repr(selection)
                voice.extend(selection)
                if not self.remove_phantom_measure:
                    container = self._make_multimeasure_rest_container(
                        voice.name, (1, 4), phantom=True, suppress_note=True
                    )
                    voice.append(container)
                continue
            timespans = []
            for command in commands:
                if command.scope.measures is None:
                    raise Exception(format(command))
                measures = command.scope.measures
                result = self._get_measure_time_signatures(*measures)
                start_offset, time_signatures = result
                runtime = self._bundle_manifests(voice.name)
                try:
                    selection = command._make_selection(
                        time_signatures, runtime
                    )
                except:
                    print(f"Interpreting ...\n\n{format(command)}\n")
                    raise
                timespan = abjad.AnnotatedTimespan(
                    start_offset=start_offset, annotation=selection
                )
                timespans.append(timespan)
                if command.persist and command.state:
                    state = command.state
                    assert "name" not in state
                    state["name"] = command.persist
                    voice_metadata[command.parameter] = command.state
                command_count += 1
            if bool(voice_metadata):
                self._voice_metadata[voice.name] = voice_metadata
            timespans.sort()
            self._assert_nonoverlapping_rhythms(timespans, voice.name)
            selections = self._intercalate_silences(timespans, voice.name)
            if not self.remove_phantom_measure:
                suppress_note = False
                final_leaf = abjad.inspect(selections).leaf(-1)
                if isinstance(final_leaf, abjad.MultimeasureRest):
                    suppress_note = True
                container = self._make_multimeasure_rest_container(
                    voice.name,
                    (1, 4),
                    phantom=True,
                    suppress_note=suppress_note,
                )
                selection = abjad.select(container)
                selections.append(selection)
            voice.extend(selections)
        return command_count

    def _check_all_music_in_part_containers(self):
        name = "all_music_in_part_containers"
        if getattr(self.score_template, name, None) is not True:
            return
        annotation = const.MULTIMEASURE_REST_CONTAINER
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            for component in voice:
                if isinstance(component, (abjad.MultimeasureRest, abjad.Skip)):
                    continue
                if (
                    abjad.inspect(component).annotation(abjad.const.HIDDEN)
                    is True
                ):
                    continue
                if abjad.inspect(component).annotation(annotation) is True:
                    continue
                if (
                    type(component) is abjad.Container
                    and component.identifier
                    and component.identifier.startswith("%*% ")
                ):
                    continue
                message = f"{voice.name} contains {component!r}"
                message += " outside part container."
                raise Exception(message)

    def _check_doubled_dynamics(self):
        for leaf in abjad.iterate(self.score).leaves():
            dynamics = abjad.inspect(leaf).indicators(abjad.Dynamic)
            if 1 < len(dynamics):
                voice = abjad.inspect(leaf).parentage().get(abjad.Voice)
                message = f"leaf {str(leaf)} in {voice.name} has"
                message += f" {len(dynamics)} dynamics attached:"
                for dynamic in dynamics:
                    message += f"\n   {dynamic!s}"
                raise Exception(message)

    def _check_persistent_indicators(self):
        if self.do_not_check_persistence:
            return
        if self.environment == "docs":
            return
        tag = const.SOUNDS_DURING_SEGMENT
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            if not abjad.inspect(voice).annotation(tag):
                continue
            for i, leaf in enumerate(abjad.iterate(voice).leaves()):
                self._check_persistent_indicators_for_leaf(voice.name, leaf, i)

    def _check_persistent_indicators_for_leaf(self, voice, leaf, i):
        prototype = (
            indicators.Accelerando,
            abjad.MetronomeMark,
            indicators.Ritardando,
        )
        mark = abjad.inspect(leaf).effective(prototype)
        if mark is None:
            message = f"{voice} leaf {i} ({leaf!s}) missing metronome mark."
            raise Exception(message)
        instrument = abjad.inspect(leaf).effective(abjad.Instrument)
        if instrument is None:
            message = f"{voice} leaf {i} ({leaf!s}) missing instrument."
            raise Exception(message)
        if not self.score_template.do_not_require_margin_markup:
            markup = abjad.inspect(leaf).effective(abjad.MarginMarkup)
            if markup is None:
                message = f"{voice} leaf {i} ({leaf!s}) missing margin markup."
                raise Exception(message)
        clef = abjad.inspect(leaf).effective(abjad.Clef)
        if clef is None:
            raise Exception(f"{voice} leaf {i} ({leaf!s}) missing clef.")

    def _check_range(self):
        tag = abjad.tags.ALLOW_OUT_OF_RANGE
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            for pleaf in abjad.iterate(voice).leaves(pitched=True):
                if abjad.inspect(pleaf).annotation(abjad.const.HIDDEN):
                    continue
                instrument = abjad.inspect(pleaf).effective(abjad.Instrument)
                if instrument is None:
                    continue
                if pleaf not in instrument.pitch_range:
                    if abjad.inspect(pleaf).has_indicator(tag):
                        continue
                    if not self.do_not_color_out_of_range_pitches:
                        string = r"\baca-out-of-range-warning"
                        literal = abjad.LilyPondLiteral(string)
                        abjad.attach(literal, pleaf, tag="_check_range")

    def _check_wellformedness(self):
        if self.do_not_check_wellformedness:
            return
        if not abjad.inspect(self.score).wellformed(
            allow_percussion_clef=True,
            check_out_of_range_pitches=not (
                self.do_not_check_out_of_range_pitches
            ),
        ):
            message = abjad.inspect(self.score).tabulate_wellformedness(
                allow_percussion_clef=True,
                check_out_of_range_pitches=not (
                    self.do_not_check_out_of_range_pitches
                ),
            )
            raise Exception("\n" + message)

    def _clone_segment_initial_short_instrument_name(self):
        if self.first_segment:
            return
        prototype = abjad.MarginMarkup
        for context in abjad.iterate(self.score).components(abjad.Context):
            first_leaf = abjad.inspect(context).leaf(0)
            if abjad.inspect(first_leaf).has_indicator(abjad.StartMarkup):
                continue
            margin_markup = abjad.inspect(first_leaf).indicator(prototype)
            if margin_markup is None:
                continue
            if isinstance(margin_markup.markup, str):
                markup = margin_markup.markup
            else:
                markup = abjad.new(margin_markup.markup)
            start_markup = abjad.StartMarkup(
                context=margin_markup.context,
                format_slot=margin_markup.format_slot,
                markup=markup,
            )
            abjad.attach(
                start_markup,
                first_leaf,
                tag="_clone_segment_initial_short_instrument_name",
            )

    def _collect_alive_during_segment(self):
        result = []
        for context in abjad.iterate(self.score).components(abjad.Context):
            if context.name not in result:
                result.append(context.name)
        return result

    def _collect_metadata(self):
        metadata, persist = abjad.OrderedDict(), abjad.OrderedDict()
        persist["alive_during_segment"] = self._collect_alive_during_segment()
        # __make_layout_ly__ adds bol measure numbers to metadata
        bol_measure_numbers = self.metadata.get("bol_measure_numbers")
        if bol_measure_numbers:
            metadata["bol_measure_numbers"] = bol_measure_numbers
        if self._container_to_part_assignment:
            value = self._container_to_part_assignment
            persist["container_to_part_assignment"] = value
        if self._duration is not None:
            metadata["duration"] = self._duration
        if self._fermata_measure_numbers:
            metadata["fermata_measure_numbers"] = self._fermata_measure_numbers
        dictionary = self.metadata.get("first_appearance_margin_markup")
        if dictionary:
            metadata["first_appearance_margin_markup"] = dictionary
        metadata["first_measure_number"] = self._get_first_measure_number()
        metadata["final_measure_number"] = self._get_final_measure_number()
        if self._final_measure_is_fermata is True:
            metadata["final_measure_is_fermata"] = True
        dictionary = self._collect_persistent_indicators()
        if dictionary:
            persist["persistent_indicators"] = dictionary
        if self.segment_name is not None:
            metadata["segment_name"] = self.segment_name
        metadata["segment_number"] = self._get_segment_number()
        if self._start_clock_time is not None:
            metadata["start_clock_time"] = self._start_clock_time
        if self._stop_clock_time is not None:
            metadata["stop_clock_time"] = self._stop_clock_time
        metadata["time_signatures"] = self._cached_time_signatures
        if self.voice_metadata:
            persist["voice_metadata"] = self.voice_metadata
        self.metadata.clear()
        self.metadata.update(metadata)
        self.metadata.sort(recurse=True)
        for key, value in self.metadata.items():
            if not bool(value):
                message = f"{key} metadata should be nonempty"
                message += f" (not {value!r})."
                raise Exception(message)
        self.persist.clear()
        self.persist.update(persist)
        self.persist.sort(recurse=True)
        for key, value in self.persist.items():
            if not bool(value):
                message = f"{key} persist should be nonempty"
                message += f" (not {value!r})."
                raise Exception(message)

    def _collect_persistent_indicators(self):
        result = abjad.OrderedDict()
        contexts = abjad.iterate(self.score).components(abjad.Context)
        contexts = list(contexts)
        contexts.sort(key=lambda _: _.name)
        do_not_persist_on_phantom_measure = (
            abjad.Instrument,
            abjad.MetronomeMark,
            abjad.MarginMarkup,
            abjad.TimeSignature,
        )
        for context in contexts:
            momentos = []
            wrappers = []
            dictionary = context._get_persistent_wrappers(
                omit_annotation=const.PHANTOM
            )
            for wrapper in dictionary.values():
                if isinstance(
                    wrapper.indicator, do_not_persist_on_phantom_measure
                ):
                    wrappers.append(wrapper)
            dictionary = context._get_persistent_wrappers()
            for wrapper in dictionary.values():
                if not isinstance(
                    wrapper.indicator, do_not_persist_on_phantom_measure
                ):
                    wrappers.append(wrapper)
            for wrapper in wrappers:
                leaf = wrapper.component
                parentage = abjad.inspect(leaf).parentage()
                first_context = parentage.get(abjad.Context)
                indicator = wrapper.indicator
                if isinstance(indicator, abjad.GlissandoIndicator):
                    continue
                if isinstance(indicator, abjad.RepeatTie):
                    continue
                if isinstance(indicator, abjad.StopBeam):
                    continue
                if isinstance(indicator, abjad.StopPianoPedal):
                    continue
                if isinstance(indicator, abjad.StopSlur):
                    continue
                if isinstance(indicator, abjad.StopTextSpan):
                    continue
                if isinstance(indicator, abjad.StopTrillSpan):
                    continue
                if isinstance(indicator, abjad.Tie):
                    continue
                prototype, manifest = None, None
                if isinstance(indicator, abjad.Instrument):
                    manifest = "instruments"
                elif isinstance(indicator, abjad.MetronomeMark):
                    manifest = "metronome_marks"
                elif isinstance(indicator, abjad.MarginMarkup):
                    manifest = "margin_markups"
                else:
                    prototype = type(indicator)
                    prototype = self._prototype_string(prototype)
                value = self._indicator_to_key(indicator, self.manifests)
                if value is None and self.environment != "docs":
                    raise Exception(
                        "can not find persistent indicator in manifest:\n\n"
                        f"  {indicator}"
                    )
                editions = wrapper.tag.editions()
                if editions:
                    words = [str(_) for _ in editions]
                    editions = abjad.Tag.from_words(words)
                else:
                    editions = None
                momento = abjad.Momento(
                    context=first_context.name,
                    edition=editions,
                    manifest=manifest,
                    prototype=prototype,
                    value=value,
                )
                momentos.append(momento)
            if momentos:
                momentos.sort(key=lambda _: format(_))
                result[context.name] = momentos
        dictionary = self.previous_persist.get("persistent_indicators")
        if dictionary:
            for context_name, momentos in dictionary.items():
                if context_name not in result:
                    result[context_name] = momentos
        return result

    def _color_octaves_(self):
        if not self.color_octaves:
            return
        score = self.score
        vertical_moments = abjad.iterate(score).vertical_moments()
        markup = abjad.Markup("OCTAVE", direction=abjad.Up)
        abjad.tweak(markup).color = "red"
        for vertical_moment in vertical_moments:
            pleaves, pitches = [], []
            for leaf in vertical_moment.leaves:
                if abjad.inspect(leaf).annotation(abjad.const.HIDDEN) is True:
                    continue
                if abjad.inspect(leaf).has_indicator(
                    abjad.tags.STAFF_POSITION
                ):
                    continue
                if isinstance(leaf, abjad.Note):
                    pleaves.append(leaf)
                    pitches.append(leaf.written_pitch)
                elif isinstance(leaf, abjad.Chord):
                    pleaves.append(leaf)
                    pitches.extend(leaf.written_pitches)
            if not pitches:
                continue
            pitch_classes = [_.pitch_class for _ in pitches]
            if pitchclasses.PitchClassSegment(pitch_classes).has_duplicates():
                color = True
                for pleaf in pleaves:
                    inspection = abjad.inspect(pleaf)
                    if inspection.has_indicator(abjad.tags.ALLOW_OCTAVE):
                        color = False
                if not color:
                    continue
                for pleaf in pleaves:
                    abjad.attach(markup, pleaf, tag="_color_octaves_")
                    string = r"\baca-octave-warning"
                    literal = abjad.LilyPondLiteral(string)
                    abjad.attach(literal, pleaf, tag="_color_octaves_")

    def _color_repeat_pitch_classes_(self):
        if self.do_not_color_repeat_pitch_classes:
            return
        lts = self._find_repeat_pitch_classes(self.score)
        tag = "_color_repeat_pitch_classes_"
        for lt in lts:
            for leaf in lt:
                string = r"\baca-repeat-pitch-class-warning"
                literal = abjad.LilyPondLiteral(string)
                abjad.attach(literal, leaf, tag=tag)

    def _color_unpitched_notes(self):
        if self.do_not_color_unpitched_music:
            return
        tag = abjad.tags.NOT_YET_PITCHED
        for pleaf in abjad.iterate(self.score).leaves(pitched=True):
            if not abjad.inspect(pleaf).has_indicator(tag):
                continue
            string = r"\baca-unpitched-music-warning"
            literal = abjad.LilyPondLiteral(string)
            abjad.attach(literal, pleaf, tag="_color_unpitched_notes")

    def _color_unregistered_pitches(self):
        if self.do_not_color_unregistered_pitches:
            return
        tag = abjad.tags.NOT_YET_REGISTERED
        for pleaf in abjad.iterate(self.score).leaves(pitched=True):
            if not abjad.inspect(pleaf).has_indicator(tag):
                continue
            string = r"\baca-unregistered-pitch-warning"
            literal = abjad.LilyPondLiteral(string)
            abjad.attach(literal, pleaf, tag="_color_unregistered_pitches")

    def _comment_measure_numbers(self):
        first_measure_number = self._get_first_measure_number()
        for leaf in abjad.iterate(self.score).leaves():
            offset = abjad.inspect(leaf).timespan().start_offset
            measure_number = self._offset_to_measure_number.get(offset, None)
            if measure_number is None:
                continue
            local_measure_number = measure_number - first_measure_number
            local_measure_number += 1
            if self.segment_name:
                name = self.segment_name + " "
            else:
                name = ""
            context = abjad.inspect(leaf).parentage().get(abjad.Context)
            if self.first_segment or self.environment == "docs":
                string = f"% [{name}{context.name}"
                string += f" measure {measure_number}]"
            else:
                string = f"% [{name}{context.name}"
                string += f" measure {measure_number} /"
                string += f" measure {local_measure_number}]"
            literal = abjad.LilyPondLiteral(string, "absolute_before")
            abjad.attach(literal, leaf, tag="_comment_measure_numbers")

    def _deactivate_tags(self, tags):
        tags = tags or []
        tags = set(tags)
        tags.update(self.deactivate or [])
        if not tags:
            return
        for leaf in abjad.iterate(self.score).leaves():
            if not isinstance(leaf, abjad.Skip):
                continue
            wrappers = abjad.inspect(leaf).wrappers()
            for wrapper in wrappers:
                if wrapper.tag is None:
                    continue
                for tag in tags:
                    if tag in wrapper.tag:
                        wrapper.deactivate = True
                        break

    @staticmethod
    def _extend_beam(leaf):
        if not abjad.inspect(leaf).has_indicator(abjad.StopBeam):
            parentage = abjad.inspect(leaf).parentage(grace=True)
            voice = parentage.get(abjad.Voice)
            message = f"{leaf!s} in {voice.name} has no StopBeam."
            raise Exception(message)
        abjad.detach(abjad.StopBeam, leaf)
        if not abjad.inspect(leaf).has_indicator(abjad.StartBeam):
            abjad.detach(abjad.BeamCount, leaf)
            left = leaf.written_duration.flag_count
            beam_count = abjad.BeamCount(left, 1)
            abjad.attach(beam_count, leaf, "_extend_beam")
        current_leaf = leaf
        while True:
            next_leaf = abjad.inspect(current_leaf).leaf(1)
            if next_leaf is None:
                parentage = abjad.inspect(current_leaf).parentage(grace=True)
                voice = parentage.get(abjad.Voice)
                message = f"no leaf follows {current_leaf!s} in {voice.name};"
                message += "\n\tDo not set extend_beam=True on last figure."
                raise Exception(message)
                return
            if abjad.inspect(next_leaf).has_indicator(abjad.StartBeam):
                abjad.detach(abjad.StartBeam, next_leaf)
                if not abjad.inspect(next_leaf).has_indicator(abjad.StopBeam):
                    abjad.detach(abjad.BeamCount, next_leaf)
                    right = next_leaf.written_duration.flag_count
                    beam_count = abjad.BeamCount(1, right)
                    abjad.attach(beam_count, next_leaf, "_extend_beam")
                return
            current_leaf = next_leaf

    def _extend_beams(self):
        for leaf in abjad.iterate(self.score).leaves():
            if abjad.inspect(leaf).indicator(abjad.tags.RIGHT_BROKEN_BEAM):
                self._extend_beam(leaf)

    @staticmethod
    def _find_repeat_pitch_classes(argument):
        violators = []
        for voice in abjad.iterate(argument).components(abjad.Voice):
            if abjad.inspect(voice).annotation(const.INTERMITTENT) is True:
                continue
            previous_lt, previous_pcs = None, []
            for lt in abjad.iterate(voice).logical_ties():
                inspection = abjad.inspect(lt.head)
                if inspection.annotation(abjad.const.HIDDEN) is True:
                    written_pitches = []
                elif isinstance(lt.head, abjad.Note):
                    written_pitches = [lt.head.written_pitch]
                elif isinstance(lt.head, abjad.Chord):
                    written_pitches = lt.head.written_pitches
                else:
                    written_pitches = []
                pcs = pitchclasses.PitchClassSet(written_pitches)
                inspection = abjad.inspect(lt.head)
                if inspection.has_indicator(
                    abjad.tags.NOT_YET_PITCHED
                ) or inspection.has_indicator(abjad.tags.ALLOW_REPEAT_PITCH):
                    pass
                elif pcs & previous_pcs:
                    if previous_lt not in violators:
                        violators.append(previous_lt)
                    if lt not in violators:
                        violators.append(lt)
                previous_lt = lt
                previous_pcs = pcs
        return violators

    def _force_nonnatural_accidentals(self):
        if self.do_not_force_nonnatural_accidentals:
            return
        natural = abjad.Accidental("natural")
        for pleaf in classes.Selection(self.score).pleaves():
            if isinstance(pleaf, abjad.Note):
                note_heads = [pleaf.note_head]
            else:
                note_heads = pleaf.note_heads
            for note_head in note_heads:
                if note_head.written_pitch.accidental != natural:
                    note_head.is_forced = True

    def _get_final_measure_number(self):
        return self._get_first_measure_number() + self.measure_count - 1

    def _get_first_measure_number(self):
        if self.first_measure_number is not None:
            return self.first_measure_number
        if not self.previous_metadata:
            return 1
        string = "first_measure_number"
        first_measure_number = self.previous_metadata.get(string)
        time_signatures = self.previous_metadata.get("time_signatures")
        if first_measure_number is None or time_signatures is None:
            return 1
        first_measure_number += len(time_signatures)
        return first_measure_number

    @staticmethod
    def _get_key(dictionary, value):
        if dictionary is not None:
            for key, value_ in dictionary.items():
                if value_ == value:
                    return key

    def _get_lilypond_includes(self):
        if self.environment == "docs":
            if abjad.inspect(self.score).indicator(abjad.tags.TWO_VOICE):
                return ["two-voice-staff.ily"]
            elif abjad.inspect(self.score).indicator(abjad.tags.THREE_VOICE):
                return ["three-voice-staff.ily"]
            else:
                return ["string-trio.ily"]
        elif self.environment == "external":
            if abjad.inspect(self.score).indicator(abjad.tags.TWO_VOICE):
                return [self._absolute_two_voice_staff_stylesheet_path]
            else:
                return [self._absolute_string_trio_stylesheet_path]
        includes = []
        includes.append(self._score_package_stylesheet_path)
        if self.clock_time_extra_offset is not None:
            value = self.clock_time_extra_offset
            if isinstance(value, tuple):
                string = f"#'({value[0]} . {value[1]})"
            else:
                string = abjad.Scheme.format_embedded_scheme_value(value)
            string = f"clock-time-extra-offset = {string}"
            literal = abjad.LilyPondLiteral(string)
            includes.append(literal)
        if self.local_measure_number_extra_offset is not None:
            value = self.local_measure_number_extra_offset
            if isinstance(value, tuple):
                string = f"#'({value[0]} . {value[1]})"
            else:
                string = abjad.Scheme.format_embedded_scheme_value(value)
            string = f"local-measure-number-extra-offset = {string}"
            literal = abjad.LilyPondLiteral(string)
            includes.append(literal)
        if self.measure_number_extra_offset is not None:
            value = self.measure_number_extra_offset
            if isinstance(value, tuple):
                string = f"#'({value[0]} . {value[1]})"
            else:
                string = abjad.Scheme.format_embedded_scheme_value(value)
            string = f"measure-number-extra-offset = {string}"
            literal = abjad.LilyPondLiteral(string)
            includes.append(literal)
        if self.spacing_extra_offset is not None:
            value = self.spacing_extra_offset
            if isinstance(value, tuple):
                string = f"#'({value[0]} . {value[1]})"
            else:
                string = abjad.Scheme.format_embedded_scheme_value(value)
            string = f"spacing-extra-offset = {string}"
            literal = abjad.LilyPondLiteral(string)
            includes.append(literal)
        if self.stage_number_extra_offset is not None:
            value = self.stage_number_extra_offset
            if isinstance(value, tuple):
                string = f"#'({value[0]} . {value[1]})"
            else:
                string = abjad.Scheme.format_embedded_scheme_value(value)
            string = f"stage-number-extra-offset = {string}"
            literal = abjad.LilyPondLiteral(string)
            includes.append(literal)
        if not self.first_segment or self.nonfirst_segment_lilypond_include:
            includes.append(self._score_package_nonfirst_segment_path)
        includes.extend(self.includes or [])
        return includes

    def _get_measure_number_tag(self, leaf):
        start_offset = abjad.inspect(leaf).timespan().start_offset
        measure_number = self._offset_to_measure_number.get(start_offset)
        if measure_number is not None:
            return f"MEASURE_{measure_number}"

    def _get_measure_offsets(self, start_measure, stop_measure):
        skips = classes.Selection(self.score["Global_Skips"]).skips()
        start_skip = skips[start_measure - 1]
        assert isinstance(start_skip, abjad.Skip), start_skip
        start_offset = abjad.inspect(start_skip).timespan().start_offset
        stop_skip = skips[stop_measure - 1]
        assert isinstance(stop_skip, abjad.Skip), stop_skip
        stop_offset = abjad.inspect(stop_skip).timespan().stop_offset
        return start_offset, stop_offset

    def _get_measure_time_signatures(
        self, start_measure=None, stop_measure=None
    ):
        assert stop_measure is not None
        start_index = start_measure - 1
        if stop_measure is None:
            time_signatures = [self.time_signatures[start_index]]
        else:
            if stop_measure == -1:
                stop_measure = self.measure_count
            stop_index = stop_measure
            time_signatures = self.time_signatures[start_index:stop_index]
        measure_timespan = self._get_measure_timespan(start_measure)
        return measure_timespan.start_offset, time_signatures

    def _get_measure_timespan(self, measure_number):
        start_offset, stop_offset = self._get_measure_offsets(
            measure_number, measure_number
        )
        return abjad.Timespan(start_offset, stop_offset)

    def _get_measure_timespans(self, measure_numbers):
        timespans = []
        first_measure_number = self._get_first_measure_number()
        measure_indices = [
            _ - first_measure_number - 1 for _ in measure_numbers
        ]
        skips = classes.Selection(self.score["Global_Skips"]).skips()
        for i, skip in enumerate(skips):
            if i in measure_indices:
                timespan = abjad.inspect(skip).timespan()
                timespans.append(timespan)
        return timespans

    def _get_persistent_indicator(self, context, prototype):
        assert isinstance(context, abjad.Context), repr(context)
        if not self.previous_metadata:
            return
        dictionary = self.previous_persist.get("persistent_indicators")
        if not dictionary:
            return
        momentos = dictionary.get(context.name)
        if not momentos:
            return
        prototype_string = self._prototype_string(prototype)
        for momento in momentos:
            if momento.prototype == prototype_string:
                indicator = self._key_to_indicator(momento.value, prototype)
                return (indicator, momento.context)

    def _get_previous_segment_voice_metadata(self, voice_name):
        if not self.previous_persist:
            return
        voice_metadata = self.previous_persist.get("voice_metadata")
        if not voice_metadata:
            return
        return voice_metadata.get(voice_name, abjad.OrderedDict())

    def _get_previous_state(self, voice_name, command_persist):
        if not self.previous_persist:
            return
        if not command_persist:
            return
        dictionary = self.previous_persist.get("voice_metadata")
        if not bool(dictionary):
            return
        dictionary = dictionary.get(voice_name)
        if not bool(dictionary):
            return
        previous_state = dictionary.get(command_persist)
        return previous_state

    def _get_previous_stop_clock_time(self):
        if self.previous_metadata:
            return self.previous_metadata.get("stop_clock_time")

    def _get_segment_measure_numbers(self):
        first_measure_number = self._get_first_measure_number()
        final_measure_number = self._get_final_measure_number()
        return list(range(first_measure_number, final_measure_number + 1))

    def _get_segment_number(self):
        if not self.previous_metadata:
            segment_number = 0
        else:
            segment_number = self.previous_metadata.get("segment_number")
            if segment_number is None:
                message = "previous metadata missing segment number."
                raise Exception(message)
        return segment_number + 1

    @staticmethod
    def _get_tag(status, stem, prefix=None, suffix=None):
        stem = abjad.String(stem).delimit_words()
        stem = "_".join([_.upper() for _ in stem])
        if suffix is not None:
            name = f"{status.upper()}_{stem}_{suffix.upper()}"
        else:
            name = f"{status.upper()}_{stem}"
        if prefix is not None:
            name = f"{prefix.upper()}_{name}"
        tag = getattr(abjad.tags, name)
        return abjad.Tag(tag)

    def _handle_mutator(self, command):
        if hasattr(command, "_mutates_score") and command._mutates_score():
            self._cache = None
            self._update_score_one_time()

    def _import_manifests(self):
        if not self.segment_directory:
            return
        score_package = self.segment_directory._import_score_package()
        if not self.instruments:
            instruments = getattr(score_package, "instruments", None)
            self._instruments = instruments
        if not self.margin_markups:
            margin_markups = getattr(score_package, "margin_markups", None)
            self._margin_markups = margin_markups
        if not self.metronome_marks:
            metronome_marks = getattr(score_package, "metronome_marks", None)
            self._metronome_marks = metronome_marks
        if not self.score_template:
            score_template = getattr(score_package, "ScoreTemplate", None)
            if score_template is not None:
                score_template = score_template()
            self._score_template = score_template

    @staticmethod
    def _indicator_to_grob(indicator):
        if isinstance(indicator, abjad.Dynamic):
            return "DynamicText"
        elif isinstance(indicator, abjad.Instrument):
            return "InstrumentName"
        elif isinstance(indicator, abjad.MetronomeMark):
            return "TextScript"
        elif isinstance(indicator, abjad.MarginMarkup):
            return "InstrumentName"
        elif isinstance(indicator, indicators.StaffLines):
            return "StaffSymbol"
        return type(indicator).__name__

    @staticmethod
    def _indicator_to_key(indicator, manifests):
        if isinstance(indicator, abjad.Clef):
            key = indicator.name
        elif isinstance(indicator, abjad.Dynamic):
            if indicator.name == "niente":
                key = "niente"
            else:
                key = indicator.command or indicator.name
        elif isinstance(indicator, abjad.StartHairpin):
            key = indicator.shape
        elif isinstance(indicator, abjad.Instrument):
            key = SegmentMaker._get_key(
                manifests["abjad.Instrument"], indicator
            )
        elif isinstance(indicator, abjad.MetronomeMark):
            key = SegmentMaker._get_key(
                manifests["abjad.MetronomeMark"], indicator
            )
        elif isinstance(indicator, abjad.MarginMarkup):
            key = SegmentMaker._get_key(
                manifests["abjad.MarginMarkup"], indicator
            )
        elif isinstance(indicator, abjad.PersistentOverride):
            key = indicator
        elif isinstance(indicator, indicators.StaffLines):
            key = indicator.line_count
        elif isinstance(
            indicator, (indicators.Accelerando, indicators.Ritardando)
        ):
            key = {"hide": indicator.hide}
        else:
            key = str(indicator)
        return key

    def _initialize_time_signatures(self, time_signatures):
        time_signatures = time_signatures or ()
        time_signatures_ = list(time_signatures)
        time_signatures_ = []
        for time_signature in time_signatures:
            time_signature = abjad.TimeSignature(time_signature)
            time_signatures_.append(time_signature)
        time_signatures_ = tuple(time_signatures_)
        if not time_signatures_:
            time_signatures_ = None
        self._time_signatures = time_signatures_

    def _intercalate_silences(self, timespans, voice_name):
        selections = []
        durations = [_.duration for _ in self.time_signatures]
        measure_start_offsets = abjad.mathtools.cumulative_sums(durations)
        segment_duration = measure_start_offsets[-1]
        self._segment_duration = segment_duration
        previous_stop_offset = abjad.Offset(0)
        for timespan in timespans:
            start_offset = timespan.start_offset
            if start_offset < previous_stop_offset:
                raise Exception("overlapping offsets: {timespan!r}.")
            if previous_stop_offset < start_offset:
                selection = self._make_measure_silences(
                    previous_stop_offset,
                    start_offset,
                    measure_start_offsets,
                    voice_name,
                )
                ###selections.extend(silences)
                selections.append(selection)
            selection = timespan.annotation
            assert isinstance(selection, abjad.Selection), repr(selection)
            selections.append(selection)
            duration = abjad.inspect(selection).duration()
            previous_stop_offset = start_offset + duration
        if previous_stop_offset < segment_duration:
            selection = self._make_measure_silences(
                previous_stop_offset,
                segment_duration,
                measure_start_offsets,
                voice_name,
            )
            assert isinstance(selection, abjad.Selection)
            ###selections.extend(silences)
            selections.append(selection)
        assert all(isinstance(_, abjad.Selection) for _ in selections)
        return selections

    def _key_to_indicator(self, key, prototype):
        assert isinstance(key, (int, str)), repr(key)
        if key is None:
            return
        if prototype in (abjad.Clef, abjad.Dynamic):
            indicator = prototype(key)
        elif prototype is abjad.Instrument:
            indicator = self.instruments.get(key)
        elif prototype is abjad.MarginMarkup:
            indicator = self.margin_markups.get(key)
        elif prototype is abjad.MetronomeMark:
            indicator = self.metronome_marks.get(key)
        elif prototype is abjad.TimeSignature:
            indicator = abjad.TimeSignature.from_string(key)
        elif prototype is indicators.StaffLines:
            indicator = indicators.StaffLines(line_count=key)
        else:
            raise Exception(prototype)
        return indicator

    def _label_clock_time(self):
        if self.environment == "docs":
            return
        skips = classes.Selection(self.score["Global_Skips"]).skips()
        clock_times = self._calculate_clock_times()
        if clock_times is None:
            return
        total = len(skips)
        clock_times = clock_times[:total]
        first_measure_number = self._get_first_measure_number()
        final_clock_time = clock_times[-1]
        final_clock_string = final_clock_time.to_clock_string()
        final_seconds = int(final_clock_time)
        final_fermata_string = f"{final_seconds}''"
        final_measure_number = first_measure_number + total - 1
        final_is_fermata = False
        if final_measure_number in self._fermata_measure_numbers:
            final_is_fermata = True
        for measure_index in range(len(skips)):
            measure_number = first_measure_number + measure_index
            is_fermata, fermata_duration = False, None
            if measure_number in self._fermata_measure_numbers:
                is_fermata = True
            skip = skips[measure_index]
            clock_time = clock_times[measure_index]
            clock_string = clock_time.to_clock_string()
            seconds = int(clock_time)
            fermata_string = f"{seconds}''"
            if measure_index < total - 1:
                tag = abjad.const.CLOCK_TIME
                if measure_index == total - 2:
                    if is_fermata and final_is_fermata:
                        string = r"- \baca-start-ct-both-fermata"
                        string += (
                            f' "{fermata_string}" "{final_fermata_string}"'
                        )
                    elif is_fermata and not final_is_fermata:
                        string = r"- \baca-start-ct-both-left-fermata"
                        string += (
                            f' "{fermata_string}" "[{final_clock_string}]"'
                        )
                    elif not is_fermata and final_is_fermata:
                        string = r"- \baca-start-ct-both-right-fermata"
                        string += (
                            f' "[{clock_string}]" "{final_fermata_string}"'
                        )
                    else:
                        string = r"- \baca-start-ct-both"
                        string += (
                            f' "[{clock_string}]" "[{final_clock_string}]"'
                        )
                else:
                    if not is_fermata:
                        string = r"- \baca-start-ct-left-only"
                        string += f' "[{clock_string}]"'
                    else:
                        seconds = int(clock_time)
                        string = r"- \baca-start-ct-left-only-fermata"
                        string += f' "{fermata_string}"'
                start_text_span = abjad.StartTextSpan(
                    command=r"\bacaStartTextSpanCT", left_text=string
                )
                abjad.attach(
                    start_text_span,
                    skip,
                    context="GlobalSkips",
                    deactivate=True,
                    tag=tag,
                )
            if 0 < measure_index:
                tag = abjad.Tag(abjad.const.CLOCK_TIME)
                stop_text_span = abjad.StopTextSpan(
                    command=r"\bacaStopTextSpanCT"
                )
                abjad.attach(
                    stop_text_span,
                    skip,
                    context="GlobalSkips",
                    deactivate=True,
                    tag=tag,
                )

    def _label_measure_numbers(self):
        skips = classes.Selection(self.score["Global_Skips"]).skips()
        total = len(skips)
        first_measure_number = self._get_first_measure_number()
        for measure_index, skip in enumerate(skips):
            local_measure_number = measure_index + 1
            measure_number = first_measure_number + measure_index
            if measure_index < total - 1:
                tag = abjad.Tag(abjad.const.LOCAL_MEASURE_NUMBER)
                string = r"- \baca-start-lmn-left-only"
                string += f' "{local_measure_number}"'
                start_text_span = abjad.StartTextSpan(
                    command=r"\bacaStartTextSpanLMN", left_text=string
                )
                abjad.attach(
                    start_text_span,
                    skip,
                    context="GlobalSkips",
                    deactivate=True,
                    tag=tag,
                )
                tag = abjad.Tag(abjad.const.MEASURE_NUMBER)
                string = r"- \baca-start-mn-left-only"
                string += f' "{measure_number}"'
                start_text_span = abjad.StartTextSpan(
                    command=r"\bacaStartTextSpanMN", left_text=string
                )
                abjad.attach(
                    start_text_span,
                    skip,
                    context="GlobalSkips",
                    deactivate=True,
                    tag=tag,
                )
            if 0 < measure_index:
                tag = abjad.Tag(abjad.const.LOCAL_MEASURE_NUMBER)
                stop_text_span = abjad.StopTextSpan(
                    command=r"\bacaStopTextSpanLMN"
                )
                abjad.attach(
                    stop_text_span,
                    skip,
                    context="GlobalSkips",
                    deactivate=True,
                    tag=tag,
                )
                tag = abjad.Tag(abjad.const.MEASURE_NUMBER)
                stop_text_span = abjad.StopTextSpan(
                    command=r"\bacaStopTextSpanMN"
                )
                abjad.attach(
                    stop_text_span,
                    skip,
                    context="GlobalSkips",
                    deactivate=True,
                    tag=tag,
                )

    def _label_stage_numbers(self):
        skips = classes.Selection(self.score["Global_Skips"]).skips()
        if not self.stage_markup:
            return
        total = len(self.stage_markup)
        for i, item in enumerate(self.stage_markup):
            if len(item) == 2:
                value, lmn = item
                color = None
            elif len(item) == 3:
                value, lmn, color = item
            else:
                raise Exception(item)
            measure_index = lmn - 1
            skip = skips[measure_index]
            tag = abjad.Tag(abjad.const.STAGE_NUMBER)
            if color is not None:
                string = r"- \baca-start-snm-colored-left-only"
                string += f' "{value}" #{color}'
            else:
                string = r"- \baca-start-snm-left-only"
                string += f' "{value}"'
            start_text_span = abjad.StartTextSpan(
                command=r"\bacaStartTextSpanSNM", left_text=string
            )
            abjad.attach(
                start_text_span,
                skip,
                context="GlobalSkips",
                deactivate=True,
                tag=tag,
            )
            if 0 < i:
                tag = abjad.Tag(abjad.const.STAGE_NUMBER)
                stop_text_span = abjad.StopTextSpan(
                    command=r"\bacaStopTextSpanSNM"
                )
                abjad.attach(
                    stop_text_span,
                    skip,
                    context="GlobalSkips",
                    deactivate=True,
                    tag=tag,
                )
        skip = skips[-1]
        tag = abjad.Tag(abjad.const.STAGE_NUMBER)
        stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanSNM")
        abjad.attach(
            stop_text_span,
            skip,
            context="GlobalSkips",
            deactivate=True,
            tag=tag,
        )

    def _magnify_staves_(self):
        if self.magnify_staves is None:
            return
        if isinstance(self.magnify_staves, tuple):
            multiplier, tag = self.magnify_staves
        else:
            multiplier, tag = self.magnify_staves, None
        multiplier = abjad.Multiplier(multiplier)
        numerator, denominator = multiplier.pair
        string = rf"\magnifyStaff #{numerator}/{denominator}"
        tag = abjad.Tag(tag).prepend("_magnify_staves_")
        for staff in abjad.iterate(self.score).components(abjad.Staff):
            first_leaf = abjad.inspect(staff).leaf(0)
            assert first_leaf is not None
            literal = abjad.LilyPondLiteral(string)
            abjad.attach(literal, first_leaf, tag=tag)

    def _make_global_rests(self):
        rests = []
        for time_signature in self.time_signatures:
            rest = abjad.MultimeasureRest(
                abjad.Duration(1),
                multiplier=time_signature.duration,
                tag="_make_global_rests(1)",
            )
            rests.append(rest)
        if not self.remove_phantom_measure:
            tag = f"{const.PHANTOM}:_make_global_rests(2)"
            rest = abjad.MultimeasureRest(
                abjad.Duration(1), multiplier=(1, 4), tag=tag
            )
            abjad.annotate(rest, const.PHANTOM, True)
            rests.append(rest)
        return rests

    def _make_global_skips(self):
        context = self.score["Global_Skips"]
        for time_signature in self.time_signatures:
            skip = abjad.Skip(
                1,
                multiplier=time_signature.duration,
                tag="_make_global_skips(1)",
            )
            abjad.attach(
                time_signature,
                skip,
                context="Score",
                tag="_make_global_skips(2)",
            )
            context.append(skip)
        if not self.remove_phantom_measure:
            tag = f"{const.PHANTOM}:_make_global_skips(3)"
            skip = abjad.Skip(1, multiplier=(1, 4), tag=tag)
            abjad.annotate(skip, const.PHANTOM, True)
            context.append(skip)
            if time_signature != abjad.TimeSignature((1, 4)):
                time_signature = abjad.TimeSignature((1, 4))
                abjad.attach(time_signature, skip, context="Score", tag=tag)
        if self.first_segment:
            return
        # empty start bar allows LilyPond to print bar numbers
        # at start of nonfirst segments
        first_skip = classes.Selection(context).skip(0)
        literal = abjad.LilyPondLiteral(r'\bar ""')
        tag = abjad.Tag(abjad.tags.EMPTY_START_BAR)
        tag = tag.prepend("+SEGMENT")
        abjad.attach(
            literal, first_skip, tag=tag.prepend("_make_global_skips(3)")
        )

    def _make_lilypond_file(self):
        tag = "baca.SegmentMaker._make_lilypond_file"
        includes = self._get_lilypond_includes()
        lilypond_file = abjad.LilyPondFile.new(
            music=self.score,
            date_time_token=False,
            includes=includes,
            tag=tag,
            use_relative_includes=False,
        )
        block_names = ("layout", "paper")
        for item in lilypond_file.items[:]:
            if getattr(item, "name", None) in block_names:
                lilypond_file.items.remove(item)
        if self._midi:
            block = abjad.Block(name="midi")
            lilypond_file.items.append(block)
        for item in lilypond_file.items[:]:
            if getattr(item, "name", None) == "header":
                lilypond_file.items.remove(item)
        if self.environment != "docs" and not self.do_not_include_layout_ly:
            assert len(lilypond_file.score_block.items) == 1
            score = lilypond_file.score_block.items[0]
            assert isinstance(score, abjad.Score)
            include = abjad.Container(tag=tag)
            literal = abjad.LilyPondLiteral("", "absolute_before")
            abjad.attach(literal, include, tag=None)
            string = r'\include "layout.ly"'
            literal = abjad.LilyPondLiteral(string, "opening")
            abjad.attach(literal, include, tag=tag)
            container = abjad.Container(
                [include, score], simultaneous=True, tag=tag
            )
            literal = abjad.LilyPondLiteral("", "absolute_before")
            abjad.attach(literal, container, tag=None)
            literal = abjad.LilyPondLiteral("", "closing")
            abjad.attach(literal, container, tag=None)
            lilypond_file.score_block.items[:] = [container]
            lilypond_file.score_block.items.append("")
        self._lilypond_file = lilypond_file

    def _make_measure_silences(
        self, start, stop, measure_start_offsets, voice_name
    ):
        tag = "_make_measure_silences"
        offsets = [start]
        for measure_start_offset in measure_start_offsets:
            if start < measure_start_offset < stop:
                offsets.append(measure_start_offset)
        offsets.append(stop)
        silences = []
        durations = abjad.mathtools.difference_series(offsets)
        for i, duration in enumerate(durations):
            if i == 0:
                silence = self._make_multimeasure_rest_container(
                    voice_name, duration
                )
            else:
                if self.skips_instead_of_rests:
                    silence = abjad.Skip(1, multiplier=duration, tag=tag)
                else:
                    silence = abjad.MultimeasureRest(
                        1, multiplier=duration, tag=tag
                    )
            silences.append(silence)
        assert all(isinstance(_, abjad.Component) for _ in silences)
        selection = abjad.select(silences)
        return selection

    def _make_multimeasure_rest_container(
        self, voice_name, duration, phantom=False, suppress_note=False
    ):
        tag = "_make_multimeasure_rest_container"
        if phantom is True:
            tag = f"{const.PHANTOM}:{tag}"
        if suppress_note is True:
            assert phantom is True
        if suppress_note is not True:
            note = abjad.Note("c'1", multiplier=duration, tag=tag)
        else:
            note = abjad.MultimeasureRest(1, multiplier=duration, tag=tag)
        literal = abjad.LilyPondLiteral(r"\baca-invisible-music")
        abjad.attach(literal, note, tag=tag)
        abjad.annotate(note, abjad.const.HIDDEN, True)
        hidden_note_voice = abjad.Voice([note], name=voice_name, tag=tag)
        abjad.annotate(hidden_note_voice, const.HIDDEN_NOTE_VOICE, True)
        abjad.annotate(hidden_note_voice, const.INTERMITTENT, True)
        if self.skips_instead_of_rests:
            rest = abjad.Skip(1, multiplier=duration, tag=tag)
        else:
            rest = abjad.MultimeasureRest(1, multiplier=duration, tag=tag)
        if "Music_Voice" in voice_name:
            name = voice_name.replace("Music_Voice", "Rest_Voice")
        else:
            name = voice_name.replace("Voice", "Rest_Voice")
        multimeasure_rest_voice = abjad.Voice([rest], name=name, tag=tag)
        abjad.annotate(multimeasure_rest_voice, const.INTERMITTENT, True)
        container = abjad.Container(
            [hidden_note_voice, multimeasure_rest_voice],
            simultaneous=True,
            tag=tag,
        )
        abjad.annotate(container, const.MULTIMEASURE_REST_CONTAINER, True)
        if phantom is True:
            for component in abjad.iterate(container).components():
                abjad.annotate(component, const.PHANTOM, True)
        return container

    def _make_score(self):
        score_template = getattr(self, "score_template")
        if score_template is None:
            message = "segment-maker can not find score template."
            raise Exception(message)
        score = score_template()
        self._score = score
        if self.do_not_include_layout_ly:
            first_measure_number = self._get_first_measure_number()
            if first_measure_number != 1:
                abjad.setting(score).current_bar_number = first_measure_number

    def _momento_to_indicator(self, momento):
        # for selector evaluation:
        import baca

        if momento.manifest is not None:
            dictionary = getattr(self, momento.manifest)
            if dictionary is None:
                raise Exception(f"can not find {name!r} manifest.")
            return dictionary.get(momento.value)
        class_ = eval(momento.prototype)
        if hasattr(class_, "from_string"):
            indicator = class_.from_string(momento.value)
        elif class_ is abjad.Dynamic and momento.value.startswith("\\"):
            indicator = class_(name="", command=momento.value)
        elif isinstance(momento.value, class_):
            indicator = momento.value
        elif class_ is indicators.StaffLines:
            indicator = class_(line_count=momento.value)
        elif momento.value is None:
            indicator = class_()
        elif isinstance(momento.value, dict):
            indicator = class_(**momento.value)
        else:
            try:
                indicator = class_(momento.value)
            except:
                raise Exception(format(momento))
        return indicator

    def _move_global_rests(self):
        string = "_global_rests_in_topmost_staff"
        if not getattr(self.score_template, string, None):
            return
        if "Global_Rests" not in self.score:
            return
        global_rests = self.score["Global_Rests"]
        self.score["Global_Context"].remove(global_rests)
        music_context = self.score["Music_Context"]
        for staff in abjad.iterate(music_context).components(abjad.Staff):
            break
        staff.simultaneous = True
        staff.insert(0, global_rests)

    def _populate_offset_to_measure_number(self):
        measure_number = self._get_first_measure_number()
        for skip in classes.Selection(self.score["Global_Skips"]).skips():
            offset = abjad.inspect(skip).timespan().start_offset
            self._offset_to_measure_number[offset] = measure_number
            measure_number += 1

    @staticmethod
    def _prepend_tag_to_wrappers(leaf, tag):
        for wrapper in abjad.inspect(leaf).wrappers():
            if isinstance(wrapper.indicator, abjad.LilyPondLiteral):
                if wrapper.indicator.argument == "":
                    continue
            tag_ = wrapper.tag.prepend(tag)
            wrapper.tag = tag_

    def _print_cache(self):
        for context in self._cache:
            print(f"CONTEXT {context} ...")
            leaves_by_measure_number = self._cache[context]
            for measure_number in leaves_by_measure_number:
                print(f"MEASURE {measure_number} ...")
                for leaf in leaves_by_measure_number[measure_number]:
                    print(leaf)

    @staticmethod
    def _prototype_string(class_):
        parts = class_.__module__.split(".")
        if parts[-1] != class_.__name__:
            parts.append(class_.__name__)
        return f"{parts[0]}.{parts[-1]}"

    def _reanalyze_trending_dynamics(self):
        for leaf in abjad.iterate(self.score).leaves():
            for wrapper in abjad.inspect(leaf).wrappers():
                if isinstance(
                    wrapper.indicator, abjad.Dynamic
                ) and abjad.inspect(leaf).indicators(abjad.StartHairpin):
                    self._treat_persistent_wrapper(
                        self.manifests, wrapper, "explicit"
                    )

    def _reapply_persistent_indicators(self):
        if self.first_segment:
            return
        string = "persistent_indicators"
        dictionary = self.previous_persist.get("persistent_indicators")
        if not dictionary:
            return
        for context in abjad.iterate(self.score).components(abjad.Context):
            momentos = dictionary.get(context.name)
            if not momentos:
                continue
            for momento in momentos:
                result = self._analyze_momento(context, momento)
                if result is None:
                    continue
                leaf, previous_indicator, status, edition = result
                if isinstance(previous_indicator, abjad.TimeSignature):
                    if status in (None, "explicit"):
                        continue
                    assert status == "reapplied", repr(status)
                    wrapper = abjad.inspect(leaf).wrapper(abjad.TimeSignature)
                    site = "_reapply_persistent_indicators(1)"
                    edition = edition.prepend(site)
                    wrapper.tag = wrapper.tag.prepend(edition)
                    self._treat_persistent_wrapper(
                        self.manifests, wrapper, status
                    )
                    continue
                # TODO: change to parameter comparison
                prototype = (
                    indicators.Accelerando,
                    abjad.MetronomeMark,
                    indicators.Ritardando,
                )
                if isinstance(previous_indicator, prototype):
                    site = "_reapply_persistent_indicators(2)"
                    if status == "reapplied":
                        wrapper = abjad.attach(
                            previous_indicator,
                            leaf,
                            tag=edition.append(site),
                            wrapper=True,
                        )
                        self._treat_persistent_wrapper(
                            self.manifests, wrapper, status
                        )
                    else:
                        assert status in ("redundant", None), repr(status)
                        if status is None:
                            status = "explicit"
                        wrappers = abjad.inspect(leaf).wrappers(prototype)
                        # lone metronome mark or lone tempo trend:
                        if len(wrappers) == 1:
                            wrapper = wrappers[0]
                        # metronome mark + tempo trend:
                        else:
                            assert 1 < len(wrappers), repr(wrappers)
                            prototype = abjad.MetronomeMark
                            wrapper = abjad.inspect(leaf).wrapper(prototype)
                        wrapper.tag = wrapper.tag.prepend(edition)
                        self._treat_persistent_wrapper(
                            self.manifests, wrapper, status
                        )
                    continue
                attached = False
                site = "_reapply_persistent_indicators(3)"
                tag = edition.append(site)
                if isinstance(previous_indicator, abjad.MarginMarkup):
                    tag = tag.append("-PARTS")
                try:
                    wrapper = abjad.attach(
                        previous_indicator, leaf, tag=tag, wrapper=True
                    )
                    attached = True
                except abjad.PersistentIndicatorError:
                    pass
                if attached:
                    self._treat_persistent_wrapper(
                        self.manifests, wrapper, status
                    )

    def _remove_redundant_time_signatures(self):
        previous_time_signature = None
        self._cached_time_signatures = []
        skips = classes.Selection(self.score["Global_Skips"]).skips()
        if not self.remove_phantom_measure:
            skips = skips[:-1]
        for skip in skips:
            time_signature = abjad.inspect(skip).indicator(abjad.TimeSignature)
            self._cached_time_signatures.append(str(time_signature))
            if time_signature == previous_time_signature:
                abjad.detach(time_signature, skip)
            else:
                previous_time_signature = time_signature

    def _remove_tags(self, tags):
        tags = tags or []
        tags = list(tags)
        if self.environment == "docs":
            tags += abjad.tags.documentation_removal_tags()
        for leaf in abjad.iterate(self.score).leaves():
            for wrapper in abjad.inspect(leaf).wrappers():
                if wrapper.tag is None:
                    continue
                for word in wrapper.tag:
                    if word in tags:
                        abjad.detach(wrapper, leaf)
                        break

    def _scope_to_leaf_selection(self, command):
        leaves = []
        selections = self._scope_to_leaf_selections(command.scope)
        for selection in selections:
            leaves.extend(selection)
        selection = abjad.select(leaves)
        if not selection:
            message = f"EMPTY SELECTION:\n\n{format(command)}"
            if self.allow_empty_selections:
                print(message)
            else:
                raise Exception(message)
        assert selection.are_leaves(), repr(selection)
        if isinstance(command.scope, scoping.TimelineScope):
            selection = command.scope._sort_by_timeline(selection)
        return selection

    def _scope_to_leaf_selections(self, scope):
        if self._cache is None:
            self._cache_leaves()
        if isinstance(scope, scoping.Scope):
            scopes = [scope]
        else:
            assert isinstance(scope, scoping.TimelineScope)
            scopes = list(scope.scopes)
        leaf_selections = []
        for scope in scopes:
            leaves = []
            try:
                leaves_by_measure_number = self._cache[scope.voice_name]
            except KeyError:
                print(f"Unknown voice {scope.voice_name} ...\n")
                raise
            start = scope.measures[0]
            if scope.measures[1] == -1:
                stop = self.measure_count + 1
            else:
                stop = scope.measures[1] + 1
            if start < 0:
                start = self.measure_count - abs(start) + 1
            if stop < 0:
                stop = self.measure_count - abs(stop) + 1
            for measure_number in range(start, stop):
                leaves_ = leaves_by_measure_number.get(measure_number, [])
                leaves.extend(leaves_)
            leaf_selections.append(abjad.select(leaves))
        return leaf_selections

    def _set_status_tag(wrapper, status, redraw=None, stem=None):
        assert isinstance(wrapper, abjad.Wrapper), repr(wrapper)
        stem = stem or abjad.String.to_indicator_stem(wrapper.indicator)
        prefix = None
        if redraw is True:
            prefix = "redrawn"
        tag = wrapper.tag.prepend("_set_status_tag")
        status_tag = SegmentMaker._get_tag(status, stem, prefix=prefix)
        tag = tag.prepend(status_tag)
        wrapper.tag = tag

    def _shift_clefs_into_fermata_measures(self):
        fermata_stop_offsets = self._fermata_stop_offsets[:]
        if self.previous_metadata.get("final_measure_is_fermata") is True:
            fermata_stop_offsets.insert(0, abjad.Offset(0))
        if not fermata_stop_offsets:
            return
        for staff in abjad.iterate(self.score).components(abjad.Staff):
            for leaf in abjad.iterate(staff).leaves():
                start_offset = abjad.inspect(leaf).timespan().start_offset
                if start_offset not in fermata_stop_offsets:
                    continue
                wrapper = abjad.inspect(leaf).wrapper(abjad.Clef)
                if wrapper is None or not wrapper.tag:
                    continue
                if abjad.tags.EXPLICIT_CLEF not in wrapper.tag:
                    continue
                measure_number = self._offset_to_measure_number.get(
                    start_offset
                )
                if measure_number is None:
                    continue
                clef = wrapper.indicator
                suite = baca_overrides.clef_shift(
                    clef, selector="baca.leaf(0)"
                )
                runtime = self._bundle_manifests()
                suite(leaf, runtime=runtime)

    def _style_fermata_measures(self):
        if (
            self.fermata_measure_staff_line_count is None
            and self.fermata_measure_empty_overrides is None
        ):
            return
        if not self._fermata_start_offsets:
            return
        prototype = indicators.StaffLines
        bar_lines_already_styled = []
        empty_fermata_measure_start_offsets = []
        for measure_number in self.fermata_measure_empty_overrides or []:
            timespan = self._get_measure_timespan(measure_number)
            empty_fermata_measure_start_offsets.append(timespan.start_offset)
        for staff in abjad.iterate(self.score).components(abjad.Staff):
            for leaf in abjad.iterate(staff).leaves():
                if abjad.inspect(leaf).annotation(const.PHANTOM) is True:
                    continue
                start_offset = abjad.inspect(leaf).timespan().start_offset
                if start_offset not in self._fermata_start_offsets:
                    continue
                voice = abjad.inspect(leaf).parentage().get(abjad.Voice)
                if "Rest_Voice" in voice.name:
                    continue
                if start_offset in empty_fermata_measure_start_offsets:
                    staff_lines = indicators.StaffLines(line_count=0)
                elif self.fermata_measure_staff_line_count is None:
                    continue
                else:
                    staff_lines = indicators.StaffLines(
                        line_count=self.fermata_measure_staff_line_count
                    )
                before = abjad.inspect(leaf).effective(prototype)
                next_leaf = abjad.inspect(leaf).leaf(1)
                if abjad.inspect(next_leaf).annotation(const.PHANTOM) is True:
                    next_leaf = None
                after = None
                if next_leaf is not None:
                    after = abjad.inspect(next_leaf).effective(prototype)
                if before != staff_lines:
                    strings = staff_lines._get_lilypond_format(context=staff)
                    if getattr(before, "line_count", 5) == 5:
                        context = staff.lilypond_type
                        string = f"{context}.BarLine.bar-extent = #'(-2 . 2)"
                        string = r"\once \override " + string
                        strings.append(string)
                    if strings:
                        literal = abjad.LilyPondLiteral(strings)
                        abjad.attach(
                            literal, leaf, tag="_style_fermata_measures(1)"
                        )
                if next_leaf is not None and staff_lines != after:
                    if after is None:
                        after_ = indicators.StaffLines(line_count=5)
                    else:
                        after_ = after
                    strings = after_._get_lilypond_format(context=staff)
                    literal = abjad.LilyPondLiteral(strings)
                    abjad.attach(
                        literal, next_leaf, tag="_style_fermata_measures(2)"
                    )
                if next_leaf is None and before != staff_lines:
                    if before is None:
                        before_line_count = 5
                    else:
                        before_line_count = getattr(before, "line_count", 5)
                    strings = [
                        r"\stopStaff",
                        r"\once \override Staff.StaffSymbol.line-count ="
                        f" {before_line_count}",
                        r"\startStaff",
                    ]
                    literal = abjad.LilyPondLiteral(
                        strings, format_slot="after"
                    )
                    abjad.attach(
                        literal, leaf, tag="_style_fermata_measures(3)"
                    )
                if start_offset in bar_lines_already_styled:
                    continue
                strings = []
                if staff_lines.line_count == 0 and not (
                    next_leaf is None and self.final_segment
                ):
                    string = r"Score.BarLine.transparent = ##t"
                    string = r"\once \override " + string
                    strings.append(string)
                    string = r"Score.SpanBar.transparent = ##t"
                    string = r"\once \override " + string
                    strings.append(string)
                elif staff_lines.line_count == 1:
                    string = "Score.BarLine.bar-extent = #'(-2 . 2)"
                    string = r"\once \override " + string
                    strings.append(string)
                if strings:
                    literal = abjad.LilyPondLiteral(strings, "after")
                    tag = abjad.Tag(abjad.tags.EOL_FERMATA)
                    measure_number_tag = self._get_measure_number_tag(leaf)
                    if measure_number_tag is not None:
                        tag = tag.append(measure_number_tag)
                    abjad.attach(
                        literal,
                        leaf,
                        tag=tag.prepend("_style_fermata_measures(4)"),
                    )
                bar_lines_already_styled.append(start_offset)
        if not self.fermata_measure_empty_overrides:
            return
        pair = (0, 2.5)
        prototype = abjad.MultimeasureRest
        rests = classes.Selection(self.score["Global_Rests"]).leaves(prototype)
        for measure_number in self.fermata_measure_empty_overrides:
            measure_index = measure_number - 1
            rest = rests[measure_index]
            abjad.override(rest).multi_measure_rest_text.extra_offset = pair

    def _style_phantom_measures(self):
        if self.remove_phantom_measure:
            return
        tag = const.PHANTOM
        skip = abjad.inspect(self.score["Global_Skips"]).leaf(-1)
        for literal in abjad.inspect(skip).indicators(abjad.LilyPondLiteral):
            if r"\baca-time-signature-color" in literal.argument:
                abjad.detach(literal, skip)
        self._prepend_tag_to_wrappers(
            skip, f"{tag}:_style_phantom_measures(1)"
        )
        string = r"\baca-time-signature-transparent"
        literal = abjad.LilyPondLiteral(string)
        abjad.attach(literal, skip, tag=f"{tag}:_style_phantom_measures(2)")
        strings = [
            r"\once \override Score.BarLine.transparent = ##t",
            r"\once \override Score.SpanBar.transparent = ##t",
        ]
        literal = abjad.LilyPondLiteral(strings, format_slot="after")
        abjad.attach(literal, skip, tag=f"{tag}:_style_phantom_measures(3)")
        if "Global_Rests" in self.score:
            rest = self.score["Global_Rests"][-1]
            self._prepend_tag_to_wrappers(
                rest, f"{tag}:_style_phantom_measures(4)"
            )
        start_offset = abjad.inspect(skip).timespan().start_offset
        enumeration = const.MULTIMEASURE_REST_CONTAINER
        containers = []
        for container in abjad.select(self.score).components(abjad.Container):
            if abjad.inspect(container).annotation(enumeration) is not True:
                continue
            leaf = abjad.inspect(container).leaf(0)
            if abjad.inspect(leaf).timespan().start_offset != start_offset:
                continue
            containers.append(container)
        string_1 = r"\once \override Score.TimeSignature.X-extent = ##f"
        string_2 = r"\once \override MultiMeasureRest.transparent = ##t"
        strings = [
            r"\stopStaff",
            r"\once \override Staff.StaffSymbol.transparent = ##t",
            r"\startStaff",
        ]
        for container in containers:
            for leaf in abjad.select(container).leaves():
                self._prepend_tag_to_wrappers(
                    leaf, f"{tag}:_style_phantom_measures(5)"
                )
                if not isinstance(leaf, abjad.MultimeasureRest):
                    continue
                if abjad.inspect(leaf).annotation(abjad.const.HIDDEN) is True:
                    continue
                literal = abjad.LilyPondLiteral(string_1)
                abjad.attach(
                    literal, leaf, tag=f"{tag}:_style_phantom_measures(6)"
                )
                literal = abjad.LilyPondLiteral(string_2)
                abjad.attach(
                    literal, leaf, tag=f"{tag}:_style_phantom_measures(7)"
                )
                literal = abjad.LilyPondLiteral(strings)
                abjad.attach(
                    literal, leaf, tag=f"{tag}:_style_phantom_measures(8)"
                )

    def _transpose_score_(self):
        if not self.transpose_score:
            return
        for pleaf in classes.Selection(self.score).pleaves():
            if abjad.inspect(pleaf).has_indicator(abjad.tags.DO_NOT_TRANSPOSE):
                continue
            abjad.Instrument.transpose_from_sounding_pitch(pleaf)

    @staticmethod
    def _treat_persistent_wrapper(manifests, wrapper, status):
        assert isinstance(wrapper, abjad.Wrapper), repr(wrapper)
        assert bool(wrapper.indicator.persistent), repr(wrapper)
        assert isinstance(status, str), repr(status)
        indicator = wrapper.indicator
        prototype = (
            abjad.GlissandoIndicator,
            abjad.Ottava,
            abjad.RepeatTie,
            abjad.StartBeam,
            abjad.StartPianoPedal,
            abjad.StartSlur,
            abjad.StartTextSpan,
            abjad.StartTrillSpan,
            abjad.StopBeam,
            abjad.StopPianoPedal,
            abjad.StopSlur,
            abjad.StopTextSpan,
            abjad.StopTrillSpan,
            abjad.Tie,
        )
        if isinstance(indicator, prototype):
            return
        context = wrapper._find_correct_effective_context()
        assert isinstance(context, abjad.Context), repr(wrapper)
        leaf = wrapper.component
        assert isinstance(leaf, abjad.Leaf), repr(wrapper)
        existing_tag = wrapper.tag
        tempo_trend = (indicators.Accelerando, indicators.Ritardando)
        if isinstance(indicator, abjad.MetronomeMark) and abjad.inspect(
            leaf
        ).has_indicator(tempo_trend):
            status = "explicit"
        if isinstance(wrapper.indicator, abjad.Dynamic) and abjad.inspect(
            leaf
        ).indicators(abjad.StartHairpin):
            status = "explicit"
        if isinstance(wrapper.indicator, (abjad.Dynamic, abjad.StartHairpin)):
            color = SegmentMaker._status_to_color[status]
            words = [
                f"{status.upper()}_DYNAMIC_COLOR",
                "_treat_persistent_wrapper(1)",
            ]
            words.extend(existing_tag.editions())
            tag_ = abjad.Tag.from_words(words)
            string = f"#(x11-color '{color})"
            abjad.tweak(wrapper.indicator, tag=tag_).color = string
            SegmentMaker._set_status_tag(wrapper, status)
            return
        SegmentMaker._attach_color_literal(
            wrapper, status, existing_deactivate=wrapper.deactivate
        )
        SegmentMaker._attach_latent_indicator_alert(
            manifests, wrapper, status, existing_deactivate=wrapper.deactivate
        )
        SegmentMaker._attach_color_cancelation_literal(
            wrapper,
            status,
            existing_deactivate=wrapper.deactivate,
            existing_tag=existing_tag,
        )
        if isinstance(wrapper.indicator, abjad.Clef):
            string = rf"\set {context.lilypond_type}.forceClef = ##t"
            literal = abjad.LilyPondLiteral(string)
            wrapper_ = abjad.attach(
                literal,
                wrapper.component,
                tag=wrapper.tag.prepend("_treat_persistent_wrapper(2)"),
                wrapper=True,
            )
            SegmentMaker._set_status_tag(wrapper_, status, stem="CLEF")
        SegmentMaker._set_status_tag(wrapper, status)
        SegmentMaker._attach_color_redraw_literal(
            wrapper,
            status,
            existing_deactivate=wrapper.deactivate,
            existing_tag=existing_tag,
        )
        if isinstance(
            indicator, (abjad.Instrument, abjad.MarginMarkup)
        ) and not getattr(indicator, "hide", False):
            strings = indicator._get_lilypond_format(context=context)
            literal = abjad.LilyPondLiteral(strings, "after")
            stem = abjad.String.to_indicator_stem(indicator)
            wrapper_ = abjad.attach(
                literal,
                leaf,
                tag=existing_tag.prepend("_treat_persistent_wrapper(3)"),
                wrapper=True,
            )
            SegmentMaker._set_status_tag(
                wrapper_, status, redraw=True, stem=stem
            )

    def _treat_untreated_persistent_wrappers(self):
        if self.environment == "layout":
            return
        dynamic_prototype = (abjad.Dynamic, abjad.StartHairpin)
        tempo_prototype = (
            indicators.Accelerando,
            abjad.MetronomeMark,
            indicators.Ritardando,
        )
        for leaf in abjad.iterate(self.score).leaves():
            for wrapper in abjad.inspect(leaf).wrappers():
                if not getattr(wrapper.indicator, "persistent", False):
                    continue
                if wrapper.tag and wrapper.tag.has_persistence_tag():
                    continue
                if isinstance(wrapper.indicator, abjad.Instrument):
                    prototype = abjad.Instrument
                elif isinstance(wrapper.indicator, dynamic_prototype):
                    prototype = dynamic_prototype
                elif isinstance(wrapper.indicator, tempo_prototype):
                    prototype = tempo_prototype
                else:
                    prototype = type(wrapper.indicator)
                # TODO: optimize
                previous_indicator = abjad.inspect(leaf).effective(
                    prototype, n=-1
                )
                if scoping.compare_persistent_indicators(
                    previous_indicator, wrapper.indicator
                ):
                    status = "redundant"
                else:
                    status = "explicit"
                self._treat_persistent_wrapper(self.manifests, wrapper, status)

    @staticmethod
    def _unpack_measure_token_list(measure_token_list):
        assert isinstance(measure_token_list, list), repr(measure_token_list)
        measure_tokens = []
        for measure_token in measure_token_list:
            if isinstance(measure_token, int):
                measure_tokens.append(measure_token)
            elif isinstance(measure_token, tuple):
                assert len(measure_token) == 2, repr(scopes)
                start, stop = measure_token
                measure_tokens.append((start, stop))
            else:
                raise TypeError(measure_token_list)
        return measure_tokens

    def _unpack_scope_pair(self, scopes, abbreviations):
        assert isinstance(scopes, tuple), repr(scopes)
        assert len(scopes) == 2, repr(scopes)
        assert isinstance(scopes[0], (list, str)), repr(scopes)
        assert isinstance(scopes[1], (int, list, tuple)), repr(scopes)
        if isinstance(scopes[0], str):
            voice_names = [scopes[0]]
        else:
            voice_names = scopes[0]
        assert isinstance(voice_names, list), repr(voice_names)
        assert all(isinstance(_, str) for _ in voice_names)
        token_type = typing.Union[int, abjad.IntegerPair]
        measure_tokens: typing.List[token_type] = []
        if isinstance(scopes[1], int):
            measure_tokens.append(scopes[1])
        elif isinstance(scopes[1], tuple):
            assert len(scopes[1]) == 2, repr(scopes)
            start, stop = scopes[1]
            measure_tokens.append((start, stop))
        elif isinstance(scopes[1], list):
            measure_tokens = self._unpack_measure_token_list(scopes[1])
        else:
            raise TypeError(scopes)
        scopes_ = []
        voice_names_ = []
        for voice_name in voice_names:
            result = abbreviations.get(voice_name, voice_name)
            if isinstance(result, list):
                voice_names_.extend(result)
            else:
                assert isinstance(result, str)
                voice_names_.append(result)
        voice_names = voice_names_
        for voice_name in voice_names:
            for measure_token in measure_tokens:
                scope = scoping.Scope(
                    measures=measure_token, voice_name=voice_name
                )
                scopes_.append(scope)
        prototype = (scoping.Scope, scoping.TimelineScope)
        assert all(isinstance(_, prototype) for _ in scopes_)
        return scopes_

    def _unpack_scopes(self, scopes, abbreviations):
        scope_type = (scoping.Scope, scoping.TimelineScope)
        scopes__: typing.List[scoping.ScopeTyping]
        if isinstance(scopes, str):
            result = abbreviations.get(scopes, scopes)
            if isinstance(result, str):
                voice_names = [result]
            else:
                assert isinstance(result, list), repr(result)
                voice_names = result
            scopes__ = []
            for voice_name in voice_names:
                scope = scoping.Scope(voice_name=voice_name)
                scopes__.append(scope)
        elif isinstance(scopes, tuple):
            scopes__ = self._unpack_scope_pair(scopes, abbreviations)
        elif isinstance(scopes, scope_type):
            scopes__ = [scopes]
        else:
            assert isinstance(scopes, list), repr(scopes)
            scopes_ = []
            for scope in scopes:
                if isinstance(scope, tuple):
                    scopes__ = self._unpack_scope_pair(scope, abbreviations)
                    scopes_.extend(scopes__)
                else:
                    scopes_.append(scope)
            scopes__ = scopes_
        assert isinstance(scopes__, list), repr(scopes__)
        scopes_ = []
        for scope in scopes__:
            if isinstance(scope, str):
                voice_name = abbreviations.get(scope, scope)
                scope_ = scoping.Scope(voice_name=voice_name)
                scopes_.append(scope_)
            elif isinstance(scope, tuple):
                voice_name, measures = scope
                voice_name = abbreviations.get(voice_name, voice_name)
                if isinstance(measures, list):
                    measures = self._unpack_measure_token_list(measures)
                    for measure_token in measures:
                        scope_ = scoping.Scope(
                            measures=measure_token, voice_name=voice_name
                        )
                        scopes_.append(scope_)
                else:
                    scope_ = scoping.Scope(
                        measures=measures, voice_name=voice_name
                    )
                    scopes_.append(scope_)
            else:
                scope_ = scope
                scopes_.append(scope_)
        return scopes_

    def _update_score_one_time(self):
        is_forbidden_to_update = self.score._is_forbidden_to_update
        self.score._is_forbidden_to_update = False
        self.score._update_now(offsets=True)
        self.score._is_forbidden_to_update = is_forbidden_to_update

    def _validate_measure_count_(self):
        if not self.validate_measure_count:
            return
        found = len(self.time_signatures)
        if found != self.validate_measure_count:
            message = f"found {found} measures"
            message += f" (not {self.validate_measure_count})."
            raise Exception(message)

    def _voice_to_rhythm_commands(self, voice):
        commands = []
        for command in self.commands:
            if not isinstance(command, rhythmcommands.RhythmCommand):
                continue
            if command.scope.voice_name == voice.name:
                commands.append(command)
        return commands

    def _whitespace_leaves(self):
        for leaf in abjad.iterate(self.score).leaves():
            literal = abjad.LilyPondLiteral("", "absolute_before")
            abjad.attach(literal, leaf, tag=None)
        for container in abjad.iterate(self.score).components(abjad.Container):
            if hasattr(container, "_main_leaf"):
                literal = abjad.LilyPondLiteral("", "absolute_after")
                abjad.attach(literal, container, tag=None)
            else:
                literal = abjad.LilyPondLiteral("", "absolute_before")
                abjad.attach(literal, container, tag=None)
            literal = abjad.LilyPondLiteral("", "closing")
            abjad.attach(literal, container, tag=None)

    ### PUBLIC PROPERTIES ###

    @property
    def activate(self) -> typing.Optional[typing.List[str]]:
        """
        Gets tags to activate in LilyPond output.
        """
        return self._activate

    @property
    def allow_empty_selections(self) -> typing.Optional[bool]:
        """
        Is true when segment allows empty selectors.

        Otherwise segment raises exception on empty selectors.
        """
        return self._allow_empty_selections

    @property
    def breaks(self) -> typing.Optional[segmentclasses.BreakMeasureMap]:
        """
        Gets breaks.
        """
        return self._breaks

    @property
    def clock_time_extra_offset(
        self
    ) -> typing.Union[bool, typings.Pair, None]:
        """
        Gets clock time extra offset.
        """
        return self._clock_time_extra_offset

    @property
    def clock_time_override(self) -> typing.Optional[abjad.MetronomeMark]:
        """
        Gets clock time override.
        """
        return self._clock_time_override

    @property
    def color_octaves(self) -> typing.Optional[bool]:
        r"""
        Is true when segment-maker colors octaves.

        ..  container:: example

            Colors octaves:

            >>> maker = baca.SegmentMaker(
            ...     color_octaves=True,
            ...     score_template=baca.StringTrioScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 31)),
            ...     time_signatures=[(6, 16), (6, 16)],
            ...     )

            >>> figure = baca.figure([1], 16)
            >>> selection = figure([[2, 4, 5, 7, 9, 11]])
            >>> maker(
            ...     ('Violin_Music_Voice', 1),
            ...     baca.music(selection),
            ...     )

            >>> selection = figure([[-3, -5, -7, -8, -10, -12]])
            >>> maker(
            ...     ('Cello_Music_Voice', 1),
            ...     baca.music(selection),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.setting(lilypond_file['Score']).auto_beaming = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! baca.StringTrioScoreTemplate.__call__
                \with                                                                                    %! baca.StringTrioScoreTemplate.__call__
                {                                                                                        %! baca.StringTrioScoreTemplate.__call__
                    autoBeaming = ##f                                                                    %! baca.StringTrioScoreTemplate.__call__
                }                                                                                        %! baca.StringTrioScoreTemplate.__call__
                <<                                                                                       %! baca.StringTrioScoreTemplate.__call__
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                    <<                                                                                   %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                        {                                                                                %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #31                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 6/16                                                                   %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #31                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                    \context MusicContext = "Music_Context"                                              %! baca.StringTrioScoreTemplate.__call__
                    <<                                                                                   %! baca.StringTrioScoreTemplate.__call__
                <BLANKLINE>
                        \context StringSectionStaffGroup = "String_Section_Staff_Group"                  %! baca.StringTrioScoreTemplate.__call__
                        <<                                                                               %! baca.StringTrioScoreTemplate.__call__
                <BLANKLINE>
                            \tag Violin                                                                  %! baca.ScoreTemplate._attach_liypond_tag
                            \context ViolinMusicStaff = "Violin_Music_Staff"                             %! baca.StringTrioScoreTemplate.__call__
                            {                                                                            %! baca.StringTrioScoreTemplate.__call__
                <BLANKLINE>
                                \context ViolinMusicVoice = "Violin_Music_Voice"                         %! baca.StringTrioScoreTemplate.__call__
                                {                                                                        %! baca.StringTrioScoreTemplate.__call__
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {                                          %! baca.music
                <BLANKLINE>
                                        % [Violin_Music_Voice measure 1]                                 %! _comment_measure_numbers
                                        \clef "treble"                                                   %! DEFAULT_CLEF:_set_status_tag:abjad.ScoreTemplate.attach_defaults
                                        \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                                    %@% \override ViolinMusicStaff.Clef.color = ##f                      %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                        \set ViolinMusicStaff.forceClef = ##t                            %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):abjad.ScoreTemplate.attach_defaults
                                        d'16                                                             %! baca.music
                                        ^ \baca-default-indicator-markup "(Violin)"                      %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                        \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)     %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
                <BLANKLINE>
                                        e'16                                                             %! baca.music
                <BLANKLINE>
                                        \baca-octave-warning                                             %! _color_octaves_
                                        f'16                                                             %! baca.music
                                        - \tweak color #red                                              %! _color_octaves_
                                        ^ \markup { OCTAVE }                                             %! _color_octaves_
                <BLANKLINE>
                                        g'16                                                             %! baca.music
                <BLANKLINE>
                                        a'16                                                             %! baca.music
                <BLANKLINE>
                                        b'16                                                             %! baca.music
                <BLANKLINE>
                                    }                                                                    %! baca.music
                <BLANKLINE>
                                    <<                                                                   %! _make_multimeasure_rest_container
                <BLANKLINE>
                                        \context Voice = "Violin_Music_Voice"                            %! _make_multimeasure_rest_container
                                        {                                                                %! _make_multimeasure_rest_container
                <BLANKLINE>
                                            % [Violin_Music_Voice measure 2]                             %! _comment_measure_numbers
                                            \baca-invisible-music                                        %! _make_multimeasure_rest_container
                                            c'1 * 3/8                                                    %! _make_multimeasure_rest_container
                <BLANKLINE>
                                        }                                                                %! _make_multimeasure_rest_container
                <BLANKLINE>
                                        \context Voice = "Violin_Rest_Voice"                             %! _make_multimeasure_rest_container
                                        {                                                                %! _make_multimeasure_rest_container
                <BLANKLINE>
                                            % [Violin_Rest_Voice measure 2]                              %! _comment_measure_numbers
                                            R1 * 3/8                                                     %! _make_multimeasure_rest_container
                <BLANKLINE>
                                        }                                                                %! _make_multimeasure_rest_container
                <BLANKLINE>
                                    >>                                                                   %! _make_multimeasure_rest_container
                <BLANKLINE>
                                    <<                                                                   %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        \context Voice = "Violin_Music_Voice"                            %! PHANTOM:_make_multimeasure_rest_container
                                        {                                                                %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                            % [Violin_Music_Voice measure 3]                             %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                            \baca-invisible-music                                        %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                            R1 * 1/4                                                     %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        }                                                                %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        \context Voice = "Violin_Rest_Voice"                             %! PHANTOM:_make_multimeasure_rest_container
                                        {                                                                %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                            % [Violin_Rest_Voice measure 3]                              %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                            \once \override Score.TimeSignature.X-extent = ##f           %! PHANTOM:_style_phantom_measures(6)
                                            \once \override MultiMeasureRest.transparent = ##t           %! PHANTOM:_style_phantom_measures(7)
                                            \stopStaff                                                   %! PHANTOM:_style_phantom_measures(8)
                                            \once \override Staff.StaffSymbol.transparent = ##t          %! PHANTOM:_style_phantom_measures(8)
                                            \startStaff                                                  %! PHANTOM:_style_phantom_measures(8)
                                            R1 * 1/4                                                     %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        }                                                                %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    >>                                                                   %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                }                                                                        %! baca.StringTrioScoreTemplate.__call__
                <BLANKLINE>
                            }                                                                            %! baca.StringTrioScoreTemplate.__call__
                <BLANKLINE>
                            \tag Viola                                                                   %! baca.ScoreTemplate._attach_liypond_tag
                            \context ViolaMusicStaff = "Viola_Music_Staff"                               %! baca.StringTrioScoreTemplate.__call__
                            {                                                                            %! baca.StringTrioScoreTemplate.__call__
                <BLANKLINE>
                                \context ViolaMusicVoice = "Viola_Music_Voice"                           %! baca.StringTrioScoreTemplate.__call__
                                {                                                                        %! baca.StringTrioScoreTemplate.__call__
                <BLANKLINE>
                                    % [Viola_Music_Voice measure 1]                                      %! _comment_measure_numbers
                                    \clef "alto"                                                         %! DEFAULT_CLEF:_set_status_tag:abjad.ScoreTemplate.attach_defaults
                                    \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                                %@% \override ViolaMusicStaff.Clef.color = ##f                           %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                    \set ViolaMusicStaff.forceClef = ##t                                 %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):abjad.ScoreTemplate.attach_defaults
                                    R1 * 6/16                                                            %! _call_rhythm_commands
                                    ^ \baca-default-indicator-markup "(Viola)"                           %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                    \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)          %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
                <BLANKLINE>
                                    % [Viola_Music_Voice measure 2]                                      %! _comment_measure_numbers
                                    R1 * 6/16                                                            %! _call_rhythm_commands
                <BLANKLINE>
                                    <<                                                                   %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        \context Voice = "Viola_Music_Voice"                             %! PHANTOM:_make_multimeasure_rest_container
                                        {                                                                %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                            % [Viola_Music_Voice measure 3]                              %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                            \baca-invisible-music                                        %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                            R1 * 1/4                                                     %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        }                                                                %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        \context Voice = "Viola_Rest_Voice"                              %! PHANTOM:_make_multimeasure_rest_container
                                        {                                                                %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                            % [Viola_Rest_Voice measure 3]                               %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                            \once \override Score.TimeSignature.X-extent = ##f           %! PHANTOM:_style_phantom_measures(6)
                                            \once \override MultiMeasureRest.transparent = ##t           %! PHANTOM:_style_phantom_measures(7)
                                            \stopStaff                                                   %! PHANTOM:_style_phantom_measures(8)
                                            \once \override Staff.StaffSymbol.transparent = ##t          %! PHANTOM:_style_phantom_measures(8)
                                            \startStaff                                                  %! PHANTOM:_style_phantom_measures(8)
                                            R1 * 1/4                                                     %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        }                                                                %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    >>                                                                   %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                }                                                                        %! baca.StringTrioScoreTemplate.__call__
                <BLANKLINE>
                            }                                                                            %! baca.StringTrioScoreTemplate.__call__
                <BLANKLINE>
                            \tag Cello                                                                   %! baca.ScoreTemplate._attach_liypond_tag
                            \context CelloMusicStaff = "Cello_Music_Staff"                               %! baca.StringTrioScoreTemplate.__call__
                            {                                                                            %! baca.StringTrioScoreTemplate.__call__
                <BLANKLINE>
                                \context CelloMusicVoice = "Cello_Music_Voice"                           %! baca.StringTrioScoreTemplate.__call__
                                {                                                                        %! baca.StringTrioScoreTemplate.__call__
                <BLANKLINE>
                                    \scaleDurations #'(1 . 1) {                                          %! baca.music
                <BLANKLINE>
                                        % [Cello_Music_Voice measure 1]                                  %! _comment_measure_numbers
                                        \clef "bass"                                                     %! DEFAULT_CLEF:_set_status_tag:abjad.ScoreTemplate.attach_defaults
                                        \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:_attach_color_literal(2)
                                    %@% \override CelloMusicStaff.Clef.color = ##f                       %! DEFAULT_CLEF_COLOR_CANCELLATION:_attach_color_literal(1)
                                        \set CelloMusicStaff.forceClef = ##t                             %! DEFAULT_CLEF:_set_status_tag:_treat_persistent_wrapper(2):abjad.ScoreTemplate.attach_defaults
                                        a16                                                              %! baca.music
                                        ^ \baca-default-indicator-markup "(Cello)"                       %! DEFAULT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                        \override CelloMusicStaff.Clef.color = #(x11-color 'violet)      %! DEFAULT_CLEF_REDRAW_COLOR:_attach_color_literal(2)
                <BLANKLINE>
                                        g16                                                              %! baca.music
                <BLANKLINE>
                                        \baca-octave-warning                                             %! _color_octaves_
                                        f16                                                              %! baca.music
                                        - \tweak color #red                                              %! _color_octaves_
                                        ^ \markup { OCTAVE }                                             %! _color_octaves_
                <BLANKLINE>
                                        e16                                                              %! baca.music
                <BLANKLINE>
                                        d16                                                              %! baca.music
                <BLANKLINE>
                                        c16                                                              %! baca.music
                <BLANKLINE>
                                    }                                                                    %! baca.music
                <BLANKLINE>
                                    <<                                                                   %! _make_multimeasure_rest_container
                <BLANKLINE>
                                        \context Voice = "Cello_Music_Voice"                             %! _make_multimeasure_rest_container
                                        {                                                                %! _make_multimeasure_rest_container
                <BLANKLINE>
                                            % [Cello_Music_Voice measure 2]                              %! _comment_measure_numbers
                                            \baca-invisible-music                                        %! _make_multimeasure_rest_container
                                            c'1 * 3/8                                                    %! _make_multimeasure_rest_container
                <BLANKLINE>
                                        }                                                                %! _make_multimeasure_rest_container
                <BLANKLINE>
                                        \context Voice = "Cello_Rest_Voice"                              %! _make_multimeasure_rest_container
                                        {                                                                %! _make_multimeasure_rest_container
                <BLANKLINE>
                                            % [Cello_Rest_Voice measure 2]                               %! _comment_measure_numbers
                                            R1 * 3/8                                                     %! _make_multimeasure_rest_container
                <BLANKLINE>
                                        }                                                                %! _make_multimeasure_rest_container
                <BLANKLINE>
                                    >>                                                                   %! _make_multimeasure_rest_container
                <BLANKLINE>
                                    <<                                                                   %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        \context Voice = "Cello_Music_Voice"                             %! PHANTOM:_make_multimeasure_rest_container
                                        {                                                                %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                            % [Cello_Music_Voice measure 3]                              %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                            \baca-invisible-music                                        %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                            R1 * 1/4                                                     %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        }                                                                %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        \context Voice = "Cello_Rest_Voice"                              %! PHANTOM:_make_multimeasure_rest_container
                                        {                                                                %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                            % [Cello_Rest_Voice measure 3]                               %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                            \once \override Score.TimeSignature.X-extent = ##f           %! PHANTOM:_style_phantom_measures(6)
                                            \once \override MultiMeasureRest.transparent = ##t           %! PHANTOM:_style_phantom_measures(7)
                                            \stopStaff                                                   %! PHANTOM:_style_phantom_measures(8)
                                            \once \override Staff.StaffSymbol.transparent = ##t          %! PHANTOM:_style_phantom_measures(8)
                                            \startStaff                                                  %! PHANTOM:_style_phantom_measures(8)
                                            R1 * 1/4                                                     %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        }                                                                %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    >>                                                                   %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                }                                                                        %! baca.StringTrioScoreTemplate.__call__
                <BLANKLINE>
                            }                                                                            %! baca.StringTrioScoreTemplate.__call__
                <BLANKLINE>
                        >>                                                                               %! baca.StringTrioScoreTemplate.__call__
                <BLANKLINE>
                    >>                                                                                   %! baca.StringTrioScoreTemplate.__call__
                <BLANKLINE>
                >>                                                                                       %! baca.StringTrioScoreTemplate.__call__

        """
        return self._color_octaves

    @property
    def commands(self) -> typing.List[scoping.Command]:
        """
        Gets commands.
        """
        return self._commands

    @property
    def deactivate(self) -> typing.Optional[typing.List[str]]:
        """
        Gets tags to deactivate in LilyPond output.
        """
        return self._deactivate

    @property
    def do_not_check_out_of_range_pitches(self) -> typing.Optional[bool]:
        """
        Is true when segment does not check out-of-range pitches.
        """
        return self._do_not_check_out_of_range_pitches

    @property
    def do_not_check_persistence(self) -> typing.Optional[bool]:
        """
        Is true when segment-maker does not check persistent indicators.
        """
        return self._do_not_check_persistence

    @property
    def do_not_check_wellformedness(self) -> typing.Optional[bool]:
        """
        Is true when segment does not check wellformedness.
        """
        return self._do_not_check_wellformedness

    @property
    def do_not_color_out_of_range_pitches(self) -> typing.Optional[bool]:
        r"""
        Is true when segment-maker does not color out-of-range pitches.

        ..  container:: example

            Colors out-of-range pitches:

            >>> figure = baca.figure([1], 16)
            >>> collection_lists = [
            ...     [[4]],
            ...     [[-12, 2, 3, 5, 8, 9, 0]],
            ...     [[11]],
            ...     [[10, 7, 9, 10, 0, 5]],
            ...     ]
            >>> figures, time_signatures = [], []
            >>> for i, collections in enumerate(collection_lists):
            ...     selection = figure(collections)
            ...     figures.append(selection)
            ...     time_signature = abjad.inspect(selection).duration()
            ...     time_signatures.append(time_signature)
            ...
            >>> figures_ = []
            >>> for figure in figures:
            ...     figures_.extend(figure)
            ...
            >>> figures = abjad.select(figures_)

            >>> maker = baca.SegmentMaker(
            ...     do_not_check_out_of_range_pitches=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=time_signatures,
            ...     )
            >>> maker(
            ...     ('Music_Voice', 1),
            ...     baca.instrument(abjad.Violin()),
            ...     baca.music(figures, do_not_check_total_duration=True),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.setting(lilypond_file['Score']).auto_beaming = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                <BLANKLINE>
                \context Score = "Score"                                                                 %! baca.SingleStaffScoreTemplate.__call__
                \with                                                                                    %! baca.SingleStaffScoreTemplate.__call__
                {                                                                                        %! baca.SingleStaffScoreTemplate.__call__
                    autoBeaming = ##f                                                                    %! baca.SingleStaffScoreTemplate.__call__
                }                                                                                        %! baca.SingleStaffScoreTemplate.__call__
                <<                                                                                       %! baca.SingleStaffScoreTemplate.__call__
                <BLANKLINE>
                    \context GlobalContext = "Global_Context"                                            %! abjad.ScoreTemplate._make_global_context
                    <<                                                                                   %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                        \context GlobalSkips = "Global_Skips"                                            %! abjad.ScoreTemplate._make_global_context
                        {                                                                                %! abjad.ScoreTemplate._make_global_context
                <BLANKLINE>
                            % [Global_Skips measure 1]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 1/16                                                                   %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/16                                                                    %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 7/16                                                                   %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 7/16                                                                    %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 1/16                                                                   %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/16                                                                    %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
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
                                \scaleDurations #'(1 . 1) {                                              %! baca.music
                <BLANKLINE>
                                    % [Music_Voice measure 1]                                            %! _comment_measure_numbers
                                    e'16                                                                 %! baca.music
                                    ^ \baca-explicit-indicator-markup "(Violin)"                         %! EXPLICIT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                <BLANKLINE>
                                }                                                                        %! baca.music
                <BLANKLINE>
                                \scaleDurations #'(1 . 1) {                                              %! baca.music
                <BLANKLINE>
                                    % [Music_Voice measure 2]                                            %! _comment_measure_numbers
                                    \baca-out-of-range-warning                                           %! _check_range
                                    c16                                                                  %! baca.music
                <BLANKLINE>
                                    d'16                                                                 %! baca.music
                <BLANKLINE>
                                    ef'!16                                                               %! baca.music
                <BLANKLINE>
                                    f'16                                                                 %! baca.music
                <BLANKLINE>
                                    af'!16                                                               %! baca.music
                <BLANKLINE>
                                    a'16                                                                 %! baca.music
                <BLANKLINE>
                                    c'16                                                                 %! baca.music
                <BLANKLINE>
                                }                                                                        %! baca.music
                <BLANKLINE>
                                \scaleDurations #'(1 . 1) {                                              %! baca.music
                <BLANKLINE>
                                    % [Music_Voice measure 3]                                            %! _comment_measure_numbers
                                    b'16                                                                 %! baca.music
                <BLANKLINE>
                                }                                                                        %! baca.music
                <BLANKLINE>
                                \scaleDurations #'(1 . 1) {                                              %! baca.music
                <BLANKLINE>
                                    % [Music_Voice measure 4]                                            %! _comment_measure_numbers
                                    bf'!16                                                               %! baca.music
                <BLANKLINE>
                                    g'16                                                                 %! baca.music
                <BLANKLINE>
                                    a'16                                                                 %! baca.music
                <BLANKLINE>
                                    bf'!16                                                               %! baca.music
                <BLANKLINE>
                                    c'16                                                                 %! baca.music
                <BLANKLINE>
                                    f'16                                                                 %! baca.music
                <BLANKLINE>
                                }                                                                        %! baca.music
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
        return self._do_not_color_out_of_range_pitches

    @property
    def do_not_color_repeat_pitch_classes(self) -> typing.Optional[bool]:
        r"""
        Is true when segment-maker does not color repeat pitch-classes.

        ..  container:: example

            Colors repeat pitch-classes:

            >>> figure = baca.figure([1], 16)
            >>> collection_lists = [
            ...     [[4]],
            ...     [[6, 2, 3, 5, 9, 9, 0]],
            ...     [[11]],
            ...     [[10, 7, 9, 12, 0, 5]],
            ...     ]
            >>> figures, time_signatures = [], []
            >>> for i, collections in enumerate(collection_lists):
            ...     selection = figure(collections)
            ...     figures.append(selection)
            ...     time_signature = abjad.inspect(selection).duration()
            ...     time_signatures.append(time_signature)
            ...
            >>> figures_ = []
            >>> for figure in figures:
            ...     figures_.extend(figure)
            ...
            >>> figures = abjad.select(figures_)

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 24)),
            ...     time_signatures=time_signatures,
            ...     )
            >>> maker(
            ...     ('Music_Voice', 1),
            ...     baca.music(figures, do_not_check_total_duration=True),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

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
                            \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 1/16                                                                   %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/16                                                                    %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 7/16                                                                   %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 7/16                                                                    %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
                            \time 1/16                                                                   %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/16                                                                    %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \baca-new-spacing-section #1 #24                                             %! HorizontalSpacingSpecifier(1):SPACING_COMMAND
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
                                \scaleDurations #'(1 . 1) {                                              %! baca.music
                <BLANKLINE>
                                    % [Music_Voice measure 1]                                            %! _comment_measure_numbers
                                    e'16                                                                 %! baca.music
                <BLANKLINE>
                                }                                                                        %! baca.music
                <BLANKLINE>
                                \scaleDurations #'(1 . 1) {                                              %! baca.music
                <BLANKLINE>
                                    % [Music_Voice measure 2]                                            %! _comment_measure_numbers
                                    fs'!16                                                               %! baca.music
                <BLANKLINE>
                                    d'16                                                                 %! baca.music
                <BLANKLINE>
                                    ef'!16                                                               %! baca.music
                <BLANKLINE>
                                    f'16                                                                 %! baca.music
                <BLANKLINE>
                                    \baca-repeat-pitch-class-warning                                     %! _color_repeat_pitch_classes_
                                    a'16                                                                 %! baca.music
                <BLANKLINE>
                                    \baca-repeat-pitch-class-warning                                     %! _color_repeat_pitch_classes_
                                    a'16                                                                 %! baca.music
                <BLANKLINE>
                                    c'16                                                                 %! baca.music
                <BLANKLINE>
                                }                                                                        %! baca.music
                <BLANKLINE>
                                \scaleDurations #'(1 . 1) {                                              %! baca.music
                <BLANKLINE>
                                    % [Music_Voice measure 3]                                            %! _comment_measure_numbers
                                    b'16                                                                 %! baca.music
                <BLANKLINE>
                                }                                                                        %! baca.music
                <BLANKLINE>
                                \scaleDurations #'(1 . 1) {                                              %! baca.music
                <BLANKLINE>
                                    % [Music_Voice measure 4]                                            %! _comment_measure_numbers
                                    bf'!16                                                               %! baca.music
                <BLANKLINE>
                                    g'16                                                                 %! baca.music
                <BLANKLINE>
                                    a'16                                                                 %! baca.music
                <BLANKLINE>
                                    \baca-repeat-pitch-class-warning                                     %! _color_repeat_pitch_classes_
                                    c''16                                                                %! baca.music
                <BLANKLINE>
                                    \baca-repeat-pitch-class-warning                                     %! _color_repeat_pitch_classes_
                                    c'16                                                                 %! baca.music
                <BLANKLINE>
                                    f'16                                                                 %! baca.music
                <BLANKLINE>
                                }                                                                        %! baca.music
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
        return self._do_not_color_repeat_pitch_classes

    @property
    def do_not_color_unpitched_music(self) -> typing.Optional[bool]:
        r"""
        Is true when segment ignores unpitched notes.

        ..  container:: example

            Ignores unpitched notes:

            >>> maker = baca.SegmentMaker(
            ...     do_not_color_unpitched_music=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.make_even_divisions(),
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
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
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

        ..  container:: example

            Colors unpitched notes:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.make_even_divisions(),
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
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                \baca-unpitched-music-warning                                            %! _color_unpitched_notes
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
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
        return self._do_not_color_unpitched_music

    @property
    def do_not_color_unregistered_pitches(self) -> typing.Optional[bool]:
        r"""
        Is true when segment ignores unregistered pitches.
        """
        return self._do_not_color_unregistered_pitches

    @property
    def do_not_force_nonnatural_accidentals(self) -> typing.Optional[bool]:
        """
        Is true when segment-maker does not force nonnatural accidentals.
        """
        return self._do_not_force_nonnatural_accidentals

    @property
    def do_not_include_layout_ly(self) -> typing.Optional[bool]:
        """
        Is true when segment-maker does not include layout.ly.
        """
        return self._do_not_include_layout_ly

    @property
    def fermata_measure_empty_overrides(
        self
    ) -> typing.Optional[typing.Sequence[int]]:
        """
        Gets fermata measure empty overrides.
        """
        return self._fermata_measure_empty_overrides

    @property
    def fermata_measure_staff_line_count(self) -> typing.Optional[int]:
        """
        Gets fermata measure staff lines.
        """
        return self._fermata_measure_staff_line_count

    @property
    def final_bar_line(self) -> typing.Union[bool, str, None]:
        r"""
        Gets final bar line.

        ..  container:: example

            Nonlast segment sets final bar line to ``'|'`` by default:

            >>> maker = baca.SegmentMaker(
            ...     do_not_color_unpitched_music=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.make_even_divisions(),
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
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
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

            Override nonlast segment final bar line like this:

            >>> maker = baca.SegmentMaker(
            ...     do_not_color_unpitched_music=True,
            ...     final_bar_line='||',
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.make_even_divisions(),
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
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "||"                                                                    %! _attach_final_bar_line
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
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

        ..  container:: example

            Last segment in score sets final bar line to ``'|.'`` by default:

            >>> maker = baca.SegmentMaker(
            ...     do_not_color_unpitched_music=True,
            ...     final_segment=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.make_even_divisions(),
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
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|."                                                                    %! _attach_final_bar_line
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
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

            Override last segment final bar line like this:

            >>> maker = baca.SegmentMaker(
            ...     do_not_color_unpitched_music=True,
            ...     final_bar_line='||',
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.make_even_divisions(),
            ...     )

            >>> metadata = {'segment_count': 1}
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     metadata=metadata,
            ...     )
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
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "||"                                                                    %! _attach_final_bar_line
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
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
        return self._final_bar_line

    @property
    def final_markup(self) -> typing.Optional[tuple]:
        r"""
        Gets final markup.

        ..  container:: example

            Sets final markup:

            >>> maker = baca.SegmentMaker(
            ...     do_not_color_unpitched_music=True,
            ...     final_bar_line='|.',
            ...     final_markup=(['Madison, WI'], ['October 2016']),
            ...     final_markup_extra_offset=(-9, -2),
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.make_even_divisions(),
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
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|."                                                                    %! _attach_final_bar_line
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                c'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                c'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
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
                                        \once \override MultiMeasureRestText.extra-offset = #'(-9 . -2)
                                        \once \override Score.TimeSignature.X-extent = ##f               %! PHANTOM:_style_phantom_measures(6)
                                        \once \override MultiMeasureRest.transparent = ##t               %! PHANTOM:_style_phantom_measures(7)
                                        \stopStaff                                                       %! PHANTOM:_style_phantom_measures(8)
                                        \once \override Staff.StaffSymbol.transparent = ##t              %! PHANTOM:_style_phantom_measures(8)
                                        \startStaff                                                      %! PHANTOM:_style_phantom_measures(8)
                                        R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
                                        _ \markup {                                                      %! PHANTOM:_style_phantom_measures(5):SCORE_2
                                            \override                                                    %! PHANTOM:_style_phantom_measures(5):SCORE_2
                                                #'(font-name . "Palatino")                               %! PHANTOM:_style_phantom_measures(5):SCORE_2
                                                \with-color                                              %! PHANTOM:_style_phantom_measures(5):SCORE_2
                                                    #black                                               %! PHANTOM:_style_phantom_measures(5):SCORE_2
                                                    \right-column                                        %! PHANTOM:_style_phantom_measures(5):SCORE_2
                                                        {                                                %! PHANTOM:_style_phantom_measures(5):SCORE_2
                                                            \line                                        %! PHANTOM:_style_phantom_measures(5):SCORE_2
                                                                {                                        %! PHANTOM:_style_phantom_measures(5):SCORE_2
                                                                    "Madison, WI"                        %! PHANTOM:_style_phantom_measures(5):SCORE_2
                                                                }                                        %! PHANTOM:_style_phantom_measures(5):SCORE_2
                                                            \line                                        %! PHANTOM:_style_phantom_measures(5):SCORE_2
                                                                {                                        %! PHANTOM:_style_phantom_measures(5):SCORE_2
                                                                    "October 2016"                       %! PHANTOM:_style_phantom_measures(5):SCORE_2
                                                                }                                        %! PHANTOM:_style_phantom_measures(5):SCORE_2
                                                        }                                                %! PHANTOM:_style_phantom_measures(5):SCORE_2
                                            }                                                            %! PHANTOM:_style_phantom_measures(5):SCORE_2
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
        return self._final_markup

    @property
    def final_markup_extra_offset(self) -> typing.Optional[abjad.NumberPair]:
        """
        Gets final markup extra offset.
        """
        return self._final_markup_extra_offset

    @property
    def final_segment(self) -> typing.Optional[bool]:
        """
        Is true when composer declares segment to be last in score.
        """
        return self._final_segment

    @property
    def first_measure_number(self) -> typing.Optional[int]:
        """
        Gets user-defined first measure number.
        """
        return self._first_measure_number

    @property
    def first_segment(self) -> typing.Optional[bool]:
        """
        Is true when segment is first in score.
        """
        if self._first_segment is not None:
            return self._first_segment
        return self._get_segment_number() == 1

    @property
    def ignore_repeat_pitch_classes(self) -> typing.Optional[bool]:
        """
        Is true when segment ignores repeat pitch-classes.
        """
        return self._ignore_repeat_pitch_classes

    @property
    def includes(self) -> typing.Optional[typing.Sequence[str]]:
        """
        Gets includes.
        """
        return self._includes

    @property
    def instruments(self) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets instruments.
        """
        return self._instruments

    @property
    def lilypond_file(self) -> typing.Optional[abjad.LilyPondFile]:
        """
        Gets LilyPond file.
        """
        return self._lilypond_file

    @property
    def local_measure_number_extra_offset(
        self
    ) -> typing.Union[bool, typings.Pair, None]:
        """
        Gets local measure number extra offset.
        """
        return self._local_measure_number_extra_offset

    @property
    def magnify_staves(
        self
    ) -> typing.Union[
        abjad.Multiplier, typing.Tuple[abjad.Multiplier, str], None
    ]:
        """
        Gets staff magnification.
        """
        return self._magnify_staves

    @property
    def manifests(self) -> abjad.OrderedDict:
        """
        Gets manifests.
        """
        manifests = abjad.OrderedDict()
        manifests["abjad.Instrument"] = self.instruments
        manifests["abjad.MarginMarkup"] = self.margin_markups
        manifests["abjad.MetronomeMark"] = self.metronome_marks
        return manifests

    @property
    def margin_markups(self) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets margin markups.
        """
        return self._margin_markups

    @property
    def measure_count(self) -> int:
        """
        Gets measure count.
        """
        if self.time_signatures:
            return len(self.time_signatures)
        return 0

    @property
    def measure_number_extra_offset(
        self
    ) -> typing.Union[bool, typings.Pair, None]:
        """
        Gets measure number extra offset.
        """
        return self._measure_number_extra_offset

    @property
    def metadata(self) -> abjad.OrderedDict:
        r"""
        Gets segment metadata.

        ..  container:: example

            >>> metadata = abjad.OrderedDict()
            >>> persist = abjad.OrderedDict()
            >>> persist['persistent_indicators'] = abjad.OrderedDict()
            >>> persist['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='Music_Voice',
            ...         prototype='abjad.Clef',
            ...         value='alto',
            ...         )
            ...     ]
            >>> metadata['segment_number'] = 1
            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     previous_metadata=metadata,
            ...     previous_persist=persist,
            ...     )

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
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \bar ""                                                                      %! _make_global_skips(3):+SEGMENT:EMPTY_START_BAR
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                                R1 * 4/8                                                                 %! _call_rhythm_commands
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                R1 * 3/8                                                                 %! _call_rhythm_commands
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                R1 * 4/8                                                                 %! _call_rhythm_commands
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                R1 * 3/8                                                                 %! _call_rhythm_commands
                <BLANKLINE>
                                <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                    {                                                                    %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        % [Music_Voice measure 5]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                        \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                        R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
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

            >>> abjad.f(maker.metadata, strict=89)
            abjad.OrderedDict(
                [
                    ('final_measure_number', 4),
                    ('first_measure_number', 1),
                    ('segment_number', 2),
                    (
                        'time_signatures',
                        ['4/8', '3/8', '4/8', '3/8'],
                        ),
                    ]
                )

            >>> abjad.f(maker.persist, strict=89)
            abjad.OrderedDict(
                [
                    (
                        'alive_during_segment',
                        [
                            'Score',
                            'Global_Context',
                            'Global_Skips',
                            'Music_Context',
                            'Music_Staff',
                            'Music_Voice',
                            'Rest_Voice',
                            ],
                        ),
                    (
                        'persistent_indicators',
                        abjad.OrderedDict(
                            [
                                (
                                    'MusicStaff',
                                    [
                                        abjad.Momento(
                                            context='Music_Voice',
                                            prototype='abjad.Clef',
                                            value='alto',
                                            ),
                                        ],
                                    ),
                                (
                                    'Score',
                                    [
                                        abjad.Momento(
                                            context='Global_Skips',
                                            prototype='abjad.TimeSignature',
                                            value='3/8',
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                        ),
                    ]
                )

        """
        return self._metadata

    @property
    def metronome_marks(self) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets metronome marks.
        """
        return self._metronome_marks

    @property
    def midi(self) -> typing.Optional[bool]:
        """
        Is true when segment-maker outputs MIDI.
        """
        return self._midi

    @property
    def nonfirst_segment_lilypond_include(self) -> typing.Optional[bool]:
        """
        Is true when nonfirst segment lilypond include appears in output file.
        """
        return self._nonfirst_segment_lilypond_include

    @property
    def persist(self) -> abjad.OrderedDict:
        """
        Gets persist metadata.
        """
        return self._persist

    @property
    def previous_metadata(self) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets previous segment metadata.
        """
        return self._previous_metadata

    @property
    def previous_persist(self) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets previous segment persist.
        """
        return self._previous_persist

    @property
    def remove_phantom_measure(self) -> typing.Optional[bool]:
        """
        Is true when segment-maker removes phantom measure.
        """
        return self._remove_phantom_measure

    @property
    def score_template(self) -> typing.Optional[abjad.ScoreTemplate]:
        """
        Gets score template.

        ..  container:: example

            Gets score template:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     )

            >>> maker.score_template
            SingleStaffScoreTemplate()

        """
        return self._score_template

    @property
    def skips_instead_of_rests(self) -> typing.Optional[bool]:
        r"""
        Is true when segment fills empty measures with skips.

        ..  container:: example

            Fills empty measures with multimeasure rests:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
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
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                                R1 * 4/8                                                                 %! _call_rhythm_commands
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                R1 * 3/8                                                                 %! _call_rhythm_commands
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                R1 * 4/8                                                                 %! _call_rhythm_commands
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                R1 * 3/8                                                                 %! _call_rhythm_commands
                <BLANKLINE>
                                <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                    {                                                                    %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        % [Music_Voice measure 5]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                        \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                        R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
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

        ..  container:: example

            Fills empty measures with skips:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     skips_instead_of_rests=True,
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> lilypond_file = maker.run(environment='docs')

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
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                                s1 * 4/8                                                                 %! _call_rhythm_commands
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                s1 * 3/8                                                                 %! _call_rhythm_commands
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                s1 * 4/8                                                                 %! _call_rhythm_commands
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                s1 * 3/8                                                                 %! _call_rhythm_commands
                <BLANKLINE>
                                <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                    {                                                                    %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        % [Music_Voice measure 5]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                        \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                        R1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    }                                                                    %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    \context Voice = "Rest_Voice"                                        %! PHANTOM:_make_multimeasure_rest_container
                                    {                                                                    %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        % [Rest_Voice measure 5]                                         %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                        s1 * 1/4                                                         %! PHANTOM:_make_multimeasure_rest_container
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
        return self._skips_instead_of_rests

    @property
    def spacing(
        self
    ) -> typing.Optional[segmentclasses.HorizontalSpacingSpecifier]:
        """
        Gets spacing.
        """
        return self._spacing

    @property
    def spacing_extra_offset(self) -> typing.Union[bool, typings.Pair, None]:
        """
        Gets spacing extra offset.
        """
        return self._spacing_extra_offset

    @property
    def stage_markup(self) -> typing.Optional[typing.Sequence[typing.Tuple]]:
        """
        Gets stage markup.
        """
        return self._stage_markup

    @property
    def stage_number_extra_offset(
        self
    ) -> typing.Union[bool, typings.Pair, None]:
        """
        Gets stage number extra offset.
        """
        return self._stage_number_extra_offset

    @property
    def test_container_identifiers(self) -> typing.Optional[bool]:
        """
        Is true when segment-maker adds container identifiers in docs
        environment.
        """
        return self._test_container_identifiers

    @property
    def time_signatures(self) -> typing.List[abjad.TimeSignature]:
        """
        Gets time signatures.
        """
        return self._time_signatures

    @property
    def transpose_score(self) -> typing.Optional[bool]:
        r"""
        Is true when segment transposes score.

        ..  container:: example

            Transposes score:

            >>> instruments = abjad.OrderedDict()
            >>> instruments['clarinet'] = abjad.ClarinetInBFlat()
            >>> maker = baca.SegmentMaker(
            ...     instruments=instruments,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     transpose_score=True,
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.instrument(instruments['clarinet']),
            ...     baca.make_even_divisions(),
            ...     baca.pitches('E4 F4'),
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
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                                fs'!8                                                                    %! baca.make_even_divisions
                                ^ \baca-explicit-indicator-markup "(“clarinet”)"                         %! EXPLICIT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                g'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                fs'!8                                                                    %! baca.make_even_divisions
                <BLANKLINE>
                                g'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                fs'!8                                                                    %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                g'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                fs'!8                                                                    %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                g'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                fs'!8                                                                    %! baca.make_even_divisions
                <BLANKLINE>
                                g'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                fs'!8                                                                    %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                g'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                fs'!8                                                                    %! baca.make_even_divisions
                <BLANKLINE>
                                g'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                <<                                                                       %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                    \context Voice = "Music_Voice"                                       %! PHANTOM:_make_multimeasure_rest_container
                                    {                                                                    %! PHANTOM:_make_multimeasure_rest_container
                <BLANKLINE>
                                        % [Music_Voice measure 5]                                        %! PHANTOM:_style_phantom_measures(5):_comment_measure_numbers
                                        \baca-invisible-music                                            %! PHANTOM:_style_phantom_measures(5):_make_multimeasure_rest_container
                                        d'1 * 1/4                                                        %! PHANTOM:_make_multimeasure_rest_container
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

        ..  container:: example

            Does not transpose score:

            >>> instruments = abjad.OrderedDict()
            >>> instruments['clarinet'] = abjad.ClarinetInBFlat()
            >>> maker = baca.SegmentMaker(
            ...     instruments=instruments,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     transpose_score=False,
            ...     )

            >>> maker(
            ...     'Music_Voice',
            ...     baca.instrument(instruments['clarinet']),
            ...     baca.make_even_divisions(),
            ...     baca.pitches('E4 F4'),
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
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 2]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 3]                                                   %! _comment_measure_numbers
                            \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 1/2                                                                     %! _make_global_skips(1)
                <BLANKLINE>
                            % [Global_Skips measure 4]                                                   %! _comment_measure_numbers
                            \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:_set_status_tag:_make_global_skips(2)
                            \baca-time-signature-color #'blue                                            %! EXPLICIT_TIME_SIGNATURE_COLOR:_attach_color_literal(2)
                            s1 * 3/8                                                                     %! _make_global_skips(1)
                            \baca-bar-line-visible                                                       %! _attach_final_bar_line
                            \bar "|"                                                                     %! _attach_final_bar_line
                <BLANKLINE>
                            % [Global_Skips measure 5]                                                   %! PHANTOM:_style_phantom_measures(1):_comment_measure_numbers
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
                                e'8                                                                      %! baca.make_even_divisions
                                ^ \baca-explicit-indicator-markup "(“clarinet”)"                         %! EXPLICIT_INSTRUMENT_ALERT:_attach_latent_indicator_alert
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 2]                                                %! _comment_measure_numbers
                                e'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 3]                                                %! _comment_measure_numbers
                                f'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                % [Music_Voice measure 4]                                                %! _comment_measure_numbers
                                f'8                                                                      %! baca.make_even_divisions
                                [                                                                        %! baca.make_even_divisions
                <BLANKLINE>
                                e'8                                                                      %! baca.make_even_divisions
                <BLANKLINE>
                                f'8                                                                      %! baca.make_even_divisions
                                ]                                                                        %! baca.make_even_divisions
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
        return self._transpose_score

    @property
    def validate_measure_count(self) -> typing.Optional[int]:
        """
        Gets validate measure count.

        ..  container:: example exception

            Raises exception when measures found do not equal validate count:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     validate_measure_count=6,
            ...     )
            Traceback (most recent call last):
                ...
            Exception: found 4 measures (not 6).

        """
        return self._validate_measure_count

    @property
    def voice_metadata(self) -> abjad.OrderedDict:
        """
        Gets voice metadata.
        """
        return self._voice_metadata

    ### PUBLIC METHODS ###

    def run(
        self,
        activate: typing.List[str] = None,
        deactivate: typing.List[str] = None,
        do_not_print_timing: bool = None,
        environment: str = None,
        metadata: abjad.OrderedDict = None,
        midi: bool = None,
        persist: abjad.OrderedDict = None,
        previous_metadata: abjad.OrderedDict = None,
        previous_persist: abjad.OrderedDict = None,
        remove: typing.List[str] = None,
        segment_directory: abjad.Path = None,
    ) -> abjad.LilyPondFile:
        """
        Runs segment-maker.

        :param deactivate: tags to deactivate in LilyPond file output.

        :param environment: stylesheet path control parameter. Leave set to
            none to render segments in real score.
            Set to ``"docs"`` for API examples.
            Set to ``"external"`` to debug API examples in a separate file.
            Set to ``"layout"`` when making layout.ly file.

        :param metadata: metadata found in current segment directory.

        :param midi: set to true to generate MIDI output.

        :param previous_metadata: metadata found in previous segment directory.

        :param remove: tags to remove in LilyPond file output.

        :param segment_directory: path providing access to current segment
            directory.

        """
        self._environment = environment
        self._metadata: abjad.OrderedDict = abjad.OrderedDict(metadata)
        self._midi = midi
        self._persist = abjad.OrderedDict(persist)
        self._previous_metadata = abjad.OrderedDict(previous_metadata)
        self._previous_persist = abjad.OrderedDict(previous_persist)
        self._segment_directory = segment_directory
        self._import_manifests()
        with abjad.Timer() as timer:
            self._make_score()
            self._make_lilypond_file()
            self._make_global_skips()
            self._label_measure_numbers()
            self._label_stage_numbers()
        count = int(timer.elapsed_time)
        seconds = abjad.String("second").pluralize(count)
        if not do_not_print_timing and self.environment != "docs":
            print(f"  Score initialization {count} {seconds} ...")

        with abjad.Timer() as timer:
            with abjad.ForbidUpdate(component=self.score, update_on_exit=True):
                command_count = self._call_rhythm_commands()
        count = int(timer.elapsed_time)
        seconds = abjad.String("second").pluralize(count)
        commands = abjad.String("command").pluralize(command_count)
        if not do_not_print_timing and self.environment != "docs":
            message = f"  Rhythm commands {count} {seconds}"
            message += f" [for {command_count} {commands}] ..."
            print(message)

        with abjad.Timer() as timer:
            self._populate_offset_to_measure_number()
            self._extend_beams()
            self._annotate_sounds_during()
            self._attach_first_segment_score_template_defaults()
            self._reapply_persistent_indicators()
            self._attach_first_appearance_score_template_defaults()
            self._apply_spacing()
        count = int(timer.elapsed_time)
        seconds = abjad.String("second").pluralize(count)
        if not do_not_print_timing and self.environment != "docs":
            print(f"  After-rhythm methods {count} {seconds} ...")

        with abjad.Timer() as timer:
            with abjad.ForbidUpdate(component=self.score, update_on_exit=True):
                command_count = self._call_commands()
        count = int(timer.elapsed_time)
        seconds = abjad.String("second").pluralize(count)
        commands = abjad.String("command").pluralize(command_count)
        if not do_not_print_timing and self.environment != "docs":
            message = f"  Nonrhythm commands {count} {seconds}"
            message += f" [for {command_count} {commands}] ..."
            print(message)

        # TODO: optimize by consolidating score iteration:
        with abjad.Timer() as timer:
            with abjad.ForbidUpdate(component=self.score, update_on_exit=True):
                self._clone_segment_initial_short_instrument_name()
                self._remove_redundant_time_signatures()
                self._cache_fermata_measure_numbers()
                self._treat_untreated_persistent_wrappers()
                self._attach_metronome_marks()
                self._reanalyze_trending_dynamics()
                self._transpose_score_()
                self._attach_final_bar_line()
                self._add_final_markup()
                self._color_unregistered_pitches()
                self._color_unpitched_notes()
                self._check_wellformedness()
                self._check_doubled_dynamics()
                self._check_range()
                self._check_persistent_indicators()
                self._color_repeat_pitch_classes_()
                self._color_octaves_()
                self._force_nonnatural_accidentals()
                self._magnify_staves_()
                self._whitespace_leaves()
                self._comment_measure_numbers()
                self._apply_breaks()
                self._style_fermata_measures()
                self._shift_clefs_into_fermata_measures()
                self._deactivate_tags(deactivate)
                self._remove_tags(remove)
                self._add_container_identifiers()
                self._check_all_music_in_part_containers()
                self._check_duplicate_part_assignments()
                self._move_global_rests()

        count = int(timer.elapsed_time)
        seconds = abjad.String("second").pluralize(count)
        if self.environment == "layout" or (
            not do_not_print_timing and self.environment != "docs"
        ):
            print(f"  Postprocessing {count} {seconds} ...")

        with abjad.Timer() as timer:
            method = getattr(self.score, "_update_now")
            method(offsets_in_seconds=True)
        count = int(timer.elapsed_time)
        seconds = abjad.String("second").pluralize(count)
        if not do_not_print_timing and self.environment != "docs":
            print(f"  Offsets-in-seconds update {count} {seconds} ...")

        with abjad.Timer() as timer:
            self._label_clock_time()
            self._activate_tags(activate)
            self._collect_metadata()
            self._style_phantom_measures()
        count = int(timer.elapsed_time)
        seconds = abjad.String("second").pluralize(count)
        if not do_not_print_timing and self.environment != "docs":
            print(f"  Clocktime markup {count} {seconds} ...")

        assert isinstance(self.lilypond_file, abjad.LilyPondFile)
        return self.lilypond_file
