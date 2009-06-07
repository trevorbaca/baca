from abjad.tools import listtools


## TODO: Replace outer and inner strings with signed integer values. ##

def rotate_nested(l, outer, inner):
   '''Rotate outer list according to 'outer' and 
   inner list according to 'innner'.

   >>> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   >>> rotate_nested(l, 'right', 'right')
   [[8, 6, 7], [3, 1, 2], [5, 4]]

   >>> rotate_nested(l, 'right', 'left')
   [[7, 8, 6], [2, 3, 1], [5, 4]]

   >>> rotate_nested(l, 'left', 'right')
   [[5, 4], [8, 6, 7], [3, 1, 2]]

   >>> rotate_nested(l, 'left', 'left')
   [[5, 4], [7, 8, 6], [2, 3, 1]]'''

   assert isinstance(l, list)
   assert all([isinstance(x, list) for x in l])
   assert inner in ('left', 'right')
   assert outer in ('left', 'right')

   return listtools.rotate([
      listtools.rotate(x, inner) for x in l], outer)
