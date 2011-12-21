from abjad import *
import baca


def test_InstrumentEditor_base_states_01():
    '''Start-up, select instrument, main menu.
    '''

    editor = baca.scf.editors.InstrumentEditor()
    editor.run(user_input='1 q')
    assert editor.ts == (4,)
    assert editor.transcript[-2] == \
    ['Accordion',
      '',
      "     instrument name (in):                'accordion'",
      "     instrument name markup (inm):        Markup('Accordion')",
      "     short instrument name (sin):         'acc.'",
      "     short instrument name markup (sinm): Markup('Acc.')",
      '',
      '     range: [E1, C8]',
      '     clefs: treble, bass',
      '']


def test_InstrumentEditor_base_states_02():
    '''Start-up values without target.
    '''

    editor = baca.scf.editors.InstrumentEditor()
    assert isinstance(editor.session, baca.scf.Session)
    assert editor.target is None


def test_InstrumentEditor_base_states_03():
    '''Start-up values with target.
    '''

    accordion = instrumenttools.Accordion()
    accordion.instrument_name = 'accordion I'
    accordion.short_instrument_name = 'acc. I'
    editor = baca.scf.editors.InstrumentEditor(target=accordion)
    assert isinstance(editor.session, baca.scf.Session)
    assert editor.target is accordion
