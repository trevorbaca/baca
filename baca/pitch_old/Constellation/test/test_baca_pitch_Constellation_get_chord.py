from abjad import *
import baca


def test_baca_pitch_Constellation_get_chord_01():

    assert baca.pitch_old.CC[0].get_chord(1) == [-38, -36, -34, -29, -28, -25, -21, -20, -19, -18, -15, -11]
