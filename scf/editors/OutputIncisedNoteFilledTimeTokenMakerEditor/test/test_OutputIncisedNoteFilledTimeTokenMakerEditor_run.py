from abjad.tools import timetokentools
import scf


def test_OutputIncisedNoteFilledTimeTokenMakerEditor_run_01():

    editor = scf.editors.OutputIncisedNoteFilledTimeTokenMakerEditor()
    editor.run(user_input='1 [-8] [2] [-3] [4] 32 q', is_autoadvancing=True)

    maker = timetokentools.OutputIncisedNoteFilledTimeTokenMaker([-8], [2], [-3], [4], 32)

    assert editor.target == maker
