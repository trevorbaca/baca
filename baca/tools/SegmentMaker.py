import abjad
import baca
import os
import pathlib
import time
import traceback
from abjad import rhythmmakertools as rhythmos
from .BreakMeasureMap import BreakMeasureMap
from .CommandWrapper import CommandWrapper
from .HorizontalSpacingSpecifier import HorizontalSpacingSpecifier
from .MetronomeMarkMeasureMap import MetronomeMarkMeasureMap
from .ScoreTemplate import ScoreTemplate
from .Typing import Dict
from .Typing import List
from .Typing import Optional
from .Typing import Number
from .Typing import NumberPair
from .Typing import Set
from .Typing import Tuple
from .Typing import Union as U


class SegmentMaker(abjad.SegmentMaker):
    r'''Segment-maker.

    >>> from abjad import rhythmmakertools as rhythmos

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     ignore_unpitched_notes=True,
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.make_even_runs(),
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
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \override Score.BarLine.transparent = ##f                                    %! SM5
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
                            {
            <BLANKLINE>
                                % [MusicVoice measure 1]                                             %! SM4
                                c'8
                                [
            <BLANKLINE>
                                c'8
            <BLANKLINE>
                                c'8
            <BLANKLINE>
                                c'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 2]                                             %! SM4
                                c'8
                                [
            <BLANKLINE>
                                c'8
            <BLANKLINE>
                                c'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 3]                                             %! SM4
                                c'8
                                [
            <BLANKLINE>
                                c'8
            <BLANKLINE>
                                c'8
            <BLANKLINE>
                                c'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 4]                                             %! SM4
                                c'8
                                [
            <BLANKLINE>
                                c'8
            <BLANKLINE>
                                c'8
                                ]
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    '''

    ### CLASS ATTRIBUTES ###

    __documentation_section__ = '(2) Makers'

    __slots__ = (
        '_allow_empty_selections',
        '_breaks',
        '_cache',
        '_cached_time_signatures',
        '_color_octaves',
        '_color_out_of_range_pitches',
        '_color_repeat_pitch_classes',
        '_do_not_check_persistence',
        '_do_not_include_layout_ly',
        '_duration',
        '_environment',
        '_fermata_measure_numbers',
        '_fermata_measure_staff_line_count',
        '_fermata_start_offsets',
        '_fermata_stop_offsets',
        '_final_bar_line',
        '_final_markup',
        '_final_markup_extra_offset',
        '_first_measure_number',
        '_ignore_repeat_pitch_classes',
        '_ignore_unpitched_notes',
        '_ignore_unregistered_pitches',
        '_instruments',
        '_last_measure_is_fermata',
        '_last_segment',
        '_margin_markups',
        '_measures_per_stage',
        '_metronome_mark_measure_map',
        '_metronome_mark_spanner_right_broken',
        '_metronome_mark_stem_height',
        '_metronome_marks',
        '_midi',
        '_offset_to_measure_number',
        '_previously_alive_contexts',
        '_print_timings',
        '_range_checker',
        '_rehearsal_mark',
        '_score',
        '_score_template',
        '_segment_bol_measure_numbers',
        '_segment_directory',
        '_segment_duration',
        '_skip_wellformedness_checks',
        '_skips_instead_of_rests',
        '_sounds_during_segment',
        '_spacing',
        '_start_clock_time',
        '_stop_clock_time',
        '_time_signatures',
        '_transpose_score',
        '_validate_measure_count',
        '_validate_stage_count',
        '_voice_metadata',
        '_wrappers',
        )

    _absolute_string_trio_stylesheet_path = pathlib.Path(
        '/',
        'Users',
        'trevorbaca',
        'Scores',
        '_docs',
        'source',
        '_stylesheets',
        'string-trio-stylesheet.ily',
        )

    _absolute_two_voice_staff_stylesheet_path = pathlib.Path(
        '/',
        'Users',
        'trevorbaca',
        'Scores',
        '_docs',
        'source',
        '_stylesheets',
        'two-voice-staff-stylesheet.ily',
        )

    _prototype_to_manifest_name = {
        'abjad.Instrument': 'instruments',
        'abjad.MetronomeMark': 'metronome_marks',
        'abjad.MarginMarkup': 'margin_markups',
        }

    _publish_storage_format = True

    _status_to_color = {
        'default': 'DarkViolet',
        'explicit': 'blue',
        'reapplied': 'green4',
        'redundant': 'DeepPink1',
        }

    _status_to_redraw_color = {
        'default': 'violet',
        'explicit': 'DeepSkyBlue2',
        'reapplied': 'OliveDrab',
        'redundant': 'DeepPink4',
        }

    _relative_string_trio_stylesheet_path = pathlib.Path(
        '..',
        '..',
        '..',
        '..',
        'source',
        '_stylesheets',
        'string-trio-stylesheet.ily',
        )

    _relative_two_voice_staff_stylesheet_path = pathlib.Path(
        '..',
        '..',
        '..',
        '..',
        'source',
        '_stylesheets',
        'two-voice-staff-stylesheet.ily',
        )

    _score_package_stylesheet_path = pathlib.Path(
        '..', '..', 'stylesheets', 'stylesheet.ily',
        )

    _score_package_nonfirst_stylesheet_path = pathlib.Path(
        '..', '..', 'stylesheets', 'nonfirst-segment.ily',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        allow_empty_selections: bool = None,
        color_octaves: bool = None,
        color_out_of_range_pitches: bool = None,
        color_repeat_pitch_classes: bool = None,
        do_not_check_persistence: bool = None,
        do_not_include_layout_ly: bool = None,
        fermata_measure_staff_line_count: int = None,
        final_bar_line: U[bool, str, None] = None,
        final_markup: U[tuple, None] = None,
        final_markup_extra_offset: U[NumberPair, None] = None,
        first_measure_number: U[int, None] = None,
        ignore_repeat_pitch_classes: bool = None,
        ignore_unpitched_notes: bool = None,
        ignore_unregistered_pitches: bool = None,
        instruments: abjad.OrderedDict = None,
        last_segment: bool = None,
        breaks: BreakMeasureMap = None,
        margin_markups: abjad.OrderedDict = None,
        measures_per_stage: List[int] = None,
        metronome_mark_measure_map: MetronomeMarkMeasureMap = None,
        metronome_mark_spanner_right_broken: bool = None,
        metronome_mark_stem_height: Optional[Number] = 1.5,
        metronome_marks: abjad.OrderedDict = None,
        print_timings: bool = None,
        range_checker: abjad.PitchRange = None,
        rehearsal_mark: str = None,
        score_template: ScoreTemplate = None,
        skip_wellformedness_checks: bool = None,
        skips_instead_of_rests: bool = None,
        spacing: HorizontalSpacingSpecifier = None,
        time_signatures: List[tuple] = None,
        transpose_score: bool = None,
        validate_measure_count: int = None,
        validate_stage_count: int = None,
        ) -> None:
        super(SegmentMaker, self).__init__()
        self._allow_empty_selections: bool = allow_empty_selections
        self._color_octaves: bool = color_octaves
        self._color_out_of_range_pitches: bool = \
            color_out_of_range_pitches
        self._color_repeat_pitch_classes: bool = \
            color_repeat_pitch_classes
        self._cache = None
        self._cached_time_signatures: List[abjad.TimeSignature] = []
        self._do_not_check_persistence: bool = do_not_check_persistence
        self._do_not_include_layout_ly: bool = do_not_include_layout_ly
        self._duration: abjad.Duration = None
        self._fermata_measure_numbers: list = []
        self._fermata_measure_staff_line_count: int = \
            fermata_measure_staff_line_count
        self._fermata_start_offsets: List[abjad.Offset] = []
        self._fermata_stop_offsets: List[abjad.Offset] = []
        self._final_bar_line: U[bool, str, None] = final_bar_line
        self._final_markup: tuple = final_markup
        self._final_markup_extra_offset: NumberPair = \
            final_markup_extra_offset
        self._first_measure_number: int = first_measure_number
        self._ignore_repeat_pitch_classes: bool = \
            ignore_repeat_pitch_classes
        self._ignore_unpitched_notes: bool = ignore_unpitched_notes
        self._ignore_unregistered_pitches: bool = \
            ignore_unregistered_pitches
        self._instruments: abjad.OrderedDict = instruments
        self._last_measure_is_fermata = False
        self._last_segment: bool = last_segment
        self._breaks: BreakMeasureMap = breaks
        self._margin_markups: abjad.OrderedDict = margin_markups
        if measures_per_stage is True:
            measures_per_stage = len(time_signatures) * [1]
        self._measures_per_stage: List[int] = measures_per_stage
        self._metronome_mark_measure_map: MetronomeMarkMeasureMap = \
            metronome_mark_measure_map
        self._metronome_mark_spanner_right_broken: bool = \
            metronome_mark_spanner_right_broken
        self._metronome_mark_stem_height: Optional[Number] = \
            metronome_mark_stem_height
        self._metronome_marks: abjad.OrderedDict = metronome_marks
        self._midi: bool = None
        self._offset_to_measure_number: Dict[abjad.Offset, int] = {}
        self._previously_alive_contexts: List[str] = []
        self._print_timings: bool = print_timings
        self._range_checker: abjad.PitchRange = range_checker
        self._rehearsal_mark: str = rehearsal_mark
        self._score_template: ScoreTemplate = score_template
        self._segment_bol_measure_numbers: List[int] = []
        self._segment_duration: abjad.Duration = None
        self._skip_wellformedness_checks: bool = skip_wellformedness_checks
        self._skips_instead_of_rests: bool = skips_instead_of_rests
        self._spacing: HorizontalSpacingSpecifier = spacing
        self._sounds_during_segment: abjad.OrderedDict = abjad.OrderedDict()
        self._start_clock_time: str = None
        self._stop_clock_time: str = None
        self._transpose_score: bool = transpose_score
        self._validate_measure_count: int = validate_measure_count
        self._validate_stage_count: int = validate_stage_count
        self._voice_metadata: abjad.OrderedDict = abjad.OrderedDict()
        self._wrappers: List[CommandWrapper] = []
        self._initialize_time_signatures(time_signatures)
        self._validate_measure_count_()
        self._validate_measures_per_stage()

    ### SPECIAL METHODS ###

    def __call__(self, scopes, *commands):
        r'''Wraps each command in `commands` with each scope in `scopes`.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
            ...     baca.label(abjad.label().with_indices()),
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
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
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
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 1]                                             %! SM4
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    [
                                    ^ \markup {
                                        \small
                                            0
                                        }
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    ^ \markup {
                                        \small
                                            1
                                        }
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    ^ \markup {
                                        \small
                                            2
                                        }
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    ]
                                    ^ \markup {
                                        \small
                                            3
                                        }
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 2]                                             %! SM4
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    [
                                    ^ \markup {
                                        \small
                                            4
                                        }
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    ^ \markup {
                                        \small
                                            5
                                        }
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    ]
                                    ^ \markup {
                                        \small
                                            6
                                        }
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 3]                                             %! SM4
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    [
                                    ^ \markup {
                                        \small
                                            7
                                        }
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    ^ \markup {
                                        \small
                                            8
                                        }
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    ^ \markup {
                                        \small
                                            9
                                        }
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    ]
                                    ^ \markup {
                                        \small
                                            10
                                        }
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 4]                                             %! SM4
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    [
                                    ^ \markup {
                                        \small
                                            11
                                        }
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    ^ \markup {
                                        \small
                                            12
                                        }
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    ]
                                    ^ \markup {
                                        \small
                                            13
                                        }
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        Returns none.
        '''
        prototype = (baca.Scope, baca.TimelineScope)
        if isinstance(scopes, prototype):
            scopes = [scopes]
        else:
            assert all(isinstance(_, prototype) for _ in scopes), repr(scopes)
        for command in commands:
            if not isinstance(command, baca.Command):
                raise Exception(f'commands only:\n\n{format(command)}')
        for scope in scopes:
            for command in commands:
                wrapper = baca.CommandWrapper(command=command, scope=scope)
                self.wrappers.append(wrapper)

    ### PRIVATE METHODS ###

    def _add_final_bar_line(self):
        if self.final_bar_line is False:
            return
        strings = []
        abbreviation = '|'
        if self.last_segment:
            abbreviation = '|.'
        if isinstance(self.final_bar_line, str):
            abbreviation = self.final_bar_line
        strings.append(r'\override Score.BarLine.transparent = ##f')
        strings.append(rf'\bar "{abbreviation}"')
        literal = abjad.LilyPondLiteral(strings, 'after')
        last_skip = baca.select(self.score['GlobalSkips']).skip(-1)
        abjad.attach(literal, last_skip, tag='SM5')

    def _add_final_markup(self):
        if self.final_markup is None:
            return
        command = baca.markup.final_markup(*self.final_markup)
        self.score.add_final_markup(
            command.indicators[0],
            extra_offset=self.final_markup_extra_offset,
            )

    def _alive_during_any_previous_segment(self, context) -> bool:
        assert isinstance(context, abjad.Context), repr(context)
        # HERE
        names: List = self.previous_metadata.get('alive_during_segment', [])
        return context.name in names

    def _alive_during_previous_segment(self, context) -> bool:
        assert isinstance(context, abjad.Context), repr(context)
        names: List = self.previous_metadata.get('alive_during_segment', [])
        return context.name in names

    def _analyze_momento(self, context, momento):
        previous_indicator = self._momento_to_indicator(momento)
        if previous_indicator is None:
            return
        if isinstance(previous_indicator, baca.SpacingSection):
            return
        if momento.context in self.score:
            momento_context = self.score[momento.context]
        else:
            # context alive in previous segment doesn't exist in this segment
            return
        leaf = abjad.inspect(momento_context).get_leaf(0)
        if isinstance(previous_indicator, abjad.Instrument):
            prototype = abjad.Instrument
        else:
            prototype = type(previous_indicator)
        indicator = abjad.inspect(leaf).get_indicator(prototype)
        status = None
        if indicator is None:
            status = 'reapplied'
        elif previous_indicator == indicator:
            if isinstance(previous_indicator, abjad.TimeSignature):
                status = 'reapplied'
            elif isinstance(previous_indicator, abjad.Dynamic):
                if previous_indicator.sforzando:
                    status = 'explicit'
                else:
                    status = 'redundant'
            else:
                status = 'redundant'
        edition = momento.edition or abjad.Tag()
        return leaf, previous_indicator, status, edition

    def _annotate_sounds_during(self):
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            pleaves = baca.select(voice).pleaves()
            value = bool(pleaves)
            abjad.annotate(voice, abjad.tags.SOUNDS_DURING_SEGMENT, value)
            self._sounds_during_segment[voice.name] = value

    def _apply_breaks(self):
        if self.breaks is None:
            return
        self.breaks(self.score['GlobalSkips'])

    def _apply_first_and_last_ties(self, voice):
        dummy_tie = abjad.Tie()
        for current_leaf in abjad.iterate(voice).leaves():
            if not dummy_tie._attachment_test(current_leaf):
                continue
            if abjad.inspect(current_leaf).has_indicator(abjad.tags.TIE_TO):
                previous_leaf = abjad.inspect(current_leaf).get_leaf(-1)
                if dummy_tie._attachment_test(previous_leaf):
                    previous_logical_tie = abjad.inspect(
                        previous_leaf).get_logical_tie()
                    if current_leaf not in previous_logical_tie:
                        current_logical_tie = abjad.inspect(
                            current_leaf).get_logical_tie()
                        leaves = previous_logical_tie + current_logical_tie
                        abjad.detach(abjad.Tie, previous_leaf)
                        abjad.detach(abjad.Tie, current_leaf)
                        inspector = abjad.inspect(current_leaf)
                        string = abjad.tags.REPEAT_TIE 
                        repeat_ties = inspector.has_indicator(string)
                        tie = abjad.Tie(repeat=repeat_ties)
                        abjad.attach(tie, leaves, tag='SM16')
                abjad.detach(abjad.tags.TIE_TO, current_leaf)
            if abjad.inspect(current_leaf).has_indicator(abjad.tags.TIE_FROM):
                next_leaf = abjad.inspect(current_leaf).get_leaf(1)
                if dummy_tie._attachment_test(next_leaf):
                    current_logical_tie = abjad.inspect(
                        current_leaf).get_logical_tie()
                    if next_leaf not in current_logical_tie:
                        next_logical_tie = abjad.inspect(
                            next_leaf).get_logical_tie()
                        leaves = current_logical_tie + next_logical_tie
                        abjad.detach(abjad.Tie, current_leaf)
                        abjad.detach(abjad.Tie, next_leaf)
                        inspector = abjad.inspect(current_leaf)
                        string = abjad.tags.REPEAT_TIE
                        repeat_ties = inspector.has_indicator(string)
                        tie = abjad.Tie(repeat=repeat_ties)
                        abjad.attach(tie, leaves, tag='SM17')
                abjad.detach(abjad.tags.TIE_FROM, current_leaf)

    def _apply_spacing(self):
        start_time = time.time()
        if self.spacing is None:
            return
        self.spacing(self)
        stop_time = time.time()
        total_time = int(stop_time - start_time)
        if self.print_timings:
            print(f'spacing time {total_time} seconds ...')
        if os.getenv('TRAVIS'):
            return
        if 3 < total_time:
            raise Exception(f'spacing time {total_time} seconds!')

    def _assert_nonoverlapping_rhythms(self, rhythms, voice):
        previous_stop_offset = 0
        for rhythm in rhythms:
            start_offset = rhythm.start_offset
            if start_offset < previous_stop_offset:
                raise Exception(f'{voice!r} has overlapping rhythms.')
            duration = abjad.inspect(rhythm.annotation).get_duration()
            stop_offset = start_offset + duration
            previous_stop_offset = stop_offset

    def _assert_valid_stage_number(self, stage_number):
        if not 1 <= stage_number <= self.stage_count:
            message = f'must be 1 <= x <= {self.stage_count}: {stage_number}.'
            raise Exception(message)

    @staticmethod
    def _attach_color_cancelation_literal(
        wrapper,
        status,
        existing_deactivate=None,
        existing_tag=None,
        ):
        if getattr(wrapper.indicator, 'latent', False):
            return
        if getattr(wrapper.indicator, 'hide', False):
            return
        if not getattr(wrapper.indicator, 'redraw', False):
            return
        SegmentMaker._attach_color_literal(
            wrapper,
            status,
            existing_deactivate=wrapper.deactivate,
            existing_tag=existing_tag,
            cancelation=True,
            )

    @staticmethod
    def _attach_color_literal(
        wrapper,
        status,
        existing_deactivate=None,
        existing_tag=None,
        redraw=False,
        cancelation=False,
        ):
        assert isinstance(wrapper, abjad.Wrapper), repr(wrapper)
        if getattr(wrapper.indicator, 'hide', False) is True:
            return
        if not getattr(wrapper.indicator, 'persistent', False):
            return
        if wrapper.indicator.persistent == 'abjad.MetronomeMark':
            return
        if existing_tag is not None:
            assert isinstance(existing_tag, abjad.Tag), repr(existing_tag)
        stem = abjad.String.to_indicator_stem(wrapper.indicator)
        grob = SegmentMaker._indicator_to_grob(wrapper.indicator)
        context = wrapper._find_correct_effective_context()
        assert isinstance(context, abjad.Context), repr(context)
        string = rf'\override {context.lilypond_type}.{grob}.color ='
        if cancelation is True:
            string += ' ##f'
        elif redraw is True:
            color = SegmentMaker._status_to_redraw_color[status]
            string += f" #(x11-color '{color})"
        else:
            string = rf'\once {string}'
            color = SegmentMaker._status_to_color[status]
            string += f" #(x11-color '{color})"
        if redraw:
            literal = abjad.LilyPondLiteral(string, 'after')
        else:
            literal = abjad.LilyPondLiteral(string)
        if getattr(wrapper.indicator, 'latent', False):
            if redraw:
                prefix = 'redrawn'
            else:
                prefix = None
            if cancelation:
                suffix = 'color_cancellation'
            else:
                suffix = 'color'
        else:
            prefix = None
            if redraw:
                suffix = 'redraw_color'
            elif cancelation:
                suffix = 'color_cancellation'
            else:
                suffix = 'color'
        tag = SegmentMaker._get_tag(status, stem, prefix=prefix, suffix=suffix)
        if existing_tag:
            tag = existing_tag.prepend(tag)
        if cancelation is True:
            abjad.attach(
                literal,
                wrapper.component,
                deactivate=True,
                tag=tag.prepend('SM7'),
                )
        else:
            abjad.attach(
                literal,
                wrapper.component,
                deactivate=existing_deactivate,
                tag=tag.prepend('SM6'),
                )

    @staticmethod
    def _attach_color_redraw_literal(
        wrapper,
        status,
        existing_deactivate=None,
        existing_tag=None,
        ):
        if not getattr(wrapper.indicator, 'redraw', False):
            return
        if getattr(wrapper.indicator, 'hide', False):
            return
        SegmentMaker._attach_color_literal(
            wrapper,
            status,
            existing_deactivate=wrapper.deactivate,
            existing_tag=existing_tag,
            redraw=True,
            )

    def _attach_fermatas(self):
        always_make_global_rests = getattr(
            self.score_template,
            'always_make_global_rests',
            False,
            )
        if (not self.metronome_mark_measure_map and
            not always_make_global_rests):
            del(self.score['GlobalRests'])
            return
        has_fermata = False
        if self.metronome_mark_measure_map:
            for entry in self.metronome_mark_measure_map:
                if isinstance(entry[1], abjad.Fermata):
                    has_fermata = True
        if not has_fermata and not always_make_global_rests:
            del(self.score['GlobalRests'])
            return
        context = self.score['GlobalRests']
        rests = self._make_multimeasure_rests()
        context.extend(rests)
        if not self.metronome_mark_measure_map:
            return
        directive_prototype = (
            abjad.BreathMark,
            abjad.Fermata,
            )
        last_measure_index = len(rests) - 1
        first_measure_number = self._get_first_measure_number()
        for stage_number, directive in self.metronome_mark_measure_map:
            if not isinstance(directive, directive_prototype):
                continue
            assert 0 < stage_number <= self.stage_count
            result = self._stage_number_to_measure_indices(stage_number)
            start_measure_index, stop_measure_index = result
            measure_number = first_measure_number + start_measure_index
            rest = context[start_measure_index]
            assert isinstance(rest, abjad.MultimeasureRest)
            if start_measure_index == last_measure_index:
                self._last_measure_is_fermata = True
            if isinstance(directive, abjad.Fermata):
                if directive.command == 'shortfermata':
                    string = 'scripts.ushortfermata'
                elif directive.command == 'fermata':
                    string = 'scripts.ufermata'
                elif directive.command == 'longfermata':
                    string = 'scripts.ulongfermata'
                elif directive.command == 'verylongfermata':
                    string = 'scripts.uverylongfermata'
                else:
                    raise Exception(f'unknown fermata: {directive.command!r}.')
                directive = abjad.Markup.musicglyph(string)
                directive = abjad.new(directive, direction=abjad.Up)
            else:
                directive = abjad.new(directive)
            abjad.attach(directive, rest, tag='SM18')
            strings = []
            string = r'\once \override'
            string += ' Score.MultiMeasureRest.transparent = ##t'
            strings.append(string)
            string = r'\once \override Score.TimeSignature.stencil = ##f'
            strings.append(string)
            literal = abjad.LilyPondLiteral(strings)
            abjad.attach(literal, rest, tag='SM19')
            abjad.attach(
                abjad.tags.FERMATA_MEASURE,
                rest,
                tag=abjad.tags.FERMATA_MEASURE,
                )
            timespan = abjad.inspect(rest).get_timespan()
            self._fermata_start_offsets.append(timespan.start_offset)
            self._fermata_stop_offsets.append(timespan.stop_offset)
            self._fermata_measure_numbers.append(measure_number)

    def _attach_first_appearance_score_template_defaults(self):
        if self.first_segment:
            return
        staff_or_group = (abjad.Staff, abjad.StaffGroup)
        dictionary = self.previous_metadata['persistent_indicators']
        for staff in abjad.iterate(self.score).components(staff_or_group):
            if staff.name in dictionary:
                continue
            for wrapper in self.score_template.attach_defaults(staff):
                tag = wrapper.tag.extend(['-PARTS', '-SCORE'])
                wrapper.tag = tag
                self._categorize_persistent_wrapper(
                    self.manifests,
                    wrapper,
                    'default',
                    )

    def _attach_first_segment_score_template_defaults(self):
        if not self.first_segment:
            return
        for wrapper in self.score_template.attach_defaults(self.score):
            self._categorize_persistent_wrapper(
                self.manifests,
                wrapper,
                'default',
                )

    @staticmethod
    def _attach_latent_indicator_alert(
        manifests,
        wrapper,
        status,
        existing_deactivate=None,
        existing_tag=None,
        ):
        if not getattr(wrapper.indicator, 'latent', False):
            return
        if existing_tag is not None:
            assert isinstance(existing_tag, abjad.Tag), repr(existing_tag)
        leaf = wrapper.component
        indicator = wrapper.indicator
        assert indicator.latent, repr(indicator)
        if isinstance(indicator, abjad.Clef):
            return
        key = SegmentMaker._indicator_to_key(indicator, manifests)
        if key is not None:
            key = f'“{key}”'
        else:
            key = type(indicator).__name__
        if isinstance(indicator, abjad.Instrument):
            if status == 'default':
                tag = abjad.tags.DEFAULT_INSTRUMENT_ALERT
            elif status == 'explicit':
                tag = abjad.tags.EXPLICIT_INSTRUMENT_ALERT
            elif status == 'reapplied':
                tag = abjad.tags.REAPPLIED_INSTRUMENT_ALERT
            else:
                assert status == 'redundant', repr(status)
                tag = abjad.tags.REDUNDANT_INSTRUMENT_ALERT
            left, right = '(', ')'
        else:
            assert isinstance(indicator, abjad.MarginMarkup)
            if status == 'default':
                tag = abjad.tags.DEFAULT_MARGIN_MARKUP_ALERT
            elif status == 'explicit':
                tag = abjad.tags.EXPLICIT_MARGIN_MARKUP_ALERT
            elif status == 'reapplied':
                tag = abjad.tags.REAPPLIED_MARGIN_MARKUP_ALERT
            else:
                assert status == 'redundant', repr(status)
                tag = abjad.tags.REDUNDANT_MARGIN_MARKUP_ALERT
            left, right = '[', ']'
        tag = abjad.Tag(tag)
        markup = abjad.Markup.from_literal(f'{left}{key}{right}')
        markup = abjad.new(markup, direction=abjad.Up)
        color = SegmentMaker._status_to_color[status]
        color = abjad.SchemeColor(color)
        markup = markup.with_color(color)
        if existing_tag:
            tag = existing_tag.prepend(tag)
        abjad.attach(
            markup,
            leaf,
            deactivate=existing_deactivate,
            tag=tag.prepend('SM11'),
            )

    def _attach_metronome_marks(self):
        skips = baca.select(self.score['GlobalSkips']).skips()
        left_broken_text = abjad.Markup().null()
        left_broken_text = abjad.new(left_broken_text, direction=None)
        spanner = abjad.MetronomeMarkSpanner(
            left_broken_padding=0,
            left_broken_text=left_broken_text,
            parenthesize=False,
            right_padding=0,
            stem_height=self.metronome_mark_stem_height,
            )
        tag = abjad.Tag(abjad.tags.METRONOME_MARK_SPANNER)
        string = 'metronome_mark_spanner_right_broken'
        left_broken = self.previous_metadata.get(string)
        abjad.attach(
            spanner,
            skips,
            left_broken=left_broken,
            right_broken=self.metronome_mark_spanner_right_broken,
            tag=tag.prepend('SM29'),
            )
        if left_broken:
            literal = abjad.LilyPondLiteral(
                r'\stopTextSpan',
                format_slot='closing',
                )
            abjad.attach(
                literal,
                skips[0],
                tag=abjad.Tag('-SEGMENT').prepend('SM39'),
                )
        if not self.metronome_mark_measure_map:
            return
        for stage_number, directive in self.metronome_mark_measure_map:
            self._assert_valid_stage_number(stage_number)
            start, _ = self._stage_number_to_measure_indices(stage_number)
            skip = skips[start]
            spanner.attach(directive, skip, tag='SM30')

    def _attach_rehearsal_mark(self):
        if not self.rehearsal_mark:
            return
        rehearsal_mark = abjad.RehearsalMark.from_string(self.rehearsal_mark)
        skip = baca.select(self.score['GlobalSkips']).skip(0)
        abjad.attach(rehearsal_mark, skip, tag='SM9')

    def _born_this_segment(self, component):
        prototype = (abjad.Staff, abjad.StaffGroup)
        assert isinstance(component, prototype), repr(component)
        return not self._alive_during_previous_segment(component)

    def _cache_leaves(self):
        stage_timespans = []
        for stage_index in range(self.stage_count):
            stage_number = stage_index + 1
            stage_offsets = self._get_stage_offsets(stage_number, stage_number)
            stage_timespan = abjad.Timespan(*stage_offsets)
            stage_timespans.append(stage_timespan)
        self._cache = abjad.OrderedDict()
        contexts = [self.score['GlobalSkips']]
        contexts.extend(abjad.select(self.score).components(abjad.Voice))
        for context in contexts:
            leaves_by_stage_number = abjad.OrderedDict()
            self._cache[context.name] = leaves_by_stage_number
            for stage_index in range(self.stage_count):
                stage_number = stage_index + 1
                leaves_by_stage_number[stage_number] = []
            for leaf in abjad.iterate(context).leaves():
                leaf_timespan = abjad.inspect(leaf).get_timespan()
                for stage_index, stage_timespan in enumerate(stage_timespans):
                    stage_number = stage_index + 1
                    if leaf_timespan.starts_during_timespan(stage_timespan):
                        leaves_by_stage_number[stage_number].append(leaf)


    def _cache_previously_alive_contexts(self) -> None:
        if self.segment_directory is None:
            return
        contexts: Set[str] = set()
        string = 'alive_during_segment'
        for segment in self.segment_directory.parent.list_paths():
            if segment == self.segment_directory:
                break
            contexts_ = segment.get_metadatum(string)
            contexts.update(contexts_)
        self._previously_alive_contexts.extend(sorted(contexts))

    def _call_commands(self):
        start_time = time.time()
        for wrapper in self.wrappers:
            assert isinstance(wrapper, baca.CommandWrapper)
            assert isinstance(wrapper.command, baca.Command)
            if isinstance(wrapper.command, baca.RhythmCommand):
                continue
            selection = self._scope_to_leaf_selection(wrapper)
            wrapper.command.manifests = self.manifests
            dictionary = self._offset_to_measure_number
            wrapper.command.offset_to_measure_number = dictionary
            try:
                wrapper.command(selection)
            except:
                traceback.print_exc()
                raise Exception(f'can not interpret ...\n\n{format(wrapper)}')
            self._handle_mutator(wrapper)
        stop_time = time.time()
        count = int(stop_time - start_time)
        counter = abjad.String('second').pluralize(count)
        if self.print_timings:
            print(f'command interpretation {count} {counter} ...')

    def _call_rhythm_commands(self):
        self._attach_metronome_marks()
        self._attach_fermatas()
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            assert not len(voice), repr(voice)
            voice_metadata = self._voice_metadata.get(voice.name)
            voice_metadata = voice_metadata or abjad.OrderedDict()
            wrappers = self._voice_to_rhythm_wrappers(voice)
            if not wrappers:
                if self.skips_instead_of_rests:
                    maker = rhythmos.SkipRhythmMaker()
                else:
                    mask = abjad.silence([0], 1, use_multimeasure_rests=True)
                    maker = rhythmos.NoteRhythmMaker(division_masks=[mask])
                selections = maker(self.time_signatures)
                voice.extend(selections)
                continue
            rhythms = []
            for wrapper in wrappers:
                assert isinstance(wrapper, baca.CommandWrapper)
                if wrapper.scope.stages is None:
                    raise Exception(format(wrapper))
                command = wrapper.command
                previous_voice_metadata = self._get_previous_voice_metadata(
                    voice,
                    command.voice_metadata_pairs,
                    )
                result = self._get_stage_time_signatures(*wrapper.scope.stages)
                start_offset, time_signatures = result
                command._previous_voice_metadata = previous_voice_metadata
                try:
                    rhythm = command(start_offset, time_signatures)
                except:
                    raise Exception(f'\n\n{format(wrapper)}')
                rhythms.append(rhythm)
                command_voice_metadata = command.voice_metadata
                if bool(command_voice_metadata):
                    for key, value in command_voice_metadata.items():
                        voice_metadata[key] = value
            if bool(voice_metadata):
                self._voice_metadata[voice.name] = voice_metadata
            rhythms.sort()
            self._assert_nonoverlapping_rhythms(rhythms, voice.name)
            rhythms = self._intercalate_silences(rhythms)
            voice.extend(rhythms)
            self._apply_first_and_last_ties(voice)

    @staticmethod
    def _categorize_persistent_wrapper(
        manifests,
        wrapper,
        status,
        ):
        assert isinstance(wrapper, abjad.Wrapper), repr(wrapper)
        assert bool(wrapper.indicator.persistent), repr(wrapper)
        assert isinstance(status, str), repr(status)
        context = wrapper._find_correct_effective_context()
        assert isinstance(context, abjad.Context), repr(wrapper)
        leaf = wrapper.component
        assert isinstance(leaf, abjad.Leaf), repr(wrapper)
        indicator = wrapper.indicator
        existing_tag = wrapper.tag
        if wrapper.spanner:
            prototype = (abjad.Accelerando, abjad.Ritardando)
            if (status == 'reapplied' and
                isinstance(wrapper.indicator, prototype)):
                pass
            elif wrapper.spanner._is_trending(wrapper.component):
                status = 'explicit'
        SegmentMaker._attach_color_literal(
            wrapper,
            status,
            existing_deactivate=wrapper.deactivate,
            existing_tag=existing_tag,
            )
        SegmentMaker._attach_latent_indicator_alert(
            manifests,
            wrapper,
            status,
            existing_deactivate=wrapper.deactivate,
            existing_tag=existing_tag,
            )
        SegmentMaker._attach_color_cancelation_literal(
            wrapper,
            status,
            existing_deactivate=wrapper.deactivate,
            existing_tag=existing_tag,
            )
        if isinstance(wrapper.indicator, abjad.Clef):
            string = rf'\set {context.lilypond_type}.forceClef = ##t'
            literal = abjad.LilyPondLiteral(string)
            wrapper_ = abjad.attach(
                literal,
                wrapper.component,
                tag=wrapper.tag.prepend('SM33'),
                wrapper=True,
                )
            SegmentMaker._set_status_tag(
                wrapper_,
                status,
                stem='CLEF',
                )
        SegmentMaker._set_status_tag(
            wrapper,
            status,
            )
        SegmentMaker._attach_color_redraw_literal(
            wrapper,
            status,
            existing_deactivate=wrapper.deactivate,
            existing_tag=existing_tag,
            )
        if (isinstance(indicator, (abjad.Instrument, abjad.MarginMarkup)) and
            not getattr(indicator, 'hide', False)):
            strings = indicator._get_lilypond_format(context=context)
            literal = abjad.LilyPondLiteral(strings, 'after')
            stem = abjad.String.to_indicator_stem(indicator)
            wrapper_ = abjad.attach(
                literal,
                leaf,
                tag=existing_tag.prepend('SM34'),
                wrapper=True,
                )
            SegmentMaker._set_status_tag(
                wrapper_,
                status,
                redraw=True,
                stem=stem,
                )

    def _categorize_uncategorized_persistent_wrappers(self):
        for leaf in abjad.iterate(self.score).leaves():
            for wrapper in abjad.inspect(leaf).wrappers():
                if not getattr(wrapper.indicator, 'persistent', False):
                    continue
                if wrapper.tag and wrapper.tag.has_persistence_tag():
                    continue
                if isinstance(wrapper.indicator, abjad.Instrument):
                    prototype = abjad.Instrument
                else:
                    prototype = type(wrapper.indicator)
                previous_indicator = abjad.inspect(leaf).get_effective(
                    prototype,
                    n=-1,
                    )
                if previous_indicator != wrapper.indicator:
                    status = 'explicit'
                elif (isinstance(previous_indicator, abjad.Dynamic) and
                    previous_indicator.sforzando):
                    status = 'explicit'
                else:
                    status = 'redundant'
                self._categorize_persistent_wrapper(
                    self.manifests,
                    wrapper,
                    status,
                    )

    def _check_all_music_in_part_containers(self):
        name = 'all_music_in_part_containers'
        if getattr(self.score_template, name, None) is not True:
            return
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            for component in voice:
                if isinstance(component, (abjad.MultimeasureRest, abjad.Skip)):
                    continue
                if (type(component) is abjad.Container and
                    component.identifier and
                    component.identifier.startswith('%*% ')):
                    continue
                message = f'{voice.name} contains {component!r}'
                message += ' outside part container.'
                raise Exception(message)

    def _check_persistent_indicators(self):
        if self.do_not_check_persistence:
            return
        if self._environment == 'docs':
            return
        tag = abjad.tags.SOUNDS_DURING_SEGMENT
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            if not abjad.inspect(voice).get_annotation(tag):
                continue
            for i, leaf in enumerate(abjad.iterate(voice).leaves()):
                self._check_persistent_indicators_for_leaf(voice.name, leaf, i)

    def _check_persistent_indicators_for_leaf(self, voice, leaf, i):
        prototype = (
            abjad.Accelerando,
            abjad.MetronomeMark,
            abjad.Ritardando,
            )
        mark = abjad.inspect(leaf).get_effective(prototype)
        if mark is None:
            message = f'{voice} leaf {i} ({leaf!s}) missing metronome mark.'
            raise Exception(message)
        instrument = abjad.inspect(leaf).get_effective(abjad.Instrument)
        if instrument is None:
            message = f'{voice} leaf {i} ({leaf!s}) missing instrument.'
            raise Exception(message)
        if instrument.hide:
            markup = abjad.inspect(leaf).get_effective(abjad.MarginMarkup)
            if markup is None:
                message = f'{voice} leaf {i} ({leaf!s}) missing margin markup.'
                raise Exception(message)
        clef = abjad.inspect(leaf).get_effective(abjad.Clef)
        if clef is None:
            message = f'{voice} leaf {i} ({leaf!s}) missing clef.'
            raise Exception(message)

    def _check_range(self):
        if not self.range_checker:
            return
        if isinstance(self.range_checker, abjad.PitchRange):
            markup = abjad.Markup('*', direction=abjad.Up)
            abjad.tweak(markup).color = 'red'
            for voice in abjad.iterate(self.score).components(abjad.Voice):
                for leaf in abjad.iterate(voice).leaves(pitched=True):
                    if leaf not in self.range_checker:
                        if self.color_out_of_range_pitches:
                            abjad.label(leaf).color_leaves('red')
                            abjad.attach(markup, leaf, tag='SM13')
                        else:
                            raise Exception(f'out of range: {leaf!r}.')
        else:
            raise NotImplementedError(self.range_checker)

    def _check_wellformedness(self):
        if self.skip_wellformedness_checks:
            return
        if (self.color_octaves or
            self.color_repeat_pitch_classes or
            self.ignore_repeat_pitch_classes):
            return
        manager = baca.WellformednessManager(allow_percussion_clef=True)
        if not manager.is_well_formed(self.score):
            message = manager.tabulate_wellformedness(self.score)
            raise Exception('\n' + message)

    def _collect_alive_during_segment(self):
        result = []
        for context in abjad.iterate(self.score).components(abjad.Context):
            result.append(context.name)
        return result

    def _collect_first_appearance_margin_markup(self):
        if self.first_segment:
            return
        if not self.margin_markups:
            return
        self._cache_previously_alive_contexts()
        dictionary = abjad.OrderedDict()
        prototype = abjad.MarginMarkup
        for staff in abjad.iterate(self.score).components(abjad.Staff):
            if staff.name in self._previously_alive_contexts:
                continue
            for leaf in abjad.iterate(staff).leaves():
                margin_markup = abjad.inspect(leaf).get_effective(prototype)
                if margin_markup is not None:
                    key = self._indicator_to_key(margin_markup, self.manifests)
                    dictionary[staff.name] = key
                    break
        return dictionary

    def _collect_metadata(self):
        result = abjad.OrderedDict()
        result['alive_during_segment'] = self._collect_alive_during_segment()
        result['container_to_part'] = self._container_to_part
        result['duration'] = self._duration
        result['fermata_measure_numbers'] = self._fermata_measure_numbers
        dictionary = self._collect_first_appearance_margin_markup()
        result['first_appearance_margin_markup'] = dictionary
        result['first_measure_number'] = self._get_first_measure_number()
        result['last_measure_number'] = self._get_last_measure_number()
        if self._last_measure_is_fermata:
            result['last_measure_is_fermata'] = True
        result['metronome_mark_spanner_right_broken'] = \
            self.metronome_mark_spanner_right_broken
        result['persistent_indicators'] = self._collect_persistent_indicators()
        result['segment_name'] = self.segment_name
        result['segment_number'] = self._get_segment_number()
        result['sounds_during_segment'] = self._sounds_during_segment
        result['start_clock_time'] = self._start_clock_time
        result['stop_clock_time'] = self._stop_clock_time
        result['time_signatures'] = self._cached_time_signatures
        result['voice_metadata'] = self._voice_metadata
        items = sorted(result.items())
        metadata = abjad.OrderedDict(items)
        self.metadata.update(metadata)
        items = list(self.metadata.items())
        for key, value in items:
            if not bool(value):
                del(self.metadata[key])

    def _collect_persistent_indicators(self):
        result = abjad.OrderedDict()
        contexts = abjad.iterate(self.score).components(abjad.Context)
        contexts = list(contexts)
        contexts.sort(key=lambda _: _.name)
        for context in contexts:
            momentos = []
            dictionary = context._get_persistent_wrappers()
            for wrapper in dictionary.values():
                leaf = wrapper.component
                parentage = abjad.inspect(leaf).get_parentage()
                first_context = parentage.get_first(abjad.Context)
                indicator = wrapper.indicator
                value = self._indicator_to_key(indicator, self.manifests)
                if isinstance(indicator.persistent, str):
                    prototype = indicator.persistent
                else:
                    prototype = type(indicator)
                    prototype = self._prototype_string(prototype)
                momento = abjad.Momento(
                    context=first_context.name,
                    edition=wrapper.tag.edition(),
                    prototype=prototype,
                    value=value,
                    )
                momentos.append(momento)
            if momentos:
                momentos.sort(key=lambda _: _.prototype)
                result[context.name] = momentos
        return result

    def _color_octaves_(self):
        if not self.color_octaves:
            return
        score = self.score
        vertical_moments = abjad.iterate(score).vertical_moments()
        markup = abjad.Markup('OCTAVE', direction=abjad.Up)
        abjad.tweak(markup).color = 'red'
        for vertical_moment in vertical_moments:
            pitches = []
            for leaf in vertical_moment.leaves:
                if isinstance(leaf, abjad.Note):
                    pitches.append(leaf.written_pitch)
                elif isinstance(leaf, abjad.Chord):
                    pitches.extend(leaf.written_pitches)
            if not pitches:
                continue
            pitch_classes = [_.pitch_class for _ in pitches]
            if baca.PitchClassSegment(pitch_classes).has_duplicates():
                notes_and_chords = vertical_moment.notes_and_chords
                notes_and_chords = abjad.select(notes_and_chords)
                abjad.label(notes_and_chords).color_leaves('red')
                for leaf in notes_and_chords:
                    abjad.attach(markup, leaf, tag='SM12')

    def _color_repeat_pitch_classes_(self):
        manager = baca.WellformednessManager
        lts = manager._find_repeat_pitch_classes(self.score)
        markup = abjad.Markup('@', direction=abjad.Up)
        abjad.tweak(markup).color = 'red'
        for lt in lts:
            abjad.label(lt).color_leaves('red')
            for leaf in lt:
                abjad.attach(markup, leaf, tag='SM14')

    def _color_unpitched_notes(self):
        if self.ignore_unpitched_notes:
            return
        tag = abjad.tags.NOT_YET_PITCHED
        for pleaf in abjad.iterate(self.score).leaves(pitched=True):
            if not abjad.inspect(pleaf).has_indicator(tag):
                continue
            literal = abjad.LilyPondLiteral(r'\makeBlue')
            abjad.attach(literal, pleaf, tag='SM24')

    def _color_unregistered_pitches(self):
        if self.ignore_unregistered_pitches:
            return
        tag = abjad.tags.NOT_YET_REGISTERED
        for pleaf in abjad.iterate(self.score).leaves(pitched=True):
            if not abjad.inspect(pleaf).has_indicator(tag):
                continue
            literal = abjad.LilyPondLiteral(r'\makeMagenta')
            abjad.attach(literal, pleaf, tag='SM25')

    def _comment_measure_numbers(self):
        contexts = []
        contexts.extend(self.score['GlobalContext'])
        contexts.extend(abjad.iterate(self.score).components(abjad.Voice))
        for context in contexts:
            for leaf in abjad.iterate(context).leaves():
                offset = abjad.inspect(leaf).get_timespan().start_offset
                measure_number = self._offset_to_measure_number.get(
                    offset,
                    None,
                    )
                if measure_number is None:
                    continue
                if self.segment_name :
                    name = self.segment_name + ' '
                else:
                    name = ''
                string = f'% [{name}{context.name} measure {measure_number}]'
                literal = abjad.LilyPondLiteral(string, 'absolute_before')
                abjad.attach(literal, leaf, tag='SM4')

    def _deactivate_tags(self, tags):
        if not tags:
            return
        for leaf in abjad.iterate(self.score).leaves():
            for wrapper in abjad.inspect(leaf).wrappers():
                if wrapper.tag is None:
                    continue
                for tag in tags:
                    if tag in wrapper.tag:
                        wrapper.deactivate = True
                        break

    @staticmethod
    def _extend_beam(leaf):
        beam = abjad.inspect(leaf).get_spanner(abjad.Beam)
        if beam is None:
            return
        all_leaves = []
        all_leaves.extend(beam.leaves)
        durations = []
        if hasattr(beam, 'durations'):
            durations.extend(beam.durations)
        else:
            duration = abjad.inspect(beam.leaves).get_duration()
            durations.append(duration)
        intervening_skips = []
        index = 1
        while True:
            next_leaf = abjad.inspect(leaf).get_leaf(index)
            if next_leaf is None:
                return
            index += 1
            if isinstance(next_leaf, abjad.Skip):
                beam = abjad.inspect(next_leaf).get_spanner(abjad.Beam)
                if beam is None:
                    intervening_skips.append(next_leaf)
                    continue
            break
        abjad.detach(abjad.Beam, leaf)
        all_leaves.extend(intervening_skips)
        if intervening_skips:
            intervening_skips = abjad.select(intervening_skips)
            duration = abjad.inspect(intervening_skips).get_duration()
            durations.append(duration)
        beam = abjad.inspect(next_leaf).get_spanner(abjad.Beam)
        if beam is None:
            all_leaves.append(next_leaf)
            duration = abjad.inspect(next_leaf).get_duration()
            durations.append(duration)
        else:
            all_leaves.extend(beam.leaves)
            if hasattr(beam, 'durations'):
                durations.extend(beam.durations)
            else:
                duration = abjad.inspect(beam.leaves).get_duration()
                durations.append(duration)
        abjad.detach(abjad.Beam, next_leaf)
        all_leaves = abjad.select(all_leaves)
        assert abjad.inspect(all_leaves).get_duration() == sum(durations)
        beam = abjad.DuratedComplexBeam(beam_rests=True, durations=durations)
        abjad.attach(beam, all_leaves, tag='SM35')

    def _extend_beams(self):
        for leaf in abjad.iterate(self.score).leaves():
            if abjad.inspect(leaf).get_indicator(abjad.tags.RIGHT_BROKEN_BEAM):
                self._extend_beam(leaf)

    def _get_first_measure_number(self):
        if self.first_measure_number is not None:
            return self.first_measure_number
        if not self.previous_metadata:
            return 1
        string = 'first_measure_number'
        first_measure_number = self.previous_metadata.get(string)
        time_signatures = self.previous_metadata.get('time_signatures')
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

    def _get_last_measure_number(self):
        return self._get_first_measure_number() + self.measure_count - 1

    def _get_measure_number_tag(self, leaf):
        start_offset = abjad.inspect(leaf).get_timespan().start_offset
        measure_number = self._offset_to_measure_number.get(start_offset)
        if measure_number is not None:
            return f'MEASURE_{measure_number}'

    def _get_measure_timespans(self, measure_numbers):
        timespans = []
        first_measure_number = self._get_first_measure_number()
        measure_indices = [
            _ - first_measure_number - 1 for _ in measure_numbers
            ]
        skips = baca.select(self.score['GlobalSkips']).skips()
        for i, skip in enumerate(skips):
            if i in measure_indices:
                timespan = abjad.inspect(skip).get_timespan()
                timespans.append(timespan)
        return timespans

    def _get_persistent_indicator(self, context, prototype):
        assert isinstance(context, abjad.Context), repr(context)
        if not self.previous_metadata:
            return
        dictionary = self.previous_metadata.get('persistent_indicators')
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

    def _get_previous_stop_clock_time(self):
        if self.previous_metadata:
            return self.previous_metadata.get('stop_clock_time')

    def _get_previous_voice_metadata(self, voice, voice_metadata_pairs):
        if not bool(self.previous_metadata) or not bool(voice_metadata_pairs):
            return
        voice_metadata = self.previous_metadata.get('voice_metadata')
        if not bool(voice_metadata):
            return
        this_voice_metadata = voice_metadata.get(voice.name)
        if not bool(this_voice_metadata):
            return
        result = abjad.OrderedDict()
        for name, keys in voice_metadata_pairs:
            key_value_pairs = this_voice_metadata.get(name)
            assert isinstance(key_value_pairs, list)
            for key, value in key_value_pairs:
                result[key] = value
        return result

    def _get_segment_measure_numbers(self):
        first_measure_number = self._get_first_measure_number()
        last_measure_number = self._get_last_measure_number()
        return list(range(first_measure_number, last_measure_number + 1))

    def _get_segment_number(self):
        if not self.previous_metadata:
            segment_number = 0
        else:
            segment_number = self.previous_metadata.get('segment_number')
            if segment_number is None:
                message = 'previous metadata missing segment number.'
                raise Exception(message)
        return segment_number + 1

    def _get_stage_offsets(self, start_stage, stop_stage):
        skips = baca.select(self.score['GlobalSkips']).skips()
        result = self._stage_number_to_measure_indices(start_stage)
        start_measure_index, stop_measure_index = result
        start_skip = skips[start_measure_index]
        assert isinstance(start_skip, abjad.Skip), start_skip
        start_offset = abjad.inspect(start_skip).get_timespan().start_offset
        result = self._stage_number_to_measure_indices(stop_stage)
        start_measure_index, stop_measure_index = result
        stop_skip = skips[stop_measure_index]
        assert isinstance(stop_skip, abjad.Skip), stop_skip
        stop_offset = abjad.inspect(stop_skip).get_timespan().stop_offset
        return start_offset, stop_offset

    def _get_stage_time_signatures(self, start_stage=None, stop_stage=None):
        assert len(self.time_signatures) == sum(self.measures_per_stage)
        stages = baca.Sequence(self.time_signatures).partition_by_counts(
            self.measures_per_stage,
            )
        start_index = start_stage - 1
        if stop_stage is None:
            time_signatures = stages[start_index]
        else:
            stop_index = stop_stage
            stages = stages[start_index:stop_index]
            time_signatures = baca.sequence(stages).flatten(depth=-1)
        pair = (start_stage, stop_stage)
        start_offset, stop_offset = self._get_stage_offsets(*pair)
        return start_offset, time_signatures

    def _get_stylesheets(self):
        if self._environment == 'docs':
            if abjad.inspect(self.score).get_indicator(abjad.tags.TWO_VOICE):
                return [self._relative_two_voice_staff_stylesheet_path]
            else:
                return [self._relative_string_trio_stylesheet_path]
        elif self._environment == 'external':
            if abjad.inspect(self.score).get_indicator(abjad.tags.TWO_VOICE):
                return [self._absolute_two_voice_staff_stylesheet_path]
            else:
                return [self._absolute_string_trio_stylesheet_path]
        includes = []
        includes.append(self._score_package_stylesheet_path)
        if 1 < self._get_segment_number():
            includes.append(self._score_package_nonfirst_stylesheet_path)
        return includes

    @staticmethod
    def _get_tag(status, stem, prefix=None, suffix=None):
        stem = abjad.String(stem).delimit_words()
        stem = '_'.join([_.upper() for _ in stem])
        if suffix is not None:
            name = f'{status.upper()}_{stem}_{suffix.upper()}'
        else:
            name = f'{status.upper()}_{stem}'
        if prefix is not None:
            name = f'{prefix.upper()}_{name}'
        tag = getattr(abjad.tags, name)
        return abjad.Tag(tag)

    def _handle_mutator(self, command):
        if (hasattr(command.command, '_mutates_score') and
            command.command._mutates_score()):
            self._cache = None

    @staticmethod
    def _indicator_to_grob(indicator):
        if isinstance(indicator, abjad.Dynamic):
            return 'DynamicText'
        elif isinstance(indicator, abjad.Instrument):
            return 'InstrumentName'
        elif isinstance(indicator, abjad.MetronomeMark):
            return 'TextScript'
        elif isinstance(indicator, abjad.MarginMarkup):
            return 'InstrumentName'
        elif isinstance(indicator, baca.StaffLines):
            return 'StaffSymbol'
        return type(indicator).__name__

    @staticmethod
    def _indicator_to_key(indicator, manifests):
        if isinstance(indicator, abjad.Clef):
            return indicator.name
        if isinstance(indicator, abjad.Dynamic):
            return indicator.command or indicator.name
        if isinstance(indicator, abjad.Instrument):
            return SegmentMaker._get_key(
                manifests['abjad.Instrument'],
                indicator,
                )
        elif isinstance(indicator, abjad.MetronomeMark):
            return SegmentMaker._get_key(
                manifests['abjad.MetronomeMark'],
                indicator,
                )
        elif isinstance(indicator, abjad.MarginMarkup):
            return SegmentMaker._get_key(
                manifests['abjad.MarginMarkup'],
                indicator,
                )
        elif isinstance(indicator, baca.StaffLines):
            return indicator.line_count
        elif isinstance(indicator, (abjad.Accelerando, abjad.Ritardando)):
            return f'abjad.{repr(indicator)}'
        return str(indicator)

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

    def _intercalate_silences(self, rhythms):
        result = []
        durations = [_.duration for _ in self.time_signatures]
        measure_start_offsets = abjad.mathtools.cumulative_sums(durations)
        segment_duration = measure_start_offsets[-1]
        self._segment_duration = segment_duration
        previous_stop_offset = abjad.Offset(0)
        for rhythm in rhythms:
            start_offset = rhythm.start_offset
            if start_offset < previous_stop_offset:
                raise Exception('overlapping offsets: {rhythm!r}.')
            if previous_stop_offset < start_offset:
                silences = self._make_measure_silences(
                    previous_stop_offset,
                    start_offset,
                    measure_start_offsets,
                    )
                result.extend(silences)
            result.extend(rhythm.annotation)
            duration = abjad.inspect(rhythm.annotation).get_duration()
            previous_stop_offset = start_offset + duration
        if previous_stop_offset < segment_duration:
            silences = self._make_measure_silences(
                previous_stop_offset,
                segment_duration,
                measure_start_offsets,
                )
            result.extend(silences)
        return result

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
        elif prototype is baca.StaffLines:
            indicator = baca.StaffLines(line_count=key)
        else:
            raise Exception(prototype)
        return indicator

    def _label_clock_time(self):
        skips = baca.select(self.score['GlobalSkips']).skips()
        if abjad.inspect(skips[0]).get_effective(abjad.MetronomeMark) is None:
            return
        start_clock_time = self._get_previous_stop_clock_time()
        start_clock_time = start_clock_time or "0'00''"
        self._start_clock_time = start_clock_time 
        minutes = 0
        if "'" in self._start_clock_time:
            tick_index = self._start_clock_time.find("'")
            minutes = self._start_clock_time[:tick_index]
            minutes = int(minutes)
        seconds = self._start_clock_time[-4:-2]
        seconds = int(seconds)
        seconds = 60 * minutes + seconds
        segment_start_offset = abjad.Duration(seconds)
        tag = abjad.Tag(abjad.tags.CLOCK_TIME_MARKUP)
        label = abjad.label(
            skips,
            deactivate=True,
            tag=tag.prepend('SM28'),
            )
        segment_stop_duration = label.with_start_offsets(
            brackets=True,
            clock_time=True,
            color=abjad.SchemeColor('DarkCyan'),
            font_size=3,
            global_offset=segment_start_offset,
            )
        segment_stop_offset = abjad.Offset(segment_stop_duration)
        self._stop_clock_time = segment_stop_offset.to_clock_string()
        segment_duration = segment_stop_offset - segment_start_offset
        segment_duration = segment_duration.to_clock_string()
        self._duration = segment_duration

    def _label_measure_indices(self):
        skips = baca.select(self.score['GlobalSkips']).skips()
        first_measure_number = self._get_first_measure_number()
        for measure_index, skip in enumerate(skips):
            measure_number = first_measure_number + measure_index
            markup = abjad.Markup(f'({measure_number})')
            markup = markup.with_color(abjad.SchemeColor('DarkCyan'))
            markup = markup.fontsize(3)
            markup = abjad.new(markup, direction=abjad.Up)
            tag = abjad.Tag(abjad.tags.MEASURE_NUMBER_MARKUP)
            abjad.attach(
                markup,
                skip,
                deactivate=True,
                tag=tag.prepend('SM31'),
                )
            markup = abjad.Markup(f'<{measure_index}>')
            markup = markup.with_color(abjad.SchemeColor('DarkCyan'))
            markup = markup.fontsize(3)
            markup = abjad.new(markup, direction=abjad.Up)
            tag = abjad.Tag(abjad.tags.MEASURE_INDEX_MARKUP)
            abjad.attach(
                markup,
                skip,
                deactivate=True,
                tag=tag.prepend('SM32'),
                )

    def _label_stage_numbers(self):
        skips = baca.select(self.score['GlobalSkips']).skips()
        for stage_index in range(self.stage_count):
            stage_number = stage_index + 1
            result = self._stage_number_to_measure_indices(stage_number)
            start_measure_index, stop_measure_index = result
            name = self.segment_name or self.rehearsal_mark
            if bool(name):
                string = f'[{name}.{stage_number}]'
            else:
                string = f'[{stage_number}]'
            markup = abjad.Markup(string)
            markup = markup.with_color(abjad.SchemeColor('DarkCyan'))
            markup = markup.fontsize(3)
            markup = abjad.new(markup, direction=abjad.Up)
            skip = skips[start_measure_index]
            tag = abjad.Tag(abjad.tags.STAGE_NUMBER_MARKUP)
            abjad.attach(
                markup,
                skip,
                deactivate=True,
                tag=tag.prepend('SM3'),
                )

    def _make_global_skips(self):
        context = self.score['GlobalSkips']
        for time_signature in self.time_signatures:
            skip = abjad.Skip(1)
            multiplier = abjad.Multiplier(time_signature.duration)
            abjad.attach(multiplier, skip, tag=None)
            abjad.attach(time_signature, skip, context='Score', tag='SM1')
            context.append(skip)
        if self.first_segment:
            return
        # empty start bar allows LilyPond to print bar numbers
        # at start of nonfirst segments
        first_skip = baca.select(context).skip(0)
        literal = abjad.LilyPondLiteral(r'\bar ""')
        tag = abjad.Tag.from_words([
            '+SEGMENT',
            abjad.tags.EMPTY_START_BAR,
            ])
        abjad.attach(
            literal,
            first_skip,
            tag=tag.prepend('SM2'),
            )

    def _make_lilypond_align_above_context_settings(self):
        if self.first_segment:
            return
        top_level = list(self.score['MusicContext'])
        for i, staff_or_group in enumerate(top_level):
            assert isinstance(staff_or_group, (abjad.Staff, abjad.StaffGroup))
            if not self._born_this_segment(staff_or_group):
                continue
            below = top_level[i + 1:]
            for staff in abjad.iterate(below).components(abjad.Staff):
                if self._alive_during_previous_segment(staff):
                    value = abjad.Scheme(staff.name, force_quotes=True)
                    abjad.setting(staff_or_group).align_above_context = value
                    break

    def _make_lilypond_file(self):
        includes = self._get_stylesheets()
        if self._environment == 'external':
            use_relative_includes = False
        else:
            use_relative_includes = True
        lilypond_file = abjad.LilyPondFile.new(
            music=self.score,
            date_time_token=False,
            includes=includes,
            use_relative_includes=use_relative_includes,
            )
        block_names = ('layout', 'paper')
        for item in lilypond_file.items[:]:
            if getattr(item, 'name', None) in block_names:
                lilypond_file.items.remove(item)
        if self._midi:
            block = abjad.Block(name='midi')
            lilypond_file.items.append(block)
        for item in lilypond_file.items[:]:
            if getattr(item, 'name', None) == 'header':
                lilypond_file.items.remove(item)
        if self._environment != 'docs' and not self.do_not_include_layout_ly:
            assert len(lilypond_file.score_block.items) == 1
            score = lilypond_file.score_block.items[0]
            assert isinstance(score, abjad.Score)
            include = abjad.Container()
            string = r'\include "layout.ly"'
            literal = abjad.LilyPondLiteral(string, 'opening')
            abjad.attach(literal, include, tag=None)
            container = abjad.Container(
                [include, score],
                is_simultaneous=True,
                )
            lilypond_file.score_block.items[:] = [container]
        self._lilypond_file = lilypond_file

    def _make_measure_silences(self, start, stop, measure_start_offsets):
        offsets = [start]
        for measure_start_offset in measure_start_offsets:
            if start < measure_start_offset < stop:
                offsets.append(measure_start_offset)
        offsets.append(stop)
        silences = []
        durations = abjad.mathtools.difference_series(offsets)
        for duration in durations:
            multiplier = abjad.Multiplier(duration)
            if self.skips_instead_of_rests:
                silence = abjad.Skip(1)
            else:
                silence = abjad.MultimeasureRest(1)
            abjad.attach(multiplier, silence, tag=None)
            silences.append(silence)
        return silences

    def _make_multimeasure_rests(self):
        rests = []
        for time_signature in self.time_signatures:
            rest = abjad.MultimeasureRest(abjad.Duration(1))
            multiplier = abjad.Multiplier(time_signature.duration)
            abjad.attach(multiplier, rest, tag=None)
            rests.append(rest)
        return rests

    def _make_score(self):
        score = self.score_template()
        first_measure_number = self._get_first_measure_number()
        if first_measure_number != 1:
            abjad.setting(score).current_bar_number = first_measure_number
        self._score = score

    def _momento_to_indicator(self, momento):
        if momento.value is None:
            return
        if momento.value in ('abjad.Accelerando()', 'abjad.Ritardando()'):
            indicator = eval(momento.value)
            return indicator
        if momento.prototype in self._prototype_to_manifest_name:
            name = self._prototype_to_manifest_name.get(momento.prototype)
            dictionary = getattr(self, name)
            return dictionary.get(momento.value)
        class_ = eval(momento.prototype)
        if hasattr(class_, 'from_string'):
            return class_.from_string(momento.value)
        if class_ is abjad.Dynamic and momento.value.startswith('\\'):
            return class_(name='', command=momento.value)
        return class_(momento.value)

    def _populate_offset_to_measure_number(self):
        measure_number = self._get_first_measure_number()
        for skip in baca.select(self.score['GlobalSkips']).skips():
            offset = abjad.inspect(skip).get_timespan().start_offset
            self._offset_to_measure_number[offset] = measure_number
            measure_number += 1

    def _print_cache(self):
        for context in self._cache:
            print(f'CONTEXT {context} ...')
            leaves_by_stage_number = self._cache[context]
            for stage_number in leaves_by_stage_number:
                print(f'STAGE {stage_number} ...')
                for leaf in leaves_by_stage_number[stage_number]:
                    print(leaf)

    @staticmethod
    def _prototype_string(class_):
        parts = class_.__module__.split('.')
        return f'{parts[0]}.{parts[-1]}'

    def _reapply_persistent_indicators(self):
        if self.first_segment:
            return
        string = 'persistent_indicators'
        dictionary = self.previous_metadata.get('persistent_indicators')
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
                    if status is None:
                        continue
                    assert status == 'reapplied', repr(status)
                    wrapper = abjad.inspect(leaf).wrapper(abjad.TimeSignature)
                    edition = edition.prepend('SM38')
                    wrapper.tag = wrapper.tag.prepend(edition)
                    self._categorize_persistent_wrapper(
                        self.manifests,
                        wrapper,
                        status,
                        )
                    continue
                prototype = (
                    #abjad.Accelerando,
                    abjad.MetronomeMark,
                    #abjad.Ritardando,
                    )
                if isinstance(previous_indicator, prototype):
                    spanner = abjad.inspect(leaf).get_spanner(
                        abjad.MetronomeMarkSpanner
                        )
                    if status == 'reapplied':
                        wrapper = spanner.attach(
                            previous_indicator,
                            leaf,
                            tag=edition.append('SM36'),
                            wrapper=True,
                            )
                        self._categorize_persistent_wrapper(
                            self.manifests,
                            wrapper,
                            status,
                            )
                        #if isinstance(previous_indicator, abjad.Ritardando):
                        #    print(wrapper)
                        #    raise Exception('RRR', status)
                    else:
                        assert status in ('redundant', None), repr(status)
                        if status is None or spanner._is_trending(leaf):
                            status = 'explicit'
                        #prototype = abjad.MetronomeMark
                        wrapper = abjad.inspect(leaf).wrapper(prototype)
                        wrapper.tag = wrapper.tag.prepend(edition)
                        self._categorize_persistent_wrapper(
                            self.manifests,
                            wrapper,
                            status,
                            )
                    continue
                attached = False
                try:
                    wrapper = abjad.attach(
                        previous_indicator,
                        leaf,
                        tag=edition.append('SM37'),
                        wrapper=True,
                        )
                    attached = True
                except abjad.PersistentIndicatorError:
                    pass
                if attached:
                    self._categorize_persistent_wrapper(
                        self.manifests,
                        wrapper,
                        status,
                        )

    def _remove_redundant_time_signatures(self):
        previous_time_signature = None
        self._cached_time_signatures = []
        for skip in baca.select(self.score['GlobalSkips']).skips():
            time_signature = abjad.inspect(skip).get_indicator(
                abjad.TimeSignature
                )
            self._cached_time_signatures.append(str(time_signature))
            if time_signature == previous_time_signature:
                abjad.detach(time_signature, skip)
            else:
                previous_time_signature = time_signature

    def _remove_tags(self, tags):
        tags = tags or ()
        assert isinstance(tags, (tuple, list)), repr(tags)
        if self._environment == 'docs':
            remove_documentation_tags = (
                abjad.tags.CLOCK_TIME_MARKUP,
                abjad.tags.FIGURE_NAME_MARKUP,
                abjad.tags.MEASURE_INDEX_MARKUP,
                abjad.tags.MEASURE_NUMBER_MARKUP,
                abjad.tags.SPACING_MARKUP,
                abjad.tags.STAGE_NUMBER_MARKUP,
                )
            tags += remove_documentation_tags
        for leaf in abjad.iterate(self.score).leaves():
            for wrapper in abjad.inspect(leaf).wrappers():
                if wrapper.tag is None:
                    continue
                for word in wrapper.tag:
                    if word in tags:
                        abjad.detach(wrapper, leaf)
                        break

    def _scope_to_leaf_selection(self, wrapper):
        leaves = []
        selections = self._scope_to_leaf_selections(wrapper.scope)
        for selection in selections:
            leaves.extend(selection)
        selection = abjad.select(leaves)
        if not selection:
            message = f'EMPTY SELECTION:\n\n{format(wrapper)}'
            if self.allow_empty_selections:
                print(message)
            else:
                raise Exception(message)
        assert selection.are_leaves(), repr(selection)
        if isinstance(wrapper.scope, baca.TimelineScope):
            selection = wrapper.scope._sort_by_timeline(selection)
        return selection

    def _scope_to_leaf_selections(self, scope):
        if self._cache is None:
            self._cache_leaves()
        if isinstance(scope, baca.Scope):
            scopes = [scope]
        else:
            assert isinstance(scope, baca.TimelineScope)
            scopes = list(scope.scopes)
        leaf_selections = []
        for scope in scopes:
            leaves = []
            try:
                leaves_by_stage_number = self._cache[scope.voice_name]
            except KeyError:
                message = f'unknown voice {scope.voice_name!r}.'
                raise Exception(message)
            start = scope.stages[0]
            if (scope.stages[1] == abjad.Infinity or
                scope.stages[1] is abjad.Infinity):
                stop = self.stage_count + 1
            else:
                stop = scope.stages[1] + 1
            for stage_number in range(start, stop):
                leaves.extend(leaves_by_stage_number[stage_number])
            leaf_selections.append(abjad.select(leaves))
        return leaf_selections

    def _set_status_tag(
        wrapper,
        status,
        redraw=None,
        stem=None,
        ):
        assert isinstance(wrapper, abjad.Wrapper), repr(wrapper)
        existing_tag = wrapper.tag
        stem = stem or abjad.String.to_indicator_stem(wrapper.indicator)
        prefix = None
        if redraw is True:
            prefix = 'redrawn'
        tag = SegmentMaker._get_tag(status, stem, prefix=prefix)
        if wrapper.tag:
            tag = wrapper.tag.prepend(tag)
        if wrapper.spanner is not None:
            tag = tag.prepend('SM27')
            wrapper.deactivate = True
            wrapper.tag = tag
            if isinstance(wrapper.spanner, abjad.MetronomeMarkSpanner):
                color = SegmentMaker._status_to_color[status]
                tag = f'{status.upper()}_{stem}_WITH_COLOR'
                tag = getattr(abjad.tags, tag)
                tag = abjad.Tag(tag)
                if existing_tag:
                    tag = existing_tag.prepend(tag)
                alternate = (color, tag.prepend('SM15'))
                wrapper._alternate = alternate
        else:
            tag = tag.prepend('SM8')
            wrapper.tag = tag

    def _shift_clefs_into_fermata_measures(self):
        fermata_stop_offsets = self._fermata_stop_offsets[:]
        if self.previous_metadata.get('last_measure_is_fermata') is True:
            fermata_stop_offsets.insert(0, abjad.Offset(0))
        if not fermata_stop_offsets:
            return
        for staff in abjad.iterate(self.score).components(abjad.Staff):
            for leaf in abjad.iterate(staff).leaves():
                start_offset = abjad.inspect(leaf).get_timespan().start_offset
                if start_offset not in fermata_stop_offsets:
                    continue
                wrapper = abjad.inspect(leaf).wrapper(abjad.Clef)
                if wrapper is None or not wrapper.tag:
                    continue
                if abjad.tags.EXPLICIT_CLEF not in wrapper.tag:
                    continue
                measure_number = self._offset_to_measure_number.get(
                    start_offset,
                    )
                if measure_number is None:
                    continue
                clef = wrapper.indicator
                dictionary = self._offset_to_measure_number
                command = baca.shift_clef(clef, selector=baca.leaf(0))
                command.offset_to_measure_number = dictionary
                command(leaf)

    def _shorten_long_repeat_ties(self):
        leaves = abjad.iterate(self.score).leaves()
        for leaf in leaves:
            ties = abjad.inspect(leaf).get_spanners(abjad.Tie)
            if not ties:
                continue
            tie = ties.pop()
            if not tie.repeat:
                continue
            previous_leaf = abjad.inspect(leaf).get_leaf(-1)
            if previous_leaf is None:
                continue
            minimum_duration = abjad.Duration(1, 8)
            if abjad.inspect(previous_leaf).get_duration() < minimum_duration:
                string = r"\shape #'((2 . 0) (1 . 0) (0.5 . 0) (0 . 0))"
                string += " RepeatTie"
                literal = abjad.LilyPondLiteral(string)
                abjad.attach(literal, leaf, tag='SM26')

    def _stage_number_to_measure_indices(self, stage_number):
        if stage_number is abjad.Infinity or stage_number == abjad.Infinity:
            stage_number = self.stage_count
        if self.stage_count < stage_number:
            count = self.stage_count
            counter = abjad.String('stage').pluralize(count)
            message = f'segment has only {count} {counter}'
            message += f' (not {stage_number}).'
            raise Exception(message)
        measure_indices = abjad.mathtools.cumulative_sums(
            self.measures_per_stage)
        stop = stage_number - 1
        start_measure_index = measure_indices[stop]
        stop_measure_index = measure_indices[stage_number] - 1
        return start_measure_index, stop_measure_index

    def _style_fermata_measures(self):
        if self.fermata_measure_staff_line_count is None:
            return
        if not self._fermata_start_offsets:
            return
        prototype = baca.StaffLines
        staff_lines = baca.StaffLines(self.fermata_measure_staff_line_count)
        bar_lines_already_styled = []
        for staff in abjad.iterate(self.score).components(abjad.Staff):
            for leaf in abjad.iterate(staff).leaves():
                start_offset = abjad.inspect(leaf).get_timespan().start_offset
                if start_offset not in self._fermata_start_offsets:
                    continue
                before = abjad.inspect(leaf).get_effective(prototype)
                next_leaf = abjad.inspect(leaf).get_leaf(1)
                if next_leaf is not None:
                    after = abjad.inspect(next_leaf).get_effective(prototype)
                if before != staff_lines:
                    strings = staff_lines._get_lilypond_format(context=staff)
                    if getattr(before, 'line_count', 5) == 5:
                        context = staff.name
                        string = f"{context}.BarLine.bar-extent = #'(-2 . 2)"
                        string = r'\once \override ' + string
                        strings.append(string)
                    if strings:
                        literal = abjad.LilyPondLiteral(strings)
                        abjad.attach(literal, leaf, tag='SM20')
                if next_leaf is not None and staff_lines != after:
                    strings = after._get_lilypond_format(context=staff)
                    literal = abjad.LilyPondLiteral(strings)
                    abjad.attach(literal, next_leaf, tag='SM21')
                if next_leaf is None and before != staff_lines:
                    before_line_count = getattr(before, 'line_count', 5)
                    before_staff_lines = baca.StaffLines(
                        line_count=before_line_count,
                        hide=True,
                        )
                    abjad.attach(
                        before_staff_lines,
                        leaf,
                        tag='SM23',
                        synthetic_offset=1_000_000,
                        )
                if start_offset in bar_lines_already_styled:
                    continue
                strings = []
                if (staff_lines.line_count == 0 and
                    not (next_leaf is None and self.last_segment)):
                    string = r'Score.BarLine.transparent = ##t'
                    string = r'\once \override ' + string
                    strings.append(string)
                    string = r'Score.SpanBar.transparent = ##t'
                    string = r'\once \override ' + string
                    strings.append(string)
                elif staff_lines.line_count == 1:
                    string = "Score.BarLine.bar-extent = #'(-2 . 2)"
                    string = r'\once \override ' + string
                    strings.append(string)
                if strings:
                    literal = abjad.LilyPondLiteral(strings, 'after')
                    tag = abjad.Tag(abjad.tags.EOL_FERMATA)
                    measure_number_tag = self._get_measure_number_tag(leaf)
                    if measure_number_tag is not None:
                        tag = tag.append(measure_number_tag)
                    abjad.attach(
                        literal,
                        leaf,
                        tag=tag.prepend('SM22'),
                        )
                bar_lines_already_styled.append(start_offset)

    def _transpose_score_(self):
        if not self.transpose_score:
            return
        for pleaf in baca.select(self.score).pleaves():
            if abjad.inspect(pleaf).has_indicator(abjad.tags.DO_NOT_TRANSPOSE):
                continue
            abjad.Instrument.transpose_from_sounding_pitch(pleaf)

    def _validate_measure_count_(self):
        if not self.validate_measure_count:
            return
        found = len(self.time_signatures)
        if found != self.validate_measure_count:
            raise Exception(f'{found} != {self.validate_measure_count}')

    def _validate_measures_per_stage(self):
        if self.measures_per_stage is None:
            return
        if not sum(self.measures_per_stage) == self.measure_count:
            message = f'measures per stage {self.measures_per_stage}'
            message += f' do not match measure count {self.measure_count}.'
            raise Exception(message)

    def _validate_stage_count_(self):
        if not self.validate_stage_count:
            return
        if self.stage_count != self.validate_stage_count:
            message = f'{self.stage_count} != {self.validate_stage_count}'
            raise Exception(message)

    def _voice_to_rhythm_wrappers(self, voice):
        wrappers = []
        for wrapper in self.wrappers:
            if not isinstance(wrapper.command, baca.RhythmCommand):
                continue
            if wrapper.scope.voice_name == voice.name:
                wrappers.append(wrapper)
        return wrappers

    def _whitespace_leaves(self):
        for leaf in abjad.iterate(self.score).leaves():
            literal = abjad.LilyPondLiteral('', 'absolute_before')
            abjad.attach(literal, leaf, tag=None)
            if abjad.inspect(leaf).get_leaf(1) is None:
                literal = abjad.LilyPondLiteral('', 'absolute_after')
                abjad.attach(literal, leaf, tag=None)

    ### PUBLIC PROPERTIES ###

    @property
    def allow_empty_selections(self) -> Optional[bool]:
        r'''Is true when segment allows empty selectors.

        Otherwise segment raises exception on empty selectors.
        '''
        return self._allow_empty_selections

    @property
    def breaks(self) -> Optional[BreakMeasureMap]:
        r'''Gets breaks.
        '''
        return self._breaks

    @property
    def color_octaves(self) -> Optional[bool]:
        r'''Is true when segment-maker colors octaves.

        ..  container:: example

            Colors octaves:

            >>> maker = baca.SegmentMaker(
            ...     color_octaves=True,
            ...     score_template=baca.StringTrioScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 31)),
            ...     time_signatures=[(6, 16), (6, 16)],
            ...     )

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'ViolinMusicVoice',
            ...     [[2, 4, 5, 7, 9, 11]],
            ...     baca.flags(),
            ...     )
            >>> maker(
            ...     baca.scope('ViolinMusicVoice', 1),
            ...     baca.rhythm(contribution['ViolinMusicVoice']),
            ...     )

            >>> contribution = music_maker(
            ...     'CelloMusicVoice',
            ...     [[-3, -5, -7, -8, -10, -12]],
            ...     baca.flags(),
            ...     )
            >>> maker(
            ...     baca.scope('CelloMusicVoice', 1),
            ...     baca.rhythm(contribution['CelloMusicVoice']),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.setting(lilypond_file['Score']).auto_beaming = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                \with
                {
                    autoBeaming = ##f
                }
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 31)             %! HSS1:SPACING
                            \time 6/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 31)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
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
                                    {
                                        \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                            % [ViolinMusicVoice measure 1]                               %! SM4
                                            \set ViolinMusicStaff.instrumentName = \markup {             %! SM8:DEFAULT_INSTRUMENT:ST1
                                                \hcenter-in                                              %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    #10                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    Violin                                               %! SM8:DEFAULT_INSTRUMENT:ST1
                                                }                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                            \set ViolinMusicStaff.shortInstrumentName = \markup {        %! SM8:DEFAULT_INSTRUMENT:ST1
                                                \hcenter-in                                              %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    #10                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    Vn.                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                                }                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                            \clef "treble"                                               %! SM8:DEFAULT_CLEF:ST3
                                            \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                            \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                                        %@% \override ViolinMusicStaff.Clef.color = ##f                  %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                            \set ViolinMusicStaff.forceClef = ##t                        %! SM8:DEFAULT_CLEF:SM33:ST3
                                            d'16
                                            ^ \markup {                                                  %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                \with-color                                              %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                    #(x11-color 'DarkViolet)                             %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                    (Violin)                                             %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                }                                                        %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                            \set ViolinMusicStaff.instrumentName = \markup {             %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                \hcenter-in                                              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    #10                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    Violin                                               %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                }                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            \set ViolinMusicStaff.shortInstrumentName = \markup {        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                \hcenter-in                                              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    #10                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    Vn.                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                }                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            \override ViolinMusicStaff.Clef.color = #(x11-color 'violet) %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
                <BLANKLINE>
                                            e'16
                <BLANKLINE>
                                            \once \override Accidental.color = #red
                                            \once \override Beam.color = #red
                                            \once \override Dots.color = #red
                                            \once \override NoteHead.color = #red
                                            \once \override Stem.color = #red
                                            f'16
                                            - \tweak color #red                                          %! SM12
                                            ^ \markup { OCTAVE }                                         %! SM12
                <BLANKLINE>
                                            g'16
                <BLANKLINE>
                                            a'16
                <BLANKLINE>
                                            b'16
                                        }
                                    }
                <BLANKLINE>
                                    % [ViolinMusicVoice measure 2]                                       %! SM4
                                    R1 * 3/8
                <BLANKLINE>
                                }
                            }
                            \tag Viola                                                                   %! ST4
                            \context ViolaMusicStaff = "ViolaMusicStaff"
                            {
                                \context ViolaMusicVoice = "ViolaMusicVoice"
                                {
                <BLANKLINE>
                                    % [ViolaMusicVoice measure 1]                                        %! SM4
                                    \set ViolaMusicStaff.instrumentName = \markup {                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                        \hcenter-in                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                            #10                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                            Viola                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                        }                                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \set ViolaMusicStaff.shortInstrumentName = \markup {                 %! SM8:DEFAULT_INSTRUMENT:ST1
                                        \hcenter-in                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                            #10                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                            Va.                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                        }                                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \clef "alto"                                                         %! SM8:DEFAULT_CLEF:ST3
                                    \once \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                    \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                                %@% \override ViolaMusicStaff.Clef.color = ##f                           %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                    \set ViolaMusicStaff.forceClef = ##t                                 %! SM8:DEFAULT_CLEF:SM33:ST3
                                    R1 * 3/8
                                    ^ \markup {                                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        \with-color                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            #(x11-color 'DarkViolet)                                     %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            (Viola)                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        }                                                                %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                    \set ViolaMusicStaff.instrumentName = \markup {                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        \hcenter-in                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            #10                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            Viola                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        }                                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \set ViolaMusicStaff.shortInstrumentName = \markup {                 %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        \hcenter-in                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            #10                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            Va.                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        }                                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)          %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
                <BLANKLINE>
                                    % [ViolaMusicVoice measure 2]                                        %! SM4
                                    R1 * 3/8
                <BLANKLINE>
                                }
                            }
                            \tag Cello                                                                   %! ST4
                            \context CelloMusicStaff = "CelloMusicStaff"
                            {
                                \context CelloMusicVoice = "CelloMusicVoice"
                                {
                                    {
                                        \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                            % [CelloMusicVoice measure 1]                                %! SM4
                                            \set CelloMusicStaff.instrumentName = \markup {              %! SM8:DEFAULT_INSTRUMENT:ST1
                                                \hcenter-in                                              %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    #10                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    Cello                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                                }                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                            \set CelloMusicStaff.shortInstrumentName = \markup {         %! SM8:DEFAULT_INSTRUMENT:ST1
                                                \hcenter-in                                              %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    #10                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    Vc.                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                                }                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                            \clef "bass"                                                 %! SM8:DEFAULT_CLEF:ST3
                                            \once \override CelloMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                            \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                                        %@% \override CelloMusicStaff.Clef.color = ##f                   %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                            \set CelloMusicStaff.forceClef = ##t                         %! SM8:DEFAULT_CLEF:SM33:ST3
                                            a16
                                            ^ \markup {                                                  %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                \with-color                                              %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                    #(x11-color 'DarkViolet)                             %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                    (Cello)                                              %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                }                                                        %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            \override CelloMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                            \set CelloMusicStaff.instrumentName = \markup {              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                \hcenter-in                                              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    #10                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    Cello                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                }                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            \set CelloMusicStaff.shortInstrumentName = \markup {         %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                \hcenter-in                                              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    #10                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    Vc.                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                }                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            \override CelloMusicStaff.Clef.color = #(x11-color 'violet)  %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
                <BLANKLINE>
                                            g16
                <BLANKLINE>
                                            \once \override Accidental.color = #red
                                            \once \override Beam.color = #red
                                            \once \override Dots.color = #red
                                            \once \override NoteHead.color = #red
                                            \once \override Stem.color = #red
                                            f16
                                            - \tweak color #red                                          %! SM12
                                            ^ \markup { OCTAVE }                                         %! SM12
                <BLANKLINE>
                                            e16
                <BLANKLINE>
                                            d16
                <BLANKLINE>
                                            c16
                                        }
                                    }
                <BLANKLINE>
                                    % [CelloMusicVoice measure 2]                                        %! SM4
                                    R1 * 3/8
                <BLANKLINE>
                                }
                            }
                        >>
                    >>
                >>

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._color_octaves

    @property
    def color_out_of_range_pitches(self) -> Optional[bool]:
        r'''Is true when segment-maker colors out-of-range pitches.

        ..  container:: example

            Colors out-of-range pitches:

            >>> music_maker = baca.MusicMaker()

            >>> collection_lists = [
            ...     [[4]],
            ...     [[-12, 2, 3, 5, 8, 9, 0]],
            ...     [[11]],
            ...     [[10, 7, 9, 10, 0, 5]],
            ...     ]
            >>> figures, time_signatures = [], []
            >>> for i, collections in enumerate(collection_lists):
            ...     contribution = music_maker(
            ...         'Voice 1',
            ...         collections,
            ...         baca.flags(),
            ...         )
            ...     figures.append(contribution['Voice 1'])
            ...     time_signatures.append(contribution.time_signature)
            ...
            >>> figures_ = []
            >>> for figure in figures:
            ...     figures_.extend(figure)
            ...
            >>> figures = abjad.select(figures_)

            >>> pitch_range = abjad.Violin().pitch_range
            >>> maker = baca.SegmentMaker(
            ...     color_out_of_range_pitches=True,
            ...     range_checker=pitch_range,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=time_signatures,
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.rhythm(figures),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.setting(lilypond_file['Score']).auto_beaming = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                \with
                {
                    autoBeaming = ##f
                }
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 1/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/16
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 7/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 7/16
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 1/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/16
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
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
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 1]                                         %! SM4
                                        e'16
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 2]                                         %! SM4
                                        \once \override Accidental.color = #red
                                        \once \override Beam.color = #red
                                        \once \override Dots.color = #red
                                        \once \override NoteHead.color = #red
                                        \once \override Stem.color = #red
                                        c16
                                        - \tweak color #red                                              %! SM13
                                        ^ \markup { * }                                                  %! SM13
                <BLANKLINE>
                                        d'16
                <BLANKLINE>
                                        ef'16
                <BLANKLINE>
                                        f'16
                <BLANKLINE>
                                        af'16
                <BLANKLINE>
                                        a'16
                <BLANKLINE>
                                        c'16
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 3]                                         %! SM4
                                        b'16
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 4]                                         %! SM4
                                        bf'16
                <BLANKLINE>
                                        g'16
                <BLANKLINE>
                                        a'16
                <BLANKLINE>
                                        bf'16
                <BLANKLINE>
                                        c'16
                <BLANKLINE>
                                        f'16
                <BLANKLINE>
                                    }
                                }
                            }
                        }
                    >>
                >>

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._color_out_of_range_pitches

    @property
    def color_repeat_pitch_classes(self) -> Optional[bool]:
        r'''Is true when segment-maker colors repeat pitch-classes.

        ..  container:: example

            Colors repeat pitch-classes:

            >>> music_maker = baca.MusicMaker()

            >>> collection_lists = [
            ...     [[4]],
            ...     [[6, 2, 3, 5, 9, 9, 0]],
            ...     [[11]],
            ...     [[10, 7, 9, 12, 0, 5]],
            ...     ]
            >>> figures, time_signatures = [], []
            >>> for i, collections in enumerate(collection_lists):
            ...     contribution = music_maker(
            ...         'Voice 1',
            ...         collections,
            ...         baca.flags(),
            ...         )
            ...     figures.append(contribution['Voice 1'])
            ...     time_signatures.append(contribution.time_signature)
            ...
            >>> figures_ = []
            >>> for figure in figures:
            ...     figures_.extend(figure)
            ...
            >>> figures = abjad.select(figures_)

            >>> maker = baca.SegmentMaker(
            ...     color_repeat_pitch_classes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.HorizontalSpacingSpecifier(
            ...         minimum_width=abjad.Duration(1, 24),
            ...         ),
            ...     time_signatures=time_signatures,
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.rhythm(figures),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.setting(lilypond_file['Score']).auto_beaming = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                \with
                {
                    autoBeaming = ##f
                }
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 1/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/16
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 7/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 7/16
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 1/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/16
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
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
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 1]                                         %! SM4
                                        e'16
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 2]                                         %! SM4
                                        fs'16
                <BLANKLINE>
                                        d'16
                <BLANKLINE>
                                        ef'16
                <BLANKLINE>
                                        f'16
                <BLANKLINE>
                                        \once \override Accidental.color = #red
                                        \once \override Beam.color = #red
                                        \once \override Dots.color = #red
                                        \once \override NoteHead.color = #red
                                        \once \override Stem.color = #red
                                        a'16
                                        - \tweak color #red                                              %! SM14
                                        ^ \markup { @ }                                                  %! SM14
                <BLANKLINE>
                                        \once \override Accidental.color = #red
                                        \once \override Beam.color = #red
                                        \once \override Dots.color = #red
                                        \once \override NoteHead.color = #red
                                        \once \override Stem.color = #red
                                        a'16
                                        - \tweak color #red                                              %! SM14
                                        ^ \markup { @ }                                                  %! SM14
                <BLANKLINE>
                                        c'16
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 3]                                         %! SM4
                                        b'16
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 4]                                         %! SM4
                                        bf'16
                <BLANKLINE>
                                        g'16
                <BLANKLINE>
                                        a'16
                <BLANKLINE>
                                        \once \override Accidental.color = #red
                                        \once \override Beam.color = #red
                                        \once \override Dots.color = #red
                                        \once \override NoteHead.color = #red
                                        \once \override Stem.color = #red
                                        c''16
                                        - \tweak color #red                                              %! SM14
                                        ^ \markup { @ }                                                  %! SM14
                <BLANKLINE>
                                        \once \override Accidental.color = #red
                                        \once \override Beam.color = #red
                                        \once \override Dots.color = #red
                                        \once \override NoteHead.color = #red
                                        \once \override Stem.color = #red
                                        c'16
                                        - \tweak color #red                                              %! SM14
                                        ^ \markup { @ }                                                  %! SM14
                <BLANKLINE>
                                        f'16
                <BLANKLINE>
                                    }
                                }
                            }
                        }
                    >>
                >>

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._color_repeat_pitch_classes

    @property
    def do_not_check_persistence(self) -> Optional[bool]:
        r'''Is true when segment-maker does not check persistent indicators.
        '''
        return self._do_not_check_persistence

    @property
    def do_not_include_layout_ly(self) -> Optional[bool]:
        r'''Is true when segment-maker does not include layout.ly.
        '''
        return self._do_not_include_layout_ly

    @property
    def fermata_measure_staff_line_count(self) -> Optional[int]:
        r'''Gets fermata measure staff lines.
        '''
        return self._fermata_measure_staff_line_count

    @property
    def final_bar_line(self) -> U[bool, str, None]:
        r'''Gets final bar line.

        ..  container:: example

            Nonlast segment sets final bar line to ``'|'`` by default:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
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
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
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
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 1]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 2]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 3]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 4]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

            Override nonlast segment final bar line like this:

            >>> maker = baca.SegmentMaker(
            ...     final_bar_line='||',
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
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
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "||"                                                                    %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 1]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 2]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 3]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 4]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Last segment in score sets final bar line to ``'|.'`` by default:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     last_segment=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
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
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|."                                                                    %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 1]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 2]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 3]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 4]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

            Override last segment final bar line like this:

            >>> maker = baca.SegmentMaker(
            ...     final_bar_line='||',
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
            ...     )

            >>> metadata = {'segment_count': 1}
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     metadata=metadata,
            ...     )
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
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "||"                                                                    %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 1]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 2]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 3]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 4]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        '''
        return self._final_bar_line

    @property
    def final_markup(self) -> Optional[tuple]:
        r'''Gets final markup.

        ..  container:: example

            Sets final markup:

            >>> maker = baca.SegmentMaker(
            ...     final_bar_line='|.',
            ...     final_markup=(['Madison, WI'], ['October 2016']),
            ...     final_markup_extra_offset=(-9, -2),
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
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
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|."                                                                    %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context Staff = "MusicStaff"
                        {
                            \context Voice = "MusicVoice"
                            {
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 1]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 2]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 3]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 4]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    \once \override TextScript.extra-offset = #'(-9 . -2)
                                    c'8
                                    ]
                                    _ \markup {                                                          %! SCORE2
                                        \whiteout                                                        %! SCORE2
                                            \upright                                                     %! SCORE2
                                                \with-color                                              %! SCORE2
                                                    #black                                               %! SCORE2
                                                    \right-column                                        %! SCORE2
                                                        {                                                %! SCORE2
                                                            \line                                        %! SCORE2
                                                                {                                        %! SCORE2
                                                                    "Madison, WI"                        %! SCORE2
                                                                }                                        %! SCORE2
                                                            \line                                        %! SCORE2
                                                                {                                        %! SCORE2
                                                                    "October 2016"                       %! SCORE2
                                                                }                                        %! SCORE2
                                                        }                                                %! SCORE2
                                        }                                                                %! SCORE2
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        '''
        return self._final_markup

    @property
    def final_markup_extra_offset(self) -> Optional[NumberPair]:
        r'''Gets final markup extra offset.
        '''
        return self._final_markup_extra_offset

    @property
    def first_measure_number(self) -> Optional[int]:
        r'''Gets user-defined first measure number.
        '''
        return self._first_measure_number

    @property
    def first_segment(self) -> bool:
        r'''Is true when segment is first in score.
        '''
        return self._get_segment_number() == 1

    @property
    def ignore_repeat_pitch_classes(self) -> Optional[bool]:
        r'''Is true when segment ignores repeat pitch-classes.
        '''
        return self._ignore_repeat_pitch_classes

    @property
    def ignore_unpitched_notes(self) -> Optional[bool]:
        r'''Is true when segment ignores unpitched notes.

        ..  container:: example

            Ignores unpitched notes:

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
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
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
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
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 1]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 2]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 3]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 4]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Colors unpitched notes:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
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
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
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
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 1]                                             %! SM4
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    [
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 2]                                             %! SM4
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    [
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 3]                                             %! SM4
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    [
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 4]                                             %! SM4
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    [
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                <BLANKLINE>
                                    \makeBlue                                                            %! SM24
                                    c'8
                                    ]
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        '''
        return self._ignore_unpitched_notes

    @property
    def ignore_unregistered_pitches(self) -> Optional[bool]:
        r'''Is true when segment ignores unregistered pitches.

        ..  container:: example

            Ignores unregistered pitches:

                >>> music_maker = baca.MusicMaker(
                ...     baca.PitchFirstRhythmCommand(
                ...         rhythm_maker=baca.PitchFirstRhythmMaker(
                ...             acciaccatura_specifiers=[
                ...                 baca.AcciaccaturaSpecifier(),
                ...                 ],
                ...             talea=rhythmos.Talea(
                ...                 counts=[3],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     color_unregistered_pitches=True,
                ...     denominator=8,
                ...     )

            >>> collection_lists = [
            ...     [[4]],
            ...     [[6, 2, 3, 5, 9, 8, 0]],
            ...     [[11]],
            ...     [[10, 7, 9, 8, 0, 5]],
            ...     ]
            >>> figures, time_signatures = [], []
            >>> for collections in collection_lists:
            ...     contribution = music_maker('Voice 1', collections)
            ...     figures.append(contribution['Voice 1'])
            ...     time_signatures.append(contribution.time_signature)
            ...
            >>> figures_ = []
            >>> for figure in figures:
            ...     figures_.extend(figure)
            ...
            >>> figures = abjad.select(figures_)

            >>> maker = baca.SegmentMaker(
            ...     ignore_unregistered_pitches=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=time_signatures,
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.rhythm(figures),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 3/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/16
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/16
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/16
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/16
                            \override Score.BarLine.transparent = ##f                                    %! SM5
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
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 1]                                         %! SM4
                                        e'8.
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 2]                                         %! SM4
                                        \acciaccatura {
                <BLANKLINE>
                                            fs'16 [                                                      %! ACC1
                <BLANKLINE>
                                            d'16
                <BLANKLINE>
                                            ef'16
                <BLANKLINE>
                                            f'16
                <BLANKLINE>
                                            a'16
                <BLANKLINE>
                                            af'16 ]                                                      %! ACC1
                <BLANKLINE>
                                        }
                                        c'8.
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 3]                                         %! SM4
                                        b'8.
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 4]                                         %! SM4
                                        \acciaccatura {
                <BLANKLINE>
                                            bf'16 [                                                      %! ACC1
                <BLANKLINE>
                                            g'16
                <BLANKLINE>
                                            a'16
                <BLANKLINE>
                                            af'16
                <BLANKLINE>
                                            c'16 ]                                                       %! ACC1
                <BLANKLINE>
                                        }
                                        f'8.
                <BLANKLINE>
                                    }
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Colors unregistered pitches:

                >>> music_maker = baca.MusicMaker(
                ...     baca.PitchFirstRhythmCommand(
                ...         rhythm_maker=baca.PitchFirstRhythmMaker(
                ...             acciaccatura_specifiers=[
                ...                 baca.AcciaccaturaSpecifier(),
                ...                 ],
                ...             talea=rhythmos.Talea(
                ...                 counts=[3],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     color_unregistered_pitches=True,
                ...     denominator=8,
                ...     )

            >>> collection_lists = [
            ...     [[4]],
            ...     [[6, 2, 3, 5, 9, 8, 0]],
            ...     [[11]],
            ...     [[10, 7, 9, 8, 0, 5]],
            ...     ]
            >>> figures, time_signatures = [], []
            >>> for collections in collection_lists:
            ...     contribution = music_maker('Voice 1', collections)
            ...     figures.append(contribution['Voice 1'])
            ...     time_signatures.append(contribution.time_signature)
            ...
            >>> figures_ = []
            >>> for figure in figures:
            ...     figures_.extend(figure)
            ...
            >>> figures = abjad.select(figures_)

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 24)),
            ...     time_signatures=time_signatures,
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.rhythm(figures),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \context Score = "Score"
                \with
                {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                }
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \time 3/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/16
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/16
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/16
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/16
                            \override Score.BarLine.transparent = ##f                                    %! SM5
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
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 1]                                         %! SM4
                                        \makeMagenta                                                     %! SM25
                                        e'8.
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 2]                                         %! SM4
                                        \acciaccatura {
                <BLANKLINE>
                                            \makeMagenta                                                 %! SM25
                                            fs'16 [                                                      %! ACC1
                <BLANKLINE>
                                            \makeMagenta                                                 %! SM25
                                            d'16
                <BLANKLINE>
                                            \makeMagenta                                                 %! SM25
                                            ef'16
                <BLANKLINE>
                                            \makeMagenta                                                 %! SM25
                                            f'16
                <BLANKLINE>
                                            \makeMagenta                                                 %! SM25
                                            a'16
                <BLANKLINE>
                                            \makeMagenta                                                 %! SM25
                                            af'16 ]                                                      %! ACC1
                <BLANKLINE>
                                        }
                                        \makeMagenta                                                     %! SM25
                                        c'8.
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 3]                                         %! SM4
                                        \makeMagenta                                                     %! SM25
                                        b'8.
                                    }
                                }
                                {
                                    \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                        % [MusicVoice measure 4]                                         %! SM4
                                        \acciaccatura {
                <BLANKLINE>
                                            \makeMagenta                                                 %! SM25
                                            bf'16 [                                                      %! ACC1
                <BLANKLINE>
                                            \makeMagenta                                                 %! SM25
                                            g'16
                <BLANKLINE>
                                            \makeMagenta                                                 %! SM25
                                            a'16
                <BLANKLINE>
                                            \makeMagenta                                                 %! SM25
                                            af'16
                <BLANKLINE>
                                            \makeMagenta                                                 %! SM25
                                            c'16 ]                                                       %! ACC1
                <BLANKLINE>
                                        }
                                        \makeMagenta                                                     %! SM25
                                        f'8.
                <BLANKLINE>
                                    }
                                }
                            }
                        }
                    >>
                >>

        '''
        return self._ignore_unregistered_pitches

    @property
    def instruments(self) -> Optional[abjad.OrderedDict]:
        r'''Gets instruments.
        '''
        return self._instruments

    @property
    def last_segment(self) -> Optional[bool]:
        r'''Is true when composer declares segment to be last in score.
        '''
        return self._last_segment

    @property
    def manifests(self) -> abjad.OrderedDict:
        r'''Gets manifests.
        '''
        manifests = abjad.OrderedDict()
        manifests['abjad.Instrument'] = self.instruments
        manifests['abjad.MarginMarkup'] = self.margin_markups
        manifests['abjad.MetronomeMark'] = self.metronome_marks
        return manifests

    @property
    def margin_markups(self) -> Optional[abjad.OrderedDict]:
        r'''Gets margin markups.
        '''
        return self._margin_markups

    @property
    def measure_count(self) -> int:
        r'''Gets measure count.
        '''
        if self.time_signatures:
            return len(self.time_signatures)
        return 0

    @property
    def measures_per_stage(self) -> List[int]:
        r'''Gets measures per stage.
        '''
        if self._measures_per_stage is None:
            time_signatures = self.time_signatures or []
            return [len(time_signatures)]
        return self._measures_per_stage

    @property
    def metadata(self) -> abjad.OrderedDict:
        r'''Gets segment metadata.

        ..  container:: example

            >>> metadata = {}
            >>> metadata['persistent_indicators'] = {}
            >>> metadata['persistent_indicators']['MusicStaff'] = [
            ...     abjad.Momento(
            ...         context='MusicVoice',
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
            ...     )

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
                            \bar ""                                                                      %! SM2:+SEGMENT:EMPTY_START_BAR
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
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
                                \clef "alto"                                                             %! SM8:REAPPLIED_CLEF:SM37
                                \once \override Staff.Clef.color = #(x11-color 'green4)                  %! SM6:REAPPLIED_CLEF_COLOR:SM37
                            %@% \override Staff.Clef.color = ##f                                         %! SM7:REAPPLIED_CLEF_COLOR_CANCELLATION:SM37
                                \set Staff.forceClef = ##t                                               %! SM8:REAPPLIED_CLEF:SM33:SM37
                                R1 * 1/2
                                \override Staff.Clef.color = #(x11-color 'OliveDrab)                     %! SM6:REAPPLIED_CLEF_REDRAW_COLOR:SM37
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                R1 * 3/8
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                R1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                R1 * 3/8
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            >>> abjad.f(maker.metadata, strict=89)
            abjad.OrderedDict(
                [
                    (
                        'alive_during_segment',
                        [
                            'Score',
                            'GlobalContext',
                            'GlobalSkips',
                            'MusicContext',
                            'MusicStaff',
                            'MusicVoice',
                            ],
                        ),
                    ('first_measure_number', 1),
                    ('last_measure_number', 4),
                    (
                        'persistent_indicators',
                        abjad.OrderedDict(
                            [
                                (
                                    'MusicStaff',
                                    [
                                        abjad.Momento(
                                            context='MusicVoice',
                                            prototype='abjad.Clef',
                                            value='alto',
                                            ),
                                        ],
                                    ),
                                (
                                    'Score',
                                    [
                                        abjad.Momento(
                                            context='GlobalSkips',
                                            prototype='abjad.TimeSignature',
                                            value='3/8',
                                            ),
                                        ],
                                    ),
                                ]
                            ),
                        ),
                    ('segment_number', 2),
                    (
                        'sounds_during_segment',
                        abjad.OrderedDict(
                            [
                                ('MusicVoice', False),
                                ]
                            ),
                        ),
                    (
                        'time_signatures',
                        ['4/8', '3/8', '4/8', '3/8'],
                        ),
                    ]
                )

        '''
        return self._metadata

    @property
    def metronome_mark_measure_map(self) -> Optional[MetronomeMarkMeasureMap]:
        r'''Gets metronome mark measure map.

        ..  container:: example

            With metronome mark measure map:

            >>> metronome_marks = abjad.MetronomeMarkDictionary()
            >>> metronome_marks['90'] = abjad.MetronomeMark((1, 4), 90)
            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     metronome_mark_measure_map=baca.MetronomeMarkMeasureMap([
            ...         (1, metronome_marks['90']),
            ...         ]),
            ...     metronome_marks=metronome_marks,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
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
                        %@% \once \override TextSpanner.bound-details.left.text =                        %! SM27:EXPLICIT_METRONOME_MARK:SM30
                        %@% \markup {                                                                    %! SM27:EXPLICIT_METRONOME_MARK:SM30
                        %@%     \fontsize                                                                %! SM27:EXPLICIT_METRONOME_MARK:SM30
                        %@%         #-6                                                                  %! SM27:EXPLICIT_METRONOME_MARK:SM30
                        %@%         \general-align                                                       %! SM27:EXPLICIT_METRONOME_MARK:SM30
                        %@%             #Y                                                               %! SM27:EXPLICIT_METRONOME_MARK:SM30
                        %@%             #DOWN                                                            %! SM27:EXPLICIT_METRONOME_MARK:SM30
                        %@%             \note-by-number                                                  %! SM27:EXPLICIT_METRONOME_MARK:SM30
                        %@%                 #2                                                           %! SM27:EXPLICIT_METRONOME_MARK:SM30
                        %@%                 #0                                                           %! SM27:EXPLICIT_METRONOME_MARK:SM30
                        %@%                 #1.5                                                         %! SM27:EXPLICIT_METRONOME_MARK:SM30
                        %@%     \upright                                                                 %! SM27:EXPLICIT_METRONOME_MARK:SM30
                        %@%         {                                                                    %! SM27:EXPLICIT_METRONOME_MARK:SM30
                        %@%             =                                                                %! SM27:EXPLICIT_METRONOME_MARK:SM30
                        %@%             90                                                               %! SM27:EXPLICIT_METRONOME_MARK:SM30
                        %@%         }                                                                    %! SM27:EXPLICIT_METRONOME_MARK:SM30
                        %@%     \hspace                                                                  %! SM27:EXPLICIT_METRONOME_MARK:SM30
                        %@%         #1                                                                   %! SM27:EXPLICIT_METRONOME_MARK:SM30
                        %@%     }                                                                        %! SM27:EXPLICIT_METRONOME_MARK:SM30 %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.Y-extent = ##f                                   %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left-broken.text =
                            \markup {
                                \null
                                }                                                                        %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.left.text =                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                            \markup {                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                \with-color                                                              %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                    #(x11-color 'blue)                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                    {                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                        \fontsize                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                            #-6                                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                            \general-align                                               %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                                #Y                                                       %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                                #DOWN                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                                \note-by-number                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                                    #2                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                                    #0                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                                    #1.5                                                 %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                        \upright                                                         %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                            {                                                            %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                                =                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                                90                                                       %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                            }                                                            %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                        \hspace                                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                            #1                                                           %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                    }                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                }                                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30 %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                            \once \override TextSpanner.dash-period = 0                                  %! SM29:METRONOME_MARK_SPANNER
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                            \startTextSpan                                                               %! SM29:METRONOME_MARK_SPANNER
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \stopTextSpan                                                                %! SM29:METRONOME_MARK_SPANNER
                            \override Score.BarLine.transparent = ##f                                    %! SM5
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
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 1]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 2]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 3]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 4]                                             %! SM4
                                    c'8
                                    [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                                    ]
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        '''
        return self._metronome_mark_measure_map

    @property
    def metronome_mark_spanner_right_broken(self) -> Optional[bool]:
        r'''Is true when metronome mark spanner is right-broken.
        '''
        return self._metronome_mark_spanner_right_broken

    @property
    def metronome_mark_stem_height(self) -> Optional[Number]:
        r'''Gets metronome mark stem height.
        '''
        return self._metronome_mark_stem_height

    @property
    def metronome_marks(self) -> abjad.OrderedDict:
        r'''Gets metronome marks.
        '''
        return self._metronome_marks

    @property
    def midi(self) -> Optional[bool]:
        r'''Is true when segment-maker outputs MIDI.
        '''
        return self._midi

    @property
    def previous_metadata(self) -> abjad.OrderedDict:
        r'''Gets previous segment metadata.
        '''
        return self._previous_metadata

    @property
    def print_timings(self) -> Optional[bool]:
        r'''Is true when segment prints interpreter timings.
        '''
        return self._print_timings

    @property
    def range_checker(self) -> Optional[abjad.PitchRange]:
        r'''Gets range checker.
        '''
        return self._range_checker

    @property
    def rehearsal_mark(self) -> Optional[str]:
        r'''Gets rehearsal mark.
        '''
        return self._rehearsal_mark

    @property
    def score_template(self) -> Optional[abjad.ScoreTemplate]:
        r'''Gets score template.

        ..  container:: example

            Gets score template:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     )

            >>> maker.score_template
            SingleStaffScoreTemplate()

        '''
        return self._score_template

    @property
    def skip_wellformedness_checks(self) -> Optional[bool]:
        r'''Is true when segment skips wellformedness checks.
        '''
        return self._skip_wellformedness_checks

    @property
    def skips_instead_of_rests(self) -> Optional[bool]:
        r'''Is true when segment fills empty measures with skips.

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
                \context Score = "Score"
                <<
                    \context GlobalContext = "GlobalContext"
                    <<
                        \context GlobalSkips = "GlobalSkips"
                        {
                <BLANKLINE>
                            % [GlobalSkips measure 1]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
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
                                R1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                R1 * 3/8
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                R1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                R1 * 3/8
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Fills empty measures with skips:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     skips_instead_of_rests=True,
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
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
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
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
                                s1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                s1 * 3/8
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                s1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                s1 * 3/8
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        '''
        return self._skips_instead_of_rests

    @property
    def spacing(self) -> Optional[HorizontalSpacingSpecifier]:
        r'''Gets spacing.
        '''
        return self._spacing

    @property
    def stage_count(self) -> int:
        r'''Gets stage count.

        Defined equal to 1 when `self.measures_per_stage` is none.
        '''
        if self.measures_per_stage is None:
            return 1
        return len(self.measures_per_stage)

    @property
    def time_signatures(self) -> List[abjad.TimeSignature]:
        r'''Gets time signatures.
        '''
        return self._time_signatures

    @property
    def transpose_score(self) -> Optional[bool]:
        r'''Is true when segment transposes score.

        ..  container:: example

            Transposes score:

            >>> instruments = abjad.InstrumentDictionary()
            >>> instruments['clarinet'] = abjad.ClarinetInBFlat()
            >>> maker = baca.SegmentMaker(
            ...     instruments=instruments,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     transpose_score=True,
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.instrument(instruments['clarinet']),
            ...     baca.make_even_runs(),
            ...     baca.pitches('E4 F4'),
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
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
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
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 1]                                             %! SM4
                                    \set Staff.instrumentName = \markup { "Clarinet in B-flat" }         %! SM8:EXPLICIT_INSTRUMENT:IC
                                    \set Staff.shortInstrumentName = \markup { "Cl. in B-flat" }         %! SM8:EXPLICIT_INSTRUMENT:IC
                                    \once \override Staff.InstrumentName.color = #(x11-color 'blue)      %! SM6:EXPLICIT_INSTRUMENT_COLOR:IC
                                    fs'8
                                    [
                                    ^ \markup {                                                          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        \with-color                                                      %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                            #(x11-color 'blue)                                           %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                            (“clarinet”)                                                 %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        }                                                                %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)    %! SM6:REDRAWN_EXPLICIT_INSTRUMENT_COLOR:IC
                                    \set Staff.instrumentName = \markup { "Clarinet in B-flat" }         %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                                    \set Staff.shortInstrumentName = \markup { "Cl. in B-flat" }         %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                <BLANKLINE>
                                    g'8
                <BLANKLINE>
                                    fs'8
                <BLANKLINE>
                                    g'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 2]                                             %! SM4
                                    fs'8
                                    [
                <BLANKLINE>
                                    g'8
                <BLANKLINE>
                                    fs'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 3]                                             %! SM4
                                    g'8
                                    [
                <BLANKLINE>
                                    fs'8
                <BLANKLINE>
                                    g'8
                <BLANKLINE>
                                    fs'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 4]                                             %! SM4
                                    g'8
                                    [
                <BLANKLINE>
                                    fs'8
                <BLANKLINE>
                                    g'8
                                    ]
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Does not transpose score:

            >>> instruments = abjad.InstrumentDictionary()
            >>> instruments['clarinet'] = abjad.ClarinetInBFlat()
            >>> maker = baca.SegmentMaker(
            ...     instruments=instruments,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     transpose_score=False,
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.instrument(instruments['clarinet']),
            ...     baca.make_even_runs(),
            ...     baca.pitches('E4 F4'),
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
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
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
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 1]                                             %! SM4
                                    \set Staff.instrumentName = \markup { "Clarinet in B-flat" }         %! SM8:EXPLICIT_INSTRUMENT:IC
                                    \set Staff.shortInstrumentName = \markup { "Cl. in B-flat" }         %! SM8:EXPLICIT_INSTRUMENT:IC
                                    \once \override Staff.InstrumentName.color = #(x11-color 'blue)      %! SM6:EXPLICIT_INSTRUMENT_COLOR:IC
                                    e'8
                                    [
                                    ^ \markup {                                                          %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        \with-color                                                      %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                            #(x11-color 'blue)                                           %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                            (“clarinet”)                                                 %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                        }                                                                %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)    %! SM6:REDRAWN_EXPLICIT_INSTRUMENT_COLOR:IC
                                    \set Staff.instrumentName = \markup { "Clarinet in B-flat" }         %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                                    \set Staff.shortInstrumentName = \markup { "Cl. in B-flat" }         %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                <BLANKLINE>
                                    f'8
                <BLANKLINE>
                                    e'8
                <BLANKLINE>
                                    f'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 2]                                             %! SM4
                                    e'8
                                    [
                <BLANKLINE>
                                    f'8
                <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 3]                                             %! SM4
                                    f'8
                                    [
                <BLANKLINE>
                                    e'8
                <BLANKLINE>
                                    f'8
                <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 4]                                             %! SM4
                                    f'8
                                    [
                <BLANKLINE>
                                    e'8
                <BLANKLINE>
                                    f'8
                                    ]
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        '''
        return self._transpose_score

    @property
    def validate_measure_count(self) -> Optional[int]:
        r'''Gets validate measure count.
        '''
        return self._validate_measure_count
    
    @property
    def validate_stage_count(self) -> Optional[int]:
        r'''Gets validate stage count.
        '''
        return self._validate_stage_count

    @property
    def wrappers(self) -> List[CommandWrapper]:
        r'''Gets wrappers.
        '''
        return self._wrappers

    ### PUBLIC METHODS ###

    def copy_rhythm(self, source, target, **keywords):
        r'''Copies rhythm.

        Gets rhythm command defined at `source` scope start.

        Makes new rhythm command for `target` scope with optional `keywords`.

        Returns none.
        '''
        assert isinstance(source, baca.Scope)
        assert isinstance(target, baca.Scope)
        for wrapper in self.wrappers:
            if not isinstance(wrapper.command, baca.RhythmCommand):
                continue
            if wrapper.scope.voice_name != source.voice_name:
                continue
            assert isinstance(wrapper.scope.stages, tuple)
            start = wrapper.scope.stages[0]
            stop = wrapper.scope.stages[1] + 1
            stages = range(start, stop)
            if source.stages[0] in stages:
                break
        else:
            raise Exception(f'no {voice_name!r} rhythm command for {stage}.')
        assert isinstance(wrapper, baca.CommandWrapper)
        assert isinstance(wrapper.command, baca.RhythmCommand)
        command = abjad.new(wrapper.command, **keywords)
        wrapper = baca.CommandWrapper(command, target)
        self.wrappers.append(wrapper)

    def run(
        self,
        deactivate: List[str] = None,
        environment: str = None,
        metadata: abjad.OrderedDict = None,
        midi: bool = None,
        previous_metadata: abjad.OrderedDict = None,
        remove: List[str] = None,
        segment_directory: abjad.Path = None,
        ) -> abjad.LilyPondFile:
        r'''Runs segment-maker.

        :param environment: leave set to none to render segments in real score.
            Set to `'docs'` for API examples.
            Set to `'external'` to debug API examples in an external file.

        '''
        self._environment: Optional[str] = environment
        self._metadata: abjad.OrderedDict = abjad.OrderedDict(metadata)
        self._midi: Optional[bool] = midi
        self._previous_metadata: Optional[
            abjad.OrderedDict] = abjad.OrderedDict(previous_metadata)
        self._segment_directory: Optional[abjad.Path] = segment_directory
        self._make_score()
        self._make_lilypond_file()
        self._make_global_skips()
        self._label_measure_indices()
        self._label_stage_numbers()
        self._call_rhythm_commands()
        self._populate_offset_to_measure_number()
        self._extend_beams()
        self._annotate_sounds_during()
        self._attach_first_segment_score_template_defaults()
        self._reapply_persistent_indicators()
        self._attach_first_appearance_score_template_defaults()
        self._apply_spacing()
        self._call_commands()
        self._shorten_long_repeat_ties()
        self._categorize_uncategorized_persistent_wrappers()
        self._label_clock_time()
        self._transpose_score_()
        self._attach_rehearsal_mark()
        self._add_final_bar_line()
        self._add_final_markup()
        self._color_unregistered_pitches()
        self._color_unpitched_notes()
        self._check_wellformedness()
        self._check_range()
        self._check_persistent_indicators()
        self._color_repeat_pitch_classes_()
        self._color_octaves_()
        self._remove_redundant_time_signatures()
        self._whitespace_leaves()
        self._comment_measure_numbers()
        self._apply_breaks()
        self._style_fermata_measures()
        self._shift_clefs_into_fermata_measures()
        self._deactivate_tags(deactivate or [])
        self._remove_tags(remove)
        self._add_container_identifiers()
        self._check_all_music_in_part_containers()
        self._make_lilypond_align_above_context_settings()
        self._collect_metadata()
        return self._lilypond_file
