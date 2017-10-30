import abjad
import baca
import pathlib
import time
import traceback


class SegmentMaker(abjad.SegmentMaker):
    r'''Segment-maker.

    ..  container:: example

        With empty input:

        >>> segment_maker = baca.SegmentMaker(
        ...     score_template=baca.ViolinSoloScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> result = segment_maker.run(is_doc_example=True)
        >>> lilypond_file, metadata = result
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
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
                            \set ViolinMusicStaff.instrumentName = \markup { Violin }
                            \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                            \clef "treble"
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

        >>> segment_maker = baca.SegmentMaker(
        ...     score_template=baca.ViolinSoloScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> segment_maker(
        ...     baca.scope('Violin Music Voice', 1),
        ...     baca.even_runs(),
        ...     )

        >>> result = segment_maker.run(is_doc_example=True)
        >>> lilypond_file, metadata = result
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
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
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
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

    __documentation_section__ = 'Music'

    __slots__ = (
        '_allow_empty_selections',
        '_allow_figure_names',
        '_cache',
        '_cached_score_template_start_clefs',
        '_cached_score_template_start_instruments',
        '_color_octaves',
        '_color_out_of_range_pitches',
        '_color_repeat_pitch_classes',
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
        '_score',
        '_score_template',
        '_skip_wellformedness_checks',
        '_skips_instead_of_rests',
        '_spacing_map',
        '_spacing_specifier',
        '_stage_label_base_string',
        '_stages',
        '_metronome_mark_measure_map',
        '_time_signatures',
        '_transpose_score',
        '_volta_measure_map',
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

    _extend_beam_tag = 'extend beam'

    _publish_storage_format = True

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
        metronome_mark_measure_map=None,
        time_signatures=None,
        transpose_score=None,
        volta_measure_map=None,
        ):
        superclass = super(SegmentMaker, self)
        superclass.__init__()
        if allow_empty_selections is not None:
            allow_empty_selections = bool(allow_empty_selections)
        self._allow_empty_selections = allow_empty_selections
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
        self._cache = None
        self._design_checker = design_checker
        self._fermata_start_offsets = []
        if final_barline not in (None, False, abjad.Exact):
            assert isinstance(final_barline, str), repr(final_barline)
        self._final_barline = final_barline
        if final_markup is not None:
            assert isinstance(final_markup, (tuple, list))
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
            assert isinstance(spacing_specifier, baca.HorizontalSpacingSpecifier)
        self._spacing_specifier = spacing_specifier
        if stage_label_base_string is not None:
            assert isinstance(stage_label_base_string, str)
        self._stage_label_base_string = stage_label_base_string
        self._metronome_mark_measure_map = metronome_mark_measure_map
        if transpose_score is not None:
            transpose_score = bool(transpose_score)
        self._transpose_score = transpose_score
        self._volta_measure_map = volta_measure_map
        self._wrappers = []

    ### SPECIAL METHODS ###

    def __call__(self, scopes, *commands):
        r'''Wraps each command in `commands` with each scope in `scopes`.

        ..  container:: example

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     baca.label(abjad.label().with_indices()),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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

        Returns none.
        '''
        prototype = (baca.Scope, baca.CompoundScope)
        if isinstance(scopes, prototype):
            scopes = [scopes]
        else:
            assert all(isinstance(_, prototype) for _ in scopes), repr(scopes)
        prototype = (baca.Builder, baca.Command)
        assert all(isinstance(_, prototype) for _ in commands)
        for scope in scopes:
            for command in commands:
                wrapper = baca.Wrapper(
                    command=command,
                    scope=scope,
                    )
                self.wrappers.append(wrapper)

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
        if self.final_barline == abjad.Exact:
            selection = abjad.select(self._score)
            last_leaf = selection._get_component(abjad.Leaf, -1)
            command = 'override Score.BarLine.transparent = ##f'
            command = abjad.LilyPondCommand(command)
            abjad.attach(command, last_leaf)

    def _add_final_markup(self):
        if self.final_markup is None:
            return
        command = baca.markup.final_markup(*self.final_markup)
        self._score.add_final_markup(
            command.arguments[0],
            extra_offset=self.final_markup_extra_offset,
            )

    def _apply_first_and_last_ties(self, voice):
        dummy_tie = abjad.Tie()
        for current_leaf in abjad.iterate(voice).leaves():
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
            segment = self._get_segment_identifier()
            print('can not find previous metadata before {segment}.')
            return
        for context in abjad.iterate(self._score).components(abjad.Context):
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
        for context in abjad.iterate(self._score).components(abjad.Context):
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
            print(f'spacing specifier time {total_time} seconds ...')
        if 3 < total_time:
            raise Exception(f'spacing specifier time {total_time} seconds!')

    def _assert_valid_stage_number(self, stage_number):
        if not 1 <= stage_number <= self.stage_count:
            message = f'must be 1 <= x <= {self.stage_count}: {stage_number}.'
            raise Exception(message)

    def _attach_fermatas(self):
        if not self.metronome_mark_measure_map:
            return
        context = self._score['Global Rests']
        directive_prototype = (
            abjad.Fermata,
            abjad.BreathMark,
            )
        rest_prototype = abjad.MultimeasureRest
        for stage_number, directive in self.metronome_mark_measure_map:
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
                    raise Exception(f'unknown fermata: {directive.command!r}.')
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
        if not self.metronome_mark_measure_map:
            return
        context = self._score['Global Skips']
        skips = abjad.select(context).leaves(abjad.Skip)
        left_broken_text = abjad.Markup().null()
        left_broken_text._direction = None
        spanner = abjad.MetronomeMarkSpanner(
            left_broken_padding=0,
            left_broken_text=left_broken_text,
            start_with_parenthesized_tempo=False,
            )
        abjad.attach(spanner, skips)
        for stage_number, directive in self.metronome_mark_measure_map:
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

    def _cache_leaves(self):
        stage_timespans = []
        for stage_index in range(self.stage_count):
            stage_number = stage_index + 1
            stage_offsets = self._get_offsets(stage_number, stage_number)
            stage_timespan = abjad.Timespan(*stage_offsets)
            stage_timespans.append(stage_timespan)
        self._cache = abjad.TypedOrderedDict()
        contexts = [self._score['Global Skips']]
        contexts.extend(abjad.select(self._score).components(abjad.Voice))
        for context in contexts:
            leaves_by_stage_number = abjad.TypedOrderedDict()
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

    def _check_design(self):
        if self.design_checker is None:
            return
        return self.design_checker(self._score)

    def _check_range(self):
        if not self.range_checker:
            return
        if isinstance(self.range_checker, abjad.PitchRange):
            markup = abjad.Markup('*', direction=abjad.Up)
            abjad.tweak(markup).color = 'red'
            for voice in abjad.iterate(self._score).components(abjad.Voice):
                for leaf in abjad.iterate(voice).leaves(pitched=True):
                    if leaf not in self.range_checker:
                        if self.color_out_of_range_pitches:
                            abjad.label(leaf).color_leaves('red')
                            abjad.attach(markup, leaf)
                        else:
                            raise Exception(f'out of range: {leaf!r}.')
        else:
            raise NotImplementedError(self.range_checker)

    def _check_wellformedness(self):
        if self.skip_wellformedness_checks:
            return
        score = self._lilypond_file['Score']
        if (self.color_octaves or
            self.color_repeat_pitch_classes or
            self.ignore_repeat_pitch_classes):
            return
        manager = baca.WellformednessManager()
        if not manager.is_well_formed(score):
            message = manager.tabulate_wellformedness(score)
            raise Exception(message)

    def _color_octaves_(self):
        if not self.color_octaves:
            return
        score = self._score
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
                    abjad.attach(markup, leaf)

    def _color_repeat_pitch_classes_(self):
        if not self.color_repeat_pitch_classes:
            return
        markup = abjad.Markup('@', direction=abjad.Up)
        abjad.tweak(markup).color = 'red'
        for voice in abjad.iterate(self._score).components(abjad.Voice):
            previous_logical_tie, previous_pitch_classes = None, []
            agent = abjad.iterate(voice)
            for logical_tie in agent.logical_ties(pitched=True):
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
        for pleaf in abjad.iterate(self._score).leaves(pitched=True):
            if abjad.inspect(pleaf).has_indicator('not yet pitched'):
                abjad.override(pleaf).beam.color = color
                abjad.override(pleaf).dots.color = color
                abjad.override(pleaf).flag.color = color
                abjad.override(pleaf).note_head.color = color
                abjad.override(pleaf).stem.color = color

    def _color_unregistered_pitches(self):
        if self.ignore_unregistered_pitches:
            return
        color = 'magenta'
        for pleaf in abjad.iterate(self._score).leaves(pitched=True):
            if abjad.inspect(pleaf).has_indicator('not yet registered'):
                abjad.override(pleaf).accidental.color = color
                abjad.override(pleaf).beam.color = color
                abjad.override(pleaf).dots.color = color
                abjad.override(pleaf).flag.color = color
                abjad.override(pleaf).note_head.color = color
                abjad.override(pleaf).stem.color = color

    def _contributions_do_not_overlap(self, contributions):
        previous_stop_offset = 0
        for contribution in contributions:
            if contribution.start_offset < previous_stop_offset:
                return False
            start_offset = contribution.start_offset
            duration = abjad.inspect(contribution.payload).get_duration()
            stop_offset = start_offset + duration
            previous_stop_offset = stop_offset
        return True

    def _detach_figure_names(self):
        if self.allow_figure_names:
            return
        for leaf in abjad.iterate(self._score).leaves():
            markups = abjad.inspect(leaf).get_indicators(abjad.Markup)
            for markup in markups:
                if (isinstance(markup._annotation, str) and
                    markup._annotation.startswith('figure name:')):
                    abjad.detach(markup, leaf)

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
        abjad.attach(beam, all_leaves)

    def _extend_beams(self):
        for leaf in abjad.iterate(self._score).leaves():
            if abjad.inspect(leaf).get_indicator(self._extend_beam_tag):
                self._extend_beam(leaf)

    def _get_end_clefs(self):
        result = abjad.TypedOrderedDict()
        staves = abjad.iterate(self._score).components(abjad.Staff)
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
        contexts = abjad.iterate(self._score).components(abjad.Context)
        contexts = list(contexts)
        contexts.sort(key=lambda x: x.name)
        for context in contexts:
            if not abjad.inspect(context).get_annotation('default_instrument'):
                continue
            leaf = abjad.inspect(context).get_leaf(-1)
            instrument = abjad.inspect(leaf).get_effective(abjad.Instrument)
            if instrument is None:
                print(f'can not find {context.name!r} end-instrument.')
            result[context.name] = instrument.name
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
            message = f'can not find {mark!r} in {self.metronome_marks!r}.'
            raise Exception(message)
        return name

    def _get_end_settings(self):
        result = {}
        if self._is_doc_example:
            return result
        result['end_clefs_by_staff'] = self._get_end_clefs()
        result['end_instruments_by_context'] = self._get_end_instruments()
        result['end_metronome_mark'] = self._get_end_metronome_mark()
        result['end_time_signature'] = self._get_end_time_signature()
        return result

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
        name = self._previous_metadata.get('end_metronome_mark')
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

    def _get_rhythm_wrappers_for_voice(self, voice_name):
        wrappers = []
        for wrapper in self.wrappers:
            if not isinstance(wrapper.command, baca.RhythmBuilder):
                continue
            if wrapper.scope.voice_name == voice_name:
                wrappers.append(wrapper)
        return wrappers

    def _get_segment_identifier(self):
        segment_name = self._metadata.get('segment_name')
        if segment_name is not None:
            return segment_name
        segment_number = self._get_segment_number()
        return segment_number

    def _get_segment_number(self):
        return self._metadata.get('segment_number', 1)

    def _get_stage_numbers(self, argument):
        if isinstance(argument, baca.StageSpecifier):
            start = argument.start
            stop = argument.stop
        elif isinstance(argument, tuple):
            start, stop = argument
        else:
            raise TypeError(f'must be specifier or tuple: {argument!r}.')
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
        contribution = baca.SegmentContribution(
            payload=time_signatures,
            start_offset=start_offset
            )
        return contribution

    def _handle_mutator(self, command):
        if (hasattr(command.command, '_mutates_score') and
            command.command._mutates_score()):
            self._cache = None

    def _hide_instrument_names_(self):
        if not self.hide_instrument_names:
            return
        classes = (abjad.Staff, abjad.StaffGroup)
        prototype = abjad.Instrument
        for staff in abjad.iterate(self._score).components(classes):
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
                raise Exception('overlapping offsets: {contribution!r}.')
            if previous_stop_offset < contribution.start_offset:
                selection = self._make_intercalated_rests(
                    previous_stop_offset,
                    contribution.start_offset,
                    pairs,
                    )
                result.append(selection)
            result.extend(contribution.payload)
            duration = abjad.inspect(contribution.payload).get_duration()
            previous_stop_offset = contribution.start_offset + duration
        if previous_stop_offset < segment_duration:
            selection = self._make_intercalated_rests(
                previous_stop_offset,
                segment_duration,
                pairs,
                )
            result.append(selection)
        return result

    def _interpret_commands(self):
        start_time = time.time()
        for wrapper in self.wrappers:
            assert isinstance(wrapper, baca.Wrapper)
            assert isinstance(wrapper.command, (baca.Builder, baca.Command))
            if isinstance(wrapper.command, baca.RhythmBuilder):
                continue
            selection = self._scope_to_leaf_selection(wrapper)
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

    def _interpret_rhythm_commands(self):
        self._make_music_for_time_signature_context()
        self._attach_tempo_indicators()
        self._attach_fermatas()
        self._make_spacing_regions()
        for voice in abjad.iterate(self._score).components(abjad.Voice):
            self._interpret_rhythm_commands_for_voice(voice)

    def _interpret_rhythm_commands_for_voice(self, voice):
        assert not len(voice), repr(voice)
        rhythm_commands = self._get_rhythm_wrappers_for_voice(voice.name)
        if not rhythm_commands:
            if self.skips_instead_of_rests:
                measures = self._make_skips()
            else:
                measures = self._make_rests()
            voice.extend(measures)
            return
        effective_staff = abjad.inspect(voice).get_effective_staff()
        effective_staff_name = effective_staff.context_name
        contributions = []
        for rhythm_command in rhythm_commands:
            assert isinstance(rhythm_command, baca.Wrapper)
            if rhythm_command.scope.stages is not None:
                result = self._get_stage_numbers(rhythm_command.scope.stages)
                contribution = self._get_time_signatures(*result)
            else:
                continue
            try:
                contribution = rhythm_command.command(
                    effective_staff_name,
                    start_offset=contribution.start_offset,
                    time_signatures=contribution.payload,
                    )
            except:
                raise Exception(format(rhythm_command))
            assert contribution.start_offset is not None
            contributions.append(contribution)
        contributions.sort(key=lambda _: _.start_offset)
        if not self._contributions_do_not_overlap(contributions):
            raise Exception(f'{voice.name!r} has overlapping rhythms.')
        contributions = self._intercalate_rests(contributions)
        voice.extend(contributions)
        self._apply_first_and_last_ties(voice)

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
        for skip in abjad.iterate(skip_context).leaves(abjad.Skip):
            start_offset = abjad.inspect(skip).get_timespan().start_offset
            if start_offset in self._fermata_start_offsets:
                continue
            skips.append(skip)
        skips = abjad.select(skips)
        abjad.label(skips).with_start_offsets(clock_time=True, font_size=-2)

    def _label_instrument_changes(self):
        prototype = abjad.Instrument
        for staff in abjad.iterate(self._score).components(abjad.Staff):
            leaves = abjad.iterate(staff).leaves()
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
                string = f'[{base}.{stage_number}]'
            else:
                string = f'[{stage_number}]'
            markup = abjad.Markup(string)
            markup = markup.with_color('blue')
            markup = markup.fontsize(-3)
            start_measure = context[start_measure_index]
            leaf = abjad.inspect(start_measure).get_leaf(0)
            abjad.attach(markup, leaf)

    def _make_instrument_change_markup(self, instrument):
        string = f'to {instrument.name}'
        markup = abjad.Markup(string, direction=abjad.Up)
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

    def _make_lilypond_file(
        self,
        is_doc_example=None,
        is_test=None,
        midi=None,
        ):
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
        if midi:
            block = abjad.Block(name='midi')
            lilypond_file.items.append(block)
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
        rhythm_commands = self._get_rhythm_wrappers_for_voice(voice_name)
        for rhythm_command in rhythm_commands:
            if rhythm_command.start_tempo is not None:
                start_tempo = abjad.new(rhythm_command.start_tempo)
                first_leaf = abjad.inspect(context).get_leaf(0)
                abjad.attach(start_tempo, first_leaf, scope=abjad.Score)
            if rhythm_command.stop_tempo is not None:
                stop_tempo = abjad.new(rhythm_command.stop_tempo)
                leaf = abjad.inspect(context).get_leaf(-1)
                abjad.attach(stop_tempo, leaf, scope=abjad.Score)

    def _make_rests(self, time_signatures=None):
        time_signatures = time_signatures or self.time_signatures
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
            agent = abjad.setting(start_skip)
            agent.score.proportional_notation_duration = moment

    def _make_volta_containers(self):
        if not self.volta_measure_map:
            return
        context = self._score['Global Skips']
        measures = context[:]
        for measure in measures:
            assert isinstance(measure, abjad.Measure), repr(measure)
        for specifier in self.volta_measure_map:
            if isinstance(specifier, baca.MeasureSpecifier):
                measure_start_number = specifier.start
                measure_stop_number = specifier.stop
            elif isinstance(specifier, baca.StageSliceSpecifier):
                start = specifier.start
                stop = specifier.stop
                pair = self._stage_number_to_measure_indices(start)
                measure_start_number, _ = pair
                stop -= 1
                pair = self._stage_number_to_measure_indices(stop)
                measure_stop_number = pair[-1] + 1
            else:
                raise TypeError(specifier)
            volta_measures = measures[measure_start_number:measure_stop_number]
            container = abjad.Container()
            abjad.mutate(volta_measures).wrap(container)
            command = abjad.Repeat()
            abjad.attach(command, container)

    def _populate_time_signature_context(self):
        context = self._score['Global Skips']
        measures = self._make_skip_filled_measures()
        context.extend(measures)
        context = self._score['Global Rests']
        measures = self._make_multimeasure_rest_filled_measures()
        context.extend(measures)

    def _print_cache(self):
        for context_name in self._cache:
            print(f'CONTEXT {context_name} ...')
            leaves_by_stage_number = self._cache[context_name]
            for stage_number in leaves_by_stage_number:
                print(f'STAGE {stage_number} ...')
                for leaf in leaves_by_stage_number[stage_number]:
                    print(leaf)

    def _print_segment_duration_(self):
        if not self.print_segment_duration:
            return
        context = self._score['Global Skips']
        current_tempo = None
        leaves = abjad.iterate(context).leaves()
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
            if abjad.inspect(leaf).has_indicator(abjad.Accelerando):
                is_trending = True
            if abjad.inspect(leaf).has_indicator(abjad.Ritardando):
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
        counter = abjad.Strin('second').pluralize(total_duration)
        print(f'segment duration {total_duration} {counter} ...')

    # TODO: refactor as _scope_to_leaf_selections() in plural
    def _scope_to_leaf_selection(self, wrapper):
        leaves = []
        selections = self._scope_to_leaf_selections(wrapper.scope)
        for selection in selections:
            leaves.extend(selection)
        selection = abjad.select(leaves)
        if not selection:
            message = f'EMPTY SELECTION: {format(wrapper)}'
            if self.allow_empty_selections:
                print(message)
            else:
                raise Exception(message)
        return selection

    def _scope_to_leaf_selections(self, scope):
        if self._cache is None:
            self._cache_leaves()
        if isinstance(scope, baca.Scope):
            scopes = [scope]
        else:
            assert isinstance(scope, baca.CompoundScope)
            scopes = list(scope.scopes)
        leaf_selections = []
        for scope in scopes:
            leaves = []
            leaves_by_stage_number = self._cache[scope.voice_name]
            start = scope.stages.start
            if (scope.stages.stop == abjad.Infinity or
                scope.stages.stop is abjad.Infinity):
                stop = self.stage_count + 1
            else:
                stop = scope.stages.stop + 1
            for stage_number in range(start, stop):
                leaves.extend(leaves_by_stage_number[stage_number])
            leaf_selections.append(abjad.select(leaves))
        return leaf_selections

    def _shorten_long_repeat_ties(self):
        leaves = abjad.iterate(self._score).leaves()
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
        elif stage_number == Infinity:
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

    def _transpose_score_(self):
        if self.transpose_score:
            abjad.Instrument.transpose_from_sounding_pitch(self._score)

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
        return self._allow_empty_selections

    @property
    def allow_figure_names(self):
        r'''Is true when segment allows figure names.

        Is false when segment strips figure names.

        ..  container:: example

            Strips figure names by default:

                >>> music_maker = baca.MusicMaker()

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

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     spacing_specifier=baca.HorizontalSpacingSpecifier(
            ...         minimum_width=abjad.Duration(1, 24),
            ...         ),
            ...     time_signatures=time_signatures,
            ...     )
            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.RhythmBuilder(
            ...         rhythm_maker=figures,
            ...         ),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                        \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                        \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                        \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     allow_figure_names=True,
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     spacing_specifier=baca.HorizontalSpacingSpecifier(
            ...         minimum_width=abjad.Duration(1, 24),
            ...         ),
            ...     time_signatures=time_signatures,
            ...     )
            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.RhythmBuilder(
            ...         rhythm_maker=figures,
            ...         ),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).text_script.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                        \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                        \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                        \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     color_octaves=True,
            ...     score_template=baca.StringTrioScoreTemplate(),
            ...     spacing_specifier=baca.HorizontalSpacingSpecifier(
            ...         minimum_width=abjad.Duration(1, 24),
            ...         ),
            ...     time_signatures=[abjad.TimeSignature((6, 16))],
            ...     )

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Violin Music Voice',
            ...     [[2, 4, 5, 7, 9, 11]],
            ...     )
            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.RhythmBuilder(
            ...         rhythm_maker=contribution['Violin Music Voice'],
            ...         ),
            ...     )

            >>> contribution = music_maker(
            ...     'Cello Music Voice',
            ...     [[-3, -5, -7, -8, -10, -12]],
            ...     )
            >>> segment_maker(
            ...     baca.scope('Cello Music Voice', 1),
            ...     baca.RhythmBuilder(
            ...         rhythm_maker=contribution['Cello Music Voice'],
            ...         ),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                            \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                            \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                            \clef "treble"
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
                                    \set ViolaMusicStaff.instrumentName = \markup { Viola }
                                    \set ViolaMusicStaff.shortInstrumentName = \markup { Va. }
                                    \clef "alto"
                                    R1 * 3/8
                                    \bar "|"
                                }
                            }
                            \tag cello
                            \context CelloMusicStaff = "Cello Music Staff" {
                                \context CelloMusicVoice = "Cello Music Voice" {
                                    {
                                        {
                                            \set CelloMusicStaff.instrumentName = \markup { Cello }
                                            \set CelloMusicStaff.shortInstrumentName = \markup { Vc. }
                                            \clef "bass"
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

            >>> pitch_range = abjad.instrumenttools.Violin().pitch_range
            >>> segment_maker = baca.SegmentMaker(
            ...     color_out_of_range_pitches=True,
            ...     range_checker=pitch_range,
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     spacing_specifier=baca.HorizontalSpacingSpecifier(
            ...         minimum_width=abjad.Duration(1, 24),
            ...         ),
            ...     time_signatures=time_signatures,
            ...     )
            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.RhythmBuilder(
            ...         rhythm_maker=figures,
            ...         ),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                        \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                        \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                        \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     color_repeat_pitch_classes=True,
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     spacing_specifier=baca.HorizontalSpacingSpecifier(
            ...         minimum_width=abjad.Duration(1, 24),
            ...         ),
            ...     time_signatures=time_signatures,
            ...     )
            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.RhythmBuilder(
            ...         rhythm_maker=figures,
            ...         ),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                        \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                        \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                        \clef "treble"
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
    #       for mensurstriche final_barline=abjad.Exact
    @property
    def final_barline(self):
        r'''Gets final barline.

        ..  container:: example

            Nonlast segment sets final barline to ``'|'`` by default:

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     )

            >>> metadata = {'segment_count': 1}
            >>> result = segment_maker.run(
            ...     is_doc_example=True,
            ...     metadata=metadata,
            ...     )
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     final_barline='||',
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     final_barline='||',
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     )

            >>> metadata = {'segment_count': 1}
            >>> result = segment_maker.run(
            ...     is_doc_example=True,
            ...     metadata=metadata,
            ...     )
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     final_barline='|.',
            ...     final_markup=(['Madison, WI'], ['October 2016']),
            ...     final_markup_extra_offset=(-9, -2),
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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
                                    c'8 ]
                                        _ \markup {
                                            \whiteout
                                                \upright
                                                    \with-color
                                                        #black
                                                        \right-column
                                                            {
                                                                \line
                                                                    {
                                                                        "Madison, WI"
                                                                    }
                                                                \line
                                                                    {
                                                                        "October 2016"
                                                                    }
                                                            }
                                            }
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

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     spacing_specifier=baca.HorizontalSpacingSpecifier(
            ...         minimum_width=abjad.Duration(1, 24),
            ...         ),
            ...     time_signatures=time_signatures,
            ...     )
            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.RhythmBuilder(
            ...         rhythm_maker=figures,
            ...         ),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                        \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                        \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                        \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     ignore_unregistered_pitches=True,
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     spacing_specifier=baca.HorizontalSpacingSpecifier(
            ...         minimum_width=abjad.Duration(1, 24),
            ...         ),
            ...     time_signatures=time_signatures,
            ...     )
            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.RhythmBuilder(
            ...         rhythm_maker=figures,
            ...         ),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).spacing_spanner.strict_grace_spacing = False
            >>> abjad.override(score).spacing_spanner.strict_note_spacing = False
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                        \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                        \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                        \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     metronome_mark_measure_map=baca.MetronomeMarkMeasureMap([
            ...         (1, abjad.MetronomeMark((1, 8), 90)),
            ...         ]),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     label_clock_time=True,
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     metronome_mark_measure_map=baca.MetronomeMarkMeasureMap([
            ...         (1, abjad.MetronomeMark((1, 8), 90)),
            ...         ]),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True) # doctest: +SKIP
            >>> lilypond_file, metadata = result # doctest: +SKIP
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  todo:: MAKE THIS WORK AGAIN.

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     label_stages=True,
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     label_stages=True,
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     )

            >>> metadata = {'name': 'K'}
            >>> result = segment_maker.run(
            ...     is_doc_example=True,
            ...     metadata=metadata,
            ...     )
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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
    def metronome_mark_measure_map(self):
        r'''Gets metronome mark measure map.

        ..  container:: example

            Without metronome mark measure map:

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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

            With metronome mark measure map:

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     metronome_mark_measure_map=baca.MetronomeMarkMeasureMap([
            ...         (1, abjad.MetronomeMark((1, 8), 90)),
            ...         ]),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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

        Set to metornome mark measure map or none.

        Returns metornome mark measure map or none.
        '''
        return self._metronome_mark_measure_map

    @property
    def metronome_marks(self):
        r'''Gets metronome marks.

        Returns typed ordered dictionary or none.
        '''
        return self._metronome_marks

    @property
    def midi(self):
        r'''Is true when segment-maker outputs MIDI.

        Returns true, false or none.
        '''
        return self._midi

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
    def score_template(self):
        r'''Gets score template.

        ..  container:: example

            Gets none:

            >>> segment_maker = baca.SegmentMaker()

            >>> segment_maker.score_template is None
            True

        ..  container:: example

            Gets score template:

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     )

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

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     skips_instead_of_rests=True,
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     label_stages=True,
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     )

            >>> metadata = {'name': 'K'}
            >>> result = segment_maker.run(
            ...     is_doc_example=True,
            ...     metadata=metadata,
            ...     )
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     label_stages=True,
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     stage_label_base_string='intermezzo',
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     )

            >>> metadata = {'name': 'K'}
            >>> result = segment_maker.run(
            ...     is_doc_example=True,
            ...     metadata=metadata,
            ...     )
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     baca.pitches('E4 F4'),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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
            Must pass in instrument manifest.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._transpose_score

    @property
    def volta_measure_map(self):
        r'''Gets volta measure map.

        ..  container:: example

            Without volta measure map.

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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

            With volta measure map:

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     volta_measure_map=baca.VoltaMeasureMap([
            ...         baca.MeasureSpecifier(1, 2),
            ...         ]),
            ...     )

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.even_runs(),
            ...     )

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
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

        Set to volta measure map or none.

        Returns volta measure map or none.
        '''
        return self._volta_measure_map

    @property
    def wrappers(self):
        r'''Gets wrappers.

        Returns list of wrappers.
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
            if not isinstance(wrapper.command, baca.RhythmBuilder):
                continue
            if wrapper.scope.voice_name != source.voice_name:
                continue
            assert isinstance(wrapper.scope.stages, baca.StageSpecifier)
            start = wrapper.scope.stages.start
            stop = wrapper.scope.stages.stop + 1
            stages = range(start, stop)
            if source.stages.start in stages:
                break
        else:
            raise Exception(f'no {voice_name!r} rhythm command for {stage}.')
        assert isinstance(wrapper, baca.Wrapper)
        assert isinstance(wrapper.command, baca.RhythmBuilder)
        command = abjad.new(wrapper.command, **keywords)
        wrapper = baca.Wrapper(command, target)
        self.wrappers.append(wrapper)

    def run(
        self,
        is_doc_example=None,
        is_test=None,
        metadata=None,
        midi=None,
        previous_metadata=None,
        ):
        r'''Runs segment-maker.

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
            midi=midi,
            )
        self._populate_time_signature_context()
        self._label_stage_numbers_()
        self._interpret_rhythm_commands()
        self._extend_beams()
        self._interpret_commands()
        self._detach_figure_names()
        self._shorten_long_repeat_ties()
        self._apply_previous_segment_end_settings()
        self._attach_first_segment_score_template_defaults()
        self._apply_spacing_specifier()
        self._make_volta_containers()
        self._label_clock_time_()
        self._hide_instrument_names_()
        self._label_instrument_changes()
        self._transpose_score_()
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

    def validate_measure_count(self, measure_count):
        r'''Validates measure count.

        Raises exception when `measure_count` is incorrect.

        Returns none.
        '''
        if not measure_count == self.measure_count:
            message = f'segment measure count is not {measure_count}'
            message += f' but {self.measure_count}.'
            raise Exception(message)

    def validate_measures_per_stage(self):
        r'''Validates measures per stage.

        Raises exception when measures per stage do not match measure count.

        Returns none.
        '''
        if self.measures_per_stage is None:
            return
        if not sum(self.measures_per_stage) == self.measure_count:
            message = f'measures per stage {self.measures_per_stage}'
            message += f' do not match measure count {self.measure_count}.'
            raise Exception(message)

    def validate_stage_count(self, stage_count):
        r'''Validates stage count.

        Raises exception when `stage_count` is incorrect.

        Returns none.
        '''
        if not stage_count == self.stage_count:
            message = f'segment stage count is not {stage_count}'
            message += f' but {self.stage_count}.'
            raise Exception(message)
