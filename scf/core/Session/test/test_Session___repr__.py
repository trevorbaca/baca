import baca


def test_Session___repr___01():

    session = baca.scf.core.Session(user_input='foo')
    assert repr(session) == "Session(initial_user_input='foo', user_input='foo')"
