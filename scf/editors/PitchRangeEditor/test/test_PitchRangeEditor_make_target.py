from abjad import *
from abjad.tools.pitchtools import NamedChromaticPitch
import baca


def test_PitchRangeEditor_make_target_01():

    editor = baca.scf.editors.PitchRangeEditor()
    editor.run(user_input="fs True c'' True q") 

    assert editor.target == pitchtools.PitchRange(
        (NamedChromaticPitch('fs'), 'inclusive'), (NamedChromaticPitch("c''"), 'inclusive'))


def test_PitchRangeEditor_make_target_02():
    '''Use quotes as around command-terminated European pitch names in user input testing.
    '''

    editor = baca.scf.editors.PitchRangeEditor()
    editor.run(user_input="'fs,,' True c'' True q") 

    assert editor.target == pitchtools.PitchRange(
        (NamedChromaticPitch('fs,,'), 'inclusive'), (NamedChromaticPitch("c''"), 'inclusive'))


def test_PitchRangeEditor_make_target_03():
    '''Quit, score, studio & junk all work.

    Note that back doesn't yet work here 
    because 'b' interprets as named chromatic pitch.
    '''

    editor = baca.scf.editors.PitchRangeEditor()
    editor.run(user_input='q')
    assert editor.ts == (1,)

    editor = baca.scf.editors.PitchRangeEditor()
    editor.run(user_input='sco')
    assert editor.ts == (1,)

    editor = baca.scf.editors.PitchRangeEditor()
    editor.run(user_input='stu')
    assert editor.ts == (1,)

    editor = baca.scf.editors.PitchRangeEditor()
    editor.run(user_input='foo q')
    assert editor.ts == (3,)
