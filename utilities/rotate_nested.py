from abjad.tools import sequencetools


def rotate_nested(l, outer, inner):
    '''Rotates outer list according to 'outer'.
    Rotates inner list according to 'innner'.

        >>> from baca import utilities

    ::

        >>> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
        >>> utilities.rotate_nested(l, 1, 1)
        [[8, 6, 7], [3, 1, 2], [5, 4]]

        >>> utilities.rotate_nested(l, 1, -1)
        [[7, 8, 6], [2, 3, 1], [5, 4]]

        >>> utilities.rotate_nested(l, -1, 1)
        [[5, 4], [8, 6, 7], [3, 1, 2]]

        >>> utilities.rotate_nested(l, -1, -1)
        [[5, 4], [7, 8, 6], [2, 3, 1]]

    '''

    assert isinstance(l, (list, tuple))
    assert all([isinstance(x, list) for x in l])
    assert isinstance(inner, (int, long))
    assert isinstance(outer, (int, long))

    return sequencetools.rotate_sequence(
        [sequencetools.rotate_sequence(x, inner) for x in l], outer)