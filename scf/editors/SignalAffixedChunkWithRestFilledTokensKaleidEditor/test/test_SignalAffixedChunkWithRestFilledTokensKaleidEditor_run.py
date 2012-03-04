import kaleids
import scf


def test_SignalAffixedChunkWithRestFilledTokensKaleidEditor_run_01():

    editor = scf.editors.SignalAffixedChunkWithRestFilledTokensKaleidEditor()
    editor.run(user_input='1 [8] [2] [3] [4] 32 q', is_autoadvancing=True)

    kaleid = kaleids.SignalAffixedChunkWithRestFilledTokens([8], [2], [3], [4], 32)

    assert editor.target == kaleid
