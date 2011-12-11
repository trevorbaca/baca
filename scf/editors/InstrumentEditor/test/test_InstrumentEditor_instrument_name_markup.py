from abjad import *
import baca


def test_InstrumentEditor_instrument_name_markup_01():
    '''Quit, back & studio all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 inm q')
    assert studio.ts == (11, (1, 5, 7))

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 inm b q')
    assert studio.ts == (13, (1, 5, 7), (8, 11))

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 inm studio q')
    assert studio.ts == (13, (0, 11), (1, 5, 7))


def test_InstrumentEditor_instrument_name_markup_02():
    '''String only.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 inm -99 q')
    transcript = studio.transcript
    assert len(transcript) == 13
    assert transcript[-1][0][:10] == transcript[-3][0][:10]
