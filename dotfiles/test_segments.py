import os
import pathlib
import sys

import ide
import pytest

import baca

abjad_ide = ide.AbjadIDE()
travis_build_dir = os.getenv("TRAVIS_BUILD_DIR")
assert isinstance(travis_build_dir, str), repr(travis_build_dir)
wrapper = pathlib.Path(travis_build_dir)
assert isinstance(wrapper, pathlib.Path), repr(wrapper)
segments = wrapper / wrapper.name / "segments"
segments = baca.Path(segments, scores=wrapper.parent)
assert isinstance(segments, baca.Path), repr(segments)
directories = segments.list_paths()


# @pytest.mark.parametrize("directory", directories)
# def test_segments_01(directory):
#    exit_code = abjad_ide.check_definition_py(directory)
#    if exit_code != 0:
#        sys.exit(exit_code)


@pytest.mark.parametrize("directory", directories)
def test_segments_02(directory):
    abjad_ide._test_segment_illustration(directory)
