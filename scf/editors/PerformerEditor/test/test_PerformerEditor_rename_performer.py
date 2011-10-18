import baca
from abjad import *


def test_PerformerEditor_rename_performer_01():
    '''Quit, back and studio all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 ren q')
    assert len(studio.transcript) == 9

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 ren b q')
    transcript = studio.transcript
    assert len(transcript) == 11
    assert transcript[-2] == transcript[-5]

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 ren studio q')
    transcript = studio.transcript
    assert len(transcript) == 11
    assert transcript[-2] == transcript[-11]


def test_PerformerEditor_rename_performer_02():
    '''String input only.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 ren -99 q')
    transcript = studio.transcript
    assert len(transcript) == 11


def test_PerformerEditor_rename_performer_03():
    '''Create, name and rename performer.
    '''

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='name foo ren bar q')
    assert editor.target == scoretools.Performer(name='bar')
