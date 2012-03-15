from abjad import *
from scf import getters


def test_getters_01():
    '''Regression test.
    '''

    getter = getters.get_duration('foo bar')
    assert getter.run(user_input='asdf (1, 16)') == Duration(1, 16)
