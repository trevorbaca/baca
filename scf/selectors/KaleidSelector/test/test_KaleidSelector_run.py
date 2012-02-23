import scf


def test_KaleidSelector_run_01():

    selector = scf.selectors.KaleidSelector()

    assert selector.run(user_input='notefilled') == 'NoteFilledTokens'
