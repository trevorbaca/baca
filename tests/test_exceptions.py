import abjad
import pytest
import baca

from abjadext import rmakers


def test_exceptions_01():
    """
    Imbrication raises exception on unused pitches.
    """

    collections = [
        [0, 2, 10, 18, 16],
        [15, 20, 19, 9, 0],
    ]
    tuplets = [baca.from_collection(_, [1], 16) for _ in collections]
    voice = abjad.Voice(tuplets)
    groups = rmakers.nongrace_leaves_in_each_tuplet(tuplets)
    rmakers.beam_groups(groups)

    with pytest.raises(Exception):
        baca.imbricate(
            voice,
            "Music.1",
            [2, 19, 9, 18, 16],
            allow_unused_pitches=False,
        )
