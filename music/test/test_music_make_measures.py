from abjad import *
from baca import music


def test_make_measures_01( ):
   t = Voice([Note(n, (1, 8)) for n in range(8)])
   assert len(t) == 8
   leaves_before = t.leaves
   music.makeMeasures(t, [(n, 8) for n in (2, 2, 2, 2)])
   assert len(t) == 4
   leaves_after = t.leaves
   assert leaves_before == leaves_after
   for x in t:
      #assert isinstance(x, Measure)
      assert isinstance(x, Measure)
      assert x.duration.prolated == Rational(2, 8)


def test_make_measures_02( ):
   t = Voice([Note(n, (1, 8)) for n in range(8)])
   assert len(t) == 8
   leaves_before = t.leaves
   music.makeMeasures(t, [(n, 8) for n in (2, 3, 3)])
   assert len(t) == 3
   leaves_after = t.leaves
   assert leaves_before == leaves_after
   for i, x in enumerate(t):
      #assert isinstance(x, Measure)
      assert isinstance(x, Measure)
      if i == 0:
         assert x.duration.prolated == Rational(2, 8)
      else:
         assert x.duration.prolated == Rational(3, 8)
