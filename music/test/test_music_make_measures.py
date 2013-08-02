from abjad import *
from baca import music


def test_music_make_measures_01():
    t = Voice([Note(n, (1, 8)) for n in range(8)])
    assert len(t) == 8
    leaves_before = t.select_leaves()
    music.makeMeasures(t, [(n, 8) for n in (2, 2, 2, 2)])
    assert len(t) == 4
    leaves_after = t.select_leaves()
    assert leaves_before == leaves_after
    for x in t:
        assert isinstance(x, Measure)
        assert x.get_duration() == Fraction(2, 8)


def test_music_make_measures_02():
    t = Voice([Note(n, (1, 8)) for n in range(8)])
    assert len(t) == 8
    leaves_before = t.select_leaves()
    music.makeMeasures(t, [(n, 8) for n in (2, 3, 3)])
    assert len(t) == 3
    leaves_after = t.select_leaves()
    assert leaves_before == leaves_after
    for i, x in enumerate(t):
        assert isinstance(x, Measure)
        if i == 0:
            assert x.get_duration() == Fraction(2, 8)
        else:
            assert x.get_duration() == Fraction(3, 8)
