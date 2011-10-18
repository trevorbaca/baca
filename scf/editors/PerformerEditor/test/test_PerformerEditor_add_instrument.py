import baca
from abjad.tools.scoretools import Performer
from abjad.tools.instrumenttools import *


def test_PerformerEditor_add_instrument_01():
    '''Quit, back, studio & junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run('1 perf 1 add q')
    assert len(studio.transcript) == 10

    studio = baca.scf.Studio()
    studio.run('1 perf 1 add b q')
    transcript = studio.session.transcript
    assert len(transcript) == 12
    assert transcript[-2] == transcript[-6]

    studio = baca.scf.Studio()
    studio.run('1 perf 1 add studio q')
    transcript = studio.session.transcript
    assert len(transcript) == 12
    assert transcript[-2] == transcript[-12]

    studio = baca.scf.Studio()
    studio.run('1 perf 1 add foo q')
    transcript = studio.session.transcript
    assert len(transcript) == 12
    assert transcript[-2] == transcript[-4]


def test_PerformerEditor_add_instrument_02():
    '''Add two instruments.
    '''

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='add 1 add 2 q')
    assert editor.target == Performer(instruments=[Accordion(), AltoFlute()])
