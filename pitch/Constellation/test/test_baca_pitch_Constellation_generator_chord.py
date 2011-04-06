from abjad import *
import baca


def test_baca_pitch_Constellation_generator_chord_01( ):

   assert baca.pitch.CC[0].generator_chord == Chord("<c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4")
