import handlers
import scf


def test_NoteFilledTimeTokenMakerKaleidEditor_run_01():

    editor = scf.editors.NoteFilledTimeTokenMakerKaleidEditor()
    editor.run(user_input='q', is_autoadvancing=True)

    kaleid = handlers.kaleids.NoteFilledTimeTokenMaker()

    assert editor.target == kaleid
