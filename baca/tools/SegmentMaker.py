# -*- coding: utf-8 -*-
import abjad
import baca
import copy
import experimental
import os
import time
import traceback


class SegmentMaker(experimental.SegmentMaker):
    r'''Segment-maker.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        With empty input:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context GlobalContext = "Global Context" <<
                    \context GlobalRests = "Global Rests" {
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
                    \context GlobalSkips = "Global Skips" {
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

        With notes:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_commands(
            ...     'vn',
            ...     baca.select_stages(1),
            ...     baca.even_runs(),
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context GlobalContext = "Global Context" <<
                    \context GlobalRests = "Global Rests" {
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
                    \context GlobalSkips = "Global Skips" {
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
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8 [
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8 ]
                            }
                            {
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8 [
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8 ]
                            }
                            {
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8 [
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8 ]
                            }
                            {
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8 [
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

        Segment colors unpitched notes blue.

    '''

    ### CLASS ATTRIBUTES ###

    __documentation_section__ = 'Segments'

    __slots__ = (
        '_allow_empty_selectors',
        '_allow_figure_names',
        '_color_octaves',
        '_color_out_of_range_pitches',
        '_color_repeat_pitch_classes',
        '_cached_leaves_with_rests',
        '_cached_leaves_without_rests',
        '_cached_score_template_start_clefs',
        '_cached_score_template_start_instruments',
        '_design_checker',
        '_fermata_start_offsets',
        '_final_barline',
        '_final_markup',
        '_final_markup_extra_offset',
        '_hide_instrument_names',
        '_ignore_repeat_pitch_classes',
        '_ignore_unpitched_notes',
        '_ignore_unregistered_pitches',
        '_instruments',
        '_is_doc_example',
        '_label_clock_time',
        '_label_stage_numbers',
        '_measures_per_stage',
        '_metronome_marks',
        '_print_segment_duration',
        '_print_timings',
        '_range_checker',
        '_rehearsal_letter',
        '_scoped_specifiers',
        '_score',
        '_score_template',
        '_skip_wellformedness_checks',
        '_skips_instead_of_rests',
        '_spacing_map',
        '_spacing_specifier',
        '_stage_label_base_string',
        '_stages',
        '_tempo_specifier',
        '_time_signatures',
        '_transpose_score',
        '_volta_specifier',
        )

    _absolute_string_trio_stylesheet_path = os.path.join(
        '/',
        'Users',
        'trevorbaca',
        'Scores',
        '_docs',
        'source',
        '_stylesheets',
        'string-trio-stylesheet.ily',
        )
        
    _absolute_two_voice_staff_stylesheet_path = os.path.join(
        '/',
        'Users',
        'trevorbaca',
        'Scores',
        '_docs',
        'source',
        '_stylesheets',
        'two-voice-staff-stylesheet.ily',
        )

    _extend_beam_tag = 'extend beam'

    _publish_storage_format = True

    _relative_string_trio_stylesheet_path = os.path.join(
        '..',
        '..',
        '..',
        '..',
        'source',
        '_stylesheets',
        'string-trio-stylesheet.ily',
        )

    _relative_two_voice_staff_stylesheet_path = os.path.join(
        '..',
        '..',
        '..',
        '..',
        'source',
        '_stylesheets',
        'two-voice-staff-stylesheet.ily',
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
        allow_empty_selections=None,
        allow_figure_names=None,
        color_octaves=None,
        color_out_of_range_pitches=None,
        color_repeat_pitch_classes=None,
        design_checker=None,
        final_barline=None,
        final_markup=None,
        final_markup_extra_offset=None,
        hide_instrument_names=None,
        ignore_repeat_pitch_classes=None,
        ignore_unpitched_notes=None,
        ignore_unregistered_pitches=None,
        instruments=None,
        label_clock_time=None,
        label_stages=None,
        measures_per_stage=None,
        metronome_marks=None,
        print_segment_duration=None,
        print_timings=None,
        range_checker=None,
        rehearsal_letter=None,
        score_template=None,
        skip_wellformedness_checks=None,
        skips_instead_of_rests=None,
        spacing_map=None,
        spacing_specifier=None,
        stage_label_base_string=None,
        tempo_specifier=None,
        time_signatures=None,
        transpose_score=None,
        volta_specifier=None,
        ):
        superclass = super(SegmentMaker, self)
        superclass.__init__()
        if allow_empty_selections is not None:
            allow_empty_selections = bool(allow_empty_selections)
        self._allow_empty_selectors = allow_empty_selections
        if allow_figure_names is not None:
            allow_figure_names = bool(allow_figure_names)
        self._allow_figure_names = allow_figure_names
        if color_octaves is not None:
            color_octaves = bool(color_octaves)
        self._color_octaves = color_octaves
        if color_out_of_range_pitches is not None:
            color_out_of_range_pitches = bool(color_out_of_range_pitches)
        self._color_out_of_range_pitches = color_out_of_range_pitches
        if color_repeat_pitch_classes is not None:
            color_repeat_pitch_classes = bool(color_repeat_pitch_classes)
        self._color_repeat_pitch_classes = color_repeat_pitch_classes
        self._cached_leaves_with_rests = None
        self._cached_leaves_without_rests = None
        self._design_checker = design_checker
        self._fermata_start_offsets = []
        if final_barline not in (None, False, Exact):
            assert isinstance(final_barline, str), repr(final_barline)
        self._final_barline = final_barline
        if final_markup is not None:
            assert isinstance(final_markup, abjad.Markup)
        self._final_markup = final_markup
        if final_markup_extra_offset is not None:
            assert isinstance(final_markup_extra_offset, tuple)
        self._final_markup_extra_offset = final_markup_extra_offset
        if hide_instrument_names is not None:
            hide_instrument_names = bool(hide_instrument_names)
        self._hide_instrument_names = hide_instrument_names
        if ignore_repeat_pitch_classes is not None:
            ignore_repeat_pitch_classes = bool(
                ignore_repeat_pitch_classes)
        self._ignore_repeat_pitch_classes = ignore_repeat_pitch_classes
        if ignore_unpitched_notes is not None:
            ignore_unpitched_notes = bool(ignore_unpitched_notes)
        self._ignore_unpitched_notes = ignore_unpitched_notes
        if ignore_unregistered_pitches is not None:
            ignore_unregistered_pitches = bool(ignore_unregistered_pitches)
        self._ignore_unregistered_pitches = ignore_unregistered_pitches
        if label_clock_time is not None:
            label_clock_time = bool(label_clock_time)
        if instruments is not None:
            assert isinstance(instruments, abjad.TypedOrderedDict)
        self._instruments = instruments
        self._label_clock_time = label_clock_time
        if label_stages is not None:
            label_stages = bool(label_stages)
        self._label_stage_numbers = label_stages
        self._measures_per_stage = measures_per_stage
        if metronome_marks is not None:
            assert isinstance(metronome_marks, abjad.TypedOrderedDict)
        self._metronome_marks = metronome_marks
        self._print_segment_duration = print_segment_duration
        self._print_timings = print_timings
        self._range_checker = range_checker
        self._rehearsal_letter = rehearsal_letter
        self._scoped_specifiers = []
        self._initialize_time_signatures(time_signatures)
        if score_template is not None:
            assert isinstance(score_template, baca.ScoreTemplate)
        self._score_template = score_template
        if skip_wellformedness_checks is not None:
            skip_wellformedness_checks = bool(skip_wellformedness_checks)
        self._skip_wellformedness_checks = skip_wellformedness_checks
        if skips_instead_of_rests is not None:
            skips_instead_of_rests = bool(skips_instead_of_rests)
        self._skips_instead_of_rests = skips_instead_of_rests
        self._spacing_map = spacing_map
        if spacing_specifier is not None:
            assert isinstance(spacing_specifier, baca.HorizontalSpacingCommand)
        self._spacing_specifier = spacing_specifier
        if stage_label_base_string is not None:
            assert isinstance(stage_label_base_string, str)
        self._stage_label_base_string = stage_label_base_string
        self._tempo_specifier = tempo_specifier
        if transpose_score is not None:
            transpose_score = bool(transpose_score)
        self._transpose_score = transpose_score
        self._volta_specifier = volta_specifier

    ### SPECIAL METHODS ###

    def __call__(
        self, 
        is_doc_example=None,
        is_test=None,
        metadata=None,
        previous_metadata=None,
        ):
        r'''Calls segment-maker.

        Set `is_test` to true to use an absolute stylesheet path for tests run
        outside of in-place doctest.

        Returns LilyPond file and segment metadata.
        '''
        self._metadata = metadata or abjad.TypedOrderedDict()
        self._previous_metadata = previous_metadata or abjad.TypedOrderedDict()
        self._is_doc_example = is_doc_example
        self._make_score()
        self._make_lilypond_file(
            is_doc_example=is_doc_example,
            is_test=is_test,
            )
        self._populate_time_signature_context()
        self._label_stage_numbers_()
        self._interpret_rhythm_specifiers()
        self._extend_beams()
        self._interpret_scoped_specifiers()
        self._detach_figure_names()
        self._shorten_long_repeat_ties()
        self._apply_previous_segment_end_settings()
        self._attach_first_segment_score_template_defaults()
        self._apply_spacing_specifier()
        self._make_volta_containers()
        self._label_clock_time_()
        self._hide_instrument_names_()
        self._label_instrument_changes()
        self._transpose_instruments()
        self._attach_rehearsal_mark()
        self._add_final_barline()
        self._add_final_markup()
        self._color_unregistered_pitches()
        self._color_unpitched_notes()
        self._check_wellformedness()
        self._check_design()
        self._check_range()
        self._color_repeat_pitch_classes_()
        self._color_octaves_()
        self._update_metadata()
        self._print_segment_duration_()
        return self._lilypond_file, self._metadata

    ### PRIVATE PROPERTIES ###

    ### PRIVATE METHODS ###

    def _add_final_barline(self):
        if self.final_barline is False:
            return
        abbreviation = '|'
        if self._is_last_segment():
            abbreviation = '|.'
        if isinstance(self.final_barline, str):
            abbreviation = self.final_barline
        self._score.add_final_bar_line(
            abbreviation=abbreviation, 
            to_each_voice=True,
            )
        if self.final_barline is Exact:
            selection = abjad.select(self._score)
            last_leaf = selection._get_component(abjad.Leaf, -1)
            command = 'override Score.BarLine.transparent = ##f'
            command = abjad.LilyPondCommand(command)
            abjad.attach(command, last_leaf)

    def _add_final_markup(self):
        if self.final_markup is None:
            return
        self._score.add_final_markup(
            self.final_markup,
            extra_offset=self.final_markup_extra_offset,
            )

    def _apply_first_and_last_ties(self, voice):
        dummy_tie = abjad.Tie()
        for current_leaf in abjad.iterate(voice).by_leaf():
            if not dummy_tie._attachment_test(current_leaf):
                continue
            if abjad.inspect(current_leaf).has_indicator('tie to me'):
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
                        use_messiaen_style_ties = inspector.has_indicator(
                            'use messiaen style ties')
                        tie = abjad.Tie(
                            use_messiaen_style_ties=use_messiaen_style_ties)
                        abjad.attach(tie, leaves)
                abjad.detach('tie to me', current_leaf)
            if abjad.inspect(current_leaf).has_indicator('tie from me'):
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
                        use_messiaen_style_ties = inspector.has_indicator(
                            'use messiaen style ties')
                        tie = abjad.Tie(
                            use_messiaen_style_ties=use_messiaen_style_ties)
                        abjad.attach(tie, leaves)
                abjad.detach('tie from me', current_leaf)

    def _apply_previous_segment_end_settings(self):
        if self._is_first_segment():
            return
        if not self._previous_metadata:
            message = 'can not find previous metadata before segment {}.'
            message = message.format(self._get_segment_identifier())
            print(message)
            return
        for context in abjad.iterate(self._score).by_class(abjad.Context):
            previous_instrument = self._get_previous_instrument(context.name)
            if not previous_instrument:
                continue
            leaf = abjad.inspect(context).get_leaf(0)
            instrument = abjad.inspect(leaf).get_effective(abjad.Instrument)
            if instrument is not None:
                continue
            copied_previous_instrument = abjad.new(previous_instrument)
            copied_previous_instrument._default_scope = context.context_name
            leaf = abjad.inspect(context).get_leaf(0)
            abjad.attach(copied_previous_instrument, leaf)
        for context in abjad.iterate(self._score).by_class(abjad.Context):
            previous_clef = self._get_previous_clef(context.name)
            if previous_clef is None:
                continue
            leaf = abjad.inspect(context).get_leaf(0)
            clef = abjad.inspect(leaf).get_effective(abjad.Clef)
            if clef is not None:
                continue
            leaf = abjad.inspect(context).get_leaf(0)
            abjad.attach(previous_clef, leaf)
        context = self._score['Global Skips']
        leaf = abjad.inspect(context).get_leaf(0)
        mark = abjad.inspect(leaf).get_effective(abjad.MetronomeMark)
        if mark is None:
            previous_mark = self._get_previous_metronome_mark()
            abjad.attach(previous_mark, leaf)

    def _apply_spacing_specifier(self):
        start_time = time.time()
        if self.spacing_specifier is None:
            return
        self.spacing_specifier(self)
        stop_time = time.time()
        total_time = int(stop_time - start_time)
        if self.print_timings:
            message = 'total spacing specifier time {} seconds ...'
            message = message.format(total_time)
            print(message)
        if 3 < total_time:
            message = 'spacing specifier application took {} seconds!'
            message = message.format(total_time)
            raise Exception(message)

    def _apply_specifier_to_selection(self, specifier, selection, timespan):
        if hasattr(specifier, '__call__'):
            if timespan:
                specifier(selection, timespan)
            else:
                specifier(selection)
        elif isinstance(specifier, abjad.Spanner):
            abjad.attach(copy.copy(specifier), selection)
        else:
            abjad.attach(specifier, selection[0])

    def _assert_valid_stage_number(self, stage_number):
        if not 1 <= stage_number <= self.stage_count:
            message = 'stage number {} must be between {} and {}.'
            message = message.format(stage_number, 1, self.stage_count)
            raise Exception(message)

    def _attach_fermatas(self):
        if not self.tempo_specifier:
            return
        context = self._score['Global Rests']
        directive_prototype = (
            abjad.Fermata,
            abjad.BreathMark,
            )
        rest_prototype = abjad.MultimeasureRest
        for stage_number, directive in self.tempo_specifier:
            if not isinstance(directive, directive_prototype):
                continue
            assert 0 < stage_number <= self.stage_count
            result = self._stage_number_to_measure_indices(stage_number)
            start_measure_index, stop_measure_index = result
            start_measure = context[start_measure_index]
            assert isinstance(start_measure, abjad.Measure), repr(
                start_measure)
            start_skip = start_measure[0]
            assert isinstance(start_skip, rest_prototype), start_skip
            fermata_y_offset = None
            if isinstance(directive, abjad.Fermata):
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
                directive = abjad.Markup.musicglyph(string)
            else:
                directive = abjad.new(directive)
            abjad.attach(directive, start_skip)
            if fermata_y_offset is not None:
                grob_proxy = abjad.override(start_skip).multi_measure_rest_text
                grob_proxy.extra_offset = (0, fermata_y_offset)
            proxy = abjad.override(start_skip)
            proxy.score.multi_measure_rest.transparent = True
            abjad.override(start_skip).score.time_signature.stencil = False
            abjad.attach('fermata measure', start_skip)
            start_offset = abjad.inspect(start_skip).get_timespan().start_offset
            self._fermata_start_offsets.append(start_offset)

    def _attach_first_segment_score_template_defaults(self):
        if self._is_first_segment():
            self.score_template.attach_defaults(self._score)

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
        rehearsal_mark = abjad.RehearsalMark(
            number=letter_number
            )
        voice = self._score['Global Skips']
        leaf = abjad.inspect(voice).get_leaf(0)
        abjad.attach(rehearsal_mark, leaf)

    def _attach_tempo_indicators(self):
        if not self.tempo_specifier:
            return
        context = self._score['Global Skips']
        skips = abjad.select(context).by_leaf(abjad.Skip)
        left_broken_text = abjad.Markup().null()
        left_broken_text._direction = None
        spanner = abjad.MetronomeMarkSpanner(
            left_broken_padding=0,
            left_broken_text=left_broken_text,
            start_with_parenthesized_tempo=False,
            )
        abjad.attach(spanner, skips)
        for stage_number, directive in self.tempo_specifier:
            self._assert_valid_stage_number(stage_number)
            result = self._stage_number_to_measure_indices(stage_number)
            start_measure_index, stop_measure_index = result
            start_measure = context[start_measure_index]
            assert isinstance(start_measure, abjad.Measure)
            start_skip = start_measure[0]
            prototype = (abjad.Skip, abjad.MultimeasureRest)
            assert isinstance(start_skip, prototype), start_skip
            #abjad.attach(directive, start_skip)
            spanner.attach(directive, start_skip)

    def _check_design(self):
        if self.design_checker is None:
            return
        return self.design_checker(self._score)

    def _check_range(self):
        if not self.range_checker:
            return
        if isinstance(self.range_checker, abjad.PitchRange):
            markup = abjad.Markup('*', direction=Up)
            abjad.tweak(markup).color = 'red'
            for voice in abjad.iterate(self._score).by_class(abjad.Voice):
                for leaf in abjad.iterate(voice).by_leaf(pitched=True):
                    if leaf not in self.range_checker:
                        if self.color_out_of_range_pitches:
                            abjad.label(leaf).color_leaves('red')
                            abjad.attach(markup, leaf)
                        else:
                            message = 'out of range: {!r}.'
                            message = message.format(leaf)
                            raise Exception(message)
        else:
            raise NotImplementedError(self.range_checker)

    def _check_wellformedness(self):
        if self.skip_wellformedness_checks:
            return
        score = self._lilypond_file['Score']
#        if not abjad.inspect(score).is_well_formed():
#            inspector = abjad.inspect(score)
#            message = inspector.tabulate_well_formedness_violations()
#            raise Exception(message)
        if (self.color_octaves or
            self.color_repeat_pitch_classes or
            self.ignore_repeat_pitch_classes):
            return
        manager = baca.WellformednessManager()
        if not manager.is_well_formed(score):
            message = manager.tabulate_well_formedness_violations(score)
            raise Exception(message)

    def _color_octaves_(self):
        if not self.color_octaves:
            return
        score = self._score
        vertical_moments = abjad.iterate(score).by_vertical_moment()
        markup = abjad.Markup('OCTAVE', direction=Up)
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
                    abjad.attach(markup, leaf)

    def _color_repeat_pitch_classes_(self):
        if not self.color_repeat_pitch_classes:
            return
        markup = abjad.Markup('@', direction=Up)
        abjad.tweak(markup).color = 'red'
        for voice in abjad.iterate(self._score).by_class(abjad.Voice):
            previous_logical_tie, previous_pitch_classes = None, []
            agent = abjad.iterate(voice)
            for logical_tie in agent.by_logical_tie(pitched=True):
                head = logical_tie.head
                if isinstance(head, abjad.Note):
                    written_pitches = [head.written_pitch]
                elif isinstance(head, abjad.Chord):
                    written_pitches = head.written_pitches
                else:
                    raise TypeError(head)
                pitch_classes = [_.pitch_class for _ in written_pitches]
                if set(pitch_classes) & set(previous_pitch_classes):
                    abjad.label(previous_logical_tie).color_leaves('red')
                    for leaf in previous_logical_tie:
                        abjad.attach(markup, leaf)
                    abjad.label(logical_tie).color_leaves('red')
                    for leaf in logical_tie:
                        abjad.attach(markup, leaf)
                previous_logical_tie = logical_tie
                previous_pitch_classes = pitch_classes

    def _color_unpitched_notes(self):
        if self.ignore_unpitched_notes:
            return
        color = 'blue'
        agent = abjad.iterate(self._score)
        for note in agent.by_leaf(prototype=abjad.Note, with_grace_notes=True):
            if abjad.inspect(note).has_indicator('not yet pitched'):
                abjad.override(note).beam.color = color
                abjad.override(note).dots.color = color
                abjad.override(note).flag.color = color
                abjad.override(note).note_head.color = color
                abjad.override(note).stem.color = color

    def _color_unregistered_pitches(self):
        if self.ignore_unregistered_pitches:
            return
        color = 'magenta'
        prototype = (abjad.Note, abjad.Chord)
        score = self._score
        agent = abjad.iterate(score)
        for note in agent.by_leaf(prototype, with_grace_notes=True):
            if abjad.inspect(note).has_indicator('not yet registered'):
                abjad.override(note).accidental.color = color
                abjad.override(note).beam.color = color
                abjad.override(note).dots.color = color
                abjad.override(note).flag.color = color
                abjad.override(note).note_head.color = color
                abjad.override(note).stem.color = color

    def _compound_scope_to_logical_ties(
        self, 
        scoped_specifier,
        compound_scope,
        include_rests=False,
        leaves_instead_of_logical_ties=False,
        ):
        timespan_map, timespans = [], []
        for scope in compound_scope.simple_scopes:
            result = self._get_stage_numbers(scope.stages)
            start_stage, stop_stage = result
            offsets = self._get_offsets(start_stage, stop_stage)
            timespan = abjad.Timespan(*offsets)
            timespan_map.append((scope.voice_name, timespan))
            timespans.append(timespan)
        compound_scope._timespan_map = timespan_map
        voice_names = [_[0] for _ in timespan_map]
        result = []
        leaves = self._get_cached_leaves(include_rests=include_rests)
        for leaf in leaves:
            if leaf in compound_scope:
                if leaves_instead_of_logical_ties:
                    result.append(leaf)
                else:
                    logical_tie = abjad.inspect(leaf).get_logical_tie()
                    if logical_tie.head is leaf:
                        result.append(logical_tie)
        if not result:
            message = 'EMPTY SELECTION: {}'
            message = message.format(format(scoped_specifier))
            if self.allow_empty_selections:
                print(message)
            else:
                raise Exception(message)
        start_offset = min(_.start_offset for _ in timespans)
        stop_offset = max(_.stop_offset for _ in timespans)
        timespan = abjad.Timespan(start_offset, stop_offset)
        return abjad.select(result), timespan

    def _compound_scope_to_topmost_components(self, compound_scope):
        r'''Use for label expressions.
        '''
        timespan_map, timespans = [], []
        for scope in compound_scope.simple_scopes:
            result = self._get_stage_numbers(scope.stages)
            start_stage, stop_stage = result
            offsets = self._get_offsets(start_stage, stop_stage)
            timespan = abjad.Timespan(*offsets)
            timespan_map.append((scope.voice_name, timespan))
            timespans.append(timespan)
        compound_scope._timespan_map = timespan_map
        voice_names = [_[0] for _ in timespan_map]
        topmost_components = []
        for voice in abjad.iterate(self._score).by_class(abjad.Voice):
            if 'Context' in voice.__class__.__name__:
                continue
            result = abjad.iterate(voice).by_topmost_logical_ties_and_components()
            for argument in result:
                if isinstance(argument, abjad.LogicalTie):
                    component = argument.head
                else:
                    component = argument
                if component in compound_scope:
                    topmost_components.append(argument)
        start_offset = min(_.start_offset for _ in timespans)
        stop_offset = max(_.stop_offset for _ in timespans)
        timespan = abjad.Timespan(start_offset, stop_offset)
        return abjad.select(topmost_components), timespan

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

    def _detach_figure_names(self):
        if self.allow_figure_names:
            return
        for leaf in abjad.iterate(self._score).by_leaf():
            markups = abjad.inspect(leaf).get_indicators(abjad.Markup)
            for markup in markups:
                if (isinstance(markup._annotation, str) and
                    markup._annotation.startswith('figure name:')):
                    abjad.detach(markup, leaf)

    def _evaluate_selector(
        self,
        scoped_specifier,
        compound_scope,
        specifier_wrapper,
        specifier,
        ):
        if specifier_wrapper is not None:
            leaves = self._scope_to_leaves(scoped_specifier.scope)
            leaves = list(leaves)
            if specifier_wrapper.prototype is not None:
                prototype = specifier_wrapper.prototype
                leaves = [_ for _ in leaves if isinstance(_, prototype)]
            start_index = specifier_wrapper.start_index
            stop_index = specifier_wrapper.stop_index
            leaves = leaves[start_index:stop_index]
            if specifier_wrapper.with_previous_leaf:
                first_leaf = leaves[0]
                inspector = abjad.inspect(first_leaf)
                previous_leaf = inspector.get_leaf(-1)
                if previous_leaf is None:
                    message = 'previous leaf is none: {!r}.'
                    message = message.format(scoped_specifier)
                    raise Exception(message)
                leaves.insert(0, previous_leaf)
            if specifier_wrapper.with_next_leaf:
                last_leaf = leaves[-1]
                inspector = abjad.inspect(last_leaf)
                next_leaf = inspector.get_leaf(1)
                if next_leaf is None:
                    message = 'next leaf is none: {!r}.'
                    message = message.format(scoped_specifier)
                    raise Exception(message)
                leaves.append(next_leaf)
            selection = abjad.select(leaves)
        elif hasattr(specifier, 'selector'):
            result = self._compound_scope_to_logical_ties(
                scoped_specifier,
                compound_scope,
                include_rests=True,
                leaves_instead_of_logical_ties=True,
                )
            selection = result[0]
            #raise Exception(selection)
        else:
            result = self._compound_scope_to_logical_ties(
                scoped_specifier,
                compound_scope,
                )
            selection = result[0]
        assert isinstance(selection, abjad.Selection), repr(
            selection)
        if not selection:
            message = 'EMPTY SELECTION: {}'
            message = message.format(format(scoped_specifier))
            if self.allow_empty_selections:
                print(message)
            else:
                raise Exception(message)
        timespan = None
        if getattr(specifier, '_include_selection_timespan', False):
            timespan = self._selection_to_timespan(selection)
        return selection, timespan

    @staticmethod
    def _extend_beam(leaf):
        beam = abjad.inspect(leaf).get_spanner(abjad.Beam)
        if beam is None:
            return
        all_leaves = []
        all_leaves.extend(beam.components)
        durations = []
        if hasattr(beam, 'durations'):
            durations.extend(beam.durations)
        else:
            duration = abjad.select(beam.components).get_duration()
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
            duration = intervening_skips.get_duration()
            durations.append(duration)
        beam = abjad.inspect(next_leaf).get_spanner(abjad.Beam)
        if beam is None:
            all_leaves.append(next_leaf)
            duration = abjad.inspect(next_leaf).get_duration()
            durations.append(duration)
        else:
            all_leaves.extend(beam.components)
            if hasattr(beam, 'durations'):
                durations.extend(beam.durations)
            else:
                duration = abjad.select(beam.components).get_duration()
                durations.append(duration)
        abjad.detach(abjad.Beam, next_leaf)
        all_leaves = abjad.select(all_leaves)
        assert all_leaves.get_duration() == sum(durations)
        beam = abjad.DuratedComplexBeam(
            beam_rests=True,
            durations=durations,
            )
        abjad.attach(beam, all_leaves)

    def _extend_beams(self):
        for leaf in abjad.iterate(self._score).by_leaf():
            if abjad.inspect(leaf).get_indicator(self._extend_beam_tag):
                self._extend_beam(leaf)
        
    def _get_cached_leaves(self, include_rests=False):
        if include_rests:
            if self._cached_leaves_with_rests is None:
                prototype = (
                    abjad.Chord,
                    abjad.Note,
                    abjad.Rest,
                    abjad.Skip,
                    )
                leaves = abjad.iterate(self._score).by_timeline(prototype)
                self._cached_leaves_with_rests = list(leaves)
            leaves = self._cached_leaves_with_rests
        else:
            if self._cached_leaves_without_rests is None:
                prototype = (
                    abjad.Note,
                    abjad.Chord,
                    )
                leaves = abjad.iterate(self._score).by_timeline(prototype)
                self._cached_leaves_without_rests = list(leaves)
            leaves = self._cached_leaves_without_rests
        return leaves

    def _get_contexts_with_instrument_names(self):
        return list(self._cached_score_template_start_instruments.keys())

    def _get_end_clefs(self):
        result = abjad.TypedOrderedDict()
        staves = abjad.iterate(self._score).by_class(abjad.Staff)
        staves = list(staves)
        staves.sort(key=lambda x: x.name)
        for staff in staves:
            last_leaf = abjad.inspect(staff).get_leaf(-1)
            clef = abjad.inspect(last_leaf).get_effective(abjad.Clef)
            if clef:
                result[staff.name] = clef.name
            else:
                result[staff.name] = None
        return result

    def _get_end_instruments(self):
        result = abjad.TypedOrderedDict()
        contexts = abjad.iterate(self._score).by_class(abjad.Context)
        contexts = list(contexts)
        contexts.sort(key=lambda x: x.name)
        for context in contexts:
            if not abjad.inspect(context).get_annotation('default_instrument'):
                continue
            leaf = abjad.inspect(context).get_leaf(-1)
            instrument = abjad.inspect(leaf).get_effective(abjad.Instrument)
            if instrument is None:
                message = 'can not find {} end-instrument.'
                message = message.format(context.name)
                print(message)
            result[context.name] = instrument.instrument_name
        return result

    def _get_end_settings(self):
        result = {}
        if self._is_doc_example:
            return result
        result['end_clefs_by_staff'] = self._get_end_clefs()
        result['end_instruments_by_context'] = self._get_end_instruments()
        result['end_tempo'] = self._get_end_metronome_mark()
        result['end_time_signature'] = self._get_end_time_signature()
        return result

    def _get_end_metronome_mark(self):
        context = self._score['Global Skips']
        leaf = abjad.inspect(context).get_leaf(-1)
        mark = abjad.inspect(leaf).get_effective(abjad.MetronomeMark)
        if not mark:
            return
        if not self.metronome_marks:
            message = 'please define metronome mark manifest.'
            raise Exception(message)
        for name, mark_ in self.metronome_marks.items():
            if mark_ == mark:
                break
        else:
            message = 'can not find {!r} in metronome marks {!r}.'
            message = message.format(mark, self.metronome_marks)
            raise Exception(message)
        return name

    def _get_end_time_signature(self):
        context = self._score['Global Skips']
        last_measure = context[-1]
        prototype = abjad.TimeSignature
        time_signature = abjad.inspect(last_measure).get_effective(prototype)
        if not time_signature:
            return
        string = str(time_signature)
        return string

    def _get_name(self):
        return self._metadata.get('name')

    def _get_offsets(self, start_stage, stop_stage):
        context = self._score['Global Skips']
        result = self._stage_number_to_measure_indices(start_stage)
        start_measure_index, stop_measure_index = result
        start_measure = context[start_measure_index]
        assert isinstance(start_measure, abjad.Measure), start_measure
        start_offset = abjad.inspect(start_measure).get_timespan().start_offset
        result = self._stage_number_to_measure_indices(stop_stage)
        start_measure_index, stop_measure_index = result
        stop_measure = context[stop_measure_index]
        assert isinstance(stop_measure, abjad.Measure), stop_measure
        stop_offset = abjad.inspect(stop_measure).get_timespan().stop_offset
        return start_offset, stop_offset

    def _get_previous_clef(self, context_name):
        if not self._previous_metadata:
            return
        string = 'end_clefs_by_context'
        previous_clefs = self._previous_metadata.get(string)
        if not previous_clefs:
            return
        clef_name = previous_clefs.get(context_name)
        return abjad.Clef(clef_name)

    def _get_previous_instrument(self, context_name):
        if not self._previous_metadata:
            return
        string = 'end_instruments_by_context'
        previous_instruments = self._previous_metadata.get(string)
        if not previous_instruments:
            return
        instrument_name = previous_instruments.get(context_name)
        instrument = self.instruments.get(instrument_name)
        return instrument

    def _get_previous_metronome_mark(self):
        if not self._previous_metadata:
            return
        name = self._previous_metadata.get('end_tempo')
        if not name:
            return
        metronome_mark = self.metronome_marks.get(name)
        return metronome_mark

    def _get_rehearsal_letter(self):
        if self.rehearsal_letter:
            return self.rehearsal_letter
        segment_number = self._get_segment_number()
        if segment_number == 1:
            return ''
        segment_index = segment_number - 1
        rehearsal_ordinal = ord('A') - 1 + segment_index
        rehearsal_letter = chr(rehearsal_ordinal)
        return rehearsal_letter

    def _get_rhythm_specifier(self, voice_name, stage):
        rhythm_specifier = []
        prototype = baca.RhythmSpecifier
        for rhythm_specifier in self.scoped_specifiers:
            if not isinstance(rhythm_specifier.specifier, prototype):
                continue
            if rhythm_specifier.scope.voice_name == voice_name:
                #raise Exception(rhythm_specifier.scope.stages)
                stages = rhythm_specifier.scope.stages
                if isinstance(stages, baca.StageExpression):
                    start = rhythm_specifier.scope.stages.start
                    stop = rhythm_specifier.scope.stages.stop + 1
                elif isinstance(stages, tuple):
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
        prototype = baca.RhythmSpecifier
        for scoped_specifier in self.scoped_specifiers:
            if not isinstance(scoped_specifier.specifier, prototype):
                continue
            if scoped_specifier.scope.voice_name == voice_name:
                rhythm_specifiers.append(scoped_specifier)
        return rhythm_specifiers

    def _get_segment_identifier(self):
        segment_name = self._metadata.get('segment_name')
        if segment_name is not None:
            return segment_name
        segment_number = self._get_segment_number()
        return segment_number

    def _get_segment_number(self):
        return self._metadata.get('segment_number', 1)

    def _get_stage_numbers(self, argument):
        if isinstance(argument, baca.StageExpression):
            start = argument.start
            stop = argument.stop
        elif isinstance(argument, tuple):
            start, stop = argument
        else:
            message = 'must be stage expression or tuple: {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        return start, stop

    def _get_stylesheet_includes(self, is_doc_example=None, is_test=None):
        if is_doc_example:
            if is_test:
                if abjad.inspect(self._score).get_indicator('two-voice'):
                    return [self._absolute_two_voice_staff_stylesheet_path]
                else:
                    return [self._absolute_string_trio_stylesheet_path]
            else:
                if abjad.inspect(self._score).get_indicator('two-voice'):
                    return [self._relative_two_voice_staff_stylesheet_path]
                else:
                    return [self._relative_string_trio_stylesheet_path]
        includes = []
        includes.append(self._score_package_stylesheet_path)
        if 1 < self._get_segment_number():
            includes.append(self._score_package_nonfirst_stylesheet_path)
        return includes

    def _get_time_signatures(self, start_stage=None, stop_stage=None):
        counts = len(self.time_signatures), sum(self.measures_per_stage)
        assert counts[0] == counts[1], counts
        stages = baca.Sequence(self.time_signatures).partition_by_counts(
            self.measures_per_stage,
            )
        start_index = start_stage - 1
        if stop_stage is None:
            time_signatures = stages[start_index]
        else:
            stop_index = stop_stage
            stages = stages[start_index:stop_index]
            time_signatures = baca.Sequence(stages).flatten()
        start_offset, stop_offset = self._get_offsets(start_stage, stop_stage)
        contribution = baca.Contribution(
            payload=time_signatures,
            start_offset=start_offset
            )
        return contribution

    def _handle_mutator(self, specifier):
        if (hasattr(specifier, '_mutates_score') and
            specifier._mutates_score()):
            self._cached_leaves_with_rests = None
            self._cached_leaves_without_rests = None

    def _hide_fermata_measure_staff_lines(self):
        for leaf in abjad.iterate(self._score).by_leaf():
            start_offset = abjad.inspect(leaf).get_timespan().start_offset
            if start_offset in self._fermata_start_offsets:
                spanner = abjad.HiddenStaffSpanner()
                abjad.attach(spanner, leaf)

    def _hide_instrument_names_(self):
        if not self.hide_instrument_names:
            return
        classes = (abjad.Staff, abjad.StaffGroup)
        prototype = abjad.Instrument
        for staff in abjad.iterate(self._score).by_class(classes):
            if abjad.inspect(staff).get_indicator(prototype):
                abjad.detach(prototype, staff)

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

    def _intercalate_rests(self, contributions):
        durations = [_.duration for _ in self.time_signatures]
        start_offsets = abjad.mathtools.cumulative_sums(durations)
        segment_duration = start_offsets[-1]
        start_offsets = start_offsets[:-1]
        start_offsets = [abjad.Offset(_) for _ in start_offsets]
        assert len(start_offsets) == len(self.time_signatures)
        pairs = zip(start_offsets, self.time_signatures)
        result = []
        previous_stop_offset = abjad.Offset(0)
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
        for voice in abjad.iterate(self._score).by_class(abjad.Voice):
            self._interpret_rhythm_specifiers_for_voice(voice)

    def _interpret_rhythm_specifiers_for_voice(self, voice):
        assert not len(voice), repr(voice)
        rhythm_specifiers = self._get_rhythm_specifiers_for_voice(voice.name)
        if not rhythm_specifiers:
            if self.skips_instead_of_rests:
                measures = self._make_skips()
            else:
                measures = self._make_rests()
            voice.extend(measures) 
            return
        effective_staff = abjad.inspect(voice).get_effective_staff()
        effective_staff_name = effective_staff.context_name
        contributions = []
        for rhythm_specifier in rhythm_specifiers:
            assert isinstance(rhythm_specifier, baca.ScopedSpecifier)
            if rhythm_specifier.scope.stages is not None:
                result = self._get_stage_numbers(rhythm_specifier.scope.stages)
                contribution = self._get_time_signatures(*result)
            else:
                continue
            try:
                contribution = rhythm_specifier.specifier(
                    effective_staff_name, 
                    start_offset=contribution.start_offset,
                    time_signatures=contribution.payload,
                    )
            except:
                message = 'rhythm specifier raises exception: {}'
                message = message.format(format(rhythm_specifier))
                raise Exception(message)
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
        result = self._unwrap_scoped_specifier(scoped_specifier)
        compound_scope, specifier_wrapper, specifier = result
        if isinstance(specifier, baca.RhythmSpecifier):
            return
        selection, timespan = self._evaluate_selector(
            scoped_specifier,
            compound_scope,
            specifier_wrapper,
            specifier,
            )
        try:
            self._apply_specifier_to_selection(specifier, selection, timespan)
        except:
            traceback.print_exc()
            raise Exception(format(scoped_specifier))
        self._handle_mutator(specifier)

    def _interpret_scoped_specifiers(self):
        start_time = time.time()
        for scoped_specifier in self.scoped_specifiers:
            self._interpret_scoped_specifier(scoped_specifier)
        stop_time = time.time()
        total_time = int(stop_time - start_time)
        if self.print_timings:
            message = 'total scoped specifier time {} seconds ...'
            message = message.format(total_time)
            print(message)

    def _is_first_segment(self):
        segment_number = self._get_segment_number()
        return segment_number == 1

    def _is_last_segment(self):
        segment_number = self._get_segment_number()
        segment_count = self._metadata.get('segment_count')
        return segment_number == segment_count

    def _label_clock_time_(self):
        if not self.label_clock_time:
            return
        skip_context = self._score['Global Skips']
        skips = []
        for skip in abjad.iterate(skip_context).by_leaf(abjad.Skip):
            start_offset = abjad.inspect(skip).get_timespan().start_offset
            if start_offset in self._fermata_start_offsets:
                continue
            skips.append(skip)
        skips = abjad.select(skips)
        abjad.label(skips).with_start_offsets(clock_time=True, font_size=-2)

    def _label_instrument_changes(self):
        prototype = abjad.Instrument
        for staff in abjad.iterate(self._score).by_class(abjad.Staff):
            leaves = abjad.iterate(staff).by_leaf()
            for leaf_index, leaf in enumerate(leaves):
                instrument = abjad.inspect(leaf).get_indicator(prototype)
                if not instrument:
                    continue
                current_instrument = instrument
                previous_leaf = abjad.inspect(leaf).get_leaf(-1)
                if previous_leaf is not None:
                    agent = abjad.inspect(previous_leaf)
                    result = agent.get_effective(abjad.Instrument)
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
                    abjad.attach(markup, leaf)

    def _label_stage_numbers_(self):
        if not self.label_stages:
            return
        context = self._score['Global Skips']
        for stage_index in range(self.stage_count):
            stage_number = stage_index + 1
            result = self._stage_number_to_measure_indices(stage_number)
            start_measure_index, stop_measure_index = result
            base = self.stage_label_base_string
            base = base or self._get_name()
            base = base or self._get_rehearsal_letter()
            if base not in ('', None):
                string = '[{}.{}]'.format(base, stage_number)
            else:
                string = '[{}]'.format(stage_number)
            markup = abjad.Markup(string)
            markup = markup.with_color('blue')
            markup = markup.fontsize(-3)
            start_measure = context[start_measure_index]
            leaf = abjad.inspect(start_measure).get_leaf(0)
            abjad.attach(markup, leaf)

    def _make_instrument_change_markup(self, instrument):
        string = 'to {}'.format(instrument.instrument_name)
        markup = abjad.Markup(string, direction=Up)
        markup = markup.box().override(('box-padding', 0.75))
        return markup

    def _make_intercalated_rests(self, start_offset, stop_offset, pairs):
        duration = stop_offset - start_offset
        multiplier = abjad.Multiplier(duration)
        #rest = abjad.MultimeasureRest(abjad.Duration(1))
        #abjad.attach(multiplier, rest)
        #selection = abjad.select(rest)
        skip = abjad.Skip(abjad.Duration(1))
        abjad.attach(multiplier, skip)
        selection = abjad.select(skip)
        return selection

    def _make_lilypond_file(self, is_doc_example=None, is_test=None):
        includes = self._get_stylesheet_includes(
            is_doc_example=is_doc_example,
            is_test=is_test,
            )
        lilypond_file = abjad.LilyPondFile.new(
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
            block_names = ('header',)
            for item in lilypond_file.items[:]:
                if getattr(item, 'name', None) in block_names:
                    lilypond_file.items.remove(item)
        self._lilypond_file = lilypond_file
            
    def _make_multimeasure_rest_filled_measures(self, time_signatures=None):
        measures = []
        time_signatures = time_signatures or self.time_signatures
        for time_signature in time_signatures:
            time_signature = abjad.TimeSignature(time_signature)
            rest = abjad.MultimeasureRest(abjad.Duration(1))
            multiplier = abjad.Multiplier(time_signature.duration)
            abjad.attach(multiplier, rest)
            measure = abjad.Measure(
                time_signature,
                [rest],
                )
            measures.append(measure)
        measures = abjad.Selection(measures)
        return measures

    def _make_music_for_time_signature_context(self):
        voice_name = 'Global Skips'
        context = self._score[voice_name]
        rhythm_specifiers = self._get_rhythm_specifiers_for_voice(voice_name)
        for rhythm_specifier in rhythm_specifiers:
            if rhythm_specifier.start_tempo is not None:
                start_tempo = abjad.new(rhythm_specifier.start_tempo)
                first_leaf = abjad.inspect(context).get_leaf(0)
                abjad.attach(start_tempo, first_leaf, scope=Score)
            if rhythm_specifier.stop_tempo is not None:
                stop_tempo = abjad.new(rhythm_specifier.stop_tempo)
                leaf = abjad.inspect(context).get_leaf(-1)
                abjad.attach(stop_tempo, leaf, scope=Score)

    def _make_music_for_voice_old(self, voice):
        assert not len(voice), repr(voice)
        rhythm_specifiers = self._get_rhythm_specifiers_for_voice(voice.name)
        rhythm_specifiers.sort(key=lambda x: x.stages[0])
        assert self._stages_do_not_overlap(rhythm_specifiers)
        if not rhythm_specifiers:
            measures = self._make_rests()
            voice.extend(measures) 
            return
        effective_staff = abjad.inspect(voice).get_effective_staff()
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
        specifier = abjad.rhythmmakertools.DurationSpellingSpecifier(
            spell_metrically='unassignable',
            )
        mask = abjad.silence_all(use_multimeasure_rests=True)
        rhythm_maker = abjad.rhythmmakertools.NoteRhythmMaker(
            division_masks=[mask],
            )
        selections = rhythm_maker(time_signatures)
        return selections

    def _make_score(self):
        score = self.score_template()
        first_bar_number = self._metadata.get('first_bar_number')
        if first_bar_number is not None:
            abjad.setting(score).current_bar_number = first_bar_number
        self._score = score

    def _make_skip_filled_measures(self, time_signatures=None):
        time_signatures = time_signatures or self.time_signatures
        maker = abjad.MeasureMaker()
        measures = maker(time_signatures)
        return measures
        
    def _make_skips(self, time_signatures=None):
        time_signatures = time_signatures or self.time_signatures
        rhythm_maker = abjad.rhythmmakertools.SkipRhythmMaker()
        selections = rhythm_maker(time_signatures)
        return selections

    def _make_spacing_regions(self):
        if not self.spacing_map:
            return
        context = self._score['Global Skips']
        skips = list(abjad.iterate(context).by_leaf())
        for stage_number, duration in self.spacing_map:
            self._assert_valid_stage_number(stage_number)
            result = self._stage_number_to_measure_indices(stage_number)
            start_measure_index, stop_measure_index = result
            start_measure = context[start_measure_index]
            assert isinstance(start_measure, abjad.Measure), repr(
                start_measure)
            start_skip = start_measure[0]
            assert isinstance(start_skip, abjad.Skip), start_skip
            command = abjad.LilyPondCommand('newSpacingSection')
            abjad.attach(command, start_skip)
            moment = abjad.SchemeMoment(duration)
            abjad.setting(start_skip).score.proportional_notation_duration = moment

    def _make_volta_containers(self):
        if not self.volta_specifier:
            return
        context = self._score['Global Skips']
        measures = context[:]
        for measure in measures:
            assert isinstance(measure, abjad.Measure), repr(measure)
        for expression in self.volta_specifier:
            if isinstance(expression, baca.MeasureExpression):
                measure_start_number = expression.start
                measure_stop_number = expression.stop
            elif isinstance(expression, baca.StageSliceExpression):
                start = expression.start
                stop = expression.stop
                pair = self._stage_number_to_measure_indices(start)
                measure_start_number, _ = pair
                #pair = self._stage_number_to_measure_indices(stop)
                #measure_stop_number, _ = pair
                pair = self._stage_number_to_measure_indices(stop-1)
                measure_stop_number = pair[-1] + 1
            else:
                message = 'implement evaluation for {!r} expressions.'
                message = message.format(expression)
                raise NotImplementedError(message)
            volta_measures = measures[measure_start_number:measure_stop_number]
            #container = abjad.Container(volta_measures)
            container = abjad.Container()
            abjad.mutate(volta_measures).wrap(container)
            command = abjad.Repeat()
            abjad.attach(command, container)

    def _move_instruments_from_notes_back_to_rests(self):
        prototype = abjad.Instrument
        rest_prototype = (abjad.Rest, 
            abjad.MultimeasureRest)
        for leaf in abjad.iterate(self._score).by_leaf():
            instruments = abjad.inspect(leaf).get_indicators(prototype)
            if not instruments:
                continue
            assert len(instruments) == 1
            instrument = instruments[0]
            current_leaf = leaf
            previous_leaf = abjad.inspect(current_leaf).get_leaf(-1)
            if not isinstance(previous_leaf, rest_prototype):
                continue
            while True:
                current_leaf = previous_leaf
                previous_leaf = abjad.inspect(current_leaf).get_leaf(-1)
                if previous_leaf is None:
                    break
                if not isinstance(previous_leaf, rest_prototype):
                    new_instrument = copy.deepcopy(instrument)
                    abjad.attach(new_instrument, current_leaf)
                    break
        
    def _populate_time_signature_context(self):
        context = self._score['Global Skips']
        measures = self._make_skip_filled_measures()
        context.extend(measures)
        context = self._score['Global Rests']
        measures = self._make_multimeasure_rest_filled_measures()
        context.extend(measures)

    def _print_segment_duration_(self):
        if not self.print_segment_duration:
            return
        context = self._score['Global Skips']
        current_tempo = None
        leaves = abjad.iterate(context).by_leaf()
        measure_summaries = []
        tempo_index = 0
        is_trending = False
        for i, leaf in enumerate(leaves):
            duration = abjad.inspect(leaf).get_duration()
            tempi = abjad.inspect(leaf).get_indicators(abjad.MetronomeMark)
            if tempi:
                current_tempo = tempi[0]
                for measure_summary in measure_summaries[tempo_index:]:
                    assert measure_summary[-1] is None
                    measure_summary[-1] = current_tempo
                tempo_index = i
                is_trending = False
            if abjad.inspect(leaf).has_indicator(Accelerando):
                is_trending = True
            if abjad.inspect(leaf).has_indicator(Ritardando):
                is_trending = True
            next_tempo = None
            measure_summary = [
                duration, 
                current_tempo, 
                is_trending,
                next_tempo, 
                ]
            measure_summaries.append(measure_summary)
        total_duration = abjad.Duration(0)
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
        identifier = abjad.Strin('second').pluralize(total_duration)
        message = 'segment duration {} {} ...'
        message = message.format(total_duration, identifier)
        print(message)

    def _scope_to_leaves(self, scope):
        if not isinstance(scope, baca.SimpleScope):
            message = 'not yet implemented for {!r}.'
            message = message.format(scope)
            raise TypeError(message)
        result = self._get_stage_numbers(scope.stages)
        start_stage, stop_stage = result
        offsets = self._get_offsets(start_stage, stop_stage)
        stages_timespan = abjad.Timespan(*offsets)
        voice = self._score[scope.voice_name]
        leaves = []
        for leaf in abjad.iterate(voice).by_leaf():
            leaf_timespan = abjad.inspect(leaf).get_timespan()
            if leaf_timespan.starts_during_timespan(stages_timespan):
                leaves.append(leaf)
            elif leaves:
                break
        return abjad.select(leaves )

    def _selection_to_timespan(self, selection):
            if isinstance(selection[0], abjad.LogicalTie):
                first = selection[0].head
            else:
                first = selection[0]
            if isinstance(selection[-1], abjad.LogicalTie):
                last = selection[-1][-1]
            else:
                last = selection[-1]
            start_offset = abjad.inspect(first).get_timespan().start_offset
            stop_offset = abjad.inspect(last).get_timespan().stop_offset
            timespan = abjad.Timespan(
                start_offset=start_offset,
                stop_offset=stop_offset,
                )
            return timespan

    def _shorten_long_repeat_ties(self):
        leaves = abjad.iterate(self._score).by_leaf()
        for leaf in leaves:
            ties = abjad.inspect(leaf).get_spanners(abjad.Tie)
            if not ties:
                continue
            tie = ties.pop()
            if not tie.use_messiaen_style_ties:
                continue
            previous_leaf = abjad.inspect(leaf).get_leaf(-1)
            if previous_leaf is None:
                continue
            minimum_duration = abjad.Duration(1, 8)
            if abjad.inspect(previous_leaf).get_duration() < minimum_duration:
                string = r"shape #'((2 . 0) (1 . 0) (0.5 . 0) (0 . 0)) RepeatTie"
                command = abjad.LilyPondCommand(string)
                abjad.attach(command, leaf)

    def _stage_number_to_measure_indices(self, stage_number):
        if stage_number is Infinity:
            stage_number = self.stage_count
        if self.stage_count < stage_number:
            message = 'segment has only {} {} (not {}).'
            unit = abjad.String('stage').pluralize(self.stage_count)
            message = message.format(self.stage_count, unit, stage_number)
            raise Exception(message)
        measure_indices = abjad.mathtools.cumulative_sums(
            self.measures_per_stage)
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
        if isinstance(timespan, baca.StageExpression):
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
        for voice in abjad.iterate(self._score).by_class(abjad.Voice):
            for leaf in abjad.iterate(voice).by_leaf(
                pitched=True, with_grace_notes=True):
                prototype = abjad.Instrument
                instrument = abjad.inspect(leaf).get_effective(prototype)
                if instrument is None:
                    continue
                assert isinstance(instrument, prototype), repr(instrument)
                try:
                    instrument.transpose_from_sounding_pitch(leaf)
                except KeyError:
                    sounding_pitch_number = leaf.written_pitch.number
                    i = instrument.sounding_pitch_of_written_middle_c.number
                    written_pitch_number = sounding_pitch_number - i
                    leaf.written_pitch = written_pitch_number

    def _unpack_scopes(self, scopes, score_template=None):
        scope_prototype = (baca.SimpleScope, baca.CompoundScope)
        if isinstance(scopes, scope_prototype):
            scopes = [scopes]
        elif isinstance(scopes, tuple):
            scopes = baca.CompoundScope._to_simple_scopes(
                scopes,
                score_template=score_template,
                )
        elif isinstance(scopes, list):
            scopes__ = []
            for scope in scopes:
                if isinstance(scope, scope_prototype):
                    scopes___.append(scope)
                elif isinstance(scope, tuple):
                    scopes_ = baca.CompoundScope._to_simple_scopes(
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

    def _unwrap_scoped_specifier(self, scoped_specifier):
        specifier_wrapper = None
        specifier = scoped_specifier.specifier
        if isinstance(specifier, baca.SpecifierWrapper):
            specifier_wrapper = specifier
            specifier = specifier_wrapper.specifier
        if isinstance(scoped_specifier.scope, baca.SimpleScope):
            simple_scope = scoped_specifier.scope
            compound_scope = baca.CompoundScope([simple_scope])
        else:
            compound_scope = scoped_specifier.scope
        return compound_scope, specifier_wrapper, specifier

    def _update_metadata(self):
        self._metadata['measure_count'] = self.measure_count
        end_settings = self._get_end_settings()
        self._metadata.update(end_settings)
        class_ = type(self._metadata)
        items = sorted(self._metadata.items())
        metadata = class_(items)
        self._metadata = metadata

    ### PUBLIC PROPERTIES ###

    @property
    def allow_empty_selections(self):
        r'''Is true when segment allows empty selectors.

        Otherwise segment raises exception on empty selectors.

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._allow_empty_selectors

    @property
    def allow_figure_names(self):
        r'''Is true when segment allows figure names.

        Is false when segment strips figure names.

        ..  container:: example

            Strips figure names by default:

                >>> music_maker = baca.MusicMaker()

            ::

                >>> collection_lists = [
                ...     [[4]],
                ...     [[6, 2, 3, 5, 9, 8, 0]],
                ...     [[11]],
                ...     [[10, 7, 9, 8, 0, 5]],
                ...     ]
                >>> figures, time_signatures = [], []
                >>> for i, collections in enumerate(collection_lists):
                ...     contribution = music_maker(
                ...         'Voice 1',
                ...         collections,
                ...         figure_name=i,
                ...         )
                ...     figures.append(contribution['Voice 1'])
                ...     time_signatures.append(contribution.time_signature)    
                ...
                >>> figures_ = []
                >>> for figure in figures:
                ...     figures_.extend(figure)
                ...
                >>> figures = abjad.select(figures_)

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     spacing_specifier=baca.HorizontalSpacingCommand(
                ...         minimum_width=abjad.Duration(1, 24),
                ...         ),
                ...     time_signatures=time_signatures,
                ...     )
                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.RhythmSpecifier(
                ...         rhythm_maker=figures,
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
                            {
                                \time 1/16
                                R1 * 1/16
                            }
                            {
                                \time 7/16
                                R1 * 7/16
                            }
                            {
                                \time 1/16
                                R1 * 1/16
                            }
                            {
                                \time 3/8
                                R1 * 3/8
                            }
                        }
                        \context GlobalSkips = "Global Skips" {
                            {
                                \time 1/16
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 1/16
                            }
                            {
                                \time 7/16
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 7/16
                            }
                            {
                                \time 1/16
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 1/16
                            }
                            {
                                \time 3/8
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 3/8
                            }
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \tag violin
                        \context ViolinMusicStaff = "Violin Music Staff" {
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    {
                                        e'16
                                    }
                                }
                                {
                                    {
                                        fs'16 [
                                        d'16
                                        ef'16
                                        f'16
                                        a'16
                                        af'16
                                        c'16 ]
                                    }
                                }
                                {
                                    {
                                        b'16
                                    }
                                }
                                {
                                    {
                                        bf'16 [
                                        g'16
                                        a'16
                                        af'16
                                        c'16
                                        f'16 ]
                                        \bar "|"
                                    }
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Allows figure names:

                >>> music_maker = baca.MusicMaker()

            ::

                >>> collection_lists = [
                ...     [[4]],
                ...     [[6, 2, 3, 5, 9, 8, 0]],
                ...     [[11]],
                ...     [[10, 7, 9, 8, 0, 5]],
                ...     ]
                >>> figures, time_signatures = [], []
                >>> for i, collections in enumerate(collection_lists):
                ...     contribution = music_maker(
                ...         'Voice 1',
                ...         collections,
                ...         figure_name=i,
                ...         )
                ...     figures.append(contribution['Voice 1'])
                ...     time_signatures.append(contribution.time_signature)    
                ...
                >>> figures_ = []
                >>> for figure in figures:
                ...     figures_.extend(figure)
                ...
                >>> figures = abjad.select(figures_)

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     allow_figure_names=True,
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     spacing_specifier=baca.HorizontalSpacingCommand(
                ...         minimum_width=abjad.Duration(1, 24),
                ...         ),
                ...     time_signatures=time_signatures,
                ...     )
                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.RhythmSpecifier(
                ...         rhythm_maker=figures,
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> score = lilypond_file[abjad.Score]
                >>> abjad.override(score).text_script.staff_padding = 3
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" \with {
                    \override TextScript.staff-padding = #3
                } <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
                            {
                                \time 1/16
                                R1 * 1/16
                            }
                            {
                                \time 7/16
                                R1 * 7/16
                            }
                            {
                                \time 1/16
                                R1 * 1/16
                            }
                            {
                                \time 3/8
                                R1 * 3/8
                            }
                        }
                        \context GlobalSkips = "Global Skips" {
                            {
                                \time 1/16
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 1/16
                            }
                            {
                                \time 7/16
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 7/16
                            }
                            {
                                \time 1/16
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 1/16
                            }
                            {
                                \time 3/8
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 3/8
                            }
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \tag violin
                        \context ViolinMusicStaff = "Violin Music Staff" {
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    {
                                        e'16
                                            ^ \markup {
                                                \fontsize
                                                    #2
                                                    \concat
                                                        {
                                                            [
                                                            0
                                                            \hspace
                                                                #1
                                                            \raise
                                                                #0.25
                                                                \fontsize
                                                                    #-2
                                                                    (None)
                                                            ]
                                                        }
                                                }
                                    }
                                }
                                {
                                    {
                                        fs'16 [
                                            ^ \markup {
                                                \fontsize
                                                    #2
                                                    \concat
                                                        {
                                                            [
                                                            1
                                                            \hspace
                                                                #1
                                                            \raise
                                                                #0.25
                                                                \fontsize
                                                                    #-2
                                                                    (None)
                                                            ]
                                                        }
                                                }
                                        d'16
                                        ef'16
                                        f'16
                                        a'16
                                        af'16
                                        c'16 ]
                                    }
                                }
                                {
                                    {
                                        b'16
                                            ^ \markup {
                                                \fontsize
                                                    #2
                                                    \concat
                                                        {
                                                            [
                                                            2
                                                            \hspace
                                                                #1
                                                            \raise
                                                                #0.25
                                                                \fontsize
                                                                    #-2
                                                                    (None)
                                                            ]
                                                        }
                                                }
                                    }
                                }
                                {
                                    {
                                        bf'16 [
                                            ^ \markup {
                                                \fontsize
                                                    #2
                                                    \concat
                                                        {
                                                            [
                                                            3
                                                            \hspace
                                                                #1
                                                            \raise
                                                                #0.25
                                                                \fontsize
                                                                    #-2
                                                                    (None)
                                                            ]
                                                        }
                                                }
                                        g'16
                                        a'16
                                        af'16
                                        c'16
                                        f'16 ]
                                        \bar "|"
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
        return self._allow_figure_names

    @property
    def color_octaves(self):
        r'''Is true when segment-maker colors octaves.

        ..  container:: example

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     color_octaves=True,
                ...     score_template=baca.StringTrioScoreTemplate(),
                ...     spacing_specifier=baca.HorizontalSpacingCommand(
                ...         minimum_width=abjad.Duration(1, 24),
                ...         ),
                ...     time_signatures=[abjad.TimeSignature((6, 16))],
                ...     )

            ::

                >>> music_maker = baca.MusicMaker()
                >>> contribution = music_maker(
                ...     'Violin Music Voice',
                ...     [[2, 4, 5, 7, 9, 11]],
                ...     )
                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.RhythmSpecifier(
                ...         rhythm_maker=contribution['Violin Music Voice'],
                ...         ),
                ...     )

            ::

                >>> contribution = music_maker(
                ...     'Cello Music Voice',
                ...     [[-3, -5, -7, -8, -10, -12]],
                ...     )
                >>> specifiers = segment_maker.append_commands(
                ...     'vc',
                ...     baca.select_stages(1),
                ...     baca.RhythmSpecifier(
                ...         rhythm_maker=contribution['Cello Music Voice'],
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin.viola.cello
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
                            {
                                \time 6/16
                                R1 * 3/8
                            }
                        }
                        \context GlobalSkips = "Global Skips" {
                            {
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 3/8
                            }
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \context StringSectionStaffGroup = "String Section Staff Group" <<
                            \tag violin
                            \context ViolinMusicStaff = "Violin Music Staff" {
                                \context ViolinMusicVoice = "Violin Music Voice" {
                                    {
                                        {
                                            d'16 [
                                            e'16
                                            \once \override Accidental.color = #red
                                            \once \override Beam.color = #red
                                            \once \override Dots.color = #red
                                            \once \override NoteHead.color = #red
                                            \once \override Stem.color = #red
                                            f'16
                                                - \tweak color #red
                                                ^ \markup { OCTAVE }
                                            g'16
                                            a'16
                                            b'16 ]
                                            \bar "|"
                                        }
                                    }
                                }
                            }
                            \tag viola
                            \context ViolaMusicStaff = "Viola Music Staff" {
                                \context ViolaMusicVoice = "Viola Music Voice" {
                                    R1 * 3/8
                                    \bar "|"
                                }
                            }
                            \tag cello
                            \context CelloMusicStaff = "Cello Music Staff" {
                                \context CelloMusicVoice = "Cello Music Voice" {
                                    {
                                        {
                                            a16 [
                                            g16
                                            \once \override Accidental.color = #red
                                            \once \override Beam.color = #red
                                            \once \override Dots.color = #red
                                            \once \override NoteHead.color = #red
                                            \once \override Stem.color = #red
                                            f16
                                                - \tweak color #red
                                                ^ \markup { OCTAVE }
                                            e16
                                            d16
                                            c16 ]
                                            \bar "|"
                                        }
                                    }
                                }
                            }
                        >>
                    >>
                >>

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._color_octaves

    @property
    def color_out_of_range_pitches(self):
        r'''Is true when segment-maker colors out-of-range pitches.

        ..  container:: example

            ::

                >>> music_maker = baca.MusicMaker()

            ::

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
                ...         figure_name=i,
                ...         )
                ...     figures.append(contribution['Voice 1'])
                ...     time_signatures.append(contribution.time_signature)    
                ...
                >>> figures_ = []
                >>> for figure in figures:
                ...     figures_.extend(figure)
                ...
                >>> figures = abjad.select(figures_)

            ::

                >>> pitch_range = abjad.instrumenttools.Violin().pitch_range
                >>> segment_maker = baca.SegmentMaker(
                ...     color_out_of_range_pitches=True,
                ...     range_checker=pitch_range,
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     spacing_specifier=baca.HorizontalSpacingCommand(
                ...         minimum_width=abjad.Duration(1, 24),
                ...         ),
                ...     time_signatures=time_signatures,
                ...     )
                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.RhythmSpecifier(
                ...         rhythm_maker=figures,
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
                            {
                                \time 1/16
                                R1 * 1/16
                            }
                            {
                                \time 7/16
                                R1 * 7/16
                            }
                            {
                                \time 1/16
                                R1 * 1/16
                            }
                            {
                                \time 3/8
                                R1 * 3/8
                            }
                        }
                        \context GlobalSkips = "Global Skips" {
                            {
                                \time 1/16
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 1/16
                            }
                            {
                                \time 7/16
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 7/16
                            }
                            {
                                \time 1/16
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 1/16
                            }
                            {
                                \time 3/8
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 3/8
                            }
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \tag violin
                        \context ViolinMusicStaff = "Violin Music Staff" {
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    {
                                        e'16
                                    }
                                }
                                {
                                    {
                                        \once \override Accidental.color = #red
                                        \once \override Beam.color = #red
                                        \once \override Dots.color = #red
                                        \once \override NoteHead.color = #red
                                        \once \override Stem.color = #red
                                        c16 [
                                            - \tweak color #red
                                            ^ \markup { * }
                                        d'16
                                        ef'16
                                        f'16
                                        af'16
                                        a'16
                                        c'16 ]
                                    }
                                }
                                {
                                    {
                                        b'16
                                    }
                                }
                                {
                                    {
                                        bf'16 [
                                        g'16
                                        a'16
                                        bf'16
                                        c'16
                                        f'16 ]
                                        \bar "|"
                                    }
                                }
                            }
                        }
                    >>
                >>

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._color_out_of_range_pitches

    @property
    def color_repeat_pitch_classes(self):
        r'''Is true when segment-maker colors repeat pitch-classes.

        ..  container:: example

            ::

                >>> music_maker = baca.MusicMaker()

            ::

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
                ...         figure_name=i,
                ...         )
                ...     figures.append(contribution['Voice 1'])
                ...     time_signatures.append(contribution.time_signature)    
                ...
                >>> figures_ = []
                >>> for figure in figures:
                ...     figures_.extend(figure)
                ...
                >>> figures = abjad.select(figures_)

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     color_repeat_pitch_classes=True,
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     spacing_specifier=baca.HorizontalSpacingCommand(
                ...         minimum_width=abjad.Duration(1, 24),
                ...         ),
                ...     time_signatures=time_signatures,
                ...     )
                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.RhythmSpecifier(
                ...         rhythm_maker=figures,
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
                            {
                                \time 1/16
                                R1 * 1/16
                            }
                            {
                                \time 7/16
                                R1 * 7/16
                            }
                            {
                                \time 1/16
                                R1 * 1/16
                            }
                            {
                                \time 3/8
                                R1 * 3/8
                            }
                        }
                        \context GlobalSkips = "Global Skips" {
                            {
                                \time 1/16
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 1/16
                            }
                            {
                                \time 7/16
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 7/16
                            }
                            {
                                \time 1/16
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 1/16
                            }
                            {
                                \time 3/8
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 3/8
                            }
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \tag violin
                        \context ViolinMusicStaff = "Violin Music Staff" {
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    {
                                        e'16
                                    }
                                }
                                {
                                    {
                                        fs'16 [
                                        d'16
                                        ef'16
                                        f'16
                                        \once \override Accidental.color = #red
                                        \once \override Beam.color = #red
                                        \once \override Dots.color = #red
                                        \once \override NoteHead.color = #red
                                        \once \override Stem.color = #red
                                        a'16
                                            - \tweak color #red
                                            ^ \markup { @ }
                                        \once \override Accidental.color = #red
                                        \once \override Beam.color = #red
                                        \once \override Dots.color = #red
                                        \once \override NoteHead.color = #red
                                        \once \override Stem.color = #red
                                        a'16
                                            - \tweak color #red
                                            ^ \markup { @ }
                                        c'16 ]
                                    }
                                }
                                {
                                    {
                                        b'16
                                    }
                                }
                                {
                                    {
                                        bf'16 [
                                        g'16
                                        a'16
                                        \once \override Accidental.color = #red
                                        \once \override Beam.color = #red
                                        \once \override Dots.color = #red
                                        \once \override NoteHead.color = #red
                                        \once \override Stem.color = #red
                                        c''16
                                            - \tweak color #red
                                            ^ \markup { @ }
                                        \once \override Accidental.color = #red
                                        \once \override Beam.color = #red
                                        \once \override Dots.color = #red
                                        \once \override NoteHead.color = #red
                                        \once \override Stem.color = #red
                                        c'16
                                            - \tweak color #red
                                            ^ \markup { @ }
                                        f'16 ]
                                        \bar "|"
                                    }
                                }
                            }
                        }
                    >>
                >>

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        '''
        return self._color_repeat_pitch_classes

    @property
    def design_checker(self):
        r'''Gets design-checker.

        Defaults to none.

        Set to design-checker or none.

        Returns design-checker or none.
        '''
        return self._design_checker

    # TODO: write examples showing Score.BarLine.transparent = ##f
    #       for mensurstriche final_barline=Exact
    @property
    def final_barline(self):
        r'''Gets final barline.

        ..  container:: example

            Nonlast segment sets final barline to ``'|'`` by default:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Last segment in score sets final barline to ``'|.'`` by default:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     )

            ::

                >>> metadata = {'segment_count': 1}
                >>> result = segment_maker(
                ...     is_doc_example=True,
                ...     metadata=metadata,
                ...     )
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|."
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Nonlast segment sets final barline explicitly:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     final_barline='||',
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "||"
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Last segment in score sets final barline explicitly:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     final_barline='||',
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     )

            ::

                >>> metadata = {'segment_count': 1}
                >>> result = segment_maker(
                ...     is_doc_example=True,
                ...     metadata=metadata,
                ...     )
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "||"
                                }
                            }
                        }
                    >>
                >>

        Set to barline string or none.

        Returns barline string or none.
        '''
        return self._final_barline

    @property
    def final_markup(self):
        r'''Gets final markup.
    
        ..  container:: example

            No final markup by default:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            With final markup:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     final_barline='|.',
                ...     final_markup=abjad.Markup('Madison, WI'),
                ...     final_markup_extra_offset=(-9, -2),
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    \once \override TextScript.extra-offset = #'(-9 . -2)
                                    c'8 ] - \markup { "Madison, WI" }
                                    \bar "|."
                                }
                            }
                        }
                    >>
                >>

        Defaults to none.

        Set to markup or none.

        Returns markup or none.
        '''
        return self._final_markup

    @property
    def final_markup_extra_offset(self):
        r'''Gets final markup extra offset.

        See example for final markup, above.

        Defaults to none.

        Set to pair or none.

        Returns pair or none.
        '''
        return self._final_markup_extra_offset

    # TODO: write examples
    @property
    def hide_instrument_names(self):
        r'''Is true when segment hides instrument names.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._hide_instrument_names

    @property
    def ignore_repeat_pitch_classes(self):
        r'''Is true when segment ignores repeat pitch-classes.

        Is false when segment raises exception on repeat pitch-classes.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._ignore_repeat_pitch_classes
    
    @property
    def ignore_unpitched_notes(self):
        r'''Is true when segment ignores unpitched notes.

        Is false when segment colors unpitched notes.

        ..  container:: example

            Colors unpitched notes by default:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Ignores unpitched notes:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     ignore_unpitched_notes=True,
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    c'8 [
                                    c'8
                                    c'8
                                    c'8 ]
                                }
                                {
                                    c'8 [
                                    c'8
                                    c'8 ]
                                }
                                {
                                    c'8 [
                                    c'8
                                    c'8
                                    c'8 ]
                                }
                                {
                                    c'8 [
                                    c'8
                                    c'8 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._ignore_unpitched_notes

    @property
    def ignore_unregistered_pitches(self):
        r'''Is true when segment ignores unregistered pitches.

        Is false when segment colors unregistered pitches.

        ..  container:: example

            Colors unregistered pitches by default:

                >>> music_maker = baca.MusicMaker(
                ...     baca.MusicRhythmSpecifier(
                ...         rhythm_maker=baca.MusicRhythmMaker(
                ...             acciaccatura_specifiers=[
                ...                 baca.AcciaccaturaSpecifier(),
                ...                 ],
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[3],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     color_unregistered_pitches=True,
                ...     denominator=8,
                ...     )

            ::

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

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     spacing_specifier=baca.HorizontalSpacingCommand(
                ...         minimum_width=abjad.Duration(1, 24),
                ...         ),
                ...     time_signatures=time_signatures,
                ...     )
                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.RhythmSpecifier(
                ...         rhythm_maker=figures,
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> score = lilypond_file[abjad.Score]
                >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
                >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" \with {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                } <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
                            {
                                \time 3/16
                                R1 * 3/16
                            }
                            {
                                R1 * 3/16
                            }
                            {
                                R1 * 3/16
                            }
                            {
                                R1 * 3/16
                            }
                        }
                        \context GlobalSkips = "Global Skips" {
                            {
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 3/16
                            }
                            {
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 3/16
                            }
                            {
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 3/16
                            }
                            {
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 3/16
                            }
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \tag violin
                        \context ViolinMusicStaff = "Violin Music Staff" {
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    {
                                        \once \override Accidental.color = #magenta
                                        \once \override Beam.color = #magenta
                                        \once \override Dots.color = #magenta
                                        \once \override Flag.color = #magenta
                                        \once \override NoteHead.color = #magenta
                                        \once \override Stem.color = #magenta
                                        e'8.
                                    }
                                }
                                {
                                    {
                                        \acciaccatura {
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            fs'16 [
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            d'16
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            ef'16
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            f'16
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            a'16
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            af'16 ]
                                        }
                                        \once \override Accidental.color = #magenta
                                        \once \override Beam.color = #magenta
                                        \once \override Dots.color = #magenta
                                        \once \override Flag.color = #magenta
                                        \once \override NoteHead.color = #magenta
                                        \once \override Stem.color = #magenta
                                        c'8.
                                    }
                                }
                                {
                                    {
                                        \once \override Accidental.color = #magenta
                                        \once \override Beam.color = #magenta
                                        \once \override Dots.color = #magenta
                                        \once \override Flag.color = #magenta
                                        \once \override NoteHead.color = #magenta
                                        \once \override Stem.color = #magenta
                                        b'8.
                                    }
                                }
                                {
                                    {
                                        \acciaccatura {
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            bf'16 [
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            g'16
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            a'16
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            af'16
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            c'16 ]
                                        }
                                        \once \override Accidental.color = #magenta
                                        \once \override Beam.color = #magenta
                                        \once \override Dots.color = #magenta
                                        \once \override Flag.color = #magenta
                                        \once \override NoteHead.color = #magenta
                                        \once \override Stem.color = #magenta
                                        f'8.
                                        \bar "|"
                                    }
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Ignores unregistered pitches:

                >>> music_maker = baca.MusicMaker(
                ...     baca.MusicRhythmSpecifier(
                ...         rhythm_maker=baca.MusicRhythmMaker(
                ...             acciaccatura_specifiers=[
                ...                 baca.AcciaccaturaSpecifier(),
                ...                 ],
                ...             talea=abjad.rhythmmakertools.Talea(
                ...                 counts=[3],
                ...                 denominator=16,
                ...                 ),
                ...             ),
                ...         ),
                ...     color_unregistered_pitches=True,
                ...     denominator=8,
                ...     )

            ::

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

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     ignore_unregistered_pitches=True,
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     spacing_specifier=baca.HorizontalSpacingCommand(
                ...         minimum_width=abjad.Duration(1, 24),
                ...         ),
                ...     time_signatures=time_signatures,
                ...     )
                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.RhythmSpecifier(
                ...         rhythm_maker=figures,
                ...         ),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> score = lilypond_file[abjad.Score]
                >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
                >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" \with {
                    \override SpacingSpanner.strict-grace-spacing = ##f
                    \override SpacingSpanner.strict-note-spacing = ##f
                } <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
                            {
                                \time 3/16
                                R1 * 3/16
                            }
                            {
                                R1 * 3/16
                            }
                            {
                                R1 * 3/16
                            }
                            {
                                R1 * 3/16
                            }
                        }
                        \context GlobalSkips = "Global Skips" {
                            {
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 3/16
                            }
                            {
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 3/16
                            }
                            {
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 3/16
                            }
                            {
                                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                                \newSpacingSection
                                s1 * 3/16
                            }
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \tag violin
                        \context ViolinMusicStaff = "Violin Music Staff" {
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    {
                                        e'8.
                                    }
                                }
                                {
                                    {
                                        \acciaccatura {
                                            fs'16 [
                                            d'16
                                            ef'16
                                            f'16
                                            a'16
                                            af'16 ]
                                        }
                                        c'8.
                                    }
                                }
                                {
                                    {
                                        b'8.
                                    }
                                }
                                {
                                    {
                                        \acciaccatura {
                                            bf'16 [
                                            g'16
                                            a'16
                                            af'16
                                            c'16 ]
                                        }
                                        f'8.
                                        \bar "|"
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
        return self._ignore_unregistered_pitches

    @property
    def instruments(self):
        r'''Gets instrument list.

        Returns typed ordered dictionary or none.
        '''
        return self._instruments

    @property
    def label_clock_time(self):
        r'''Is true when segment labels clock time. Otherwise false.

        ..  container:: example

            Does not label clock time:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     tempo_specifier=baca.TempoSpecifier([
                ...         (1, abjad.MetronomeMark((1, 8), 90)),
                ...         ]),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
                            {
                                \time 4/8
                                s1 * 1/2 ^ \markup {
                                    \fontsize
                                        #-6
                                        \general-align
                                            #Y
                                            #DOWN
                                            \note-by-number
                                                #3
                                                #0
                                                #1
                                    \upright
                                        {
                                            =
                                            90
                                        }
                                    }
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>
                
        ..  container:: example

            Does label clock time:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     label_clock_time=True,
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     tempo_specifier=baca.TempoSpecifier([
                ...         (1, abjad.MetronomeMark((1, 8), 90)),
                ...         ]),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True) # doctest: +SKIP
                >>> lilypond_file, metadata = result # doctest: +SKIP
                >>> show(lilypond_file) # doctest: +SKIP

            ..  todo:: MAKE THIS WORK AGAIN.

            ..  docs::

                >>> f(lilypond_file[abjad.Score]) # doctest: +SKIP
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
                            {
                                \time 4/8
                                s1 * 1/2
                                    ^ \markup {
                                        \fontsize
                                            #-2
                                            0'00''
                                        }
                                    ^ \markup {
                                    \fontsize
                                        #-6
                                        \general-align
                                            #Y
                                            #DOWN
                                            \note-by-number
                                                #3
                                                #0
                                                #1
                                    \upright
                                        {
                                            =
                                            90
                                        }
                                    }
                            }
                            {
                                \time 3/8
                                s1 * 3/8
                                    ^ \markup {
                                        \fontsize
                                            #-2
                                            0'02''
                                        }
                            }
                            {
                                \time 4/8
                                s1 * 1/2
                                    ^ \markup {
                                        \fontsize
                                            #-2
                                            0'04''
                                        }
                            }
                            {
                                \time 3/8
                                s1 * 3/8
                                    ^ \markup {
                                        \fontsize
                                            #-2
                                            0'07''
                                        }
                            }
                        }
                    >>
                    \context MusicContext = "Music Context" <<
                        \tag violin
                        \context ViolinMusicStaff = "Violin Music Staff" {
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._label_clock_time

    @property
    def label_stages(self):
        r'''Is true when segment labels stage numbers.

        ..  container:: example

            Does not label stages by default:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Labels stage numbers:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     label_stages=True,
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
                            {
                                \time 4/8
                                s1 * 1/2
                                    - \markup {
                                        \fontsize
                                            #-3
                                            \with-color
                                                #blue
                                                [1]
                                        }
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Labels numbers with segment name:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     label_stages=True,
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     )

            ::

                >>> metadata = {'name': 'K'}
                >>> result = segment_maker(
                ...     is_doc_example=True,
                ...     metadata=metadata,
                ...     )
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
                            {
                                \time 4/8
                                s1 * 1/2
                                    - \markup {
                                        \fontsize
                                            #-3
                                            \with-color
                                                #blue
                                                [K.1]
                                        }
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

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
    def metronome_marks(self):
        r'''Gets metronome marks.

        Returns typed ordered dictionary or none.
        '''
        return self._metronome_marks

    @property
    def print_segment_duration(self):
        r'''Is true when segment prints duration in seconds.
        
        Output prints to terminal.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._print_segment_duration

    @property
    def print_timings(self):
        r'''Is true when segment prints interpreter timings.

        Output prints to terminal.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._print_timings

    @property
    def range_checker(self):
        r'''Gets range checker.

        Set to pitch range, true, false or none.

        Returns pitch range, true, false or none.
        '''
        return self._range_checker

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
    def score_template(self):
        r'''Gets score template.

        ..  container:: example

            Gets none:

            ::

                >>> segment_maker = baca.SegmentMaker()

            ::

                >>> segment_maker.score_template is None
                True

        ..  container:: example

            Gets score template:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     )

            ::

                >>> segment_maker.score_template
                ViolinSoloScoreTemplate()

        Defaults to none.

        Set to score template or none.

        Returns score template or none.
        '''
        return self._score_template

    @property
    def skip_wellformedness_checks(self):
        r'''Is true when segment skips wellformedness checks.

        Returns true, false or none.
        '''
        return self._skip_wellformedness_checks

    @property
    def skips_instead_of_rests(self):
        r'''Is true when segment fills empty measures with skips.

        Is false when segment fills empty measures with multimeasure rests.

        ..  container:: example

            Fills empty measures with multimeasure rests by default:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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

            Fills empty measures with skips:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     skips_instead_of_rests=True,
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                s1 * 1/2
                                s1 * 3/8
                                s1 * 1/2
                                s1 * 3/8
                                \bar "|"
                            }
                        }
                    >>
                >>

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._skips_instead_of_rests

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
    def stage_label_base_string(self):
        r'''Gets stage label base string.

        ..  container:: example

            Takes base string from segment name by default:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     label_stages=True,
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     )

            ::

                >>> metadata = {'name': 'K'}
                >>> result = segment_maker(
                ...     is_doc_example=True,
                ...     metadata=metadata,
                ...     )
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
                            {
                                \time 4/8
                                s1 * 1/2
                                    - \markup {
                                        \fontsize
                                            #-3
                                            \with-color
                                                #blue
                                                [K.1]
                                        }
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Takes base string from stage label property:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     label_stages=True,
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     stage_label_base_string='intermezzo',
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     )

            ::

                >>> metadata = {'name': 'K'}
                >>> result = segment_maker(
                ...     is_doc_example=True,
                ...     metadata=metadata,
                ...     )
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
                            {
                                \time 4/8
                                s1 * 1/2
                                    - \markup {
                                        \fontsize
                                            #-3
                                            \with-color
                                                #blue
                                                [intermezzo.1]
                                        }
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        Defaults to none.

        Set to string or none.

        Returns string or none.
        '''
        return self._stage_label_base_string

    @property
    def tempo_specifier(self):
        r'''Gets tempo specifier.

        ..  container:: example

            Without tempo specifier:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            With tempo specifier:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     tempo_specifier=baca.TempoSpecifier([
                ...         (1, abjad.MetronomeMark((1, 8), 90)),
                ...         ]),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
                            {
                                \time 4/8
                                s1 * 1/2 ^ \markup {
                                    \fontsize
                                        #-6
                                        \general-align
                                            #Y
                                            #DOWN
                                            \note-by-number
                                                #3
                                                #0
                                                #1
                                    \upright
                                        {
                                            =
                                            90
                                        }
                                    }
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        Defaults to none.

        Set to tempo specifier or none.

        Returns tempo specifier or none.
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
        r'''Is true when segment transposes score.

        ..  container:: example

            Does not transpose score by default:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     baca.pitches('E4 F4'),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    e'8 [
                                    f'8
                                    e'8
                                    f'8 ]
                                }
                                {
                                    e'8 [
                                    f'8
                                    e'8 ]
                                }
                                {
                                    f'8 [
                                    e'8
                                    f'8
                                    e'8 ]
                                }
                                {
                                    f'8 [
                                    e'8
                                    f'8 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        ..  note:: Build example with transposing instrument.

        ..  note:: Score package must currently be passed in for transposition
            to work. Eventually instrument list will be passed instead.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._transpose_score

    @property
    def volta_specifier(self):
        r'''Gets volta specifier.

        ..  container:: example

            Without volta specifier:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            With volta specifier:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     volta_specifier=baca.VoltaSpecifier([
                ...         baca.MeasureExpression(1, 2),
                ...         ]),
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
                            {
                                \time 4/8
                                s1 * 1/2
                            }
                            \repeat volta 2
                            {
                                {
                                    \time 3/8
                                    s1 * 3/8
                                }
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        Defaults to none.

        Set to volta specifier or none.

        Returns volta specifier or none.
        '''
        return self._volta_specifier

    ### PUBLIC METHODS ###

    def append_specifiers(self, scopes, *specifiers, **keywords):
        r'''Appends each specifier in `specifiers` to each scope in `scopes`.

        ..  container:: example

            With label specifier:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_specifiers(
                ...     ('vn', baca.select_stages(1)),
                ...     baca.even_runs(),
                ...     abjad.label().with_indices(),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                        ^ \markup {
                                            \small
                                                0
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                        ^ \markup {
                                            \small
                                                1
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                        ^ \markup {
                                            \small
                                                2
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                        ^ \markup {
                                            \small
                                                3
                                            }
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                        ^ \markup {
                                            \small
                                                4
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                        ^ \markup {
                                            \small
                                                5
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                        ^ \markup {
                                            \small
                                                6
                                            }
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                        ^ \markup {
                                            \small
                                                7
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                        ^ \markup {
                                            \small
                                                8
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                        ^ \markup {
                                            \small
                                                9
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                        ^ \markup {
                                            \small
                                                10
                                            }
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                        ^ \markup {
                                            \small
                                                11
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                        ^ \markup {
                                            \small
                                                12
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                        ^ \markup {
                                            \small
                                                13
                                            }
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        Returns scoped specifiers.
        '''
        if keywords != {}:
            message = 'found specifier keywords: {!r}.'
            message = message.format(keywords)
            raise Exception(message)
        scopes = self._unpack_scopes(
            scopes,
            score_template=self.score_template,
            )
        assert isinstance(specifiers, tuple), repr(specifiers)
        if specifiers and isinstance(specifiers[0], list):
            message = 'REFACTOR: remove outer list: {!r}.'
            message = message.format(specifiers)
            raise Exception(message)
        specifiers_ = []
        for scope in scopes:
            for specifier in specifiers:
                if specifier is None:
                    message = '{!r} contains none-valued specifier.'
                    message = message.format(scope)
                    raise Exception(message)
                default_scope = None
                if isinstance(specifier, abjad.Instrument):
                    default_scope = specifier._default_scope
                specifier = abjad.new(specifier, **keywords)
                if default_scope is not None:
                    specifier._default_scope = default_scope
                specifier_ = baca.ScopedSpecifier(
                    scope=scope,
                    specifier=specifier,
                    )
                self.scoped_specifiers.append(specifier_)
                specifiers_.append(specifier_)
        return specifiers_

    def append_commands(self, voice_name, selector, *commands):
        r'''Appends each `commands` to `voice_name` with `selector`.

        ..  container:: example

            With label specifier:

            ::

                >>> segment_maker = baca.SegmentMaker(
                ...     score_template=baca.ViolinSoloScoreTemplate(),
                ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
                ...     )

            ::

                >>> specifiers = segment_maker.append_commands(
                ...     'vn',
                ...     baca.select_stages(1),
                ...     baca.even_runs(),
                ...     abjad.label().with_indices(),
                ...     )

            ::

                >>> result = segment_maker(is_doc_example=True)
                >>> lilypond_file, metadata = result
                >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin
                    \context GlobalContext = "Global Context" <<
                        \context GlobalRests = "Global Rests" {
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
                        \context GlobalSkips = "Global Skips" {
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
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                        ^ \markup {
                                            \small
                                                0
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                        ^ \markup {
                                            \small
                                                1
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                        ^ \markup {
                                            \small
                                                2
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                        ^ \markup {
                                            \small
                                                3
                                            }
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                        ^ \markup {
                                            \small
                                                4
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                        ^ \markup {
                                            \small
                                                5
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                        ^ \markup {
                                            \small
                                                6
                                            }
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                        ^ \markup {
                                            \small
                                                7
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                        ^ \markup {
                                            \small
                                                8
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                        ^ \markup {
                                            \small
                                                9
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                        ^ \markup {
                                            \small
                                                10
                                            }
                                }
                                {
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                                        ^ \markup {
                                            \small
                                                11
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                                        ^ \markup {
                                            \small
                                                12
                                            }
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                        ^ \markup {
                                            \small
                                                13
                                            }
                                    \bar "|"
                                }
                            }
                        }
                    >>
                >>

        Returns scoped specifiers.
        '''
        return self.append_specifiers((voice_name, selector), *commands)

    def copy_specifier(self, scoped_offset, target_scope, **keywords):
        r'''Copies rhythm specifier.
        
        Gets rhythm specifier defined at `scoped_offset`.
        
        Makes new rhythm specifier with `target_scope` and optional `keywords`.

        Returns rhythm specifier.
        '''
        _voice_name, _stage = scoped_offset
        rhythm_specifier = self._get_rhythm_specifier(_voice_name, _stage)
        rhythm_specifier = copy.deepcopy(rhythm_specifier)
        assert isinstance(rhythm_specifier, baca.ScopedSpecifier)
        if target_scope is None:
            target_scope = rhythm_specifier.scope
        elif isinstance(target_scope, baca.SimpleScope):
            pass
        else:
            target_scope = baca.SimpleScope(
                voice_name=_voice_name,
                stages=(target_scope.start, target_scope.stop),
                )
        rhythm_specifier = rhythm_specifier.specifier
        new_rhythm_specifier = abjad.new(rhythm_specifier, **keywords)
        new_scoped_specifier = baca.ScopedSpecifier(
            target_scope,
            new_rhythm_specifier,
            )
        self.scoped_specifiers.append(new_scoped_specifier)
        return new_scoped_specifier

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
