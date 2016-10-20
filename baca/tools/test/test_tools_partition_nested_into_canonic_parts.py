# -*- coding: utf-8 -*-
import baca


def test_tools_partition_nested_into_canonic_parts_01():

    parts = baca.tools.partition_nested_into_canonic_parts(41)
    assert parts == (32, 8, 1)

    parts = baca.tools.partition_nested_into_canonic_parts(-41)
    assert parts == (-32, -8, -1)

    parts = baca.tools.partition_nested_into_canonic_parts([2, 3, 9, 41])
    assert parts == [2, 3, 8, 1, 32, 8, 1]

    parts = baca.tools.partition_nested_into_canonic_parts([2, [3, 9], 41])
    assert parts == [2, [3, 8, 1], 32, 8, 1]


def test_tools_partition_nested_into_canonic_parts_02():

    parts = baca.tools.partition_nested_into_canonic_parts([-2, -3, -9, -41])
    assert parts == [-2, -3, -8, -1, -32, -8, -1]

    parts = baca.tools.partition_nested_into_canonic_parts([-2, [-3, -9], -41])
    assert parts == [-2, [-3, -8, -1], -32, -8, -1]
