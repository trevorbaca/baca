import baca
from abjad.tools.scoretools import Performer
from abjad.tools.instrumenttools import *


def test_PerformerEditor_delete_instrument_01():
    '''Quit, back, studio & junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run('1 perf 1 del q')
    assert studio.ts == (9, (1, 5))

    studio = baca.scf.Studio()
    studio.run('1 perf 1 del b q')
    assert studio.ts == (11, (1, 5), (6, 9))

    studio = baca.scf.Studio()
    studio.run('1 perf 1 del studio q')
    assert studio.ts == (11, (0, 9), (1, 5))

    studio = baca.scf.Studio()
    studio.run('1 perf 1 del foo q')
    transcript = studio.transcript
    assert studio.ts == (11, (1, 5))


def test_PerformerEditor_delete_instrument_02():
    '''Add two instruments. Delete one.
    '''

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='add 1 add 2 del 1 q')
    assert editor.target == Performer(instruments=[AltoFlute()])
