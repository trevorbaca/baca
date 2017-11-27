import abjad
import baca
import os
import pathlib
import time
import traceback
from abjad import rhythmmakertools as rhythmos


class SegmentMaker(abjad.SegmentMaker):
    r'''Segment-maker.

    >>> from abjad import rhythmmakertools as rhythmos

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \time 4/8
                        \bar "" % SEGMENT:EMPTY-BAR
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 2] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
            <BLANKLINE>
                            %%% MusicVoice [measure 1] %%%
                            \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                            \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                            R1 * 1/2
            <BLANKLINE>
                            %%% MusicVoice [measure 2] %%%
                            R1 * 3/8
            <BLANKLINE>
                            %%% MusicVoice [measure 3] %%%
                            R1 * 1/2
            <BLANKLINE>
                            %%% MusicVoice [measure 4] %%%
                            R1 * 3/8
                            \bar "|"
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.make_even_runs(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \time 4/8
                        \bar "" % SEGMENT:EMPTY-BAR
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 2] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                c'8 [
            <BLANKLINE>
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8
            <BLANKLINE>
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8
            <BLANKLINE>
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8 [
            <BLANKLINE>
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8
            <BLANKLINE>
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8 [
            <BLANKLINE>
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8
            <BLANKLINE>
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8
            <BLANKLINE>
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8 [
            <BLANKLINE>
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8
            <BLANKLINE>
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override Flag.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'8 ]
                                \bar "|"
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

        Segment-maker colors unpitched notes blue.

    '''

    ### CLASS ATTRIBUTES ###

    __documentation_section__ = '(2) Makers'

    __slots__ = (
        '_allow_empty_selections',
        '_allow_figure_names',
        '_break_offsets',
        '_builds_metadata',
        '_cache',
        '_color_octaves',
        '_color_out_of_range_pitches',
        '_color_repeat_pitch_classes',
        '_design_checker',
        '_end_staff_lines_by_staff',
        '_fermata_measure_staff_line_count',
        '_fermata_start_offsets',
        '_final_bar_line',
        '_final_markup',
        '_final_markup_extra_offset',
        '_hide_instrument_names',
        '_ignore_repeat_pitch_classes',
        '_ignore_unpitched_notes',
        '_ignore_unregistered_pitches',
        '_instruments',
        '_label_clock_time',
        '_label_stage_numbers',
        '_layout_measure_map',
        '_measures_per_stage',
        '_metronome_mark_measure_map',
        '_metronome_marks',
        '_print_segment_duration',
        '_print_timings',
        '_range_checker',
        '_rehearsal_letter',
        '_score',
        '_score_template',
        '_segment_duration',
        '_skip_wellformedness_checks',
        '_skips_instead_of_rests',
        '_spacing_specifier',
        '_stage_label_base_string',
        '_time_signatures',
        '_transpose_score',
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
        fermata_measure_staff_line_count=None,
        final_bar_line=None,
        final_markup=None,
        final_markup_extra_offset=None,
        hide_instrument_names=None,
        ignore_repeat_pitch_classes=None,
        ignore_unpitched_notes=None,
        ignore_unregistered_pitches=None,
        instruments=None,
        label_clock_time=None,
        label_stages=None,
        layout_measure_map=None,
        measures_per_stage=None,
        metronome_mark_measure_map=None,
        metronome_marks=None,
        print_segment_duration=None,
        print_timings=None,
        range_checker=None,
        rehearsal_letter=None,
        score_template=None,
        skip_wellformedness_checks=None,
        skips_instead_of_rests=None,
        spacing_specifier=None,
        stage_label_base_string=None,
        time_signatures=None,
        transpose_score=None,
        ):
        super(SegmentMaker, self).__init__()
        if allow_empty_selections is not None:
            allow_empty_selections = bool(allow_empty_selections)
        self._allow_empty_selections = allow_empty_selections
        if allow_figure_names is not None:
            allow_figure_names = bool(allow_figure_names)
        self._allow_figure_names = allow_figure_names
        self._break_offsets = []
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
        self._end_staff_lines_by_staff = abjad.TypedOrderedDict()
        if fermata_measure_staff_line_count is not None:
            assert isinstance(fermata_measure_staff_line_count, int)
            assert 0 <= fermata_measure_staff_line_count
        self._fermata_measure_staff_line_count = fermata_measure_staff_line_count
        self._fermata_start_offsets = []
        if final_bar_line not in (None, False, abjad.Exact):
            assert isinstance(final_bar_line, str), repr(final_bar_line)
        self._final_bar_line = final_bar_line
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
        if layout_measure_map is not None:
            assert isinstance(layout_measure_map, baca.LayoutMeasureMap)
        self._layout_measure_map = layout_measure_map
        self._measures_per_stage = measures_per_stage
        self._metronome_mark_measure_map = metronome_mark_measure_map
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
        self._segment_duration = None
        if skip_wellformedness_checks is not None:
            skip_wellformedness_checks = bool(skip_wellformedness_checks)
        self._skip_wellformedness_checks = skip_wellformedness_checks
        if skips_instead_of_rests is not None:
            skips_instead_of_rests = bool(skips_instead_of_rests)
        self._skips_instead_of_rests = skips_instead_of_rests
        if spacing_specifier is not None:
            assert isinstance(spacing_specifier, baca.HorizontalSpacingSpecifier)
        self._spacing_specifier = spacing_specifier
        if stage_label_base_string is not None:
            assert isinstance(stage_label_base_string, str)
        self._stage_label_base_string = stage_label_base_string
        if transpose_score is not None:
            transpose_score = bool(transpose_score)
        self._transpose_score = transpose_score
        self._wrappers = []

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 1] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    c'8 [
                                        ^ \markup {
                                            \small
                                                0
                                            }
                <BLANKLINE>
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
                <BLANKLINE>
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
                <BLANKLINE>
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
                <BLANKLINE>
                                    %%% MusicVoice [measure 2] %%%
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
                <BLANKLINE>
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
                <BLANKLINE>
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
                <BLANKLINE>
                                    %%% MusicVoice [measure 3] %%%
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
                <BLANKLINE>
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
                <BLANKLINE>
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
                <BLANKLINE>
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
                <BLANKLINE>
                                    %%% MusicVoice [measure 4] %%%
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
                <BLANKLINE>
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
                <BLANKLINE>
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
        abbreviation = '|'
        if self._is_last_segment():
            abbreviation = '|.'
        if isinstance(self.final_bar_line, str):
            abbreviation = self.final_bar_line
        self._score.add_final_bar_line(
            abbreviation=abbreviation,
            to_each_voice=True,
            )
        if self.final_bar_line == abjad.Exact:
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
            command.indicators[0],
            extra_offset=self.final_markup_extra_offset,
            )

    def _apply_fermata_measure_staff_line_count(self):
        if self.fermata_measure_staff_line_count is None:
            return
        if not self._fermata_start_offsets:
            return
        self._attach_fermata_measure_adjustments(self._break_offsets)
        for build_name, build_metadata in self._builds_metadata.items():
            break_measure_numbers = build_metadata.get('break_measures')
            break_measure_timespans = self._get_measure_timespans(
                break_measure_numbers)
            break_measure_stop_offsets = [
                _.stop_offset for _ in break_measure_timespans
                ]
            if break_measure_stop_offsets:
                self._attach_fermata_measure_adjustments(
                    break_measure_stop_offsets,
                    build_name,
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
                        repeat_ties = inspector.has_indicator(
                            'use messiaen style ties')
                        tie = abjad.Tie(
                            repeat_ties=repeat_ties)
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
                        repeat_ties = inspector.has_indicator(
                            'use messiaen style ties')
                        tie = abjad.Tie(
                            repeat_ties=repeat_ties)
                        abjad.attach(tie, leaves)
                abjad.detach('tie from me', current_leaf)

    def _apply_layout_measure_map(self):
        if self.layout_measure_map is None:
            return
        self.layout_measure_map(self._score['GlobalSkips'])

    def _apply_spacing_specifier(self):
        start_time = time.time()
        if self.spacing_specifier is None:
            return
        self.spacing_specifier(self)
        stop_time = time.time()
        total_time = int(stop_time - start_time)
        if self.print_timings:
            print(f'spacing specifier time {total_time} seconds ...')
        if os.getenv('TRAVIS'):
            return
        if 3 < total_time:
            raise Exception(f'spacing specifier time {total_time} seconds!')

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

    def _attach_fermata_measure_adjustments(self, break_offsets, build=None):
        prototype = baca.StaffLines
        staff_lines = baca.StaffLines(self.fermata_measure_staff_line_count)
        breaks_already_treated = []
        if build is None:
            tag = 'SEGMENT'
        else:
            tag = 'BUILD:' + build.upper()
        tag += ':FERMATA-MEASURE-TREATMENT'
        for staff in abjad.iterate(self._score).components(abjad.Staff):
            for leaf in abjad.iterate(staff).leaves():
                start_offset = abjad.inspect(leaf).get_timespan().start_offset
                if start_offset not in self._fermata_start_offsets:
                    continue
                leaf_stop = abjad.inspect(leaf).get_timespan().stop_offset
                ends_at_break = leaf_stop in break_offsets
                before = abjad.inspect(leaf).get_effective(prototype)
                next_leaf = abjad.inspect(leaf).get_leaf(1)
                if next_leaf is not None:
                    after = abjad.inspect(next_leaf).get_effective(prototype)
                if before != staff_lines:
                    if build is None:
                        abjad.attach(staff_lines, leaf)
                    if getattr(before, 'line_count', 5) == 5:
                        pair = (-2, 2)
                        abjad.override(leaf).staff.bar_line.bar_extent = pair
                if next_leaf is not None and staff_lines != after:
                    abjad.attach(after, next_leaf)
                if ends_at_break and leaf_stop not in breaks_already_treated:
                    if staff_lines.line_count == 0:
                        string = r'\override Score.BarLine.transparent = ##t'
                        string = r'\once ' + string
                        literal = abjad.LilyPondLiteral(string, 'after')
                        abjad.attach(literal, leaf, tag=tag)
                        string = r'\override Score.SpanBar.transparent = ##t'
                        string = r'\once ' + string
                        literal = abjad.LilyPondLiteral(string, 'after')
                        abjad.attach(literal, leaf, tag=tag)
                    elif staff_lines.line_count == 1:
                        string = "Score.BarLine.bar-extent = #'(-2 . 2)"
                        string = r'\once \override ' + string
                        literal = abjad.LilyPondLiteral(string, 'after')
                        abjad.attach(literal, leaf, tag=tag)
                    breaks_already_treated.append(leaf_stop)
                if (build is None and
                    next_leaf is None and
                    before != staff_lines):
                    name = staff.name
                    before_line_count = getattr(before, 'line_count', 5)
                    self._end_staff_lines_by_staff[name] = before_line_count

    def _attach_fermatas(self):
        if not self.metronome_mark_measure_map:
            del(self._score['GlobalRests'])
            return
        has_fermata = False
        for entry in self.metronome_mark_measure_map:
            if isinstance(entry[1], abjad.Fermata):
                has_fermata = True
        if not has_fermata:
            del(self._score['GlobalRests'])
            return
        context = self._score['GlobalRests']
        rests = self._make_multimeasure_rests()
        context.extend(rests)
        directive_prototype = (
            abjad.BreathMark,
            abjad.Fermata,
            )
        for stage_number, directive in self.metronome_mark_measure_map:
            if not isinstance(directive, directive_prototype):
                continue
            assert 0 < stage_number <= self.stage_count
            result = self._stage_number_to_measure_indices(stage_number)
            start_measure_index, stop_measure_index = result
            rest = context[start_measure_index]
            assert isinstance(rest, abjad.MultimeasureRest)
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
            abjad.attach(directive, rest)
            if fermata_y_offset is not None:
                proxy = abjad.override(rest).multi_measure_rest_text
                proxy.extra_offset = (0, fermata_y_offset)
            proxy = abjad.override(rest)
            proxy.score.multi_measure_rest.transparent = True
            abjad.override(rest).score.time_signature.stencil = False
            abjad.attach('fermata measure', rest)
            start_offset = abjad.inspect(rest).get_timespan().start_offset
            self._fermata_start_offsets.append(start_offset)

    def _attach_first_segment_score_template_defaults(self):
        if self._is_first_segment():
            self.score_template.attach_defaults(self._score)

    def _attach_metronome_marks(self):
        skips = baca.select(self._score['GlobalSkips']).skips()
        left_broken_text = abjad.Markup().null()
        left_broken_text = abjad.new(left_broken_text, direction=None)
        spanner = abjad.MetronomeMarkSpanner(
            left_broken_padding=0,
            left_broken_text=left_broken_text,
            start_with_parenthesized_tempo=False,
            )
        abjad.attach(spanner, skips)
        if not self.metronome_mark_measure_map:
            return
        for stage_number, directive in self.metronome_mark_measure_map:
            self._assert_valid_stage_number(stage_number)
            start, _ = self._stage_number_to_measure_indices(stage_number)
            skip = skips[start]
            spanner.attach(directive, skip)

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
        skip = baca.select(self._score['GlobalSkips']).skip(0)
        abjad.attach(rehearsal_mark, skip)

    def _blacken_explicit_contexted_indicators(self):
        for leaf in abjad.iterate(self._score).leaves():
            wrapper = abjad.inspect(leaf).get_indicator(
                abjad.Clef,
                unwrap=False,
                )
            if wrapper is not None and wrapper.tag is None:
                tag = 'SEGMENT:EXPLICIT-CONTEXTED-INDICATOR'
                clef = wrapper.indicator
                context = wrapper.context
                string = self._color_explicit('Clef', context, once=False)
                literal = abjad.LilyPondLiteral(string)
                abjad.attach(literal, leaf, tag=tag)
                abjad.detach(clef, leaf)
                abjad.attach(clef, leaf, context=context, tag=tag)

    def _cache_break_offsets(self):
        prototype = (abjad.LineBreak, abjad.PageBreak)
        for skip in baca.select(self._score['GlobalSkips']).skips():
            if abjad.inspect(skip).has_indicator(prototype):
                offset = abjad.inspect(skip).get_timespan().start_offset
                self._break_offsets.append(offset)
        segment_stop_offset = abjad.inspect(skip).get_timespan().stop_offset
        self._break_offsets.append(segment_stop_offset)

    def _cache_leaves(self):
        stage_timespans = []
        for stage_index in range(self.stage_count):
            stage_number = stage_index + 1
            stage_offsets = self._get_stage_offsets(stage_number, stage_number)
            stage_timespan = abjad.Timespan(*stage_offsets)
            stage_timespans.append(stage_timespan)
        self._cache = abjad.TypedOrderedDict()
        contexts = [self._score['GlobalSkips']]
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

    def _call_commands(self):
        start_time = time.time()
        for wrapper in self.wrappers:
            assert isinstance(wrapper, baca.CommandWrapper)
            assert isinstance(wrapper.command, baca.Command)
            if isinstance(wrapper.command, baca.RhythmCommand):
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

    def _call_rhythm_commands(self):
        self._attach_metronome_marks()
        self._attach_fermatas()
        for voice in abjad.iterate(self._score).components(abjad.Voice):
            assert not len(voice), repr(voice)
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
                result = self._get_stage_time_signatures(*wrapper.scope.stages)
                start_offset, time_signatures = result
                try:
                    rhythm = wrapper.command(start_offset, time_signatures)
                except:
                    raise Exception(format(wrapper))
                rhythms.append(rhythm)
            rhythms.sort()
            self._assert_nonoverlapping_rhythms(rhythms, voice.name)
            rhythms = self._intercalate_silences(rhythms)
            voice.extend(rhythms)
            self._apply_first_and_last_ties(voice)

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

    @staticmethod
    def _color_duplicate(grob, context=None, once=True):
        if context is not None:
            context = getattr(context, 'context_name', context)
            string = rf'\override {context}.{grob}.color ='
        else:
            string = rf'\override {grob}.color ='
        if once:
            string = rf'\once {string}'
        string += " #(x11-color 'DeepPink1)"
        return string

    @staticmethod
    def _color_explicit(grob, context=None, once=True):
        if context is not None:
            context = getattr(context, 'context_name', context)
            string = rf'\override {context}.{grob}.color ='
        else:
            string = rf'\override {grob}.color ='
        if once:
            string = rf'\once {string}'
        string += " #(x11-color 'black)"
        return string


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

    @staticmethod
    def _color_reapplied(grob, context=None):
        if context is not None:
            context = getattr(context, 'context_name', context)
            string = rf'\once \override {context}.{grob}.color ='
        else:
            string = rf'\once \override {grob}.color ='
        string += " #(x11-color 'DarkBlue)"
        return string

    @staticmethod
    def _color_reminder(grob, context=None):
        if context is not None:
            context = getattr(context, 'context_name', context)
            string = rf'\once \override {context}.{grob}.color ='
        else:
            string = rf'\once \override {grob}.color ='
        string += " #(x11-color 'DarkCyan)"
        return string

    @staticmethod
    def _color_restated(grob, context=None, once=True):
        if context is not None:
            context = getattr(context, 'context_name', context)
            string = rf'\override {context}.{grob}.color ='
        else:
            string = rf'\override {grob}.color ='
        if once:
            string = rf'\once {string}'
        string = f"{string} #(x11-color 'ForestGreen)"
        return string

    def _color_repeat_pitch_classes_(self):
        manager = baca.WellformednessManager
        lts = manager._find_repeat_pitch_classes(self._score)
        markup = abjad.Markup('@', direction=abjad.Up)
        abjad.tweak(markup).color = 'red'
        for lt in lts:
            abjad.label(lt).color_leaves('red')
            for leaf in lt:
                abjad.attach(markup, leaf)

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

    def _comment_measure_numbers(self):
        offset_to_measure_number = {}
        measure_number = self._metadata.get('first_bar_number', 1)
        for skip in baca.select(self._score['GlobalSkips']).skips():
            offset = abjad.inspect(skip).get_timespan().start_offset
            offset_to_measure_number[offset] = measure_number
            measure_number += 1
        contexts = []
        contexts.extend(self._score['GlobalContext'])
        contexts.extend(abjad.iterate(self._score).components(abjad.Voice))
        for context in contexts:
            for leaf in abjad.iterate(context).leaves():
                offset = abjad.inspect(leaf).get_timespan().start_offset
                measure_number = offset_to_measure_number.get(offset, None)
                if measure_number is None:
                    continue
                string = f'%%% {context.name} [measure {measure_number}] %%%'
                literal = abjad.LilyPondLiteral(string, 'absolute_before')
                abjad.attach(literal, leaf)

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
        staves.sort(key=lambda _: _.name)
        for staff in staves:
            last_leaf = abjad.inspect(staff).get_leaf(-1)
            clef = abjad.inspect(last_leaf).get_effective(abjad.Clef)
            if clef:
                result[staff.name] = clef.name
            else:
                result[staff.name] = None
        return result

    def _get_end_dynamics(self):
        result = abjad.TypedOrderedDict()
        voices = abjad.iterate(self._score).components(abjad.Voice)
        voices = list(voices)
        voices.sort(key=lambda _: _.name)
        for voice in voices:
            leaf = abjad.inspect(voice).get_leaf(-1)
            dynamic = abjad.inspect(leaf).get_effective(abjad.Dynamic)
            if dynamic is not None:
                result[voice.name] = dynamic.name
        return result

    def _get_end_instruments(self):
        result = abjad.TypedOrderedDict()
        contexts = abjad.iterate(self._score).components(abjad.Context)
        contexts = list(contexts)
        contexts.sort(key=lambda _: _.name)
        for context in contexts:
            if not abjad.inspect(context).get_annotation('default_instrument'):
                continue
            leaf = abjad.inspect(context).get_leaf(-1)
            instrument = abjad.inspect(leaf).get_effective(abjad.Instrument)
            if instrument is not None:
                result[context.name] = instrument.name
            else:
                print(f'can not find {context.name!r} end-instrument.')
        return result

    def _get_end_metronome_mark(self):
        skip = baca.select(self._score['GlobalSkips']).skip(-1)
        mark = abjad.inspect(skip).get_effective(abjad.MetronomeMark)
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

    def _get_end_settings(self, docs=None):
        result = {}
        if docs:
            return result
        result['end_clefs_by_staff'] = self._get_end_clefs()
        result['end_dynamics_by_context'] = self._get_end_dynamics()
        result['end_instruments_by_context'] = self._get_end_instruments()
        result['end_metronome_mark'] = self._get_end_metronome_mark()
        result['end_staff_lines_by_staff'] = self._get_end_staff_lines()
        result['end_time_signature'] = self._get_end_time_signature()
        result['time_signatures'] = self._get_time_signatures()
        return result

    def _get_end_staff_lines(self):
        if self._end_staff_lines_by_staff:
            return self._end_staff_lines_by_staff
        result = abjad.TypedOrderedDict()
        staves = abjad.iterate(self._score).components(abjad.Staff)
        staves = list(staves)
        staves.sort(key=lambda _: _.name)
        for staff in staves:
            leaf = abjad.inspect(staff).get_leaf(-1)
            lines = abjad.inspect(leaf).get_effective(baca.StaffLines)
            if lines is not None:
                result[staff.name] = lines.line_count
        return result

    def _get_end_time_signature(self):
        skip = baca.select(self._score['GlobalSkips']).skip(-1)
        time_signature = abjad.inspect(skip).get_effective(abjad.TimeSignature)
        if not time_signature:
            return
        string = str(time_signature)
        return string

    def _get_first_measure_number(self):
        return self._metadata.get('first_bar_number', 1)

    def _get_measure_timespans(self, measure_numbers):
        timespans = []
        first_measure_number = self._get_first_measure_number()
        measure_indices = [
            _ - first_measure_number - 1 for _ in measure_numbers
            ]
        skips = baca.select(self._score['GlobalSkips']).skips()
        for i, skip in enumerate(skips):
            if i in measure_indices:
                timespan = abjad.inspect(skip).get_timespan()
                timespans.append(timespan)
        return timespans

    def _get_name(self):
        return self._metadata.get('name')

    def _get_previous_clef(self, context):
        if not self._previous_metadata:
            return
        string = 'end_clefs_by_staff'
        dictionary = self._previous_metadata.get(string)
        if dictionary:
            clef_name = dictionary.get(context)
            if clef_name is not None:
                return abjad.Clef(clef_name)

    def _get_previous_dynamic(self, context):
        if not self._previous_metadata:
            return
        string = 'end_dynamics_by_context'
        dictionary = self._previous_metadata.get(string)
        if dictionary:
            dynamic_name = dictionary.get(context)
            if dynamic_name is not None:
                return abjad.Dynamic(dynamic_name)

    def _get_previous_instrument(self, context):
        if not self._previous_metadata:
            return
        string = 'end_instruments_by_context'
        dictionary = self._previous_metadata.get(string)
        if dictionary:
            instrument_name = dictionary.get(context)
            return self.instruments.get(instrument_name)

    def _get_previous_metronome_mark(self):
        if not self._previous_metadata:
            return
        name = self._previous_metadata.get('end_metronome_mark')
        return self.metronome_marks.get(name)

    def _get_previous_staff_lines(self, context):
        if not self._previous_metadata:
            return
        string = 'end_staff_lines_by_staff'
        dictionary = self._previous_metadata.get(string)
        if dictionary:
            line_count = dictionary.get(context)
            if line_count is not None:
                return baca.StaffLines(line_count=line_count)

    def _get_previous_time_signature(self):
        if self._previous_metadata:
            return self._previous_metadata.get('end_time_signature')

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

    def _get_segment_identifier(self):
        segment_name = self._metadata.get('segment_name')
        if segment_name is not None:
            return segment_name
        segment_number = self._get_segment_number()
        return segment_number

    def _get_segment_number(self):
        return self._metadata.get('segment_number', 1)

    def _get_stage_offsets(self, start_stage, stop_stage):
        skips = baca.select(self._score['GlobalSkips']).skips()
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

    def _get_stylesheets(self, environment=None):
        if environment == 'docs':
            if abjad.inspect(self._score).get_indicator('two-voice'):
                return [self._relative_two_voice_staff_stylesheet_path]
            else:
                return [self._relative_string_trio_stylesheet_path]
        elif environment == 'external':
            if abjad.inspect(self._score).get_indicator('two-voice'):
                return [self._absolute_two_voice_staff_stylesheet_path]
            else:
                return [self._absolute_string_trio_stylesheet_path]
        includes = []
        includes.append(self._score_package_stylesheet_path)
        if 1 < self._get_segment_number():
            includes.append(self._score_package_nonfirst_stylesheet_path)
        return includes

    def _get_time_signatures(self):
        strings = []
        prototype = abjad.TimeSignature
        for skip in baca.select(self._score['GlobalSkips']).skips():
            time_signature = abjad.inspect(skip).get_effective(prototype)
            assert time_signature is not None
            string = str(time_signature)
            strings.append(string)
        return strings

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
        for skip in baca.select(self._score['GlobalSkips']).skips():
            start_offset = abjad.inspect(skip).get_timespan().start_offset
            if start_offset in self._fermata_start_offsets:
                continue
            skips.append(skip)
        skips = abjad.select(skips)
        abjad.label(skips).with_start_offsets(clock_time=True, font_size=-2)

    def _label_instrument_changes(self):
        prototype = abjad.Instrument
        for staff in abjad.iterate(self._score).components(abjad.Staff):
            for i, leaf in enumerate(abjad.iterate(staff).leaves()):
                instrument = abjad.inspect(leaf).get_indicator(prototype)
                if not instrument:
                    continue
                current_instrument = instrument
                previous_leaf = abjad.inspect(leaf).get_leaf(-1)
                if previous_leaf is not None:
                    agent = abjad.inspect(previous_leaf)
                    result = agent.get_effective(abjad.Instrument)
                    previous_instrument = result
                elif (i == 0 and 1 < self._get_segment_number()):
                    instrument = self._get_previous_instrument(staff.name)
                    previous_instrument = instrument
                else:
                    continue
                previous_name = getattr(previous_instrument, 'name', None)
                current_name = getattr(current_instrument, 'name', None)
                if previous_name != current_name:
                    markup = self._make_instrument_change_markup(
                        current_instrument)
                    abjad.attach(markup, leaf)

    def _label_stage_numbers_(self):
        if not self.label_stages:
            return
        skips = baca.select(self._score['GlobalSkips']).skips()
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
            skip = skips[start_measure_index]
            abjad.attach(markup, skip)

    def _make_global_skips(self):
        context = self._score['GlobalSkips']
        for time_signature in self.time_signatures:
            skip = abjad.Skip(1)
            multiplier = abjad.Multiplier(time_signature.duration)
            abjad.attach(multiplier, skip)
            abjad.attach(time_signature, skip, context='Score')
            context.append(skip)
        # ghost bar line allows LilyPond to print first bar number
        tag = 'SEGMENT:EMPTY-BAR'
        first_skip = baca.select(context).skip(0)
        literal = abjad.LilyPondLiteral(r'\bar ""')
        abjad.attach(literal, first_skip, tag=tag)

    def _make_instrument_change_markup(self, instrument):
        string = f'to {instrument.name}'
        markup = abjad.Markup(string, direction=abjad.Up)
        markup = markup.box().override(('box-padding', 0.75))
        return markup

    def _make_lilypond_file(self, environment=None, midi=None):
        includes = self._get_stylesheets(environment=environment)
        if environment == 'external':
            use_relative_includes = False
        else:
            use_relative_includes = True
        lilypond_file = abjad.LilyPondFile.new(
            music=self._score,
            date_time_token=False,
            includes=includes,
            use_relative_includes=use_relative_includes,
            )
        block_names = ('layout', 'paper')
        for item in lilypond_file.items[:]:
            if getattr(item, 'name', None) in block_names:
                lilypond_file.items.remove(item)
        if midi:
            block = abjad.Block(name='midi')
            lilypond_file.items.append(block)
        for item in lilypond_file.items[:]:
            if getattr(item, 'name', None) == 'header':
                lilypond_file.items.remove(item)
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
            abjad.attach(multiplier, silence)
            silences.append(silence)
        return silences

    def _make_multimeasure_rests(self):
        rests = []
        for time_signature in self.time_signatures:
            rest = abjad.MultimeasureRest(abjad.Duration(1))
            multiplier = abjad.Multiplier(time_signature.duration)
            abjad.attach(multiplier, rest)
            rests.append(rest)
        return rests

    def _make_score(self):
        score = self.score_template()
        first_bar_number = self._metadata.get('first_bar_number')
        if first_bar_number is not None:
            abjad.setting(score).current_bar_number = first_bar_number
        self._score = score

    def _print_cache(self):
        for context in self._cache:
            print(f'CONTEXT {context} ...')
            leaves_by_stage_number = self._cache[context]
            for stage_number in leaves_by_stage_number:
                print(f'STAGE {stage_number} ...')
                for leaf in leaves_by_stage_number[stage_number]:
                    print(leaf)

    def _print_segment_duration_(self):
        if not self.print_segment_duration:
            return
        current_tempo = None
        skips = baca.select(self._score['GlobalSkips']).skips()
        measure_summaries = []
        tempo_index = 0
        is_trending = False
        for i, skip in enumerate(skips):
            duration = abjad.inspect(skip).get_duration()
            tempi = abjad.inspect(skip).get_indicators(abjad.MetronomeMark)
            if tempi:
                current_tempo = tempi[0]
                for measure_summary in measure_summaries[tempo_index:]:
                    assert measure_summary[-1] is None
                    measure_summary[-1] = current_tempo
                tempo_index = i
                is_trending = False
            if abjad.inspect(skip).has_indicator(abjad.Accelerando):
                is_trending = True
            if abjad.inspect(skip).has_indicator(abjad.Ritardando):
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

    def _reapply_previous_segment_settings(self):
        if self._is_first_segment():
            return
        if not self._previous_metadata:
            segment = self._get_segment_identifier()
            print(f'can not find previous metadata before {segment}.')
            return
        skip = baca.select(self._score['GlobalSkips']).skip(0)
        mark = abjad.inspect(skip).get_piecewise(abjad.MetronomeMark)
        if mark is None:
            tag = 'SEGMENT:REMINDER-METRONOME-MARK'
            string = self._color_reminder('TextScript')
            literal = abjad.LilyPondLiteral(string)
            abjad.attach(literal, skip, tag=tag)
            prototype = abjad.MetronomeMarkSpanner
            spanner = abjad.inspect(skip).get_spanner(prototype)
            previous_mark = self._get_previous_metronome_mark()
            spanner.attach(previous_mark, skip, tag=tag)
        time_signature = abjad.inspect(skip).get_indicator(abjad.TimeSignature)
        assert time_signature is not None
        previous_time_signature = self._get_previous_time_signature()
        if str(previous_time_signature) == str(time_signature):
            tag = 'SEGMENT:DUPLICATE-TIME-SIGNATURE'
            wrapper = abjad.inspect(skip).get_indicator(
                abjad.TimeSignature,
                unwrap=False,
                )
            context = wrapper.context
            string = self._color_duplicate('TimeSignature', context)
            literal = abjad.LilyPondLiteral(string)
            abjad.attach(literal, skip, tag=tag)
            abjad.detach(time_signature, skip)
            abjad.attach(time_signature, skip, context=context, tag=tag)
        for context in abjad.iterate(self._score).components(abjad.Context):
            previous_clef = self._get_previous_clef(context.name)
            previous_dynamic = self._get_previous_dynamic(context.name)
            previous_instrument = self._get_previous_instrument(context.name)
            previous_staff_lines = self._get_previous_staff_lines(context.name)
            if not any([
                previous_clef,
                previous_dynamic,
                previous_instrument,
                previous_staff_lines,
                ]):
                continue
            first_leaf = abjad.inspect(context).get_leaf(0)
            if previous_instrument is not None:
                prototype = abjad.Instrument
                instrument = abjad.inspect(first_leaf).get_indicator(prototype)
                if instrument is None:
                    tag = 'SEGMENT:RESTATED-INSTRUMENT'
                    string = self._color_restated('InstrumentName', context)
                    literal = abjad.LilyPondLiteral(string)
                    abjad.attach(literal, first_leaf, tag=tag)
                    instrument = abjad.new(
                        previous_instrument,
                        context=context.context_name,
                        )
                    abjad.attach(instrument, first_leaf, tag=tag)
            if previous_staff_lines is not None:
                prototype = baca.StaffLines
                staff_lines = abjad.inspect(first_leaf).get_indicator(
                    prototype)
                if staff_lines is None:
                    tag = 'SEGMENT:REAPPLIED-STAFF-LINES'
                    string = self._color_reapplied('StaffSymbol', context)
                    literal = abjad.LilyPondLiteral(string)
                    abjad.attach(literal, first_leaf, tag=tag)
                    abjad.attach(previous_staff_lines, first_leaf, tag=tag)
                elif previous_staff_lines == staff_lines:
                    tag = 'SEGMENT:DUPLICATE-STAFF-LINES'
                    string = self._color_duplicate('StaffSymbol', context)
                    literal = abjad.LilyPondLiteral(string)
                    abjad.attach(literal, first_leaf, tag=tag)
            if previous_clef is not None:
                clef = abjad.inspect(first_leaf).get_indicator(abjad.Clef)
                if clef is None:
                    tag = 'SEGMENT:RESTATED-CLEF'
                    string = self._color_restated('Clef', context, once=False)
                    literal = abjad.LilyPondLiteral(string)
                    abjad.attach(literal, first_leaf, tag=tag)
                    abjad.attach(previous_clef, first_leaf, tag=tag)
                    string = rf'\set {context.context_name}.forceClef = ##t'
                    literal = abjad.LilyPondLiteral(string)
                    abjad.attach(literal, first_leaf, tag=tag)
                elif str(previous_clef) == str(clef):
                    wrapper = abjad.inspect(first_leaf).get_indicator(
                        abjad.Clef,
                        unwrap=False,
                        )
                    tag = 'SEGMENT:DUPLICATE-CLEF'
                    string = self._color_duplicate(
                        'Clef',
                        context=wrapper.context,
                        once=False,
                        )
                    literal = abjad.LilyPondLiteral(string)
                    abjad.attach(literal, first_leaf, tag=tag)
                    abjad.detach(clef, first_leaf)
                    abjad.attach(clef, first_leaf, tag=tag)
                    string = rf'\set {wrapper.context}.forceClef = ##t'
                    literal = abjad.LilyPondLiteral(string)
                    abjad.attach(literal, first_leaf, tag=tag)
            if previous_dynamic is not None:
                prototype = abjad.Dynamic
                dynamic = abjad.inspect(first_leaf).get_effective(prototype)
                if dynamic is None:
                    tag = 'SEGMENT:REMINDER-DYNAMIC'
                    string = self._color_reminder('DynamicText', context)
                    literal = abjad.LilyPondLiteral(string)
                    abjad.attach(literal, first_leaf, tag=tag)
                    abjad.attach(previous_dynamic, first_leaf, tag=tag)

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

    def _shorten_long_repeat_ties(self):
        leaves = abjad.iterate(self._score).leaves()
        for leaf in leaves:
            ties = abjad.inspect(leaf).get_spanners(abjad.Tie)
            if not ties:
                continue
            tie = ties.pop()
            if not tie.repeat_ties:
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

    def _update_metadata(self, environment=None):
        if environment is not None:
            return
        self._metadata['measure_count'] = self.measure_count
        end_settings = self._get_end_settings()
        self._metadata.update(end_settings)
        class_ = type(self._metadata)
        items = sorted(self._metadata.items())
        metadata = class_(items)
        self._metadata = metadata

    def _voice_to_rhythm_wrappers(self, voice):
        wrappers = []
        for wrapper in self.wrappers:
            if not isinstance(wrapper.command, baca.RhythmCommand):
                continue
            if wrapper.scope.voice_name == voice.name:
                wrappers.append(wrapper)
        return wrappers

    def _whitespace_leaves(self):
        for leaf in abjad.iterate(self._score).leaves():
            abjad.attach(abjad.LilyPondLiteral('', 'absolute_before'), leaf)
            if abjad.inspect(leaf).get_leaf(1) is None:
                abjad.attach(abjad.LilyPondLiteral('', 'absolute_after'), leaf)

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

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing_specifier=baca.HorizontalSpacingSpecifier(
            ...         minimum_width=abjad.Duration(1, 24),
            ...         ),
            ...     time_signatures=time_signatures,
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=figures,
            ...         ),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 1/16
                            \bar "" % SEGMENT:EMPTY-BAR
                            \newSpacingSection
                            s1 * 1/16
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 7/16
                            \newSpacingSection
                            s1 * 7/16
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 1/16
                            \newSpacingSection
                            s1 * 1/16
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 3/8
                            \newSpacingSection
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 1] %%%
                                        \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                        \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                        e'16
                                    }
                                }
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 2] %%%
                                        fs'16 [
                <BLANKLINE>
                                        d'16
                <BLANKLINE>
                                        ef'16
                <BLANKLINE>
                                        f'16
                <BLANKLINE>
                                        a'16
                <BLANKLINE>
                                        af'16
                <BLANKLINE>
                                        c'16 ]
                                    }
                                }
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 3] %%%
                                        b'16
                                    }
                                }
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 4] %%%
                                        bf'16 [
                <BLANKLINE>
                                        g'16
                <BLANKLINE>
                                        a'16
                <BLANKLINE>
                                        af'16
                <BLANKLINE>
                                        c'16
                <BLANKLINE>
                                        f'16 ]
                                        \bar "|"
                <BLANKLINE>
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

            >>> maker = baca.SegmentMaker(
            ...     allow_figure_names=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing_specifier=baca.HorizontalSpacingSpecifier(
            ...         minimum_width=abjad.Duration(1, 24),
            ...         ),
            ...     time_signatures=time_signatures,
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=figures,
            ...         ),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> score = lilypond_file[abjad.Score]
            >>> abjad.override(score).text_script.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" \with {
                    \override TextScript.staff-padding = #3
                } <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 1/16
                            \bar "" % SEGMENT:EMPTY-BAR
                            \newSpacingSection
                            s1 * 1/16
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 7/16
                            \newSpacingSection
                            s1 * 7/16
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 1/16
                            \newSpacingSection
                            s1 * 1/16
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 3/8
                            \newSpacingSection
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 1] %%%
                                        \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                        \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
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
                <BLANKLINE>
                                        %%% MusicVoice [measure 2] %%%
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
                <BLANKLINE>
                                        d'16
                <BLANKLINE>
                                        ef'16
                <BLANKLINE>
                                        f'16
                <BLANKLINE>
                                        a'16
                <BLANKLINE>
                                        af'16
                <BLANKLINE>
                                        c'16 ]
                                    }
                                }
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 3] %%%
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
                <BLANKLINE>
                                        %%% MusicVoice [measure 4] %%%
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
                <BLANKLINE>
                                        g'16
                <BLANKLINE>
                                        a'16
                <BLANKLINE>
                                        af'16
                <BLANKLINE>
                                        c'16
                <BLANKLINE>
                                        f'16 ]
                                        \bar "|"
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
        return self._allow_figure_names

    @property
    def color_octaves(self):
        r'''Is true when segment-maker colors octaves.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     color_octaves=True,
            ...     score_template=baca.StringTrioScoreTemplate(),
            ...     spacing_specifier=baca.HorizontalSpacingSpecifier(
            ...         minimum_width=abjad.Duration(1, 24),
            ...         ),
            ...     time_signatures=[abjad.TimeSignature((6, 16))],
            ...     )

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'MusicVoice',
            ...     [[2, 4, 5, 7, 9, 11]],
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=contribution['MusicVoice'],
            ...         ),
            ...     )

            >>> contribution = music_maker(
            ...     'CelloMusicVoice',
            ...     [[-3, -5, -7, -8, -10, -12]],
            ...     )
            >>> maker(
            ...     baca.scope('CelloMusicVoice', 1),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=contribution['CelloMusicVoice'],
            ...         ),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \tag violin.viola.cello
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 6/16
                            \bar "" % SEGMENT:EMPTY-BAR
                            \newSpacingSection
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context StringSectionStaffGroup = "String Section Staff Group" <<
                            \tag violin
                            \context ViolinMusicStaff = "ViolinMusicStaff" {
                                \context ViolinMusicVoice = "ViolinMusicVoice" {
                <BLANKLINE>
                                    %%% ViolinMusicVoice [measure 1] %%%
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    R1 * 3/8
                                    \bar "|"
                <BLANKLINE>
                                }
                            }
                            \tag viola
                            \context ViolaMusicStaff = "ViolaMusicStaff" {
                                \context ViolaMusicVoice = "ViolaMusicVoice" {
                <BLANKLINE>
                                    %%% ViolaMusicVoice [measure 1] %%%
                                    \set ViolaMusicStaff.instrumentName = \markup { Viola }
                                    \set ViolaMusicStaff.shortInstrumentName = \markup { Va. }
                                    \clef "alto" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    R1 * 3/8
                                    \bar "|"
                <BLANKLINE>
                                }
                            }
                            \tag cello
                            \context CelloMusicStaff = "CelloMusicStaff" {
                                \context CelloMusicVoice = "CelloMusicVoice" {
                                    {
                                        {
                <BLANKLINE>
                                            %%% CelloMusicVoice [measure 1] %%%
                                            \set CelloMusicStaff.instrumentName = \markup { Cello }
                                            \set CelloMusicStaff.shortInstrumentName = \markup { Vc. }
                                            \clef "bass" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                            \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                            a16 [
                <BLANKLINE>
                                            g16
                <BLANKLINE>
                                            f16
                <BLANKLINE>
                                            e16
                <BLANKLINE>
                                            d16
                <BLANKLINE>
                                            c16 ]
                                            \bar "|"
                <BLANKLINE>
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
            >>> maker = baca.SegmentMaker(
            ...     color_out_of_range_pitches=True,
            ...     range_checker=pitch_range,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing_specifier=baca.HorizontalSpacingSpecifier(
            ...         minimum_width=abjad.Duration(1, 24),
            ...         ),
            ...     time_signatures=time_signatures,
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=figures,
            ...         ),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 1/16
                            \bar "" % SEGMENT:EMPTY-BAR
                            \newSpacingSection
                            s1 * 1/16
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 7/16
                            \newSpacingSection
                            s1 * 7/16
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 1/16
                            \newSpacingSection
                            s1 * 1/16
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 3/8
                            \newSpacingSection
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 1] %%%
                                        \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                        \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                        e'16
                                    }
                                }
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 2] %%%
                                        \once \override Accidental.color = #red
                                        \once \override Beam.color = #red
                                        \once \override Dots.color = #red
                                        \once \override NoteHead.color = #red
                                        \once \override Stem.color = #red
                                        c16 [
                                            - \tweak color #red
                                            ^ \markup { * }
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
                                        c'16 ]
                                    }
                                }
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 3] %%%
                                        b'16
                                    }
                                }
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 4] %%%
                                        bf'16 [
                <BLANKLINE>
                                        g'16
                <BLANKLINE>
                                        a'16
                <BLANKLINE>
                                        bf'16
                <BLANKLINE>
                                        c'16
                <BLANKLINE>
                                        f'16 ]
                                        \bar "|"
                <BLANKLINE>
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

            >>> maker = baca.SegmentMaker(
            ...     color_repeat_pitch_classes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing_specifier=baca.HorizontalSpacingSpecifier(
            ...         minimum_width=abjad.Duration(1, 24),
            ...         ),
            ...     time_signatures=time_signatures,
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=figures,
            ...         ),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 1/16
                            \bar "" % SEGMENT:EMPTY-BAR
                            \newSpacingSection
                            s1 * 1/16
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 7/16
                            \newSpacingSection
                            s1 * 7/16
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 1/16
                            \newSpacingSection
                            s1 * 1/16
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 3/8
                            \newSpacingSection
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 1] %%%
                                        \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                        \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                        e'16
                                    }
                                }
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 2] %%%
                                        fs'16 [
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
                                            - \tweak color #red
                                            ^ \markup { @ }
                <BLANKLINE>
                                        \once \override Accidental.color = #red
                                        \once \override Beam.color = #red
                                        \once \override Dots.color = #red
                                        \once \override NoteHead.color = #red
                                        \once \override Stem.color = #red
                                        a'16
                                            - \tweak color #red
                                            ^ \markup { @ }
                <BLANKLINE>
                                        c'16 ]
                                    }
                                }
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 3] %%%
                                        b'16
                                    }
                                }
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 4] %%%
                                        bf'16 [
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
                                            - \tweak color #red
                                            ^ \markup { @ }
                <BLANKLINE>
                                        \once \override Accidental.color = #red
                                        \once \override Beam.color = #red
                                        \once \override Dots.color = #red
                                        \once \override NoteHead.color = #red
                                        \once \override Stem.color = #red
                                        c'16
                                            - \tweak color #red
                                            ^ \markup { @ }
                <BLANKLINE>
                                        f'16 ]
                                        \bar "|"
                <BLANKLINE>
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

    @property
    def fermata_measure_staff_line_count(self):
        r'''Gets fermata measure staff lines.

        Defaults to none.

        Set to nonnegative integer or none.

        Returns nonnegative integer or none.
        '''
        return self._fermata_measure_staff_line_count

    # TODO: write examples showing Score.BarLine.transparent = ##f
    #       for mensurstriche final_bar_line=abjad.Exact
    @property
    def final_bar_line(self):
        r'''Gets final bar line.

        ..  container:: example

            Nonlast segment sets final bar line to ``'|'`` by default:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 1] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 2] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 3] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 4] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Last segment in score sets final bar line to ``'|.'`` by default:

            >>> maker = baca.SegmentMaker(
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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 1] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 2] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 3] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 4] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|."
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Nonlast segment sets final bar line explicitly:

            >>> maker = baca.SegmentMaker(
            ...     final_bar_line='||',
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 1] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 2] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 3] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 4] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "||"
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Last segment in score sets final bar line explicitly:

            >>> maker = baca.SegmentMaker(
            ...     final_bar_line='||',
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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 1] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 2] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 3] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 4] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "||"
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        Set to bar line string or none.

        Returns bar line string or none.
        '''
        return self._final_bar_line

    @property
    def final_markup(self):
        r'''Gets final markup.

        ..  container:: example

            No final markup by default:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 1] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 2] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 3] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 4] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            With final markup:

            >>> maker = baca.SegmentMaker(
            ...     final_bar_line='|.',
            ...     final_markup=(['Madison, WI'], ['October 2016']),
            ...     final_markup_extra_offset=(-9, -2),
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 1] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 2] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 3] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 4] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
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
                <BLANKLINE>
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

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 1] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 2] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 3] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 4] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 1] %%%
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    c'8 [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 2] %%%
                                    c'8 [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 3] %%%
                                    c'8 [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 4] %%%
                                    c'8 [
                <BLANKLINE>
                                    c'8
                <BLANKLINE>
                                    c'8 ]
                                    \bar "|"
                <BLANKLINE>
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
            ...     spacing_specifier=baca.HorizontalSpacingSpecifier(
            ...         minimum_width=abjad.Duration(1, 24),
            ...         ),
            ...     time_signatures=time_signatures,
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=figures,
            ...         ),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
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
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 3/16
                            \bar "" % SEGMENT:EMPTY-BAR
                            \newSpacingSection
                            s1 * 3/16
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 3/16
                            \newSpacingSection
                            s1 * 3/16
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 3/16
                            \newSpacingSection
                            s1 * 3/16
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 3/16
                            \newSpacingSection
                            s1 * 3/16
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 1] %%%
                                        \once \override Accidental.color = #magenta
                                        \once \override Beam.color = #magenta
                                        \once \override Dots.color = #magenta
                                        \once \override Flag.color = #magenta
                                        \once \override NoteHead.color = #magenta
                                        \once \override Stem.color = #magenta
                                        \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                        \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                        e'8.
                                    }
                                }
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 2] %%%
                                        \acciaccatura {
                <BLANKLINE>
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            fs'16 [
                <BLANKLINE>
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            d'16
                <BLANKLINE>
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            ef'16
                <BLANKLINE>
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            f'16
                <BLANKLINE>
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            a'16
                <BLANKLINE>
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            af'16 ]
                <BLANKLINE>
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
                <BLANKLINE>
                                        %%% MusicVoice [measure 3] %%%
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
                <BLANKLINE>
                                        %%% MusicVoice [measure 4] %%%
                                        \acciaccatura {
                <BLANKLINE>
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            bf'16 [
                <BLANKLINE>
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            g'16
                <BLANKLINE>
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            a'16
                <BLANKLINE>
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            af'16
                <BLANKLINE>
                                            \once \override Accidental.color = #magenta
                                            \once \override Beam.color = #magenta
                                            \once \override Dots.color = #magenta
                                            \once \override Flag.color = #magenta
                                            \once \override NoteHead.color = #magenta
                                            \once \override Stem.color = #magenta
                                            c'16 ]
                <BLANKLINE>
                                        }
                                        \once \override Accidental.color = #magenta
                                        \once \override Beam.color = #magenta
                                        \once \override Dots.color = #magenta
                                        \once \override Flag.color = #magenta
                                        \once \override NoteHead.color = #magenta
                                        \once \override Stem.color = #magenta
                                        f'8.
                                        \bar "|"
                <BLANKLINE>
                                    }
                                }
                            }
                        }
                    >>
                >>

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
            ...     spacing_specifier=baca.HorizontalSpacingSpecifier(
            ...         minimum_width=abjad.Duration(1, 24),
            ...         ),
            ...     time_signatures=time_signatures,
            ...     )
            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=figures,
            ...         ),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
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
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 3/16
                            \bar "" % SEGMENT:EMPTY-BAR
                            \newSpacingSection
                            s1 * 3/16
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 3/16
                            \newSpacingSection
                            s1 * 3/16
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 3/16
                            \newSpacingSection
                            s1 * 3/16
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)
                            \time 3/16
                            \newSpacingSection
                            s1 * 3/16
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 1] %%%
                                        \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                        \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                        e'8.
                                    }
                                }
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 2] %%%
                                        \acciaccatura {
                <BLANKLINE>
                                            fs'16 [
                <BLANKLINE>
                                            d'16
                <BLANKLINE>
                                            ef'16
                <BLANKLINE>
                                            f'16
                <BLANKLINE>
                                            a'16
                <BLANKLINE>
                                            af'16 ]
                <BLANKLINE>
                                        }
                                        c'8.
                                    }
                                }
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 3] %%%
                                        b'8.
                                    }
                                }
                                {
                                    {
                <BLANKLINE>
                                        %%% MusicVoice [measure 4] %%%
                                        \acciaccatura {
                <BLANKLINE>
                                            bf'16 [
                <BLANKLINE>
                                            g'16
                <BLANKLINE>
                                            a'16
                <BLANKLINE>
                                            af'16
                <BLANKLINE>
                                            c'16 ]
                <BLANKLINE>
                                        }
                                        f'8.
                                        \bar "|"
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

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     metronome_mark_measure_map=baca.MetronomeMarkMeasureMap([
            ...         (1, abjad.MetronomeMark((1, 8), 90)),
            ...         ]),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
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
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 1] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 2] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 3] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 4] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Does label clock time:

            >>> maker = baca.SegmentMaker(
            ...     label_clock_time=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     metronome_mark_measure_map=baca.MetronomeMarkMeasureMap([
            ...         (1, abjad.MetronomeMark((1, 8), 90)),
            ...         ]),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs') # doctest: +SKIP
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  todo:: MAKE THIS WORK AGAIN.

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
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
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 1] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 2] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 3] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 4] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                <BLANKLINE>
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

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 1] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 2] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 3] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 4] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Labels stage numbers:

            >>> maker = baca.SegmentMaker(
            ...     label_stages=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
                            s1 * 1/2
                                - \markup {
                                    \fontsize
                                        #-3
                                        \with-color
                                            #blue
                                            [1]
                                    }
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 1] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 2] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 3] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 4] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Labels numbers with segment name:

            >>> maker = baca.SegmentMaker(
            ...     label_stages=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
            ...     )

            >>> metadata = {'name': 'K'}
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     metadata=metadata,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
                            s1 * 1/2
                                - \markup {
                                    \fontsize
                                        #-3
                                        \with-color
                                            #blue
                                            [K.1]
                                    }
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 1] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 2] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 3] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 4] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                <BLANKLINE>
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
    def layout_measure_map(self):
        r'''Gets layout measure map.

        Set to layout measure map or none.

        Returns layout measure map or none.
        '''
        return self._layout_measure_map

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
    def metadata(self):
        r'''Gets segment metadata after run.

        Returns ordered dictionary.
        '''
        return self._metadata

    @property
    def metronome_mark_measure_map(self):
        r'''Gets metronome mark measure map.

        ..  container:: example

            Without metronome mark measure map:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 1] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 2] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 3] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 4] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            With metronome mark measure map:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     metronome_mark_measure_map=baca.MetronomeMarkMeasureMap([
            ...         (1, abjad.MetronomeMark((1, 8), 90)),
            ...         ]),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
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
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 1] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 2] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 3] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 4] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                <BLANKLINE>
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

            >>> maker = baca.SegmentMaker()

            >>> maker.score_template is None
            True

        ..  container:: example

            Gets score template:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     )

            >>> maker.score_template
            SingleStaffScoreTemplate()

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

        ..  container:: example

            Fills empty measures with multimeasure rests:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                R1 * 1/2
                <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                R1 * 3/8
                <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                R1 * 1/2
                <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                R1 * 3/8
                                \bar "|"
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
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                s1 * 1/2
                <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                s1 * 3/8
                <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                s1 * 1/2
                <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                s1 * 3/8
                                \bar "|"
                <BLANKLINE>
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

            >>> maker = baca.SegmentMaker(
            ...     label_stages=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
            ...     )

            >>> metadata = {'name': 'K'}
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     metadata=metadata,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
                            s1 * 1/2
                                - \markup {
                                    \fontsize
                                        #-3
                                        \with-color
                                            #blue
                                            [K.1]
                                    }
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 1] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 2] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 3] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 4] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        ..  container:: example

            Takes base string from stage label property:

            >>> maker = baca.SegmentMaker(
            ...     label_stages=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     stage_label_base_string='intermezzo',
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
            ...     )

            >>> metadata = {'name': 'K'}
            >>> lilypond_file = maker.run(
            ...     environment='docs',
            ...     metadata=metadata,
            ...     )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
                            s1 * 1/2
                                - \markup {
                                    \fontsize
                                        #-3
                                        \with-color
                                            #blue
                                            [intermezzo.1]
                                    }
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 1] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 2] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 3] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 4] %%%
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 [
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8
                <BLANKLINE>
                                    \once \override Beam.color = #blue
                                    \once \override Dots.color = #blue
                                    \once \override Flag.color = #blue
                                    \once \override NoteHead.color = #blue
                                    \once \override Stem.color = #blue
                                    c'8 ]
                                    \bar "|"
                <BLANKLINE>
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

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.make_even_runs(),
            ...     baca.pitches('E4 F4'),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score])
                \context Score = "Score" <<
                    \context GlobalContext = "GlobalContext" <<
                        \context GlobalSkips = "GlobalSkips" {
                <BLANKLINE>
                            %%% GlobalSkips [measure 1] %%%
                            \time 4/8
                            \bar "" % SEGMENT:EMPTY-BAR
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 2] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                            %%% GlobalSkips [measure 3] %%%
                            \time 4/8
                            s1 * 1/2
                <BLANKLINE>
                            %%% GlobalSkips [measure 4] %%%
                            \time 3/8
                            s1 * 3/8
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext" <<
                        \context Staff = "MusicStaff" {
                            \context Voice = "MusicVoice" {
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 1] %%%
                                    \clef "treble" % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CONTEXTED-INDICATOR
                                    e'8 [
                <BLANKLINE>
                                    f'8
                <BLANKLINE>
                                    e'8
                <BLANKLINE>
                                    f'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 2] %%%
                                    e'8 [
                <BLANKLINE>
                                    f'8
                <BLANKLINE>
                                    e'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 3] %%%
                                    f'8 [
                <BLANKLINE>
                                    e'8
                <BLANKLINE>
                                    f'8
                <BLANKLINE>
                                    e'8 ]
                                }
                                {
                <BLANKLINE>
                                    %%% MusicVoice [measure 4] %%%
                                    f'8 [
                <BLANKLINE>
                                    e'8
                <BLANKLINE>
                                    f'8 ]
                                    \bar "|"
                <BLANKLINE>
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
        builds_metadata=None,
        environment=None,
        metadata=None,
        midi=None,
        previous_metadata=None,
        ):
        r'''Runs segment-maker.

        Leave `environment` set to none to render segments in real score.

        Set `environment` to `'docs'` for API examples.
        
        Set `environment` to `'external'` to debug API examples in an external
        file.

        Returns LilyPond file.
        '''
        self._builds_metadata = abjad.TypedOrderedDict(builds_metadata)
        self._metadata = abjad.TypedOrderedDict(metadata)
        self._previous_metadata = abjad.TypedOrderedDict(previous_metadata)
        self._make_score()
        self._make_lilypond_file(environment=environment, midi=midi)
        self._make_global_skips()
        self._label_stage_numbers_()
        self._call_rhythm_commands()
        self._extend_beams()
        self._call_commands()
        self._detach_figure_names()
        self._shorten_long_repeat_ties()
        self._attach_first_segment_score_template_defaults()
        self._reapply_previous_segment_settings()
        self._blacken_explicit_contexted_indicators()
        self._apply_spacing_specifier()
        self._label_clock_time_()
        self._hide_instrument_names_()
        self._label_instrument_changes()
        self._transpose_score_()
        self._attach_rehearsal_mark()
        self._add_final_bar_line()
        self._add_final_markup()
        self._color_unregistered_pitches()
        self._color_unpitched_notes()
        self._check_wellformedness()
        self._check_design()
        self._check_range()
        self._color_repeat_pitch_classes_()
        self._color_octaves_()
        self._whitespace_leaves()
        self._comment_measure_numbers()
        self._apply_layout_measure_map()
        self._cache_break_offsets()
        self._apply_fermata_measure_staff_line_count()
        self._update_metadata(environment=environment)
        self._print_segment_duration_()
        return self._lilypond_file

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
