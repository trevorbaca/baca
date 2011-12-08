from abjad import *
import baca


def test_InstrumentEditor_base_states_01():
    '''Start-up, select instrument.
    '''

    pass


def test_InstrumentEditor_base_states_02():
    '''Default values without target.
    '''

    instrument_editor = baca.scf.editors.InstrumentEditor()
    
    assert isinstance(instrument_editor.session, baca.scf.Session)
    assert instrument_editor.target is None


def test_InstrumentEditor_base_states_03():
    '''Default values with target.
    '''

    accordion = instrumenttools.Accordion()
    accordion.instrument_name = 'accordion I'
    accordion.short_instrument_name = 'acc. I'
    instrument_editor = baca.scf.editors.InstrumentEditor(target=accordion)
    
    assert isinstance(instrument_editor.session, baca.scf.Session)
    assert instrument_editor.target is accordion


def test_InstrumentEditor_base_states_04():
    '''Main menu.
    '''

    accordion = instrumenttools.Accordion()
    accordion.instrument_name = 'accordion I'
    accordion.short_instrument_name = 'acc. I'

    instrument_editor = baca.scf.editors.InstrumentEditor(target=accordion)
    instrument_editor.session.user_input = 'q'
    instrument_editor.run()

    assert instrument_editor.session.transcript[-2] == [
     'Accordion I',
     '',
     "     in: instrument name ('accordion I')",
     "     inm: instrument name markup (Markup('Accordion I'))",
     "     sin: short instrument name ('acc. I')",
     "     sinm: short instrument name markup (Markup('Acc. I'))",
     '']
