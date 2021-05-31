import difflib
import os
import pathlib
import shutil
import sys

import ide
import pytest

import abjad

import baca  # isort:skip

abjad_ide = ide.AbjadIDE()
github_workspace = os.getenv("GITHUB_WORKSPACE")
assert isinstance(github_workspace, str), repr(github_workspace)
wrapper = pathlib.Path(github_workspace)
assert isinstance(wrapper, pathlib.Path), repr(wrapper)
segments = wrapper / wrapper.name / "segments"
segments = baca.Path(segments, scores=wrapper.parent)
assert isinstance(segments, baca.Path), repr(segments)
directories = segments.list_paths()


@pytest.mark.parametrize("directory", directories)
def test_segments(directory):
    # abjad_ide._test_segment_illustration(directory)
    # only run on GitHub because segment illustration usually takes a while
    if not os.getenv("GITHUB_WORKSPACE"):
        return
    abjad_ide = ide.AbjadIDE()
    with abjad.FilesystemState(keep=[directory]):
        ly = directory / "illustration.ly"
        ly_old = directory / "illustration.old.ly"
        if ly.exists():
            shutil.copyfile(ly, ly_old)
        ily = directory / "illustration.ily"
        ily_old = directory / "illustration.old.ily"
        if ily.exists():
            shutil.copyfile(ily, ily_old)
        exit_code = abjad_ide.make_illustration_pdf(directory, open_after=False)
        if exit_code != 0:
            sys.exit(exit_code)
        if not ly_old.exists():
            return
        assert ly.exists()
        assert ly_old.exists()
        if not abjad.io.compare_files(ly_old, ly):
            ly_old_text = ly_old.read_text().splitlines(keepends=True)
            ly_text = ly.read_text().splitlines(keepends=True)
            print("".join(difflib.ndiff(ly_old_text, ly_text)))
            sys.exit(1)
        if not ily_old.exists():
            return
        assert ily.exists()
        assert ily_old.exists()
        if not abjad.io.compare_files(ily_old, ily):
            ily_old_text = ily_old.read_text().splitlines(keepends=True)
            ily_text = ily.read_text().splitlines(keepends=True)
            print("".join(difflib.ndiff(ily_old_text, ily_text)))
            sys.exit(1)
