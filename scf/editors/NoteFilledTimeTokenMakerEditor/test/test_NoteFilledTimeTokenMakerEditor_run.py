from abjad.tools import rhythmmakertools
import handlertools
import scf


def test_NoteFilledTimeTokenMakerEditor_run_01():

    editor = scf.editors.NoteFilledTimeTokenMakerEditor()
    editor.run(user_input='q', is_autoadvancing=True)

    maker = rhythmmakertools.NoteFilledRhythmMaker()

    assert editor.target == maker
