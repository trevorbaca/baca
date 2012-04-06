from abjad.tools import timetokentools
import scf


def test_TokenIncisedNoteFilledTimeTokenMakerEditor_run_01():

    editor = scf.editors.TokenIncisedNoteFilledTimeTokenMakerEditor()
    editor.run(user_input='1 [-8] [0, 1] [-1] [1] 32 q', is_autoadvancing=True)

    maker = timetokentools.TokenIncisedNoteFilledTimeTokenMaker([-8], [0, 1], [-1], [1], 32)

    assert editor.target == maker
