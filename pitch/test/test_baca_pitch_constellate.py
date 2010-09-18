from abjad.tools import pitchtools
from constellate import constellate


def test_pitch_constellate_01( ):

   pitch_range = pitchtools.PitchRange(0, 37)
   t = constellate([[0, 2, 10], [16, 19, 20]], pitch_range)

   assert t == [[0, 2, 4, 7, 8, 10], [0, 2, 10, 16, 19, 20], [0, 2, 10, 28, 31, 32], [4, 7, 8, 12, 14, 22], [12, 14, 16, 19, 20, 22], [12, 14, 22, 28, 31, 32], [4, 7, 8, 24, 26, 34], [16, 19, 20, 24, 26, 34], [24, 26, 28, 31, 32, 34]]


def test_pitch_constellate_02( ):

   pitch_range = pitchtools.PitchRange(0, 37)
   t = constellate([[4, 8, 11], [7, 15, 17]], pitch_range)

   assert t == [[4, 7, 8, 11, 15, 17], [4, 8, 11, 19, 27, 29], [7, 15, 16, 17, 20, 23], [16, 19, 20, 23, 27, 29], [7, 15, 17, 28, 32, 35], [19, 27, 28, 29, 32, 35]]
