from abjad.components._Component import _Component
from abjad.tools import seqtools
from baca.util.rotate_nested import rotate_nested


def helianthate(l, outer, inner, flattened = True):
   '''Rotate inner lists and outer list simultaneously 
   and accumulate results until identity.

   abjad> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   abjad> util.helianthate(l, -1, 1)
   [1, 2, 3, 4, 5, 6, 7, 8, 5, 4, 8, 6, 7, 3, 1, 2, 7, 8,
      6, 2, 3, 1, 4, 5, 1, 2, 3, 5, 4, 6, 7, 8, 4, 5, 8, 6, 7, 3, 1,
      2, 7, 8, 6, 2, 3, 1, 5, 4]

   abjad> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   abjad> util.helianthate(l, -1, 1, flattened = False)
   [[1, 2, 3], [4, 5], [6, 7, 8], [5, 4], [8, 6, 7], [3, 1, 2], [7, 8, 6], 
      [2, 3, 1], [4, 5], [1, 2, 3], [5, 4], [6, 7, 8], [4, 5], [8, 6, 7], 
      [3, 1, 2], [7, 8, 6], [2, 3, 1], [5, 4]]
   '''

   if not all([not isinstance(x, _Component) for x in l]):
      raise TypeError('function not defined from score components.')

   start = l[:]
   result = l[:]

   if not isinstance(inner, (int, long)) or not isinstance(outer, (int, long)):
      raise TypeError('must be integer.')

   while True:
      last = result[-len(start):]
      input = last
      next = rotate_nested(input, outer, inner)
      if next == start:
         break
      result.extend(next) 

   if flattened:
      result = seqtools.flatten_sequence(result)

   return result
