from baca import utilities


def test_baca_util_partition_nested_into_canonic_parts_01():

#   t = utilities.partition_nested_into_canonic_parts(41)
#   assert t == (32, 8, 1)

#   t = utilities.partition_nested_into_canonic_parts(-41)
#   assert t == (-32, -8, -1)

    t = utilities.partition_nested_into_canonic_parts([2, 3, 9, 41])
    assert t == [2, 3, 8, 1, 32, 8, 1]

    t = utilities.partition_nested_into_canonic_parts([2, [3, 9], 41])
    assert t == [2, [3, 8, 1], 32, 8, 1]


def test_baca_util_partition_nested_into_canonic_parts_02():

    t = utilities.partition_nested_into_canonic_parts([-2, -3, -9, -41])
    assert t == [-2, -3, -8, -1, -32, -8, -1]

    t = utilities.partition_nested_into_canonic_parts([-2, [-3, -9], -41])
    assert t == [-2, [-3, -8, -1], -32, -8, -1]
