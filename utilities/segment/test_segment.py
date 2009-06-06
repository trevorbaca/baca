from baca import utilities


def test_utilities_segment_01( ):

   l = [1] * 10
   t = utilities.segment(l, [2])

   assert t == [[1, 1], [1, 1], [1, 1], [1, 1], [1, 1]]

   
def test_utilities_segment_02( ):

   l = [1] * 10
   t = utilities.segment(l, [2, 3])

   assert t == [[1, 1], [1, 1, 1], [1, 1], [1, 1, 1]]


def test_utilities_segment_03( ):

   l = [1] * 10
   t = utilities.segment(l, [2, 3], cycle = False)

   assert t == [[1, 1], [1, 1, 1]]


#def test_utilities_segment_04( ):
#   '''Function probably never exhibited this behavior.'''
#
#   l = [1]
#   t = utilities.segment(l, [2, 3, 2, 3])
#
#   assert t == [[1]]


def test_utilities_segment_05( ):

   l = [1]
   t = utilities.segment(l, [2, 3, 2, 3], cycle = 'sheet')

   assert t == [[1, 1], [1, 1, 1], [1, 1], [1, 1, 1]]


#def test_utilities_segment_06( ):
#   '''Do not know if function originally returned final [4] or not.'''
#
#   t = utilities.segment(['(1, 1, 1)', 1, 2, -2, 3, '(1, 1, 1)', -2, 4], [8])
#   assert t == [[1, 1, 1, 1, 2, -2], [3, 1, 1, 1, -2], [4]]
