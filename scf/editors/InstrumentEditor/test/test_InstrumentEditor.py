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

    accordion = instrumenttools.Accordion()
    accordion.instrument_name = 'accordion I'
    accordion.short_instrument_name = 'acc. I'

    instrument_editor = baca.scf.editors.InstrumentEditor(target=accordion)
    instrument_editor.session.user_input = 'q'
    instrument_editor.edit_interactively()

    assert instrument_editor.session.transcript[-2] == [
     'Accordion',
     '',
     "     in: instrument name ('accordion I')",
     "     inm: instrument name markup (Markup('Accordion I'))",
     "     sin: short instrument name ('acc. I')",
     "     sinm: short instrument name markup (Markup('Acc. I'))",
     '']


def test_InstrumentEditor_04():
    '''(String) attribute management.
    '''

    accordion = instrumenttools.Accordion()
    accordion.instrument_name = 'accordion I'
    accordion.short_instrument_name = 'acc. I'

    instrument_editor = baca.scf.editors.InstrumentEditor(target=accordion)
    instrument_editor.session.user_input = 'in\nfoo\nq'
    instrument_editor.edit_interactively()
    assert accordion.instrument_name == 'foo'

    instrument_editor = baca.scf.editors.InstrumentEditor(target=accordion)
    instrument_editor.session.user_input = 'sin\nf. I\nq'
    instrument_editor.edit_interactively()
    assert accordion.short_instrument_name == 'f. I'


def test_InstrumentEditor_05():
    '''(Markup) attribute management.
    '''

    accordion = instrumenttools.Accordion()
    accordion.instrument_name = 'accordion I'
    accordion.short_instrument_name = 'acc. I'

    instrument_editor = baca.scf.editors.InstrumentEditor(target=accordion)
    instrument_editor.session.user_input = 'inm\nfoo I\nq'
    instrument_editor.edit_interactively()
    assert accordion.instrument_name_markup == markuptools.Markup('foo I')

    instrument_editor = baca.scf.editors.InstrumentEditor(target=accordion)
    instrument_editor.session.user_input = 'sinm\nf. I\nq'
    instrument_editor.edit_interactively()
    assert accordion.short_instrument_name_markup == markuptools.Markup('f. I')


def test_InstrumentEditor_06():
    '''Make instrument.
    '''

    instrument_editor = baca.scf.editors.InstrumentEditor()
    instrument_editor.session.user_input = '9\nq'
    instrument = instrument_editor.edit_interactively()
    assert instrument == instrumenttools.ContrabassFlute()
