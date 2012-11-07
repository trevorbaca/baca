from abjad.tools import rhythmmakertools
import handlertools
import scf


def test_NoteFilledRhythmMakerEditor_run_01():

    editor = scf.editors.NoteFilledRhythmMakerEditor()
    editor.run(user_input='q', is_autoadvancing=True)

    maker = rhythmmakertools.NoteFilledRhythmMaker()

    assert editor.target == maker
