from abjad.tools import rhythmmakertools
import scf


def test_OutputIncisedNoteFilledRhythmMakerEditor_run_01():

    editor = scf.editors.OutputIncisedNoteFilledRhythmMakerEditor()
    editor.run(user_input='1 [-8] [2] [-3] [4] 32 q', is_autoadvancing=True)

    maker = rhythmmakertools.OutputIncisedNoteFilledRhythmMaker([-8], [2], [-3], [4], 32)

    assert editor.target == maker
