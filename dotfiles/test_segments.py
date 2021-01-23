import os
import pathlib

import ide
import pytest

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
    abjad_ide._test_segment_illustration(directory)
