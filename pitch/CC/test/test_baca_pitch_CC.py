from abjad.tools import pitchtools
import baca


def test_baca_pitch_CC_01( ):
   assert len(baca.pitch.CC) == 8


def test_baca_pitch_CC_02( ):
   pitch_range = pitchtools.PitchRange(-39, 48)
   assert baca.pitch.CC.pitch_range == pitch_range


def test_baca_pitch_CC_03( ):
   generator_numbers = [80, 59, 56, 60, 83, 65, 79, 94]
   assert baca.pitch.CC._generator_numbers == generator_numbers


def test_baca_pitch_CC_04( ):
   pivot_numbers = [80, 75, 60, 73, 117, 69, 108, 99]
   assert baca.pitch.CC._pivot_numbers == pivot_numbers
