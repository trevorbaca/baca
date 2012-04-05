from abjad.tools import timetokentools
import scf


def test_RestFilledTimeTokenMakerEditor_run_01():

    editor = scf.editors.RestFilledTimeTokenMakerEditor()
    editor.run(user_input='q', is_autoadvancing=True)

    maker = timetokentools.RestFilledTimeTokenMaker()

    assert editor.target == maker
