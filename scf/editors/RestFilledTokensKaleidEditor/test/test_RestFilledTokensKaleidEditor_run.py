import handlers
import scf


def test_RestFilledTimeTokenMakerKaleidEditor_run_01():

    editor = scf.editors.RestFilledTimeTokenMakerKaleidEditor()
    editor.run(user_input='q', is_autoadvancing=True)

    kaleid = handlers.kaleids.RestFilledTimeTokenMaker()

    assert editor.target == kaleid
