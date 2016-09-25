# -*- coding: utf-8 -*-
import abjad


def intaglio(l, s, t=1):
    '''Repeats `s` and weight-partitions according to `l`.

    ::

        >>> import baca

    ::

        >>> baca.tools.intaglio([3, 5, 10, 10], [4])
        [[3], [1, 4], [4, 4, 2], [2, 4, 4]]

    ::

        >>> baca.tools.intaglio([3, 5, 10, 10], [5])
        [[3], [2, 3], [2, 5, 3], [2, 5, 3]]

    ::

        >>> baca.tools.intaglio([3, 5, 5, 10, 10], [4, 5])
        [[3], [1, 4], [1, 4], [5, 4, 1], [4, 4, 2]]

    Negative values work fine in `s`:

    ::

        >>> baca.tools.intaglio([3, 5, 10, 10], [4, -5])
        [[3], [1, -4], [-1, 4, -5], [4, -5, 1]]

    Optional `t` gloms light-weight sublists:

    ::

        >>> baca.tools.intaglio([3, 5, 6, 6], [1])
        [[1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]

    ::

        >>> baca.tools.intaglio([3, 5, 6, 6], [1], t = 5)
        [[3], [5], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]]

    Large values of `t` glom all sublists:

    ::

        >>> baca.tools.intaglio([3, 5, 6, 6], [1], t=99)
        [[3], [5], [6], [6]]

    '''
    assert all([isinstance(x, int) and x > 0 for x in l])
    assert all([isinstance(x, int) and x != 0 for x in s])
    assert 0 < len(l)
    assert 0 < len(s)
    result = []
    result = abjad.sequencetools.repeat_sequence_to_weight(s, sum(l))
    result = abjad.sequencetools.split_sequence(
        result, 
        l, 
        cyclic=False, 
        overhang=True,
        )
    for i, sublist in enumerate(result):
        if abjad.mathtools.weight(sublist) <= t:
            result[i] = [abjad.mathtools.weight(sublist)]
    return result
