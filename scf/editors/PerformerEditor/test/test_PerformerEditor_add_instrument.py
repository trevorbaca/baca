import baca


def test_PerformerEditor_add_instrument_01():

    pass


def test_PerformerEditor_add_instrument_02():
    '''Quit while adding instrument.
    '''

    performer_editor = baca.scf.editors.PerformerEditor()
    performer_editor.session.user_input = 'add q'
    performer_editor.run()
    transcript = performer_editor.session.transcript

    assert len(transcript) == 4
    assert transcript[2][:4] == [
      'Performer - select instrument',
      '',
      '     1: accordion',
      '     2: alto flute']


def test_PerformerEditor_add_instrument_03():
    '''Back while adding instrument.
    '''

    performer_editor = baca.scf.editors.PerformerEditor()
    performer_editor.session.user_input = 'add b q'
    performer_editor.run()
    transcript = performer_editor.session.transcript

    assert len(transcript) == 6
    assert transcript[0] == transcript[4]
