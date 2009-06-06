from abjad.tools import listtools
from abjad.tools import mathtools


def sectionalize(n, ratio):
   '''
   >>> utilities.sectionalize(20, (1, 1, 1))
   [6, 1, 6, 1, 6]

   >>> utilities.sectionalize(97, (1, 1, 1))
   [32, 1, 31, 1, 32]

   >>> utilities.sectionalize(97, (1, 1, 2))
   [24, 1, 24, 1, 47]
   '''

   parts = mathtools.integer_partition_by_ratio(n - (len(ratio) - 1), ratio)
   result = listtools.insert_slice_cyclic(parts, [1])
   return result
