import baca
from abjad.tools.scoretools import Performer
from abjad.tools.instrumenttools import *


def test_PerformerEditor_delete_instruments_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 setup perf 1 del q')
    assert studio.ts == (11, (1, 7))

    studio.run(user_input='1 setup perf 1 del b q')
    assert studio.ts == (13, (1, 7), (8, 11))

    studio.run(user_input='1 setup perf 1 del studio q')
    assert studio.ts == (13, (0, 11), (1, 7))

    studio.run(user_input='1 setup perf 1 del score q')
    assert studio.ts == (13, (1, 7), (2, 11))

    studio.run(user_input='1 setup perf 1 del foo q')
    transcript = studio.transcript
    assert studio.ts == (13, (1, 7))


def test_PerformerEditor_delete_instruments_02():
    '''Add two instruments. Delete one.
    '''

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='add flute add acc del flute q')
    assert editor.target == Performer(instruments=[Accordion()])


def test_PerformerEditor_delete_instruments_03():
    '''Numeric range handling.
    '''

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='add 1-3 del 1,3 q')
    assert editor.target == Performer(instruments=[AltoFlute()])
