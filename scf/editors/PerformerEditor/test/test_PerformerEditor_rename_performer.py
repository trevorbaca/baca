import scf
from abjad import *


def test_PerformerEditor_rename_performer_01():
    '''Quit, back and studio all work.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='1 setup performers 1 ren q')
    assert studio.ts == (11, (1, 7))

    studio.run(user_input='1 setup performers 1 ren b q')
    assert studio.ts == (13, (1, 7), (8, 11))

    studio.run(user_input='1 setup performers 1 ren studio q')
    assert studio.ts == (13, (0, 11), (1, 7))


def test_PerformerEditor_rename_performer_02():
    '''String input only.
    '''

    studio = scf.studio.Studio()
    studio.run(user_input='1 setup performers 1 ren -99 q')
    assert studio.ts == (13, (1, 7))


def test_PerformerEditor_rename_performer_03():
    '''Create, name and rename performer.
    '''

    editor = scf.editors.PerformerEditor()
    editor.run(user_input='name foo ren bar q')
    assert editor.target == scoretools.Performer(name='bar')
