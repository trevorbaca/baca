from abjad.tools.instrumenttools import *
from abjad.tools.scoretools import InstrumentationSpecifier
from abjad.tools.scoretools import Performer
import baca


def test_InstrumentationEditor_move_performer_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = baca.scf.Studio(user_input='1 perf mv q')
    studio.run()
    assert studio.ts == (7,)

    studio = baca.scf.Studio(user_input='1 perf mv b q')
    studio.run()
    assert studio.ts == (9, (4, 7))

    studio = baca.scf.Studio(user_input='1 perf mv studio q')
    studio.run()
    assert studio.ts == (9, (0, 7))

    studio = baca.scf.Studio(user_input='1 perf mv score q')
    studio.run()
    assert studio.ts == (9, (2, 7))

    studio = baca.scf.Studio(user_input='1 perf mv foo q')
    studio.run()
    assert studio.ts == (9,)


def test_InstrumentationEditor_move_performer_02():
    '''Add three performers. Make two moves.
    '''

    editor = baca.scf.editors.InstrumentationEditor()
    editor.run(user_input='add 1 1 add 2 1 add 3 1 mv 1 2 mv 2 3 q')
    assert editor.target == InstrumentationSpecifier([
        Performer(name='bassist', instruments=[Contrabass()]), 
        Performer(name='bassoonist', instruments=[Bassoon()]), 
        Performer(name='accordionist', instruments=[Accordion()])])
