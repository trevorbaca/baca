from baca import util


def test_baca_sectionalize_01( ):

   t = util.sectionalize(20, (1, 1, 1))
   assert t == [6, 1, 6, 1, 6]

   t = util.sectionalize(97, (1, 1, 1))
   assert t == [32, 1, 31, 1, 32]

   t = util.sectionalize(97, (1, 1, 2))
   assert t == [24, 1, 24, 1, 47]
