from abjad import *
import baca


def test_baca_pitch_Constellation___len___01():

    assert len(baca.pitch.CC.get(1)) == 180
