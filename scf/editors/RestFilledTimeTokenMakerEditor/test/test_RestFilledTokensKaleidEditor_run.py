import handlers
import scf


def test_RestFilledTimeTokenMakerEditor_run_01():

    editor = scf.editors.RestFilledTimeTokenMakerEditor()
    editor.run(user_input='q', is_autoadvancing=True)

    kaleid = handlers.kaleids.RestFilledTimeTokenMaker()

    assert editor.target == kaleid
