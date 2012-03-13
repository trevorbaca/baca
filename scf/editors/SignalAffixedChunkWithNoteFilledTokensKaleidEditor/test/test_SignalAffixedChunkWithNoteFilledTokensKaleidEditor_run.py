import handlers
import scf


def test_SignalAffixedChunkWithNoteFilledTokensKaleidEditor_run_01():

    editor = scf.editors.SignalAffixedChunkWithNoteFilledTokensKaleidEditor()
    editor.run(user_input='1 [-8] [2] [-3] [4] 32 q', is_autoadvancing=True)

    kaleid = handlers.kaleids.SignalAffixedChunkWithNoteFilledTokens([-8], [2], [-3], [4], 32)

    assert editor.target == kaleid
