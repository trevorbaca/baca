from abjad.components._Component import _Component
from abjad.tools import listtools
from baca.utilities.rotate_nested import rotate_nested


## TODO: Clean up docstring with examples from test file instead. ##

def helianthate(l, outer, inner, flattened = True):
   '''Rotate inner lists and outer list simultaneously and accumulate
   results until identity.

   abjad> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   abjad> utilities.helianthate(l, -1, 1)

   abjad> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   abjad> utilities.helianthate(l, -1, 1, flattened = False)

   abjad> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   abjad> utilities.helianthate(l, -1, 1)[:24]
   [1, 2, 3, 4, 5, 6, 7, 8, 5, 4, 8, 6, 7, 3, 1, 2, 7, 8, 6, 2, 3, 1, 4, 5]
   '''

   assert all([not isinstance(x, _Component) for x in l])

   start = l[:]
   result = l[:]

#   if inner == 'right':
#      inner = 1
#   elif inner == 'left':
#      inner = -1
#   else:
#      raise ValueError
#
#   if outer == 'right':
#      outer = 1
#   elif outer == 'left':
#      outer = -1
#   else:
#      raise ValueError

   assert isinstance(inner, (int, long))
   assert isinstance(outer, (int, long))

   while True:
      last = result[-len(start):]
      input = last
      next = rotate_nested(input, outer, inner)
      if next == start:
         break
      result.extend(next) 

   if flattened:
      result = listtools.flatten(result)

   return result
