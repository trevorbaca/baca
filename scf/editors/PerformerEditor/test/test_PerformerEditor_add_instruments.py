import baca
from abjad.tools.scoretools import Performer
from abjad.tools.instrumenttools import *


def test_PerformerEditor_add_instruments_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run('1 perf 1 add q')
    assert studio.ts == (10, (1, 5))

    studio = baca.scf.Studio()
    studio.run('1 perf 1 add b q')
    assert studio.ts == (12, (1, 5), (6, 10))

    studio = baca.scf.Studio()
    studio.run('1 perf 1 add studio q')
    assert studio.ts == (12, (0, 10), (1, 5))

    studio = baca.scf.Studio()
    studio.run('1 perf 1 add score q')
    assert studio.ts == (12, (1, 5), (2, 10))

    studio = baca.scf.Studio()
    studio.run('1 perf 1 add foo q')
    assert studio.ts == (12, (1, 5), (8, 10))


def test_PerformerEditor_add_instruments_02():
    '''Add two instruments.
    '''

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='add 1 add 2 q')
    assert editor.target == Performer(instruments=[Accordion(), AltoFlute()])


def test_PerformerEditor_add_instruments_03():
    '''Range handling.
    '''

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='add 1-2 q')
    assert editor.target == Performer(instruments=[Accordion(), AltoFlute()])
