from abjad.tools.instrumenttools import *
from abjad.tools.scoretools import InstrumentationSpecifier
from abjad.tools.scoretools import Performer
import baca


def test_InstrumentationEditor_add_performers_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = baca.scf.studio.Studio()
    studio.run(user_input='1 setup performers add q')
    assert studio.ts == (10,)

    studio.run(user_input='1 setup performers add b q')
    assert studio.ts == (12, (6, 10))

    studio.run(user_input='1 setup performers add studio q')
    assert studio.ts == (12, (0, 10))

    studio.run(user_input='1 setup performers add score q')
    assert studio.ts == (12, (2, 10))

    studio.run(user_input='1 setup performers add foo q')
    assert studio.ts == (12, (8, 10))


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
