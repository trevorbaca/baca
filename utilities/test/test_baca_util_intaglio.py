import pytest
from abjad import *
from baca import utilities


def test_baca_util_intaglio_01():
    '''One-element s is allowed.
    '''

    l, s = [3, 5, 10, 10], [4]
    result = utilities.intaglio(l, s)

    assert result == [[3], [1, 4], [4, 4, 2], [2, 4, 4]]
    assert len(l) == len(result)
    assert [mathtools.weight(x) for x in result] == l


def test_baca_util_intaglio_02():

    l, s = [3, 5, 10, 10], [5]
    result = utilities.intaglio(l, s)

    assert result == [[3], [2, 3], [2, 5, 3], [2, 5, 3]]
    assert len(l) == len(result)
    assert [mathtools.weight(x) for x in result] == l


def test_baca_util_intaglio_03():
    '''Multielement s is allowed.
    '''

    l, s = [3, 5, 10, 10], [4, 5]
    result = utilities.intaglio(l, s)

    assert result == [[3], [1, 4], [1, 4, 5], [4, 5, 1]]
    assert len(l) == len(result)
    assert [mathtools.weight(x) for x in result] == l


def test_baca_util_intaglio_04():
    '''s can contain negative values.
    '''

    l, s = [3, 5, 10, 10], [4, -5]
    result = utilities.intaglio(l, s)

    assert result == [[3], [1, -4], [-1, 4, -5], [4, -5, 1]]
    assert len(l) == len(result)
    assert [mathtools.weight(x) for x in result] == l


def test_baca_util_intaglio_05():
    '''l must be nonempty and contain positive integers only.
    '''

    assert pytest.raises(AssertionError, 'utilities.intaglio([], [4])')

    statement = 'utilities.intaglio([-3, 5, 10, 10], [4])'
    assert pytest.raises(AssertionError, statement)

    statement = 'utilities.intaglio([0, 5, 10, 10], [4])'
    assert pytest.raises(AssertionError, statement)

    statement = 'utilities.intaglio([3.2, 5, 10, 10], [4])'
    assert pytest.raises(AssertionError, statement)


def test_baca_util_intaglio_06():
    '''s must be nonempty and contain nonzero integers only.
    '''

    statement = 'utilities.intaglio([3, 5, 10, 10], [])'
    assert pytest.raises(AssertionError, statement)

    statement = 'utilities.intaglio([3, 5, 10, 10], [0])'
    assert pytest.raises(AssertionError, statement)

    statement = 'utilities.intaglio([3, 5, 10, 10], [2.2])'
    assert pytest.raises(AssertionError, statement)
