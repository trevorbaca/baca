"""
Tags.
"""
import os

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
COLORED_PHRASING_SLUR = abjad.Tag("COLORED_PHRASING_SLUR")
CLOCK_TIME = abjad.Tag("CLOCK_TIME")
EMPTY_START_BAR = abjad.Tag("EMPTY_START_BAR")
FERMATA_MEASURE = abjad.Tag("FERMATA_MEASURE")
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
STAGE_NUMBER = abjad.Tag("STAGE_NUMBER")

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

NOT_PARTS = abjad.Tag("-PARTS")

NOT_SCORE = abjad.Tag("-SCORE")

NOT_SECTION = abjad.Tag("-SECTION")

ONLY_PARTS = abjad.Tag("+PARTS")

ONLY_SCORE = abjad.Tag("+SCORE")

ONLY_SECTION = abjad.Tag("+SECTION")

# OTHER TAGS

FERMATA_MEASURE_EMPTY_BAR_EXTENT = abjad.Tag("FERMATA_MEASURE_EMPTY_BAR_EXTENT")

FERMATA_MEASURE_NEXT_BAR_EXTENT = abjad.Tag("FERMATA_MEASURE_NEXT_BAR_EXTENT")

FERMATA_MEASURE_RESUME_BAR_EXTENT = abjad.Tag("FERMATA_MEASURE_RESUME_BAR_EXTENT")

NOT_TOPMOST = abjad.Tag("NOT_TOPMOST")


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


def clef_color_tags(path=None):
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

    ..  container:: example

        Section directory:

        >>> import pathlib
        >>> path = pathlib.Path("etude", "sections", "01")
        >>> for tag in baca.tags.clef_color_tags(path=path):
        ...     tag
        ...
        Tag(string='EXPLICIT_CLEF_COLOR')
        Tag(string='EXPLICIT_CLEF_REDRAW_COLOR')
        Tag(string='REAPPLIED_CLEF_COLOR')
        Tag(string='REAPPLIED_CLEF_REDRAW_COLOR')
        Tag(string='REDUNDANT_CLEF_COLOR')
        Tag(string='REDUNDANT_CLEF_REDRAW_COLOR')

    ..  container:: example

        Sections directory:

        >>> path = pathlib.Path("etude", "sections")
        >>> for tag in baca.tags.clef_color_tags(path=path):
        ...     tag
        ...
        Tag(string='EXPLICIT_CLEF_COLOR')
        Tag(string='EXPLICIT_CLEF_REDRAW_COLOR')
        Tag(string='REAPPLIED_CLEF_COLOR')
        Tag(string='REAPPLIED_CLEF_REDRAW_COLOR')
        Tag(string='REDUNDANT_CLEF_COLOR')
        Tag(string='REDUNDANT_CLEF_REDRAW_COLOR')

    ..  container:: example

        Build directory:

        >>> path = pathlib.Path("etude", "builds", "letter-score")
        >>> for tag in baca.tags.clef_color_tags(path=path):
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
    if path and "builds" in path.parts:
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


def function_name(frame, self=None, *, n=None):
    """
    Gets function name from ``frame``.
    """
    parts = []
    path = frame.f_code.co_filename.removesuffix(".py")
    found_library = False
    for part in reversed(path.split(os.sep)):
        parts.append(part)
        if part == "baca":
            break
        if found_library:
            break
        if part == "library":
            found_library = True
    parts = [_ for _ in parts if _ != "library"]
    parts.reverse()
    if parts[0] == "baca":
        parts.pop()
    if isinstance(self, str):
        parts.append(self)
    elif self is not None:
        parts.append(type(self).__name__)
    parts.append(frame.f_code.co_name)
    string = ".".join(parts) + ("()" if n is None else f"({n})")
    return abjad.Tag(string)


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


def persistent_indicator_color_expression_tags(path=None):
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

    ..  container:: example

        Section directory:

        >>> path = pathlib.Path("etude", "sections", "01")
        >>> section_tags = baca.tags.persistent_indicator_color_expression_tags(path)
        >>> for tag in section_tags:
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

    ..  container:: example

        Sections directory:

        >>> path = pathlib.Path("etude", "sections")
        >>> sections_tags = baca.tags.persistent_indicator_color_expression_tags(path)
        >>> for tag in sections_tags:
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

    ..  container:: example

        >>> tags == section_tags == sections_tags
        True

    ..  container:: example

        Build directory:

        >>> path = pathlib.Path("etude", "builds", "letter-score")
        >>> tags = baca.tags.persistent_indicator_color_expression_tags(path)
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
    tags.extend(clef_color_tags(path))
    tags.extend(dynamic_color_tags())
    tags.extend(instrument_color_tags())
    tags.extend(short_instrument_name_color_tags())
    tags.extend(metronome_mark_color_expression_tags())
    tags.extend(staff_lines_color_tags(path))
    tags.extend(time_signature_color_tags(path))
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


def staff_lines_color_tags(path=None):
    """
    Gets staff lines color tags.

    ..  container:: example

        >>> for tag in baca.tags.staff_lines_color_tags():
        ...     tag
        ...
        Tag(string='EXPLICIT_STAFF_LINES_COLOR')
        Tag(string='REAPPLIED_STAFF_LINES_COLOR')
        Tag(string='REDUNDANT_STAFF_LINES_COLOR')

    ..  container:: example

        Section directory:

        >>> import pathlib
        >>> path = pathlib.Path("etude", "sections", "01")
        >>> for tag in baca.tags.staff_lines_color_tags(path):
        ...     tag
        ...
        Tag(string='EXPLICIT_STAFF_LINES_COLOR')
        Tag(string='REAPPLIED_STAFF_LINES_COLOR')
        Tag(string='REDUNDANT_STAFF_LINES_COLOR')

    ..  container:: example

        Build directory:

        >>> path = pathlib.Path("etude", "builds", "letter-score")
        >>> for tag in baca.tags.staff_lines_color_tags(path):
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
    if path and "builds" in path.parts:
        tags.append(REAPPLIED_STAFF_LINES)
    return tags


def time_signature_color_tags(path=None):
    """
    Gets time signature color tags.

    ..  container:: example

        >>> for tag in baca.tags.time_signature_color_tags():
        ...     tag
        ...
        Tag(string='EXPLICIT_TIME_SIGNATURE_COLOR')
        Tag(string='REAPPLIED_TIME_SIGNATURE_COLOR')
        Tag(string='REDUNDANT_TIME_SIGNATURE_COLOR')

    ..  container:: example

        Section directory:

        >>> import pathlib
        >>> path = pathlib.Path("etude", "sections", "_")
        >>> for tag in baca.tags.time_signature_color_tags():
        ...     tag
        ...
        Tag(string='EXPLICIT_TIME_SIGNATURE_COLOR')
        Tag(string='REAPPLIED_TIME_SIGNATURE_COLOR')
        Tag(string='REDUNDANT_TIME_SIGNATURE_COLOR')

    ..  container:: example

        Build directory:

        >>> path = pathlib.Path("etude", "builds", "letter-score")
        >>> for tag in baca.tags.time_signature_color_tags():
        ...     tag
        ...
        Tag(string='EXPLICIT_TIME_SIGNATURE_COLOR')
        Tag(string='REAPPLIED_TIME_SIGNATURE_COLOR')
        Tag(string='REDUNDANT_TIME_SIGNATURE_COLOR')

    """
    tags = [
        EXPLICIT_TIME_SIGNATURE_COLOR,
        REAPPLIED_TIME_SIGNATURE_COLOR,
        REDUNDANT_TIME_SIGNATURE_COLOR,
    ]
    if path and "builds" in path.parts:
        tags.append(REAPPLIED_TIME_SIGNATURE)
    return tags


def wrappers(wrappers: list[abjad.Wrapper], *tags: abjad.Tag):
    for wrapper in wrappers:
        for tag in tags:
            wrapper.tag = wrapper.tag.append(tag)
