from abjad import *
import baca


def test_InstrumentEditor_pitch_range_01():
    
    editor = baca.scf.editors.InstrumentEditor()
    editor.run(user_input='marimba q')
    assert editor.target.pitch_range == pitchtools.PitchRange(-19, 36)

    editor = baca.scf.editors.InstrumentEditor()
    editor.run(user_input='marimba pr (-24,36) q')
    assert editor.target.pitch_range == pitchtools.PitchRange(-24, 36)
