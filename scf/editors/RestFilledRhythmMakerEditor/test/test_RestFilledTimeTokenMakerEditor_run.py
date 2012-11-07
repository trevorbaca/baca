from abjad.tools import rhythmmakertools
import scf


def test_RestFilledRhythmMakerEditor_run_01():

    editor = scf.editors.RestFilledRhythmMakerEditor()
    editor.run(user_input='q', is_autoadvancing=True)

    maker = rhythmmakertools.RestFilledRhythmMaker()

    assert editor.target == maker
