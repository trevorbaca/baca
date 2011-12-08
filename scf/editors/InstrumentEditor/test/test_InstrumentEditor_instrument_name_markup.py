from abjad import *
import baca


def test_InstrumentEditor_instrument_name_markup_01():
    '''(Markup) attribute management and interaction with other attributes.
    '''

    accordion = instrumenttools.Accordion()
    accordion.instrument_name = 'accordion I'
    accordion.short_instrument_name = 'acc. I'

    instrument_editor = baca.scf.editors.InstrumentEditor(target=accordion)
    instrument_editor.session.user_input = 'inm foo_I q'
    instrument_editor.run()
    assert accordion.instrument_name_markup == markuptools.Markup('foo I')

    instrument_editor = baca.scf.editors.InstrumentEditor(target=accordion)
    instrument_editor.session.user_input = 'sinm f._I q'
    instrument_editor.run()
    assert accordion.short_instrument_name_markup == markuptools.Markup('f. I')
