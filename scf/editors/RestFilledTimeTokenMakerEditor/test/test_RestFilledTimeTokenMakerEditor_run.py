from abjad.tools import rhythmmakertools
import scf


def test_RestFilledTimeTokenMakerEditor_run_01():

    editor = scf.editors.RestFilledTimeTokenMakerEditor()
    editor.run(user_input='q', is_autoadvancing=True)

    maker = rhythmmakertools.RestFilledRhythmMaker()

    assert editor.target == maker
