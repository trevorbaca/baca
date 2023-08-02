"""
Jobs.
"""
import os
import pathlib
import typing

import abjad

from . import path as _path
from . import tags as _tags


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
        tags_ = _tags.clef_color_tags(build=build)
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
        tags_ = _tags.dynamic_color_tags()
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
        tags_ = _tags.instrument_color_tags()
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
        tags_ = _tags.short_instrument_name_color_tags()
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
        tags_ = _tags.metronome_mark_color_expression_tags()
        return bool(set(tags) & set(tags_))

    def deactivate(tags):
        tags_ = _tags.metronome_mark_color_suppression_tags()
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
        tags_ = _tags.persistent_indicator_color_expression_tags(build=build)
        return bool(set(tags) & set(tags_))

    def deactivate(tags):
        tags_ = _tags.persistent_indicator_color_suppression_tags()
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
        tags_ = _tags.staff_lines_color_tags(build=build)
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
        tags_ = _tags.time_signature_color_tags(build=build)
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


def handle_fermata_bar_lines(path: pathlib.Path) -> list[str]:
    """
    Handles fermata bar lines.
    """
    assert isinstance(path, pathlib.Path)
    messages = ["Handling fermata bar lines ..."]
    if path.name == "_sections":
        path = path.parent

    def activate(tags):
        return bool(set(tags) & set([_tags.FERMATA_MEASURE]))

    # activate fermata measure bar line adjustment tags ...
    _, _, messages_ = _activate(path, activate, name="bar line adjustment")
    messages.extend(messages_)
    # ... then deactivate non-EOL tags
    if path.is_dir():
        metadata_source = path
    else:
        metadata_source = path.parent
    bol_measure_numbers = _path.get_metadata(metadata_source).get("bol_measure_numbers")
    if bol_measure_numbers:
        eol_measure_numbers = [_ - 1 for _ in bol_measure_numbers[1:]]
        final_measure_number = _path.get_metadata(metadata_source).get(
            "final_measure_number"
        )
        if final_measure_number is not None:
            eol_measure_numbers.append(final_measure_number)
        eol_measure_numbers = [abjad.Tag(f"MEASURE_{_}") for _ in eol_measure_numbers]

        def deactivate(tags):
            if _tags.FERMATA_MEASURE in tags:
                if not bool(set(tags) & set(eol_measure_numbers)):
                    return True
            return False

        _, _, messages_ = _deactivate(path, deactivate, name="EOL fermata bar line")
        messages.extend(messages_)
    messages.append("")
    return messages


def handle_mol_tags(path: pathlib.Path) -> list[str]:
    assert isinstance(path, pathlib.Path)
    messages = ["Handling MOL tags ..."]
    if path.name == "_sections":
        path = path.parent

    # activate all middle-of-line tags ...
    def activate(tags):
        tags_ = set([_tags.NOT_MOL, _tags.ONLY_MOL])
        return bool(set(tags) & tags_)

    _, _, messages_ = _activate(path, activate, name="MOL")
    messages.extend(messages_)
    # ... then deactivate conflicting middle-of-line tags
    if path.is_dir():
        metadata_source = path
    else:
        metadata_source = path.parent
    bol_measure_numbers = _path.get_metadata(metadata_source).get("bol_measure_numbers")
    if bol_measure_numbers:
        nonmol_measure_numbers = bol_measure_numbers[:]
        final_measure_number = _path.get_metadata(metadata_source).get(
            "final_measure_number"
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

        _, _, messages_ = _deactivate(path, deactivate, name="conflicting MOL")
        messages.extend(messages_)
    messages.append("")
    return messages


def handle_shifted_clefs(path: pathlib.Path) -> list[str]:
    assert isinstance(path, pathlib.Path)
    messages = ["Handling shifted clefs ..."]

    def activate(tags):
        return _tags.SHIFTED_CLEF in tags

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
    string = "bol_measure_numbers"
    bol_measure_numbers = _path.get_metadata(metadata_source).get(string)
    if not bol_measure_numbers:
        print("WARNING: no BOL metadata found!")
        print(metadata_source)
    if bol_measure_numbers:
        bol_measure_numbers = [abjad.Tag(f"MEASURE_{_}") for _ in bol_measure_numbers]

        def deactivate(tags):
            if _tags.SHIFTED_CLEF not in tags:
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
        tags_ = [_tags.SHOW_TO_JOIN_BROKEN_SPANNERS]
        return bool(set(tags) & set(tags_))

    def deactivate(tags):
        tags_ = [_tags.HIDE_TO_JOIN_BROKEN_SPANNERS]
        return bool(set(tags) & set(tags_))

    _, _, messages_ = _activate(path, activate, name="broken spanner expression")
    messages.extend(messages_)
    _, _, messages_ = _deactivate(path, deactivate, name="broken spanner suppression")
    messages.extend(messages_)
    messages.append("")
    return messages


def not_topmost(path: pathlib.Path) -> list[str]:
    assert isinstance(path, pathlib.Path)
    messages = [f"Deactivating {_tags.NOT_TOPMOST.string} ..."]
    count, skipped, messages_ = _deactivate(
        path,
        _tags.NOT_TOPMOST,
        name="not topmost",
    )
    messages.extend(messages_)
    messages.append("")
    return messages


def show_music_annotations(path: pathlib.Path, *, undo: bool = False) -> list[str]:
    assert isinstance(path, pathlib.Path)
    messages, name = [], "music annotation"

    def match(tags):
        tags_ = _tags.music_annotation_tags()
        return bool(set(tags) & set(tags_))

    def match_2(tags):
        tags_ = [_tags.INVISIBLE_MUSIC_COMMAND]
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
