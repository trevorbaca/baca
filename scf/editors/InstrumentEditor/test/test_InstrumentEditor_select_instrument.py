import baca


def test_InstrumentEditor_select_instrument_01():
    '''Quit, back, studio & junk all work.
    '''

    editor = baca.scf.editors.InstrumentEditor()
    editor.run(user_input='q')
    assert len(editor.transcript) == 2

    # TODO: make work
    #editor = baca.scf.editors.InstrumentEditor()
    #editor.run(user_input='b q')
    #assert len(editor.transcript) == 2

    editor = baca.scf.editors.InstrumentEditor()
    editor.run(user_input='studio q')
    assert len(editor.transcript) == 2

    editor = baca.scf.editors.InstrumentEditor()
    editor.run(user_input='foo q')
    transcript = editor.transcript
    assert len(transcript) == 4
    assert transcript[-2] == transcript[-4]
