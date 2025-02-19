import abjad
import baca
import pytest
import rmakers


@pytest.fixture(autouse=True)
def add_libraries(doctest_namespace):
    doctest_namespace["abjad"] = abjad
    doctest_namespace["baca"] = baca
    doctest_namespace["rmakers"] = rmakers
