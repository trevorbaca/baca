import kaleids
import scf


def test_RestFilledTokensKaleidEditor_run_01():

    editor = scf.editors.RestFilledTokensKaleidEditor()
    editor.run(user_input='q', is_autoadvancing=True)

    kaleid = kaleids.RestFilledTokens()

    assert editor.target == kaleid
