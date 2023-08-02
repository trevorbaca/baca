"""
Tags.
"""
import os
import pathlib
import typing

import abjad

# BAR EXTENT

EXPLICIT_BAR_EXTENT = abjad.Tag("EXPLICIT_BAR_EXTENT")
REAPPLIED_BAR_EXTENT = abjad.Tag("REAPPLIED_BAR_EXTENT")
REDUNDANT_BAR_EXTENT = abjad.Tag("REDUNDANT_BAR_EXTENT")

# CLEF

EXPLICIT_CLEF = abjad.Tag("EXPLICIT_CLEF")
EXPLICIT_CLEF_COLOR = abjad.Tag("EXPLICIT_CLEF_COLOR")
EXPLICIT_CLEF_COLOR_CANCELLATION = abjad.Tag("EXPLICIT_CLEF_COLOR_CANCELLATION")
EXPLICIT_CLEF_REDRAW_COLOR = abjad.Tag("EXPLICIT_CLEF_REDRAW_COLOR")
REAPPLIED_CLEF = abjad.Tag("REAPPLIED_CLEF")
REAPPLIED_CLEF_COLOR = abjad.Tag("REAPPLIED_CLEF_COLOR")
REAPPLIED_CLEF_COLOR_CANCELLATION = abjad.Tag("REAPPLIED_CLEF_COLOR_CANCELLATION")
REAPPLIED_CLEF_REDRAW_COLOR = abjad.Tag("REAPPLIED_CLEF_REDRAW_COLOR")
REDUNDANT_CLEF = abjad.Tag("REDUNDANT_CLEF")
REDUNDANT_CLEF_COLOR = abjad.Tag("REDUNDANT_CLEF_COLOR")
REDUNDANT_CLEF_COLOR_CANCELLATION = abjad.Tag("REDUNDANT_CLEF_COLOR_CANCELLATION")
REDUNDANT_CLEF_REDRAW_COLOR = abjad.Tag("REDUNDANT_CLEF_REDRAW_COLOR")

# COMMANDS IMPORTANT

ONE_VOICE_COMMAND = abjad.Tag("ONE_VOICE_COMMAND")

# DOCUMENT ANNOTATIONS

ANCHOR_NOTE = abjad.Tag("ANCHOR_NOTE")
ANCHOR_SKIP = abjad.Tag("ANCHOR_SKIP")
BREAK = abjad.Tag("BREAK")
CLOCK_TIME = abjad.Tag("CLOCK_TIME")
EMPTY_START_BAR = abjad.Tag("EMPTY_START_BAR")
FERMATA_MEASURE = abjad.Tag("FERMATA_MEASURE")
FERMATA_MEASURE_EMPTY_BAR_EXTENT = abjad.Tag("FERMATA_MEASURE_EMPTY_BAR_EXTENT")
FERMATA_MEASURE_NEXT_BAR_EXTENT = abjad.Tag("FERMATA_MEASURE_NEXT_BAR_EXTENT")
FERMATA_MEASURE_RESUME_BAR_EXTENT = abjad.Tag("FERMATA_MEASURE_RESUME_BAR_EXTENT")
FIGURE_LABEL = abjad.Tag("FIGURE_LABEL")
HIDDEN = abjad.Tag("HIDDEN")
HIDE_IN_PARTS = abjad.Tag("HIDE_IN_PARTS")
INVISIBLE_MUSIC_COLORING = abjad.Tag("INVISIBLE_MUSIC_COLORING")
INVISIBLE_MUSIC_COMMAND = abjad.Tag("INVISIBLE_MUSIC_COMMAND")
LOCAL_MEASURE_NUMBER = abjad.Tag("LOCAL_MEASURE_NUMBER")
MEASURE_NUMBER = abjad.Tag("MEASURE_NUMBER")
MOMENT_NUMBER = abjad.Tag("MOMENT_NUMBER")
MULTIMEASURE_REST = abjad.Tag("MULTIMEASURE_REST")
NOT_MOL = abjad.Tag("NOT_MOL")
NOTE = abjad.Tag("NOTE")
ONLY_MOL = abjad.Tag("ONLY_MOL")
REST_VOICE = abjad.Tag("REST_VOICE")
SHIFTED_CLEF = abjad.Tag("SHIFTED_CLEF")
SHOW_IN_PARTS = abjad.Tag("SHOW_IN_PARTS")
SKIP = abjad.Tag("SKIP")
SPACING = abjad.Tag("SPACING")
SPACING_OVERRIDE = abjad.Tag("SPACING_OVERRIDE")
SPACING_COMMAND = abjad.Tag("SPACING_COMMAND")
SPACING_OVERRIDE_COMMAND = abjad.Tag("SPACING_OVERRIDE_COMMAND")
STAFF_HIGHLIGHT = abjad.Tag("STAFF_HIGHLIGHT")
STAGE_NUMBER = abjad.Tag("STAGE_NUMBER")

# DOCUMENT TYPE RESTRICTIONS

# TODO: remove + and - prefixes
NOT_PARTS = abjad.Tag("-PARTS")
NOT_SCORE = abjad.Tag("-SCORE")
NOT_SECTION = abjad.Tag("-SECTION")
ONLY_PARTS = abjad.Tag("+PARTS")
ONLY_SCORE = abjad.Tag("+SCORE")
ONLY_SECTION = abjad.Tag("+SECTION")

# DOCUMENT TYPES

BUILD = abjad.Tag("BUILD")
PARTS = abjad.Tag("PARTS")
SCORE = abjad.Tag("SCORE")
SECTION = abjad.Tag("SECTION")

# DYNAMIC

EXPLICIT_DYNAMIC = abjad.Tag("EXPLICIT_DYNAMIC")
EXPLICIT_DYNAMIC_COLOR = abjad.Tag("EXPLICIT_DYNAMIC_COLOR")
REAPPLIED_DYNAMIC = abjad.Tag("REAPPLIED_DYNAMIC")
REAPPLIED_DYNAMIC_COLOR = abjad.Tag("REAPPLIED_DYNAMIC_COLOR")
REDUNDANT_DYNAMIC = abjad.Tag("REDUNDANT_DYNAMIC")
REDUNDANT_DYNAMIC_COLOR = abjad.Tag("REDUNDANT_DYNAMIC_COLOR")

# FIGURES

FORESHADOW = abjad.Tag("FORESHADOW")
INCOMPLETE = abjad.Tag("INCOMPLETE")
RECOLLECTION = abjad.Tag("RECOLLECTION")

# INSTRUMENT

EXPLICIT_INSTRUMENT = abjad.Tag("EXPLICIT_INSTRUMENT")
EXPLICIT_INSTRUMENT_ALERT = abjad.Tag("EXPLICIT_INSTRUMENT_ALERT")
EXPLICIT_INSTRUMENT_COLOR = abjad.Tag("EXPLICIT_INSTRUMENT_COLOR")
REDRAWN_EXPLICIT_INSTRUMENT = abjad.Tag("REDRAWN_EXPLICIT_INSTRUMENT")
REDRAWN_EXPLICIT_INSTRUMENT_COLOR = abjad.Tag("REDRAWN_EXPLICIT_INSTRUMENT_COLOR")
REAPPLIED_INSTRUMENT = abjad.Tag("REAPPLIED_INSTRUMENT")
REAPPLIED_INSTRUMENT_ALERT = abjad.Tag("REAPPLIED_INSTRUMENT_ALERT")
REAPPLIED_INSTRUMENT_COLOR = abjad.Tag("REAPPLIED_INSTRUMENT_COLOR")
REDRAWN_REAPPLIED_INSTRUMENT = abjad.Tag("REDRAWN_REAPPLIED_INSTRUMENT")
REDRAWN_REAPPLIED_INSTRUMENT_COLOR = abjad.Tag("REDRAWN_REAPPLIED_INSTRUMENT_COLOR")
REDUNDANT_INSTRUMENT = abjad.Tag("REDUNDANT_INSTRUMENT")
REDUNDANT_INSTRUMENT_ALERT = abjad.Tag("REDUNDANT_INSTRUMENT_ALERT")
REDUNDANT_INSTRUMENT_COLOR = abjad.Tag("REDUNDANT_INSTRUMENT_COLOR")
REDRAWN_REDUNDANT_INSTRUMENT = abjad.Tag("REDRAWN_REDUNDANT_INSTRUMENT")
REDRAWN_REDUNDANT_INSTRUMENT_COLOR = abjad.Tag("REDRAWN_REDUNDANT_INSTRUMENT_COLOR")

# METRONOME MARK

EXPLICIT_METRONOME_MARK = abjad.Tag("EXPLICIT_METRONOME_MARK")
EXPLICIT_METRONOME_MARK_WITH_COLOR = abjad.Tag("EXPLICIT_METRONOME_MARK_WITH_COLOR")
REAPPLIED_METRONOME_MARK = abjad.Tag("REAPPLIED_METRONOME_MARK")
REAPPLIED_METRONOME_MARK_WITH_COLOR = abjad.Tag("REAPPLIED_METRONOME_MARK_WITH_COLOR")
REDUNDANT_METRONOME_MARK = abjad.Tag("REDUNDANT_METRONOME_MARK")
REDUNDANT_METRONOME_MARK_WITH_COLOR = abjad.Tag("REDUNDANT_METRONOME_MARK_WITH_COLOR")

# METRONOME MARK SPANNER

METRIC_MODULATION_IS_NOT_SCALED = abjad.Tag("METRIC_MODULATION_IS_NOT_SCALED")
METRIC_MODULATION_IS_SCALED = abjad.Tag("METRIC_MODULATION_IS_SCALED")
METRIC_MODULATION_IS_STRIPPED = abjad.Tag("METRIC_MODULATION_IS_STRIPPED")

# NOT TOPMOST

NOT_TOPMOST = abjad.Tag("NOT_TOPMOST")

# PERSISTENT OVERRIDE

EXPLICIT_PERSISTENT_OVERRIDE = abjad.Tag("EXPLICIT_PERSISTENT_OVERRIDE")
REAPPLIED_PERSISTENT_OVERRIDE = abjad.Tag("REAPPLIED_PERSISTENT_OVERRIDE")
REDUNDANT_PERSISTENT_OVERRIDE = abjad.Tag("REDUNDANT_PERSISTENT_OVERRIDE")

# PITCH COLORINGS

MOCK_COLORING = abjad.Tag("MOCK_COLORING")
NOT_YET_PITCHED_COLORING = abjad.Tag("NOT_YET_PITCHED_COLORING")
NOT_YET_REGISTERED_COLORING = abjad.Tag("NOT_YET_REGISTERED_COLORING")
OCTAVE_COLORING = abjad.Tag("OCTAVE_COLORING")
OUT_OF_RANGE_COLORING = abjad.Tag("OUT_OF_RANGE_COLORING")
REPEAT_PITCH_CLASS_COLORING = abjad.Tag("REPEAT_PITCH_CLASS_COLORING")
TACET_COLORING = abjad.Tag("TACET_COLORING")

# RHYTHM

DURATION_MULTIPLIER = abjad.Tag("DURATION_MULTIPLIER")

# SHORT INSTRUMET NAME

EXPLICIT_SHORT_INSTRUMENT_NAME = abjad.Tag("EXPLICIT_SHORT_INSTRUMENT_NAME")
EXPLICIT_SHORT_INSTRUMENT_NAME_ALERT = abjad.Tag("EXPLICIT_SHORT_INSTRUMENT_NAME_ALERT")
EXPLICIT_SHORT_INSTRUMENT_NAME_COLOR = abjad.Tag("EXPLICIT_SHORT_INSTRUMENT_NAME_COLOR")
REDRAWN_EXPLICIT_SHORT_INSTRUMENT_NAME = abjad.Tag(
    "REDRAWN_EXPLICIT_SHORT_INSTRUMENT_NAME"
)
REDRAWN_EXPLICIT_SHORT_INSTRUMENT_NAME_COLOR = abjad.Tag(
    "REDRAWN_EXPLICIT_SHORT_INSTRUMENT_NAME_COLOR"
)
REAPPLIED_SHORT_INSTRUMENT_NAME = abjad.Tag("REAPPLIED_SHORT_INSTRUMENT_NAME")
REAPPLIED_SHORT_INSTRUMENT_NAME_ALERT = abjad.Tag(
    "REAPPLIED_SHORT_INSTRUMENT_NAME_ALERT"
)
REAPPLIED_SHORT_INSTRUMENT_NAME_COLOR = abjad.Tag(
    "REAPPLIED_SHORT_INSTRUMENT_NAME_COLOR"
)
REDRAWN_REAPPLIED_SHORT_INSTRUMENT_NAME = abjad.Tag(
    "REDRAWN_REAPPLIED_SHORT_INSTRUMENT_NAME"
)
REDRAWN_REAPPLIED_SHORT_INSTRUMENT_NAME_COLOR = abjad.Tag(
    "REDRAWN_REAPPLIED_SHORT_INSTRUMENT_NAME_COLOR"
)
REDUNDANT_SHORT_INSTRUMENT_NAME = abjad.Tag("REDUNDANT_SHORT_INSTRUMENT_NAME")
REDUNDANT_SHORT_INSTRUMENT_NAME_ALERT = abjad.Tag(
    "REDUNDANT_SHORT_INSTRUMENT_NAME_ALERT"
)
REDUNDANT_SHORT_INSTRUMENT_NAME_COLOR = abjad.Tag(
    "REDUNDANT_SHORT_INSTRUMENT_NAME_COLOR"
)
REDRAWN_REDUNDANT_SHORT_INSTRUMENT_NAME = abjad.Tag(
    "REDRAWN_REDUNDANT_SHORT_INSTRUMENT_NAME"
)
REDRAWN_REDUNDANT_SHORT_INSTRUMENT_NAME_COLOR = abjad.Tag(
    "REDRAWN_REDUNDANT_SHORT_INSTRUMENT_NAME_COLOR"
)

# SPACING SECTION

EXPLICIT_SPACING_SECTION = abjad.Tag("EXPLICIT_SPACING_SECTION")
EXPLICIT_SPACING_SECTION_COLOR = abjad.Tag("EXPLICIT_SPACING_SECTION_COLOR")
REAPPLIED_SPACING_SECTION = abjad.Tag("REAPPLIED_SPACING_SECTION")
REAPPLIED_SPACING_SECTION_COLOR = abjad.Tag("REAPPLIED_SPACING_SECTION_COLOR")
REDUNDANT_SPACING_SECTION = abjad.Tag("REDUNDANT_SPACING_SECTION")
REDUNDANT_SPACING_SECTION_COLOR = abjad.Tag("REDUNDANT_SPACING_SECTION_COLOR")

# SPANNERS BROKEN

AUTODETECT = abjad.Tag("AUTODETECT")
HIDE_TO_JOIN_BROKEN_SPANNERS = abjad.Tag("HIDE_TO_JOIN_BROKEN_SPANNERS")
LEFT_BROKEN = abjad.Tag("LEFT_BROKEN")
RIGHT_BROKEN = abjad.Tag("RIGHT_BROKEN")
RIGHT_BROKEN_BEAM = abjad.Tag("RIGHT_BROKEN_BEAM")  # used in figure-maker
RIGHT_BROKEN_SHOW_NEXT = abjad.Tag("RIGHT_BROKEN_SHOW_NEXT")
SHOW_TO_JOIN_BROKEN_SPANNERS = abjad.Tag("SHOW_TO_JOIN_BROKEN_SPANNERS")

# SPANNERS CUSTOM

BOW_SPEED_SPANNER = abjad.Tag("BOW_SPEED_SPANNER")
CIRCLE_BOW_SPANNER = abjad.Tag("CIRCLE_BOW_SPANNER")
CLB_SPANNER = abjad.Tag("CLB_SPANNER")
COVERED_SPANNER = abjad.Tag("COVERED_SPANNER")
DAMP_SPANNER = abjad.Tag("DAMP_SPANNER")
EOS_STOP_MM_SPANNER = abjad.Tag("EOS_STOP_MM_SPANNER")
HALF_CLT_SPANNER = abjad.Tag("HALF_CLT_SPANNER")
MATERIAL_ANNOTATION_SPANNER = abjad.Tag("MATERIAL_ANNOTATION_SPANNER")
METRIC_MODULATION_SPANNER = abjad.Tag("METRIC_MODULATION_SPANNER")
MOMENT_ANNOTATION_SPANNER = abjad.Tag("MOMENT_ANNOTATION_SPANNER")
PITCH_ANNOTATION_SPANNER = abjad.Tag("PITCH_ANNOTATION_SPANNER")
PIZZICATO_SPANNER = abjad.Tag("PIZZICATO_SPANNER")
RHYTHM_ANNOTATION_SPANNER = abjad.Tag("RHYTHM_ANNOTATION_SPANNER")
SCP_SPANNER = abjad.Tag("SCP_SPANNER")
SPAZZOLATO_SPANNER = abjad.Tag("SPAZZOLATO_SPANNER")
STRING_NUMBER_SPANNER = abjad.Tag("STRING_NUMBER_SPANNER")
TASTO_SPANNER = abjad.Tag("TASTO_SPANNER")
VIBRATO_SPANNER = abjad.Tag("VIBRATO_SPANNER")

# SPANNERS OTHER

SPANNER_START = abjad.Tag("SPANNER_START")
SPANNER_STOP = abjad.Tag("SPANNER_STOP")

# STAFF LINES

EXPLICIT_STAFF_LINES = abjad.Tag("EXPLICIT_STAFF_LINES")
EXPLICIT_STAFF_LINES_COLOR = abjad.Tag("EXPLICIT_STAFF_LINES_COLOR")
REAPPLIED_STAFF_LINES = abjad.Tag("REAPPLIED_STAFF_LINES")
REAPPLIED_STAFF_LINES_COLOR = abjad.Tag("REAPPLIED_STAFF_LINES_COLOR")
REDUNDANT_STAFF_LINES = abjad.Tag("REDUNDANT_STAFF_LINES")
REDUNDANT_STAFF_LINES_COLOR = abjad.Tag("REDUNDANT_STAFF_LINES_COLOR")

# TIME SIGNATURE

EXPLICIT_TIME_SIGNATURE = abjad.Tag("EXPLICIT_TIME_SIGNATURE")
EXPLICIT_TIME_SIGNATURE_COLOR = abjad.Tag("EXPLICIT_TIME_SIGNATURE_COLOR")
REAPPLIED_TIME_SIGNATURE = abjad.Tag("REAPPLIED_TIME_SIGNATURE")
REAPPLIED_TIME_SIGNATURE_COLOR = abjad.Tag("REAPPLIED_TIME_SIGNATURE_COLOR")
REDUNDANT_TIME_SIGNATURE = abjad.Tag("REDUNDANT_TIME_SIGNATURE")
REDUNDANT_TIME_SIGNATURE_COLOR = abjad.Tag("REDUNDANT_TIME_SIGNATURE_COLOR")


def activate(score, *tags):
    assert all(isinstance(_, abjad.Tag) for _ in tags), repr(tags)
    for leaf in abjad.iterate.leaves(score):
        if not isinstance(leaf, abjad.Skip):
            continue
        wrappers = abjad.get.wrappers(leaf)
        for wrapper in wrappers:
            if wrapper.tag is None:
                continue
            for tag in tags:
                if tag.string in wrapper.tag.words():
                    wrapper.deactivate = False
                    break


def clef_color_tags(*, build=False):
    """
    Gets clef color tags.

    ..  container:: example

        >>> for tag in baca.tags.clef_color_tags():
        ...     tag
        ...
        Tag(string='EXPLICIT_CLEF_COLOR')
        Tag(string='EXPLICIT_CLEF_REDRAW_COLOR')
        Tag(string='REAPPLIED_CLEF_COLOR')
        Tag(string='REAPPLIED_CLEF_REDRAW_COLOR')
        Tag(string='REDUNDANT_CLEF_COLOR')
        Tag(string='REDUNDANT_CLEF_REDRAW_COLOR')

        >>> for tag in baca.tags.clef_color_tags(build=True):
        ...     tag
        ...
        Tag(string='EXPLICIT_CLEF_COLOR')
        Tag(string='EXPLICIT_CLEF_REDRAW_COLOR')
        Tag(string='REAPPLIED_CLEF_COLOR')
        Tag(string='REAPPLIED_CLEF_REDRAW_COLOR')
        Tag(string='REDUNDANT_CLEF_COLOR')
        Tag(string='REDUNDANT_CLEF_REDRAW_COLOR')
        Tag(string='REAPPLIED_CLEF')

    """
    tags = [
        EXPLICIT_CLEF_COLOR,
        EXPLICIT_CLEF_REDRAW_COLOR,
        REAPPLIED_CLEF_COLOR,
        REAPPLIED_CLEF_REDRAW_COLOR,
        REDUNDANT_CLEF_COLOR,
        REDUNDANT_CLEF_REDRAW_COLOR,
    ]
    if build is True:
        tags.append(REAPPLIED_CLEF)
    return tags


def deactivate(score, *tags):
    assert all(isinstance(_, abjad.Tag) for _ in tags), repr(tags)
    for leaf in abjad.iterate.leaves(score):
        wrappers = abjad.get.wrappers(leaf)
        for wrapper in wrappers:
            if wrapper.tag is None:
                continue
            for tag in tags:
                if tag.string in wrapper.tag.words():
                    wrapper.deactivate = True
                    break


def dynamic_color_tags():
    """
    Gets dynamic color tags.

    ..  container:: example

        >>> for tag in baca.tags.dynamic_color_tags():
        ...     tag
        ...
        Tag(string='EXPLICIT_DYNAMIC_COLOR')
        Tag(string='REAPPLIED_DYNAMIC')
        Tag(string='REAPPLIED_DYNAMIC_COLOR')
        Tag(string='REDUNDANT_DYNAMIC_COLOR')

    """
    return [
        EXPLICIT_DYNAMIC_COLOR,
        REAPPLIED_DYNAMIC,
        REAPPLIED_DYNAMIC_COLOR,
        REDUNDANT_DYNAMIC_COLOR,
    ]


def has_persistence_tag(tag):
    """
    Is true when tag has persistence tag.

    ..  container:: example

        >>> baca.tags.has_persistence_tag(abjad.Tag("FOO"))
        False

    """
    tags = persistent_indicator_tags()
    for word in tag.words():
        if type(tag)(word) in tags:
            return True
    return False


def instrument_color_tags():
    """
    Gets instrument color tags.

    ..  container:: example

        >>> for tag in baca.tags.instrument_color_tags():
        ...     tag
        ...
        Tag(string='EXPLICIT_INSTRUMENT_ALERT')
        Tag(string='EXPLICIT_INSTRUMENT_COLOR')
        Tag(string='REAPPLIED_INSTRUMENT_COLOR')
        Tag(string='REAPPLIED_INSTRUMENT_ALERT')
        Tag(string='REDRAWN_EXPLICIT_INSTRUMENT_COLOR')
        Tag(string='REDRAWN_REAPPLIED_INSTRUMENT_COLOR')
        Tag(string='REDUNDANT_INSTRUMENT_ALERT')
        Tag(string='REDUNDANT_INSTRUMENT_COLOR')
        Tag(string='REDRAWN_REDUNDANT_INSTRUMENT_COLOR')

    """
    return [
        EXPLICIT_INSTRUMENT_ALERT,
        EXPLICIT_INSTRUMENT_COLOR,
        REAPPLIED_INSTRUMENT_COLOR,
        REAPPLIED_INSTRUMENT_ALERT,
        REDRAWN_EXPLICIT_INSTRUMENT_COLOR,
        REDRAWN_REAPPLIED_INSTRUMENT_COLOR,
        REDUNDANT_INSTRUMENT_ALERT,
        REDUNDANT_INSTRUMENT_COLOR,
        REDRAWN_REDUNDANT_INSTRUMENT_COLOR,
    ]


def layout_removal_tags():
    """
    Gets layout removal tags.

    ..  container:: example

        >>> for tag in baca.tags.layout_removal_tags():
        ...     tag
        ...
        Tag(string='EMPTY_START_BAR')
        Tag(string='EXPLICIT_TIME_SIGNATURE_COLOR')
        Tag(string='LOCAL_MEASURE_NUMBER')
        Tag(string='MEASURE_NUMBER')
        Tag(string='REDUNDANT_TIME_SIGNATURE_COLOR')
        Tag(string='STAGE_NUMBER')

    """
    return [
        EMPTY_START_BAR,
        EXPLICIT_TIME_SIGNATURE_COLOR,
        LOCAL_MEASURE_NUMBER,
        MEASURE_NUMBER,
        REDUNDANT_TIME_SIGNATURE_COLOR,
        STAGE_NUMBER,
    ]


def metronome_mark_color_expression_tags():
    """
    Gets metronome mark color expression tags.

    ..  container:: example

        >>> for tag in baca.tags.metronome_mark_color_expression_tags():
        ...     tag
        ...
        Tag(string='EXPLICIT_METRONOME_MARK_WITH_COLOR')
        Tag(string='REAPPLIED_METRONOME_MARK_WITH_COLOR')
        Tag(string='REDUNDANT_METRONOME_MARK_WITH_COLOR')

    """
    return [
        EXPLICIT_METRONOME_MARK_WITH_COLOR,
        REAPPLIED_METRONOME_MARK_WITH_COLOR,
        REDUNDANT_METRONOME_MARK_WITH_COLOR,
    ]


def metronome_mark_color_suppression_tags():
    """
    Gets metronome mark color suppression tags.

    ..  container:: example

        >>> for tag in baca.tags.metronome_mark_color_suppression_tags():
        ...     tag
        ...
        Tag(string='EXPLICIT_METRONOME_MARK')
        Tag(string='REDUNDANT_METRONOME_MARK')

    """
    return [EXPLICIT_METRONOME_MARK, REDUNDANT_METRONOME_MARK]


def music_annotation_tags():
    """
    Gets music annotation tags.

    ..  container:: example

        >>> for tag in baca.tags.music_annotation_tags():
        ...     tag
        Tag(string='CLOCK_TIME')
        Tag(string='FIGURE_LABEL')
        Tag(string='INVISIBLE_MUSIC_COLORING')
        Tag(string='LOCAL_MEASURE_NUMBER')
        Tag(string='MATERIAL_ANNOTATION_SPANNER')
        Tag(string='MOCK_COLORING')
        Tag(string='MOMENT_ANNOTATION_SPANNER')
        Tag(string='NOT_YET_PITCHED_COLORING')
        Tag(string='OCTAVE_COLORING')
        Tag(string='PITCH_ANNOTATION_SPANNER')
        Tag(string='REPEAT_PITCH_CLASS_COLORING')
        Tag(string='RHYTHM_ANNOTATION_SPANNER')
        Tag(string='SPACING')
        Tag(string='SPACING_OVERRIDE')
        Tag(string='STAGE_NUMBER')
        Tag(string='TACET_COLORING')

    """
    return [
        CLOCK_TIME,
        FIGURE_LABEL,
        INVISIBLE_MUSIC_COLORING,
        LOCAL_MEASURE_NUMBER,
        MATERIAL_ANNOTATION_SPANNER,
        MOCK_COLORING,
        MOMENT_ANNOTATION_SPANNER,
        NOT_YET_PITCHED_COLORING,
        OCTAVE_COLORING,
        PITCH_ANNOTATION_SPANNER,
        REPEAT_PITCH_CLASS_COLORING,
        RHYTHM_ANNOTATION_SPANNER,
        SPACING,
        SPACING_OVERRIDE,
        STAGE_NUMBER,
        TACET_COLORING,
    ]


def persistent_indicator_color_expression_tags(*, build=False):
    """
    Gets persistent indicator color expression tags.

    >>> import pathlib

    ..  container:: example

        >>> tags = baca.tags.persistent_indicator_color_expression_tags()
        >>> for tag in tags:
        ...     tag
        Tag(string='EXPLICIT_CLEF_COLOR')
        Tag(string='EXPLICIT_CLEF_REDRAW_COLOR')
        Tag(string='REAPPLIED_CLEF_COLOR')
        Tag(string='REAPPLIED_CLEF_REDRAW_COLOR')
        Tag(string='REDUNDANT_CLEF_COLOR')
        Tag(string='REDUNDANT_CLEF_REDRAW_COLOR')
        Tag(string='EXPLICIT_DYNAMIC_COLOR')
        Tag(string='REAPPLIED_DYNAMIC')
        Tag(string='REAPPLIED_DYNAMIC_COLOR')
        Tag(string='REDUNDANT_DYNAMIC_COLOR')
        Tag(string='EXPLICIT_INSTRUMENT_ALERT')
        Tag(string='EXPLICIT_INSTRUMENT_COLOR')
        Tag(string='REAPPLIED_INSTRUMENT_COLOR')
        Tag(string='REAPPLIED_INSTRUMENT_ALERT')
        Tag(string='REDRAWN_EXPLICIT_INSTRUMENT_COLOR')
        Tag(string='REDRAWN_REAPPLIED_INSTRUMENT_COLOR')
        Tag(string='REDUNDANT_INSTRUMENT_ALERT')
        Tag(string='REDUNDANT_INSTRUMENT_COLOR')
        Tag(string='REDRAWN_REDUNDANT_INSTRUMENT_COLOR')
        Tag(string='EXPLICIT_SHORT_INSTRUMENT_NAME_ALERT')
        Tag(string='EXPLICIT_SHORT_INSTRUMENT_NAME_COLOR')
        Tag(string='REAPPLIED_SHORT_INSTRUMENT_NAME_ALERT')
        Tag(string='REAPPLIED_SHORT_INSTRUMENT_NAME_COLOR')
        Tag(string='REDRAWN_EXPLICIT_SHORT_INSTRUMENT_NAME')
        Tag(string='REDRAWN_EXPLICIT_SHORT_INSTRUMENT_NAME_COLOR')
        Tag(string='REDRAWN_REAPPLIED_SHORT_INSTRUMENT_NAME')
        Tag(string='REDRAWN_REAPPLIED_SHORT_INSTRUMENT_NAME_COLOR')
        Tag(string='REDUNDANT_SHORT_INSTRUMENT_NAME_ALERT')
        Tag(string='REDUNDANT_SHORT_INSTRUMENT_NAME_COLOR')
        Tag(string='REDRAWN_REDUNDANT_SHORT_INSTRUMENT_NAME_COLOR')
        Tag(string='EXPLICIT_METRONOME_MARK_WITH_COLOR')
        Tag(string='REAPPLIED_METRONOME_MARK_WITH_COLOR')
        Tag(string='REDUNDANT_METRONOME_MARK_WITH_COLOR')
        Tag(string='EXPLICIT_STAFF_LINES_COLOR')
        Tag(string='REAPPLIED_STAFF_LINES_COLOR')
        Tag(string='REDUNDANT_STAFF_LINES_COLOR')
        Tag(string='EXPLICIT_TIME_SIGNATURE_COLOR')
        Tag(string='REAPPLIED_TIME_SIGNATURE_COLOR')
        Tag(string='REDUNDANT_TIME_SIGNATURE_COLOR')

        Build directory:

        >>> tags = baca.tags.persistent_indicator_color_expression_tags(build=True)
        >>> for tag in tags:
        ...     tag
        Tag(string='EXPLICIT_CLEF_COLOR')
        Tag(string='EXPLICIT_CLEF_REDRAW_COLOR')
        Tag(string='REAPPLIED_CLEF_COLOR')
        Tag(string='REAPPLIED_CLEF_REDRAW_COLOR')
        Tag(string='REDUNDANT_CLEF_COLOR')
        Tag(string='REDUNDANT_CLEF_REDRAW_COLOR')
        Tag(string='REAPPLIED_CLEF')
        Tag(string='EXPLICIT_DYNAMIC_COLOR')
        Tag(string='REAPPLIED_DYNAMIC')
        Tag(string='REAPPLIED_DYNAMIC_COLOR')
        Tag(string='REDUNDANT_DYNAMIC_COLOR')
        Tag(string='EXPLICIT_INSTRUMENT_ALERT')
        Tag(string='EXPLICIT_INSTRUMENT_COLOR')
        Tag(string='REAPPLIED_INSTRUMENT_COLOR')
        Tag(string='REAPPLIED_INSTRUMENT_ALERT')
        Tag(string='REDRAWN_EXPLICIT_INSTRUMENT_COLOR')
        Tag(string='REDRAWN_REAPPLIED_INSTRUMENT_COLOR')
        Tag(string='REDUNDANT_INSTRUMENT_ALERT')
        Tag(string='REDUNDANT_INSTRUMENT_COLOR')
        Tag(string='REDRAWN_REDUNDANT_INSTRUMENT_COLOR')
        Tag(string='EXPLICIT_SHORT_INSTRUMENT_NAME_ALERT')
        Tag(string='EXPLICIT_SHORT_INSTRUMENT_NAME_COLOR')
        Tag(string='REAPPLIED_SHORT_INSTRUMENT_NAME_ALERT')
        Tag(string='REAPPLIED_SHORT_INSTRUMENT_NAME_COLOR')
        Tag(string='REDRAWN_EXPLICIT_SHORT_INSTRUMENT_NAME')
        Tag(string='REDRAWN_EXPLICIT_SHORT_INSTRUMENT_NAME_COLOR')
        Tag(string='REDRAWN_REAPPLIED_SHORT_INSTRUMENT_NAME')
        Tag(string='REDRAWN_REAPPLIED_SHORT_INSTRUMENT_NAME_COLOR')
        Tag(string='REDUNDANT_SHORT_INSTRUMENT_NAME_ALERT')
        Tag(string='REDUNDANT_SHORT_INSTRUMENT_NAME_COLOR')
        Tag(string='REDRAWN_REDUNDANT_SHORT_INSTRUMENT_NAME_COLOR')
        Tag(string='EXPLICIT_METRONOME_MARK_WITH_COLOR')
        Tag(string='REAPPLIED_METRONOME_MARK_WITH_COLOR')
        Tag(string='REDUNDANT_METRONOME_MARK_WITH_COLOR')
        Tag(string='EXPLICIT_STAFF_LINES_COLOR')
        Tag(string='REAPPLIED_STAFF_LINES_COLOR')
        Tag(string='REDUNDANT_STAFF_LINES_COLOR')
        Tag(string='REAPPLIED_STAFF_LINES')
        Tag(string='EXPLICIT_TIME_SIGNATURE_COLOR')
        Tag(string='REAPPLIED_TIME_SIGNATURE_COLOR')
        Tag(string='REDUNDANT_TIME_SIGNATURE_COLOR')
        Tag(string='REAPPLIED_TIME_SIGNATURE')

    """
    tags = []
    tags.extend(clef_color_tags(build=build))
    tags.extend(dynamic_color_tags())
    tags.extend(instrument_color_tags())
    tags.extend(short_instrument_name_color_tags())
    tags.extend(metronome_mark_color_expression_tags())
    tags.extend(staff_lines_color_tags(build=build))
    tags.extend(time_signature_color_tags(build=build))
    return tags


def persistent_indicator_color_suppression_tags():
    """
    Gets persistent indicator color suppression tags.

    ..  container:: example

        >>> tags = baca.tags.persistent_indicator_color_suppression_tags()
        >>> for tag in tags:
        ...     tag
        ...
        Tag(string='EXPLICIT_METRONOME_MARK')
        Tag(string='REDUNDANT_METRONOME_MARK')

    """
    tags = []
    tags.extend(metronome_mark_color_suppression_tags())
    return tags


def persistent_indicator_tags():
    """
    Gets persistent indicator tags.

    ..  container:: example

        >>> for tag in baca.tags.persistent_indicator_tags():
        ...     tag
        ...
        Tag(string='EXPLICIT_CLEF')
        Tag(string='REAPPLIED_CLEF')
        Tag(string='REDUNDANT_CLEF')
        Tag(string='EXPLICIT_DYNAMIC')
        Tag(string='REAPPLIED_DYNAMIC')
        Tag(string='REDUNDANT_DYNAMIC')
        Tag(string='EXPLICIT_INSTRUMENT')
        Tag(string='REAPPLIED_INSTRUMENT')
        Tag(string='REDUNDANT_INSTRUMENT')
        Tag(string='EXPLICIT_SHORT_INSTRUMENT_NAME')
        Tag(string='REAPPLIED_SHORT_INSTRUMENT_NAME')
        Tag(string='REDUNDANT_SHORT_INSTRUMENT_NAME')
        Tag(string='EXPLICIT_METRONOME_MARK')
        Tag(string='REAPPLIED_METRONOME_MARK')
        Tag(string='REDUNDANT_METRONOME_MARK')
        Tag(string='EXPLICIT_PERSISTENT_OVERRIDE')
        Tag(string='REAPPLIED_PERSISTENT_OVERRIDE')
        Tag(string='REDUNDANT_PERSISTENT_OVERRIDE')
        Tag(string='EXPLICIT_STAFF_LINES')
        Tag(string='REAPPLIED_STAFF_LINES')
        Tag(string='REDUNDANT_STAFF_LINES')
        Tag(string='EXPLICIT_TIME_SIGNATURE')
        Tag(string='REAPPLIED_TIME_SIGNATURE')
        Tag(string='REDUNDANT_TIME_SIGNATURE')

    """
    return [
        EXPLICIT_CLEF,
        REAPPLIED_CLEF,
        REDUNDANT_CLEF,
        #
        EXPLICIT_DYNAMIC,
        REAPPLIED_DYNAMIC,
        REDUNDANT_DYNAMIC,
        #
        EXPLICIT_INSTRUMENT,
        REAPPLIED_INSTRUMENT,
        REDUNDANT_INSTRUMENT,
        #
        EXPLICIT_SHORT_INSTRUMENT_NAME,
        REAPPLIED_SHORT_INSTRUMENT_NAME,
        REDUNDANT_SHORT_INSTRUMENT_NAME,
        #
        EXPLICIT_METRONOME_MARK,
        REAPPLIED_METRONOME_MARK,
        REDUNDANT_METRONOME_MARK,
        #
        EXPLICIT_PERSISTENT_OVERRIDE,
        REAPPLIED_PERSISTENT_OVERRIDE,
        REDUNDANT_PERSISTENT_OVERRIDE,
        #
        EXPLICIT_STAFF_LINES,
        REAPPLIED_STAFF_LINES,
        REDUNDANT_STAFF_LINES,
        #
        EXPLICIT_TIME_SIGNATURE,
        REAPPLIED_TIME_SIGNATURE,
        REDUNDANT_TIME_SIGNATURE,
        #
    ]


def short_instrument_name_color_tags():
    """
    Gets short instrument name color tags.

    ..  container:: example

        >>> for tag in baca.tags.short_instrument_name_color_tags():
        ...     tag
        Tag(string='EXPLICIT_SHORT_INSTRUMENT_NAME_ALERT')
        Tag(string='EXPLICIT_SHORT_INSTRUMENT_NAME_COLOR')
        Tag(string='REAPPLIED_SHORT_INSTRUMENT_NAME_ALERT')
        Tag(string='REAPPLIED_SHORT_INSTRUMENT_NAME_COLOR')
        Tag(string='REDRAWN_EXPLICIT_SHORT_INSTRUMENT_NAME')
        Tag(string='REDRAWN_EXPLICIT_SHORT_INSTRUMENT_NAME_COLOR')
        Tag(string='REDRAWN_REAPPLIED_SHORT_INSTRUMENT_NAME')
        Tag(string='REDRAWN_REAPPLIED_SHORT_INSTRUMENT_NAME_COLOR')
        Tag(string='REDUNDANT_SHORT_INSTRUMENT_NAME_ALERT')
        Tag(string='REDUNDANT_SHORT_INSTRUMENT_NAME_COLOR')
        Tag(string='REDRAWN_REDUNDANT_SHORT_INSTRUMENT_NAME_COLOR')

    """
    return [
        EXPLICIT_SHORT_INSTRUMENT_NAME_ALERT,
        EXPLICIT_SHORT_INSTRUMENT_NAME_COLOR,
        REAPPLIED_SHORT_INSTRUMENT_NAME_ALERT,
        REAPPLIED_SHORT_INSTRUMENT_NAME_COLOR,
        REDRAWN_EXPLICIT_SHORT_INSTRUMENT_NAME,
        REDRAWN_EXPLICIT_SHORT_INSTRUMENT_NAME_COLOR,
        REDRAWN_REAPPLIED_SHORT_INSTRUMENT_NAME,
        REDRAWN_REAPPLIED_SHORT_INSTRUMENT_NAME_COLOR,
        REDUNDANT_SHORT_INSTRUMENT_NAME_ALERT,
        REDUNDANT_SHORT_INSTRUMENT_NAME_COLOR,
        REDRAWN_REDUNDANT_SHORT_INSTRUMENT_NAME_COLOR,
    ]


def spacing_markup_tags():
    """
    Gets markup spacing tags.

    ..  container:: example

        >>> for tag in baca.tags.spacing_markup_tags():
        ...     tag
        ...
        Tag(string='SPACING')
        Tag(string='SPACING_OVERRIDE')

    """
    return [SPACING, SPACING_OVERRIDE]


def spacing_tags():
    """
    Gets spacing tags.

    ..  container:: example

        >>> for tag in baca.tags.spacing_tags():
        ...     tag
        ...
        Tag(string='SPACING_COMMAND')
        Tag(string='SPACING')
        Tag(string='SPACING_OVERRIDE_COMMAND')
        Tag(string='SPACING_OVERRIDE')

    """
    return [
        SPACING_COMMAND,
        SPACING,
        SPACING_OVERRIDE_COMMAND,
        SPACING_OVERRIDE,
    ]


def staff_lines_color_tags(*, build=False):
    """
    Gets staff lines color tags.

    ..  container:: example

        >>> for tag in baca.tags.staff_lines_color_tags():
        ...     tag
        ...
        Tag(string='EXPLICIT_STAFF_LINES_COLOR')
        Tag(string='REAPPLIED_STAFF_LINES_COLOR')
        Tag(string='REDUNDANT_STAFF_LINES_COLOR')

        Build directory:

        >>> for tag in baca.tags.staff_lines_color_tags(build=True):
        ...     tag
        ...
        Tag(string='EXPLICIT_STAFF_LINES_COLOR')
        Tag(string='REAPPLIED_STAFF_LINES_COLOR')
        Tag(string='REDUNDANT_STAFF_LINES_COLOR')
        Tag(string='REAPPLIED_STAFF_LINES')

    """
    tags = [
        EXPLICIT_STAFF_LINES_COLOR,
        REAPPLIED_STAFF_LINES_COLOR,
        REDUNDANT_STAFF_LINES_COLOR,
    ]
    if build is True:
        tags.append(REAPPLIED_STAFF_LINES)
    return tags


def time_signature_color_tags(*, build=False):
    """
    Gets time signature color tags.

    ..  container:: example

        >>> for tag in baca.tags.time_signature_color_tags():
        ...     tag
        ...
        Tag(string='EXPLICIT_TIME_SIGNATURE_COLOR')
        Tag(string='REAPPLIED_TIME_SIGNATURE_COLOR')
        Tag(string='REDUNDANT_TIME_SIGNATURE_COLOR')

        Build directory:

        >>> for tag in baca.tags.time_signature_color_tags(build=True):
        ...     tag
        ...
        Tag(string='EXPLICIT_TIME_SIGNATURE_COLOR')
        Tag(string='REAPPLIED_TIME_SIGNATURE_COLOR')
        Tag(string='REDUNDANT_TIME_SIGNATURE_COLOR')
        Tag(string='REAPPLIED_TIME_SIGNATURE')

    """
    tags = [
        EXPLICIT_TIME_SIGNATURE_COLOR,
        REAPPLIED_TIME_SIGNATURE_COLOR,
        REDUNDANT_TIME_SIGNATURE_COLOR,
    ]
    if build is True:
        tags.append(REAPPLIED_TIME_SIGNATURE)
    return tags


def wrappers(wrappers: list[abjad.Wrapper], *tags: abjad.Tag):
    for wrapper in wrappers:
        for tag in tags:
            wrapper.tag = wrapper.tag.append(tag)


# BUILD FUNCTIONS


def _activate(
    path: pathlib.Path,
    tag: abjad.Tag | typing.Callable,
    *,
    indent: int = 0,
    name: str = "",
    prepend_empty_chord: bool = False,
    skip_file_name: str = "",
    undo: bool = False,
) -> tuple[int, int, list[str]]:
    """
    Activates ``tag`` in .ily or .ly ``path``.

    Returns triple.

    First item in triple is count of deactivated tags activated by method.

    Second item in pair is count of already-active tags skipped by method.

    Third item in pair is list of string messages that explain what happened.
    """
    assert isinstance(path, pathlib.Path), repr(path)
    assert path.is_file(), repr(path)
    assert path.suffix in (".ily", ".ly")
    if path.name not in ("layout.ly", "music.ily", "music.ly"):
        assert path.name[0].isdigit(), repr(path)
    assert isinstance(indent, int), repr(indent)
    if path.name == skip_file_name:
        return 0, 0, []
    if isinstance(tag, str):
        raise Exception(f"must be tag or callable: {tag!r}")
    text = path.read_text()
    if undo:
        text, count, skipped = abjad.deactivate(
            text,
            tag,
            prepend_empty_chord=prepend_empty_chord,
        )
    else:
        text, count, skipped = abjad.activate(text, tag)
    path.write_text(text)
    if name is None:
        if isinstance(tag, abjad.Tag):
            name = tag.string
        else:
            name = str(tag)
    if undo:
        adjective = "inactive"
        gerund = "deactivating"
    else:
        adjective = "active"
        gerund = "activating"
    messages = []
    total = count + skipped
    if total == 0:
        messages.append(f"found no {name} tags")
    if 0 < total:
        tags = abjad.string.pluralize("tag", total)
        messages.append(f"found {total} {name} {tags}")
        if 0 < count:
            tags = abjad.string.pluralize("tag", count)
            message = f"{gerund} {count} {name} {tags}"
            messages.append(message)
        if 0 < skipped:
            tags = abjad.string.pluralize("tag", skipped)
            message = f"skipping {skipped} ({adjective}) {name} {tags}"
            messages.append(message)
    whitespace = indent * " "
    messages = [
        whitespace + abjad.string.capitalize_start(_) + " ..." for _ in messages
    ]
    return count, skipped, messages


def _deactivate(
    path: pathlib.Path,
    tag: abjad.Tag | typing.Callable,
    *,
    indent: int = 0,
    name: str = "",
    prepend_empty_chord: bool = False,
    skip_file_name: str = "",
):
    return _activate(
        path,
        tag,
        name=name,
        indent=indent,
        prepend_empty_chord=prepend_empty_chord,
        skip_file_name=skip_file_name,
        undo=True,
    )


def color_clefs(path: pathlib.Path, *, undo: bool = False) -> list[str]:
    assert isinstance(path, pathlib.Path)
    messages, name = ["Coloring clefs ..."], "clef color"

    def match(tags):
        build = "builds" in path.parts
        tags_ = clef_color_tags(build=build)
        return bool(set(tags) & set(tags_))

    if not undo:
        _, _, messages_ = _activate(path, match, name=name)
    else:
        _, _, messages_ = _deactivate(path, match, name=name)
    messages.extend(messages_)
    messages.append("")
    return messages


def color_dynamics(path: pathlib.Path, *, undo: bool = False) -> list[str]:
    assert isinstance(path, pathlib.Path)
    messages, name = ["Coloring dynamics ..."], "dynamic color"

    def match(tags):
        tags_ = dynamic_color_tags()
        return bool(set(tags) & set(tags_))

    if not undo:
        _, _, messages_ = _activate(path, match, name=name)
    else:
        _, _, messages_ = _deactivate(path, match, name=name)
    messages.extend(messages_)
    messages.append("")
    return messages


def color_instruments(path: pathlib.Path, *, undo: bool = False) -> list[str]:
    assert isinstance(path, pathlib.Path)
    messages, name = ["Coloring instruments ..."], "instrument color"

    def match(tags):
        tags_ = instrument_color_tags()
        return bool(set(tags) & set(tags_))

    if not undo:
        _, _, messages_ = _activate(path, match, name=name)
    else:
        _, _, messages_ = _deactivate(path, match, name=name)
    messages.extend(messages_)
    messages.append("")
    return messages


def color_short_instrument_names(
    path: pathlib.Path, *, undo: bool = False
) -> list[str]:
    assert isinstance(path, pathlib.Path)
    messages, name = [
        "Coloring short instrument names ..."
    ], "short instrument name color"

    def match(tags):
        tags_ = short_instrument_name_color_tags()
        return bool(set(tags) & set(tags_))

    if not undo:
        _, _, messages_ = _activate(path, match, name=name)
    else:
        _, _, messages_ = _deactivate(path, match, name=name)
    messages.extend(messages_)
    messages.append("")
    return messages


def color_metronome_marks(path: pathlib.Path, undo: bool = False) -> list[str]:
    assert isinstance(path, pathlib.Path)

    def activate(tags):
        tags_ = metronome_mark_color_expression_tags()
        return bool(set(tags) & set(tags_))

    def deactivate(tags):
        tags_ = metronome_mark_color_suppression_tags()
        return bool(set(tags) & set(tags_))

    if undo:
        messages = ["Uncoloring metronome marks ..."]
        _, _, messages_ = _activate(
            path, deactivate, name="metronome mark color suppression"
        )
        messages.extend(messages_)
        _, _, messages_ = _deactivate(
            path, activate, name="metronome mark color expression"
        )
        messages.extend(messages_)
    else:
        messages = ["Coloring metronome marks ..."]
        _, _, messages_ = _activate(
            path, activate, name="metronome mark color experssion"
        )
        messages.extend(messages_)
        _, _, messages_ = _deactivate(
            path, deactivate, name="metronome mark color suppression"
        )
        messages.extend(messages_)
    messages.append("")
    return messages


def color_persistent_indicators(path: pathlib.Path, *, undo: bool = False) -> list[str]:
    assert isinstance(path, pathlib.Path)
    name = "persistent indicator"

    def activate(tags):
        build = "builds" in path.parts
        tags_ = persistent_indicator_color_expression_tags(build=build)
        return bool(set(tags) & set(tags_))

    def deactivate(tags):
        tags_ = persistent_indicator_color_suppression_tags()
        return bool(set(tags) & set(tags_))

    if undo:
        messages = [f"Uncoloring {name}s ..."]
        _, _, messages_ = _activate(
            path, deactivate, name="persistent indicator color suppression"
        )
        messages.extend(messages_)
        _, _, messages_ = _deactivate(
            path, activate, name="persistent indicator color expression"
        )
        messages.extend(messages_)
    else:
        messages = [f"Coloring {name}s ..."]
        _, _, messages_ = _activate(
            path, activate, name="persistent indicator color expression"
        )
        messages.extend(messages_)
        _, _, messages_ = _deactivate(
            path, deactivate, name="persistent indicator color suppression"
        )
        messages.extend(messages_)
    messages.append("")
    return messages


def color_staff_lines(path: pathlib.Path, *, undo: bool = False) -> list[str]:
    assert isinstance(path, pathlib.Path)
    messages, name = ["Coloring staff lines ..."], "staff lines color"

    def match(tags):
        build = "builds" in path.parts
        tags_ = staff_lines_color_tags(build=build)
        return bool(set(tags) & set(tags_))

    if not undo:
        _, _, messages_ = _activate(path, match, name=name)
    else:
        _, _, messages_ = _deactivate(path, match, name=name)
    messages.extend(messages_)
    messages.append("")
    return messages


def color_time_signatures(path: pathlib.Path, *, undo: bool = False) -> list[str]:
    assert isinstance(path, pathlib.Path)
    messages, name = ["Coloring time signatures ..."], "time signature color"

    def match(tags):
        build = "builds" in path.parts
        tags_ = time_signature_color_tags(build=build)
        return bool(set(tags) & set(tags_))

    if not undo:
        _, _, messages_ = _activate(path, match, name=name)
    else:
        _, _, messages_ = _deactivate(path, match, name=name)
    messages.extend(messages_)
    messages.append("")
    return messages


def handle_edition_tags(path: pathlib.Path) -> list[str]:
    """
    Handles edition tags.

    The logic here is important:

        * deactivations run first:

            -TAG (where TAG is either my directory or my buildtype)

            +TAG (where TAG is neither my directory nor my buildtype)

        * activations run afterwards:

            TAG_SET such that there exists at least one build-forbid -TAG (equal to
            neither my directory nor my buildtype) in TAG_SET and such that there exists
            no -TAG (equal to either my directory or my buildtype) in TAG_SET

            +TAG (where TAG is either my directory or my buildtype)

        Notionally: first we deactivate anything that is tagged EITHER specifically
        against me OR specifically for another build; then we activate anything that is
        deactivated for editions other than me; then we activate anything is tagged
        specifically for me.

    """
    assert isinstance(path, pathlib.Path)
    messages = ["Handling edition tags ..."]
    if "sections" in path.parts:
        my_name = "SECTION"
    elif "builds" in path.parts:
        if "-score" in str(path):
            my_name = "SCORE"
        elif "-parts" in str(path):
            my_name = "PARTS"
        else:
            raise Exception(path)
    else:
        raise Exception(path)
    this_edition = abjad.Tag(f"+{abjad.string.to_shout_case(my_name)}")
    not_this_edition = abjad.Tag(f"-{abjad.string.to_shout_case(my_name)}")
    if path.is_dir():
        directory_name = path.name
    else:
        directory_name = path.parent.name
    this_directory = abjad.Tag(f"+{abjad.string.to_shout_case(directory_name)}")
    not_this_directory = abjad.Tag(f"-{abjad.string.to_shout_case(directory_name)}")

    def deactivate(tags):
        if not_this_edition in tags:
            return True
        if not_this_directory in tags:
            return True
        for tag in tags:
            if tag.string.startswith("+"):
                return True
        return False

    _, _, messages_ = _deactivate(path, deactivate, name="other-edition")
    messages.extend(messages_)

    def activate(tags):
        for tag in tags:
            if tag in [not_this_edition, not_this_directory]:
                return False
        for tag in tags:
            if tag.string.startswith("-"):
                return True
        return bool(set(tags) & set([this_edition, this_directory]))

    _, _, messages_ = _activate(path, activate, name="this-edition")
    messages.extend(messages_)
    messages.append("")
    return messages


def handle_fermata_bar_lines(
    path: pathlib.Path,
    bol_measure_numbers: list | None,
    final_measure_number: int | None,
) -> list[str]:
    assert isinstance(path, pathlib.Path)
    messages = ["Handling fermata bar lines ..."]
    if path.name == "_sections":
        path = path.parent

    def activate(tags):
        return bool(set(tags) & set([FERMATA_MEASURE]))

    # activate fermata measure bar line adjustment tags ...
    _, _, messages_ = _activate(path, activate, name="bar line adjustment")
    messages.extend(messages_)
    # ... then deactivate non-EOL tags
    if bol_measure_numbers:
        eol_measure_numbers = [_ - 1 for _ in bol_measure_numbers[1:]]
        if final_measure_number is not None:
            eol_measure_numbers.append(final_measure_number)
        eol_measure_numbers = [abjad.Tag(f"MEASURE_{_}") for _ in eol_measure_numbers]

        def deactivate(tags):
            if FERMATA_MEASURE in tags:
                if not bool(set(tags) & set(eol_measure_numbers)):
                    return True
            return False

        _, _, messages_ = _deactivate(path, deactivate, name="EOL fermata bar line")
        messages.extend(messages_)
    messages.append("")
    return messages


def handle_mol_tags(
    path: pathlib.Path,
    bol_measure_numbers: list | None,
    final_measure_number: int | None,
) -> list[str]:
    assert isinstance(path, pathlib.Path)
    messages = ["Handling MOL tags ..."]
    if path.name == "_sections":
        path = path.parent

    # activate all middle-of-line tags ...
    def activate(tags):
        tags_ = set([NOT_MOL, ONLY_MOL])
        return bool(set(tags) & tags_)

    _, _, messages_ = _activate(path, activate, name="MOL")
    messages.extend(messages_)
    # ... then deactivate conflicting middle-of-line tags
    if bol_measure_numbers:
        nonmol_measure_numbers = bol_measure_numbers[:]
        if final_measure_number is not None:
            nonmol_measure_numbers.append(final_measure_number + 1)
        nonmol_measure_numbers = [
            abjad.Tag(f"MEASURE_{_}") for _ in nonmol_measure_numbers
        ]

        def deactivate(tags):
            if NOT_MOL in tags:
                if not bool(set(tags) & set(nonmol_measure_numbers)):
                    return True
            if ONLY_MOL in tags:
                if bool(set(tags) & set(nonmol_measure_numbers)):
                    return True
            return False

        _, _, messages_ = _deactivate(path, deactivate, name="conflicting MOL")
        messages.extend(messages_)
    messages.append("")
    return messages


def handle_shifted_clefs(
    path: pathlib.Path, bol_measure_numbers: list | None
) -> list[str]:
    assert isinstance(path, pathlib.Path)
    messages = ["Handling shifted clefs ..."]

    def activate(tags):
        return SHIFTED_CLEF in tags

    # set X-extent to false and left-shift measure-initial clefs ...
    _, _, messages_ = _activate(path, activate, name="shifted clef")
    messages.extend(messages_)
    # ... then unshift clefs at beginning-of-line
    if "builds" in path.parts:
        index = path.parts.index("builds")
        build_parts = path.parts[: index + 2]
        build_directory = pathlib.Path(os.path.sep.join(build_parts))
        metadata_source = build_directory
    elif path.is_dir():
        metadata_source = path
    else:
        metadata_source = path.parent
    if not bol_measure_numbers:
        print("WARNING: no BOL metadata found!")
        print(metadata_source)
    if bol_measure_numbers:
        bol_measure_numbers = [abjad.Tag(f"MEASURE_{_}") for _ in bol_measure_numbers]

        def deactivate(tags):
            if SHIFTED_CLEF not in tags:
                return False
            if any(_ in tags for _ in bol_measure_numbers):
                return True
            return False

        _, _, messages_ = _deactivate(path, deactivate, name="BOL clef")
        messages.extend(messages_)
    messages.append("")
    return messages


def join_broken_spanners(path: pathlib.Path) -> list[str]:
    assert isinstance(path, pathlib.Path)
    messages = ["Joining broken spanners ..."]

    def activate(tags):
        tags_ = [SHOW_TO_JOIN_BROKEN_SPANNERS]
        return bool(set(tags) & set(tags_))

    def deactivate(tags):
        tags_ = [HIDE_TO_JOIN_BROKEN_SPANNERS]
        return bool(set(tags) & set(tags_))

    _, _, messages_ = _activate(path, activate, name="broken spanner expression")
    messages.extend(messages_)
    _, _, messages_ = _deactivate(path, deactivate, name="broken spanner suppression")
    messages.extend(messages_)
    messages.append("")
    return messages


def not_topmost(path: pathlib.Path) -> list[str]:
    assert isinstance(path, pathlib.Path)
    messages = [f"Deactivating {NOT_TOPMOST.string} ..."]
    count, skipped, messages_ = _deactivate(
        path,
        NOT_TOPMOST,
        name="not topmost",
    )
    messages.extend(messages_)
    messages.append("")
    return messages


def show_music_annotations(path: pathlib.Path, *, undo: bool = False) -> list[str]:
    assert isinstance(path, pathlib.Path)
    messages, name = [], "music annotation"

    def match(tags):
        tags_ = music_annotation_tags()
        return bool(set(tags) & set(tags_))

    def match_2(tags):
        tags_ = [INVISIBLE_MUSIC_COMMAND]
        return bool(set(tags) & set(tags_))

    if not undo:
        messages.append(f"Showing {name}s ...")
        _, _, messages_ = _activate(path, match, name=name)
        messages.extend(messages_)
        _, _, messages_ = _deactivate(path, match_2, name=name)
        messages.extend(messages_)
    else:
        messages.append(f"Hiding {name}s ...")
        _, _, messages_ = _activate(path, match_2, name=name)
        messages.extend(messages_)
        _, _, messages_ = _deactivate(path, match, name=name)
        messages.extend(messages_)
    messages.append("")
    return messages


def show_tag(
    path: pathlib.Path,
    tag: abjad.Tag | str,
    *,
    match: typing.Callable | None = None,
    prepend_empty_chord: bool = False,
    skip_file_name: str = "",
    undo: bool = False,
) -> list[str]:
    assert isinstance(path, pathlib.Path)
    messages = []
    if match is not None:
        assert callable(match)
    if isinstance(tag, str):
        assert match is not None, repr(match)
        name = tag
    else:
        assert isinstance(tag, abjad.Tag), repr(tag)
        name = tag.string

    if match is None:

        def match(tags):
            tags_ = [tag]
            return bool(set(tags) & set(tags_))

    if not undo:
        messages.append(f"Showing {name} tags ...")
        _, _, messages_ = _activate(
            path, match, name=name, skip_file_name=skip_file_name
        )
        messages.extend(messages_)
    else:
        messages.append(f"Hiding {name} tags ...")
        _, _, messages_ = _deactivate(
            path,
            match,
            name=name,
            prepend_empty_chord=prepend_empty_chord,
            skip_file_name=skip_file_name,
        )
        messages.extend(messages_)
    messages.append("")
    return messages
