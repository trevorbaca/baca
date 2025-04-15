"""
Path.
"""

import importlib
import os
import pathlib
import types

import abjad
import black


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


def get_contents_directory(path: pathlib.Path):
    assert isinstance(path, pathlib.Path), repr(path)
    wrapper_directory = get_wrapper_directory(path)
    contents_directory = wrapper_directory / "source" / wrapper_directory.name
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
    try:
        wrapper_directory = get_wrapper_directory(path)
    except Exception:
        wrapper_directory = None
    if wrapper_directory is not None:
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
