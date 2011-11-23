from abjad import *
import baca
import py.test


def test_InstrumentEditor_01():
    '''Default values without target.
    '''

    instrument_editor = baca.scf.editors.InstrumentEditor()
    
    assert isinstance(instrument_editor.session, baca.scf.Session)
    assert instrument_editor.target is None


def test_InstrumentEditor_02():
    '''Default values with target.
    '''

    accordion = instrumenttools.Accordion()
    accordion.instrument_name = 'accordion I'
    accordion.short_instrument_name = 'acc. I'
    instrument_editor = baca.scf.editors.InstrumentEditor(target=accordion)
    
    assert isinstance(instrument_editor.session, baca.scf.Session)
    assert instrument_editor.target is accordion


def test_InstrumentEditor_03():
    '''Main menu.
    '''

    session = baca.scf.Session(test='menu_lines')
    accordion = instrumenttools.Accordion()
    accordion.instrument_name = 'accordion I'
    accordion.short_instrument_name = 'acc. I'
    instrument_editor = baca.scf.editors.InstrumentEditor(session=session, target=accordion)
    instrument_editor.edit_interactively()

    assert session.test_result == [
     'Accordion I',
     '',
     '     in: instrument name',
     '     inm: instrument name markup',
     '     sin: short instrument name',
     '     sinm: short instrument name markup',
     '']


def test_InstrumentEditor_04():
    '''Main menu to instrument name dialogue.
    '''

    session = baca.scf.Session(test='menu_lines', user_input='in')
    accordion = instrumenttools.Accordion()
    accordion.instrument_name = 'accordion I'
    accordion.short_instrument_name = 'acc. I'
    instrument_editor = baca.scf.editors.InstrumentEditor(session=session, target=accordion)
    instrument_editor.edit_interactively()

    assert session.test_result == ['Instrument name> ']


def test_InstrumentEditor_05():
    '''Attribute management.
    '''
    py.test.skip()

    session = baca.scf.Session(user_input='in\nfoo')
    accordion = instrumenttools.Accordion()
    accordion.instrument_name = 'accordion I'
    accordion.short_instrument_name = 'acc. I'
    instrument_editor = baca.scf.editors.InstrumentEditor(session=session, target=accordion)
    instrument_editor.edit_interactively()
