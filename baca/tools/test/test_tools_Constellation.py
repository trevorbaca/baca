# -*- coding: utf-8 -*-
import abjad
import baca


def test_tools_Constellation_01():

    CC = baca.tools.make_CC()
    assert isinstance(CC[0], baca.tools.Constellation)


def test_tools_Constellation_02():
    r'''__contains__.
    '''

    CC = baca.tools.make_CC()
    field = [-38, -36, -34, -29, -28, -25, -21, -20, -19, -18, -15, -11]
    assert field in CC[0]
    assert not [-38] in CC[0]


def test_tools_Constellation_03():
    r'''__getitem__.
    '''

    CC = baca.tools.make_CC()
    field = [-38, -36, -34, -29, -28, -25, -21, -20, -19, -18, -15, -11]
    assert CC[0][0] == field


def test_tools_Constellation_04():
    r'''__len__.
    '''

    CC = baca.tools.make_CC()
    assert len(CC.get(1)) == 180


def test_tools_Constellation_05():
    r'''constellation_number.
    '''

    CC = baca.tools.make_CC()
    assert CC[0].constellation_number == 1
    assert CC[1].constellation_number == 2
    assert CC[2].constellation_number == 3
    assert CC[3].constellation_number == 4
    assert CC[4].constellation_number == 5
    assert CC[5].constellation_number == 6
    assert CC[6].constellation_number == 7
    assert CC[7].constellation_number == 8


def test_tools_Constellation_06():
    r'''generator chord.
    '''

    CC = baca.tools.make_CC()
    chord = abjad.Chord("<c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4")
    assert CC[0].generator_chord.written_pitches == chord.written_pitches


def test_tools_Constellation_07():
    r'''get_chord().
    '''

    CC = baca.tools.make_CC()
    chord = [-38, -36, -34, -29, -28, -25, -21, -20, -19, -18, -15, -11]
    assert CC[0].get_chord(1) == chord


def test_tools_Constellation_08():
    r'''get_numbrer_of_chord().
    '''

    CC = baca.tools.make_CC()
    constellation = CC[0]
    assert constellation.get_number_of_chord(constellation.get_chord(17)) == 17


def test_tools_Constellation_09():
    r'''generator_chromatic_pitch_numbers().
    '''

    CC = baca.tools.make_CC()

    assert CC[0].partitioned_generator_pitch_numbers == \
        [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
    assert CC[1].partitioned_generator_pitch_numbers == \
        [[-12, -10, -2], [4, 11, 27, 33, 37], [8, 17, 19, 30]]
    assert CC[2].partitioned_generator_pitch_numbers == \
        [[-8, 2, 15, 25], [-1, 20, 29, 31], [0, 10, 21, 42]]
    assert CC[3].partitioned_generator_pitch_numbers == \
        [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]]
    assert CC[4].partitioned_generator_pitch_numbers == \
        [[-12, -9, 1, 4], [-1, 18, 20, 33], [14, 19, 22, 29]]
    assert CC[5].partitioned_generator_pitch_numbers == \
        [[-10, -2, 0, 5], [-5, 3, 13, 16], [11, 30, 32, 45]]
    assert CC[6].partitioned_generator_pitch_numbers == \
        [[-10, -2, 5, 15, 25], [-1, 7, 18, 20], [0, 28, 33]]
    assert CC[7].partitioned_generator_pitch_numbers == \
        [[-12, 17, 27, 37], [-1, 7, 18, 21], [2, 10, 16, 20]]


def test_tools_Constellation_10():
    r'''pitch_range.
    '''

    CC = baca.tools.make_CC()
    assert CC[0].pitch_range == abjad.pitchtools.PitchRange('[A0, C8]')


def test_tools_Constellation_11():
    r'''pivot chord.
    '''

    CC = baca.tools.make_CC()
    chord = abjad.Chord("<c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4")
    assert CC[0].pivot_chord.written_pitches == chord.written_pitches
