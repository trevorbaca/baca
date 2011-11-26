import baca


def test_Session___init___01():
    '''Attributes assigned at initialization time.
    '''

    session = baca.scf.Session()

    assert session.initial_user_input is None
    assert session.menu_pieces == []
    assert session.scores_to_show == 'active'
    assert session.user_input is None
