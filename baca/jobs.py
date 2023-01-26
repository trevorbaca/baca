"""
Jobs.
"""
import pathlib
import typing

import abjad

from . import path as _path
from . import tags as _tags


def _run_job(
    *,
    activate: typing.Any = None,
    deactivate: typing.Any = None,
    deactivate_first: typing.Any = None,
    path: typing.Any = None,
    prepend_empty_chord: typing.Any = None,
    skip_file_name: typing.Any = None,
    title: typing.Any = None,
    undo: bool = False,
):
    if undo is True:
        assert activate is not None
        assert deactivate is None
        deactivate = activate
        activate = None
        title = "Un" + title[0].lower() + title[1:]
    assert isinstance(path, pathlib.Path), repr(path)
    messages = []
    if title is not None:
        messages.append(title)
    total_count = 0
    if deactivate_first is True:
        if deactivate is not None:
            assert isinstance(deactivate, tuple)
            match, name = deactivate
            if match is not None:
                result = _path.deactivate(
                    path,
                    match,
                    name=name,
                    prepend_empty_chord=prepend_empty_chord,
                    skip_file_name=skip_file_name,
                )
                assert result is not None
                count, skipped, messages_ = result
                messages.extend(messages_)
                total_count += count
    if activate is not None:
        assert isinstance(activate, tuple)
        match, name = activate
        if match is not None:
            result = _path.activate(
                path,
                match,
                name=name,
                skip_file_name=skip_file_name,
            )
            assert result is not None
            count, skipped, messages_ = result
            messages.extend(messages_)
            total_count += count
    if deactivate_first is not True:
        if deactivate is not None:
            assert isinstance(deactivate, tuple)
            match, name = deactivate
            if match is not None:
                result = _path.deactivate(
                    path,
                    match,
                    name=name,
                    prepend_empty_chord=prepend_empty_chord,
                    skip_file_name=skip_file_name,
                )
                assert result is not None
                count, skipped, messages_ = result
                messages.extend(messages_)
                total_count += count
    messages.append("")
    return messages


def color_clefs(path, *, undo=False):
    name = "clef color"

    def match(tags):
        build = "builds" in path.parts
        tags_ = _tags.clef_color_tags(build=build)
        return bool(set(tags) & set(tags_))

    messages = _run_job(
        activate=(match, name),
        path=path,
        title="Coloring clefs ...",
        undo=undo,
    )
    return messages


def color_dynamics(path, *, undo=False):
    name = "dynamic color"

    def match(tags):
        tags_ = _tags.dynamic_color_tags()
        return bool(set(tags) & set(tags_))

    messages = _run_job(
        activate=(match, name),
        path=path,
        title="Coloring dynamics ...",
        undo=undo,
    )
    return messages


def color_instruments(path, *, undo=False):
    name = "instrument color"

    def match(tags):
        tags_ = _tags.instrument_color_tags()
        return bool(set(tags) & set(tags_))

    messages = _run_job(
        activate=(match, name),
        path=path,
        title="Coloring instruments ...",
        undo=undo,
    )
    return messages


def color_short_instrument_names(path, *, undo=False):
    name = "short instrument name color"

    def match(tags):
        tags_ = _tags.short_instrument_name_color_tags()
        return bool(set(tags) & set(tags_))

    messages = _run_job(
        activate=(match, name),
        path=path,
        title="Coloring short instrument names ...",
        undo=undo,
    )
    return messages


def color_metronome_marks(path, undo=False):
    def activate(tags):
        tags_ = _tags.metronome_mark_color_expression_tags()
        return bool(set(tags) & set(tags_))

    def deactivate(tags):
        tags_ = _tags.metronome_mark_color_suppression_tags()
        return bool(set(tags) & set(tags_))

    if undo:
        messages = _run_job(
            activate=(deactivate, "metronome mark color suppression"),
            deactivate=(activate, "metronome mark color expression"),
            path=path,
            title="Uncoloring metronome marks ...",
        )
    else:
        messages = _run_job(
            activate=(activate, "metronome mark color expression"),
            deactivate=(deactivate, "metronome mark color suppression"),
            path=path,
            title="Coloring metronome marks ...",
        )
    return messages


def color_persistent_indicators(path, *, undo=False):
    name = "persistent indicator"
    activate_name = "persistent indicator color expression"

    def activate(tags):
        build = "builds" in path.parts
        tags_ = _tags.persistent_indicator_color_expression_tags(build=build)
        return bool(set(tags) & set(tags_))

    deactivate_name = "persistent indicator color suppression"

    def deactivate(tags):
        tags_ = _tags.persistent_indicator_color_suppression_tags()
        return bool(set(tags) & set(tags_))

    if undo:
        messages = _run_job(
            activate=(deactivate, deactivate_name),
            deactivate=(activate, activate_name),
            path=path,
            title=f"Uncoloring {name}s ...",
        )
    else:
        messages = _run_job(
            activate=(activate, activate_name),
            deactivate=(deactivate, deactivate_name),
            path=path,
            title=f"Coloring {name}s ...",
        )
    return messages


def color_staff_lines(path, *, undo=False):
    name = "staff lines color"

    def match(tags):
        build = "builds" in path.parts
        tags_ = _tags.staff_lines_color_tags(build=build)
        return bool(set(tags) & set(tags_))

    messages = _run_job(
        activate=(match, name),
        path=path,
        title="Coloring staff lines ...",
        undo=undo,
    )
    return messages


def color_time_signatures(path, *, undo=False):
    name = "time signature color"

    def match(tags):
        build = "builds" in path.parts
        tags_ = _tags.time_signature_color_tags(build=build)
        return bool(set(tags) & set(tags_))

    messages = _run_job(
        activate=(match, name),
        path=path,
        title="Coloring time signatures ...",
        undo=undo,
    )
    return messages


def handle_edition_tags(path):
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
    if "sections" in str(path):
        my_name = "SECTION"
    elif "-score" in str(path):
        my_name = "SCORE"
    elif "-parts" in str(path):
        my_name = "PARTS"
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

    def activate(tags):
        for tag in tags:
            if tag in [not_this_edition, not_this_directory]:
                return False
        for tag in tags:
            if tag.string.startswith("-"):
                return True
        return bool(set(tags) & set([this_edition, this_directory]))

    messages = _run_job(
        activate=(activate, "this-edition"),
        deactivate=(deactivate, "other-edition"),
        deactivate_first=True,
        path=path,
        title="Handling edition tags ...",
    )
    return messages


def handle_fermata_bar_lines(path):
    """
    Handles fermata bar lines.
    """
    if path.name == "_sections":
        path = path.parent

    def activate(tags):
        return bool(set(tags) & set([_tags.FERMATA_MEASURE]))

    # then deactivate non-EOL tags:
    if path.is_dir():
        metadata_source = path
    else:
        metadata_source = path.parent
    bol_measure_numbers = _path.get_metadatum(metadata_source, "bol_measure_numbers")
    if bol_measure_numbers:
        eol_measure_numbers = [_ - 1 for _ in bol_measure_numbers[1:]]
        final_measure_number = _path.get_metadatum(
            metadata_source, "final_measure_number"
        )
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
    messages = _run_job(
        activate=(activate, "bar line adjustment"),
        deactivate=(deactivate, "EOL fermata bar line"),
        path=path,
        title="Handling fermata bar lines ...",
    )
    return messages


def handle_mol_tags(path):
    if path.name == "_sections":
        path = path.parent

    # activate all middle-of-line tags
    def activate(tags):
        tags_ = set([_tags.NOT_MOL, _tags.ONLY_MOL])
        return bool(set(tags) & tags_)

    # then deactivate conflicting middle-of-line tags
    if path.is_dir():
        metadata_source = path
    else:
        metadata_source = path.parent
    bol_measure_numbers = _path.get_metadatum(metadata_source, "bol_measure_numbers")
    if bol_measure_numbers:
        nonmol_measure_numbers = bol_measure_numbers[:]
        final_measure_number = _path.get_metadatum(
            metadata_source, "final_measure_number"
        )
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
    messages = _run_job(
        activate=(activate, "MOL"),
        deactivate=(deactivate, "conflicting MOL"),
        path=path,
        title="Handling MOL tags ...",
    )
    return messages


def handle_shifted_clefs(path):
    def activate(tags):
        return _tags.SHIFTED_CLEF in tags

    # then deactivate shifted clefs at BOL:
    if path.name == "_sections":
        metadata_source = path.parent
    elif path.is_dir():
        metadata_source = path
    else:
        metadata_source = path.parent
    string = "bol_measure_numbers"
    bol_measure_numbers = _path.get_metadatum(metadata_source, string)
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
    messages = _run_job(
        activate=(activate, "shifted clef"),
        deactivate=(deactivate, "BOL clef"),
        path=path,
        title="Handling shifted clefs ...",
    )
    return messages


def join_broken_spanners(path):
    def activate(tags):
        tags_ = [_tags.SHOW_TO_JOIN_BROKEN_SPANNERS]
        return bool(set(tags) & set(tags_))

    def deactivate(tags):
        tags_ = [_tags.HIDE_TO_JOIN_BROKEN_SPANNERS]
        return bool(set(tags) & set(tags_))

    messages = _run_job(
        activate=(activate, "broken spanner expression"),
        deactivate=(deactivate, "broken spanner suppression"),
        path=path,
        title="Joining broken spanners ...",
    )
    return messages


def not_topmost(path):
    messages = _run_job(
        deactivate=(_tags.NOT_TOPMOST, "not topmost"),
        path=path,
        title=f"Deactivating {_tags.NOT_TOPMOST.string} ...",
    )
    return messages


def show_music_annotations(path, *, undo=False):
    name = "music annotation"

    def match(tags):
        tags_ = _tags.music_annotation_tags()
        return bool(set(tags) & set(tags_))

    def match_2(tags):
        tags_ = [_tags.INVISIBLE_MUSIC_COMMAND]
        return bool(set(tags) & set(tags_))

    if undo:
        messages = _run_job(
            activate=(match_2, name),
            deactivate=(match, name),
            path=path,
            title=f"Hiding {name}s ...",
        )
    else:
        messages = _run_job(
            activate=(match, name),
            deactivate=(match_2, name),
            path=path,
            title=f"Showing {name}s ...",
        )
    return messages


def show_tag(
    path,
    tag,
    *,
    match=None,
    prepend_empty_chord=None,
    skip_file_name=None,
    undo=False,
):
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

    if undo:
        messages = _run_job(
            deactivate=(match, name),
            path=path,
            prepend_empty_chord=prepend_empty_chord,
            skip_file_name=skip_file_name,
            title=f"Hiding {name} tags ...",
        )
    else:
        messages = _run_job(
            activate=(match, name),
            path=path,
            skip_file_name=skip_file_name,
            title=f"Showing {name} tags ...",
        )
    return messages
