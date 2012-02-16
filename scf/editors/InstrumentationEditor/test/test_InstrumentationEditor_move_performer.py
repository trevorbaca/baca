from abjad.tools.instrumenttools import *
from abjad.tools.scoretools import InstrumentationSpecifier
from abjad.tools.scoretools import Performer
import baca


def test_InstrumentationEditor_move_performer_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = baca.scf.studiopackage.Studio()
    studio.run(user_input='1 setup perf move q')
    assert studio.ts == (9,)

    studio.run(user_input='1 setup perf move b q')
    assert studio.ts == (11, (6, 9))

    studio.run(user_input='1 setup perf move studio q')
    assert studio.ts == (11, (0, 9))

    studio.run(user_input='1 setup perf move score q')
    assert studio.ts == (11, (2, 9))

    studio.run(user_input='1 setup perf move foo q')
    assert studio.ts == (11,)


def test_InstrumentationEditor_move_performer_02():
    '''Add three performers. Make two moves.
    '''

    editor = baca.scf.editors.InstrumentationEditor()
    editor.run(user_input='add 1 1 add 2 1 add 3 1 move 1 2 move 2 3 q')
    assert editor.target == InstrumentationSpecifier([
        Performer(name='bassist', instruments=[Contrabass()]), 
        Performer(name='bassoonist', instruments=[Bassoon()]), 
        Performer(name='accordionist', instruments=[Accordion()])])
