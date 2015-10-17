from baca import tools


def test_tools_partition_nested_into_inward_pointing_parts_01():
    '''Partition only negative values by default.
    '''

    l = [[1, 1, 5]]
    t = tools.partition_nested_into_inward_pointing_parts(l)
    assert t == [[1, 1, 5]]

    l = [[1, 1, -5]]
    t = tools.partition_nested_into_inward_pointing_parts(l)
    assert t == [[1, 1, 1, -4]]


def test_tools_partition_nested_into_inward_pointing_parts_02():
    '''Partition positive values according to target.
    '''

    l = [[1], [5], [5, 1], [1, 5], [5, 5], [1, 5, 1]]
    t = tools.partition_nested_into_inward_pointing_parts(
        l, target = 'positive')
    assert t == [[1], [4, 1], [4, 1, 1], [1, 1, 4], [4, 1, 1, 4], [1, 4, 1, 1]]

    l = [[1, 1, -5]]
    t = tools.partition_nested_into_inward_pointing_parts(
        l, target = 'positive')
    assert t == [[1, 1, -5]]
