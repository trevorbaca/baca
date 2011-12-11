from abjad.tools.instrumenttools import *
from abjad.tools.scoretools import InstrumentationSpecifier
from abjad.tools.scoretools import Performer
import baca


def test_InstrumentationEditor_add_performer_01():
    '''Quit, back, studio, score & junk all work.
    '''

    studio = baca.scf.Studio(user_input='1 perf add q')
    studio.run()
    assert studio.ts == (8,)

    studio = baca.scf.Studio(user_input='1 perf add b q')
    studio.run()
    assert studio.ts == (10, (4, 8))

    studio = baca.scf.Studio(user_input='1 perf add studio q')
    studio.run()
    assert studio.ts == (10, (0, 8))

    studio = baca.scf.Studio(user_input='1 perf add score q')
    studio.run()
    assert studio.ts == (10, (2, 8))

    studio = baca.scf.Studio(user_input='1 perf add foo q')
    studio.run()
    assert studio.ts == (10, (6, 8))


def test_InstrumentationEditor_add_performer_02():
    '''Add three performers.
    '''

    editor = baca.scf.editors.InstrumentationEditor()
    editor.run(user_input='add acc default add bass default add bassoon default q')
    assert editor.target == InstrumentationSpecifier([
        Performer(name='accordionist', instruments=[Accordion()]), 
        Performer(name='bassist', instruments=[Contrabass()]), 
        Performer(name='bassoonist', instruments=[Bassoon()])])
