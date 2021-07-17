import abjad

from . import segments as _segments
from . import tags as _tags


def color_clefs(path, undo=False):
    name = "clef color"

    def match(tags):
        tags_ = _tags.clef_color_tags(path)
        return bool(set(tags) & set(tags_))

    if undo:
        return _segments.Job(
            deactivate=(match, name),
            path=path,
            title="uncoloring clefs ...",
        )
    else:
        return _segments.Job(
            activate=(match, name), path=path, title="coloring clefs ..."
        )


def color_dynamics(path, undo=False):
    name = "dynamic color"

    def match(tags):
        tags_ = _tags.dynamic_color_tags(path)
        return bool(set(tags) & set(tags_))

    if undo:
        return _segments.Job(
            deactivate=(match, name),
            path=path,
            title="uncoloring dynamics ...",
        )
    else:
        return _segments.Job(
            activate=(match, name),
            path=path,
            title="coloring dynamics ...",
        )


def color_instruments(path, undo=False):
    """
    Colors instruments.
    """
    name = "instrument color"

    def match(tags):
        tags_ = _tags.instrument_color_tags(path)
        return bool(set(tags) & set(tags_))

    if undo:
        return _segments.Job(
            deactivate=(match, name),
            path=path,
            title="uncoloring instruments ...",
        )
    else:
        return _segments.Job(
            activate=(match, name),
            path=path,
            title="coloring instruments ...",
        )


def color_margin_markup(path, undo=False):
    """
    Colors margin markup.
    """
    name = "margin markup color"

    def match(tags):
        tags_ = _tags.margin_markup_color_tags(path)
        return bool(set(tags) & set(tags_))

    if undo:
        return _segments.Job(
            deactivate=(match, name),
            path=path,
            title="uncoloring margin markup ...",
        )
    else:
        return _segments.Job(
            activate=(match, name),
            path=path,
            title="coloring margin markup ...",
        )


def color_metronome_marks(path, undo=False):
    """
    Colors metronome marks.
    """

    def activate(tags):
        tags_ = _tags.metronome_mark_color_expression_tags(path)
        return bool(set(tags) & set(tags_))

    def deactivate(tags):
        tags_ = _tags.metronome_mark_color_suppression_tags(path)
        return bool(set(tags) & set(tags_))

    if undo:
        return _segments.Job(
            activate=(deactivate, "metronome mark color suppression"),
            deactivate=(activate, "metronome mark color expression"),
            path=path,
            title="uncoloring metronome marks ...",
        )
    else:
        return _segments.Job(
            activate=(activate, "metronome mark color expression"),
            deactivate=(deactivate, "metronome mark color suppression"),
            path=path,
            title="coloring metronome marks ...",
        )


def color_persistent_indicators(path, undo=False):
    """
    Color persistent indicators.
    """
    name = "persistent indicator"
    activate_name = "persistent indicator color expression"

    def activate(tags):
        tags_ = _tags.persistent_indicator_color_expression_tags(path)
        return bool(set(tags) & set(tags_))

    deactivate_name = "persistent indicator color suppression"

    def deactivate(tags):
        tags_ = _tags.persistent_indicator_color_suppression_tags(path)
        return bool(set(tags) & set(tags_))

    if undo:
        return _segments.Job(
            activate=(deactivate, deactivate_name),
            deactivate=(activate, activate_name),
            path=path,
            title=f"uncoloring {name}s ...",
        )
    else:
        return _segments.Job(
            activate=(activate, activate_name),
            deactivate=(deactivate, deactivate_name),
            path=path,
            title=f"coloring {name}s ...",
        )


def color_staff_lines(path, undo=False):
    """
    Colors staff lines.
    """
    name = "staff lines color"

    def match(tags):
        tags_ = _tags.staff_lines_color_tags(path)
        return bool(set(tags) & set(tags_))

    if undo:
        return _segments.Job(
            deactivate=(match, name),
            path=path,
            title="uncoloring staff lines ...",
        )
    else:
        return _segments.Job(
            activate=(match, name),
            path=path,
            title="coloring staff lines ...",
        )


def color_time_signatures(path, undo=False):
    """
    Colors time signatures.
    """
    name = "time signature color"

    def match(tags):
        tags_ = _tags.time_signature_color_tags(path)
        return bool(set(tags) & set(tags_))

    if undo:
        return _segments.Job(
            deactivate=(match, name),
            path=path,
            title="uncoloring time signatures ...",
        )
    else:
        return _segments.Job(
            activate=(match, name),
            path=path,
            title="coloring time signatures ...",
        )


def handle_edition_tags(path):
    """
    Handles edition tags.

    The logic here is important:

        * deactivations run first:

            -TAG (where TAG is either my directory or my buildtype)

            +TAG (where TAG is neither my directory nor my buildtype)

        * activations run afterwards:

            TAG_SET such that there exists at least one build-forbid
                -TAG (equal to neither my directory nor my buildtype) in
                TAG_SET and such that there exists no -TAG (equal to either
                my directory or my buildtype) in TAG_SET

            +TAG (where TAG is either my directory or my buildtype)

        Notionally: first we deactivate anything that is tagged EITHER
        specifically against me OR specifically for another build; then we
        activate anything that is deactivated for editions other than me;
        then we activate anything is tagged specifically for me.

    ..  todo: Tests.

    """
    if path.parent.parent.name == "segments":
        my_name = "SEGMENT"
    elif path.is_score_build() or path.parent.is_score_build():
        my_name = "SCORE"
    elif path.is_parts() or path.is_part():
        my_name = "PARTS"
    else:
        raise Exception(path)
    this_edition = abjad.Tag(f"+{abjad.String(my_name).to_shout_case()}")
    not_this_edition = abjad.Tag(f"-{abjad.String(my_name).to_shout_case()}")
    if path.is_dir():
        directory_name = path.name
    else:
        directory_name = path.parent.name
    this_directory = abjad.Tag(f"+{abjad.String(directory_name).to_shout_case()}")
    not_this_directory = abjad.Tag(f"-{abjad.String(directory_name).to_shout_case()}")

    def deactivate(tags):
        if not_this_edition in tags:
            return True
        if not_this_directory in tags:
            return True
        for tag in tags:
            if str(tag).startswith("+"):
                return True
        return False

    def activate(tags):
        for tag in tags:
            if tag in [not_this_edition, not_this_directory]:
                return False
        for tag in tags:
            if str(tag).startswith("-"):
                return True
        return bool(set(tags) & set([this_edition, this_directory]))

    return _segments.Job(
        activate=(activate, "this-edition"),
        deactivate=(deactivate, "other-edition"),
        deactivate_first=True,
        path=path,
        title="handling edition tags ...",
    )


def handle_fermata_bar_lines(path):
    """
    Handles fermata bar lines.
    """
    if path.name == "_segments":
        path = path.parent

    def activate(tags):
        return bool(set(tags) & set([_tags.FERMATA_MEASURE]))

    # then deactivate non-EOL tags:
    bol_measure_numbers = path.get_metadatum("bol_measure_numbers")
    if bol_measure_numbers:
        eol_measure_numbers = [_ - 1 for _ in bol_measure_numbers[1:]]
        final_measure_number = path.get_metadatum("final_measure_number")
        if final_measure_number is not None:
            eol_measure_numbers.append(final_measure_number)
        eol_measure_numbers = [abjad.Tag(f"MEASURE_{_}") for _ in eol_measure_numbers]

        def deactivate(tags):
            if _tags.FERMATA_MEASURE in tags:
                if not bool(set(tags) & set(eol_measure_numbers)):
                    return True
            return False

    else:
        deactivate = None
    return _segments.Job(
        activate=(activate, "bar line adjustment"),
        deactivate=(deactivate, "EOL fermata bar line"),
        path=path,
        title="handling fermata bar lines ...",
    )


def handle_mol_tags(path):
    """
    Handles MOL (middle-of-line) tags.
    """
    if path.name == "_segments":
        path = path.parent

    # activate all middle-of-line tags
    def activate(tags):
        tags_ = set([_tags.NOT_MOL, _tags.ONLY_MOL])
        return bool(set(tags) & tags_)

    # then deactivate conflicting middle-of-line tags
    bol_measure_numbers = path.get_metadatum("bol_measure_numbers")
    if bol_measure_numbers:
        nonmol_measure_numbers = bol_measure_numbers[:]
        final_measure_number = path.get_metadatum("final_measure_number")
        if final_measure_number is not None:
            nonmol_measure_numbers.append(final_measure_number + 1)
        nonmol_measure_numbers = [
            abjad.Tag(f"MEASURE_{_}") for _ in nonmol_measure_numbers
        ]

        def deactivate(tags):
            if _tags.NOT_MOL in tags:
                if not bool(set(tags) & set(nonmol_measure_numbers)):
                    return True
            if _tags.ONLY_MOL in tags:
                if bool(set(tags) & set(nonmol_measure_numbers)):
                    return True
            return False

    else:
        deactivate = None
    return _segments.Job(
        activate=(activate, "MOL"),
        deactivate=(deactivate, "conflicting MOL"),
        path=path,
        title="handling MOL tags ...",
    )


def handle_shifted_clefs(path):
    """
    Handles shifted clefs.
    """

    def activate(tags):
        return _tags.SHIFTED_CLEF in tags

    # then deactivate shifted clefs at BOL:
    if path.name == "_segments":
        metadata_source = path.parent
    else:
        metadata_source = path
    string = "bol_measure_numbers"
    bol_measure_numbers = metadata_source.get_metadatum(string)
    if bol_measure_numbers:
        bol_measure_numbers = [abjad.Tag(f"MEASURE_{_}") for _ in bol_measure_numbers]

        def deactivate(tags):
            if _tags.SHIFTED_CLEF not in tags:
                return False
            if any(_ in tags for _ in bol_measure_numbers):
                return True
            return False

    else:
        deactivate = None
    return _segments.Job(
        activate=(activate, "shifted clef"),
        deactivate=(deactivate, "BOL clef"),
        path=path,
        title="handling shifted clefs ...",
    )


def hide_default_clefs(path, undo=False):
    """
    Hides default clefs.
    """
    name = "default clef"

    def match(tags):
        tags_ = [_tags.DEFAULT_CLEF]
        return bool(set(tags) & set(tags_))

    if undo:
        return _segments.Job(
            activate=(match, name),
            path=path,
            title="showing default clefs ...",
        )
    else:
        return _segments.Job(
            deactivate=(match, name),
            path=path,
            title="hiding default clefs ...",
        )


def join_broken_spanners(path):
    """
    Joins broken spanners.
    """

    def activate(tags):
        tags_ = [_tags.SHOW_TO_JOIN_BROKEN_SPANNERS]
        return bool(set(tags) & set(tags_))

    def deactivate(tags):
        tags_ = [_tags.HIDE_TO_JOIN_BROKEN_SPANNERS]
        return bool(set(tags) & set(tags_))

    return _segments.Job(
        activate=(activate, "broken spanner expression"),
        deactivate=(deactivate, "broken spanner suppression"),
        path=path,
        title="joining broken spanners ...",
    )


def show_music_annotations(path, undo=False):
    """
    Shows music annotations.
    """
    name = "music annotation"

    def match(tags):
        tags_ = _tags.music_annotation_tags()
        return bool(set(tags) & set(tags_))

    def match_2(tags):
        tags_ = [_tags.INVISIBLE_MUSIC_COMMAND]
        return bool(set(tags) & set(tags_))

    if undo:
        return _segments.Job(
            activate=(match_2, name),
            deactivate=(match, name),
            path=path,
            title=f"hiding {name}s ...",
        )
    else:
        return _segments.Job(
            activate=(match, name),
            deactivate=(match_2, name),
            path=path,
            title=f"showing {name}s ...",
        )


def show_tag(
    path,
    tag,
    *,
    match=None,
    prepend_empty_chord=None,
    skip_file_name=None,
    undo=False,
):
    """
    Shows tag.
    """
    if isinstance(tag, str):
        assert match is not None, repr(match)
    else:
        assert isinstance(tag, abjad.Tag), repr(tag)
    name = str(tag)

    if match is None:

        def match(tags):
            tags_ = [tag]
            return bool(set(tags) & set(tags_))

    if undo:
        return _segments.Job(
            deactivate=(match, name),
            path=path,
            prepend_empty_chord=prepend_empty_chord,
            skip_file_name=skip_file_name,
            title=f"hiding {name} tags ...",
        )
    else:
        return _segments.Job(
            activate=(match, name),
            path=path,
            skip_file_name=skip_file_name,
            title=f"showing {name} tags ...",
        )
