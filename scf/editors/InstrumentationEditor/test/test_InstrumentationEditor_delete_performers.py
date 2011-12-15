from abjad.tools.scoretools import InstrumentationSpecifier
from abjad.tools.scoretools import Performer
from abjad.tools.instrumenttools import *
import baca


def test_InstrumentationEditor_delete_performers_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf del q')
    assert studio.ts == (7,)

    studio.run(user_input='1 perf del b q')
    assert studio.ts == (9, (4, 7))

    studio.run(user_input='1 perf del studio q')
    assert studio.ts == (9, (0, 7))

    studio.run(user_input='1 perf del score q')
    assert studio.ts == (9, (2, 7))

    studio.run(user_input='1 perf del foo q')
    assert studio.ts == (9,)


def test_InstrumentationEditor_delete_performers_02():
    '''Add three performers. Delete two.
    '''

    editor = baca.scf.editors.InstrumentationEditor()
    editor.run(user_input='add acc default add bass default add bassoon default del 3 del 2 q')
    assert editor.target == InstrumentationSpecifier([Performer('accordionist', instruments=[Accordion()])])


def test_InstrumentationEditor_delete_performers_03():
    '''Range handling.
    '''

    editor = baca.scf.editors.InstrumentationEditor()
    editor.run(user_input='add 1-3 default default default del 3-2 q')
    assert editor.target == InstrumentationSpecifier([Performer('accordionist', instruments=[Accordion()])])
