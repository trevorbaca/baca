from abjad import *
import baca


def test_InstrumentEditor_instrument_name_01():
    '''Quit, back & studio all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 in q')
    assert len(studio.transcript) == 11

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 in b q')
    transcript = studio.transcript
    assert len(transcript) == 13
    assert transcript[-2] == transcript[-5]

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 in studio q')
    transcript = studio.transcript
    assert len(transcript) == 13
    assert transcript[-2] == transcript[-13]


def test_InstrumentEditor_instrument_name_02():
    '''String only.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 in -99 q')
    transcript = studio.transcript
    assert len(transcript) == 13
    assert transcript[-1][0][:10] == transcript[-3][0][:10]


def test_InstrumentEditor_instrument_name_03():
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
