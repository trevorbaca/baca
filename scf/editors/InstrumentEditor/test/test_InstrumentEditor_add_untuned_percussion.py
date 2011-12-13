import baca


def test_InstrumentEditor_add_untuned_percussion_01():
    '''Quit, back, score, studio & junk all work.
    '''

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='untuned q')
    assert editor.ts == (4, (0, 2))

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='untuned b')
    assert editor.ts == (4, (0, 2))

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='untuned sco')
    assert editor.ts == (4, (0, 2))

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='untuned stu')
    assert editor.ts == (4, (0, 2))

    editor = baca.scf.editors.PerformerEditor()
    editor.run(user_input='untuned foo q')
    assert editor.ts == (6, (0, 2, 4))
