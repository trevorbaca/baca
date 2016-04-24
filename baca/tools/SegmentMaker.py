# -*- encoding: utf-8 -*-
import copy
import os
import time
import baca
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import expressiontools
from abjad.tools import indicatortools
from abjad.tools import instrumenttools
from abjad.tools import lilypondfiletools
from abjad.tools import markuptools
from abjad.tools import mathtools
from abjad.tools import rhythmmakertools
from abjad.tools import scoretools
from abjad.tools import selectiontools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools import templatetools
from abjad.tools import timespantools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import detach
from abjad.tools.topleveltools import inspect_
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import new
from abjad.tools.topleveltools import select
from abjad.tools.topleveltools import set_
from experimental.tools import makertools


class SegmentMaker(makertools.SegmentMaker):
    r'''Segment-maker.

    ::

        >>> import baca

    ..  container:: example

        **Example 1.** With empty input:

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> score = lilypond_file.score_block.items[0]
            >>> f(score)
            \context Score = "Score" <<
                \tag violin
                \context TimeSignatureContext = "Time Signature Context" <<
                    \context TimeSignatureContextMultimeasureRests = "Time Signature Context Multimeasure Rests" {
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                    }
                    \context TimeSignatureContextSkips = "Time Signature Context Skips" {
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            R1 * 1/2
                            R1 * 3/8
                            R1 * 1/2
                            R1 * 3/8
                            \bar "|"
                        }
                    }
                >>
            >>

    ..  container:: example

        **Example 2.** With notes:

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.tools.stages(1)),
            ...     baca.rhythm.make_messiaen_note_rhythm_specifier(),
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> score = lilypond_file.score_block.items[0]
            >>> f(score)
            \context Score = "Score" <<
                \tag violin
                \context TimeSignatureContext = "Time Signature Context" <<
                    \context TimeSignatureContextMultimeasureRests = "Time Signature Context Multimeasure Rests" {
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                    }
                    \context TimeSignatureContextSkips = "Time Signature Context Skips" {
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            c'2
                            c'4.
                            c'2
                            c'4.
                            \bar "|"
                        }
                    }
                >>
            >>

    ..  container:: example

        **Example 3.** Labels logical ties:

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.tools.stages(1)),
            ...     [
            ...         baca.rhythm.make_messiaen_note_rhythm_specifier(),
            ...         label().with_indices(),
            ...         ],
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> score = lilypond_file.score_block.items[0]
            >>> f(score)
            \context Score = "Score" <<
                \tag violin
                \context TimeSignatureContext = "Time Signature Context" <<
                    \context TimeSignatureContextMultimeasureRests = "Time Signature Context Multimeasure Rests" {
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                    }
                    \context TimeSignatureContextSkips = "Time Signature Context Skips" {
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            c'2
                                ^ \markup {
                                    \small
                                        0
                                    }
                            c'4.
                                ^ \markup {
                                    \small
                                        1
                                    }
                            c'2
                                ^ \markup {
                                    \small
                                        2
                                    }
                            c'4.
                                ^ \markup {
                                    \small
                                        3
                                    }
                            \bar "|"
                        }
                    }
                >>
            >>

    '''

    ### CLASS ATTRIBUTES ###

    __documentation_section__ = 'Segment-maker components'

    __slots__ = (
        '_cached_leaves_with_rests',
        '_cached_leaves_without_rests',
        '_cached_score_template_start_clefs',
        '_cached_score_template_start_instruments',
        '_fermata_start_offsets',
        '_final_barline',
        '_final_markup',
        '_final_markup_extra_offset',
        '_label_clock_time',
        '_label_stage_numbers',
        '_measures_per_stage',
        '_print_segment_duration',
        '_print_timings',
        '_rehearsal_letter',
        '_scoped_specifiers',
        '_score',
        '_score_package',
        '_score_template',
        '_spacing_map',
        '_spacing_specifier',
        '_stages',
        '_tempo_specifier',
        '_time_signatures',
        '_transpose_score',
        '_volta_specifier',
        )

    _string_trio_stylesheet_path = os.path.join(
        '..',
        '..',
        '..',
        '..',
        'source',
        '_stylesheets',
        'string-trio-stylesheet.ily',
        )

    _score_package_stylesheet_path = os.path.join(
        '..', '..', 'stylesheets', 'stylesheet.ily',
        )

    _score_package_nonfirst_stylesheet_path = os.path.join(
        '..', '..', 'stylesheets', 'nonfirst-segment.ily',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        final_barline=None,
        final_markup=None,
        final_markup_extra_offset=None,
        label_clock_time=None,
        label_stage_numbers=None,
        measures_per_stage=None,
        print_segment_duration=None,
        print_timings=None,
        rehearsal_letter=None,
        score_package=None,
        score_template=None,
        spacing_map=None,
        spacing_specifier=None,
        tempo_specifier=None,
        time_signatures=None,
        transpose_score=None,
        volta_specifier=None,
        ):
        superclass = super(SegmentMaker, self)
        superclass.__init__()
        self._cached_leaves_with_rests = None
        self._cached_leaves_without_rests = None
        self._fermata_start_offsets = []
        self._final_barline = final_barline
        if final_markup is not None:
            assert isinstance(final_markup, markuptools.Markup)
        self._final_markup = final_markup
        if final_markup_extra_offset is not None:
            assert isinstance(final_markup_extra_offset, tuple)
        self._final_markup_extra_offset = final_markup_extra_offset
        assert isinstance(label_clock_time, (bool, type(None)))
        self._label_clock_time = label_clock_time
        assert isinstance(label_stage_numbers, (bool, type(None)))
        self._label_stage_numbers = label_stage_numbers
        self._measures_per_stage = measures_per_stage
        self._print_segment_duration = print_segment_duration
        self._print_timings = print_timings
        self._rehearsal_letter = rehearsal_letter
        self._scoped_specifiers = []
        self._initialize_time_signatures(time_signatures)
        self._score_package = score_package
        if score_template is not None:
            assert isinstance(score_template, baca.tools.ScoreTemplate)
        self._score_template = score_template
        self._spacing_map = spacing_map
        if spacing_specifier is not None:
            assert isinstance(spacing_specifier, baca.tools.SpacingSpecifier)
        self._spacing_specifier = spacing_specifier
        self._tempo_specifier = tempo_specifier
        if transpose_score is not None:
            transpose_score = bool(transpose_score)
        self._transpose_score = transpose_score
        self._volta_specifier = volta_specifier

    ### SPECIAL METHODS ###

    def __call__(
        self, 
        is_doc_example=None,
        segment_metadata=None,
        previous_segment_metadata=None,
        ):
        r'''Calls segment-maker.

        Returns LilyPond file and segment metadata.
        '''
        self._segment_metadata = segment_metadata or \
            datastructuretools.TypedOrderedDict()
        self._previous_segment_metadata = previous_segment_metadata or \
            datastructuretools.TypedOrderedDict()
        self._make_score()
        self._remove_score_template_start_instruments()
        self._remove_score_template_start_clefs()
        self._make_lilypond_file(is_doc_example=is_doc_example)
        self._populate_time_signature_context()
        self._label_stage_numbers_()
        self._interpret_rhythm_specifiers()
        #self._hide_fermata_measure_staff_lines()
        self._interpret_scoped_specifiers()
        self._shorten_long_repeat_ties()
        self._attach_first_segment_default_instruments()
        self._attach_first_segment_default_clefs()
        self._apply_previous_segment_end_settings()
        self._apply_spacing_specifier()
        self._make_volta_containers()
        self._label_clock_time_()
        #self._move_instruments_from_notes_back_to_rests()
        self._label_instrument_changes()
        self._transpose_instruments()
        self._attach_rehearsal_mark()
        self._add_final_barline()
        self._add_final_markup()
        self._check_well_formedness()
        self._update_segment_metadata()
        self._print_segment_duration_()
        return self.lilypond_file, self._segment_metadata

    ### PRIVATE PROPERTIES ###

    @property
    def _contexts_with_instrument_names(self):
        return list(self._cached_score_template_start_instruments.keys())

    ### PRIVATE METHODS ###

    def _add_final_barline(self):
        if isinstance(self.final_barline, str):
            abbreviation = self.final_barline
        else:
            abbreviation = '|'
            if self._is_last_segment():
                abbreviation = '|.'
        self._score.add_final_bar_line(
            abbreviation=abbreviation, 
            to_each_voice=True,
            )

    def _add_final_markup(self):
        if self.final_markup is None:
            return
        self._score.add_final_markup(
            self.final_markup,
            extra_offset=self.final_markup_extra_offset,
            )

    def _apply_first_and_last_ties(self, voice):
        dummy_tie = spannertools.Tie()
        for current_leaf in iterate(voice).by_leaf():
            if not dummy_tie._attachment_test(current_leaf):
                continue
            if inspect_(current_leaf).has_indicator('tie to me'):
                previous_leaf = inspect_(current_leaf).get_leaf(-1)
                if dummy_tie._attachment_test(previous_leaf):
                    previous_logical_tie = inspect_(previous_leaf).get_logical_tie()
                    if current_leaf not in previous_logical_tie:
                        current_logical_tie = inspect_(current_leaf).get_logical_tie()
                        leaves = previous_logical_tie + current_logical_tie
                        detach(spannertools.Tie, previous_leaf)
                        detach(spannertools.Tie, current_leaf)
                        inspector = inspect_(current_leaf)
                        use_messiaen_style_ties = inspector.has_indicator(
                            'use messiaen style ties')
                        tie = spannertools.Tie(
                            use_messiaen_style_ties=use_messiaen_style_ties)
                        attach(tie, leaves)
                detach('tie to me', current_leaf)
            if inspect_(current_leaf).has_indicator('tie from me'):
                next_leaf = inspect_(current_leaf).get_leaf(1)
                if spannertools.Tie._attachment_test(next_leaf):
                    current_logical_tie = inspect_(current_leaf).get_logical_tie()
                    if next_leaf not in current_logical_tie:
                        next_logical_tie = inspect_(next_leaf).get_logical_tie()
                        leaves = current_logical_tie + next_logical_tie
                        detach(spannertools.Tie, current_leaf)
                        detach(spannertools.Tie, next_leaf)
                        inspector = inspect_(current_leaf)
                        use_messiaen_style_ties = inspector.has_indicator(
                            'use messiaen style ties')
                        tie = spannertools.Tie(
                            use_messiaen_style_ties=use_messiaen_style_ties)
                        attach(tie, leaves)
                detach('tie from me', current_leaf)

    def _apply_previous_segment_end_settings(self):
        if self._is_first_segment():
            return
        if self.score_package is None:
            return
        if not self._previous_segment_metadata:
            message = 'can not find previous metadata before segment {}.'
            message = message.format(self._get_segment_identifier())
            raise Exception(message)
            return
        key = 'end_instruments_by_context'
        previous_instruments = self._previous_segment_metadata.get(key)
        if not previous_instruments:
            message = 'can not find previous instruments before segment {}.'
            message = message.format(self._get_segment_identifier())
            raise Exception(message)
            return
        for context in iterate(self._score).by_class(scoretools.Context):
            previous_instrument_name = previous_instruments.get(context.name)
            if not previous_instrument_name:
                continue
            first_leaf = inspect_(context).get_leaf(0)
            prototype = instrumenttools.Instrument
            instrument = inspect_(first_leaf).get_effective(prototype)
            if instrument is not None:
                continue
            previous_instrument = self._get_instrument_by_name(
                previous_instrument_name, 
                self.score_package.materials,
                )
            if previous_instrument is None:
                message = 'can not previous instrument for {}.'
                message = message.format(context.name)
                raise Exception(message)
            copied_previous_instrument = new(previous_instrument)
            copied_previous_instrument._default_scope = context.context_name
            attach(copied_previous_instrument, context)
        key = 'end_clefs_by_staff'
        previous_clefs = self._previous_segment_metadata.get(key)
        if not previous_clefs:
            message = 'can not find previous clefs before segment {}.'
            message = message.format(self._get_segment_identifier())
            raise Exception(message)
            return
        for staff in iterate(self._score).by_class(scoretools.Staff):
            previous_clef_name = previous_clefs.get(staff.name)
            if not previous_clef_name:
                continue
            first_leaf = inspect_(staff).get_leaf(0)
            prototype = indicatortools.Clef
            clef = inspect_(first_leaf).get_effective(prototype)
            if clef is not None:
                continue
            clef = indicatortools.Clef(previous_clef_name)
            attach(clef, staff)

    def _apply_spacing_specifier(self):
        if self.spacing_specifier is None:
            return
        self.spacing_specifier(self)

    def _assert_valid_stage_number(self, stage_number):
        if not 1 <= stage_number <= self.stage_count:
            message = 'stage number {} must be between {} and {}.'
            message = message.format(stage_number, 1, self.stage_count)
            raise Exception(message)

    def _attach_fermatas(self):
        if not self.tempo_specifier:
            return
        context = self._score['Time Signature Context Multimeasure Rests']
        directive_prototype = (
            indicatortools.Fermata,
            indicatortools.BreathMark,
            )
        rest_prototype = scoretools.MultimeasureRest
        for stage_number, directive in self.tempo_specifier:
            if not isinstance(directive, directive_prototype):
                continue
            assert 0 < stage_number <= self.stage_count
            result = self._stage_number_to_measure_indices(stage_number)
            start_measure_index, stop_measure_index = result
            start_measure = context[start_measure_index]
            assert isinstance(start_measure, scoretools.Measure), start_measure
            start_skip = start_measure[0]
            assert isinstance(start_skip, rest_prototype), start_skip
            fermata_y_offset = None
            if isinstance(directive, indicatortools.Fermata):
                if directive.command == 'shortfermata':
                    string = 'scripts.ushortfermata'
                    fermata_y_offset = -7
                elif directive.command == 'fermata':
                    string = 'scripts.ufermata'
                    fermata_y_offset = -7
                elif directive.command == 'longfermata':
                    string = 'scripts.ulongfermata'
                    fermata_y_offset = -7
                elif directive.command == 'verylongfermata':
                    string = 'scripts.uverylongfermata'
                    fermata_y_offset = -7
                else:
                    message = 'unknown fermata command: {!r}.'
                    message = message.format(directive.command)
                    raise Exception(message)
                directive = markuptools.Markup.musicglyph(string)
            else:
                directive = new(directive)
            attach(directive, start_skip)
            if fermata_y_offset is not None:
                grob_proxy = override(start_skip).multi_measure_rest_text
                grob_proxy.extra_offset = (0, fermata_y_offset)
            proxy = override(start_skip)
            proxy.score.multi_measure_rest.transparent = True
            override(start_skip).score.time_signature.stencil = False
            attach('fermata measure', start_skip)
            start_offset = inspect_(start_skip).get_timespan().start_offset
            self._fermata_start_offsets.append(start_offset)

    def _attach_first_segment_default_clefs(self):
        if not self._is_first_segment():
            return
        cached_clefs = self._cached_score_template_start_clefs
        previous_clefs = self._previous_segment_metadata.get(
            'end_clefs_by_staff', datastructuretools.TypedOrderedDict())
        prototype = indicatortools.Clef
        for staff in iterate(self._score).by_class(scoretools.Staff):
            if inspect_(staff).has_indicator(prototype):
                continue
            first_leaf = inspect_(staff).get_leaf(0)
            if (first_leaf is None or
                not inspect_(first_leaf).has_indicator(prototype)):
                clef_name = previous_clefs.get(staff.name)
                if clef_name is None:
                    clef_name = cached_clefs.get(staff.name)
                # TODO: remove if-clause
                if clef_name is not None:
                    clef = indicatortools.Clef(clef_name)
                    attach(clef, staff)

    def _attach_first_segment_default_instruments(self):
        if not self._is_first_segment():
            return
        if self.score_package is None:
            return
        cached_instruments = self._cached_score_template_start_instruments
        previous_instruments = self._previous_segment_metadata.get(
            'end_instruments_by_context',
            datastructuretools.TypedOrderedDict(),
            )
        prototype = instrumenttools.Instrument
        contexts_with_instrument_names = self._contexts_with_instrument_names
        for context in iterate(self._score).by_class(scoretools.Context):
            if context.name not in contexts_with_instrument_names:
                continue
            if inspect_(context).has_indicator(prototype):
                continue
            first_leaf = inspect_(context).get_leaf(0)
            if (first_leaf is not None and 
                inspect_(first_leaf).has_indicator(prototype)):
                continue
            if (first_leaf is None or
                not inspect_(first_leaf).has_indicator(prototype)):
                instrument_name = previous_instruments.get(context.name)
                if instrument_name is None:
                    instrument_name = cached_instruments.get(context.name)
                instrument = self.score_package.materials.instruments[
                    instrument_name]
                instrument = copy.deepcopy(instrument)
                instrument._default_scope = context.context_name
                attach(instrument, context)

    def _attach_rehearsal_mark(self):
        if self.rehearsal_letter == '':
            return
        letter_number = None
        if self.rehearsal_letter is None:
            segment_number = self._get_segment_number()
            letter_number = segment_number - 1
        elif isinstance(self.rehearsal_letter, str):
            assert len(self.rehearsal_letter) == 1
            rehearsal_letter = self.rehearsal_letter.upper()
            letter_number = ord(rehearsal_letter) - ord('A') + 1
        if letter_number == 0:
            return
        rehearsal_mark = indicatortools.RehearsalMark(number=letter_number)
        voice = self._score['Time Signature Context Skips']
        first_leaf = inspect_(voice).get_leaf(0)
        attach(rehearsal_mark, first_leaf)

    def _attach_tempo_indicators(self):
        if not self.tempo_specifier:
            return
        context = self._score['Time Signature Context Skips']
        # TODO: adjust TempoSpanner to make this possible:
        #attach(spannertools.TempoSpanner(), context)
        skips = list(iterate(context).by_class(scoretools.Leaf))
        left_broken_text = markuptools.Markup().null()
        left_broken_text._direction = None
        tempo_spanner = spannertools.TempoSpanner(
            left_broken_padding=0,
            left_broken_text=left_broken_text,
            start_with_parenthesized_tempo=False,
            )
        attach(tempo_spanner, skips)
        for stage_number, directive in self.tempo_specifier:
            self._assert_valid_stage_number(stage_number)
            result = self._stage_number_to_measure_indices(stage_number)
            start_measure_index, stop_measure_index = result
            start_measure = context[start_measure_index]
            assert isinstance(start_measure, scoretools.Measure), start_measure
            start_skip = start_measure[0]
            prototype = (scoretools.Skip, scoretools.MultimeasureRest)
            assert isinstance(start_skip, prototype), start_skip
            # TODO: adjust TempoSpanner to make measure attachment work
            attach(directive, start_skip, is_annotation=True)

    def _check_well_formedness(self):
        score_block = self.lilypond_file['score']
        score = score_block['Score']
        if not inspect_(score).is_well_formed():
            string = inspect_(score).tabulate_well_formedness_violations()
            raise Exception(string)

    def _compound_scope_to_logical_ties(
        self, 
        compound_scope,
        include_rests=False,
        ):
        timespan_map, timespans = [], []
        for scope in compound_scope.simple_scopes:
            result = self._get_stage_numbers(scope.stages)
            start_stage, stop_stage = result
            offsets = self._get_offsets(start_stage, stop_stage)
            timespan = timespantools.Timespan(*offsets)
            timespan_map.append((scope.voice_name, timespan))
            timespans.append(timespan)
        compound_scope._timespan_map = timespan_map
        voice_names = [_[0] for _ in timespan_map]
        logical_ties = []
        leaves = self._get_cached_leaves(include_rests=include_rests)
        for note in leaves:
            if note in compound_scope:
                logical_tie = inspect_(note).get_logical_tie()
                if logical_tie.head is note:
                    logical_ties.append(logical_tie)
        start_offset = min(_.start_offset for _ in timespans)
        stop_offset = max(_.stop_offset for _ in timespans)
        timespan = timespantools.Timespan(start_offset, stop_offset)
        return logical_ties, timespan

    def _compound_scope_to_topmost_components(self, compound_scope):
        timespan_map, timespans = [], []
        for scope in compound_scope.simple_scopes:
            result = self._get_stage_numbers(scope.stages)
            start_stage, stop_stage = result
            offsets = self._get_offsets(start_stage, stop_stage)
            timespan = timespantools.Timespan(*offsets)
            timespan_map.append((scope.voice_name, timespan))
            timespans.append(timespan)
        compound_scope._timespan_map = timespan_map
        voice_names = [_[0] for _ in timespan_map]
        topmost_components = []
        for voice in iterate(self._score).by_class(scoretools.Voice):
            if 'Context' in voice.__class__.__name__:
                continue
            result = iterate(voice).by_topmost_logical_ties_and_components()
            for expr in result:
                if isinstance(expr, selectiontools.LogicalTie):
                    component = expr.head
                else:
                    component = expr
                if component in compound_scope:
                    topmost_components.append(expr)
        start_offset = min(_.start_offset for _ in timespans)
        stop_offset = max(_.stop_offset for _ in timespans)
        timespan = timespantools.Timespan(start_offset, stop_offset)
        return topmost_components, timespan

    def _contributions_do_not_overlap(self, contributions):
        previous_stop_offset = 0
        for contribution in contributions:
            if contribution.start_offset < previous_stop_offset:
                return False
            start_offset = contribution.start_offset
            durations = [_.get_duration() for _ in contribution.payload]
            duration = sum(durations)
            stop_offset = start_offset + duration
            previous_stop_offset = stop_offset
        return True

    def _get_cached_leaves(self, include_rests=False):
        if include_rests:
            if self._cached_leaves_with_rests is None:
                prototype = (
                    scoretools.Note,
                    scoretools.Rest,
                    scoretools.Chord,
                    )
                leaves = list(iterate(self._score).by_timeline(prototype))
                self._cached_leaves_with_rests = leaves
            leaves = self._cached_leaves_with_rests
        else:
            if self._cached_leaves_without_rests is None:
                prototype = (
                    scoretools.Note,
                    scoretools.Chord,
                    )
                leaves = list(iterate(self._score).by_timeline(prototype))
                self._cached_leaves_without_rests = leaves
            leaves = self._cached_leaves_without_rests
        return leaves

    def _get_end_clefs(self):
        result = datastructuretools.TypedOrderedDict()
        staves = iterate(self._score).by_class(scoretools.Staff)
        staves = [_ for _ in staves if _.is_semantic]
        staves.sort(key=lambda x: x.name)
        prototype = indicatortools.Clef
        for staff in staves:
            last_leaf = inspect_(staff).get_leaf(-1)
            clef = inspect_(last_leaf).get_effective(prototype)
            if clef:
                result[staff.name] = clef.name
            else:
                result[staff.name] = None
        return result

    def _get_end_instruments(self):
        result = datastructuretools.TypedOrderedDict()
        contexts = iterate(self._score).by_class(scoretools.Context)
        contexts = list(contexts)
        contexts.sort(key=lambda x: x.name)
        prototype = instrumenttools.Instrument
        for context in contexts:
            if not inspect_(context).has_indicator(prototype):
                continue
            last_leaf = inspect_(context).get_leaf(-1)
            instrument = inspect_(last_leaf).get_effective(prototype)
            if instrument is None:
                continue
            result[context.name] = instrument.instrument_name
        return result

    def _get_end_settings(self):
        end_settings = {}
        end_settings['end_clefs_by_staff'] = self._get_end_clefs()
        end_settings['end_instruments_by_context'] = \
            self._get_end_instruments()
        end_settings['end_tempo'] = self._get_end_tempo_name()
        end_settings['end_time_signature'] = self._get_end_time_signature()
        return end_settings

    def _get_end_tempo_name(self):
        context = self._score['Time Signature Context Skips']
        last_leaf = inspect_(context).get_leaf(-1)
        prototype = indicatortools.Tempo
        effective_tempo = inspect_(last_leaf).get_effective(prototype)
        if not effective_tempo:
            return
        if self.score_package is None:
            return
        tempi = self.score_package.materials.tempi
        for tempo_name, tempo in tempi.items():
            if tempo == effective_tempo:
                break
        else:
            message = 'can not find {!r} in tempo inventory {!r}.'
            message = message.format(tempo, tempi)
            raise Exception(message)
        return tempo_name

    def _get_end_time_signature(self):
        context = self._score['Time Signature Context Skips']
        last_measure = context[-1]
        prototype = indicatortools.TimeSignature
        time_signature = inspect_(last_measure).get_effective(prototype)
        if not time_signature:
            return
        string = str(time_signature)
        return string

    def _get_instrument_by_name(self, instrument_name, material_package):
        instruments = material_package.instruments
        for instrument_name_, instrument in instruments.items():
            if instrument_name_ == instrument_name:
                return instrument

    def _get_name(self):
        return self._segment_metadata.get('name')

    def _get_offsets(self, start_stage, stop_stage):
        context = self._score['Time Signature Context Skips']
        result = self._stage_number_to_measure_indices(start_stage)
        start_measure_index, stop_measure_index = result
        start_measure = context[start_measure_index]
        assert isinstance(start_measure, scoretools.Measure), start_measure
        start_offset = inspect_(start_measure).get_timespan().start_offset
        result = self._stage_number_to_measure_indices(stop_stage)
        start_measure_index, stop_measure_index = result
        stop_measure = context[stop_measure_index]
        assert isinstance(stop_measure, scoretools.Measure), stop_measure
        stop_offset = inspect_(stop_measure).get_timespan().stop_offset
        return start_offset, stop_offset

    def _get_previous_instrument(self, staff_name):
        if not self._previous_segment_metadata:
            return
        previous_instruments = self._previous_segment_metadata.get(
            'end_instruments_by_context')
        if not previous_instruments:
            return
        instrument = previous_instruments.get(staff_name)
        return instrument

    def _get_rehearsal_letter(self):
        segment_number = self._get_segment_number()
        if segment_number == 1:
            return ''
        segment_index = segment_number - 1
        rehearsal_ordinal = ord('A') - 1 + segment_index
        rehearsal_letter = chr(rehearsal_ordinal)
        return rehearsal_letter

    def _get_rhythm_specifier(self, voice_name, stage):
        rhythm_specifier = []
        prototype = baca.tools.RhythmSpecifier
        for rhythm_specifier in self.scoped_specifiers:
            if not isinstance(rhythm_specifier.specifier, prototype):
                continue
            if rhythm_specifier.scope.voice_name == voice_name:
                if rhythm_specifier.scope.stages is not None:
                    start = rhythm_specifier.scope.stages[0]
                    stop = rhythm_specifier.scope.stages[-1] + 1
                else:
                    raise Exception
                if stage in range(start, stop):
                    return rhythm_specifier
        message = 'no rhythm specifier for {!r} found for stage {}.'
        message = message.format(voice_name, stage)
        raise Exception(message)

    def _get_rhythm_specifiers_for_voice(self, voice_name):
        rhythm_specifiers = []
        prototype = baca.tools.RhythmSpecifier
        for scoped_specifier in self.scoped_specifiers:
            if not isinstance(scoped_specifier.specifier, prototype):
                continue
            if scoped_specifier.scope.voice_name == voice_name:
                rhythm_specifiers.append(scoped_specifier)
        return rhythm_specifiers

    def _get_segment_identifier(self):
        segment_name = self._segment_metadata.get('segment_name')
        if segment_name is not None:
            return segment_name
        segment_number = self._get_segment_number()
        return segment_number

    def _get_segment_number(self):
        return self._segment_metadata.get('segment_number', 1)

    def _get_stage_numbers(self, expr):
        if isinstance(expr, baca.tools.StageExpression):
            stage_start_number = expr.stage_start_number
            stage_stop_number = expr.stage_stop_number
        elif isinstance(expr, tuple):
            stage_start_number, stage_stop_number = expr
        else:
            message = 'must be stage expression or tuple: {!r}.'
            message = message.format(expr)
            raise TypeError(message)
        return stage_start_number, stage_stop_number

    def _get_stylesheet_includes(self, is_doc_example=None):
        if is_doc_example:
            return [self._string_trio_stylesheet_path]
        includes = []
        includes.append(self._score_package_stylesheet_path)
        if 1 < self._get_segment_number():
            includes.append(self._score_package_nonfirst_stylesheet_path)
        return includes

    def _get_time_signatures(self, start_stage=None, stop_stage=None):
        import baca
        counts = len(self.time_signatures), sum(self.measures_per_stage)
        assert counts[0] == counts[1], counts
        stages = sequencetools.partition_sequence_by_counts(
            self.time_signatures,
            self.measures_per_stage,
            )
        start_index = start_stage - 1
        if stop_stage is None:
            time_signatures = stages[start_index]
        else:
            stop_index = stop_stage
            stages = stages[start_index:stop_index]
            time_signatures = sequencetools.flatten_sequence(stages)
        start_offset, stop_offset = self._get_offsets(start_stage, stop_stage)
        contribution = baca.tools.Contribution(
            payload=time_signatures,
            start_offset=start_offset
            )
        return contribution

    def _hide_fermata_measure_staff_lines(self):
        for leaf in iterate(self._score).by_leaf():
            start_offset = inspect_(leaf).get_timespan().start_offset
            if start_offset in self._fermata_start_offsets:
                spanner = spannertools.HiddenStaffSpanner()
                attach(spanner, leaf)

    def _initialize_time_signatures(self, time_signatures):
        time_signatures = time_signatures or ()
        time_signatures_ = list(time_signatures)
        time_signatures_ = []
        for time_signature in time_signatures:
            time_signature = indicatortools.TimeSignature(time_signature)
            time_signatures_.append(time_signature)
        time_signatures_ = tuple(time_signatures_)
        if not time_signatures_:
            time_signatures_ = None
        self._time_signatures = time_signatures_

    def _intercalate_rests(self, contributions):
        durations = [_.duration for _ in self.time_signatures]
        start_offsets = mathtools.cumulative_sums(durations)
        segment_duration = start_offsets[-1]
        start_offsets = start_offsets[:-1]
        start_offsets = [durationtools.Offset(_) for _ in start_offsets]
        assert len(start_offsets) == len(self.time_signatures)
        pairs = zip(start_offsets, self.time_signatures)
        result = []
        previous_stop_offset = durationtools.Offset(0)
        for contribution in contributions:
            if contribution.start_offset < previous_stop_offset:
                raise Exception
            if previous_stop_offset < contribution.start_offset:
                selection = self._make_intercalated_rests(
                    previous_stop_offset,
                    contribution.start_offset,
                    pairs,
                    )
                result.append(selection)
            result.extend(contribution.payload)
            durations = [_.get_duration() for _ in contribution.payload]
            duration = sum(durations)
            previous_stop_offset = contribution.start_offset + duration
        if previous_stop_offset < segment_duration:
            selection = self._make_intercalated_rests(
                previous_stop_offset,
                segment_duration,
                pairs,
                )
            result.append(selection)
        return result

    def _interpret_rhythm_specifiers(self):
        self._make_music_for_time_signature_context()
        self._attach_tempo_indicators()
        self._attach_fermatas()
        self._make_spacing_regions()
        for voice in iterate(self._score).by_class(scoretools.Voice):
            self._interpret_rhythm_specifiers_for_voice(voice)

    def _interpret_rhythm_specifiers_for_voice(self, voice):
        assert not len(voice), repr(voice)
        rhythm_specifiers = self._get_rhythm_specifiers_for_voice(voice.name)
        if not rhythm_specifiers:
            measures = self._make_rests()
            voice.extend(measures) 
            return
        effective_staff = inspect_(voice).get_effective_staff()
        effective_staff_name = effective_staff.context_name
        contributions = []
        for rhythm_specifier in rhythm_specifiers:
            assert isinstance(rhythm_specifier, baca.tools.ScopedSpecifier)
            if rhythm_specifier.scope.stages is not None:
                result = self._get_stage_numbers(rhythm_specifier.scope.stages)
                contribution = self._get_time_signatures(*result)
            else:
                continue
            contribution = rhythm_specifier.specifier(
                effective_staff_name, 
                start_offset=contribution.start_offset,
                time_signatures=contribution.payload,
                )
            assert contribution.start_offset is not None
            contributions.append(contribution)
        contributions.sort(key=lambda _: _.start_offset)
        if not self._contributions_do_not_overlap(contributions):
            message = '{!r} has overlapping rhythms.'
            message = message.format(voice.name)
            raise Exception(message)
        contributions = self._intercalate_rests(contributions)
        voice.extend(contributions)
        self._apply_first_and_last_ties(voice)

    def _interpret_scoped_specifier(self, scoped_specifier):
        assert not isinstance(scoped_specifier.specifier, (list, tuple))
        specifier = scoped_specifier.specifier
        if isinstance(specifier, baca.tools.RhythmSpecifier):
            return
        is_wrapped = False
        if isinstance(specifier, baca.tools.SpecifierWrapper):
            specifier_wrapper = specifier
            specifier = specifier_wrapper.specifier
            is_wrapped = True
        contiguous_leaf_prototype = (
            baca.tools.TransitionSpecifier,
            baca.tools.OverrideHandler,
            )
        expression_prototype = (
            expressiontools.LabelExpression,
            expressiontools.SequenceExpression,
            )
        leaf_indicator_prototype = (
            indicatortools.Clef,
            instrumenttools.Instrument,
            markuptools.Markup,
            )
        note_indicator_prototype = (
            indicatortools.Dynamic,
            indicatortools.LilyPondCommand,
            indicatortools.LaissezVibrer,
            )
        attach_leaf_prototype = (
            note_indicator_prototype,
            leaf_indicator_prototype,
            )
        needs_logical_ties_prototype = (
            baca.tools.GlissandoSpecifier,
            baca.tools.PitchSpecifier,
            baca.tools.TrillSpecifier,
            baca.tools.Handler,
            spannertools.Spanner,
            )
        needs_logical_ties_prototype += note_indicator_prototype
        needs_logical_ties_with_rests_prototype = ()
        needs_logical_ties_with_rests_prototype += \
            leaf_indicator_prototype
        needs_logical_ties_with_rests_prototype += \
            contiguous_leaf_prototype
        if isinstance(scoped_specifier.scope, baca.tools.SimpleScope):
            simple_scope = scoped_specifier.scope
            compound_scope = baca.tools.CompoundScope([simple_scope])
            stages = scoped_specifier.scope.stages
        else:
            compound_scope = scoped_specifier.scope
            stages = None
        leaves = None
        if is_wrapped:
            leaves = self._scope_to_leaves(scoped_specifier.scope)
            if specifier_wrapper.prototype is not None:
                prototype = specifier_wrapper.prototype
                leaves = [_ for _ in leaves if isinstance(_, prototype)]
            start_index = specifier_wrapper.start_index
            stop_index = specifier_wrapper.stop_index
            leaves = leaves[start_index:stop_index]
            if specifier_wrapper.with_previous_leaf:
                first_leaf = leaves[0]
                inspector = inspect_(first_leaf)
                previous_leaf = inspector.get_leaf(-1)
                if previous_leaf is None:
                    message = 'previous leaf is none: {!r}.'
                    message = message.format(scoped_specifier)
                    raise Exception(message)
                leaves.insert(0, previous_leaf)
            if specifier_wrapper.with_next_leaf:
                last_leaf = leaves[-1]
                inspector = inspect_(last_leaf)
                next_leaf = inspector.get_leaf(1)
                if next_leaf is None:
                    message = 'next leaf is none: {!r}.'
                    message = message.format(scoped_specifier)
                    raise Exception(message)
                leaves.append(next_leaf)
            stage_expression = stages
            start_index = stage_expression.component_start_index
            stop_index = stage_expression.component_stop_index
            leaves = leaves[start_index:stop_index]
        elif (isinstance(stages, baca.tools.StageExpression) and 
            stages._prototype is scoretools.Leaf):
            leaves = self._scope_to_leaves(scoped_specifier.scope)
            stage_expression = stages
            start_index = stage_expression.component_start_index
            stop_index = stage_expression.component_stop_index
            leaves = leaves[start_index:stop_index]
        elif isinstance(specifier, needs_logical_ties_with_rests_prototype):
            result = self._compound_scope_to_logical_ties(
                compound_scope,
                include_rests=True
                )
            logical_ties_with_rests = result[0]
            if not logical_ties_with_rests:
                message = '{!r} selects no logical ties with rests.'
                message = message.format(scoped_specifier)
                raise Exception(message)
        elif isinstance(specifier, needs_logical_ties_prototype):
            result = self._compound_scope_to_logical_ties(compound_scope)
            logical_ties = result[0]
            if not logical_ties:
                message = '{!r} selects no logical ties.'
                message = message.format(scoped_specifier)
                raise Exception(message)
        elif getattr(specifier, '_selector_type', None) == 'logical ties':
            result = self._compound_scope_to_logical_ties(compound_scope)
            logical_ties = result[0]
            if not logical_ties:
                message = '{!r} selects no logical ties.'
                message = message.format(scoped_specifier)
                raise Exception(message)
        elif isinstance(specifier, expression_prototype):
            pass
        else:
            message = 'what type of specifier is {!r}?'
            message += '\nIn scoped specifier {!r}.'
            message = message.format(specifier, scoped_specifier)
            raise TypeError(message)
        if getattr(specifier, '_include_selection_timespan', False):
            if leaves:
                first = leaves[0]
                last = leaves[-1]
            elif logical_ties:
                first = logical_ties[0].head
                last = logical_ties[-1][-1]
            else:
                raise Exception('must have leaves or logical ties.')
            start_offset = inspect_(first).get_timespan().start_offset
            stop_offset = inspect_(last).get_timespan().stop_offset
            timespan = timespantools.Timespan(
                start_offset=start_offset,
                stop_offset=stop_offset,
                )
        if leaves:
            if isinstance(specifier, attach_leaf_prototype):
                attach(specifier, leaves[0])
            elif isinstance(specifier, spannertools.Spanner):
                assert not len(specifier), repr(specifier)
                attach(copy.copy(specifier), leaves)
            else:
                specifier(leaves)
        elif isinstance(specifier, baca.tools.PitchSpecifier):
            specifier(logical_ties)
        elif isinstance(specifier, note_indicator_prototype):
            if not logical_ties:
                message = 'no logical ties to which to attach specifier'
                message += ' {!r} belonging to specifier {!r}.'
                message = message.format(specifier, scoped_specifier)
                raise Exception(message)
            attach(specifier, logical_ties[0].head)
        elif isinstance(specifier, leaf_indicator_prototype):
            if not logical_ties_with_rests:
                message = 'no logical ties to which to attach specifier'
                message += ' {!r} belonging to specifier {!r}.'
                message = message.format(specifier, scoped_specifier)
                raise Exception(message)
            attach(specifier, logical_ties_with_rests[0].head)
        elif isinstance(specifier, spannertools.Spanner):
            spanner = specifier
            assert not len(spanner)
            spanner = copy.deepcopy(spanner)
            leaves = self._logical_ties_to_leaves(logical_ties)
            attach(spanner, leaves)
        elif isinstance(specifier, contiguous_leaf_prototype):
            specifier(logical_ties_with_rests)
        elif isinstance(specifier, expression_prototype):
            result = self._compound_scope_to_topmost_components(compound_scope)
            topmost_components = result[0]
            selection = select(topmost_components)
            specifier(selection)
        elif isinstance(specifier, baca.tools.Handler):
            specifier(logical_ties)
        else:
            if getattr(specifier, '_include_selection_timespan', False):
                specifier(logical_ties, timespan)
            else:
                specifier(logical_ties)
        if getattr(specifier, '_mutates_score', False):
            self._cached_leaves_with_rests = None
            self._cached_leaves_without_rests = None

    def _interpret_scoped_specifiers(self):
        start = time.time()
        for scoped_specifier in self.scoped_specifiers:
            self._interpret_scoped_specifier(scoped_specifier)
        stop = time.time()
        total = int(stop - start)
        if self.print_timings:
            message = 'total scoped specifier time {} seconds ...'
            message = message.format(total)
            print(message)

    def _is_first_segment(self):
        segment_number = self._get_segment_number()
        return segment_number == 1

    def _is_last_segment(self):
        segment_number = self._get_segment_number()
        segment_count = self._segment_metadata.get('segment_count')
        return segment_number == segment_count

    def _label_clock_time_(self):
        if not self.label_clock_time:
            return
        skip_context = self._score['Time Signature Context Skips']
        skips = []
        for skip in iterate(skip_context).by_leaf(scoretools.Skip):
            start_offset = inspect_(skip).get_timespan().start_offset
            if start_offset in self._fermata_start_offsets:
                continue
            skips.append(skip)
        skips = select(skips)
        label(skips).with_start_offsets(clock_time=True, font_size=-2)

    def _label_instrument_changes(self):
        prototype = instrumenttools.Instrument
        for staff in iterate(self._score).by_class(scoretools.Staff):
            leaves = iterate(staff).by_class(scoretools.Leaf)
            for leaf_index, leaf in enumerate(leaves):
                instruments = inspect_(leaf).get_indicators(prototype)
                if not instruments:
                    continue
                assert len(instruments) == 1
                current_instrument = instruments[0]
                previous_leaf = inspect_(leaf).get_leaf(-1)
                if previous_leaf is not None:
                    result = inspect_(previous_leaf).get_effective(prototype)
                    previous_instrument = result
                elif (leaf_index == 0 and 
                    1 < self._get_segment_number()):
                    instrument = self._get_previous_instrument(staff.name)
                    previous_instrument = instrument
                else:
                    continue
                if previous_instrument != current_instrument:
                    markup = self._make_instrument_change_markup(
                        current_instrument)
                    attach(markup, leaf)

    def _label_stage_numbers_(self):
        if not self.label_stage_numbers:
            return
        context = self._score['Time Signature Context Skips']
        for stage_index in range(self.stage_count):
            stage_number = stage_index + 1
            result = self._stage_number_to_measure_indices(stage_number)
            start_measure_index, stop_measure_index = result
            base = self._get_name() or self._get_rehearsal_letter()
            string = '[{}.{}]'.format(base, stage_number)
            markup = markuptools.Markup(string)
            markup = markup.with_color('blue')
            markup = markup.fontsize(-3)
            start_measure = context[start_measure_index]
            attach(markup, start_measure)

    def _logical_ties_to_leaves(self, logical_ties):
        first_note = logical_ties[0].head
        last_note = logical_ties[-1][-1]
        leaves = []
        current_leaf = first_note
        while current_leaf is not last_note:
            leaves.append(current_leaf)
            current_leaf = inspect_(current_leaf).get_leaf(1)
        leaves.append(last_note)
        return leaves

    def _make_instrument_change_markup(self, instrument):
        string = 'to {}'.format(instrument.instrument_name)
        markup = markuptools.Markup(string, direction=Up)
        markup = markup.box().override(('box-padding', 0.75))
        return markup

    def _make_intercalated_rests(self, start_offset, stop_offset, pairs):
        duration = stop_offset - start_offset
        rest = scoretools.MultimeasureRest(durationtools.Duration(1))
        multiplier = durationtools.Multiplier(duration)
        attach(multiplier, rest)
        selection = select(rest)
        return selection

    def _make_lilypond_file(self, is_doc_example=None):
        includes = self._get_stylesheet_includes(is_doc_example=is_doc_example)
        lilypond_file = lilypondfiletools.make_basic_lilypond_file(
            music=self._score,
            date_time_token=False,
            includes=includes,
            use_relative_includes=True,
            )
        block_names = ('layout', 'paper')
        for item in lilypond_file.items[:]:
            if getattr(item, 'name', None) in block_names:
                lilypond_file.items.remove(item)
        if not is_doc_example:
            #block_names = ('header', 'layout', 'paper')
            block_names = ('header',)
            for item in lilypond_file.items[:]:
                if getattr(item, 'name', None) in block_names:
                    lilypond_file.items.remove(item)
        self._lilypond_file = lilypond_file
            
    def _make_multimeasure_rest_filled_measures(self, time_signatures=None):
        measures = []
        time_signatures = time_signatures or self.time_signatures
        for time_signature in time_signatures:
            time_signature = indicatortools.TimeSignature(time_signature)
            rest = scoretools.MultimeasureRest(durationtools.Duration(1))
            multiplier = durationtools.Multiplier(time_signature.duration)
            attach(multiplier, rest)
            measure = scoretools.Measure(
                time_signature,
                [rest],
                )
            measures.append(measure)
        measures = selectiontools.Selection(measures)
        return measures

    def _make_music_for_time_signature_context(self):
        voice_name = 'Time Signature Context Skips'
        context = self._score[voice_name]
        rhythm_specifiers = self._get_rhythm_specifiers_for_voice(voice_name)
        for rhythm_specifier in rhythm_specifiers:
            if rhythm_specifier.start_tempo is not None:
                start_tempo = new(rhythm_specifier.start_tempo)
                first_leaf = inspect_(context).get_leaf(0)
                attach(start_tempo, first_leaf, scope=Score)
            if rhythm_specifier.stop_tempo is not None:
                stop_tempo = new(rhythm_specifier.stop_tempo)
                last_leaf = inspect_(context).get_leaf(-1)
                attach(stop_tempo, last_leaf, scope=Score)

    def _make_music_for_voice_old(self, voice):
        assert not len(voice), repr(voice)
        rhythm_specifiers = self._get_rhythm_specifiers_for_voice(voice.name)
        rhythm_specifiers.sort(key=lambda x: x.stages[0])
        assert self._stages_do_not_overlap(rhythm_specifiers)
        if not rhythm_specifiers:
            measures = self._make_rests()
            voice.extend(measures) 
            return
        effective_staff = inspect_(voice).get_effective_staff()
        effective_staff_name = effective_staff.context_name
        next_stage = 1
        contributions = []
        for rhythm_specifier in rhythm_specifiers:
            if rhythm_specifier.stages is None:
                continue
            if next_stage < rhythm_specifier.start_stage:
                start_stage = next_stage
                stop_stage = rhythm_specifier.start_stage - 1
                contribution = self._get_time_signatures(
                    start_stage=next_stage,
                    stop_stage=stop_stage,
                    )
                time_signatures = contribution.payload
                measures = self._make_rests(time_signatures)
                voice.extend(measures)
            contribution = self._get_time_signatures(*rhytm_specifier.stages)
            contribution = rhythm_specifier(
                effective_staff_name, 
                start_offset=contribution.start_offset,
                time_signatures=contribution.payload,
                )
            voice.extend(contribution.payload)
            next_stage = rhythm_specifier.stop_stage + 1
        if next_stage <= self.stage_count:
            contribution = self._get_time_signatures(
                next_stage,
                self.stage_count,
                )
            time_signature = contribution.payload
            measures = self._make_rests(time_signatures)
            voice.extend(measures)

    def _make_rests(self, time_signatures=None):
        time_signatures = time_signatures or self.time_signatures
        specifier = rhythmmakertools.DurationSpellingSpecifier(
            spell_metrically='unassignable',
            )
        mask = rhythmmakertools.silence_all(use_multimeasure_rests=True)
        rhythm_maker = rhythmmakertools.NoteRhythmMaker(
            division_masks=[mask],
            )
        selections = rhythm_maker(time_signatures)
        return selections

    def _make_score(self):
        score = self.score_template()
        first_bar_number = self._segment_metadata.get('first_bar_number')
        if first_bar_number is not None:
            set_(score).current_bar_number = first_bar_number
        self._score = score

    def _make_skip_filled_measures(self, time_signatures=None):
        time_signatures = time_signatures or self.time_signatures
        measures = scoretools.make_spacer_skip_measures(time_signatures)
        return measures

    def _make_spacing_regions(self):
        if not self.spacing_map:
            return
        context = self._score['Time Signature Context Skips']
        skips = list(iterate(context).by_class(scoretools.Leaf))
        for stage_number, duration in self.spacing_map:
            self._assert_valid_stage_number(stage_number)
            result = self._stage_number_to_measure_indices(stage_number)
            start_measure_index, stop_measure_index = result
            start_measure = context[start_measure_index]
            assert isinstance(start_measure, scoretools.Measure), start_measure
            start_skip = start_measure[0]
            assert isinstance(start_skip, scoretools.Skip), start_skip
            command = indicatortools.LilyPondCommand('newSpacingSection')
            attach(command, start_skip)
            moment = schemetools.SchemeMoment(duration)
            set_(start_skip).score.proportional_notation_duration = moment

    def _make_volta_containers(self):
        if not self.volta_specifier:
            return
        context = self._score['Time Signature Context Skips']
        measures = context[:]
        for measure in measures:
            assert isinstance(measure, scoretools.Measure), repr(measure)
        for expression in self.volta_specifier:
            if isinstance(expression, baca.tools.MeasureExpression):
                measure_start_number = expression.start_number
                measure_stop_number = expression.stop_number
            elif isinstance(expression, baca.tools.StageSliceExpression):
                stage_start_number = expression.start_number
                stage_stop_number = expression.stop_number
                pair = self._stage_number_to_measure_indices(
                    stage_start_number)
                measure_start_number, _ = pair
                #pair = self._stage_number_to_measure_indices(stage_stop_number)
                #measure_stop_number, _ = pair
                pair = self._stage_number_to_measure_indices(
                    stage_stop_number - 1
                    )
                measure_stop_number = pair[-1] + 1
            else:
                message = 'implement evaluation for {!r} expressions.'
                message = message.format(expression)
                raise NotImplementedError(message)
            volta_measures = measures[measure_start_number:measure_stop_number]
            container = scoretools.Container(volta_measures)
            command = indicatortools.Repeat()
            attach(command, container)

    def _move_instruments_from_notes_back_to_rests(self):
        prototype = instrumenttools.Instrument
        rest_prototype = (scoretools.Rest, scoretools.MultimeasureRest)
        for leaf in iterate(self._score).by_class(scoretools.Leaf):
            instruments = inspect_(leaf).get_indicators(prototype)
            if not instruments:
                continue
            assert len(instruments) == 1
            instrument = instruments[0]
            current_leaf = leaf
            previous_leaf = inspect_(current_leaf).get_leaf(-1)
            if not isinstance(previous_leaf, rest_prototype):
                continue
            while True:
                current_leaf = previous_leaf
                previous_leaf = inspect_(current_leaf).get_leaf(-1)
                if previous_leaf is None:
                    break
                if not isinstance(previous_leaf, rest_prototype):
                    new_instrument = copy.deepcopy(instrument)
                    attach(new_instrument, current_leaf)
                    break
        
    def _populate_time_signature_context(self):
        context = self._score['Time Signature Context Skips']
        measures = self._make_skip_filled_measures()
        context.extend(measures)
        context = self._score['Time Signature Context Multimeasure Rests']
        measures = self._make_multimeasure_rest_filled_measures()
        context.extend(measures)

    def _print_segment_duration_(self):
        if not self.print_segment_duration:
            return
        context = self._score['Time Signature Context Skips']
        current_tempo = None
        leaves = iterate(context).by_class(scoretools.Leaf)
        measure_summaries = []
        tempo_index = 0
        is_trending = False
        for i, leaf in enumerate(leaves):
            duration = inspect_(leaf).get_duration()
            tempi = inspect_(leaf).get_indicators(indicatortools.Tempo)
            if tempi:
                current_tempo = tempi[0]
                for measure_summary in measure_summaries[tempo_index:]:
                    assert measure_summary[-1] is None
                    measure_summary[-1] = current_tempo
                tempo_index = i
                is_trending = False
            if inspect_(leaf).has_indicator(Accelerando):
                is_trending = True
            if inspect_(leaf).has_indicator(Ritardando):
                is_trending = True
            next_tempo = None
            measure_summary = [
                duration, 
                current_tempo, 
                is_trending,
                next_tempo, 
                ]
            measure_summaries.append(measure_summary)
        total_duration = durationtools.Duration(0)
        for measure_summary in measure_summaries:
            duration, current_tempo, is_trending, next_tempo = measure_summary
            if is_trending and current_tempo is not None:
                effective_tempo = current_tempo + next_tempo
                effective_tempo /= 2
            else:
                effective_tempo = current_tempo
            if effective_tempo is None:
                message = 'no effective tempo found ...'
                print(message)
                return
            duration_ = effective_tempo.duration_to_milliseconds(duration)
            duration_ /= 1000
            total_duration += duration_
        total_duration = int(round(total_duration))
        identifier = stringtools.pluralize('second', total_duration)
        message = 'segment duration {} {} ...'
        message = message.format(total_duration, identifier)
        print(message)

    def _remove_score_template_start_clefs(self):
        dictionary = datastructuretools.TypedOrderedDict()
        self._cached_score_template_start_clefs = dictionary
        prototype = indicatortools.Clef
        for context in iterate(self._score).by_class(scoretools.Context):
            if not inspect_(context).has_indicator(prototype):
                continue
            clef = inspect_(context).get_indicator(prototype)
            self._cached_score_template_start_clefs[context.name] = clef.name
            detach(indicatortools.Clef, context)

    def _remove_score_template_start_instruments(self):
        dictionary = datastructuretools.TypedOrderedDict()
        self._cached_score_template_start_instruments = dictionary
        for context in iterate(self._score).by_class(scoretools.Context):
            prototype = instrumenttools.Instrument
            if not inspect_(context).get_indicator(prototype):
                continue
            instrument = inspect_(context).get_indicator(prototype)
            instrument_name = instrument.instrument_name
            self._cached_score_template_start_instruments[context.name] = \
                instrument_name
            detach(instrumenttools.Instrument, context)
        
    def _scope_to_leaves(self, scope):
        if not isinstance(scope, baca.tools.SimpleScope):
            message = 'not yet implemented for {!r}.'
            message = message.format(scope)
            raise TypeError(message)
        result = self._get_stage_numbers(scope.stages)
        start_stage, stop_stage = result
        offsets = self._get_offsets(start_stage, stop_stage)
        stages_timespan = timespantools.Timespan(*offsets)
        voice = self._score[scope.voice_name]
        leaves = []
        for leaf in iterate(voice).by_leaf():
            leaf_timespan = inspect_(leaf).get_timespan()
            if leaf_timespan.starts_during_timespan(stages_timespan):
                leaves.append(leaf)
            elif leaves:
                break
        return leaves 

    def _shorten_long_repeat_ties(self):
        leaves = iterate(self._score).by_class(scoretools.Leaf)
        for leaf in leaves:
            ties = inspect_(leaf).get_spanners(spannertools.Tie)
            if not ties:
                continue
            tie = ties.pop()
            if not tie.use_messiaen_style_ties:
                continue
            previous_leaf = inspect_(leaf).get_leaf(-1)
            if previous_leaf is None:
                continue
            minimum_duration = durationtools.Duration(1, 8)
            if inspect_(previous_leaf).get_duration() < minimum_duration:
                string = r"shape #'((2 . 0) (1 . 0) (0.5 . 0) (0 . 0)) RepeatTie"
                command = indicatortools.LilyPondCommand(string)
                attach(command, leaf)

    def _stage_number_to_measure_indices(self, stage_number):
        if self.stage_count < stage_number:
            message = 'segment has only {} {} (not {}).'
            unit = stringtools.pluralize('stage', self.stage_count)
            message = message.format(self.stage_count, unit, stage_number)
            raise Exception(message)
        measure_indices = mathtools.cumulative_sums(self.measures_per_stage)
        start_measure_index = measure_indices[stage_number-1]
        stop_measure_index = measure_indices[stage_number] - 1
        return start_measure_index, stop_measure_index

    def _stages_do_not_overlap(self, scoped_specifiers):
        stage_numbers = []
        for scoped_specifier in scoped_specifiers:
            if scoped_specifier.stages is None:
                continue
            start_stage, stop_stage = scoped_specifier.stages
            stage_numbers_ = range(start_stage, stop_stage+1)
            stage_numbers.extend(stage_numbers_)
        return len(stage_numbers) == len(set(stage_numbers))

    def _timespan_to_time_signatures(self, timespan):
        if isinstance(timespan, baca.tools.StageExpression):
            stage_expression = timespan
            contribution = self._get_time_signatures(
                stage_expression.start,
                stage_expression.stop,
                )
        else:
            message = 'implement more time signature resolution methods.'
            raise NotImplementedError(message)
        return contribution

    def _transpose_instruments(self):
        if not self.transpose_score:
            return
        pitched_prototype = (scoretools.Note, scoretools.Chord)
        for voice in iterate(self._score).by_class(scoretools.Voice):
            for leaf in iterate(voice).by_class(scoretools.Leaf):
                if not isinstance(leaf, pitched_prototype):
                    continue
                inspector = inspect_(leaf)
                prototype = instrumenttools.Instrument
                instrument = inspector.get_effective(prototype)
                if instrument is None:
                    continue
                assert isinstance(instrument, prototype), repr(instrument)
                try:
                    instrument.transpose_from_sounding_pitch_to_written_pitch(
                        leaf)
                except KeyError:
                    sounding_pitch_number = leaf.written_pitch.pitch_number
                    i = instrument.sounding_pitch_of_written_middle_c.pitch_number
                    written_pitch_number = sounding_pitch_number - i
                    leaf.written_pitch = written_pitch_number

    def _unpack_scopes(self, scopes, score_template=None):
        scope_prototype = (baca.tools.SimpleScope, baca.tools.CompoundScope)
        if isinstance(scopes, scope_prototype):
            scopes = [scopes]
        elif isinstance(scopes, tuple):
            scopes = baca.tools.CompoundScope._to_simple_scopes(
                scopes,
                score_template=score_template,
                )
        elif isinstance(scopes, list):
            scopes__ = []
            for scope in scopes:
                if isinstance(scope, scope_prototype):
                    scopes___.append(scope)
                elif isinstance(scope, tuple):
                    scopes_ = baca.tools.CompoundScope._to_simple_scopes(
                        scope,
                        score_template=score_template,
                        )
                    scopes__.extend(scopes_)
                else:
                    message = 'list must contain only scopes and tuples: {!r}.'
                    message = message.format(scope)
                    raise TypeError(message)
            scopes = scopes__
        else:
            message = 'input must be scope, tuple or list: {!r}.'
            message = message.format(scopes)
            raise TypeError(message)
        assert isinstance(scopes, list), repr(scopes)
        assert all(isinstance(_, scope_prototype) for _ in scopes), repr(
            scopes)
        return scopes

    def _update_segment_metadata(self):
        self._segment_metadata['measure_count'] = self.measure_count
        end_settings = self._get_end_settings()
        self._segment_metadata.update(end_settings)
        class_ = type(self._segment_metadata)
        items = sorted(self._segment_metadata.items())
        segment_metadata = class_(items)
        self._segment_metadata = segment_metadata

    ### PUBLIC PROPERTIES ###

    @property
    def final_barline(self):
        r'''Is true when final barline should appear.

        Set to true, false, none or explicit barline string.

        Returns true, false, none or explicit barline string.
        '''
        return self._final_barline

    @property
    def final_markup(self):
        r'''Gets final markup.

        Set to markup or none.

        Returns markup or none.
        '''
        return self._final_markup

    @property
    def final_markup_extra_offset(self):
        r'''Gets markup extra offset.

        Set to pair or none.

        Returns pair or none.
        '''
        return self._final_markup_extra_offset

    @property
    def label_clock_time(self):
        r'''Is true when segment should label clock time.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._label_clock_time

    @property
    def label_stage_numbers(self):
        r'''Is true when segment should label stage numbers.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._label_stage_numbers

    @property
    def measure_count(self):
        r'''Gets measure count.

        Returns nonnegative integer.
        '''
        return len(self.time_signatures)

    @property
    def measures_per_stage(self):
        r'''Gets measures per stage.

        Groups all measures into a single stage when `measures_per_stage` is
        none.

        Set to list of positive integers or none.

        Returns list of positive integers or none.
        '''
        if self._measures_per_stage is None:
            return [len(self.time_signatures)]
        return self._measures_per_stage

    @property
    def print_segment_duration(self):
        r'''Is true when segment-maker should print approximate segment
        duration in seconds. Otherwise false.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._print_segment_duration

    @property
    def print_timings(self):
        r'''Is true when segment-maker should print interpret timings.
        Otherwise false.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._print_timings

    @property
    def rehearsal_letter(self):
        r'''Gets rehearsal letter.

        Set to string or none.

        Calculates rehearsal letter automatically when none.

        Suppressed rehearsal letter when set to empty string.

        Sets rehearsal letter explicitly when set to nonempty string.

        Returns string or none.
        '''
        return self._rehearsal_letter

    @property
    def scoped_specifiers(self):
        r'''Gets scoped specifiers.

        Returns list of scoped specifiers.
        '''
        return self._scoped_specifiers

    @property
    def score_package(self):
        r'''Gets score package.

        Returns package.
        '''
        return self._score_package

    @property
    def score_template(self):
        r'''Gets score template.

        Returns ``self.score_template()`` when ``self.score_template`` is not
        none.

        Returns ``self.score_package.tools.ScoreTemplate()`` when
        ``self.score_template`` is none.

        Returns score template.
        '''
        if self._score_template is not None:
            return self._score_template
        return self.score_package.tools.ScoreTemplate()

    @property
    def spacing_map(self):
        r'''Gets spacing map.

        Returns tuple of pairs.
        '''
        return self._spacing_map

    @property
    def spacing_specifier(self):
        r'''Gets spacing specifier.

        Defaults to none.

        Set to spacing specifier or none.

        Returns spacing specifier or none.
        '''
        return self._spacing_specifier

    @property
    def stage_count(self):
        r'''Gets stage count.

        Defined equal to 1 when `self.measures_per_stage` is none.

        Returns nonnegative integer.
        '''
        if self.measures_per_stage is None:
            return 1
        return len(self.measures_per_stage)

    @property
    def tempo_specifier(self):
        r'''Gets tempo specifier.

        Set to tempo specifier.

        Returns tempo specifier.
        '''
        return self._tempo_specifier

    @property
    def time_signatures(self):
        r'''Gets time signatures.

        Set to tuple of time signatures.

        Returns tuple of time signatures.
        '''
        return self._time_signatures

    @property
    def transpose_score(self):
        r'''Is true when segment should notate transposing instruments
        at written pitch rather than at sounding pitch.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._transpose_score

    @property
    def volta_specifier(self):
        r'''Gets volta specifier.

        Set to volta specifier.

        Returns volta specifier.
        '''
        return self._volta_specifier

    ### PUBLIC METHODS ###

    def copy_specifier(self, scoped_offset, target_scope, **kwargs):
        r'''Copies rhythm specifier.
        
        Gets rhythm specifier defined at `scoped_offset`.
        
        Makes new rhythm specifier with `target_scope` and optional
        `kwargs`.

        Appends rhythm specifier to segment-maker.

        Returns rhythm specifier.
        '''
        _voice_name, _stage = scoped_offset
        rhythm_specifier = self._get_rhythm_specifier(_voice_name, _stage)
        rhythm_specifier = copy.deepcopy(rhythm_specifier)
        assert isinstance(rhythm_specifier, baca.tools.ScopedSpecifier)
        if target_scope is None:
            target_scope = rhythm_specifier.scope
        else:
            target_scope = baca.tools.SimpleScope(*target_scope)
        rhythm_specifier = rhythm_specifier.specifier
        new_rhythm_specifier = new(rhythm_specifier, **kwargs)
        new_scoped_specifier = baca.tools.ScopedSpecifier(
            target_scope,
            new_rhythm_specifier,
            )
        self.scoped_specifiers.append(new_scoped_specifier)
        return new_scoped_specifier

    def append_specifiers(self, scopes, specifiers, **kwargs):
        r'''Appends each specifier in `specifiers` to each scope in `scopes`.

        Returns scoped specifiers.
        '''
        scopes = self._unpack_scopes(
            scopes,
            score_template=self.score_template,
            )
        if not isinstance(specifiers, (tuple, list)):
            specifiers = [specifiers]
        assert isinstance(specifiers, (tuple, list)), repr(specifiers)
        specifiers_ = []
        for scope in scopes:
            for specifier in specifiers:
                if specifier is None:
                    message = '{!r} contains none-valued specifier.'
                    message = message.format(scope)
                    raise Exception(message)
                default_scope = None
                if isinstance(specifier, instrumenttools.Instrument):
                    default_scope = specifier._default_scope
                specifier = new(specifier, **kwargs)
                if default_scope is not None:
                    specifier._default_scope = default_scope
                specifier_ = baca.tools.ScopedSpecifier(
                    scope=scope,
                    specifier=specifier,
                    )
                self.scoped_specifiers.append(specifier_)
                specifiers_.append(specifier_)
        return specifiers_

    def validate_measure_count(self, measure_count):
        r'''Validates measure count.

        Raises exception when `measure_count` is incorrect.

        Returns none.
        '''
        if not measure_count == self.measure_count:
            message = 'segment measure count is not {} but {}.'
            message = message.format(measure_count, self.measure_count)
            raise Exception(message)

    def validate_measures_per_stage(self):
        r'''Validates measures per stage.

        Raises exception when measures per stage do not match measure count.

        Returns none.
        '''
        if self.measures_per_stage is None:
            return
        if not sum(self.measures_per_stage) == self.measure_count:
            message = 'measures per stage {} do not match measure count {}.'
            message = message.format(
                self.measures_per_stage,
                self.measure_count,
                )
            raise Exception(message)

    def validate_stage_count(self, stage_count):
        r'''Validates stage count.

        Raises exception when `stage_count` is incorrect.

        Returns none.
        '''
        if not stage_count == self.stage_count:
            message = 'segment stage count is not {} but {}.'
            message = message.format(stage_count, self.stage_count)
            raise Exception(message)