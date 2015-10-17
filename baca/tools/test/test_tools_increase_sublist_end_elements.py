from baca import tools


def test_tools_increase_sublist_end_elements_01():

    l = [[2, 2, 2, 2], [2, 2], [2, 2, 2]]
    t = tools.increase_sublist_end_elements(l, [1, 5, 10])

    assert t == [[12, 2, 2, 7], [3, 12], [7, 2, 3]]
