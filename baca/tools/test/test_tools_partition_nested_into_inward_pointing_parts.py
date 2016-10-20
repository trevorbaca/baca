# -*- coding: utf-8 -*-
import baca


def test_tools_partition_nested_into_inward_pointing_parts_01():
    '''Partitions only negative values by default.
    '''

    sequence_ = [[1, 1, 5]]
    parts = baca.tools.partition_nested_into_inward_pointing_parts(sequence_)
    assert parts == [[1, 1, 5]]

    sequence_ = [[1, 1, -5]]
    parts = baca.tools.partition_nested_into_inward_pointing_parts(sequence_)
    assert parts == [[1, 1, 1, -4]]


def test_tools_partition_nested_into_inward_pointing_parts_02():
    '''Partitions positive values according to target.
    '''

    sequence_ = [[1], [5], [5, 1], [1, 5], [5, 5], [1, 5, 1]]
    parts = baca.tools.partition_nested_into_inward_pointing_parts(
        sequence_,
        target='positive',
        )
    assert parts == [
        [1], [4, 1], [4, 1, 1], [1, 1, 4], [4, 1, 1, 4], [1, 4, 1, 1]]

    sequence_ = [[1, 1, -5]]
    parts = baca.tools.partition_nested_into_inward_pointing_parts(
        sequence_,
        target='positive',
        )
    assert parts == [[1, 1, -5]]
