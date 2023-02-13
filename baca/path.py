"""
Path.
"""
import importlib
import os
import pathlib
import types

import black

import abjad

from . import tags as _tags


def _get_previous_section(path: str):
    music_py = pathlib.Path(path)
    section = pathlib.Path(music_py).parent
    assert section.parent.name == "sections", repr(section)
    sections = section.parent
    assert sections.name == "sections", repr(sections)
    paths = list(sorted(sections.glob("*")))
    paths = [_ for _ in paths if not _.name.startswith(".")]
    paths = [_ for _ in paths if _.is_dir()]
    index = paths.index(section)
    if index == 0:
        return {}
    previous_index = index - 1
    previous_section = paths[previous_index]
    return previous_section


def activate(
    path,
    tag,
    *,
    indent=0,
    name=None,
    prepend_empty_chord=None,
    skip_file_name=None,
    undo=False,
):
    """
    Activates ``tag`` in .ily or .ly ``path``.

    Returns triple.

    First item in triple is count of deactivated tags activated by method.

    Second item in pair is count of already-active tags skipped by method.

    Third item in pair is list of string messages that explain what happened.
    """
    assert path.is_file(), repr(path)
    assert path.suffix in (".ily", ".ly")
    if path.name not in ("layout.ly", "music.ily", "music.ly"):
        assert path.name[0].isdigit(), repr(path)
    assert isinstance(indent, int), repr(indent)
    if path.name == skip_file_name:
        triple = (0, 0, [])
        return triple
    if isinstance(tag, str):
        raise Exception(f"must be tag or callable: {tag!r}")
    triples = []
    text = path.read_text()
    if undo:
        text, count, skipped = abjad.deactivate(
            text,
            tag,
            prepend_empty_chord=prepend_empty_chord,
            skipped=True,
        )
    else:
        text, count, skipped = abjad.activate(text, tag, skipped=True)
    path.write_text(text)
    triple = (path, count, skipped)
    triples.append(triple)
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


def add_metadatum(path, name, value) -> None:
    assert " " not in name, repr(name)
    metadata = get_metadata(path)
    dictionary = dict(metadata)
    dictionary[name] = value
    metadata = types.MappingProxyType(dictionary)
    write_metadata_py(path, metadata)


def deactivate(
    path,
    tag,
    *,
    indent=0,
    name=None,
    prepend_empty_chord=None,
    skip_file_name=None,
):
    if isinstance(tag, str):
        raise Exception(f"must be tag or callable: {tag!r}")
    return activate(
        path,
        tag,
        name=name,
        indent=indent,
        prepend_empty_chord=prepend_empty_chord,
        skip_file_name=skip_file_name,
        undo=True,
    )


def extern(
    path,
    include_path,
):
    """
    Externalizes LilyPond file parsable chunks.

    Produces skeleton ``.ly`` together with ``.ily``.

    Overwrites ``path`` with skeleton ``.ly``.

    Writes ``.ily`` to ``include_path``.
    """
    tag = abjad.Tag("baca.path.extern()")
    assert isinstance(include_path, type(path)), repr(include_path)
    preamble_lines, score_lines = [], []
    stack, finished_variables = {}, {}
    found_score = False
    with open(path) as pointer:
        readlines = pointer.readlines()
    for line in readlines:
        if (
            line.startswith(r"\score")
            or line.startswith(r"\context Score")
            or line.startswith("{")
        ):
            found_score = True
        if not found_score:
            preamble_lines.append(line)
        elif " %*% " in line:
            words = line.split()
            index = words.index("%*%")
            name = words[index + 1]
            # first line in expression:
            if name not in stack:
                stack[name] = []
                stack[name].append(line)
            # last line in expression
            else:
                stack[name].append(line)
                finished_variables[name] = stack[name]
                del stack[name]
                count = len(line) - len(line.lstrip())
                indent = count * " "
                dereference = indent + rf"{{ \{name} }}"
                first_line = finished_variables[name][0]
                # TODO: TRY NOW:
                # these 4 lines can be removed after tags on right-side:
                if _tags.NOT_TOPMOST.string in first_line:
                    tag_ = tag.append(_tags.NOT_TOPMOST)
                else:
                    tag_ = tag
                result = abjad.tag.double_tag([dereference], tag_)
                dereference = []
                for tag_line in result[:1]:
                    dereference.append(indent + tag_line)
                dereference.append(result[-1])
                dereference = [_ + "\n" for _ in dereference]
                if bool(stack):
                    items = list(stack.items())
                    items[-1][-1].extend(dereference)
                else:
                    score_lines.extend(dereference)
        elif bool(stack):
            items = list(stack.items())
            items[-1][-1].append(line)
        else:
            score_lines.append(line)
    lines = []
    if include_path.parent == path.parent:
        include_name = include_path.name
    else:
        include_name = str(include_path)
    include_line = f'\\include "{include_name}"'
    include_lines = abjad.tag.double_tag([include_line], tag)
    include_lines = [_ + "\n" for _ in include_lines]
    last_include = 0
    for i, line in enumerate(preamble_lines):
        if line.startswith(r"\include"):
            last_include = i
    preamble_lines[last_include + 1 : last_include + 1] = include_lines
    if preamble_lines[-2] == "\n":
        del preamble_lines[-2]
    lines.extend(preamble_lines)
    lines.extend(score_lines)
    lines_ = []
    for line in lines:
        lines_.append(line)
    text = "".join(lines_)
    path.write_text(text)
    lines = []
    items = list(finished_variables.items())
    total = len(items)
    for i, item in enumerate(items):
        name, variable_lines = item
        first_line = variable_lines[0]
        count = len(first_line) - len(first_line.lstrip())
        first_line = first_line[count:]
        first_line = f"{name} = {first_line}"
        words = first_line.split()
        index = words.index("%*%")
        first_line = " ".join(words[:index])
        first_lines = abjad.tag.double_tag([first_line], tag)
        first_lines = [_ + "\n" for _ in first_lines]
        lines.extend(first_lines)
        for variable_line in variable_lines[1:]:
            assert variable_line[:count].isspace(), repr(line)
            variable_line = variable_line[count:]
            if variable_line == "":
                variable_line = "\n"
            assert variable_line.endswith("\n"), repr(variable_line)
            lines.append(variable_line)
        not_topmost_index = None
        for j, line in enumerate(reversed(lines)):
            if line.strip() == f"%! {_tags.NOT_TOPMOST.string}":
                not_topmost_index = j
                break
            if line.isspace():
                break
        if not_topmost_index is not None:
            assert 0 < not_topmost_index
            index = -(not_topmost_index + 1)
            del lines[index]
        last_line = lines[-1]
        assert last_line.startswith("} ") or last_line.startswith(">> ")
        words = last_line.split()
        index = words.index("%*%")
        last_line = " ".join(words[:index])
        last_lines = abjad.tag.double_tag([last_line], tag)
        last_lines = [_ + "\n" for _ in last_lines]
        lines[-1:] = last_lines
        if i < total - 1:
            lines.append("\n")
            lines.append("\n")
    text = "".join(lines)
    include_path.write_text(text)


def get_contents_directory(path):
    wrapper_directory = get_wrapper_directory(path)
    contents_directory = wrapper_directory / wrapper_directory.name
    return contents_directory


def get_wrapper_directory(path):
    parts = str(path).split(os.sep)
    while parts:
        string = os.sep.join(parts)
        candidate = pathlib.Path(string)
        _git = candidate / ".git"
        if _git.is_dir():
            return candidate
        parts.pop()
    raise Exception(path)


def get_measure_profile_metadata(path) -> tuple[int, int, list]:
    """
    Gets measure profile metadata.

    Reads section metadata when path is section.

    Reads score metadata when path is not section.

    Returns tuple of three metadata: first measure number; measure count; list of fermata
    measure numbers.
    """
    if path.parent.parent.name == "sections":
        string = "first_measure_number"
        first_measure_number = get_metadatum(path.parent, string)
        time_signatures = get_metadatum(path.parent, "time_signatures")
        if bool(time_signatures):
            measure_count = len(time_signatures)
        else:
            measure_count = 0
        string = "fermata_measure_numbers"
        fermata_measure_numbers = get_metadatum(path.parent, string)
    else:
        first_measure_number = 1
        measure_count = 0
        fermata_measure_numbers = []
        contents_directory = get_contents_directory(path)
        sections_directory = contents_directory / "sections"
        section_directories = list(sorted(sections_directory.glob("*")))
        for section_directory in section_directories:
            if not section_directory.is_dir():
                continue
            time_signatures = get_metadatum(section_directory, "time_signatures")
            measure_count += len(time_signatures)
            fermata_measure_numbers_ = get_metadatum(
                section_directory,
                "fermata_measure_numbers",
                [],
            )
            fermata_measure_numbers.extend(fermata_measure_numbers_)
    return (first_measure_number, measure_count, fermata_measure_numbers)


def get_metadata(directory) -> types.MappingProxyType:
    assert directory.is_dir(), repr(directory)
    metadata_py_path = directory / ".metadata"
    dictionary = {}
    if metadata_py_path.is_file():
        file_contents_string = metadata_py_path.read_text()
        baca = importlib.import_module("baca")
        namespace = {"abjad": abjad, "baca": baca}
        namespace.update(abjad.__dict__)
        namespace.update(baca.__dict__)
        dictionary = eval(file_contents_string, namespace)
    metadata = types.MappingProxyType(dictionary)
    return metadata


# TODO: remove in favor of metadata.get()
def get_metadatum(
    path,
    metadatum_name,
    default=None,
):
    metadata = get_metadata(path)
    metadatum = metadata.get(metadatum_name, default)
    return metadatum


def previous_metadata(path: str) -> types.MappingProxyType:
    previous_section = _get_previous_section(path)
    if previous_section:
        previous_metadata = get_metadata(previous_section)
    else:
        previous_metadata = types.MappingProxyType({})
    return previous_metadata


def remove_metadatum(path, name):
    assert " " not in name, repr(name)
    metadata = get_metadata(path)
    if name in metadata:
        dictionary = dict(metadata)
        dictionary.pop(name)
        metadata = types.MappingProxyType(dictionary)
    write_metadata_py(path, metadata)


def trim(path):
    wrapper_directory = get_wrapper_directory(path)
    count = len(wrapper_directory.parts)
    parts = path.parts
    parts = parts[count:]
    path = pathlib.Path(*parts)
    if str(path) == ".":
        return str(path)
    return str(path)


def write_metadata_py(path, metadata):
    assert isinstance(metadata, types.MappingProxyType), repr(metadata)
    metadata = types.MappingProxyType(dict(sorted(metadata.items())))
    string = str(metadata)
    string = black.format_str(string, mode=black.mode.Mode())
    metadata_py_path = path / ".metadata"
    metadata_py_path.write_text(string)
