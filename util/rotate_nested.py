from abjad.tools import sequencetools


def rotate_nested(l, outer, inner):
    '''Rotate outer list according to 'outer'.
    Rotate inner list according to 'innner'.

    abjad> l = [[1, 2, 3], [4, 5], [6, 7, 8]]
    abjad> util.rotate_nested(l, 1, 1)
    [[8, 6, 7], [3, 1, 2], [5, 4]]

    abjad> util.rotate_nested(l, 1, -1)
    [[7, 8, 6], [2, 3, 1], [5, 4]]

    abjad> util.rotate_nested(l, -1, 1)
    [[5, 4], [8, 6, 7], [3, 1, 2]]

    abjad> util.rotate_nested(l, -1, -1)
    [[5, 4], [7, 8, 6], [2, 3, 1]]
    '''

    assert isinstance(l, list)
    assert all([isinstance(x, list) for x in l])
    assert isinstance(inner, (int, long))
    assert isinstance(outer, (int, long))

    return sequencetools.rotate_sequence([sequencetools.rotate_sequence(x, inner) for x in l], outer)
