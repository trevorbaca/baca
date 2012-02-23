import scf


def test_Session_properties_01():

    session = scf.core.Session()

    assert     session.is_displayable
    assert     session.menu_header == ''
    assert not session.is_complete
    assert not session.session_once_had_user_input
    assert     session.user_input is None
    assert not session.user_input_is_consumed
    assert not session.user_specified_quit
