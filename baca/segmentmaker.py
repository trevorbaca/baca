"""
Segment-maker.
"""
import copy
import importlib
import inspect

import abjad
from abjadext import rmakers

from . import const, indicators
from . import layout as _layout
from . import memento as _memento
from . import overrides as _overrides
from . import parts as _parts
from . import piecewise as _piecewise
from . import pitchclasses, pitchcommands, rhythmcommands, scoping
from . import selection as _selection
from . import sequence as _sequence
from . import tags as _tags
from . import templates as _templates


def _site(frame, n=None):
    prefix = "baca.SegmentMaker"
    return scoping.site(frame, prefix, n=n)


nonfirst_preamble = r"""\header { composer = ##f poet = ##f title = ##f }
\layout { indent = 0 }
\paper { print-first-page-number = ##t }"""


def _attach_rhythm_annotation_spanner(command, selection):
    if not command.annotation_spanner_text and not command.frame:
        return
    leaves = []
    for leaf in abjad.iterate(selection).leaves():
        if abjad.get.parentage(leaf).get(abjad.OnBeatGraceContainer):
            continue
        leaves.append(leaf)
    container = abjad.get.before_grace_container(leaves[0])
    if container is not None:
        leaves_ = abjad.select(container).leaves()
        leaves[0:0] = leaves_
    container = abjad.get.after_grace_container(leaves[-1])
    if container is not None:
        leaves_ = abjad.select(container).leaves()
        leaves.extend(leaves_)
    string = command.annotation_spanner_text
    if string is None:
        string = command._make_rhythm_annotation_string()
    color = command.annotation_spanner_color or "#darkyellow"
    command_ = _piecewise.rhythm_annotation_spanner(
        string,
        abjad.tweak(color).color,
        abjad.tweak(8).staff_padding,
        leak_spanner_stop=True,
        selector=lambda _: _selection.Selection(_).leaves(),
    )
    command_(leaves)


class SegmentMaker:
    r"""
    Segment-maker.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     deactivate=[baca.tags.NOT_YET_PITCHED_COLORING],
        ...     includes=["baca.ily"],
        ...     preamble=[baca.global_context_string()],
        ...     score_template=baca.make_empty_score_maker(1),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )

        >>> maker(
        ...     "Music_Voice",
        ...     baca.make_even_divisions(),
        ... )

        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context GlobalContext = "Global_Context"
                <<
                    \context GlobalSkips = "Global_Skips"
                    {
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
                    }
                >>
                \context MusicContext = "Music_Context"
                {
                    \context Staff = "Music_Staff"
                    {
                        \context Voice = "Music_Voice"
                        {
                            %@% \baca-not-yet-pitched-coloring
                            b'8
                            [
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_even_divisions()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            %@% \baca-not-yet-pitched-coloring
                            b'8
                            %@% \baca-not-yet-pitched-coloring
                            b'8
                            %@% \baca-not-yet-pitched-coloring
                            b'8
                            ]
                            %@% \baca-not-yet-pitched-coloring
                            b'8
                            [
                            %@% \baca-not-yet-pitched-coloring
                            b'8
                            %@% \baca-not-yet-pitched-coloring
                            b'8
                            ]
                            %@% \baca-not-yet-pitched-coloring
                            b'8
                            [
                            %@% \baca-not-yet-pitched-coloring
                            b'8
                            %@% \baca-not-yet-pitched-coloring
                            b'8
                            %@% \baca-not-yet-pitched-coloring
                            b'8
                            ]
                            %@% \baca-not-yet-pitched-coloring
                            b'8
                            [
                            %@% \baca-not-yet-pitched-coloring
                            b'8
                            %@% \baca-not-yet-pitched-coloring
                            b'8
                            ]
                            <> \bacaStopTextSpanRhythmAnnotation
                            <<
                                \context Voice = "Music_Voice"
                                {
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    %@% \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                }
                                \context Voice = "Rest_Voice"
                                {
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                }
                            >>
                        }
                    }
                }
            >>

    ..  container:: example

        Segment-maker colors repeat pitch-classes:

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
        ...     time_signature = abjad.get.duration(selection)
        ...     time_signatures.append(time_signature)
        ...
        >>> figures_ = []
        >>> for figure in figures:
        ...     figures_.extend(figure)
        ...
        >>> figures = abjad.select(figures_)

        >>> maker = baca.SegmentMaker(
        ...     includes=["baca.ily"],
        ...     preamble=[baca.global_context_string()],
        ...     score_template=baca.make_empty_score_maker(1),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ...     time_signatures=time_signatures,
        ... )
        >>> maker(
        ...     ("Music_Voice", 1),
        ...     baca.music(figures, do_not_check_total_duration=True),
        ... )

        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context GlobalContext = "Global_Context"
                <<
                    \context GlobalSkips = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \time 1/16
                        \baca-time-signature-color #'blue
                        s1 * 1/16
                        \baca-new-spacing-section #1 #24
                        \time 7/16
                        \baca-time-signature-color #'blue
                        s1 * 7/16
                        \baca-new-spacing-section #1 #24
                        \time 1/16
                        \baca-time-signature-color #'blue
                        s1 * 1/16
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
                    }
                >>
                \context MusicContext = "Music_Context"
                {
                    \context Staff = "Music_Staff"
                    {
                        \context Voice = "Music_Voice"
                        {
                            \scaleDurations #'(1 . 1)
                            {
                                e'16
                                - \abjad-dashed-line-with-hook
                                - \baca-text-spanner-left-text "baca.music()"
                                - \tweak bound-details.right.padding 2.75
                                - \tweak color #darkcyan
                                - \tweak staff-padding 8
                                \bacaStartTextSpanRhythmAnnotation
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                fs'!16
                                d'16
                                ef'!16
                                f'16
                                \baca-repeat-pitch-class-coloring
                                a'16
                                \baca-repeat-pitch-class-coloring
                                a'16
                                c'16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                b'16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                bf'!16
                                g'16
                                a'16
                                \baca-repeat-pitch-class-coloring
                                c''16
                                \baca-repeat-pitch-class-coloring
                                c'16
                                f'16
                                <> \bacaStopTextSpanRhythmAnnotation
                            }
                            <<
                                \context Voice = "Music_Voice"
                                {
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                }
                                \context Voice = "Rest_Voice"
                                {
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                }
                            >>
                        }
                    }
                }
            >>

    ..  container:: example

        Segment-maker colors out-of-range pitches:

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
        ...     time_signature = abjad.get.duration(selection)
        ...     time_signatures.append(time_signature)
        ...
        >>> figures_ = []
        >>> for figure in figures:
        ...     figures_.extend(figure)
        ...
        >>> figures = abjad.select(figures_)

        >>> maker = baca.SegmentMaker(
        ...     do_not_check_out_of_range_pitches=True,
        ...     includes=["baca.ily"],
        ...     preamble=[baca.global_context_string()],
        ...     score_template=baca.make_empty_score_maker(1),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 24)),
        ...     time_signatures=time_signatures,
        ... )
        >>> maker(
        ...     ("Music_Voice", 1),
        ...     baca.instrument(abjad.Violin()),
        ...     baca.music(figures, do_not_check_total_duration=True),
        ... )

        >>> lilypond_file = maker.run(environment="docs")
        >>> abjad.setting(lilypond_file["Score"]).autoBeaming = False
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            \with
            {
                autoBeaming = ##f
            }
            <<
                \context GlobalContext = "Global_Context"
                <<
                    \context GlobalSkips = "Global_Skips"
                    {
                        \baca-new-spacing-section #1 #24
                        \time 1/16
                        \baca-time-signature-color #'blue
                        s1 * 1/16
                        \baca-new-spacing-section #1 #24
                        \time 7/16
                        \baca-time-signature-color #'blue
                        s1 * 7/16
                        \baca-new-spacing-section #1 #24
                        \time 1/16
                        \baca-time-signature-color #'blue
                        s1 * 1/16
                        \baca-new-spacing-section #1 #24
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
                        \baca-new-spacing-section #1 #4
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
                    }
                >>
                \context MusicContext = "Music_Context"
                {
                    \context Staff = "Music_Staff"
                    {
                        \context Voice = "Music_Voice"
                        {
                            \scaleDurations #'(1 . 1)
                            {
                                e'16
                                ^ \baca-explicit-indicator-markup "(Violin)"
                                - \abjad-dashed-line-with-hook
                                - \baca-text-spanner-left-text "baca.music()"
                                - \tweak bound-details.right.padding 2.75
                                - \tweak color #darkcyan
                                - \tweak staff-padding 8
                                \bacaStartTextSpanRhythmAnnotation
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                \baca-out-of-range-coloring
                                c16
                                d'16
                                ef'!16
                                f'16
                                af'!16
                                a'16
                                c'16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                b'16
                            }
                            \scaleDurations #'(1 . 1)
                            {
                                bf'!16
                                g'16
                                a'16
                                bf'!16
                                c'16
                                f'16
                                <> \bacaStopTextSpanRhythmAnnotation
                            }
                            <<
                                \context Voice = "Music_Voice"
                                {
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                }
                                \context Voice = "Rest_Voice"
                                {
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                }
                            >>
                        }
                    }
                }
            >>

    """

    __documentation_section__ = "Classes"

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        "_activate",
        "_allow_empty_selections",
        "_cache",
        "_cached_time_signatures",
        "_check_all_are_pitched",
        "_clock_time_extra_offset",
        "_clock_time_override",
        "_color_octaves",
        "_commands",
        "_container_to_part_assignment",
        "_deactivate",
        "_do_not_check_beamed_long_notes",
        "_do_not_check_out_of_range_pitches",
        "_do_not_check_persistence",
        "_do_not_check_wellformedness",
        "_do_not_include_layout_ly",
        "_do_not_force_nonnatural_accidentals",
        "_duration",
        "_environment",
        "_fermata_extra_offset_y",
        "_fermata_measure_empty_overrides",
        "_fermata_measure_numbers",
        "_fermata_start_offsets",
        "_fermata_stop_offsets",
        "_final_measure_is_fermata",
        "_first_measure_number",
        "_final_segment",
        "_first_segment",
        "_ignore_repeat_pitch_classes",
        "_includes",
        "_indicator_defaults",
        "_instruments",
        "_lilypond_file",
        "_local_measure_number_extra_offset",
        "_magnify_staves",
        "_margin_markups",
        "_measure_number_extra_offset",
        "_metadata",
        "_parts_metric_modulation_multiplier",
        "_metronome_marks",
        "_midi",
        "_moment_markup",
        "_offset_to_measure_number",
        "_page_layout_profile",
        "_persist",
        "_preamble",
        "_previous_metadata",
        "_previous_persist",
        "_remove",
        "_remove_phantom_measure",
        "_score",
        "_score_template",
        "_segment_bol_measure_numbers",
        "_segment_duration",
        "_segment_number",
        "_skips_instead_of_rests",
        "_spacing",
        "_spacing_extra_offset",
        "_stage_markup",
        "_stage_number_extra_offset",
        "_start_clock_time",
        "_stop_clock_time",
        "_test_container_identifiers",
        "_time_signatures",
        "_transpose_score",
        "_voice_metadata",
        "_voice_names",
    )

    _prototype_to_manifest_name = {
        "abjad.Instrument": "instruments",
        "abjad.MetronomeMark": "metronome_marks",
        "abjad.MarginMarkup": "margin_markups",
    }

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

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        activate=None,
        allow_empty_selections=False,
        check_all_are_pitched=False,
        clock_time_extra_offset=None,
        clock_time_override=None,
        color_octaves=False,
        deactivate=None,
        do_not_check_beamed_long_notes=False,
        do_not_check_out_of_range_pitches=False,
        do_not_check_persistence=False,
        do_not_check_wellformedness=False,
        do_not_force_nonnatural_accidentals=False,
        do_not_include_layout_ly=False,
        fermata_extra_offset_y=2.5,
        fermata_measure_empty_overrides=None,
        final_segment=False,
        first_measure_number=None,
        ignore_repeat_pitch_classes=False,
        indicator_defaults=None,
        includes=None,
        instruments=None,
        local_measure_number_extra_offset=None,
        magnify_staves=None,
        margin_markups=None,
        measure_number_extra_offset=None,
        metronome_marks=None,
        moment_markup=None,
        parts_metric_modulation_multiplier=None,
        phantom=False,
        preamble=None,
        remove=None,
        remove_phantom_measure=False,
        score_template=None,
        skips_instead_of_rests=False,
        spacing=None,
        spacing_extra_offset=None,
        stage_markup=None,
        stage_number_extra_offset=None,
        test_container_identifiers=False,
        time_signatures=None,
        transpose_score=False,
    ):
        if activate is not None:
            assert all(isinstance(_, abjad.Tag) for _ in activate)
        self._activate = activate
        self._allow_empty_selections = allow_empty_selections
        if check_all_are_pitched is not None:
            check_all_are_pitched = bool(check_all_are_pitched)
        self._check_all_are_pitched = check_all_are_pitched
        if clock_time_extra_offset not in (False, None):
            assert isinstance(clock_time_extra_offset, tuple)
            assert len(clock_time_extra_offset) == 2
        self._clock_time_extra_offset = clock_time_extra_offset
        if clock_time_override is not None:
            assert isinstance(clock_time_override, abjad.MetronomeMark)
        self._clock_time_override = clock_time_override
        self._color_octaves = color_octaves
        self._cache = None
        self._cached_time_signatures = []
        if deactivate is not None:
            assert all(isinstance(_, abjad.Tag) for _ in deactivate)
        self._container_to_part_assignment = None
        self._deactivate = deactivate
        if do_not_check_out_of_range_pitches is not None:
            do_not_check_out_of_range_pitches = bool(do_not_check_out_of_range_pitches)
        self._do_not_check_beamed_long_notes = do_not_check_beamed_long_notes
        self._do_not_check_out_of_range_pitches = do_not_check_out_of_range_pitches
        self._do_not_check_persistence = do_not_check_persistence
        self._do_not_check_wellformedness = do_not_check_wellformedness
        self._do_not_force_nonnatural_accidentals = do_not_force_nonnatural_accidentals
        self._do_not_include_layout_ly = do_not_include_layout_ly
        self._duration = None
        self._environment = None
        self._fermata_extra_offset_y = fermata_extra_offset_y
        self._fermata_measure_empty_overrides = fermata_measure_empty_overrides
        self._fermata_measure_numbers = []
        self._fermata_start_offsets = []
        self._fermata_stop_offsets = []
        self._first_measure_number = first_measure_number
        self._indicator_defaults = indicator_defaults
        self._ignore_repeat_pitch_classes = ignore_repeat_pitch_classes
        self._instruments = instruments
        self._final_measure_is_fermata = False
        self._final_segment = final_segment
        self._includes = includes
        self._lilypond_file = None
        self._local_measure_number_extra_offset = local_measure_number_extra_offset
        self._magnify_staves = magnify_staves
        self._margin_markups = margin_markups
        self._measure_number_extra_offset = measure_number_extra_offset
        self._metadata = abjad.OrderedDict()
        self._metronome_marks = metronome_marks
        self._midi = False
        self._moment_markup = moment_markup
        self._offset_to_measure_number = {}
        if parts_metric_modulation_multiplier is not None:
            assert isinstance(parts_metric_modulation_multiplier, tuple)
            assert len(parts_metric_modulation_multiplier) == 2
        self._parts_metric_modulation_multiplier = parts_metric_modulation_multiplier
        if remove_phantom_measure is not None:
            remove_phantom_measure = bool(remove_phantom_measure)
        self._persist = abjad.OrderedDict()
        preamble = preamble or ()
        if preamble:
            assert all(isinstance(_, str) for _ in preamble), repr(preamble)
        self._preamble = tuple(preamble)
        self._previous_metadata = None
        self._previous_persist = None
        if remove is not None:
            assert all(isinstance(_, abjad.Tag) for _ in remove)
        self._remove = remove
        self._remove_phantom_measure = remove_phantom_measure
        self._score = None
        assert score_template is not None, repr(score_template)
        self._score_template = score_template
        self._segment_bol_measure_numbers = []
        # TODO: harmonize _duration, _semgent_duration
        self._segment_duration = None
        self._segment_number = None
        self._skips_instead_of_rests = skips_instead_of_rests
        self._spacing = spacing
        self._spacing_extra_offset = spacing_extra_offset
        self._stage_markup = stage_markup
        self._stage_number_extra_offset = stage_number_extra_offset
        self._start_clock_time = None
        self._stop_clock_time = None
        if test_container_identifiers is not None:
            test_container_identifiers = bool(test_container_identifiers)
        self._test_container_identifiers = test_container_identifiers
        self._transpose_score = transpose_score
        self._voice_metadata = abjad.OrderedDict()
        self._voice_names = None
        self._commands = []
        self._initialize_time_signatures(time_signatures)

    ### SPECIAL METHODS ###

    def __call__(self, scopes, *commands):
        r"""
        Wraps each command in ``commands`` with each scope in ``scopes``.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     includes=["baca.ily"],
            ...     preamble=[baca.global_context_string()],
            ...     score_template=baca.make_empty_score_maker(1),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ... )

            >>> maker(
            ...     "Music_Voice",
            ...     baca.make_even_divisions(),
            ...     baca.label(lambda _: abjad.Label(_).with_indices()),
            ... )

            >>> lilypond_file = maker.run(environment="docs")
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context GlobalContext = "Global_Context"
                    <<
                        \context GlobalSkips = "Global_Skips"
                        {
                            \time 4/8
                            \baca-time-signature-color #'blue
                            s1 * 1/2
                            \time 3/8
                            \baca-time-signature-color #'blue
                            s1 * 3/8
                            \time 4/8
                            \baca-time-signature-color #'blue
                            s1 * 1/2
                            \time 3/8
                            \baca-time-signature-color #'blue
                            s1 * 3/8
                            \time 1/4
                            \baca-time-signature-transparent
                            s1 * 1/4
                            \once \override Score.BarLine.transparent = ##t
                            \once \override Score.SpanBar.transparent = ##t
                        }
                    >>
                    \context MusicContext = "Music_Context"
                    {
                        \context Staff = "Music_Staff"
                        {
                            \context Voice = "Music_Voice"
                            {
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 0 }
                                [
                                - \abjad-dashed-line-with-hook
                                - \baca-text-spanner-left-text "make_even_divisions()"
                                - \tweak bound-details.right.padding 2.75
                                - \tweak color #darkcyan
                                - \tweak staff-padding 8
                                \bacaStartTextSpanRhythmAnnotation
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 1 }
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 2 }
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 3 }
                                ]
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 4 }
                                [
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 5 }
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 6 }
                                ]
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 7 }
                                [
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 8 }
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 9 }
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 10 }
                                ]
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 11 }
                                [
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 12 }
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 13 }
                                ]
                                <> \bacaStopTextSpanRhythmAnnotation
                                <<
                                    \context Voice = "Music_Voice"
                                    {
                                        \abjad-invisible-music-coloring
                                        %@% \abjad-invisible-music
                                        \baca-not-yet-pitched-coloring
                                        b'1 * 1/4
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                    }
                                    \context Voice = "Rest_Voice"
                                    {
                                        \once \override Score.TimeSignature.X-extent = ##f
                                        \once \override MultiMeasureRest.transparent = ##t
                                        \stopStaff
                                        \once \override Staff.StaffSymbol.transparent = ##t
                                        \startStaff
                                        R1 * 1/4
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                    }
                                >>
                            }
                        }
                    }
                >>

        ..  container:: example

            Commands may be grouped into lists:

            >>> maker = baca.SegmentMaker(
            ...     includes=["baca.ily"],
            ...     preamble=[baca.global_context_string()],
            ...     score_template=baca.make_empty_score_maker(1),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ... )

            >>> commands = []
            >>> commands.append(baca.make_even_divisions())
            >>> commands.append(baca.label(lambda _: abjad.Label(_).with_indices()))

            >>> maker(
            ...     "Music_Voice",
            ...     commands,
            ... )

            >>> lilypond_file = maker.run(environment="docs")
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context GlobalContext = "Global_Context"
                    <<
                        \context GlobalSkips = "Global_Skips"
                        {
                            \time 4/8
                            \baca-time-signature-color #'blue
                            s1 * 1/2
                            \time 3/8
                            \baca-time-signature-color #'blue
                            s1 * 3/8
                            \time 4/8
                            \baca-time-signature-color #'blue
                            s1 * 1/2
                            \time 3/8
                            \baca-time-signature-color #'blue
                            s1 * 3/8
                            \time 1/4
                            \baca-time-signature-transparent
                            s1 * 1/4
                            \once \override Score.BarLine.transparent = ##t
                            \once \override Score.SpanBar.transparent = ##t
                        }
                    >>
                    \context MusicContext = "Music_Context"
                    {
                        \context Staff = "Music_Staff"
                        {
                            \context Voice = "Music_Voice"
                            {
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 0 }
                                [
                                - \abjad-dashed-line-with-hook
                                - \baca-text-spanner-left-text "make_even_divisions()"
                                - \tweak bound-details.right.padding 2.75
                                - \tweak color #darkcyan
                                - \tweak staff-padding 8
                                \bacaStartTextSpanRhythmAnnotation
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 1 }
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 2 }
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 3 }
                                ]
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 4 }
                                [
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 5 }
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 6 }
                                ]
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 7 }
                                [
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 8 }
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 9 }
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 10 }
                                ]
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 11 }
                                [
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 12 }
                                \baca-not-yet-pitched-coloring
                                b'8
                                ^ \markup { 13 }
                                ]
                                <> \bacaStopTextSpanRhythmAnnotation
                                <<
                                    \context Voice = "Music_Voice"
                                    {
                                        \abjad-invisible-music-coloring
                                        %@% \abjad-invisible-music
                                        \baca-not-yet-pitched-coloring
                                        b'1 * 1/4
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                    }
                                    \context Voice = "Rest_Voice"
                                    {
                                        \once \override Score.TimeSignature.X-extent = ##f
                                        \once \override MultiMeasureRest.transparent = ##t
                                        \stopStaff
                                        \once \override Staff.StaffSymbol.transparent = ##t
                                        \startStaff
                                        R1 * 1/4
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                    }
                                >>
                            }
                        }
                    }
                >>

        ..  container:: example exception

            Raises exception on noncommand input:

            >>> maker(
            ...     "Music_Voice",
            ...     "text",
            ... )
            Traceback (most recent call last):
                ...
            Exception:
            Must be command:
            'text'

        ..  container:: example exception

            Raises exception on unknown voice name:

            >>> maker(
            ...     "Percussion_Voice",
            ...     baca.make_repeated_duration_notes([(1, 4)]),
            ... )
            Traceback (most recent call last):
                ...
            Exception: unknown voice name 'Percussion_Voice'.

        """
        commands_ = _sequence.Sequence(commands).flatten(
            classes=(list, scoping.Suite), depth=-1
        )
        commands = tuple(commands_)
        self._cache_voice_names()
        if self.score_template is not None and hasattr(
            self.score_template, "voice_abbreviations"
        ):
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
                message += f"\n\n{repr(command)}"
                raise Exception(message)
        scope_count = len(scopes_)
        for i, current_scope in enumerate(scopes_):
            if self._voice_names and current_scope.voice_name not in self._voice_names:
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
                    commands_ = _sequence.Sequence([command])
                else:
                    commands_ = command
                for command_ in commands_:
                    assert isinstance(command_, scoping.Command), repr(command_)
                    measures = command_.measures
                    if isinstance(measures, int):
                        measures = (measures, measures)
                    if measures is not None:
                        scope_ = abjad.new(current_scope, measures=measures)
                    else:
                        scope_ = abjad.new(current_scope)
                    command_ = abjad.new(command_, scope=scope_)
                    self.commands.append(command_)

    def __eq__(self, expr):
        """
        Is true if ``expr`` is a segment-maker with equivalent properties.
        """
        return abjad.StorageFormatManager.compare_objects(self, expr)

    def __hash__(self):
        """
        Hashes segment-maker.
        """
        hash_values = abjad.StorageFormatManager(self).get_hash_values()
        return hash(hash_values)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _activate_tags(self):
        tags = self.activate
        if not tags:
            return
        assert all(isinstance(_, abjad.Tag) for _ in tags), repr(tags)
        for leaf in abjad.iterate(self.score).leaves():
            if not isinstance(leaf, abjad.Skip):
                continue
            wrappers = abjad.get.wrappers(leaf)
            for wrapper in wrappers:
                if wrapper.tag is None:
                    continue
                for tag in tags:
                    if tag in wrapper.tag:
                        wrapper.deactivate = False
                        break

    def _add_container_identifiers(self):
        if self.environment == "docs" and not getattr(
            self, "test_container_identifiers", False
        ):
            return
        if self.segment_number is not None:
            assert self.segment_number, repr(self.segment_number)
            segment_number = f"segment.{self.segment_number}"
        else:
            segment_number = ""
        contexts = []
        try:
            context = self.score["Global_Skips"]
            contexts.append(context)
        except ValueError:
            pass
        try:
            context = self.score["Global_Rests"]
            contexts.append(context)
        except ValueError:
            pass
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            if voice._has_indicator(const.INTERMITTENT):
                continue
            contexts.append(voice)
        container_to_part_assignment = abjad.OrderedDict()
        context_name_counts = {}
        for context in contexts:
            assert context.name is not None, repr(context)
            count = context_name_counts.get(context.name, 0)
            if count == 0:
                suffixed_context_name = context.name
            else:
                suffixed_context_name = f"{context.name}.count.{count}"
            context_name_counts[context.name] = count + 1
            if segment_number:
                context_identifier = f"{segment_number}.{suffixed_context_name}"
            else:
                context_identifier = suffixed_context_name
            context_identifier = context_identifier.replace("_", ".")
            context.identifier = f"%*% {context_identifier}"
            part_container_count = 0
            for container in abjad.iterate(context).components(abjad.Container):
                if not container.identifier:
                    continue
                if container.identifier.startswith("%*% Part"):
                    part_container_count += 1
                    part = container.identifier.strip("%*% ")
                    globals_ = globals()
                    globals_["PartAssignment"] = _parts.PartAssignment
                    part = eval(part, globals_)
                    container_identifier = (
                        f"{context_identifier}.part.{part_container_count}"
                    )
                    container_identifier = abjad.String(container_identifier)
                    assert "_" not in container_identifier, repr(container_identifier)
                    assert container_identifier not in container_to_part_assignment
                    timespan = container._get_timespan()
                    pair = (part, timespan)
                    container_to_part_assignment[container_identifier] = pair
                    container.identifier = f"%*% {container_identifier}"
        for staff in abjad.iterate(self.score).components(abjad.Staff):
            if segment_number:
                context_identifier = f"{segment_number}.{staff.name}"
            else:
                context_identifier = staff.name
            context_identifier = context_identifier.replace("_", ".")
            staff.identifier = f"%*% {context_identifier}"
        self._container_to_part_assignment = container_to_part_assignment

    def _alive_during_any_previous_segment(self, context) -> bool:
        assert isinstance(context, abjad.Context), repr(context)
        assert self.previous_persist is not None
        names = self.previous_persist.get("alive_during_segment", [])
        return context.name in names

    def _alive_during_previous_segment(self, context) -> bool:
        assert isinstance(context, abjad.Context), repr(context)
        assert self.previous_persist is not None
        names = self.previous_persist.get("alive_during_segment", [])
        return context.name in names

    def _analyze_memento(self, context, memento):
        previous_indicator = self._memento_to_indicator(memento)
        if previous_indicator is None:
            return
        if isinstance(previous_indicator, indicators.SpacingSection):
            return
        if memento.context in self.score:
            for context in abjad.iterate(self.score).components(abjad.Context):
                if context.name == memento.context:
                    memento_context = context
                    break
        else:
            # context alive in previous segment doesn't exist in this segment
            return
        leaf = abjad.get.leaf(memento_context, 0)
        if isinstance(previous_indicator, abjad.Instrument):
            prototype = abjad.Instrument
        else:
            prototype = type(previous_indicator)
        indicator = abjad.get.indicator(leaf, prototype)
        status = None
        if indicator is None:
            status = "reapplied"
        elif not scoping.compare_persistent_indicators(previous_indicator, indicator):
            status = "explicit"
        elif isinstance(previous_indicator, abjad.TimeSignature):
            status = "reapplied"
        else:
            status = "redundant"
        edition = memento.edition or abjad.Tag()
        if memento.synthetic_offset is None:
            synthetic_offset = None
        else:
            assert 0 < memento.synthetic_offset, repr(memento)
            synthetic_offset = -memento.synthetic_offset
        return leaf, previous_indicator, status, edition, synthetic_offset

    @staticmethod
    def _append_tag_to_wrappers(leaf, tag):
        assert isinstance(tag, abjad.Tag), repr(tag)
        for wrapper in abjad.get.wrappers(leaf):
            if isinstance(wrapper.indicator, abjad.LilyPondLiteral):
                if wrapper.indicator.argument == "":
                    continue
            tag_ = wrapper.tag.append(tag)
            wrapper.tag = tag_

    def _apply_breaks(self):
        if self.spacing is None:
            return
        if self.spacing.breaks is None:
            return
        global_skips = self.score["Global_Skips"]
        skips = _selection.Selection(global_skips).skips()
        measure_count = len(skips)
        literal = abjad.LilyPondLiteral(r"\autoPageBreaksOff", "before")
        abjad.attach(
            literal,
            skips[0],
            tag=_tags.BREAK.append(abjad.Tag("baca.BreakMeasureMap.__call__(1)")),
        )
        for skip in skips[:measure_count]:
            if not abjad.get.has_indicator(skip, _layout.LBSD):
                literal = abjad.LilyPondLiteral(r"\noBreak", "before")
                abjad.attach(
                    literal,
                    skip,
                    tag=_tags.BREAK.append(
                        abjad.Tag("baca.BreakMeasureMap.__call__(2)")
                    ),
                )
        assert self.spacing.breaks.commands is not None
        for measure_number, commands in self.spacing.breaks.commands.items():
            if measure_count < measure_number:
                message = f"score ends at measure {measure_count}"
                message += f" (not {measure_number})."
                raise Exception(message)
            for command in commands:
                command(global_skips)

    def _apply_spacing(self):
        if self.spacing is None:
            return
        with abjad.Timer() as timer:
            self.spacing(self)
        count = int(timer.elapsed_time)
        if False:
            seconds = abjad.String("second").pluralize(count)
            raise Exception(f"spacing application {count} {seconds}!")
        return count

    def _assert_nonoverlapping_rhythms(self, rhythms, voice):
        previous_stop_offset = 0
        for rhythm in rhythms:
            start_offset = rhythm.start_offset
            if start_offset < previous_stop_offset:
                raise Exception(f"{voice} has overlapping rhythms.")
            duration = abjad.get.duration(rhythm.annotation)
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
        if isinstance(wrapper.indicator, _memento.PersistentOverride):
            return
        if isinstance(wrapper.indicator, indicators.BarExtent):
            return
        stem = scoping.Command._to_indicator_stem(wrapper.indicator)
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
            literal = abjad.LilyPondLiteral(string, format_slot="after")
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
        status_tag = SegmentMaker._get_tag(status, stem, prefix=prefix, suffix=suffix)
        if isinstance(wrapper.indicator, abjad.TimeSignature):
            string = rf"\baca-time-signature-color #'{color}"
            literal = abjad.LilyPondLiteral(string)
        if cancelation is True:
            tag = _site(inspect.currentframe(), 1)
            tag = tag.append(status_tag)
            abjad.attach(literal, wrapper.component, deactivate=True, tag=tag)
        else:
            tag = _site(inspect.currentframe(), 2)
            tag = tag.append(status_tag)
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
        always_make_global_rests = getattr(
            self.score_template, "always_make_global_rests", False
        )
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

    def _attach_first_appearance_score_template_defaults(self):
        if self.first_segment:
            return
        staff__group = (abjad.Staff, abjad.StaffGroup)
        dictionary = self.previous_persist["persistent_indicators"]
        for staff__group in abjad.iterate(self.score).components(staff__group):
            if staff__group.name in dictionary:
                continue
            for wrapper in _templates.attach_defaults(staff__group):
                self._treat_persistent_wrapper(self.manifests, wrapper, "default")

    def _attach_first_segment_score_template_defaults(self):
        if not self.first_segment:
            return
        for wrapper in _templates.attach_defaults(self.score):
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
                tag = _tags.DEFAULT_INSTRUMENT_ALERT
            elif status == "explicit":
                tag = _tags.EXPLICIT_INSTRUMENT_ALERT
            elif status == "reapplied":
                tag = _tags.REAPPLIED_INSTRUMENT_ALERT
            else:
                assert status == "redundant", repr(status)
                tag = _tags.REDUNDANT_INSTRUMENT_ALERT
            left, right = "(", ")"
        else:
            assert isinstance(indicator, abjad.MarginMarkup)
            if status == "default":
                tag = _tags.DEFAULT_MARGIN_MARKUP_ALERT
            elif status == "explicit":
                tag = _tags.EXPLICIT_MARGIN_MARKUP_ALERT
            elif status == "reapplied":
                tag = _tags.REAPPLIED_MARGIN_MARKUP_ALERT
            else:
                assert status == "redundant", repr(status)
                tag = _tags.REDUNDANT_MARGIN_MARKUP_ALERT
            left, right = "[", "]"
        assert isinstance(tag, abjad.Tag), repr(tag)
        string = f"{left}{key}{right}"
        markup_function = SegmentMaker._status_to_markup_function[status]
        string = fr'\{markup_function} "{string}"'
        markup = abjad.Markup(string, direction=abjad.Up, literal=True)
        tag = tag.append(_site(inspect.currentframe()))
        abjad.attach(markup, leaf, deactivate=existing_deactivate, tag=tag)

    def _attach_metronome_marks(self):
        indicator_count = 0
        skips = _selection.Selection(self.score["Global_Skips"]).skips()
        final_leaf_metronome_mark = abjad.get.indicator(skips[-1], abjad.MetronomeMark)
        add_right_text_to_me = None
        if final_leaf_metronome_mark:
            tempo_prototype = (
                abjad.MetronomeMark,
                indicators.Accelerando,
                indicators.Ritardando,
            )
            for skip in reversed(skips[:-1]):
                if abjad.get.has_indicator(skip, tempo_prototype):
                    add_right_text_to_me = skip
                    break
        for i, skip in enumerate(skips):
            metronome_mark = abjad.get.indicator(skip, abjad.MetronomeMark)
            metric_modulation = abjad.get.indicator(skip, abjad.MetricModulation)
            accelerando = abjad.get.indicator(skip, indicators.Accelerando)
            ritardando = abjad.get.indicator(skip, indicators.Ritardando)
            if (
                metronome_mark is None
                and metric_modulation is None
                and accelerando is None
                and ritardando is None
            ):
                continue
            if metronome_mark is not None:
                metronome_mark._hide = True
                wrapper = abjad.get.wrapper(skip, abjad.MetronomeMark)
            if metric_modulation is not None:
                metric_modulation._hide = True
            if accelerando is not None:
                accelerando._hide = True
            if ritardando is not None:
                ritardando._hide = True
            if skip is skips[-1]:
                break
            if metronome_mark is None and metric_modulation is not None:
                wrapper = abjad.get.wrapper(skip, abjad.MetricModulation)
            if metronome_mark is None and accelerando is not None:
                wrapper = abjad.get.wrapper(skip, indicators.Accelerando)
            if metronome_mark is None and ritardando is not None:
                wrapper = abjad.get.wrapper(skip, indicators.Ritardando)
            has_trend = accelerando is not None or ritardando is not None
            indicator_count += 1
            tag = wrapper.tag
            stripped_left_text = None
            if metronome_mark is not None:
                if metric_modulation is not None:
                    if metronome_mark.custom_markup is not None:
                        left_text = str(metronome_mark._get_markup())
                        if left_text.startswith(r"\markup"):
                            left_text = left_text[8:]
                        modulation = str(metric_modulation._get_markup())
                        if modulation.startswith(r"\markup"):
                            modulation = modulation[8:]
                        string = rf"\concat {{ {left_text} \hspace #2 \upright ["
                        string += rf" \line {{ {modulation} }} \hspace #0.5"
                        string += r" \upright ] }"
                        left_text = abjad.Markup(string, literal=True)
                    else:
                        left_text = self._bracket_metric_modulation(
                            metronome_mark, metric_modulation
                        )

                    if metronome_mark.custom_markup is not None:
                        stripped_left_text = (
                            r"- \baca-metronome-mark-spanner-left-markup"
                        )
                        string = abjad.lilypond(metronome_mark.custom_markup)
                        assert string.startswith("\\")
                        stripped_left_text += f" {string}"
                    # mixed number
                    elif metronome_mark.decimal is True:
                        arguments = metronome_mark._get_markup_arguments()
                        log, dots, stem, base, n, d = arguments
                        stripped_left_text = (
                            r"- \baca-metronome-mark-spanner-left-text-mixed-number"
                        )
                        stripped_left_text += (
                            f' {log} {dots} {stem} "{base}" "{n}" "{d}"'
                        )
                    else:
                        arguments = metronome_mark._get_markup_arguments()
                        log, dots, stem, value = arguments
                        stripped_left_text = r"- \baca-metronome-mark-spanner-left-text"
                        stripped_left_text += f' {log} {dots} {stem} "{value}"'
                elif metronome_mark.custom_markup is not None:
                    assert metronome_mark.custom_markup.literal
                    left_text = r"- \baca-metronome-mark-spanner-left-markup"
                    string = abjad.lilypond(metronome_mark.custom_markup)
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
                stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanMM")
                abjad.attach(stop_text_span, skip, tag=_site(inspect.currentframe(), 1))
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
                string = ":".join(words)
                new_tag = abjad.Tag(string)
                indicator = wrapper.indicator
                abjad.detach(wrapper, skip)
                abjad.attach(
                    indicator,
                    skip,
                    tag=new_tag.append(_site(inspect.currentframe(), 5)),
                )
                tag = new_tag
            if not (
                isinstance(start_text_span.left_text, str)
                and start_text_span.left_text.endswith("(1 . 1)")
                and self.parts_metric_modulation_multiplier is not None
            ):
                abjad.attach(
                    start_text_span,
                    skip,
                    deactivate=True,
                    tag=tag.append(_site(inspect.currentframe(), 2)),
                )
            else:
                abjad.attach(
                    start_text_span,
                    skip,
                    deactivate=True,
                    tag=tag.append(_site(inspect.currentframe(), 2.1)).append(
                        _tags.METRIC_MODULATION_IS_NOT_SCALED,
                    ),
                )
                left_text_ = start_text_span.left_text
                assert left_text_.endswith("(1 . 1)")
                n, d = self.parts_metric_modulation_multiplier
                left_text_ = left_text_[:-7] + f"({n} . {d})"
                start_text_span_ = abjad.new(start_text_span, left_text=left_text_)
                abjad.attach(
                    start_text_span_,
                    skip,
                    deactivate=True,
                    tag=tag.append(_site(inspect.currentframe(), 2.2)).append(
                        _tags.METRIC_MODULATION_IS_SCALED,
                    ),
                )
            if stripped_left_text is not None:
                start_text_span_ = abjad.new(
                    start_text_span, left_text=stripped_left_text
                )
                abjad.attach(
                    start_text_span_,
                    skip,
                    deactivate=True,
                    tag=tag.append(_site(inspect.currentframe(), 2.2)).append(
                        _tags.METRIC_MODULATION_IS_STRIPPED,
                    ),
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
            string = f"{status.upper()}_METRONOME_MARK_WITH_COLOR"
            tag = abjad.Tag(string)
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
                color = f"(x11-color '{color})"
                assert len(left_text.contents) == 1, repr(left_text)
                left_text_with_color = abjad.Markup(
                    rf"\with-color #{color} {left_text.contents[0]}",
                    literal=True,
                )
            if right_text:
                wrapper = abjad.get.wrapper(skips[-1], abjad.MetronomeMark)
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
                color = f"(x11-color '{color})"
                assert len(right_text.contents) == 1, repr(right_text)
                right_text_with_color = abjad.Markup(
                    rf"\with-color #{color} {right_text.contents[0]}",
                    literal=True,
                )
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
                tag=tag.append(_site(inspect.currentframe(), 3)),
            )
        if indicator_count:
            final_skip = skip
            stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanMM")
            tag_ = _tags.EOS_STOP_MM_SPANNER
            tag_ = tag_.append(_site(inspect.currentframe(), 4))
            abjad.attach(stop_text_span, final_skip, tag=tag_)

    # this exists because of an incompletely implemented behavior in LilyPond;
    # LilyPond doesn't understand repeat-tied notes to be tied;
    # because of this LilyPond incorrectly prints accidentals in front of some
    # repeat-tied notes;
    # this method works around LilyPond's behavior
    def _attach_shadow_tie_indicators(self):
        tag = _site(inspect.currentframe())
        for plt in _selection.Selection(self.score).plts():
            if len(plt) == 1:
                continue
            for pleaf in plt[:-1]:
                if abjad.get.has_indicator(pleaf, abjad.Tie):
                    continue
                tie = abjad.Tie()
                abjad.tweak(tie).stencil = False
                abjad.attach(tie, pleaf, tag=tag)

    def _attach_sounds_during(self):
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            pleaves = []
            for pleaf in _selection.Selection(voice).pleaves():
                if abjad.get.has_indicator(pleaf, const.PHANTOM):
                    continue
                pleaves.append(pleaf)
            if bool(pleaves):
                abjad.attach(const.SOUNDS_DURING_SEGMENT, voice)

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
                raise Exception("implement tied note values in metric modulation.")
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
                raise Exception("implement tied note values in metric modulation.")
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
        manifests["previous_segment_voice_metadata"] = previous_segment_voice_metadata
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
        indicator = const.FERMATA_MEASURE
        for measure_index, rest in enumerate(rests):
            if not abjad.get.has_indicator(rest, indicator):
                continue
            if measure_index == final_measure_index:
                self._final_measure_is_fermata = True
            measure_number = first_measure_number + measure_index
            timespan = abjad.get.timespan(rest)
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
            parentage = abjad.get.parentage(leaf)
            context = parentage.get(abjad.Context)
            leaves_by_measure_number = self._cache.setdefault(
                context.name, abjad.OrderedDict()
            )
            leaf_timespan = abjad.get.timespan(leaf)
            # TODO: replace loop with bisection:
            for i, measure_timespan in enumerate(measure_timespans):
                measure_number = i + 1
                if leaf_timespan.starts_during_timespan(measure_timespan):
                    cached_leaves = leaves_by_measure_number.setdefault(
                        measure_number, []
                    )
                    cached_leaves.append(leaf)

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
        skips = _selection.Selection(self.score["Global_Skips"]).skips()
        if "Global_Rests" not in self.score:
            return
        for context in abjad.iterate(self.score).components(abjad.Context):
            if context.name == "Global_Rests":
                break
        # rests = _selection.Selection(self.score["Global_Rests"]).rests()
        rests = _selection.Selection(context).rests()
        assert len(skips) == len(rests)
        start_clock_time = self._get_previous_stop_clock_time()
        start_clock_time = start_clock_time or "0'00''"
        self._start_clock_time = start_clock_time
        start_offset = abjad.Duration.from_clock_string(start_clock_time)
        if self.clock_time_override:
            metronome_mark = self.clock_time_override
            abjad.attach(metronome_mark, skips[0])
        if abjad.get.effective(skips[0], abjad.MetronomeMark) is None:
            return
        first_measure_number = self._get_first_measure_number()
        clock_times = []
        for local_measure_index, skip in enumerate(skips):
            measure_number = first_measure_number + local_measure_index
            if measure_number not in self._fermata_measure_numbers:
                clock_times.append(start_offset)
                duration = abjad.get.duration(skip, in_seconds=True)
            else:
                rest = rests[local_measure_index]
                fermata_duration = abjad.get.annotation(rest, const.FERMATA_DURATION)
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
            except Exception:
                print(f"Interpreting ...\n\n{abjad.storage(command)}\n")
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
        tag = _site(inspect.currentframe())
        if self.skips_instead_of_rests:
            prototype = abjad.Skip
        else:
            prototype = abjad.MultimeasureRest
        silence_maker = rmakers.multiplied_duration(prototype, tag=tag)
        for voice in abjad.select(self.score).components(abjad.Voice):
            assert not len(voice), repr(voice)
            voice_metadata = self._voice_metadata.get(voice.name, abjad.OrderedDict())
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
                    raise Exception(abjad.storage(command))
                measures = command.scope.measures
                result = self._get_measure_time_signatures(*measures)
                start_offset, time_signatures = result
                runtime = self._bundle_manifests(voice.name)
                selection = None
                try:
                    selection = command._make_selection(time_signatures, runtime)
                except Exception:
                    print(f"Interpreting ...\n\n{abjad.storage(command)}\n")
                    raise
                if selection is not None:
                    _attach_rhythm_annotation_spanner(command, selection)
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
                final_leaf = abjad.get.leaf(selections, -1)
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

    def _check_all_are_pitched_(self):
        if not self.check_all_are_pitched:
            return
        indicator = const.NOT_YET_PITCHED
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            for leaf in abjad.iterate(voice).leaves():
                if abjad.get.has_indicator(leaf, indicator):
                    message = "not yet pitched:\n"
                    message += f"   {repr(leaf)} in {voice.name}"
                    raise Exception(message)

    def _check_all_music_in_part_containers(self):
        name = "all_music_in_part_containers"
        if getattr(self.score_template, name, None) is not True:
            return
        indicator = const.MULTIMEASURE_REST_CONTAINER
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            for component in voice:
                if isinstance(component, (abjad.MultimeasureRest, abjad.Skip)):
                    continue
                if abjad.get.has_indicator(component, const.HIDDEN):
                    continue
                if abjad.get.has_indicator(component, indicator):
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
            dynamics = abjad.get.indicators(leaf, abjad.Dynamic)
            if 1 < len(dynamics):
                voice = abjad.get.parentage(leaf).get(abjad.Voice)
                message = f"leaf {str(leaf)} in {voice.name} has"
                message += f" {len(dynamics)} dynamics attached:"
                for dynamic in dynamics:
                    message += f"\n   {dynamic!s}"
                raise Exception(message)

    def _check_duplicate_part_assignments(self):
        dictionary = self._container_to_part_assignment
        if not dictionary:
            return
        if not self.score_template:
            return
        part_manifest = self.score_template.part_manifest
        if not part_manifest:
            return
        part_to_timespans = abjad.OrderedDict()
        for identifier, (part_assignment, timespan) in dictionary.items():
            for part in part_manifest.expand(part_assignment):
                if part.name not in part_to_timespans:
                    part_to_timespans[part.name] = []
                part_to_timespans[part.name].append(timespan)
        messages = []
        for part_name, timespans in part_to_timespans.items():
            if len(timespans) <= 1:
                continue
            timespan_list = abjad.TimespanList(timespans)
            if timespan_list.compute_logical_and():
                message = f"  Part {part_name!r} is assigned"
                message += " to overlapping containers ..."
                messages.append(message)
        if messages:
            message = "\n" + "\n".join(messages)
            raise Exception(message)

    def _check_persistent_indicators(self):
        if self.do_not_check_persistence:
            return
        if self.environment == "docs":
            return
        indicator = const.SOUNDS_DURING_SEGMENT
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            if not abjad.get.has_indicator(voice, indicator):
                continue
            for i, leaf in enumerate(abjad.iterate(voice).leaves()):
                self._check_persistent_indicators_for_leaf(voice.name, leaf, i)

    def _check_persistent_indicators_for_leaf(self, voice, leaf, i):
        prototype = (
            indicators.Accelerando,
            abjad.MetronomeMark,
            indicators.Ritardando,
        )
        mark = abjad.get.effective(leaf, prototype)
        if mark is None:
            message = f"{voice} leaf {i} ({leaf!s}) missing metronome mark."
            raise Exception(message)
        instrument = abjad.get.effective(leaf, abjad.Instrument)
        if instrument is None:
            message = f"{voice} leaf {i} ({leaf!s}) missing instrument."
            raise Exception(message)
        if not self.score_template.do_not_require_margin_markup:
            markup = abjad.get.effective(leaf, abjad.MarginMarkup)
            if markup is None:
                message = f"{voice} leaf {i} ({leaf!s}) missing margin markup."
                raise Exception(message)
        clef = abjad.get.effective(leaf, abjad.Clef)
        if clef is None:
            raise Exception(f"{voice} leaf {i} ({leaf!s}) missing clef.")

    def _check_wellformedness(self):
        if self.do_not_check_wellformedness:
            return
        check_beamed_long_notes = not self.do_not_check_beamed_long_notes
        check_out_of_range_pitches = not self.do_not_check_out_of_range_pitches
        if not abjad.wf.wellformed(
            self.score,
            check_beamed_long_notes=check_beamed_long_notes,
            check_out_of_range_pitches=check_out_of_range_pitches,
        ):
            message = abjad.wf.tabulate_wellformedness(
                self.score,
                check_beamed_long_notes=check_beamed_long_notes,
                check_out_of_range_pitches=check_out_of_range_pitches,
            )
            raise Exception("\n" + message)

    def _clean_up_laissez_vibrer_tie_direction(self):
        default = abjad.Clef("treble")
        for note in abjad.iterate(self.score).leaves(abjad.Note):
            if note.written_duration < 1:
                continue
            if not abjad.get.has_indicator(note, abjad.LaissezVibrer):
                continue
            clef = abjad.get.effective(note, abjad.Clef, default=default)
            staff_position = abjad.StaffPosition.from_pitch_and_clef(
                note.written_pitch,
                clef,
            )
            if staff_position == abjad.StaffPosition(0):
                abjad.override(note).laissez_vibrer_tie.direction = abjad.Up

    def _clean_up_repeat_tie_direction(self):
        default = abjad.Clef("treble")
        for leaf in abjad.iterate(self.score).leaves(pitched=True):
            if leaf.written_duration < 1:
                continue
            if not abjad.get.has_indicator(leaf, abjad.RepeatTie):
                continue
            clef = abjad.get.effective(leaf, abjad.Clef, default=default)
            if hasattr(leaf, "written_pitch"):
                note_heads = [leaf.note_head]
            else:
                note_heads = leaf.note_heads
            for note_head in note_heads:
                staff_position = abjad.StaffPosition.from_pitch_and_clef(
                    note_head.written_pitch, clef
                )
                if staff_position.number == 0:
                    repeat_tie = abjad.get.indicator(leaf, abjad.RepeatTie)
                    abjad.tweak(repeat_tie).direction = abjad.Up
                    break

    def _clean_up_on_beat_grace_containers(self):
        prototype = abjad.OnBeatGraceContainer
        for container in abjad.select(self.score).components(prototype):
            container._match_anchor_leaf()
            container._set_leaf_durations()
            container._attach_lilypond_one_voice()

    def _clean_up_rhythm_maker_voice_names(self):
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            if voice.name == "Rhythm_Maker_Music_Voice":
                outer = abjad.get.parentage(voice).get(abjad.Voice, 1)
                voice.name = outer.name

    def _clone_segment_initial_short_instrument_name(self):
        if self.first_segment:
            return
        prototype = abjad.MarginMarkup
        for context in abjad.iterate(self.score).components(abjad.Context):
            first_leaf = abjad.get.leaf(context, 0)
            if abjad.get.has_indicator(first_leaf, abjad.StartMarkup):
                continue
            margin_markup = abjad.get.indicator(first_leaf, prototype)
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
            abjad.attach(start_markup, first_leaf, tag=_site(inspect.currentframe()))

    def _collect_alive_during_segment(self):
        result = []
        for context in abjad.iterate(self.score).components(abjad.Context):
            if context.name not in result:
                result.append(context.name)
        return result

    def _collect_metadata(self):
        metadata, persist = abjad.OrderedDict(), abjad.OrderedDict()
        persist["alive_during_segment"] = self._collect_alive_during_segment()
        # make-layout-ly scripts adds bol measure numbers to metadata
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
        name_to_wrappers = abjad.OrderedDict()
        for context in contexts:
            if context.name not in name_to_wrappers:
                name_to_wrappers[context.name] = []
            wrappers = context._dependent_wrappers[:]
            name_to_wrappers[context.name].extend(wrappers)
        do_not_persist_on_phantom_measure = (
            abjad.Instrument,
            abjad.MetronomeMark,
            abjad.MarginMarkup,
            abjad.TimeSignature,
        )
        for name, dependent_wrappers in name_to_wrappers.items():
            mementos = []
            wrappers = []
            dictionary = abjad._inspect._get_persistent_wrappers(
                dependent_wrappers=dependent_wrappers,
                omit_with_indicator=const.PHANTOM,
            )
            for wrapper in dictionary.values():
                if isinstance(wrapper.indicator, do_not_persist_on_phantom_measure):
                    wrappers.append(wrapper)
            dictionary = abjad._inspect._get_persistent_wrappers(
                dependent_wrappers=dependent_wrappers
            )
            for wrapper in dictionary.values():
                if not isinstance(wrapper.indicator, do_not_persist_on_phantom_measure):
                    wrappers.append(wrapper)
            for wrapper in wrappers:
                leaf = wrapper.component
                parentage = abjad.get.parentage(leaf)
                first_context = parentage.get(abjad.Context)
                indicator = wrapper.indicator
                if isinstance(indicator, abjad.Glissando):
                    continue
                if isinstance(indicator, abjad.RepeatTie):
                    continue
                if isinstance(indicator, abjad.StopBeam):
                    continue
                if isinstance(indicator, abjad.StopPhrasingSlur):
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
                    string = ":".join(words)
                    editions = abjad.Tag(string)
                else:
                    editions = None
                memento = _memento.Memento(
                    context=first_context.name,
                    edition=editions,
                    manifest=manifest,
                    prototype=prototype,
                    synthetic_offset=wrapper.synthetic_offset,
                    value=value,
                )
                mementos.append(memento)
            if mementos:
                mementos.sort(key=lambda _: abjad.storage(_))
                result[name] = mementos
        dictionary = self.previous_persist.get("persistent_indicators")
        if dictionary:
            for context_name, mementos in dictionary.items():
                if context_name not in result:
                    result[context_name] = mementos
        return result

    def _color_mock_pitch(self):
        indicator = const.MOCK
        tag = _site(inspect.currentframe())
        tag = tag.append(_tags.MOCK_COLORING)
        leaves = []
        for pleaf in abjad.iterate(self.score).leaves(pitched=True):
            if not abjad.get.has_indicator(pleaf, indicator):
                continue
            string = r"\baca-mock-coloring"
            literal = abjad.LilyPondLiteral(string, format_slot="before")
            abjad.attach(literal, pleaf, tag=tag)
            leaves.append(pleaf)

    def _color_not_yet_pitched(self):
        indicator = const.NOT_YET_PITCHED
        tag = _site(inspect.currentframe())
        tag = tag.append(_tags.NOT_YET_PITCHED_COLORING)
        leaves = []
        for pleaf in abjad.iterate(self.score).leaves(pitched=True):
            if not abjad.get.has_indicator(pleaf, indicator):
                continue
            string = r"\baca-not-yet-pitched-coloring"
            literal = abjad.LilyPondLiteral(string, format_slot="before")
            tag_ = tag
            if abjad.get.has_indicator(pleaf, const.HIDDEN):
                tag_ = tag_.append(_tags.HIDDEN)
            if abjad.get.has_indicator(pleaf, const.NOTE):
                tag_ = tag_.append(_tags.NOTE)
            abjad.attach(literal, pleaf, tag=tag_)
            leaves.append(pleaf)

    def _color_not_yet_registered(self):
        indicator = const.NOT_YET_REGISTERED
        tag = _site(inspect.currentframe())
        tag = tag.append(_tags.NOT_YET_REGISTERED_COLORING)
        for pleaf in abjad.iterate(self.score).leaves(pitched=True):
            if not abjad.get.has_indicator(pleaf, indicator):
                continue
            string = r"\baca-not-yet-registered-coloring"
            literal = abjad.LilyPondLiteral(string, format_slot="before")
            abjad.attach(literal, pleaf, tag=tag)

    def _color_octaves_(self):
        if not self.color_octaves:
            return
        score = self.score
        vertical_moments = abjad.iterate_vertical_moments(score)
        markup = abjad.Markup("OCTAVE", direction=abjad.Up)
        abjad.tweak(markup).color = "#red"
        tag = _site(inspect.currentframe())
        tag = tag.append(_tags.OCTAVE_COLORING)
        for vertical_moment in vertical_moments:
            pleaves, pitches = [], []
            for leaf in vertical_moment.leaves:
                if abjad.get.has_indicator(leaf, const.HIDDEN):
                    continue
                if abjad.get.has_indicator(leaf, const.STAFF_POSITION):
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
                    if abjad.get.has_indicator(pleaf, const.ALLOW_OCTAVE):
                        color = False
                if not color:
                    continue
                for pleaf in pleaves:
                    abjad.attach(markup, pleaf, tag=tag)
                    string = r"\baca-octave-coloring"
                    literal = abjad.LilyPondLiteral(string, format_slot="before")
                    abjad.attach(literal, pleaf, tag=tag)

    def _color_out_of_range(self):
        indicator = const.ALLOW_OUT_OF_RANGE
        tag = _site(inspect.currentframe())
        tag = tag.append(_tags.OUT_OF_RANGE_COLORING)
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            for pleaf in abjad.iterate(voice).leaves(pitched=True):
                if abjad.get.has_indicator(pleaf, const.HIDDEN):
                    continue
                if abjad.get.has_indicator(pleaf, indicator):
                    continue
                instrument = abjad.get.effective(pleaf, abjad.Instrument)
                if instrument is None:
                    continue
                if not abjad.iterpitches.sounding_pitches_are_in_range(
                    pleaf, instrument.pitch_range
                ):
                    string = r"\baca-out-of-range-coloring"
                    literal = abjad.LilyPondLiteral(string, format_slot="before")
                    abjad.attach(literal, pleaf, tag=tag)

    def _color_repeat_pitch_classes_(self):
        tag = _site(inspect.currentframe())
        tag = tag.append(_tags.REPEAT_PITCH_CLASS_COLORING)
        lts = self._find_repeat_pitch_classes(self.score)
        for lt in lts:
            for leaf in lt:
                string = r"\baca-repeat-pitch-class-coloring"
                literal = abjad.LilyPondLiteral(string, format_slot="before")
                abjad.attach(literal, leaf, tag=tag)

    def _comment_measure_numbers(self):
        if self.environment == "docs":
            return
        first_measure_number = self._get_first_measure_number()
        for leaf in abjad.iterate(self.score).leaves():
            offset = abjad.get.timespan(leaf).start_offset
            measure_number = self._offset_to_measure_number.get(offset, None)
            if measure_number is None:
                continue
            local_measure_number = measure_number - first_measure_number
            local_measure_number += 1
            context = abjad.get.parentage(leaf).get(abjad.Context)
            string = f"% [{context.name} measure {local_measure_number}]"
            literal = abjad.LilyPondLiteral(string, format_slot="absolute_before")
            abjad.attach(literal, leaf, tag=_site(inspect.currentframe()))

    def _deactivate_tags(self):
        tags = self.deactivate
        if not tags:
            return
        assert all(isinstance(_, abjad.Tag) for _ in tags), repr(tags)
        for leaf in abjad.iterate(self.score).leaves():
            wrappers = abjad.get.wrappers(leaf)
            for wrapper in wrappers:
                if wrapper.tag is None:
                    continue
                for tag in tags:
                    if tag in wrapper.tag:
                        wrapper.deactivate = True
                        break

    @staticmethod
    def _extend_beam(leaf):
        if not abjad.get.has_indicator(leaf, abjad.StopBeam):
            parentage = abjad.get.parentage(leaf)
            voice = parentage.get(abjad.Voice)
            message = f"{leaf!s} in {voice.name} has no StopBeam."
            raise Exception(message)
        abjad.detach(abjad.StopBeam, leaf)
        if not abjad.get.has_indicator(leaf, abjad.StartBeam):
            abjad.detach(abjad.BeamCount, leaf)
            left = leaf.written_duration.flag_count
            beam_count = abjad.BeamCount(left, 1)
            abjad.attach(beam_count, leaf, "_extend_beam")
        current_leaf = leaf
        while True:
            next_leaf = abjad.get.leaf(current_leaf, 1)
            if next_leaf is None:
                parentage = abjad.get.parentage(current_leaf)
                voice = parentage.get(abjad.Voice)
                message = f"no leaf follows {current_leaf!s} in {voice.name};"
                message += "\n\tDo not set extend_beam=True on last figure."
                raise Exception(message)
                return
            if abjad.get.has_indicator(next_leaf, abjad.StartBeam):
                abjad.detach(abjad.StartBeam, next_leaf)
                if not abjad.get.has_indicator(next_leaf, abjad.StopBeam):
                    abjad.detach(abjad.BeamCount, next_leaf)
                    right = next_leaf.written_duration.flag_count
                    beam_count = abjad.BeamCount(1, right)
                    abjad.attach(beam_count, next_leaf, "_extend_beam")
                return
            current_leaf = next_leaf

    def _extend_beams(self):
        for leaf in abjad.iterate(self.score).leaves():
            if abjad.get.indicator(leaf, const.RIGHT_BROKEN_BEAM):
                self._extend_beam(leaf)

    @staticmethod
    def _find_repeat_pitch_classes(argument):
        violators = []
        for voice in abjad.iterate(argument).components(abjad.Voice):
            if abjad.get.has_indicator(voice, const.INTERMITTENT):
                continue
            previous_lt, previous_pcs = None, []
            for lt in abjad.iterate(voice).logical_ties():
                if abjad.get.has_indicator(lt.head, const.HIDDEN):
                    written_pitches = []
                elif isinstance(lt.head, abjad.Note):
                    written_pitches = [lt.head.written_pitch]
                elif isinstance(lt.head, abjad.Chord):
                    written_pitches = lt.head.written_pitches
                else:
                    written_pitches = []
                pcs = pitchclasses.PitchClassSet(written_pitches)
                if abjad.get.has_indicator(
                    lt.head, const.NOT_YET_PITCHED
                ) or abjad.get.has_indicator(lt.head, const.ALLOW_REPEAT_PITCH):
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
        for plt in _selection.Selection(self.score).plts():
            if isinstance(plt[0], abjad.Note):
                note_heads = [plt[0].note_head]
            else:
                note_heads = plt[0].note_heads
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
            assert self.includes, repr(self.includes)
            return self.includes
        includes = ["../../stylesheet.ily"]
        if self.clock_time_extra_offset is not None:
            value = self.clock_time_extra_offset
            assert isinstance(value, tuple)
            string = f"#'({value[0]} . {value[1]})"
            string = f"clock-time-extra-offset = {string}"
            literal = abjad.LilyPondLiteral(string)
            includes.append(literal)
        if self.local_measure_number_extra_offset is not None:
            value = self.local_measure_number_extra_offset
            assert isinstance(value, tuple)
            string = f"#'({value[0]} . {value[1]})"
            string = f"local-measure-number-extra-offset = {string}"
            literal = abjad.LilyPondLiteral(string)
            includes.append(literal)
        if self.measure_number_extra_offset is not None:
            value = self.measure_number_extra_offset
            assert isinstance(value, tuple)
            string = f"#'({value[0]} . {value[1]})"
            string = f"measure-number-extra-offset = {string}"
            literal = abjad.LilyPondLiteral(string)
            includes.append(literal)
        if self.spacing_extra_offset is not None:
            value = self.spacing_extra_offset
            assert isinstance(value, tuple)
            string = f"#'({value[0]} . {value[1]})"
            string = f"spacing-extra-offset = {string}"
            literal = abjad.LilyPondLiteral(string)
            includes.append(literal)
        if self.stage_number_extra_offset is not None:
            value = self.stage_number_extra_offset
            assert isinstance(value, tuple)
            string = f"#'({value[0]} . {value[1]})"
            string = f"stage-number-extra-offset = {string}"
            literal = abjad.LilyPondLiteral(string)
            includes.append(literal)
        includes.extend(self.includes or [])
        return includes

    def _get_measure_number_tag(self, leaf):
        start_offset = abjad.get.timespan(leaf).start_offset
        measure_number = self._offset_to_measure_number.get(start_offset)
        if measure_number is not None:
            return abjad.Tag(f"MEASURE_{measure_number}")

    def _get_measure_offsets(self, start_measure, stop_measure):
        skips = _selection.Selection(self.score["Global_Skips"]).skips()
        start_skip = skips[start_measure - 1]
        assert isinstance(start_skip, abjad.Skip), start_skip
        start_offset = abjad.get.timespan(start_skip).start_offset
        stop_skip = skips[stop_measure - 1]
        assert isinstance(stop_skip, abjad.Skip), stop_skip
        stop_offset = abjad.get.timespan(stop_skip).stop_offset
        return start_offset, stop_offset

    def _get_measure_time_signatures(self, start_measure=None, stop_measure=None):
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
        measure_indices = [_ - first_measure_number - 1 for _ in measure_numbers]
        skips = _selection.Selection(self.score["Global_Skips"]).skips()
        for i, skip in enumerate(skips):
            if i in measure_indices:
                timespan = abjad.get.timespan(skip)
                timespans.append(timespan)
        return timespans

    def _get_persistent_indicator(self, context, prototype):
        assert isinstance(context, abjad.Context), repr(context)
        if not self.previous_metadata:
            return
        dictionary = self.previous_persist.get("persistent_indicators")
        if not dictionary:
            return
        mementos = dictionary.get(context.name)
        if not mementos:
            return
        prototype_string = self._prototype_string(prototype)
        for memento in mementos:
            if memento.prototype == prototype_string:
                indicator = self._key_to_indicator(memento.value, prototype)
                return (indicator, memento.context)

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
        tag = getattr(_tags, name)
        return tag

    def _handle_mutator(self, command):
        if hasattr(command, "_mutates_score") and command._mutates_score():
            self._cache = None
            self._update_score_one_time()

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
            key = SegmentMaker._get_key(manifests["abjad.Instrument"], indicator)
        elif isinstance(indicator, abjad.MetronomeMark):
            key = SegmentMaker._get_key(manifests["abjad.MetronomeMark"], indicator)
        elif isinstance(indicator, abjad.MarginMarkup):
            key = SegmentMaker._get_key(manifests["abjad.MarginMarkup"], indicator)
        elif isinstance(indicator, _memento.PersistentOverride):
            key = indicator
        elif isinstance(indicator, indicators.BarExtent):
            key = indicator.line_count
        elif isinstance(indicator, indicators.StaffLines):
            key = indicator.line_count
        elif isinstance(indicator, (indicators.Accelerando, indicators.Ritardando)):
            key = {"hide": indicator.hide}
        else:
            key = str(indicator)
        return key

    def _initialize_time_signatures(self, time_signatures):
        time_signatures = time_signatures or ()
        time_signatures_ = list(time_signatures)
        time_signatures_ = []
        for time_signature in time_signatures:
            if isinstance(time_signature, str):
                time_signature = abjad.TimeSignature.from_string(time_signature)
            else:
                time_signature = abjad.TimeSignature(time_signature)
            time_signatures_.append(time_signature)
        time_signatures_ = tuple(time_signatures_)
        if not time_signatures_:
            time_signatures_ = None
        self._time_signatures = time_signatures_

    def _intercalate_silences(self, timespans, voice_name):
        selections = []
        durations = [_.duration for _ in self.time_signatures]
        measure_start_offsets = abjad.math.cumulative_sums(durations)
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
                selections.append(selection)
            selection = timespan.annotation
            assert isinstance(selection, abjad.Selection), repr(selection)
            selections.append(selection)
            duration = abjad.get.duration(selection)
            previous_stop_offset = start_offset + duration
        if previous_stop_offset < segment_duration:
            selection = self._make_measure_silences(
                previous_stop_offset,
                segment_duration,
                measure_start_offsets,
                voice_name,
            )
            assert isinstance(selection, abjad.Selection)
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
        skips = _selection.Selection(self.score["Global_Skips"]).skips()
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
            is_fermata = False
            if measure_number in self._fermata_measure_numbers:
                is_fermata = True
            skip = skips[measure_index]
            clock_time = clock_times[measure_index]
            clock_string = clock_time.to_clock_string()
            seconds = int(clock_time)
            fermata_string = f"{seconds}''"
            if measure_index < total - 1:
                tag = _tags.CLOCK_TIME
                if measure_index == total - 2:
                    if is_fermata and final_is_fermata:
                        string = r"- \baca-start-ct-both-fermata"
                        string += f' "{fermata_string}" "{final_fermata_string}"'
                    elif is_fermata and not final_is_fermata:
                        string = r"- \baca-start-ct-both-left-fermata"
                        string += f' "{fermata_string}" "[{final_clock_string}]"'
                    elif not is_fermata and final_is_fermata:
                        string = r"- \baca-start-ct-both-right-fermata"
                        string += f' "[{clock_string}]" "{final_fermata_string}"'
                    else:
                        string = r"- \baca-start-ct-both"
                        string += f' "[{clock_string}]" "[{final_clock_string}]"'
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
                    tag=tag.append(_site(inspect.currentframe())),
                )
            if 0 < measure_index:
                tag = _tags.CLOCK_TIME
                stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanCT")
                abjad.attach(
                    stop_text_span,
                    skip,
                    context="GlobalSkips",
                    deactivate=True,
                    tag=tag.append(_site(inspect.currentframe())),
                )

    def _label_duration_multipliers(self):
        tag = _site(inspect.currentframe())
        tag = tag.append(_tags.DURATION_MULTIPLIER)
        already_labeled = set()
        for voice in abjad.iterate(self.score).components(abjad.Voice):
            for leaf in abjad.iterate(voice).leaves():
                if isinstance(leaf, abjad.Skip):
                    continue
                if leaf.multiplier is None:
                    continue
                if leaf in already_labeled:
                    continue
                n, d = leaf.multiplier.pair
                string = r"\baca-duration-multiplier-markup"
                string += f' #"{n}" #"{d}"'
                markup = abjad.Markup(string, direction=abjad.Up, literal=True)
                tag_ = tag
                if abjad.get.has_indicator(leaf, const.HIDDEN):
                    tag_ = tag_.append(_tags.HIDDEN)
                if abjad.get.has_indicator(leaf, const.MULTIMEASURE_REST):
                    tag_ = tag_.append(_tags.MULTIMEASURE_REST)
                if abjad.get.has_indicator(leaf, const.NOTE):
                    tag_ = tag_.append(_tags.NOTE)
                if abjad.get.has_indicator(leaf, const.PHANTOM):
                    tag_ = tag_.append(_tags.PHANTOM)
                if abjad.get.has_indicator(leaf, const.REST_VOICE):
                    tag_ = tag_.append(_tags.REST_VOICE)
                abjad.attach(markup, leaf, deactivate=True, tag=tag_)
                already_labeled.add(leaf)

    def _label_measure_numbers(self):
        skips = _selection.Selection(self.score["Global_Skips"]).skips()
        total = len(skips)
        first_measure_number = self._get_first_measure_number()
        for measure_index, skip in enumerate(skips):
            local_measure_number = measure_index + 1
            measure_number = first_measure_number + measure_index
            if measure_index < total - 1:
                tag = _tags.LOCAL_MEASURE_NUMBER
                tag = tag.append(_site(inspect.currentframe()))
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
                tag = _tags.MEASURE_NUMBER
                tag = tag.append(_site(inspect.currentframe()))
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
                tag = _tags.LOCAL_MEASURE_NUMBER
                tag = tag.append(_site(inspect.currentframe()))
                stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanLMN")
                abjad.attach(
                    stop_text_span,
                    skip,
                    context="GlobalSkips",
                    deactivate=True,
                    tag=tag,
                )
                tag = _tags.MEASURE_NUMBER
                tag = tag.append(_site(inspect.currentframe()))
                stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanMN")
                abjad.attach(
                    stop_text_span,
                    skip,
                    context="GlobalSkips",
                    deactivate=True,
                    tag=tag,
                )

    def _label_moment_numbers(self):
        skips = _selection.Selection(self.score["Global_Skips"]).skips()
        if not self.moment_markup:
            return
        for i, item in enumerate(self.moment_markup):
            if len(item) == 2:
                value, lmn = item
                color = None
            elif len(item) == 3:
                value, lmn, color = item
            else:
                raise Exception(item)
            measure_index = lmn - 1
            skip = skips[measure_index]
            tag = _tags.MOMENT_NUMBER
            tag = tag.append(_site(inspect.currentframe()))
            if color is not None:
                string = r"- \baca-start-xnm-colored-left-only"
                string += f' "{value}" {color}'
            else:
                string = r"- \baca-start-xnm-left-only"
                string += f' "{value}"'
            start_text_span = abjad.StartTextSpan(
                command=r"\bacaStartTextSpanXNM", left_text=string
            )
            abjad.attach(
                start_text_span,
                skip,
                context="GlobalSkips",
                deactivate=True,
                tag=tag,
            )
            if 0 < i:
                tag = _tags.MOMENT_NUMBER
                tag = tag.append(_site(inspect.currentframe()))
                stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanXNM")
                abjad.attach(
                    stop_text_span,
                    skip,
                    context="GlobalSkips",
                    deactivate=True,
                    tag=tag,
                )
        skip = skips[-1]
        tag = _tags.MOMENT_NUMBER
        tag = tag.append(_site(inspect.currentframe()))
        stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanXNM")
        abjad.attach(
            stop_text_span,
            skip,
            context="GlobalSkips",
            deactivate=True,
            tag=tag,
        )

    def _label_stage_numbers(self):
        skips = _selection.Selection(self.score["Global_Skips"]).skips()
        if not self.stage_markup:
            return
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
            tag = _tags.STAGE_NUMBER
            tag = tag.append(_site(inspect.currentframe()))
            if color is not None:
                string = r"- \baca-start-snm-colored-left-only"
                string += f' "{value}" {color}'
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
                tag = _tags.STAGE_NUMBER
                tag = tag.append(_site(inspect.currentframe()))
                stop_text_span = abjad.StopTextSpan(command=r"\bacaStopTextSpanSNM")
                abjad.attach(
                    stop_text_span,
                    skip,
                    context="GlobalSkips",
                    deactivate=True,
                    tag=tag,
                )
        skip = skips[-1]
        tag = _tags.STAGE_NUMBER
        tag = tag.append(_site(inspect.currentframe()))
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
        tag = abjad.Tag(tag)
        tag = tag.append(_site(inspect.currentframe()))
        for staff in abjad.iterate(self.score).components(abjad.Staff):
            first_leaf = abjad.get.leaf(staff, 0)
            assert first_leaf is not None
            literal = abjad.LilyPondLiteral(string)
            abjad.attach(literal, first_leaf, tag=tag)

    def _make_global_context(self):
        global_rests = abjad.Context(lilypond_type="GlobalRests", name="Global_Rests")
        global_skips = abjad.Context(lilypond_type="GlobalSkips", name="Global_Skips")
        global_context = abjad.Context(
            [global_rests, global_skips],
            lilypond_type="GlobalContext",
            simultaneous=True,
            name="Global_Context",
        )
        return global_context

    def _make_global_rests(self):
        rests = []
        for time_signature in self.time_signatures:
            rest = abjad.MultimeasureRest(
                abjad.Duration(1),
                multiplier=time_signature.duration,
                tag=_site(inspect.currentframe(), 1),
            )
            rests.append(rest)
        if not self.remove_phantom_measure:
            tag = _site(inspect.currentframe(), 2).append(_tags.PHANTOM)
            rest = abjad.MultimeasureRest(abjad.Duration(1), multiplier=(1, 4), tag=tag)
            abjad.attach(const.PHANTOM, rest)
            rests.append(rest)
        return rests

    def _make_global_skips(self):
        context = self.score["Global_Skips"]
        for time_signature in self.time_signatures:
            skip = abjad.Skip(
                1,
                multiplier=time_signature.duration,
                tag=_site(inspect.currentframe(), 1),
            )
            abjad.attach(
                time_signature,
                skip,
                context="Score",
                tag=_site(inspect.currentframe(), 2),
            )
            context.append(skip)
        if not self.remove_phantom_measure:
            tag = _site(inspect.currentframe(), 3)
            tag = tag.append(_tags.PHANTOM)
            skip = abjad.Skip(1, multiplier=(1, 4), tag=tag)
            abjad.attach(const.PHANTOM, skip)
            context.append(skip)
            if time_signature != abjad.TimeSignature((1, 4)):
                time_signature = abjad.TimeSignature((1, 4))
                abjad.attach(time_signature, skip, context="Score", tag=tag)
        if self.first_segment:
            return
        # empty start bar allows LilyPond to print bar numbers
        # at start of nonfirst segments
        first_skip = _selection.Selection(context).skip(0)
        literal = abjad.LilyPondLiteral(r'\bar ""')
        tag = _tags.EMPTY_START_BAR
        tag = tag.append(_tags.ONLY_SEGMENT)
        abjad.attach(
            literal,
            first_skip,
            tag=tag.append(_site(inspect.currentframe(), 4)),
        )

    def _make_lilypond_file(self):
        tag = _site(inspect.currentframe())
        items = []
        includes = self._get_lilypond_includes()
        if not self.first_segment:
            lines = abjad.tag.double_tag(nonfirst_preamble.split("\n"), tag)
            line = "\n".join(lines)
            items.append(line)
        if self.preamble:
            string = "\n".join(self.preamble)
            items.append(string)
        block = abjad.Block(name="score")
        block.items.append(self.score)
        items.append(block)
        lilypond_file = abjad.LilyPondFile(
            items=items,
            date_time_token=False,
            includes=includes,
            tag=tag,
            use_relative_includes=False,
        )
        if self.environment != "docs" and not self.do_not_include_layout_ly:
            assert len(lilypond_file.score_block.items) == 1
            score = lilypond_file.score_block.items[0]
            assert isinstance(score, abjad.Score)
            include = abjad.Container(tag=tag)
            literal = abjad.LilyPondLiteral("", format_slot="absolute_before")
            abjad.attach(literal, include, tag=None)
            string = r'\include "layout.ly"'
            literal = abjad.LilyPondLiteral(string, format_slot="opening")
            abjad.attach(literal, include, tag=tag)
            container = abjad.Container([include, score], simultaneous=True, tag=tag)
            literal = abjad.LilyPondLiteral("", format_slot="absolute_before")
            abjad.attach(literal, container, tag=None)
            literal = abjad.LilyPondLiteral("", format_slot="closing")
            abjad.attach(literal, container, tag=None)
            lilypond_file.score_block.items[:] = [container]
            lilypond_file.score_block.items.append("")
        if self.midi:
            block = abjad.Block(name="midi")
            lilypond_file.score_block.items.append(block)
        self._lilypond_file = lilypond_file

    def _make_measure_silences(self, start, stop, measure_start_offsets, voice_name):
        tag = _site(inspect.currentframe())
        offsets = [start]
        for measure_start_offset in measure_start_offsets:
            if start < measure_start_offset < stop:
                offsets.append(measure_start_offset)
        offsets.append(stop)
        silences = []
        durations = abjad.math.difference_series(offsets)
        for i, duration in enumerate(durations):
            if i == 0:
                silence = self._make_multimeasure_rest_container(voice_name, duration)
            else:
                if self.skips_instead_of_rests:
                    silence = abjad.Skip(1, multiplier=duration, tag=tag)
                else:
                    silence = abjad.MultimeasureRest(1, multiplier=duration, tag=tag)
            silences.append(silence)
        assert all(isinstance(_, abjad.Component) for _ in silences)
        selection = abjad.select(silences)
        return selection

    def _make_multimeasure_rest_container(
        self, voice_name, duration, phantom=False, suppress_note=False
    ):
        if suppress_note is True:
            assert phantom is True
        if phantom is True:
            phantom_tag = _tags.PHANTOM
        else:
            phantom_tag = abjad.Tag()
        tag = _site(inspect.currentframe(), 1)
        tag = tag.append(phantom_tag)
        tag = tag.append(_tags.HIDDEN)
        if suppress_note is not True:
            note_or_rest = _tags.NOTE
            tag = tag.append(_tags.NOTE)
            note = abjad.Note("c'1", multiplier=duration, tag=tag)
            abjad.attach(const.NOTE, note)
            abjad.attach(const.NOT_YET_PITCHED, note)
        else:
            note_or_rest = _tags.MULTIMEASURE_REST
            tag = tag.append(_tags.MULTIMEASURE_REST)
            note = abjad.MultimeasureRest(1, multiplier=duration, tag=tag)
            abjad.attach(const.MULTIMEASURE_REST, note)
        abjad.attach(const.HIDDEN, note)
        tag = _site(inspect.currentframe(), 2)
        tag = tag.append(phantom_tag)
        tag = tag.append(note_or_rest)
        tag = tag.append(_tags.INVISIBLE_MUSIC_COLORING)
        literal = abjad.LilyPondLiteral(
            r"\abjad-invisible-music-coloring", format_slot="before"
        )
        abjad.attach(literal, note, tag=tag)
        tag = _site(inspect.currentframe(), 3)
        tag = tag.append(phantom_tag)
        tag = tag.append(note_or_rest)
        tag = tag.append(_tags.INVISIBLE_MUSIC_COMMAND)
        literal = abjad.LilyPondLiteral(r"\abjad-invisible-music", format_slot="before")
        abjad.attach(literal, note, deactivate=True, tag=tag)
        abjad.attach(const.HIDDEN, note)
        tag = _site(inspect.currentframe(), 4)
        tag = tag.append(phantom_tag)
        hidden_note_voice = abjad.Voice([note], name=voice_name, tag=tag)
        abjad.attach(const.INTERMITTENT, hidden_note_voice)
        tag = _site(inspect.currentframe(), 5)
        tag = tag.append(phantom_tag)
        tag = tag.append(_tags.REST_VOICE)
        if self.skips_instead_of_rests:
            tag = tag.append(_tags.SKIP)
            rest = abjad.Skip(1, multiplier=duration, tag=tag)
            abjad.attach(const.SKIP, rest)
        else:
            tag = tag.append(_tags.MULTIMEASURE_REST)
            rest = abjad.MultimeasureRest(1, multiplier=duration, tag=tag)
            abjad.attach(const.MULTIMEASURE_REST, rest)
        abjad.attach(const.REST_VOICE, rest)
        if "Music_Voice" in voice_name:
            name = voice_name.replace("Music_Voice", "Rest_Voice")
        else:
            name = voice_name.replace("Voice", "Rest_Voice")
        tag = _site(inspect.currentframe(), 6)
        tag = tag.append(phantom_tag)
        multimeasure_rest_voice = abjad.Voice([rest], name=name, tag=tag)
        abjad.attach(const.INTERMITTENT, multimeasure_rest_voice)
        tag = _site(inspect.currentframe(), 7)
        tag = tag.append(phantom_tag)
        container = abjad.Container(
            [hidden_note_voice, multimeasure_rest_voice],
            simultaneous=True,
            tag=tag,
        )
        abjad.attach(const.MULTIMEASURE_REST_CONTAINER, container)
        if phantom is True:
            for component in abjad.iterate(container).components():
                abjad.attach(const.PHANTOM, component)
        return container

    def _make_score(self):
        score = self.score_template()
        for lilypond_type, annotation, indicator in self.indicator_defaults or ():
            context = score[lilypond_type]
            abjad.annotate(context, annotation, indicator)
        self._score = score

    def _memento_to_indicator(self, memento):
        baca = importlib.import_module("baca")
        if memento.manifest is not None:
            dictionary = getattr(self, memento.manifest)
            if dictionary is None:
                raise Exception(f"can not find {memento.manifest!r} manifest.")
            return dictionary.get(memento.value)
        globals_ = globals()
        globals_["baca"] = baca
        class_ = eval(memento.prototype, globals_)
        if hasattr(class_, "from_string"):
            indicator = class_.from_string(memento.value)
        elif class_ is abjad.Dynamic and memento.value.startswith("\\"):
            indicator = class_(name="", command=memento.value)
        elif isinstance(memento.value, class_):
            indicator = memento.value
        elif class_ is indicators.StaffLines:
            indicator = class_(line_count=memento.value)
        elif memento.value is None:
            indicator = class_()
        elif isinstance(memento.value, dict):
            indicator = class_(**memento.value)
        else:
            try:
                indicator = class_(memento.value)
            except Exception:
                raise Exception(abjad.storage(memento))
        return indicator

    def _move_global_rests(self):
        topmost = "_global_rests_in_topmost_staff"
        every = "_global_rests_in_every_staff"
        if not getattr(self.score_template, topmost, None) and not getattr(
            self.score_template, every, None
        ):
            return
        if "Global_Rests" not in self.score:
            return
        global_rests = self.score["Global_Rests"]
        self.score["Global_Context"].remove(global_rests)
        music_context = self.score["Music_Context"]
        if getattr(self.score_template, topmost, None) is True:
            for staff in abjad.iterate(music_context).components(abjad.Staff):
                break
            staff.simultaneous = True
            staff.insert(0, global_rests)
            return
        if getattr(self.score_template, every, None) is True:
            topmost_staff = True
            tag = global_rests.tag or abjad.Tag()
            for staff in abjad.iterate(music_context).components(abjad.Staff):
                staff.simultaneous = True
                global_rests_ = copy.deepcopy(global_rests)
                if not topmost_staff:
                    global_rests_._tag = tag.append(abjad.Tag("NOT_TOPMOST"))
                staff.insert(0, global_rests_)
                topmost_staff = False

    def _populate_offset_to_measure_number(self):
        measure_number = self._get_first_measure_number()
        for skip in _selection.Selection(self.score["Global_Skips"]).skips():
            offset = abjad.get.timespan(skip).start_offset
            self._offset_to_measure_number[offset] = measure_number
            measure_number += 1

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

    def _reanalyze_reapplied_synthetic_wrappers(self):
        site = _site(inspect.currentframe())
        for leaf in abjad.iterate(self.score).leaves():
            for wrapper in abjad.get.wrappers(leaf):
                if wrapper.synthetic_offset is None:
                    continue
                if 0 <= wrapper.synthetic_offset:
                    continue
                if "REAPPLIED" in str(wrapper.tag):
                    string = str(wrapper.tag)
                    string = string.replace("REAPPLIED", "EXPLICIT")
                    tag_ = abjad.Tag(string).append(site)
                    wrapper._tag = tag_
                    wrapper._synthetic_offset = None

    def _reanalyze_trending_dynamics(self):
        for leaf in abjad.iterate(self.score).leaves():
            for wrapper in abjad.get.wrappers(leaf):
                if isinstance(
                    wrapper.indicator, abjad.Dynamic
                ) and abjad.get.indicators(leaf, abjad.StartHairpin):
                    self._treat_persistent_wrapper(self.manifests, wrapper, "explicit")

    def _reapply_persistent_indicators(self):
        if self.first_segment:
            return
        dictionary = self.previous_persist.get("persistent_indicators")
        if not dictionary:
            return
        for context in abjad.iterate(self.score).components(abjad.Context):
            mementos = dictionary.get(context.name)
            if not mementos:
                continue
            for memento in mementos:
                result = self._analyze_memento(context, memento)
                if result is None:
                    continue
                (
                    leaf,
                    previous_indicator,
                    status,
                    edition,
                    synthetic_offset,
                ) = result
                if isinstance(previous_indicator, abjad.TimeSignature):
                    if status in (None, "explicit"):
                        continue
                    assert status == "reapplied", repr(status)
                    wrapper = abjad.get.wrapper(leaf, abjad.TimeSignature)
                    site = _site(inspect.currentframe(), 1)
                    edition = edition.append(site)
                    wrapper.tag = wrapper.tag.append(edition)
                    self._treat_persistent_wrapper(self.manifests, wrapper, status)
                    continue
                # TODO: change to parameter comparison
                prototype = (
                    indicators.Accelerando,
                    abjad.MetronomeMark,
                    indicators.Ritardando,
                )
                if isinstance(previous_indicator, prototype):
                    site = _site(inspect.currentframe(), 2)
                    if status == "reapplied":
                        wrapper = abjad.attach(
                            previous_indicator,
                            leaf,
                            synthetic_offset=synthetic_offset,
                            tag=edition.append(site),
                            wrapper=True,
                        )
                        self._treat_persistent_wrapper(self.manifests, wrapper, status)
                    else:
                        assert status in ("redundant", None), repr(status)
                        if status is None:
                            status = "explicit"
                        wrappers = abjad.get.wrappers(leaf, prototype)
                        # lone metronome mark or lone tempo trend:
                        if len(wrappers) == 1:
                            wrapper = wrappers[0]
                        # metronome mark + tempo trend:
                        else:
                            assert 1 < len(wrappers), repr(wrappers)
                            prototype = abjad.MetronomeMark
                            wrapper = abjad.get.wrapper(leaf, prototype)
                        wrapper.tag = wrapper.tag.append(edition)
                        self._treat_persistent_wrapper(self.manifests, wrapper, status)
                    continue
                attached = False
                site = _site(inspect.currentframe(), 3)
                tag = edition.append(site)
                if isinstance(previous_indicator, abjad.MarginMarkup):
                    tag = tag.append(_tags.NOT_PARTS)
                try:
                    wrapper = abjad.attach(
                        previous_indicator,
                        leaf,
                        synthetic_offset=synthetic_offset,
                        tag=tag,
                        wrapper=True,
                    )
                    attached = True
                except abjad.PersistentIndicatorError:
                    pass
                if attached:
                    self._treat_persistent_wrapper(self.manifests, wrapper, status)

    def _remove_redundant_time_signatures(self):
        previous_time_signature = None
        self._cached_time_signatures = []
        skips = _selection.Selection(self.score["Global_Skips"]).skips()
        if not self.remove_phantom_measure:
            skips = skips[:-1]
        for skip in skips:
            time_signature = abjad.get.indicator(skip, abjad.TimeSignature)
            self._cached_time_signatures.append(str(time_signature))
            if time_signature == previous_time_signature:
                abjad.detach(time_signature, skip)
            else:
                previous_time_signature = time_signature

    def _remove_docs_tags(self):
        tags = self.remove or []
        if self.environment == "docs":
            tags += _tags.documentation_removal_tags()
        assert all(isinstance(_, abjad.Tag) for _ in tags), repr(tags)
        for leaf in abjad.iterate(self.score).leaves():
            for wrapper in abjad.get.wrappers(leaf):
                if wrapper.tag is None:
                    continue
                for word in wrapper.tag:
                    if abjad.Tag(word) in tags:
                        abjad.detach(wrapper, leaf)
                        break

    def _scope_to_leaf_selection(self, command):
        leaves = []
        selections = self._scope_to_leaf_selections(command.scope)
        for selection in selections:
            leaves.extend(selection)
        selection = abjad.select(leaves)
        if not selection:
            message = f"EMPTY SELECTION:\n\n{abjad.storage(command)}"
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

    def _set_not_yet_pitched_to_staff_position_zero(self):
        indicator = const.NOT_YET_PITCHED
        pleaves = []
        for pleaf in abjad.iterate(self.score).leaves(pitched=True):
            if not abjad.get.has_indicator(pleaf, indicator):
                continue
            pleaves.append(pleaf)
        command = pitchcommands.staff_position(
            0,
            lambda _: _selection.Selection(_).plts(),
            set_chord_pitches_equal=True,
        )
        command(pleaves)

    def _set_status_tag(wrapper, status, redraw=None, stem=None):
        assert isinstance(wrapper, abjad.Wrapper), repr(wrapper)
        stem = stem or scoping.Command._to_indicator_stem(wrapper.indicator)
        prefix = None
        if redraw is True:
            prefix = "redrawn"
        tag = wrapper.tag.append(_site(inspect.currentframe()))
        status_tag = SegmentMaker._get_tag(status, stem, prefix=prefix)
        tag = tag.append(status_tag)
        wrapper.tag = tag

    def _shift_measure_initial_clefs(self):
        if self.environment == "docs":
            return
        for staff in abjad.iterate(self.score).components(abjad.Staff):
            for leaf in abjad.iterate(staff).leaves():
                start_offset = abjad.get.timespan(leaf).start_offset
                wrapper = abjad.get.wrapper(leaf, abjad.Clef)
                if wrapper is None or not wrapper.tag:
                    continue
                if _tags.EXPLICIT_CLEF not in wrapper.tag:
                    continue
                measure_number = self._offset_to_measure_number.get(start_offset)
                if measure_number is None:
                    continue
                clef = wrapper.indicator
                suite = _overrides.clef_shift(
                    clef, selector=lambda _: _selection.Selection(_).leaf(0)
                )
                runtime = self._bundle_manifests()
                suite(leaf, runtime=runtime)

    def _style_fermata_measures(self):
        if not self.fermata_measure_empty_overrides:
            return
        if not self._fermata_start_offsets:
            return
        bar_lines_already_styled = []
        empty_fermata_measure_start_offsets = []
        for measure_number in self.fermata_measure_empty_overrides or []:
            timespan = self._get_measure_timespan(measure_number)
            empty_fermata_measure_start_offsets.append(timespan.start_offset)
        for staff in abjad.iterate(self.score).components(abjad.Staff):
            for leaf in abjad.iterate(staff).leaves():
                if abjad.get.has_indicator(leaf, const.PHANTOM):
                    continue
                start_offset = abjad.get.timespan(leaf).start_offset
                if start_offset not in self._fermata_start_offsets:
                    continue
                voice = abjad.get.parentage(leaf).get(abjad.Voice)
                if "Rest_Voice" in voice.name:
                    continue
                if start_offset not in empty_fermata_measure_start_offsets:
                    continue
                empty_staff_lines = indicators.StaffLines(0)
                empty_bar_extent = indicators.BarExtent(0)
                previous_staff_lines = abjad.get.effective(leaf, indicators.StaffLines)
                previous_bar_extent = abjad.get.effective(leaf, indicators.BarExtent)
                next_leaf = abjad.get.leaf(leaf, 1)
                if abjad.get.has_indicator(next_leaf, const.PHANTOM):
                    next_leaf = None
                next_staff_lines = None
                if next_leaf is not None:
                    next_staff_lines = abjad.get.effective(
                        next_leaf, indicators.StaffLines
                    )
                    next_bar_extent = abjad.get.effective(
                        next_leaf, indicators.BarExtent
                    )
                if (
                    previous_staff_lines != empty_staff_lines
                ) and not abjad.get.has_indicator(leaf, indicators.StaffLines):
                    abjad.attach(
                        empty_staff_lines,
                        leaf,
                        tag=_site(inspect.currentframe(), 1),
                    )
                    if not self.final_segment:
                        abjad.attach(
                            empty_bar_extent,
                            leaf,
                            tag=_site(inspect.currentframe(), 2).append(
                                abjad.Tag("FERMATA_MEASURE_EMPTY_BAR_EXTENT")
                            ),
                        )
                if next_leaf is not None and empty_staff_lines != next_staff_lines:
                    if next_staff_lines is None:
                        next_staff_lines_ = indicators.StaffLines(5)
                    else:
                        next_staff_lines_ = next_staff_lines
                    if next_bar_extent is None:
                        next_bar_extent_ = indicators.StaffLines(5)
                    else:
                        next_bar_extent_ = next_bar_extent
                    wrapper = abjad.get.effective_wrapper(
                        next_leaf, indicators.StaffLines
                    )
                    next_leaf_start_offset = abjad.get.timespan(next_leaf).start_offset
                    if wrapper is None or (
                        wrapper.start_offset != next_leaf_start_offset
                    ):
                        abjad.attach(
                            next_staff_lines_,
                            next_leaf,
                            tag=_site(inspect.currentframe(), 3),
                        )
                        abjad.attach(
                            next_bar_extent_,
                            next_leaf,
                            tag=_site(inspect.currentframe(), 4).append(
                                abjad.Tag("FERMATA_MEASURE_NEXT_BAR_EXTENT")
                            ),
                        )
                if next_leaf is None and previous_staff_lines != empty_staff_lines:
                    previous_line_count = 5
                    if previous_staff_lines is not None:
                        previous_line_count = previous_staff_lines.line_count
                    resume_staff_lines = indicators.StaffLines(
                        previous_line_count, hide=True
                    )
                    abjad.attach(
                        resume_staff_lines,
                        leaf,
                        synthetic_offset=99,
                        tag=_site(inspect.currentframe(), 5),
                    )
                    previous_line_count = 5
                    if previous_bar_extent is not None:
                        previous_line_count = previous_bar_extent.line_count
                    resume_bar_extent = indicators.BarExtent(
                        previous_line_count, hide=True
                    )
                    abjad.attach(
                        resume_bar_extent,
                        leaf,
                        synthetic_offset=99,
                        tag=_site(inspect.currentframe(), 6).append(
                            abjad.Tag("FERMATA_MEASURE_RESUME_BAR_EXTENT")
                        ),
                    )
                if start_offset in bar_lines_already_styled:
                    continue
                if not (next_leaf is None and self.final_segment):
                    # TODO: replace literal with override
                    strings = []
                    string = r"Score.BarLine.transparent = ##t"
                    string = r"\once \override " + string
                    strings.append(string)
                    string = r"Score.SpanBar.transparent = ##t"
                    string = r"\once \override " + string
                    strings.append(string)
                    literal = abjad.LilyPondLiteral(strings)
                    tag = _tags.FERMATA_MEASURE
                    measure_number_tag = self._get_measure_number_tag(leaf)
                    if measure_number_tag is not None:
                        tag = tag.append(measure_number_tag)
                    next_leaf_ = abjad.get.leaf(leaf, 1)
                    assert next_leaf_ is not None, repr(next_leaf_)
                    abjad.attach(
                        literal,
                        next_leaf_,
                        tag=tag.append(_site(inspect.currentframe(), 7)),
                    )
                bar_lines_already_styled.append(start_offset)
        rests = _selection.Selection(self.score["Global_Rests"]).leaves(
            abjad.MultimeasureRest
        )
        for measure_number in self.fermata_measure_empty_overrides:
            measure_index = measure_number - 1
            rest = rests[measure_index]
            grob = abjad.override(rest).multi_measure_rest_text
            grob.extra_offset = (0, self.fermata_extra_offset_y)

    def _style_phantom_measures(self):
        if self.remove_phantom_measure:
            return
        skip = abjad.get.leaf(self.score["Global_Skips"], -1)
        for literal in abjad.get.indicators(skip, abjad.LilyPondLiteral):
            if r"\baca-time-signature-color" in literal.argument:
                abjad.detach(literal, skip)
        self._append_tag_to_wrappers(
            skip, _site(inspect.currentframe(), 1).append(_tags.PHANTOM)
        )
        string = r"\baca-time-signature-transparent"
        literal = abjad.LilyPondLiteral(string)
        abjad.attach(
            literal,
            skip,
            tag=_site(inspect.currentframe(), 2).append(_tags.PHANTOM),
        )
        strings = [
            r"\once \override Score.BarLine.transparent = ##t",
            r"\once \override Score.SpanBar.transparent = ##t",
        ]
        literal = abjad.LilyPondLiteral(strings, format_slot="after")
        abjad.attach(
            literal,
            skip,
            tag=_site(inspect.currentframe(), 3).append(_tags.PHANTOM),
        )
        if "Global_Rests" in self.score:
            for context in abjad.iterate(self.score).components(abjad.Context):
                if context.name == "Global_Rests":
                    rest = context[-1]
                    break
            self._append_tag_to_wrappers(
                rest,
                _site(inspect.currentframe(), 4).append(_tags.PHANTOM),
            )
        start_offset = abjad.get.timespan(skip).start_offset
        enumeration = const.MULTIMEASURE_REST_CONTAINER
        containers = []
        for container in abjad.select(self.score).components(abjad.Container):
            if not abjad.get.has_indicator(container, enumeration):
                continue
            leaf = abjad.get.leaf(container, 0)
            if abjad.get.timespan(leaf).start_offset != start_offset:
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
                self._append_tag_to_wrappers(
                    leaf,
                    _site(inspect.currentframe(), 5).append(_tags.PHANTOM),
                )
                if not isinstance(leaf, abjad.MultimeasureRest):
                    continue
                if abjad.get.has_indicator(leaf, const.HIDDEN):
                    continue
                literal = abjad.LilyPondLiteral(string_1)
                abjad.attach(
                    literal,
                    leaf,
                    tag=_site(inspect.currentframe(), 6).append(_tags.PHANTOM),
                )
                literal = abjad.LilyPondLiteral(string_2)
                abjad.attach(
                    literal,
                    leaf,
                    tag=_site(inspect.currentframe(), 7).append(_tags.PHANTOM),
                )
                literal = abjad.LilyPondLiteral(strings)
                abjad.attach(
                    literal,
                    leaf,
                    tag=_site(inspect.currentframe(), 8).append(_tags.PHANTOM),
                )

    def _transpose_score_(self):
        if not self.transpose_score:
            return
        for pleaf in _selection.Selection(self.score).pleaves():
            if abjad.get.has_indicator(pleaf, const.DO_NOT_TRANSPOSE):
                continue
            if abjad.get.has_indicator(pleaf, const.STAFF_POSITION):
                continue
            abjad.iterpitches.transpose_from_sounding_pitch(pleaf)

    @staticmethod
    def _treat_persistent_wrapper(manifests, wrapper, status):
        assert isinstance(wrapper, abjad.Wrapper), repr(wrapper)
        assert bool(wrapper.indicator.persistent), repr(wrapper)
        assert isinstance(status, str), repr(status)
        indicator = wrapper.indicator
        prototype = (
            abjad.Glissando,
            abjad.Ottava,
            abjad.RepeatTie,
            abjad.StartBeam,
            abjad.StartPhrasingSlur,
            abjad.StartPianoPedal,
            abjad.StartSlur,
            abjad.StartTextSpan,
            abjad.StartTrillSpan,
            abjad.StopBeam,
            abjad.StopPhrasingSlur,
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
        if isinstance(indicator, abjad.MetronomeMark) and abjad.get.has_indicator(
            leaf, tempo_trend
        ):
            status = "explicit"
        if isinstance(wrapper.indicator, abjad.Dynamic) and abjad.get.indicators(
            leaf, abjad.StartHairpin
        ):
            status = "explicit"
        if isinstance(wrapper.indicator, (abjad.Dynamic, abjad.StartHairpin)):
            color = SegmentMaker._status_to_color[status]
            words = [
                f"{status.upper()}_DYNAMIC_COLOR",
                "_treat_persistent_wrapper(1)",
            ]
            words.extend(existing_tag.editions())
            words = [str(_) for _ in words]
            string = ":".join(words)
            tag_ = abjad.Tag(string)
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
                tag=wrapper.tag.append(_site(inspect.currentframe(), 2)),
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
            literal = abjad.LilyPondLiteral(strings, format_slot="after")
            stem = scoping.Command._to_indicator_stem(indicator)
            wrapper_ = abjad.attach(
                literal,
                leaf,
                tag=existing_tag.append(_site(inspect.currentframe(), 3)),
                wrapper=True,
            )
            SegmentMaker._set_status_tag(wrapper_, status, redraw=True, stem=stem)

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
            for wrapper in abjad.get.wrappers(leaf):
                if not getattr(wrapper.indicator, "persistent", False):
                    continue
                if wrapper.tag and _tags.has_persistence_tag(wrapper.tag):
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
                previous_indicator = abjad.get.effective(leaf, prototype, n=-1)
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
                assert len(measure_token) == 2
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
        measure_tokens = []
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
                scope = scoping.Scope(measures=measure_token, voice_name=voice_name)
                scopes_.append(scope)
        prototype = (scoping.Scope, scoping.TimelineScope)
        assert all(isinstance(_, prototype) for _ in scopes_)
        return scopes_

    def _unpack_scopes(self, scopes, abbreviations):
        scope_type = (scoping.Scope, scoping.TimelineScope)
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
                    scope_ = scoping.Scope(measures=measures, voice_name=voice_name)
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

    def _voice_to_rhythm_commands(self, voice):
        commands = []
        for command in self.commands:
            if not isinstance(command, rhythmcommands.RhythmCommand):
                continue
            if command.scope.voice_name == voice.name:
                commands.append(command)
        return commands

    def _whitespace_leaves(self):
        if self.environment == "docs":
            return
        for leaf in abjad.iterate(self.score).leaves():
            literal = abjad.LilyPondLiteral("", format_slot="absolute_before")
            abjad.attach(literal, leaf, tag=None)
        for container in abjad.iterate(self.score).components(abjad.Container):
            if hasattr(container, "_main_leaf"):
                literal = abjad.LilyPondLiteral("", format_slot="absolute_after")
                abjad.attach(literal, container, tag=None)
            else:
                literal = abjad.LilyPondLiteral("", format_slot="absolute_before")
                abjad.attach(literal, container, tag=None)
            literal = abjad.LilyPondLiteral("", format_slot="closing")
            abjad.attach(literal, container, tag=None)

    ### PUBLIC PROPERTIES ###

    @property
    def activate(self):
        """
        Gets tags to activate in LilyPond output.
        """
        return self._activate

    @property
    def allow_empty_selections(self):
        """
        Is true when segment allows empty selectors.

        Otherwise segment raises exception on empty selectors.
        """
        return self._allow_empty_selections

    @property
    def check_all_are_pitched(self):
        """
        Is true when segment-maker checks for NOT_YET_PITCHED indicators.
        """
        return self._check_all_are_pitched

    @property
    def clock_time_extra_offset(self):
        """
        Gets clock time extra offset.
        """
        return self._clock_time_extra_offset

    @property
    def clock_time_override(self):
        """
        Gets clock time override.
        """
        return self._clock_time_override

    @property
    def color_octaves(self):
        r"""
        Is true when segment-maker colors octaves.

        ..  container:: example

            Colors octaves:

            >>> def closure():
            ...     return baca.make_empty_score(1, 1)

            >>> maker = baca.SegmentMaker(
            ...     color_octaves=True,
            ...     includes=["baca.ily"],
            ...     preamble=[baca.global_context_string()],
            ...     score_template=closure,
            ...     time_signatures=[(6, 4)],
            ... )

            >>> maker(
            ...     ("Music_Voice_1", 1),
            ...     baca.music(abjad.Container("d'4 e' f' g' a' b'")[:]),
            ... )

            >>> maker(
            ...     ("Music_Voice_2", 1),
            ...     baca.music(abjad.Container("a4 g f e d c")[:]),
            ...     baca.clef("bass"),
            ... )

            >>> lilypond_file = maker.run(environment="docs")
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context GlobalContext = "Global_Context"
                    <<
                        \context GlobalSkips = "Global_Skips"
                        {
                            \time 6/4
                            \baca-time-signature-color #'blue
                            s1 * 3/2
                            \time 1/4
                            \baca-time-signature-transparent
                            s1 * 1/4
                            \once \override Score.BarLine.transparent = ##t
                            \once \override Score.SpanBar.transparent = ##t
                        }
                    >>
                    \context MusicContext = "Music_Context"
                    <<
                        \context StaffGroup = "Music_Staff_Group"
                        <<
                            \context Staff = "Music_Staff_1"
                            {
                                \context Voice = "Music_Voice_1"
                                {
                                    d'4
                                    - \abjad-dashed-line-with-hook
                                    - \baca-text-spanner-left-text "baca.music()"
                                    - \tweak bound-details.right.padding 2.75
                                    - \tweak color #darkcyan
                                    - \tweak staff-padding 8
                                    \bacaStartTextSpanRhythmAnnotation
                                    e'4
                                    \baca-octave-coloring
                                    f'4
                                    - \tweak color #red
                                    ^ \markup { OCTAVE }
                                    g'4
                                    a'4
                                    b'4
                                    <> \bacaStopTextSpanRhythmAnnotation
                                    <<
                                        \context Voice = "Music_Voice_1"
                                        {
                                            \abjad-invisible-music-coloring
                                            %@% \abjad-invisible-music
                                            \baca-not-yet-pitched-coloring
                                            b'1 * 1/4
                                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                        }
                                        \context Voice = "Rest_Voice_1"
                                        {
                                            \once \override Score.TimeSignature.X-extent = ##f
                                            \once \override MultiMeasureRest.transparent = ##t
                                            \stopStaff
                                            \once \override Staff.StaffSymbol.transparent = ##t
                                            \startStaff
                                            R1 * 1/4
                                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                        }
                                    >>
                                }
                            }
                            \context Staff = "Music_Staff_2"
                            {
                                \context Voice = "Music_Voice_2"
                                {
                                    \clef "bass"
                                    \once \override Staff.Clef.color = #(x11-color 'blue)
                                    %@% \override Staff.Clef.color = ##f
                                    \set Staff.forceClef = ##t
                                    a4
                                    - \abjad-dashed-line-with-hook
                                    - \baca-text-spanner-left-text "baca.music()"
                                    - \tweak bound-details.right.padding 2.75
                                    - \tweak color #darkcyan
                                    - \tweak staff-padding 8
                                    \bacaStartTextSpanRhythmAnnotation
                                    \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)
                                    g4
                                    \baca-octave-coloring
                                    f4
                                    - \tweak color #red
                                    ^ \markup { OCTAVE }
                                    e4
                                    d4
                                    c4
                                    <> \bacaStopTextSpanRhythmAnnotation
                                    <<
                                        \context Voice = "Music_Voice_2"
                                        {
                                            \abjad-invisible-music-coloring
                                            %@% \abjad-invisible-music
                                            \baca-not-yet-pitched-coloring
                                            d1 * 1/4
                                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                        }
                                        \context Voice = "Rest_Voice_2"
                                        {
                                            \once \override Score.TimeSignature.X-extent = ##f
                                            \once \override MultiMeasureRest.transparent = ##t
                                            \stopStaff
                                            \once \override Staff.StaffSymbol.transparent = ##t
                                            \startStaff
                                            R1 * 1/4
                                            %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                        }
                                    >>
                                }
                            }
                        >>
                    >>
                >>

        """
        return self._color_octaves

    @property
    def commands(self):
        """
        Gets commands.
        """
        return self._commands

    @property
    def deactivate(self):
        """
        Gets tags to deactivate in LilyPond output.
        """
        return self._deactivate

    @property
    def do_not_check_beamed_long_notes(self):
        """
        Is true when segment does not check beamed long notes.
        """
        return self._do_not_check_beamed_long_notes

    @property
    def do_not_check_out_of_range_pitches(self):
        """
        Is true when segment does not check out-of-range pitches.
        """
        return self._do_not_check_out_of_range_pitches

    @property
    def do_not_check_persistence(self):
        """
        Is true when segment-maker does not check persistent indicators.
        """
        return self._do_not_check_persistence

    @property
    def do_not_check_wellformedness(self):
        """
        Is true when segment does not check wellformedness.
        """
        return self._do_not_check_wellformedness

    @property
    def do_not_force_nonnatural_accidentals(self):
        """
        Is true when segment-maker does not force nonnatural accidentals.
        """
        return self._do_not_force_nonnatural_accidentals

    @property
    def do_not_include_layout_ly(self):
        """
        Is true when segment-maker does not include layout.ly.
        """
        return self._do_not_include_layout_ly

    @property
    def environment(self):
        """
        Gets environment.
        """
        return self._environment

    @property
    def fermata_extra_offset_y(self):
        """
        Gets fermata extra offset y.
        """
        return self._fermata_extra_offset_y

    @property
    def fermata_measure_empty_overrides(self):
        """
        Gets fermata measure empty overrides.
        """
        return self._fermata_measure_empty_overrides

    @property
    def final_segment(self):
        """
        Is true when composer declares segment to be last in score.
        """
        return self._final_segment

    @property
    def first_measure_number(self):
        """
        Gets user-defined first measure number.
        """
        return self._first_measure_number

    @property
    def first_segment(self):
        """
        Is true when segment is first in score.
        """
        return self._first_segment

    @property
    def indicator_defaults(self):
        """
        Gets indicator defaults for persistence tests.
        """
        return self._indicator_defaults

    @property
    def ignore_repeat_pitch_classes(self):
        """
        Is true when segment ignores repeat pitch-classes.
        """
        return self._ignore_repeat_pitch_classes

    @property
    def includes(self):
        """
        Gets includes.
        """
        return self._includes

    @property
    def instruments(self):
        """
        Gets instruments.
        """
        return self._instruments

    @property
    def lilypond_file(self):
        """
        Gets LilyPond file.
        """
        return self._lilypond_file

    @property
    def local_measure_number_extra_offset(self):
        """
        Gets local measure number extra offset.
        """
        return self._local_measure_number_extra_offset

    @property
    def magnify_staves(self):
        """
        Gets staff magnification.
        """
        return self._magnify_staves

    @property
    def manifests(self):
        """
        Gets manifests.
        """
        manifests = abjad.OrderedDict()
        manifests["abjad.Instrument"] = self.instruments
        manifests["abjad.MarginMarkup"] = self.margin_markups
        manifests["abjad.MetronomeMark"] = self.metronome_marks
        return manifests

    @property
    def margin_markups(self):
        """
        Gets margin markups.
        """
        return self._margin_markups

    @property
    def measure_count(self):
        """
        Gets measure count.
        """
        if self.time_signatures:
            return len(self.time_signatures)
        return 0

    @property
    def measure_number_extra_offset(self):
        """
        Gets measure number extra offset.
        """
        return self._measure_number_extra_offset

    @property
    def metadata(self):
        r"""
        Gets segment metadata.

        ..  container:: example

            >>> metadata = abjad.OrderedDict()
            >>> persist = abjad.OrderedDict()
            >>> persist["persistent_indicators"] = abjad.OrderedDict()
            >>> persist["persistent_indicators"]["MusicStaff"] = [
            ...     baca.Memento(
            ...         context="Music_Voice",
            ...         prototype="abjad.Clef",
            ...         value="alto",
            ...     )
            ... ]
            >>> maker = baca.SegmentMaker(
            ...     includes=["baca.ily"],
            ...     preamble=[baca.global_context_string()],
            ...     score_template=baca.make_empty_score_maker(1),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ... )

            >>> lilypond_file = maker.run(
            ...     environment="docs",
            ...     first_segment=False,
            ...     previous_metadata=metadata,
            ...     previous_persist=persist,
            ... )

            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context GlobalContext = "Global_Context"
                    <<
                        \context GlobalSkips = "Global_Skips"
                        {
                            \time 4/8
                            \bar ""
                            \baca-time-signature-color #'blue
                            s1 * 1/2
                            \time 3/8
                            \baca-time-signature-color #'blue
                            s1 * 3/8
                            \time 4/8
                            \baca-time-signature-color #'blue
                            s1 * 1/2
                            \time 3/8
                            \baca-time-signature-color #'blue
                            s1 * 3/8
                            \time 1/4
                            \baca-time-signature-transparent
                            s1 * 1/4
                            \once \override Score.BarLine.transparent = ##t
                            \once \override Score.SpanBar.transparent = ##t
                        }
                    >>
                    \context MusicContext = "Music_Context"
                    {
                        \context Staff = "Music_Staff"
                        {
                            \context Voice = "Music_Voice"
                            {
                                R1 * 4/8
                                %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                                R1 * 3/8
                                %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                                R1 * 4/8
                                %@% ^ \baca-duration-multiplier-markup #"4" #"8"
                                R1 * 3/8
                                %@% ^ \baca-duration-multiplier-markup #"3" #"8"
                                <<
                                    \context Voice = "Music_Voice"
                                    {
                                        \abjad-invisible-music-coloring
                                        %@% \abjad-invisible-music
                                        R1 * 1/4
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                    }
                                    \context Voice = "Rest_Voice"
                                    {
                                        \once \override Score.TimeSignature.X-extent = ##f
                                        \once \override MultiMeasureRest.transparent = ##t
                                        \stopStaff
                                        \once \override Staff.StaffSymbol.transparent = ##t
                                        \startStaff
                                        R1 * 1/4
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                    }
                                >>
                            }
                        }
                    }
                >>

            >>> string = abjad.storage(maker.metadata)
            >>> print(string)
            abjad.OrderedDict(
                [
                    ('final_measure_number', 4),
                    ('first_measure_number', 1),
                    (
                        'time_signatures',
                        ['4/8', '3/8', '4/8', '3/8'],
                        ),
                    ]
                )

            >>> string = abjad.storage(maker.persist)
            >>> print(string)
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
                                        baca.Memento(
                                            context='Music_Voice',
                                            prototype='abjad.Clef',
                                            value='alto',
                                            ),
                                        ],
                                    ),
                                (
                                    'Score',
                                    [
                                        baca.Memento(
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
    def metronome_marks(self):
        """
        Gets metronome marks.
        """
        return self._metronome_marks

    @property
    def midi(self):
        """
        Is true when segment-maker outputs MIDI.
        """
        return self._midi

    @property
    def moment_markup(self):
        """
        Gets moment markup.
        """
        return self._moment_markup

    @property
    def parts_metric_modulation_multiplier(self):
        """
        Gets parts metric modulation multiplier.
        """
        return self._parts_metric_modulation_multiplier

    @property
    def persist(self):
        """
        Gets persist metadata.
        """
        return self._persist

    @property
    def preamble(self):
        """
        Gets preamble strings.
        """
        return self._preamble

    @property
    def previous_metadata(self):
        """
        Gets previous segment metadata.
        """
        return self._previous_metadata

    @property
    def previous_persist(self):
        """
        Gets previous segment persist.
        """
        return self._previous_persist

    @property
    def remove(self):
        """
        Gets tags to remove
        """
        return self._remove

    @property
    def remove_phantom_measure(self):
        """
        Is true when segment-maker removes phantom measure.
        """
        return self._remove_phantom_measure

    @property
    def score(self):
        """
        Gets score.
        """
        return self._score

    @property
    def score_template(self):
        """
        Gets score template.
        """
        return self._score_template

    @property
    def segment_number(self):
        """
        Gets segment number.
        """
        return self._segment_number

    @property
    def skips_instead_of_rests(self):
        """
        Is true when segment fills empty measures with skips instead of rests.
        """
        return self._skips_instead_of_rests

    @property
    def spacing(self):
        """
        Gets spacing.
        """
        return self._spacing

    @property
    def spacing_extra_offset(self):
        """
        Gets spacing extra offset.
        """
        return self._spacing_extra_offset

    @property
    def stage_markup(self):
        """
        Gets stage markup.
        """
        return self._stage_markup

    @property
    def stage_number_extra_offset(self):
        """
        Gets stage number extra offset.
        """
        return self._stage_number_extra_offset

    @property
    def test_container_identifiers(self):
        """
        Is true when segment-maker adds container identifiers in docs
        environment.
        """
        return self._test_container_identifiers

    @property
    def time_signatures(self):
        """
        Gets time signatures.
        """
        return self._time_signatures

    @property
    def transpose_score(self):
        r"""
        Is true when segment transposes score.

        ..  container:: example

            Transposes score:

            >>> instruments = abjad.OrderedDict()
            >>> instruments["clarinet"] = abjad.ClarinetInBFlat()
            >>> maker = baca.SegmentMaker(
            ...     includes=["baca.ily"],
            ...     preamble=[baca.global_context_string()],
            ...     instruments=instruments,
            ...     score_template=baca.make_empty_score_maker(1),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     transpose_score=True,
            ... )

            >>> maker(
            ...     "Music_Voice",
            ...     baca.instrument(instruments["clarinet"]),
            ...     baca.make_even_divisions(),
            ...     baca.pitches("E4 F4"),
            ... )

            >>> lilypond_file = maker.run(environment="docs")
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context GlobalContext = "Global_Context"
                    <<
                        \context GlobalSkips = "Global_Skips"
                        {
                            \time 4/8
                            \baca-time-signature-color #'blue
                            s1 * 1/2
                            \time 3/8
                            \baca-time-signature-color #'blue
                            s1 * 3/8
                            \time 4/8
                            \baca-time-signature-color #'blue
                            s1 * 1/2
                            \time 3/8
                            \baca-time-signature-color #'blue
                            s1 * 3/8
                            \time 1/4
                            \baca-time-signature-transparent
                            s1 * 1/4
                            \once \override Score.BarLine.transparent = ##t
                            \once \override Score.SpanBar.transparent = ##t
                        }
                    >>
                    \context MusicContext = "Music_Context"
                    {
                        \context Staff = "Music_Staff"
                        {
                            \context Voice = "Music_Voice"
                            {
                                fs'!8
                                ^ \baca-explicit-indicator-markup "(“clarinet”)"
                                [
                                - \abjad-dashed-line-with-hook
                                - \baca-text-spanner-left-text "make_even_divisions()"
                                - \tweak bound-details.right.padding 2.75
                                - \tweak color #darkcyan
                                - \tweak staff-padding 8
                                \bacaStartTextSpanRhythmAnnotation
                                g'8
                                fs'!8
                                g'8
                                ]
                                fs'!8
                                [
                                g'8
                                fs'!8
                                ]
                                g'8
                                [
                                fs'!8
                                g'8
                                fs'!8
                                ]
                                g'8
                                [
                                fs'!8
                                g'8
                                ]
                                <> \bacaStopTextSpanRhythmAnnotation
                                <<
                                    \context Voice = "Music_Voice"
                                    {
                                        \abjad-invisible-music-coloring
                                        %@% \abjad-invisible-music
                                        \baca-not-yet-pitched-coloring
                                        b'1 * 1/4
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                    }
                                    \context Voice = "Rest_Voice"
                                    {
                                        \once \override Score.TimeSignature.X-extent = ##f
                                        \once \override MultiMeasureRest.transparent = ##t
                                        \stopStaff
                                        \once \override Staff.StaffSymbol.transparent = ##t
                                        \startStaff
                                        R1 * 1/4
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                    }
                                >>
                            }
                        }
                    }
                >>

        ..  container:: example

            Does not transpose score:

            >>> instruments = abjad.OrderedDict()
            >>> instruments["clarinet"] = abjad.ClarinetInBFlat()
            >>> maker = baca.SegmentMaker(
            ...     includes=["baca.ily"],
            ...     preamble=[baca.global_context_string()],
            ...     instruments=instruments,
            ...     score_template=baca.make_empty_score_maker(1),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     transpose_score=False,
            ... )

            >>> maker(
            ...     "Music_Voice",
            ...     baca.instrument(instruments["clarinet"]),
            ...     baca.make_even_divisions(),
            ...     baca.pitches("E4 F4"),
            ... )

            >>> lilypond_file = maker.run(environment="docs")
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> score = lilypond_file["Score"]
                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context GlobalContext = "Global_Context"
                    <<
                        \context GlobalSkips = "Global_Skips"
                        {
                            \time 4/8
                            \baca-time-signature-color #'blue
                            s1 * 1/2
                            \time 3/8
                            \baca-time-signature-color #'blue
                            s1 * 3/8
                            \time 4/8
                            \baca-time-signature-color #'blue
                            s1 * 1/2
                            \time 3/8
                            \baca-time-signature-color #'blue
                            s1 * 3/8
                            \time 1/4
                            \baca-time-signature-transparent
                            s1 * 1/4
                            \once \override Score.BarLine.transparent = ##t
                            \once \override Score.SpanBar.transparent = ##t
                        }
                    >>
                    \context MusicContext = "Music_Context"
                    {
                        \context Staff = "Music_Staff"
                        {
                            \context Voice = "Music_Voice"
                            {
                                e'8
                                ^ \baca-explicit-indicator-markup "(“clarinet”)"
                                [
                                - \abjad-dashed-line-with-hook
                                - \baca-text-spanner-left-text "make_even_divisions()"
                                - \tweak bound-details.right.padding 2.75
                                - \tweak color #darkcyan
                                - \tweak staff-padding 8
                                \bacaStartTextSpanRhythmAnnotation
                                f'8
                                e'8
                                f'8
                                ]
                                e'8
                                [
                                f'8
                                e'8
                                ]
                                f'8
                                [
                                e'8
                                f'8
                                e'8
                                ]
                                f'8
                                [
                                e'8
                                f'8
                                ]
                                <> \bacaStopTextSpanRhythmAnnotation
                                <<
                                    \context Voice = "Music_Voice"
                                    {
                                        \abjad-invisible-music-coloring
                                        %@% \abjad-invisible-music
                                        \baca-not-yet-pitched-coloring
                                        b'1 * 1/4
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                    }
                                    \context Voice = "Rest_Voice"
                                    {
                                        \once \override Score.TimeSignature.X-extent = ##f
                                        \once \override MultiMeasureRest.transparent = ##t
                                        \stopStaff
                                        \once \override Staff.StaffSymbol.transparent = ##t
                                        \startStaff
                                        R1 * 1/4
                                        %@% ^ \baca-duration-multiplier-markup #"1" #"4"
                                    }
                                >>
                            }
                        }
                    }
                >>

        """
        return self._transpose_score

    @property
    def voice_metadata(self):
        """
        Gets voice metadata.
        """
        return self._voice_metadata

    ### PUBLIC METHODS ###

    def run(
        self,
        do_not_print_timing=False,
        environment=None,
        first_segment=True,
        metadata=None,
        midi=False,
        page_layout_profile=None,
        persist=None,
        previous_metadata=None,
        previous_persist=None,
        segment_number=None,
    ):
        """
        Runs segment-maker.
        """
        assert environment in (None, "docs", "layout"), repr(environment)
        self._environment = environment
        assert isinstance(first_segment, bool), repr(first_segment)
        self._first_segment = first_segment
        self._metadata = abjad.OrderedDict(metadata)
        self._midi = midi
        self._page_layout_profile = page_layout_profile
        self._persist = abjad.OrderedDict(persist)
        self._previous_metadata = abjad.OrderedDict(previous_metadata)
        self._previous_persist = abjad.OrderedDict(previous_persist)
        self._segment_number = segment_number
        with abjad.Timer() as timer:
            self._make_score()
            self._make_lilypond_file()
            self._make_global_skips()
            self._label_measure_numbers()
            self._label_stage_numbers()
            self._label_moment_numbers()
        count = int(timer.elapsed_time)
        seconds = abjad.String("second").pluralize(count)
        if not do_not_print_timing and self.environment != "docs":
            print(f"Score initialization {count} {seconds} ...")
        with abjad.Timer() as timer:
            with abjad.ForbidUpdate(component=self.score, update_on_exit=True):
                command_count = self._call_rhythm_commands()
                self._clean_up_rhythm_maker_voice_names()
        count = int(timer.elapsed_time)
        seconds = abjad.String("second").pluralize(count)
        commands = abjad.String("command").pluralize(command_count)
        if not do_not_print_timing and self.environment != "docs":
            message = f"Rhythm commands {count} {seconds}"
            message += f" [for {command_count} {commands}] ..."
            print(message)
        with abjad.Timer() as timer:
            self._populate_offset_to_measure_number()
            self._extend_beams()
            self._attach_sounds_during()
            self._attach_first_segment_score_template_defaults()
            self._reapply_persistent_indicators()
            self._attach_first_appearance_score_template_defaults()
            self._apply_spacing()
        count = int(timer.elapsed_time)
        seconds = abjad.String("second").pluralize(count)
        if not do_not_print_timing and self.environment != "docs":
            print(f"After-rhythm methods {count} {seconds} ...")
        with abjad.Timer() as timer:
            with abjad.ForbidUpdate(component=self.score, update_on_exit=True):
                command_count = self._call_commands()
        count = int(timer.elapsed_time)
        seconds = abjad.String("second").pluralize(count)
        commands = abjad.String("command").pluralize(command_count)
        if not do_not_print_timing and self.environment != "docs":
            message = f"Nonrhythm commands {count} {seconds}"
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
                self._reanalyze_reapplied_synthetic_wrappers()
                self._transpose_score_()
                self._color_not_yet_registered()
                self._color_mock_pitch()
                self._color_not_yet_pitched()
                self._set_not_yet_pitched_to_staff_position_zero()
                self._clean_up_repeat_tie_direction()
                self._clean_up_laissez_vibrer_tie_direction()
                self._check_all_are_pitched_()
                self._check_doubled_dynamics()
                self._color_out_of_range()
                self._check_persistent_indicators()
                self._color_repeat_pitch_classes_()
                self._color_octaves_()
                self._attach_shadow_tie_indicators()
                self._force_nonnatural_accidentals()
                self._label_duration_multipliers()
                self._magnify_staves_()
                self._whitespace_leaves()
                self._comment_measure_numbers()
                self._apply_breaks()
                self._style_fermata_measures()
                self._shift_measure_initial_clefs()
                self._deactivate_tags()
                self._remove_docs_tags()
                self._add_container_identifiers()
                self._check_all_music_in_part_containers()
                self._check_duplicate_part_assignments()
                self._move_global_rests()
            # mutates offsets:
            self._clean_up_on_beat_grace_containers()
            self._check_wellformedness()
        count = int(timer.elapsed_time)
        seconds = abjad.String("second").pluralize(count)
        if not do_not_print_timing and self.environment != "docs":
            print(f"Postprocessing {count} {seconds} ...")
        with abjad.Timer() as timer:
            method = getattr(self.score, "_update_now")
            method(offsets_in_seconds=True)
        count = int(timer.elapsed_time)
        seconds = abjad.String("second").pluralize(count)
        if not do_not_print_timing and self.environment != "docs":
            print(f"Offsets-in-seconds update {count} {seconds} ...")
        with abjad.Timer() as timer:
            self._label_clock_time()
            self._activate_tags()
            self._collect_metadata()
            self._style_phantom_measures()
        count = int(timer.elapsed_time)
        seconds = abjad.String("second").pluralize(count)
        if not do_not_print_timing and self.environment != "docs":
            print(f"Clocktime markup {count} {seconds} ...")
        assert isinstance(self.lilypond_file, abjad.LilyPondFile)
        return self.lilypond_file
