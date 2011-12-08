from abjad import *
import baca


def test_InstrumentEditor_instrument_name_01():
    '''Quit, back & studio all work.
    '''

    pass


def test_InstrumentEditor_instrument_name_02():
    '''(String) attribute management and interaction with other attributes.
    '''

    accordion = instrumenttools.Accordion()
    accordion.instrument_name = 'accordion I'
    accordion.short_instrument_name = 'acc. I'

    instrument_editor = baca.scf.editors.InstrumentEditor(target=accordion)
    instrument_editor.session.user_input = 'in foo q'
    instrument_editor.run()
    assert accordion.instrument_name == 'foo'

    instrument_editor = baca.scf.editors.InstrumentEditor(target=accordion)
    instrument_editor.session.user_input = 'sin f._I q'
    instrument_editor.run()
    assert accordion.short_instrument_name == 'f. I'
