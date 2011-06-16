from abjad import *
import baca


def test_baca_pitch_Constellation_constellation_number_01():

    assert baca.pitch.CC[0].constellation_number == 1
    assert baca.pitch.CC[1].constellation_number == 2
    assert baca.pitch.CC[2].constellation_number == 3
    assert baca.pitch.CC[3].constellation_number == 4
    assert baca.pitch.CC[4].constellation_number == 5
    assert baca.pitch.CC[5].constellation_number == 6
    assert baca.pitch.CC[6].constellation_number == 7
    assert baca.pitch.CC[7].constellation_number == 8
