from abjad import *
import baca


def test_baca_pitch_Constellation_pitch_range_01():

    assert baca.pitch_old.CC[0].pitch_range == pitchtools.PitchRange('[A0, C8]')