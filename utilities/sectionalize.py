from abjad import *


def sectionalize(n, ratio):
    '''Sectionalizes `n` by `ratio`.

    ::

        >>> from baca import utilities

    ::

        >>> utilities.sectionalize(20, (1, 1, 1))
        [6, 1, 6, 1, 6]

    ::

        >>> utilities.sectionalize(97, (1, 1, 1))
        [32, 1, 31, 1, 32]

    ::

        >>> utilities.sectionalize(97, (1, 1, 2))
        [24, 1, 24, 1, 47]

    Returns list.
    '''

    parts = mathtools.partition_integer_by_ratio(n - (len(ratio) - 1), ratio)
    result = sequencetools.splice_between_elements(parts, [1])
    return result
