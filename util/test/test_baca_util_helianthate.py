from abjad import *
from baca import util


def test_baca_util_helianthate_01():

   l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   t = util.helianthate(l, -1, 1)

   assert t == [[1, 2, 3], [4, 5], [6, 7, 8], [5, 4], [8, 6, 7], [3, 1, 2], [7, 8, 6], 
      [2, 3, 1], [4, 5], [1, 2, 3], [5, 4], [6, 7, 8], [4, 5], [8, 6, 7], 
      [3, 1, 2], [7, 8, 6], [2, 3, 1], [5, 4]]
