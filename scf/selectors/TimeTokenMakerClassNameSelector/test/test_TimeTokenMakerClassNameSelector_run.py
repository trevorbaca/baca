import scf


def test_TimeTokenMakerClassNameSelector_run_01():

    selector = scf.selectors.TimeTokenMakerClassNameSelector()

    assert selector.run(user_input='notefilled') == 'NoteFilledRhythmMaker'
