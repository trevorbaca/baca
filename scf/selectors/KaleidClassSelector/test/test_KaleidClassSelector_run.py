import scf


def test_KaleidClassSelector_run_01():

    selector = scf.selectors.KaleidClassSelector()

    assert selector.run(user_input='notefilled') == 'NoteFilledTokens'
