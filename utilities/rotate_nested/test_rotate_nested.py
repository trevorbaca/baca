from baca import utilities


def test_utilities_rotate_nested_01( ):

   l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   
   t = utilities.rotate_nested(l, 'right', 'right')
   assert t == [[8, 6, 7], [3, 1, 2], [5, 4]]


def test_utilities_rotate_nested_02( ):

   l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   
   t = utilities.rotate_nested(l, 'right', 'left')
   assert t == [[7, 8, 6], [2, 3, 1], [5, 4]]


def test_utilities_rotate_nested_03( ):

   l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   
   t = utilities.rotate_nested(l, 'left', 'right')
   assert t == [[5, 4], [8, 6, 7], [3, 1, 2]]


def test_utilities_rotate_nested_04( ):

   l = [[1, 2, 3], [4, 5], [6, 7, 8]]
   
   t = utilities.rotate_nested(l, 'left', 'left')
   assert t == [[5, 4], [7, 8, 6], [2, 3, 1]]
