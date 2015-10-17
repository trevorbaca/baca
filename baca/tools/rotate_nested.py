# -*- coding: utf-8 -*-
from abjad.tools import sequencetools


def rotate_nested(l, outer, inner):
    '''Rotates nested lists `l`.

    Rotates lists in `l` according to `outer`.

    Rotates list elements according to `innner`.

    Set `outer` to any integer.

    Set `inner` to any integer.

        >>> from baca import tools

    ::

        >>> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
        >>> tools.rotate_nested(l, 1, 1)
        [[8, 6, 7], [3, 1, 2], [5, 4]]

    ::

        >>> tools.rotate_nested(l, 1, -1)
        [[7, 8, 6], [2, 3, 1], [5, 4]]

    ::

        >>> tools.rotate_nested(l, -1, 1)
        [[5, 4], [8, 6, 7], [3, 1, 2]]

    ::

        >>> tools.rotate_nested(l, -1, -1)
        [[5, 4], [7, 8, 6], [2, 3, 1]]

    '''
    if isinstance(l, tuple):
        l = list(l)
    assert isinstance(l, list)
    assert all([isinstance(x, list) for x in l])
    assert isinstance(inner, int)
    assert isinstance(outer, int)
    return sequencetools.rotate_sequence(
        [sequencetools.rotate_sequence(x, inner) for x in l], outer)