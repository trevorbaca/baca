from abjad import *
from baca import utilities


def test_utilities_helianthate_01( ):

   l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   t = utilities.helianthate(l, 'left', 'right', action = 'new')

   assert t == [1, 2, 3, 4, 5, 6, 7, 8, 5, 4, 8, 6, 7, 3, 1, 2, 7, 8, 
      6, 2, 3, 1, 4, 5, 1, 2, 3, 5, 4, 6, 7, 8, 4, 5, 8, 6, 7, 3, 1, 
      2, 7, 8, 6, 2, 3, 1, 5, 4]


def test_utilities_helianthate_02( ):

   l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   t = utilities.helianthate(l, 'left', 'right', flattened = False, action = 'new')

   assert t == [[1, 2, 3], [4, 5], [6, 7, 8], [5, 4], [8, 6, 7], [3, 1, 2], [7, 8, 6], [2, 3, 1], [4, 5], [1, 2, 3], [5, 4], [6, 7, 8], [4, 5], [8, 6, 7], [3, 1, 2], [7, 8, 6], [2, 3, 1], [5, 4]]


def test_utilities_helianthate_03( ):

   l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   t = utilities.helianthate(l, 'left', 'right', action = 'new')

   assert t == [1, 2, 3, 4, 5, 6, 7, 8, 5, 4, 8, 6, 7, 3, 1, 2, 
      7, 8, 6, 2, 3, 1, 4, 5, 1, 2, 3, 5, 4, 6, 7, 8, 4, 5, 8, 6, 
      7, 3, 1, 2, 7, 8, 6, 2, 3, 1, 5, 4]


def test_utilities_helianthate_04( ):

   l = [Note(n, (1, 4)) for n in range(1, 9)]
   l = listtools.partition_by_counts(l, [3, 2, 3])
   t = utilities.helianthate(l, 'left', 'right', action = 'new')  

   assert all([isinstance(x, Note) for x in t])
   assert [x.pitch.number for x in t] == [1, 2, 3, 4, 5, 6, 7, 8, 5, 4, 8, 6, 7, 3, 1, 2, 7, 8, 6, 2, 3, 1, 4, 5, 1, 2, 3, 5, 4, 6, 7, 8, 4, 5, 8, 6, 7, 3, 1, 2, 7, 8, 6, 2, 3, 1, 5, 4]
