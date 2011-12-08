import baca


# TODO: flesh out
def test_InstrumentEditor_select_instrument_01():
    '''Quit, back, studio & junk all work.
    '''

    instrument_editor = baca.scf.editors.InstrumentEditor()
    instrument_editor.session.user_input = 'q'
    instrument_editor.run()
    transcript = instrument_editor.session.transcript

    assert len(transcript) == 2
    assert transcript[0][:4] == [
      'Instrument editor - select instrument',
      '',
      '     1: accordion',
      '     2: alto flute']
