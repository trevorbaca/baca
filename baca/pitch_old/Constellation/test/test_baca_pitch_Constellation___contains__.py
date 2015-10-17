from abjad import *
import baca


def test_baca_pitch_Constellation___contains___01():

    assert [-38, -36, -34, -29, -28, -25, -21, -20, -19, -18, -15, -11] in baca.pitch_old.CC[0]
    assert not [-38] in baca.pitch_old.CC[0]
