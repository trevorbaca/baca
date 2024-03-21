"""
Tags.
"""

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

# DOCUMENT ANNOTATIONS

ANCHOR_NOTE = abjad.Tag("ANCHOR_NOTE")
ANCHOR_SKIP = abjad.Tag("ANCHOR_SKIP")
BREAK = abjad.Tag("BREAK")
CLOCK_TIME = abjad.Tag("CLOCK_TIME")
FERMATA_MEASURE = abjad.Tag("FERMATA_MEASURE")
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
RED_START_BAR = abjad.Tag("RED_START_BAR")
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

# FRAMED LEAVES

FRAMED_LEAF = abjad.Tag("FRAMED_LEAF")

# IMPORTANT COMMANDS

ONE_VOICE_COMMAND = abjad.Tag("ONE_VOICE_COMMAND")

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

# MATERIAL ANNOTATION

MATERIAL_ANNOTATION_MARKUP = abjad.Tag("MATERIAL_ANNOTATION_MARKUP")
MATERIAL_ANNOTATION_SPANNER = abjad.Tag("MATERIAL_ANNOTATION_SPANNER")

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


# OTTAVA

EXPLICIT_OTTAVA = abjad.Tag("EXPLICIT_OTTAVA")
EXPLICIT_OTTAVA_COLOR = abjad.Tag("EXPLICIT_OTTAVA_COLOR")
REAPPLIED_OTTAVA = abjad.Tag("REAPPLIED_OTTAVA")
REAPPLIED_OTTAVA_COLOR = abjad.Tag("REAPPLIED_OTTAVA_COLOR")
REAPPLIED_OTTAVA_COLOR = abjad.Tag("REAPPLIED_OTTAVA_COLOR")
REDUNDANT_OTTAVA = abjad.Tag("REDUNDANT_OTTAVA")
REDUNDANT_OTTAVA_COLOR = abjad.Tag("REDUNDANT_OTTAVA_COLOR")

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
RIGHT_BROKEN_SHOW_NEXT = abjad.Tag("RIGHT_BROKEN_SHOW_NEXT")
SHOW_TO_JOIN_BROKEN_SPANNERS = abjad.Tag("SHOW_TO_JOIN_BROKEN_SPANNERS")

# SPANNERS CUSTOM

EOS_STOP_MM_SPANNER = abjad.Tag("EOS_STOP_MM_SPANNER")
METRIC_MODULATION_SPANNER = abjad.Tag("METRIC_MODULATION_SPANNER")
MOMENT_ANNOTATION_SPANNER = abjad.Tag("MOMENT_ANNOTATION_SPANNER")

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

# TAG GROUPS


def instrument_color_tags():
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
    return [
        EXPLICIT_TIME_SIGNATURE_COLOR,
        LOCAL_MEASURE_NUMBER,
        MEASURE_NUMBER,
        RED_START_BAR,
        REDUNDANT_TIME_SIGNATURE_COLOR,
        STAGE_NUMBER,
    ]


def metronome_mark_color_suppression_tags():
    return [EXPLICIT_METRONOME_MARK, REDUNDANT_METRONOME_MARK]


def music_annotation_tags():
    return [
        CLOCK_TIME,
        FIGURE_LABEL,
        INVISIBLE_MUSIC_COLORING,
        LOCAL_MEASURE_NUMBER,
        MATERIAL_ANNOTATION_MARKUP,
        MATERIAL_ANNOTATION_SPANNER,
        MOCK_COLORING,
        MOMENT_ANNOTATION_SPANNER,
        NOT_YET_PITCHED_COLORING,
        OCTAVE_COLORING,
        REPEAT_PITCH_CLASS_COLORING,
        SPACING,
        SPACING_OVERRIDE,
        STAFF_HIGHLIGHT,
        STAGE_NUMBER,
    ]


def persistent_indicator_color_suppression_tags():
    tags = []
    tags.extend(metronome_mark_color_suppression_tags())
    return tags


def persistent_indicator_tags():
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
        EXPLICIT_OTTAVA,
        REAPPLIED_OTTAVA,
        REDUNDANT_OTTAVA,
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
    return [SPACING, SPACING_OVERRIDE]


def spacing_tags():
    return [
        SPACING_COMMAND,
        SPACING,
        SPACING_OVERRIDE_COMMAND,
        SPACING_OVERRIDE,
    ]


# PUBLIC FUNCTIONS


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


def wrappers(wrappers: list[abjad.Wrapper], *tags: abjad.Tag):
    for wrapper in wrappers:
        for tag in tags:
            wrapper.tag = wrapper.tag.append(tag)


# TODO: move to build.py
# BUILD HELPERS


# TODO: move to build.py
def _activate_tags(
    text: str,
    match: typing.Callable,
    name: str,
    messages: list,
    *,
    prepend_empty_chord: bool = False,
    undo: bool = False,
):
    assert isinstance(text, str), repr(text)
    assert callable(match), repr(match)
    assert isinstance(messages, list), repr(messages)
    assert isinstance(name, str), repr(name)
    if undo:
        text, count, skipped = abjad.deactivate(
            text,
            match,
            prepend_empty_chord=prepend_empty_chord,
        )
    else:
        text, count, skipped = abjad.activate(text, match)
    if undo:
        adjective = "inactive"
        gerund = "deactivating"
    else:
        adjective = "active"
        gerund = "activating"
    new_messages = []
    total = count + skipped
    if total == 0:
        new_messages.append(f"found no {name} tags")
    if 0 < total:
        tags = abjad.string.pluralize("tag", total)
        new_messages.append(f"found {total} {name} {tags}")
        if 0 < count:
            tags = abjad.string.pluralize("tag", count)
            message = f"{gerund} {count} {name} {tags}"
            new_messages.append(message)
        if 0 < skipped:
            tags = abjad.string.pluralize("tag", skipped)
            message = f"skipping {skipped} ({adjective}) {name} {tags}"
            new_messages.append(message)
    new_messages = [abjad.string.capitalize_start(_) + " ..." for _ in new_messages]
    if messages is not None:
        messages.extend(new_messages)
    return text


# TODO: move to build.py
def _deactivate_tags(
    text: str,
    match: typing.Callable,
    name: str,
    messages: list,
    *,
    prepend_empty_chord: bool = False,
):
    return _activate_tags(
        text,
        match,
        name,
        messages=messages,
        prepend_empty_chord=prepend_empty_chord,
        undo=True,
    )


# TODO: move to build.py
# BUILD FUNCTIONS


def handle_edition_tags(
    text: str, messages: list[str], directory_name: str, my_name: str
) -> str:
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
    assert isinstance(text, str), repr(text)
    assert isinstance(directory_name, str), repr(directory_name)
    assert my_name in ("SECTION", "SCORE", "PARTS"), repr(my_name)
    messages.append("Handling edition tags ...")
    this_edition = abjad.Tag(f"+{my_name}")
    not_this_edition = abjad.Tag(f"-{my_name}")
    directory_name = abjad.string.to_shout_case(directory_name)
    this_directory = abjad.Tag(f"+{directory_name}")
    not_this_directory = abjad.Tag(f"-{directory_name}")

    def _deactivate(tags):
        if not_this_edition in tags:
            return True
        if not_this_directory in tags:
            return True
        for tag in tags:
            if tag.string.startswith("+"):
                return True
        return False

    text = _deactivate_tags(text, _deactivate, "other-edition", messages)

    def _activate(tags):
        for tag in tags:
            if tag in [not_this_edition, not_this_directory]:
                return False
        for tag in tags:
            if tag.string.startswith("-"):
                return True
        return bool(set(tags) & set([this_edition, this_directory]))

    text = _activate_tags(text, _activate, "this-edition", messages)
    messages.append("")
    return text


def handle_fermata_bar_lines(
    text: str,
    messages: list[str],
    bol_measure_numbers: list | None,
    final_measure_number: int | None,
) -> str:
    messages.append("Handling fermata bar lines ...")

    def _activate(tags):
        return bool(set(tags) & set([FERMATA_MEASURE]))

    # activate fermata measure bar line adjustment tags ...
    text = _activate_tags(text, _activate, "bar line adjustment", messages)
    # ... then deactivate non-EOL tags
    if bol_measure_numbers:
        eol_measure_numbers = [_ - 1 for _ in bol_measure_numbers[1:]]
        if final_measure_number is not None:
            eol_measure_numbers.append(final_measure_number)
        eol_measure_numbers = [abjad.Tag(f"MEASURE_{_}") for _ in eol_measure_numbers]

        def _deactivate(tags):
            if FERMATA_MEASURE in tags:
                if not bool(set(tags) & set(eol_measure_numbers)):
                    return True
            return False

        text = _deactivate_tags(text, _deactivate, "EOL fermata bar line", messages)
    messages.append("")
    return text


def handle_mol_tags(
    text: str,
    messages: list[str],
    bol_measure_numbers: list | None,
    final_measure_number: int | None,
) -> str:
    messages.append("Handling MOL tags ...")

    # activate all middle-of-line tags ...
    def _activate(tags):
        tags_ = set([NOT_MOL, ONLY_MOL])
        return bool(set(tags) & tags_)

    text = _activate_tags(text, _activate, "MOL", messages)
    # ... then deactivate conflicting middle-of-line tags
    if bol_measure_numbers:
        nonmol_measure_numbers = bol_measure_numbers[:]
        if final_measure_number is not None:
            nonmol_measure_numbers.append(final_measure_number + 1)
        nonmol_measure_numbers = [
            abjad.Tag(f"MEASURE_{_}") for _ in nonmol_measure_numbers
        ]

        def _deactivate(tags):
            if NOT_MOL in tags:
                if not bool(set(tags) & set(nonmol_measure_numbers)):
                    return True
            if ONLY_MOL in tags:
                if bool(set(tags) & set(nonmol_measure_numbers)):
                    return True
            return False

        text = _deactivate_tags(text, _deactivate, "conflicting MOL", messages)
    messages.append("")
    return text


def handle_shifted_clefs(
    text: str, messages: list[str], bol_measure_numbers: list | None
) -> str:
    messages.append("Handling shifted clefs ...")

    def _activate(tags):
        return SHIFTED_CLEF in tags

    # set X-extent to false and left-shift measure-initial clefs ...
    text = _activate_tags(text, _activate, "shifted clef", messages)
    # ... then unshift clefs at beginning-of-line
    if bol_measure_numbers:
        bol_measure_numbers = [abjad.Tag(f"MEASURE_{_}") for _ in bol_measure_numbers]

        def _deactivate(tags):
            if SHIFTED_CLEF not in tags:
                return False
            if any(_ in tags for _ in bol_measure_numbers):
                return True
            return False

        text = _deactivate_tags(text, _deactivate, "BOL clef", messages)
    messages.append("")
    return text


def join_broken_spanners(text: str, messages: list[str]) -> str:
    messages.append("Joining broken spanners ...")

    def _activate(tags):
        tags_ = [SHOW_TO_JOIN_BROKEN_SPANNERS]
        return bool(set(tags) & set(tags_))

    def _deactivate(tags):
        tags_ = [HIDE_TO_JOIN_BROKEN_SPANNERS]
        return bool(set(tags) & set(tags_))

    text = _activate_tags(text, _activate, "broken spanner expression", messages)
    text = _deactivate_tags(text, _deactivate, "broken spanner suppression", messages)
    messages.append("")
    return text


def not_topmost(text: str, messages: list[str]) -> str:
    messages.append(f"Deactivating {NOT_TOPMOST.string} ...")

    def _deactivate(tags):
        tags_ = [NOT_TOPMOST]
        return bool(set(tags) & set(tags_))

    text = _deactivate_tags(text, _deactivate, "not topmost", messages)
    messages.append("")
    return text


def show_music_annotations(
    text: str, messages: list[str], *, undo: bool = False
) -> str:
    name = "music annotation"

    def match(tags):
        tags_ = music_annotation_tags()
        return bool(set(tags) & set(tags_))

    def match_2(tags):
        tags_ = [INVISIBLE_MUSIC_COMMAND]
        return bool(set(tags) & set(tags_))

    if not undo:
        messages.append(f"Showing {name}s ...")
        text = _activate_tags(text, match, name, messages)
        text = _deactivate_tags(text, match_2, name, messages)
    else:
        messages.append(f"Hiding {name}s ...")
        text = _activate_tags(text, match_2, name, messages)
        text = _deactivate_tags(text, match, name, messages)
    messages.append("")
    return text


def show_tag(
    text: str,
    tag: abjad.Tag | str,
    messages: list[str],
    *,
    match: typing.Callable | None = None,
    prepend_empty_chord: bool = False,
    undo: bool = False,
) -> str:
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
        text = _activate_tags(text, match, name, messages)
    else:
        messages.append(f"Hiding {name} tags ...")
        text = _deactivate_tags(
            text,
            match,
            name,
            messages,
            prepend_empty_chord=prepend_empty_chord,
        )
    messages.append("")
    return text
