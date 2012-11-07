from abjad.tools import rhythmmakertools
import scf


def test_DivisionIncisedRestFilledRhythmMakerEditor_run_01():

    editor = scf.editors.DivisionIncisedRestFilledRhythmMakerEditor()
    editor.run(user_input='1 [8] [0, 1] [1] [1] 32 q', is_autoadvancing=True)

    maker = rhythmmakertools.DivisionIncisedRestFilledRhythmMaker([8], [0, 1], [1], [1], 32)

    assert editor.target == maker
