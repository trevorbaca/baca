# -*- coding: utf-8 -*-
from abjad import *


def intaglio(l, s, t=1):
    '''Repeats s and weight-partition according to l.

        >>> from baca import utilities

    ::

        >>> utilities.intaglio([3, 5, 10, 10], [4])
        [[3], [1, 4], [4, 4, 2], [2, 4, 4]]

        >>> utilities.intaglio([3, 5, 10, 10], [5])
        [[3], [2, 3], [2, 5, 3], [2, 5, 3]]

        >>> utilities.intaglio([3, 5, 5, 10, 10], [4, 5])
        [[3], [1, 4], [1, 4], [5, 4, 1], [4, 4, 2]]

    Negative values work fine in s.

    ::

        >>> utilities.intaglio([3, 5, 10, 10], [4, -5])
        [[3], [1, -4], [-1, 4, -5], [4, -5, 1]]

    Optional t gloms light-weight sublists.

    ::

        >>> utilities.intaglio([3, 5, 6, 6], [1])
        [[1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]

        >>> utilities.intaglio([3, 5, 6, 6], [1], t = 5)
        [[3], [5], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]

    Large values of t glom all sublists.

    ::

        >>> utilities.intaglio([3, 5, 6, 6], [1], t = 99)
        [[3], [5], [6], [6]]

    '''

    assert all([isinstance(x, int) and x > 0 for x in l])
    assert all([isinstance(x, int) and x != 0 for x in s])
    assert 0 < len(l)
    assert 0 < len(s)

    result = []

    result = sequencetools.repeat_sequence_to_weight(s, sum(l))
    result = sequencetools.split_sequence(
        result, 
        l, 
        cyclic=False, 
        overhang=True,
        )

    for i, sublist in enumerate(result):
        if mathtools.weight(sublist) <= t:
            result[i] = [mathtools.weight(sublist)]

    return result