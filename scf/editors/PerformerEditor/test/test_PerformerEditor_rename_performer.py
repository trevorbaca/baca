import baca
from abjad import *


def test_PerformerEditor_rename_performer_01():
    '''Quit, back and studio all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 ren q')
    assert studio.ts == (9, (1, 5))

    studio.run(user_input='1 perf 1 ren b q')
    assert studio.ts == (11, (1, 5), (6, 9))

    studio.run(user_input='1 perf 1 ren studio q')
    assert studio.ts == (11, (0, 9), (1, 5))


def test_PerformerEditor_rename_performer_02():
    '''String input only.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 ren -99 q')
    assert studio.ts == (11, (1, 5))


def test_PerformerEditor_rename_performer_03():
    '''Create, name and rename performer.
    '''

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='name foo ren bar q')
    assert editor.target == scoretools.Performer(name='bar')
