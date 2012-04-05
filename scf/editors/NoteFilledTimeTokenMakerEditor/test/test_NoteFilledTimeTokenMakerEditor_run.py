from abjad.tools import timetokentools
import handlers
import scf


def test_NoteFilledTimeTokenMakerEditor_run_01():

    editor = scf.editors.NoteFilledTimeTokenMakerEditor()
    editor.run(user_input='q', is_autoadvancing=True)

    maker = timetokentools.NoteFilledTimeTokenMaker()

    assert editor.target == maker
