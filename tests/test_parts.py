import baca
import pytest


def test_parts_01():
    """
    baca.assign_part() raises exception when voice does not allow part assignment.
    """

    score = baca.docs.make_empty_score(1)
    time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    baca.section.set_up_score(score, time_signatures(), docs=True)
    music = baca.make_notes(time_signatures())
    score["Music"].extend(music)
    voice = score["Music"]
    with pytest.raises(Exception):
        baca.assign_part(voice, baca.parts.PartAssignment("Flute.Music"))
