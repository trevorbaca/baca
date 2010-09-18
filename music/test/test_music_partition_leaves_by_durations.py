from abjad import *
from baca import music


def test_partition_leaves_by_durations_01( ):
   #v = Voice([
   #   divide.pair([1, -4, 1], (1, 4)), 
   #   divide.pair([1, -4, 1, 1], (1, 4))])
   v = Voice([
      tuplettools.make_tuplet_from_proportions_and_pair([1, -4, 1], (1, 4)), 
      tuplettools.make_tuplet_from_proportions_and_pair([1, -4, 1, 1], (1, 4))])

   assert len(v.leaves) == 7
   result = music.partitionLeavesByDurations(v.leaves, [(1, 4)])
   assert len(result) == 2
   assert [len(x) for x in result] == [3, 4]


def test_partition_leaves_by_durations_02( ):
   #v = Voice([
   #   divide.pair([1, -4, 1], (1, 4)), 
   #   divide.pair([1, -4, 1, 1], (1, 4))])
   v = Voice([
      tuplettools.make_tuplet_from_proportions_and_pair([1, -4, 1], (1, 4)), 
      tuplettools.make_tuplet_from_proportions_and_pair([1, -4, 1, 1], (1, 4))])
   assert len(v.leaves) == 7
   result = music.partitionLeavesByDurations(v.leaves, [(1, 2)])
   assert len(result) == 1
   assert [len(x) for x in result] == [7]


def test_partition_leaves_by_durations_03( ):
   v = Voice(Note(0, (1, 32)) * 8)
   assert len(v.leaves) == 8
   result = music.partitionLeavesByDurations(v.leaves, [(1, 32), (3, 32)])
   assert len(result) == 4
   assert [len(x) for x in result] == [1, 3, 1, 3]


def test_partition_leaves_by_durations_04( ):
   v = Voice(Note(0, (1, 32)) * 8)
   assert len(v.leaves) == 8
   result = music.partitionLeavesByDurations(v.leaves, [(3, 32)])
   assert len(result) == 3
   assert [len(x) for x in result] == [3, 3, 2]
