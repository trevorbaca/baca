from baca import utilities


def test_baca_util_replace_nested_elements_with_unary_subruns_01():

    l = [[1, 3, -4], [1, 2, -2, -4]]
    t = utilities.replace_nested_elements_with_unary_subruns(l)

    assert t == [[1, 1, 1, 1, -4], [1, 1, 1, -2, -4]]


def test_baca_util_replace_nested_elements_with_unary_subruns_02():

    l = [[1, -2, 3], [-4, 5]]
    t = utilities.replace_nested_elements_with_unary_subruns(l)

    assert t == [[1, -2, 1, 1, 1], [-4, 1, 1, 1, 1, 1]]
