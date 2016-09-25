# -*- coding: utf-8 -*-
import abjad


def sectionalize(n, ratio):
    '''Sectionalizes `n` by `ratio`.

    ::

        >>> import baca

    ::

        >>> baca.tools.sectionalize(20, (1, 1, 1))
        [6, 1, 6, 1, 6]

    ::

        >>> baca.tools.sectionalize(97, (1, 1, 1))
        [32, 1, 31, 1, 32]

    ::

        >>> baca.tools.sectionalize(97, (1, 1, 2))
        [24, 1, 24, 1, 47]

    Returns list.
    '''
    parts = abjad.mathtools.partition_integer_by_ratio(n-(len(ratio)-1), ratio)
    result = abjad.sequencetools.splice_between_elements(parts, [1])
    return result
