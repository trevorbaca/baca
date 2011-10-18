from abjad.tools.instrumenttools import *
from abjad.tools.scoretools import InstrumentationSpecifier
from abjad.tools.scoretools import Performer
import baca


def test_InstrumentationEditor_move_performer_01():
    '''Quit, back, studio & junk all work.
    '''

    studio = baca.scf.Studio(user_input='1 perf mv q')
    studio.run()
    transcript = studio.session.transcript
    assert len(transcript) == 7

    studio = baca.scf.Studio(user_input='1 perf mv b q')
    studio.run()
    transcript = studio.session.transcript
    assert len(transcript) == 9
    assert transcript[-2] == transcript[-5]

    studio = baca.scf.Studio(user_input='1 perf mv studio q')
    studio.run()
    transcript = studio.session.transcript
    assert len(transcript) == 9
    assert transcript[-2] == transcript[0]

    studio = baca.scf.Studio(user_input='1 perf mv foo q')
    studio.run()
    transcript = studio.session.transcript
    assert len(transcript) == 9


def test_InstrumentationEditor_move_performer_02():
    '''Add three performers. Make two moves.
    '''

    editor = baca.scf.editors.InstrumentationEditor()
    editor.run(user_input='add 1 1 add 2 1 add 3 1 mv 1 2 mv 2 3 q')
    assert editor.target == InstrumentationSpecifier([
        Performer(name='bassist', instruments=[Contrabass()]), 
        Performer(name='bassoonist', instruments=[Bassoon()]), 
        Performer(name='accordionist', instruments=[Accordion()])])
