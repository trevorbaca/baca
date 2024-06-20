"""
Path.
"""

import importlib
import os
import pathlib
import types
from inspect import currentframe as _frame

import black

import abjad

from . import helpers as _helpers
from . import tags as _tags


def _get_previous_section(path: pathlib.Path):
    assert isinstance(path, pathlib.Path), repr(path)
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


def add_metadatum(path: pathlib.Path, name: str, value) -> None:
    assert isinstance(path, pathlib.Path), repr(path)
    assert " " not in name, repr(name)
    metadata = get_metadata(path)
    dictionary = dict(metadata)
    dictionary[name] = value
    metadata = types.MappingProxyType(dictionary)
    write_metadata_py(path, metadata)


def externalize(
    path: pathlib.Path,
    *,
    do_not_tag: bool = False,
    file_name: str | None = None,
    in_place: bool = False,
) -> pathlib.Path | None:
    assert isinstance(path, pathlib.Path), repr(path)
    if in_place is True:
        assert file_name is None, repr(file_name)
        path_ily = None
    elif file_name is None:
        path_ily = path.with_suffix(".ily")
    else:
        path_ily = path.with_name(file_name)
    if path_ily is not None:
        assert path_ily.suffix == ".ily", repr(path_ily)
    tag = _helpers.function_name(_frame())
    preamble_lines: list[str] = []
    score_lines: list[str] = []
    stack: dict[str, list[str]] = {}
    finished_variables = {}
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
                dereference_string = indent + rf"{{ \{name} }}"
                first_line = finished_variables[name][0]
                if do_not_tag is False:
                    result = abjad.tag.double_tag([dereference_string], tag)
                    dereference = []
                    for tag_line in result[:1]:
                        dereference.append(indent + tag_line)
                    dereference.append(result[-1])
                else:
                    dereference = [dereference_string]
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
    if in_place is False:
        assert path_ily is not None
        if path_ily.parent == path.parent:
            include_name = path_ily.name
        else:
            include_name = str(path_ily)
        include_line = f'\\include "{include_name}"'
        if do_not_tag is False:
            include_lines = abjad.tag.double_tag([include_line], tag)
        else:
            include_lines = [include_line]
        include_lines = [_ + "\n" for _ in include_lines]
        last_include = 0
        for i, line in enumerate(preamble_lines):
            if line.startswith(r"\include"):
                last_include = i
        preamble_lines[last_include + 1 : last_include + 1] = include_lines
    if preamble_lines[-2] == "\n":
        del preamble_lines[-2]
    lines = []
    lines.extend(preamble_lines)
    lines.extend(score_lines)
    lines_ = []
    for line in lines:
        lines_.append(line)
    text = "".join(lines_)
    path.write_text(text)
    lines = []
    if in_place is False:
        string = abjad.Configuration().get_lilypond_version_string()
        string = rf'\version "{string}"'
        lines.append(string + "\n")
        lines.append("\n")
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
        if do_not_tag is False:
            first_lines = abjad.tag.double_tag([first_line], tag)
        else:
            first_lines = [first_line]
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
        if do_not_tag is False:
            last_lines = abjad.tag.double_tag([last_line], tag)
        else:
            last_lines = [last_line]
        last_lines = [_ + "\n" for _ in last_lines]
        lines[-1:] = last_lines
        if i < total - 1:
            lines.append("\n")
            lines.append("\n")
    if in_place is False:
        assert path_ily is not None
        text = "".join(lines)
        path_ily.write_text(text)
        return path_ily
    else:
        assert "context Score" in score_lines[0]
        score_lines[0] = "page-layout-score = " + score_lines[0]
        lines_ = preamble_lines + lines + ["\n\n"] + score_lines
        text = "".join(lines_)
        path.write_text(text)
        return None


def get_contents_directory(path: pathlib.Path):
    assert isinstance(path, pathlib.Path), repr(path)
    wrapper_directory = get_wrapper_directory(path)
    contents_directory = wrapper_directory / wrapper_directory.name
    return contents_directory


def get_sections_directory(directory_string: str):
    directory_path = pathlib.Path(directory_string)
    contents_directory = get_contents_directory(directory_path)
    sections_directory = contents_directory / "sections"
    return sections_directory


def get_wrapper_directory(path: pathlib.Path):
    assert isinstance(path, pathlib.Path), repr(path)
    parts = str(path).split(os.sep)
    while parts:
        string = os.sep.join(parts)
        candidate = pathlib.Path(string)
        _git = candidate / ".git"
        if _git.is_dir():
            return candidate
        parts.pop()
    raise Exception(path)


def get_metadata(directory: pathlib.Path) -> types.MappingProxyType:
    assert isinstance(directory, pathlib.Path), repr(directory)
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


def previous_metadata(path: pathlib.Path) -> types.MappingProxyType:
    assert isinstance(path, pathlib.Path), repr(path)
    previous_section = _get_previous_section(path)
    if previous_section:
        previous_metadata = get_metadata(previous_section)
    else:
        previous_metadata = types.MappingProxyType({})
    return previous_metadata


def remove_metadatum(path: pathlib.Path, name: str):
    assert isinstance(path, pathlib.Path), repr(path)
    assert " " not in name, repr(name)
    metadata = get_metadata(path)
    if name in metadata:
        dictionary = dict(metadata)
        dictionary.pop(name)
        metadata = types.MappingProxyType(dictionary)
    write_metadata_py(path, metadata)


def trim(path: pathlib.Path):
    assert isinstance(path, pathlib.Path), repr(path)
    wrapper_directory = get_wrapper_directory(path)
    count = len(wrapper_directory.parts)
    parts = path.parts
    parts = parts[count:]
    path = pathlib.Path(*parts)
    if str(path) == ".":
        return str(path)
    return str(path)


def write_metadata_py(path: pathlib.Path, metadata: types.MappingProxyType):
    assert isinstance(path, pathlib.Path), repr(path)
    assert isinstance(metadata, types.MappingProxyType), repr(metadata)
    metadata = types.MappingProxyType(dict(sorted(metadata.items())))
    string = str(metadata)
    string = black.format_str(string, mode=black.mode.Mode())
    metadata_py_path = path / ".metadata"
    metadata_py_path.write_text(string)
