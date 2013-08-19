from abjad import *
import baca


def test_baca_pitch_Constellation_pitch_range_01():

    assert baca.pitch.CC[0].pitch_range == pitchtools.PitchRange(
        (pitchtools.NamedPitch('a,,,'), 'inclusive'),
        (pitchtools.NamedPitch("c'''''"), 'inclusive'))
