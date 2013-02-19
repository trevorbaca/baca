from abjad.tools import sequencetools
from baca.util.rotate_nested import rotate_nested


#def helianthate(l, outer_index_of_rotation, inner_index_of_rotation, flattened = True):
def helianthate(sequence, outer_index_of_rotation, inner_index_of_rotation):
    '''Rotate inner_index_of_rotation lists and outer_index_of_rotation list simultaneously
    and accumulate results until identity.

    abjad> sequence = [[1, 2, 3], [4, 5], [6, 7, 8]]
    abjad> util.helianthate(sequence, -1, 1)
    [1, 2, 3, 4, 5, 6, 7, 8, 5, 4, 8, 6, 7, 3, 1, 2, 7, 8,
        6, 2, 3, 1, 4, 5, 1, 2, 3, 5, 4, 6, 7, 8, 4, 5, 8, 6, 7, 3, 1,
        2, 7, 8, 6, 2, 3, 1, 5, 4]

    abjad> sequence = [[1, 2, 3], [4, 5], [6, 7, 8]]
    abjad> util.helianthate(sequence, -1, 1, flattened = False)
    [[1, 2, 3], [4, 5], [6, 7, 8], [5, 4], [8, 6, 7], [3, 1, 2], [7, 8, 6],
        [2, 3, 1], [4, 5], [1, 2, 3], [5, 4], [6, 7, 8], [4, 5], [8, 6, 7],
        [3, 1, 2], [7, 8, 6], [2, 3, 1], [5, 4]]
    '''
    from abjad.tools import componenttools

    if not all([not isinstance(x, componenttools.Component) for x in sequence]):
        raise TypeError('function not defined for score components.')

    start = sequence[:]
    result = sequence[:]

    assert isinstance(outer_index_of_rotation, int), repr(outer_index_of_rotation)
    assert isinstance(inner_index_of_rotation, int), repr(inner_index_of_rotation)

    while True:
        last = result[-len(start):]
        current = last
        candidate = rotate_nested(current, outer_index_of_rotation, inner_index_of_rotation)
        if candidate == start:
            break
        result.extend(candidate)

    return result
