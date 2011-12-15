from abjad import *
import baca


def test_InstrumentEditor_instrument_name_01():
    '''Quit, back & studio all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 in q')
    assert studio.ts == (11, (1, 5, 7))

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 in b q')
    assert studio.ts == (13, (1, 5, 7), (8, 11))

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 in studio q')
    assert studio.ts == (13, (0, 11), (1, 5, 7))


def test_InstrumentEditor_instrument_name_02():
    '''String only.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 in -99 q')
    transcript = studio.transcript
    assert len(transcript) == 13
    assert transcript[-1][0][:10] == transcript[-3][0][:10]


def test_InstrumentEditor_instrument_name_03():
    '''Instrument name changes instrument name markup.
    Unless instrument name markup is set explicitly.
    '''

    editor = baca.scf.editors.InstrumentEditor()
    editor.run(user_input="1 in 'foo' q")
    instrument = editor.target
    assert instrument.instrument_name == 'foo'
    assert instrument.instrument_name_markup == markuptools.Markup('Foo')

    editor = baca.scf.editors.InstrumentEditor()
    editor.run(user_input="1 inm 'bar' in 'foo' q")
    instrument = editor.target
    assert instrument.instrument_name == 'foo'
    assert instrument.instrument_name_markup == markuptools.Markup('bar')
