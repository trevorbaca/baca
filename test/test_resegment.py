from utilities import resegment

w = [[10], [10, 10, 10], [1], [3], [4], [5], [1], [2], [10, 10]]

def test_resegment_01( ):
   result = resegment(w, [10])
   assert result == [[10], [10], [10], [10], [1, 3, 4, 5], [1, 2, 10], [10]]

def test_resegment_02( ):
   result = resegment(w, [10, 15])
   assert result == [[10], [10, 10], [10], [1, 3, 4, 5, 1, 2], [10], [10]]

def test_resegment_03( ):
   result = resegment(w, [15])
   assert result == [[10, 10], [10, 10], [1, 3, 4, 5, 1, 2], [10, 10]]

#def test_resegment_04( ):
#   '''Use max to limit sublist length.'''
#   result = resegment(w, [15], max = 1)
#   assert result == [[10], [10], [10], [10], [1], [3], [4], [5], 
#      [1], [2], [10], [10]]
