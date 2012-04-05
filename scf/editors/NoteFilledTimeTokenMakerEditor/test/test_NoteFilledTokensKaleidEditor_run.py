import handlers
import scf


def test_NoteFilledTimeTokenMakerEditor_run_01():

    editor = scf.editors.NoteFilledTimeTokenMakerEditor()
    editor.run(user_input='q', is_autoadvancing=True)

    kaleid = handlers.kaleids.NoteFilledTimeTokenMaker()

    assert editor.target == kaleid
