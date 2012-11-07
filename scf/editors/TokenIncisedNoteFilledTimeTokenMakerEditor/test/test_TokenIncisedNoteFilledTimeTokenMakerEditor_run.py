from abjad.tools import rhythmmakertools
import scf


def test_TokenIncisedNoteFilledRhythmMakerEditor_run_01():

    editor = scf.editors.TokenIncisedNoteFilledRhythmMakerEditor()
    editor.run(user_input='1 [-8] [0, 1] [-1] [1] 32 q', is_autoadvancing=True)

    maker = rhythmmakertools.TokenIncisedNoteFilledRhythmMaker([-8], [0, 1], [-1], [1], 32)

    assert editor.target == maker
