from baca import utilities


def test_utilities_unfive_01( ):
   '''Partition only negative values by default.'''
   
   l = [[1, 1, 5]]
   t = utilities.unfive(l)
   assert t == [[1, 1, 5]]

   l = [[1, 1, -5]]
   t = utilities.unfive(l)
   assert t == [[1, 1, 1, -4]]


def test_utilities_unfive_02( ):
   '''Partition positive values according to target.'''

   l = [[1], [5], [5, 1], [1, 5], [5, 5], [1, 5, 1]]
   t = utilities.unfive(l, target = 'positive')
   assert t == [[1], [4, 1], [4, 1, 1], [1, 1, 4], [4, 1, 1, 4], [1, 4, 1, 1]]

   l = [[1, 1, -5]]
   t = utilities.unfive(l, target = 'positive')
   assert t == [[1, 1, -5]]
