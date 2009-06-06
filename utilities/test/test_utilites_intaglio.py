from abjad import *
from baca.utilities import utilities
import py.test


def test_utilities_intaglio_01( ):
   '''One-element s is allowed.'''
   l, s = [3, 5, 10, 10], [4]
   result = utilities.intaglio(l, s)
   assert result == [[3], [1, 4], [4, 4, 2], [2, 4, 4]]
   assert len(l) == len(result)
   assert [listtools.weight(x) for x in result] == l


def test_utilities_intaglio_02( ):
   l, s = [3, 5, 10, 10], [5]
   result = utilities.intaglio(l, s)
   assert result == [[3], [2, 3], [2, 5, 3], [2, 5, 3]]
   assert len(l) == len(result)
   assert [listtools.weight(x) for x in result] == l


def test_utilities_intaglio_03( ):
   '''Multielement s is allowed.'''
   l, s = [3, 5, 10, 10], [4, 5]
   result = utilities.intaglio(l, s)
   assert result == [[3], [1, 4], [1, 4, 5], [4, 5, 1]]
   assert len(l) == len(result)
   assert [listtools.weight(x) for x in result] == l


def test_utilities_intaglio_04( ):
   '''s can contain negative values.'''
   l, s = [3, 5, 10, 10], [4, -5]
   result = utilities.intaglio(l, s)
   assert result == [[3], [1, -4], [-1, 4, -5], [4, -5, 1]]
   assert len(l) == len(result)
   assert [listtools.weight(x) for x in result] == l


def test_utilities_intaglio_04( ):
   '''l must be nonempty and contain positive integers only.'''
   assert py.test.raises(AssertionError, 'utilities.intaglio([ ], [4])')
   assert py.test.raises(AssertionError, 
      'utilities.intaglio([-3, 5, 10, 10], [4])')
   assert py.test.raises(AssertionError, 
      'utilities.intaglio([0, 5, 10, 10], [4])')
   assert py.test.raises(AssertionError, 
      'utilities.intaglio([3.2, 5, 10, 10], [4])')


def test_utilities_intaglio_05( ):
   '''s must be nonempty and contain nonzero integers only.'''
   assert py.test.raises(AssertionError, 
      'utilities.intaglio([3, 5, 10, 10], [ ])')
   assert py.test.raises(AssertionError, 
      'utilities.intaglio([3, 5, 10, 10], [0])')
   assert py.test.raises(AssertionError, 
      'utilities.intaglio([3, 5, 10, 10], [2.2])')
