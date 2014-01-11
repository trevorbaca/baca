from baca import utilities


def test_baca_util_sectionalize_01():

    t = utilities.sectionalize(20, (1, 1, 1))
    assert t == [6, 1, 6, 1, 6]

    t = utilities.sectionalize(97, (1, 1, 1))
    assert t == [32, 1, 31, 1, 32]

    t = utilities.sectionalize(97, (1, 1, 2))
    assert t == [24, 1, 24, 1, 47]
