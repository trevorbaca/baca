import baca
from abjad.tools.scoretools import Performer
from abjad.tools.instrumenttools import *


def test_PerformerEditor_move_instrument_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input="l'arch perf flutist move q")
    assert studio.ts == (9,)

    studio.run(user_input="l'arch perf flutist move b q")
    assert studio.ts == (11, (6, 9))

    studio.run(user_input="l'arch perf flutist move studio q")
    assert studio.ts == (11, (0, 9))

    studio.run(user_input="l'arch perf flutist move score q")
    assert studio.ts == (11, (2, 9))

    studio.run(user_input="l'arch perf flutist move foo q")
    assert studio.ts == (11,)


def test_PerformerEditor_move_instrument_02():
    '''Add two instruments. Move them.
    '''

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='add 1 add 2 move 1 2 q')
    assert editor.target == Performer(instruments=[AltoFlute(), Accordion()])
