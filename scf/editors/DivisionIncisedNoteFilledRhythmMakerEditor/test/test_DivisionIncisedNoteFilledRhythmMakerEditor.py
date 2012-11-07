from abjad.tools import rhythmmakertools
import scf


def test_DivisionIncisedNoteFilledRhythmMakerEditor_01():

    editor = scf.editors.DivisionIncisedNoteFilledRhythmMakerEditor()
    editor.run(user_input='1 [-8] [0, 1] [-1] [1] 32 q', is_autoadvancing=True)

    maker = rhythmmakertools.DivisionIncisedNoteFilledRhythmMaker([-8], [0, 1], [-1], [1], 32)

    assert editor.target == maker
