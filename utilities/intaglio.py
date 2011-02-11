from abjad.tools import mathtools
from abjad.tools import seqtools


def intaglio(l, s, t = 1):
   '''Repeat s and weight-partition according to l.

   abjad> utilities.intaglio([3, 5, 10, 10], [4])
   [[3], [1, 4], [4, 4, 2], [2, 4, 4]]

   abjad> utilities.intaglio([3, 5, 10, 10], [5])
   [[3], [2, 3], [2, 5, 3], [2, 5, 3]]

   abjad> utilities.intaglio([3, 5, 5, 10, 10], [4, 5])
   [[3], [1, 4], [1, 4], [5, 4, 1], [4, 4, 2]]

   Negative values work fine in s.

   abjad> utilities.intaglio([3, 5, 10, 10], [4, -5])
   [[3], [1, -4], [-1, 4, -5], [4, -5, 1]]

   Optional t gloms light-weight sublists.

   abjad> utilities.intaglio([3, 5, 6, 6], [1])
   [[1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]

   abjad> utilities.intaglio([3, 5, 6, 6], [1], t = 5)
   [[3], [5], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]

   Large values of t glom all sublists.

   abjad> utilities.intaglio([3, 5, 6, 6], [1], t = 99)
   [[3], [5], [6], [6]]
   '''

   assert all([isinstance(x, int) and x > 0 for x in l])
   assert all([isinstance(x, int) and x != 0 for x in s])
   assert len(l) > 0
   assert len(s) > 0

   result = [ ]

   result = seqtools.repeat_sequence_to_weight_exactly(s, sum(l))
   result = seqtools.split_sequence_once_by_weights_with_overhang(result, l)

   for i, sublist in enumerate(result):
      if mathtools.weight(sublist) <= t:
         result[i] = [seqtools.weight(sublist)]

   return result
