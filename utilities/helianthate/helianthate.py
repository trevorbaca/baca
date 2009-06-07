from abjad.leaf.leaf import _Leaf
from abjad.note.note import Note
from abjad.tools import clone
from abjad.tools import listtools
from baca.utilities import rotate_nested as utilities_rotate_nested


## TODO: Clean up docstring with examples from test file instead. ##

def helianthate(l, outer, inner, action = 'in place', flattened = True):
   '''Rotate inner lists and outer list simultaneously and accumulate
   results until identity.

   >>> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   >>> utilities.helianthate(l, 'left', 'right', action = 'new')

   >>> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   >>> utilities.helianthate(l, 'left', 'right', flattened = False, action = 'new')

   >>> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   >>> utilities.helianthate(l, 'left', 'right', action = 'new')[:24]
   [1, 2, 3, 4, 5, 6, 7, 8, 5, 4, 8, 6, 7, 3, 1, 2, 7, 8, 6, 2, 3, 1, 4, 5]

   >>> l = [note.Note(n, 1, 4) for n in range(1, 9)]
   >>> l = listtools.partition_by_counts(l, [3, 2, 3])
   >>> utilities.helianthate(l, 'left', 'right', action = 'new')'''

   if isinstance(l[0][0], _Leaf):
      start = [[n.pitch.pc for n in sublist] for sublist in l]
      result = [ ]
      for sublist in l:
         result.append([clone.unspan([element])[0] for element in sublist])
   else:
      start = l[:]
      result = l[:]

   while True:
      last = result[-len(start):]

      if isinstance(last[0][0], int) or isinstance(last[0][0], str) or \
         isinstance(last[0][0], float) or isinstance(last[0][0], tuple):
         input = last
      else:
         input = [ ]
         for sublist in last:
            new = [ ]
            print sublist
            for n in sublist:
               new.append(clone.unspan([n])[0])
            input.append(new)
               
      next = utilities_rotate_nested(input, outer, inner)

      if next == start or (isinstance(next[0][0], Note) and \
         [[n.pitch.pc for n in sublist] for sublist in next] == start):
         if flattened == True:
            result = listtools.flatten(result)
         break
      else:
         result.extend(next)

   if action == 'in place':
      l[:] = result
   else:
      return result
