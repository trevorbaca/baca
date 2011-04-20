from baca import util


def test_baca_partition_nested_into_canonic_parts_01( ):

#   t = util.partition_nested_into_canonic_parts(41)
#   assert t == (32, 8, 1)

#   t = util.partition_nested_into_canonic_parts(-41)
#   assert t == (-32, -8, -1)

   t = util.partition_nested_into_canonic_parts([2, 3, 9, 41])
   assert t == [2, 3, 8, 1, 32, 8, 1]

   t = util.partition_nested_into_canonic_parts([2, [3, 9], 41])
   assert t == [2, [3, 8, 1], 32, 8, 1]


def test_baca_partition_nested_into_canonic_parts_02( ):

   t = util.partition_nested_into_canonic_parts([-2, -3, -9, -41])
   assert t == [-2, -3, -8, -1, -32, -8, -1]

   t = util.partition_nested_into_canonic_parts([-2, [-3, -9], -41])
   assert t == [-2, [-3, -8, -1], -32, -8, -1]
