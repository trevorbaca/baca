from abjad.tools.scoretools import InstrumentationSpecifier
from abjad.tools.scoretools import Performer
from abjad.tools.instrumenttools import *
import baca


def test_InstrumentationEditor_remove_performers_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 setup performers del q')
    assert studio.ts == (9,)

    studio.run(user_input='1 setup performers del b q')
    assert studio.ts == (11, (6, 9))

    studio.run(user_input='1 setup performers del studio q')
    assert studio.ts == (11, (0, 9))

    studio.run(user_input='1 setup performers del score q')
    assert studio.ts == (11, (2, 9))

    studio.run(user_input='1 setup performers del foo q')
    assert studio.ts == (11,)


def test_InstrumentationEditor_remove_performers_02():
    '''Add three performers. Delete two.
    '''

    editor = baca.scf.editors.InstrumentationEditor()
    editor.run(user_input='add acc default add bass default add bassoon default del 3 del 2 q')
    assert editor.target == InstrumentationSpecifier([Performer('accordionist', instruments=[Accordion()])])


def test_InstrumentationEditor_remove_performers_03():
    '''Range handling.
    '''

    editor = baca.scf.editors.InstrumentationEditor()
    editor.run(user_input='add 1-3 default default default del 3-2 q')
    assert editor.target == InstrumentationSpecifier([Performer('accordionist', instruments=[Accordion()])])
