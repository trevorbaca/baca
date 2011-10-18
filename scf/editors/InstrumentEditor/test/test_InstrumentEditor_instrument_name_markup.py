from abjad import *
import baca


def test_InstrumentEditor_instrument_name_markup_01():
    '''Quit, back & studio all work.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 inm q')
    assert len(studio.transcript) == 11

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 inm b q')
    transcript = studio.transcript
    assert len(transcript) == 13
    assert transcript[-2] == transcript[-5]

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 inm studio q')
    transcript = studio.transcript
    assert len(transcript) == 13
    assert transcript[-2] == transcript[-13]


def test_InstrumentEditor_instrument_name_markup_02():
    '''String only.
    '''

    studio = baca.scf.Studio()
    studio.run(user_input='1 perf 1 1 inm -99 q')
    transcript = studio.transcript
    assert len(transcript) == 13
    assert transcript[-1][0][:10] == transcript[-3][0][:10]
