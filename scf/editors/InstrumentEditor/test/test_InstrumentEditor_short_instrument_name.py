from abjad import *
import baca


def test_InstrumentEditor_short_instrument_name_01():
    '''Quit, back & studio all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 setup perf 1 1 sin q')
    assert studio.ts == (13, (1, 7, 9))

    studio.run(user_input='1 setup performers 1 1 sin b q')
    assert studio.ts == (15, (1, 7, 9), (10, 13))

    studio.run(user_input='1 setup performers 1 1 sin studio q')
    assert studio.ts == (15, (0, 13), (1, 7, 9))


def test_InstrumentEditor_short_instrument_name_02():
    '''String only.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 setup performers 1 1 sin -99 q')
    assert studio.ts == (15, (1, 7, 9))


def test_InstrumentEditor_short_instrument_name_03():
    '''Short instrument name changes short instrument name markup.
    Unless short instrument name markup is set explicitly.
    '''

    editor = baca.scf.editors.InstrumentEditor()
    editor.run(user_input="1 sin 'foo' q")
    instrument = editor.target
    assert instrument.short_instrument_name == 'foo'
    assert instrument.short_instrument_name_markup == markuptools.Markup('Foo')

    editor = baca.scf.editors.InstrumentEditor()
    editor.run(user_input="1 sinm 'bar' sin 'foo' q")
    instrument = editor.target
    assert instrument.short_instrument_name == 'foo'
    assert instrument.short_instrument_name_markup == markuptools.Markup('bar')
