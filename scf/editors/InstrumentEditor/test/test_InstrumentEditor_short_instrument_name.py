from abjad import *
import baca


def test_InstrumentEditor_short_instrument_name_01():
    '''Quit, back & studio all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 sin q')
    assert len(studio.transcript) == 11

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 sin b q')
    transcript = studio.transcript
    assert len(transcript) == 13
    assert transcript[-2] == transcript[-5]

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 sin studio q')
    transcript = studio.transcript
    assert len(transcript) == 13
    assert transcript[-2] == transcript[-13]


def test_InstrumentEditor_short_instrument_name_02():
    '''String only.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 sin -99 q')
    transcript = studio.transcript
    assert len(transcript) == 13
    assert transcript[-1][0][:10] == transcript[-3][0][:10]


def test_InstrumentEditor_short_instrument_name_03():
    '''Short instrument name changes short instrument name markup.
    Unless short instrument name markup is set explicitly.
    '''

    editor = baca.scf.editors.InstrumentEditor()
    editor.run(user_input='1 sin foo q')
    instrument = editor.target
    assert instrument.short_instrument_name == 'foo'
    assert instrument.short_instrument_name_markup == markuptools.Markup('foo')

    editor = baca.scf.editors.InstrumentEditor()
    editor.run(user_input='1 sinm bar sin foo q')
    instrument = editor.target
    assert instrument.short_instrument_name == 'foo'
    assert instrument.short_instrument_name_markup == markuptools.Markup('bar')
