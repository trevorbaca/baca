import pytest

import abjad
import baca
from abjadext import rmakers


@pytest.fixture(autouse=True)
def add_libraries(doctest_namespace):
    doctest_namespace["abjad"] = abjad
    doctest_namespace["baca"] = baca
    doctest_namespace["f"] = abjad.f
    doctest_namespace["rmakers"] = rmakers
    doctest_namespace["Infinity"] = abjad.mathtools.Infinity()
    doctest_namespace["NegativeInfinity"] = abjad.mathtools.NegativeInfinity()
