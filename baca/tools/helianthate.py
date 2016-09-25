# -*- coding: utf-8 -*-
import abjad
from baca.tools.rotate_nested import rotate_nested


def helianthate(sequence, outer_index_of_rotation, inner_index_of_rotation):
    '''Helianthates `sequence`.

    Rotates `inner_index_of_rotation` lists and `outer_index_of_rotation` 
    list simultaneously. 
    
    Accumulates results until identity.

    ::

        >>> import baca

    ::

        >>> sequence = [[1, 2, 3], [4, 5], [6, 7, 8]]
        >>> baca.tools.helianthate(sequence, -1, 1)
        [[1, 2, 3], [4, 5], [6, 7, 8], [5, 4], [8, 6, 7], [3, 1, 2], [7, 8, 6],
            [2, 3, 1], [4, 5], [1, 2, 3], [5, 4], [6, 7, 8], [4, 5], [8, 6, 7],
            [3, 1, 2], [7, 8, 6], [2, 3, 1], [5, 4]]

    '''
    if not all([
        not isinstance(x, abjad.scoretools.Component) for x in sequence]):
        message = 'function not defined for score components.'
        raise TypeError(message)
    start = list(sequence[:])
    result = list(sequence[:])
    assert isinstance(outer_index_of_rotation, int), repr(
        outer_index_of_rotation)
    assert isinstance(inner_index_of_rotation, int), repr(
        inner_index_of_rotation)
    while True:
        last = result[-len(start):]
        current = last
        candidate = rotate_nested(
            current, 
            outer_index_of_rotation, 
            inner_index_of_rotation,
            )
        if candidate == start:
            break
        result.extend(candidate)
    return result
