import handlers
import scf


def test_TokenIncisedRestFilledTimeTokenMakerEditor_run_01():

    editor = scf.editors.TokenIncisedRestFilledTimeTokenMakerEditor()
    editor.run(user_input='1 [8] [0, 1] [1] [1] 32 q', is_autoadvancing=True)

    kaleid = handlers.kaleids.TokenIncisedRestFilledTimeTokenMaker([8], [0, 1], [1], [1], 32)

    assert editor.target == kaleid
