from abjad.tools import rhythmmakertools
import handlertools
import scf


def test_NoteRhythmMakerEditor_01():

    editor = scf.editors.NoteRhythmMakerEditor()
    editor.run(user_input='q', is_autoadvancing=True)

    maker = rhythmmakertools.NoteRhythmMaker()

    assert editor.target == maker
