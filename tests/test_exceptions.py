import abjad
import pytest
import baca

from abjadext import rmakers


def test_exceptions_01():
    """
    Cursor raises exception when exhausted.
    """

    source = [13, "da capo", abjad.Note("cs'8."), "rit."]
    cursor = baca.Cursor(source=source)
    with pytest.raises(Exception):
        cursor.next(count=99)


def test_exceptions_02():
    """
    Imbrication raises exception on unused pitches.
    """

    collections = [
        [0, 2, 10, 18, 16],
        [15, 20, 19, 9, 0],
    ]
    containers = [baca.container_from_collection(_, [1], 16) for _ in collections]
    container = abjad.Container(containers)
    groups = rmakers.nongrace_leaves_in_each_tuplet(containers)
    rmakers.beam_groups(groups)

    with pytest.raises(Exception):
        baca.imbricate(
            container,
            "Music.1",
            [2, 19, 9, 18, 16],
            allow_unused_pitches=False,
        )
