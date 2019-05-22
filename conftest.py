import abjad
import baca
import pytest
from abjadext import rmakers


@pytest.fixture(autouse=True)
def add_baca(doctest_namespace):
    doctest_namespace["baca"] = baca


@pytest.fixture(autouse=True)
def add_libraries(doctest_namespace):
    doctest_namespace["abjad"] = abjad
    doctest_namespace["f"] = abjad.f
    doctest_namespace["Infinity"] = abjad.mathtools.Infinity()
    doctest_namespace["NegativeInfinity"] = abjad.mathtools.NegativeInfinity()


@pytest.fixture(autouse=True)
def add_rmakers(doctest_namespace):
    doctest_namespace["rmakers"] = rmakers
