from abjad.tools.scoretools import InstrumentationSpecifier
from abjad.tools.scoretools import Performer
from abjad.tools.instrumenttools import *
import baca


def test_InstrumentationEditor_delete_performer_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = baca.scf.Studio(user_input='1 perf del q')
    studio.run()
    assert studio.ts == (7,)

    studio = baca.scf.Studio(user_input='1 perf del b q')
    studio.run()
    assert studio.ts == (9, (4, 7))

    studio = baca.scf.Studio(user_input='1 perf del studio q')
    studio.run()
    assert studio.ts == (9, (0, 7))

    studio = baca.scf.Studio(user_input='1 perf del score q')
    studio.run()
    assert studio.ts == (9, (2, 7))

    studio = baca.scf.Studio(user_input='1 perf del foo q')
    studio.run()
    assert studio.ts == (9,)


def test_InstrumentationEditor_delete_performer_02():
    '''Add three performers. Delete two.
    '''

    editor = baca.scf.editors.InstrumentationEditor()
    editor.run(user_input='add acc default add bass default add bassoon default del 3 del 2 q')
    assert editor.target == InstrumentationSpecifier([Performer('accordionist', instruments=[Accordion()])])
