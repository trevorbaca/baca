from abjad.tools import mathtools
from abjad.tools import sequencetools


def sectionalize(n, ratio):
   '''
   >>> util.sectionalize(20, (1, 1, 1))
   [6, 1, 6, 1, 6]

   >>> util.sectionalize(97, (1, 1, 1))
   [32, 1, 31, 1, 32]

   >>> util.sectionalize(97, (1, 1, 2))
   [24, 1, 24, 1, 47]
   '''

   parts = mathtools.partition_integer_by_ratio(n - (len(ratio) - 1), ratio)
   result = sequencetools.splice_new_elements_between_sequence_elements(parts, [1])
   return result
