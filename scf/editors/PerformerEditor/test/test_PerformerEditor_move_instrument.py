import baca
from abjad.tools.scoretools import Performer
from abjad.tools.instrumenttools import *


def test_PerformerEditor_move_instrument_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run('1 perf 1 mv q')
    assert studio.ts == (9, (1, 5))

    studio = baca.scf.Studio()
    studio.run('1 perf 1 mv b q')
    assert studio.ts == (11, (1, 5), (6, 9))

    studio = baca.scf.Studio()
    studio.run('1 perf 1 mv studio q')
    assert studio.ts == (11, (0, 9), (1, 5))

    studio = baca.scf.Studio()
    studio.run('1 perf 1 mv score q')
    assert studio.ts == (11, (1, 5), (2, 9))

    studio = baca.scf.Studio()
    studio.run('1 perf 1 mv foo q')
    assert studio.ts == (11, (1, 5))


def test_PerformerEditor_move_instrument_02():
    '''Add two instruments. Move them.
    '''

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='add 1 add 2 mv 1 2 q')
    assert editor.target == Performer(instruments=[AltoFlute(), Accordion()])
