from abjad.rational import Rational
from abjad.tools import listtools
from abjad.tools import mathtools


def partition_to_avoid_octave_adjacencies(l, direction):
   '''Partition to avoid octave adjacencies.'''

   assert direction in ('left', 'right')
   
   result = [[ ]]
   part = result[-1]
   
   for x in l:
      if not isinstance(x, (int, float, long, Rational)):
         raise ValueError
      if x % 12 in [y % 12 for y in part]:
         first_value = [y for y in part if y % 12 == x % 12][0]
         first_index = part.index(first_value)
         ## partition current part into left and middle subparts
         old_part = part[:first_index+1]
         disputed_part = part[first_index+1:]
         new_part = [ ]
         ## divvy up disputed part
         left, right = mathtools.partition_integer_into_halves(
            len(disputed_part), bigger = direction)

         disputed_parts = listtools.partition_by_lengths(
            disputed_part, [left, right])
         left_disputed_part, right_disputed_part = disputed_parts

         assert len(left_disputed_part) == left
         assert len(right_disputed_part) == right
         old_part.extend(left_disputed_part)
         new_part.extend(right_disputed_part)
         ## replace last sublist in result with old, trimmed part
         result[-1] = old_part
         ## append new part to result
         result.append(new_part)
         part = result[-1]
      part.append(x)

   result = [tuple(x) for x in result]

   return result
