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
     'Accordion',
     '',
     "     in: instrument name ('accordion I')",
     "     inm: instrument name markup (Markup('Accordion I'))",
     "     sin: short instrument name ('acc. I')",
     "     sinm: short instrument name markup (Markup('Acc. I'))",
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
    '''(String) attribute management.
    '''

    accordion = instrumenttools.Accordion()
    accordion.instrument_name = 'accordion I'
    accordion.short_instrument_name = 'acc. I'

    session = baca.scf.Session(user_input='in\nfoo')
    instrument_editor = baca.scf.editors.InstrumentEditor(session=session, target=accordion)
    instrument_editor.edit_interactively()
    assert accordion.instrument_name == 'foo'

    session = baca.scf.Session(user_input='sin\nf. I')
    instrument_editor = baca.scf.editors.InstrumentEditor(session=session, target=accordion)
    instrument_editor.edit_interactively()
    assert accordion.short_instrument_name == 'f. I'


def test_InstrumentEditor_06():
    '''(Markup) attribute management.
    '''

    accordion = instrumenttools.Accordion()
    accordion.instrument_name = 'accordion I'
    accordion.short_instrument_name = 'acc. I'

    session = baca.scf.Session(user_input='inm\nfoo I')
    instrument_editor = baca.scf.editors.InstrumentEditor(session=session, target=accordion)
    instrument_editor.edit_interactively()
    assert accordion.instrument_name_markup == markuptools.Markup('foo I')

    session = baca.scf.Session(user_input='sinm\nf. I')
    instrument_editor = baca.scf.editors.InstrumentEditor(session=session, target=accordion)
    instrument_editor.edit_interactively()
    assert accordion.short_instrument_name_markup == markuptools.Markup('f. I')
