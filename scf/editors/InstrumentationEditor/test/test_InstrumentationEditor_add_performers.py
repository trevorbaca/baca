from abjad.tools.instrumenttools import *
from abjad.tools.scoretools import InstrumentationSpecifier
from abjad.tools.scoretools import Performer
import baca


def test_InstrumentationEditor_add_performers_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf add q')
    assert studio.ts == (8,)

    studio.run(user_input='1 perf add b q')
    assert studio.ts == (10, (4, 8))

    studio.run(user_input='1 perf add studio q')
    assert studio.ts == (10, (0, 8))

    studio.run(user_input='1 perf add score q')
    assert studio.ts == (10, (2, 8))

    studio.run(user_input='1 perf add foo q')
    assert studio.ts == (10, (6, 8))


def test_InstrumentationEditor_add_performers_02():
    '''Add three performers.
    '''

    editor = baca.scf.editors.InstrumentationEditor()
    editor.run(user_input='add acc default add bass default add bassoon default q')
    assert editor.target == InstrumentationSpecifier([
        Performer(name='accordionist', instruments=[Accordion()]), 
        Performer(name='bassist', instruments=[Contrabass()]), 
        Performer(name='bassoonist', instruments=[Bassoon()])])


def test_InstrumentationEditor_add_performers_03():
    '''Range handling.
    '''

    editor = baca.scf.editors.InstrumentationEditor()
    editor.run(user_input='add 1-3 default default default q')
    assert editor.target == InstrumentationSpecifier([
        Performer(name='accordionist', instruments=[Accordion()]), 
        Performer(name='bassist', instruments=[Contrabass()]), 
        Performer(name='bassoonist', instruments=[Bassoon()])])
