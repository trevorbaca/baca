"""
Sequence.
"""

import copy
import itertools

import abjad

from . import math as _math


def accumulate(sequence: list, operands=(), count=None):
    r"""
    Accumulates ``operands`` calls against sequence to identity.

    ..  container:: example

        Accumulates identity operator:

        >>> collection_1 = abjad.PitchClassSegment([0, 1, 2, 3])
        >>> collection_2 = abjad.PitchClassSegment([4, 5])
        >>> sequence = [collection_1, collection_2]
        >>> for item in baca.sequence.accumulate(sequence):
        ...     item
        ...
        [PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])]

    ..  container:: example

        Accumulates alpha:

        >>> collection_1 = abjad.PitchClassSegment([0, 1, 2, 3])
        >>> collection_2 = abjad.PitchClassSegment([4, 5])
        >>> sequence = [collection_1, collection_2]
        >>> for item in baca.sequence.accumulate(
        ...     sequence, [lambda _: baca.pcollections.alpha(_)]
        ... ):
        ...     item
        ...
        [PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])]
        [PitchClassSegment([1, 0, 3, 2]), PitchClassSegment([5, 4])]

    ..  container:: example

        Accumulates transposition:

        >>> collection_1 = abjad.PitchClassSegment([0, 1, 2, 3])
        >>> collection_2 = abjad.PitchClassSegment([4, 5])

        >>> sequence = [collection_1, collection_2]
        >>> for item in baca.sequence.accumulate(sequence, [lambda _: _.transpose(n=3)]):
        ...     item
        ...
        [PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])]
        [PitchClassSegment([3, 4, 5, 6]), PitchClassSegment([7, 8])]
        [PitchClassSegment([6, 7, 8, 9]), PitchClassSegment([10, 11])]
        [PitchClassSegment([9, 10, 11, 0]), PitchClassSegment([1, 2])]

    ..  container:: example

        Accumulates alpha followed by transposition:

        >>> collection_1 = abjad.PitchClassSegment([0, 1, 2, 3])
        >>> collection_2 = abjad.PitchClassSegment([4, 5])

        >>> sequence = [collection_1, collection_2]
        >>> for item in baca.sequence.accumulate(
        ...     sequence,
        ...     [lambda _: baca.pcollections.alpha(_), lambda _: _.transpose(n=3)]
        ... ):
        ...     item
        ...
        [PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])]
        [PitchClassSegment([1, 0, 3, 2]), PitchClassSegment([5, 4])]
        [PitchClassSegment([4, 3, 6, 5]), PitchClassSegment([8, 7])]
        [PitchClassSegment([5, 2, 7, 4]), PitchClassSegment([9, 6])]
        [PitchClassSegment([8, 5, 10, 7]), PitchClassSegment([0, 9])]
        [PitchClassSegment([9, 4, 11, 6]), PitchClassSegment([1, 8])]
        [PitchClassSegment([0, 7, 2, 9]), PitchClassSegment([4, 11])]
        [PitchClassSegment([1, 6, 3, 8]), PitchClassSegment([5, 10])]
        [PitchClassSegment([4, 9, 6, 11]), PitchClassSegment([8, 1])]
        [PitchClassSegment([5, 8, 7, 10]), PitchClassSegment([9, 0])]
        [PitchClassSegment([8, 11, 10, 1]), PitchClassSegment([0, 3])]
        [PitchClassSegment([9, 10, 11, 0]), PitchClassSegment([1, 2])]

    ..  container:: example

        Accumulates permutation:

        >>> collection_1 = abjad.PitchClassSegment([0, 1, 2, 3])
        >>> collection_2 = abjad.PitchClassSegment([4, 5])

        >>> row = abjad.TwelveToneRow([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
        >>> sequence = [collection_1, collection_2]
        >>> for item in baca.sequence.accumulate(sequence, [lambda _: row(_)]):
        ...     item
        ...
        [PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])]
        [PitchClassSegment([10, 0, 2, 6]), PitchClassSegment([8, 7])]
        [PitchClassSegment([4, 10, 2, 5]), PitchClassSegment([1, 3])]
        [PitchClassSegment([8, 4, 2, 7]), PitchClassSegment([0, 6])]
        [PitchClassSegment([1, 8, 2, 3]), PitchClassSegment([10, 5])]
        [PitchClassSegment([0, 1, 2, 6]), PitchClassSegment([4, 7])]
        [PitchClassSegment([10, 0, 2, 5]), PitchClassSegment([8, 3])]
        [PitchClassSegment([4, 10, 2, 7]), PitchClassSegment([1, 6])]
        [PitchClassSegment([8, 4, 2, 3]), PitchClassSegment([0, 5])]
        [PitchClassSegment([1, 8, 2, 6]), PitchClassSegment([10, 7])]
        [PitchClassSegment([0, 1, 2, 5]), PitchClassSegment([4, 3])]
        [PitchClassSegment([10, 0, 2, 7]), PitchClassSegment([8, 6])]
        [PitchClassSegment([4, 10, 2, 3]), PitchClassSegment([1, 5])]
        [PitchClassSegment([8, 4, 2, 6]), PitchClassSegment([0, 7])]
        [PitchClassSegment([1, 8, 2, 5]), PitchClassSegment([10, 3])]
        [PitchClassSegment([0, 1, 2, 7]), PitchClassSegment([4, 6])]
        [PitchClassSegment([10, 0, 2, 3]), PitchClassSegment([8, 5])]
        [PitchClassSegment([4, 10, 2, 6]), PitchClassSegment([1, 7])]
        [PitchClassSegment([8, 4, 2, 5]), PitchClassSegment([0, 3])]
        [PitchClassSegment([1, 8, 2, 7]), PitchClassSegment([10, 6])]

    ..  container:: example

        Accumulates permutation followed by transposition:

        >>> collection_1 = abjad.PitchClassSegment([0, 1, 2, 3])
        >>> collection_2 = abjad.PitchClassSegment([4, 5])

        >>> row = abjad.TwelveToneRow([10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])
        >>> sequence = [collection_1, collection_2]
        >>> for item in baca.sequence.accumulate(
        ...     sequence, [lambda _: row(_), lambda _: _.transpose(n=3)],
        ... ):
        ...     item
        ...
        [PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])]
        [PitchClassSegment([10, 0, 2, 6]), PitchClassSegment([8, 7])]
        [PitchClassSegment([1, 3, 5, 9]), PitchClassSegment([11, 10])]
        [PitchClassSegment([0, 6, 7, 9]), PitchClassSegment([11, 4])]
        [PitchClassSegment([3, 9, 10, 0]), PitchClassSegment([2, 7])]
        [PitchClassSegment([6, 9, 4, 10]), PitchClassSegment([2, 3])]
        [PitchClassSegment([9, 0, 7, 1]), PitchClassSegment([5, 6])]
        [PitchClassSegment([9, 10, 3, 0]), PitchClassSegment([7, 5])]
        [PitchClassSegment([0, 1, 6, 3]), PitchClassSegment([10, 8])]
        [PitchClassSegment([10, 0, 5, 6]), PitchClassSegment([4, 1])]
        [PitchClassSegment([1, 3, 8, 9]), PitchClassSegment([7, 4])]
        [PitchClassSegment([0, 6, 1, 9]), PitchClassSegment([3, 8])]
        [PitchClassSegment([3, 9, 4, 0]), PitchClassSegment([6, 11])]
        [PitchClassSegment([6, 9, 8, 10]), PitchClassSegment([5, 11])]
        [PitchClassSegment([9, 0, 11, 1]), PitchClassSegment([8, 2])]
        [PitchClassSegment([9, 10, 11, 0]), PitchClassSegment([1, 2])]

    Returns sequence of accumulated sequences.

    Returns sequence of length ``count`` + 1 with integer ``count``.

    Returns sequence of orbit length with ``count`` set to identity.
    """
    if count is None:
        count = abjad.EXACT
    operands = operands or [lambda _: _]
    if not isinstance(operands, list):
        operands = [operands]
    items = [sequence]
    if count == abjad.EXACT:
        for i in range(1000):
            sequence = items[-1]
            for operand in operands:
                sequence = type(sequence)([operand(_) for _ in sequence])
                items.append(sequence)
            if sequence == items[0]:
                items.pop(-1)
                break
        else:
            message = "1000 iterations without identity:"
            message += f" {items[0]!r} to {items[-1]!r}."
            raise Exception(message)
    else:
        for i in range(count - 1):
            sequence = items[-1]
            for operand in operands:
                sequence = type(sequence)([operand(_) for _ in sequence])
                items.append(sequence)
    return type(sequence)(items)


def boustrophedon(sequence, *, count: int = 2):
    r"""
    Iterates sequence boustrophedon.

    ..  container:: example

        Iterates atoms boustrophedon:

        >>> sequence = [1, 2, 3, 4, 5]

        >>> baca.sequence.boustrophedon(sequence, count=0)
        []

        >>> baca.sequence.boustrophedon(sequence, count=1)
        [1, 2, 3, 4, 5]

        >>> baca.sequence.boustrophedon(sequence, count=2)
        [1, 2, 3, 4, 5, 4, 3, 2, 1]

        >>> baca.sequence.boustrophedon(sequence, count=3)
        [1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5]

    ..  container:: example

        Iterates collections boustrophedon:

        >>> collections = [
        ...     abjad.PitchClassSegment([1, 2, 3]),
        ...     abjad.PitchClassSegment([4, 5, 6]),
        ... ]
        >>> sequence = collections

        >>> baca.sequence.boustrophedon(sequence, count=0)
        []

        >>> for collection in baca.sequence.boustrophedon(sequence, count=1):
        ...     collection
        ...
        PitchClassSegment([1, 2, 3])
        PitchClassSegment([4, 5, 6])

        >>> for collection in baca.sequence.boustrophedon(sequence, count=2):
        ...     collection
        ...
        PitchClassSegment([1, 2, 3])
        PitchClassSegment([4, 5, 6])
        PitchClassSegment([5, 4])
        PitchClassSegment([3, 2, 1])

        >>> for collection in baca.sequence.boustrophedon(sequence, count=3):
        ...     collection
        ...
        PitchClassSegment([1, 2, 3])
        PitchClassSegment([4, 5, 6])
        PitchClassSegment([5, 4])
        PitchClassSegment([3, 2, 1])
        PitchClassSegment([2, 3])
        PitchClassSegment([4, 5, 6])

    ..  container:: example

        Iterates mixed items boustrophedon:

        >>> collection = abjad.PitchClassSegment([1, 2, 3])
        >>> sequence = [collection, 4, 5]
        >>> for item in baca.sequence.boustrophedon(sequence, count=3):
        ...     item
        ...
        PitchClassSegment([1, 2, 3])
        4
        5
        4
        PitchClassSegment([3, 2, 1])
        PitchClassSegment([2, 3])
        4
        5

    Returns new sequence.
    """
    assert isinstance(count, int), repr(count)
    result = []
    for i in range(count):
        if i == 0:
            for item in sequence:
                result.append(copy.copy(item))
        elif i % 2 == 0:
            if hasattr(sequence[0], "__len__"):
                result.append(sequence[0][1:])
            else:
                pass
            for item in sequence[1:]:
                result.append(copy.copy(item))
        else:
            if hasattr(sequence[-1], "__len__"):
                item = type(sequence[-1])(list(reversed(sequence[-1]))[1:])
                result.append(item)
            else:
                pass
            for item in reversed(sequence[:-1]):
                if hasattr(item, "__len__"):
                    item = type(item)(list(reversed(item)))
                    result.append(item)
                else:
                    result.append(item)
    return type(sequence)(result)


def degree_of_rotational_symmetry(sequence) -> int:
    """
    Gets degree of rotational symmetry.

    ..  container:: example

        >>> baca.sequence.degree_of_rotational_symmetry([1, 1, 1, 1, 1, 1])
        6

        >>> baca.sequence.degree_of_rotational_symmetry([1, 2, 1, 2, 1, 2])
        3

        >>> baca.sequence.degree_of_rotational_symmetry([1, 2, 3, 1, 2, 3])
        2

        >>> baca.sequence.degree_of_rotational_symmetry([1, 2, 3, 4, 5, 6])
        1

        >>> baca.sequence.degree_of_rotational_symmetry([])
        1

    """
    degree_of_rotational_symmetry = 0
    for index in range(len(sequence)):
        rotation = sequence[index:] + sequence[:index]
        if rotation == sequence:
            degree_of_rotational_symmetry += 1
    degree_of_rotational_symmetry = degree_of_rotational_symmetry or 1
    return degree_of_rotational_symmetry


def group_by_sign(sequence, *, sign=(-1, 0, 1)) -> list:
    r"""
    Groups sequence by sign of items.

    >>> sequence = [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

    ..  container:: example

        >>> for item in baca.sequence.group_by_sign(sequence):
        ...     item
        ...
        [0, 0]
        [-1, -1]
        [2, 3]
        [-5]
        [1, 2, 5]
        [-5, -6]

    ..  container:: example

        >>> for item in baca.sequence.group_by_sign(sequence, sign=[-1]):
        ...     item
        ...
        [0]
        [0]
        [-1, -1]
        [2]
        [3]
        [-5]
        [1]
        [2]
        [5]
        [-5, -6]

    ..  container:: example

        >>> for item in baca.sequence.group_by_sign(sequence, sign=[0]):
        ...     item
        ...
        [0, 0]
        [-1]
        [-1]
        [2]
        [3]
        [-5]
        [1]
        [2]
        [5]
        [-5]
        [-6]

    ..  container:: example

        >>> for item in baca.sequence.group_by_sign(sequence, sign=[1]):
        ...     item
        ...
        [0]
        [0]
        [-1]
        [-1]
        [2, 3]
        [-5]
        [1, 2, 5]
        [-5]
        [-6]

    ..  container:: example

        >>> for item in baca.sequence.group_by_sign(sequence, sign=[-1, 0]):
        ...     item
        ...
        [0, 0]
        [-1, -1]
        [2]
        [3]
        [-5]
        [1]
        [2]
        [5]
        [-5, -6]

    ..  container:: example

        >>> for item in baca.sequence.group_by_sign(sequence, sign=[-1, 1]):
        ...     item
        ...
        [0]
        [0]
        [-1, -1]
        [2, 3]
        [-5]
        [1, 2, 5]
        [-5, -6]

    ..  container:: example

        >>> for item in baca.sequence.group_by_sign(sequence, sign=[0, 1]):
        ...     item
        ...
        [0, 0]
        [-1]
        [-1]
        [2, 3]
        [-5]
        [1, 2, 5]
        [-5]
        [-6]

    ..  container:: example

        >>> for item in baca.sequence.group_by_sign(sequence, sign=[-1, 0, 1]):
        ...     item
        ...
        [0, 0]
        [-1, -1]
        [2, 3]
        [-5]
        [1, 2, 5]
        [-5, -6]

    Groups negative elements when ``-1`` in ``sign``.

    Groups zero-valued elements When ``0`` in ``sign``.

    Groups positive elements when ``1`` in ``sign``.

    Returns list of ``sequence`` types.
    """
    items = []
    pairs = itertools.groupby(sequence, abjad.math.sign)
    for current_sign, group in pairs:
        if current_sign in sign:
            items.append(type(sequence)(group))
        else:
            for item in group:
                items.append(type(sequence)([item]))
    return type(sequence)(items)


def helianthate(sequence, n=0, m=0):
    r"""
    Helianthates sequence.

    ..  container:: example

        Helianthates list of lists:

        >>> sequence = [[1, 2, 3], [4, 5], [6, 7, 8]]
        >>> sequence = baca.sequence.helianthate(sequence, n=-1, m=1)
        >>> for item in sequence:
        ...     item
        ...
        [1, 2, 3]
        [4, 5]
        [6, 7, 8]
        [5, 4]
        [8, 6, 7]
        [3, 1, 2]
        [7, 8, 6]
        [2, 3, 1]
        [4, 5]
        [1, 2, 3]
        [5, 4]
        [6, 7, 8]
        [4, 5]
        [8, 6, 7]
        [3, 1, 2]
        [7, 8, 6]
        [2, 3, 1]
        [5, 4]

    ..  container:: example

        Helianthates list of collections:

        >>> J = abjad.PitchClassSegment(items=[0, 2, 4])
        >>> K = abjad.PitchClassSegment(items=[5, 6])
        >>> L = abjad.PitchClassSegment(items=[7, 9, 11])
        >>> sequence = [J, K, L]
        >>> sequence = baca.sequence.helianthate(sequence, n=-1, m=1)
        >>> for collection in sequence:
        ...     collection
        ...
        PitchClassSegment([0, 2, 4])
        PitchClassSegment([5, 6])
        PitchClassSegment([7, 9, 11])
        PitchClassSegment([6, 5])
        PitchClassSegment([11, 7, 9])
        PitchClassSegment([4, 0, 2])
        PitchClassSegment([9, 11, 7])
        PitchClassSegment([2, 4, 0])
        PitchClassSegment([5, 6])
        PitchClassSegment([0, 2, 4])
        PitchClassSegment([6, 5])
        PitchClassSegment([7, 9, 11])
        PitchClassSegment([5, 6])
        PitchClassSegment([11, 7, 9])
        PitchClassSegment([4, 0, 2])
        PitchClassSegment([9, 11, 7])
        PitchClassSegment([2, 4, 0])
        PitchClassSegment([6, 5])

    ..  container:: example

        Trivial helianthation:

        >>> items = [[1, 2, 3], [4, 5], [6, 7, 8]]
        >>> sequence = items
        >>> baca.sequence.helianthate(sequence)
        [[1, 2, 3], [4, 5], [6, 7, 8]]

    """
    start = list(sequence[:])
    result = list(sequence[:])
    assert isinstance(n, int), repr(n)
    assert isinstance(m, int), repr(m)
    original_n = n
    original_m = m

    def _generalized_rotate(argument, n=0):
        if hasattr(argument, "rotate"):
            return abjad.sequence.rotate(argument, n=n)
        argument_type = type(argument)
        argument = abjad.sequence.rotate(argument, n=n)
        argument = argument_type(argument)
        return argument

    i = 0
    while True:
        inner = [_generalized_rotate(_, m) for _ in sequence]
        candidate = _generalized_rotate(inner, n)
        if candidate == start:
            break
        result.extend(candidate)
        n += original_n
        m += original_m
        i += 1
        if i == 1000:
            message = "1000 iterations without identity."
            raise Exception(message)
    return type(sequence)(result)


def increase_elements(sequence, addenda, *, indices=None) -> list:
    """
    Increases ``sequence`` cyclically by ``addenda``.

    Increases range elements by ``10`` and ``-10`` in alternation:

    ..  container:: example

        >>> baca.sequence.increase_elements(range(10), [10, -10])
        [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]

    ..  container:: example

        Increases list elements by 10 and -10 in alternation:

        >>> baca.sequence.increase_elements(list(range(10)), [10, -10])
        [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]

    ..  container:: example

        Increases tuple elements by 10 and -10 in alternation:

        >>> baca.sequence.increase_elements(tuple(range(10)), [10, -10])
        [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]

    ..  container:: example

        Increases pairs of elements by ``0.5`` starting at indices 0, 4, 8:

        >>> sequence = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
        >>> addenda = [0.5, 0.5]
        >>> indices = [0, 4, 8]
        >>> baca.sequence.increase_elements(sequence, addenda, indices=indices)
        [1.5, 1.5, 2, 3, 5.5, 5.5, 1, 2, 5.5, 5.5, 6]

    ..  container:: example

        >>> baca.sequence.increase_elements(range(10), [2, 0])
        [2, 1, 4, 3, 6, 5, 8, 7, 10, 9]

    ..  container:: example

        >>> sequence_1 = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
        >>> baca.sequence.increase_elements(sequence_1, [0.5, 0.5], indices=[0, 4, 8])
        [1.5, 1.5, 2, 3, 5.5, 5.5, 1, 2, 5.5, 5.5, 6]

    Returns list.
    """
    sequence = list(sequence)
    if indices is None:
        result = []
        for i, element in enumerate(sequence):
            new = element + addenda[i % len(addenda)]
            result.append(new)
    else:
        # assert no overlaps
        tmp = [tuple(range(i, len(addenda))) for i in indices]
        tmp = abjad.sequence.flatten(tmp)
        assert len(tmp) == len(set(tmp))
        result = sequence[:]
        for i in indices:
            for j in range(len(addenda)):
                result[i + j] += addenda[j]
    assert isinstance(result, list)
    return result


def negate_elements(sequence, *, absolute=False, indices=None, period=None):
    """
    Negates ``sequence`` elements.

    ..  container:: example

        Negates all elements:

        >>> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
        >>> baca.sequence.negate_elements(sequence)
        [-1, -2, -3, -4, -5, 6, 7, 8, 9, 10]

    ..  container:: example

        Negates elements at indices 0, 1 and 2:

        >>> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
        >>> baca.sequence.negate_elements(sequence, indices=[0, 1, 2])
        [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]

    ..  container:: example

        Negates elements at indices congruent to 0, 1 or 2 mod 5:

        >>> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
        >>> baca.sequence.negate_elements(
        ...     sequence,
        ...     indices=[0, 1, 2],
        ...     period=5,
        ... )
        [-1, -2, -3, 4, 5, 6, 7, 8, -9, -10]

    ..  container:: example

        Negates the absolute value of all elements:

        >>> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
        >>> baca.sequence.negate_elements(sequence, absolute=True)
        [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10]

    ..  container:: example

        Negates the absolute value elements at indices 0, 1 and 2:

        >>> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
        >>> baca.sequence.negate_elements(
        ...     sequence,
        ...     absolute=True,
        ...     indices=[0, 1, 2],
        ... )
        [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]

    ..  container:: example

        Negates the absolute value elements at indices congruent to 0, 1 or 2 mod 5:

        >>> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
        >>> baca.sequence.negate_elements(
        ...     sequence,
        ...     absolute=True,
        ...     indices=[0, 1, 2],
        ...     period=5,
        ... )
        [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]

    """
    indices = indices or range(len(sequence))
    if isinstance(indices, abjad.Pattern):
        assert period is None
        pattern = indices
    else:
        period = period or len(sequence)
        pattern = abjad.Pattern(indices=indices, period=period)
    items = []
    total_length = len(sequence)
    for i, item in enumerate(sequence):
        if pattern.matches_index(i, total_length=total_length):
            if absolute:
                items.append(-abs(item))
            else:
                items.append(-item)
        else:
            items.append(item)
    result = type(sequence)(items)
    return result


def overwrite_elements(sequence, pairs):
    """
    Overwrites ``sequence`` elements at indices according to ``pairs``.

    ..  container:: example

        Overwrites range elements:

        >>> pairs = [(0, 3), (5, 3)]
        >>> baca.sequence.overwrite_elements(range(10), pairs)
        [0, 0, 0, 3, 4, 5, 5, 5, 8, 9]

        Overwrites list elements:

        >>> pairs = [(0, 3), (5, 3)]
        >>> baca.sequence.overwrite_elements(list(range(10)), pairs)
        [0, 0, 0, 3, 4, 5, 5, 5, 8, 9]

        Overwrites tuple elements:

        >>> pairs = [(0, 3), (5, 3)]
        >>> baca.sequence.overwrite_elements(tuple(range(10)), pairs)
        [0, 0, 0, 3, 4, 5, 5, 5, 8, 9]

        Overwrites all items:

        >>> baca.sequence.overwrite_elements(range(10), [(0, 99)])
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    Set ``pairs`` to a list of ``(anchor_index, length)`` pairs.

    Coerces input to list.

    Returns new list.
    """
    sequence = list(sequence)
    result = list(sequence)
    for anchor_index, length in pairs:
        anchor = result[anchor_index]
        start = anchor_index + 1
        stop = start + length - 1
        for i in range(start, stop):
            try:
                result[i] = anchor
            except IndexError:
                break
    assert isinstance(result, list), repr(result)
    return result


def partition_in_halves(sequence) -> list:
    best_candidate, minimum_distance = [], None
    for i in range(1, len(sequence)):
        candidate = [sequence[:-i], sequence[-i:]]
        weights = [abjad.sequence.weight(_) for _ in candidate]
        maximum, minimum = max(weights), min(weights)
        if maximum == minimum:
            return candidate
        distance = maximum / minimum
        if minimum_distance is None:
            minimum_distance = distance
            best_candidate = candidate
        if distance < minimum_distance:
            minimum_distance = distance
            best_candidate = candidate
    return best_candidate


def partition_nested_into_inward_pointing_parts(sequence, target="negative"):
    """
    Partitions integers in subsequences of ``sequence`` into inward-pointing parts.

    ..  container:: example

        >>> sequence = [[1, 1, 5]]
        >>> baca.sequence.partition_nested_into_inward_pointing_parts(sequence)
        [[1, 1, 5]]

        >>> sequence = [[1, 1, -5]]
        >>> baca.sequence.partition_nested_into_inward_pointing_parts(sequence)
        [[1, 1, 1, -4]]

        >>> sequence = [[1], [5], [5, 1], [1, 5], [5, 5], [1, 5, 1]]
        >>> baca.sequence.partition_nested_into_inward_pointing_parts(
        ...     sequence, target="positive")
        [[1], [4, 1], [4, 1, 1], [1, 1, 4], [4, 1, 1, 4], [1, 4, 1, 1]]

        >>> sequence = [[1, 1, -5]]
        >>> baca.sequence.partition_nested_into_inward_pointing_parts(
        ...     sequence, target="positive")
        [[1, 1, -5]]

    """
    result = []
    if target == "negative":
        for item in sequence:
            # -5 at beginning
            if item[0] == -5:
                result.append([-4, 1] + item[1:])
            # -5 at end
            elif item[-1] == -5:
                result.append(item[:-1] + [1, -4])
            # -5 in middle
            elif -5 in item:
                new = []
                for number in item:
                    if number != -5:
                        new.append(number)
                    else:
                        new.append(-4)
                        new.append(1)
            # no -5
            else:
                result.append(item)
    if target == "positive":
        for sublist in sequence:
            new = sublist
            # 5 at beginning
            if new[0] == 5:
                new = [4, 1] + new[1:]
            # 5 at end
            if new[-1] == 5:
                new = new[:-1] + [1, 4]
            # 5 in middle
            if 5 in new:
                new = [(4, 1) if item == 5 else item for item in new]
                new = abjad.sequence.flatten(new)
                new = list(new)
            result.append(new)
    return result


def partition_to_avoid_octave_adjacencies(sequence, bigger=abjad.LEFT):
    """
    Partitions ``sequence`` to avoid octave adjacencies.

    ..  container:: example

        No duplicate items:

        >>> pitches = [0, 1, 2, 3]
        >>> baca.sequence.partition_to_avoid_octave_adjacencies(pitches, abjad.LEFT)
        [(0, 1, 2, 3)]

        >>> baca.sequence.partition_to_avoid_octave_adjacencies(pitches, abjad.RIGHT)
        [(0, 1, 2, 3)]

        All duplicate items:

        >>> pitches = [0, 0, 0, 0]
        >>> baca.sequence.partition_to_avoid_octave_adjacencies(pitches, abjad.LEFT)
        [(0,), (0,), (0,), (0,)]

        >>> pitches = [0, 0, 0, 0]
        >>> baca.sequence.partition_to_avoid_octave_adjacencies(pitches, abjad.RIGHT)
        [(0,), (0,), (0,), (0,)]

        Duplicates, with odd number of items:

        >>> pitches = [0, 1, 0]
        >>> baca.sequence.partition_to_avoid_octave_adjacencies(pitches, abjad.LEFT)
        [(0, 1), (0,)]

        >>> baca.sequence.partition_to_avoid_octave_adjacencies(pitches, abjad.RIGHT)
        [(0,), (1, 0)]

        >>> pitches = [0, 1, 2, 3, 0]
        >>> baca.sequence.partition_to_avoid_octave_adjacencies(pitches, abjad.LEFT)
        [(0, 1, 2), (3, 0)]

        >>> baca.sequence.partition_to_avoid_octave_adjacencies(pitches, abjad.RIGHT)
        [(0, 1), (2, 3, 0)]

        Duplicates, with even number of items:

        >>> pitches = [0, 1, 2, 0]
        >>> baca.sequence.partition_to_avoid_octave_adjacencies(pitches, abjad.LEFT)
        [(0, 1), (2, 0)]

        >>> baca.sequence.partition_to_avoid_octave_adjacencies(pitches, abjad.RIGHT)
        [(0, 1), (2, 0)]

        >>> pitches = [0, 1, 2, 3, 4, 0]
        >>> baca.sequence.partition_to_avoid_octave_adjacencies(pitches, abjad.LEFT)
        [(0, 1, 2), (3, 4, 0)]

        >>> baca.sequence.partition_to_avoid_octave_adjacencies(pitches, abjad.RIGHT)
        [(0, 1, 2), (3, 4, 0)]

    """
    assert bigger in (abjad.LEFT, abjad.RIGHT), repr(bigger)
    result = [[]]
    part = result[-1]
    for number in sequence:
        assert isinstance(number, int | float)
        pc = number % 12
        part_pcs = [_ % 12 for _ in part]
        if pc not in part_pcs:
            part.append(number)
            continue
        first_value = [_ for _ in part if _ % 12 == pc][0]
        first_index = part.index(first_value)
        old_part = part[: first_index + 1]
        disputed_part = part[first_index + 1 :]
        new_part = []
        length = len(disputed_part)
        left, right = _math.partition_integer_into_halves(length, bigger=bigger)
        disputed_parts = abjad.sequence.partition_by_counts(
            disputed_part, [left, right]
        )
        left_disputed_part, right_disputed_part = disputed_parts
        assert len(left_disputed_part) == left
        assert len(right_disputed_part) == right
        old_part.extend(left_disputed_part)
        new_part.extend(right_disputed_part)
        result[-1] = old_part
        result.append(new_part)
        part = result[-1]
        part.append(number)
    result = [tuple(_) for _ in result]
    return result


def period_of_rotation(sequence) -> int:
    """
    Gets period of rotation of ``sequence``.

    ..  container:: example

        >>> baca.sequence.period_of_rotation([1, 2, 3, 4, 5, 6])
        6

        >>> baca.sequence.period_of_rotation([1, 2, 3, 1, 2, 3])
        3

        >>> baca.sequence.period_of_rotation([1, 2, 1, 2, 1, 2])
        2

        >>> baca.sequence.period_of_rotation([1, 1, 1, 1, 1, 1])
        1

        >>> baca.sequence.period_of_rotation([])
        0

    Defined equal to length of sequence divided by degree of rotational symmetry of
    sequence.
    """
    return len(sequence) // degree_of_rotational_symmetry(sequence)


def quarters(durations: list[abjad.Duration]) -> list[abjad.Duration]:
    r"""
    Splits ``durations`` into quarters.

    ..  container:: example

        >>> durations = abjad.duration.durations([(2, 4), (6, 4)])
        >>> for list_ in baca.sequence.quarters(durations): list_
        Duration(1, 4)
        Duration(1, 4)
        Duration(1, 4)
        Duration(1, 4)
        Duration(1, 4)
        Duration(1, 4)
        Duration(1, 4)
        Duration(1, 4)

    """
    assert isinstance(durations, list), repr(durations)
    assert all(isinstance(_, abjad.Duration) for _ in durations), repr(durations)
    weights = abjad.duration.durations([(1, 4)])
    lists = abjad.sequence.split(durations, weights, cyclic=True, overhang=True)
    result = abjad.sequence.flatten(lists, depth=-1)
    assert all(isinstance(_, abjad.Duration) for _ in result), repr(result)
    return result


def repeat_by(sequence, counts: list[int], *, cyclic: bool = False):
    r"""
    Repeat sequence elements at ``counts``.

    ..  container:: example

        With empty counts:

        >>> baca.sequence.repeat_by([[1, 2, 3], 4, [5, 6]], [])
        [[1, 2, 3], 4, [5, 6]]

    ..  container:: example

        With acyclic counts:

        >>> sequence = [[1, 2, 3], 4, [5, 6]]

        ..  container:: example

            >>> baca.sequence.repeat_by(sequence, [0])
            [4, [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [1])
            [[1, 2, 3], 4, [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [2])
            [[1, 2, 3], [1, 2, 3], 4, [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [3])
            [[1, 2, 3], [1, 2, 3], [1, 2, 3], 4, [5, 6]]

        ..  container:: example

            >>> baca.sequence.repeat_by(sequence, [1, 0])
            [[1, 2, 3], [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [1, 1])
            [[1, 2, 3], 4, [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [1, 2])
            [[1, 2, 3], 4, 4, [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [1, 3])
            [[1, 2, 3], 4, 4, 4, [5, 6]]

        ..  container:: example

            >>> baca.sequence.repeat_by(sequence, [1, 1, 0])
            [[1, 2, 3], 4]

            >>> baca.sequence.repeat_by(sequence, [1, 1, 1])
            [[1, 2, 3], 4, [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [1, 1, 2])
            [[1, 2, 3], 4, [5, 6], [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [1, 1, 3])
            [[1, 2, 3], 4, [5, 6], [5, 6], [5, 6]]

    ..  container:: example

        With cyclic counts:

        ..  container:: example

            >>> baca.sequence.repeat_by(sequence, [0], cyclic=True)
            []

            >>> baca.sequence.repeat_by(sequence, [1], cyclic=True)
            [[1, 2, 3], 4, [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [2], cyclic=True)
            [[1, 2, 3], [1, 2, 3], 4, 4, [5, 6], [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [3], cyclic=True)
            [[1, 2, 3], [1, 2, 3], [1, 2, 3], 4, 4, 4, [5, 6], [5, 6], [5, 6]]

        ..  container:: example

            >>> baca.sequence.repeat_by(sequence, [2, 0], cyclic=True)
            [[1, 2, 3], [1, 2, 3], [5, 6], [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [2, 1], cyclic=True)
            [[1, 2, 3], [1, 2, 3], 4, [5, 6], [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [2, 2], cyclic=True)
            [[1, 2, 3], [1, 2, 3], 4, 4, [5, 6], [5, 6]]

            >>> baca.sequence.repeat_by(sequence, [2, 3], cyclic=True)
            [[1, 2, 3], [1, 2, 3], 4, 4, 4, [5, 6], [5, 6]]

    Raises exception on negative counts.

    Returns new sequence.
    """
    assert isinstance(cyclic, bool), repr(cyclic)
    if not counts:
        return type(sequence)(sequence)
    assert isinstance(counts, list), repr(counts)
    assert all(isinstance(_, int) for _ in counts), repr(counts)
    if cyclic is True:
        cyclic_counts = abjad.CyclicTuple(counts)
    items = []
    for i, item in enumerate(sequence):
        try:
            if cyclic is True:
                count = cyclic_counts[i]
            else:
                count = counts[i]
        except IndexError:
            count = 1
        items.extend(count * [item])
    return type(sequence)(items)


def repeat_subruns_to_length(notes, pairs, *, history=False):
    """
    Repeats ``notes`` according to ``pairs``.

    ..  container:: example

        >>> sequence = [abjad.Note(_, (1, 4)) for _ in [0, 2, 4, 5, 7, 9, 11]]
        >>> result = baca.sequence.repeat_subruns_to_length(sequence, [(0, 4, 1), (2, 4, 1)])
        >>> for item in result: item
        Note("c'4")
        Note("d'4")
        Note("e'4")
        Note("f'4")
        Note("c'4")
        Note("d'4")
        Note("e'4")
        Note("f'4")
        Note("g'4")
        Note("a'4")
        Note("e'4")
        Note("f'4")
        Note("g'4")
        Note("a'4")
        Note("b'4")

    Returns list of components.
    """
    assert all([isinstance(_, abjad.Note) for _ in notes])
    assert isinstance(pairs, list)
    assert all([len(_) == 3 for _ in pairs])
    assert isinstance(notes, list)
    instructions = []
    len_notes = len(notes)
    for pair in reversed(pairs):
        new_notes = []
        for i in range(pair[0], pair[0] + pair[1]):
            source = notes[i % len_notes]
            pitch_number = source.written_pitch().number()
            new_note = abjad.Note(pitch_number, source.written_duration())
            if history:
                abjad.attach(history, new_note)
            new_notes.append(new_note)
        reps = pair[-1]
        instruction = (pair[0] + pair[1], new_notes, reps)
        instructions.append(instruction)
    for index, new_notes, reps in reversed(sorted(instructions)):
        total = []
        for _ in range(reps):
            abjad.mutate.copy(new_notes)
            total.extend(new_notes)
        notes[index:index] = total
    return notes
