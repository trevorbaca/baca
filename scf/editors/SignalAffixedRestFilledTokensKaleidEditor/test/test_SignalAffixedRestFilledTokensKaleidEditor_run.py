import kaleids
import scf


def test_SignalAffixedRestFilledTokensKaleidEditor_run_01():

    editor = scf.editors.SignalAffixedRestFilledTokensKaleidEditor()
    editor.run(user_input='1 [8] [0, 1] [1] [1] 32 q', is_autoadvancing=True)

    kaleid = kaleids.SignalAffixedRestFilledTokens([8], [0, 1], [1], [1], 32)

    assert editor.target == kaleid
