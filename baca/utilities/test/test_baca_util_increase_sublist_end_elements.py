from baca import utilities


def test_baca_util_increase_sublist_end_elements_01():

    l = [[2, 2, 2, 2], [2, 2], [2, 2, 2]]
    t = utilities.increase_sublist_end_elements(l, [1, 5, 10])

    assert t == [[12, 2, 2, 7], [3, 12], [7, 2, 3]]
