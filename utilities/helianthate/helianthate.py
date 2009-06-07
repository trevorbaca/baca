#from abjad.leaf.leaf import _Leaf
#from abjad.note.note import Note
from abjad.component.component import _Component
from abjad.tools import clone
from abjad.tools import listtools
from baca.utilities.rotate_nested import rotate_nested as \
   utilities_rotate_nested


## TODO: Clean up docstring with examples from test file instead. ##

def helianthate(l, outer, inner, flattened = True):
   '''Rotate inner lists and outer list simultaneously and accumulate
   results until identity.

   >>> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   >>> utilities.helianthate(l, 'left', 'right')

   >>> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   >>> utilities.helianthate(l, 'left', 'right', flattened = False)

   >>> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   >>> utilities.helianthate(l, 'left', 'right')[:24]
   [1, 2, 3, 4, 5, 6, 7, 8, 5, 4, 8, 6, 7, 3, 1, 2, 7, 8, 6, 2, 3, 1, 4, 5]'''

   assert all([not isinstance(x, _Component) for x in l])

#   if isinstance(l[0][0], _Leaf):
#      start = [[n.pitch.pc for n in sublist] for sublist in l]
#      result = [ ]
#      for sublist in l:
#         result.append([clone.unspan([element])[0] for element in sublist])
#   else:
#      start = l[:]
#      result = l[:]

   start = l[:]
   result = l[:]

   while True:
      last = result[-len(start):]

#      if isinstance(last[0][0], (int, float, str, tuple)):
#         input = last
#      else:
#         input = [ ]
#         for sublist in last:
#            new = [ ]
#            for n in sublist:
#               new.append(clone.unspan([n])[0])
#            input.append(new)

      input = last
               
      next = utilities_rotate_nested(input, outer, inner)

#      if next == start or (isinstance(next[0][0], Note) and \
#         [[n.pitch.pc for n in sublist] for sublist in next] == start):
#         if flattened == True:
#            result = listtools.flatten(result)
#         break
#      else:
#         result.extend(next)

      if next == start:
         break

      result.extend(next) 

   if flattened:
      result = listtools.flatten(result)

   return result
