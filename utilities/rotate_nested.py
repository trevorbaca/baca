from abjad.tools import listtools


def rotate_nested(l, outer, inner):
   '''Rotate outer list according to 'outer'.
   Rotate inner list according to 'innner'.

   abjad> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   abjad> utilities.rotate_nested(l, 1, 1)
   [[8, 6, 7], [3, 1, 2], [5, 4]]

   abjad> utilities.rotate_nested(l, 1, -1)
   [[7, 8, 6], [2, 3, 1], [5, 4]]

   abjad> utilities.rotate_nested(l, -1, 1)
   [[5, 4], [8, 6, 7], [3, 1, 2]]

   abjad> utilities.rotate_nested(l, -1, -1)
   [[5, 4], [7, 8, 6], [2, 3, 1]]
   '''

   assert isinstance(l, list)
   assert all([isinstance(x, list) for x in l])
   assert isinstance(inner, (int, long))
   assert isinstance(outer, (int, long))

   return listtools.rotate([listtools.rotate(x, inner) for x in l], outer)
