import baca


def test_Session___repr___01():

    session = baca.scf.Session(test='menu_lines', user_input='foo')
    assert repr(session) == "Session(test='menu_lines', user_input='foo')"
