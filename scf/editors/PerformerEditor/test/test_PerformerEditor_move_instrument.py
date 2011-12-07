import baca
from abjad.tools.scoretools import Performer
from abjad.tools.instrumenttools import *


def test_PerformerEditor_move_instrument_01():
    '''Quit, back, studio & junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run('1 perf 1 mv q')
    assert len(studio.transcript) == 9

    studio = baca.scf.Studio()
    studio.run('1 perf 1 mv b q')
    transcript = studio.session.transcript
    assert len(transcript) == 11
    assert transcript[-2] == transcript[-5]

    studio = baca.scf.Studio()
    studio.run('1 perf 1 mv studio q')
    transcript = studio.session.transcript
    assert len(transcript) == 11
    assert transcript[-2] == transcript[-11]

    studio = baca.scf.Studio()
    studio.run('1 perf 1 mv foo q')
    transcript = studio.session.transcript
    assert len(transcript) == 11


def test_PerformerEditor_move_instrument_02():
    '''Add two instruments. Move them.
    '''

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='add 1 add 2 mv 1 2 q')
    assert editor.target == Performer(instruments=[AltoFlute(), Accordion()])
