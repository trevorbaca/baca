import scf


def test_KaleidClassNameSelector_run_01():

    selector = scf.selectors.KaleidClassNameSelector()

    assert selector.run(user_input='notefilled') == 'NoteFilledTokens'
