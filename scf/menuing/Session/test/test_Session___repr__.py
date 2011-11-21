import baca


def test_Session___repr___01():

    session = baca.scf.menuing.Session(test='menu_lines')
    assert repr(session) == "Session(test='menu_lines')"
