from abjad import *
import baca


def test_baca_pitch_Constellation_get_number_of_chord_01():

   constellation = baca.pitch.CC[0]
   assert constellation.get_number_of_chord(constellation.get_chord(17)) == 17
