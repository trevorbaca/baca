import kaleids
import scf


def test_NoteFilledTokensKaleidEditor_run_01():

    editor = scf.editors.NoteFilledTokensKaleidEditor()
    editor.run(user_input='q', is_autoadvancing=True)

    kaleid = kaleids.NoteFilledTokens()

    assert editor.target == kaleid
