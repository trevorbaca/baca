from abjad import *
import baca


def test_baca_pitch_Constellation___getitem___01():

   assert baca.pitch.CC[0][0] == [-38, -36, -34, -29, -28, -25, -21, -20, -19, -18, -15, -11]
