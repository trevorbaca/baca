import pytest

import baca


def test_parts_01():
    """
    baca.assign_part() raises exception when voice does not allow part assignment.
    """

    score = baca.docs.make_empty_score(1)
    time_signatures = baca.section.wrap([(4, 8), (3, 8), (4, 8), (3, 8)])
    music = baca.make_notes(time_signatures())
    score["Music"].extend(music)
    voice = score["Music"]
    with pytest.raises(Exception) as e:
        baca.assign_part(voice, baca.parts.PartAssignment("Flute.Music"))
    assert "Music does not allow Flute.Music part assignment:" in str(e)
