from abjad import *
from abjad.tools.pitchtools import NamedChromaticPitch
import baca


def test_PitchRangeEditor_make_target_01():

    # TODO: make fs,, work
    editor = baca.scf.editors.PitchRangeEditor()
    #editor.run(user_input='fs,, True c True q') 
    editor.run(user_input="fs True c'' True q") 

    assert editor.target == pitchtools.PitchRange(
        (NamedChromaticPitch('fs'), 'inclusive'), (NamedChromaticPitch("c''"), 'inclusive'))
