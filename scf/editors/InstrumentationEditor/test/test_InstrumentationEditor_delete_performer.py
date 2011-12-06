import baca
from abjad.tools.scoretools import InstrumentationSpecifier
from abjad.tools.scoretools import Performer


def test_InstrumentationEditor_delete_performer_01():
    '''Quit, back, studio & junk all work.
    '''

    studio = baca.scf.Studio(user_input='1 perf del q')
    studio.run()
    transcript = studio.session.transcript
    assert len(transcript) == 7

    studio = baca.scf.Studio(user_input='1 perf del b q')
    studio.run()
    transcript = studio.session.transcript
    assert len(transcript) == 9
    assert transcript[-2] == transcript[-5]

    studio = baca.scf.Studio(user_input='1 perf del studio q')
    studio.run()
    transcript = studio.session.transcript
    assert len(transcript) == 9
    assert transcript[-2] == transcript[0]

    studio = baca.scf.Studio(user_input='1 perf del foo q')
    studio.run()
    transcript = studio.session.transcript
    assert len(transcript) == 9


def test_InstrumentationEditor_delete_performer_02():
    '''Add three performers. Delete two.
    '''

    editor = baca.scf.editors.InstrumentationEditor()
    editor.run(user_input='add 1 add 2 add 3 del 3 del 2 q')
    assert editor.target == InstrumentationSpecifier([Performer('accordionist')])
