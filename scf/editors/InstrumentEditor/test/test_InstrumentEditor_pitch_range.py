from abjad import *
import scf


def test_InstrumentEditor_pitch_range_01():
    
    editor = scf.editors.InstrumentEditor()
    editor.run(user_input='marimba q')
    assert editor.target.pitch_range == pitchtools.PitchRange(-19, 36)

    editor = scf.editors.InstrumentEditor()
    editor.run(user_input='marimba range (-24, 36) q')
    assert editor.target.pitch_range == pitchtools.PitchRange(-24, 36)
