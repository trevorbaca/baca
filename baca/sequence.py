"""
Sequence.
"""
import collections
import copy
import itertools
import typing

import abjad


def accumulate(sequence, operands=None, count=None):
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


def boustrophedon(sequence, count=2):
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
    result = []
    for i in range(count):
        if i == 0:
            for item in sequence:
                result.append(copy.copy(item))
        elif i % 2 == 0:
            if isinstance(sequence[0], collections.abc.Iterable):
                result.append(sequence[0][1:])
            else:
                pass
            for item in sequence[1:]:
                result.append(copy.copy(item))
        else:
            if isinstance(sequence[-1], collections.abc.Iterable):
                item = type(sequence[-1])(list(reversed(sequence[-1]))[1:])
                result.append(item)
            else:
                pass
            for item in reversed(sequence[:-1]):
                if isinstance(item, collections.abc.Iterable):
                    item = type(item)(list(reversed(item)))
                    result.append(item)
                else:
                    result.append(item)
    return type(sequence)(result)


def degree_of_rotational_symmetry(sequence):
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

    Returns positive integer.
    """
    degree_of_rotational_symmetry = 0
    for index in range(len(sequence)):
        rotation = sequence[index:] + sequence[:index]
        if rotation == sequence:
            degree_of_rotational_symmetry += 1
    degree_of_rotational_symmetry = degree_of_rotational_symmetry or 1
    return degree_of_rotational_symmetry


def group_by_sign(sequence, sign=(-1, 0, 1)):
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

        >>> for item in baca.sequence.group_by_sign(sequence, [-1]):
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

        >>> for item in baca.sequence.group_by_sign(sequence, [0]):
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

        >>> for item in baca.sequence.group_by_sign(sequence, [1]):
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

        >>> for item in baca.sequence.group_by_sign(sequence, [-1, 0]):
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

        >>> for item in baca.sequence.group_by_sign(sequence, [-1, 1]):
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

        >>> for item in baca.sequence.group_by_sign(sequence, [0, 1]):
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

        >>> for item in baca.sequence.group_by_sign(sequence, [-1, 0, 1]):
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

    Returns nested sequence.
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


def period_of_rotation(sequence):
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

    Returns positive integer.
    """
    return len(sequence) // degree_of_rotational_symmetry(sequence)


def partition(sequence, counts=None):
    r"""
    Partitions sequence cyclically by ``counts`` with overhang.

    ..  container:: example

        >>> sequence = list(range(16))
        >>> parts = baca.sequence.partition(sequence, [3])

        >>> for part in parts:
        ...     part
        [0, 1, 2]
        [3, 4, 5]
        [6, 7, 8]
        [9, 10, 11]
        [12, 13, 14]
        [15]

    Returns new sequence.
    """
    return abjad.sequence.partition_by_counts(
        sequence, counts=counts, cyclic=True, overhang=True
    )


def quarters(
    sequence: typing.Sequence[tuple[int, int] | abjad.Duration],
    *,
    compound: bool = False,
    remainder: abjad.enums.Horizontal | None = None,
) -> list[list[tuple[int, int] | abjad.Duration]]:
    r"""
    Splits ``sequence`` into quarters.

    ..  container:: example

        >>> list_ = baca.durations([(2, 4), (6, 4)])
        >>> for item in baca.sequence.quarters(list_):
        ...     item
        ...
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]

    ..  container:: example

        Set ``compound=True`` for compound quarter notes:

        >>> pairs = [(3, 4), (6, 4)]
        >>> lists = [baca.sequence.quarters([_]) for _ in pairs]
        >>> for list_ in lists:
        ...     print("list:")
        ...     for pair in list_:
        ...         print(f"\t{repr(pair)}")
        ...
        list:
            [Duration(1, 4)]
            [Duration(1, 4)]
            [Duration(1, 4)]
        list:
            [Duration(1, 4)]
            [Duration(1, 4)]
            [Duration(1, 4)]
            [Duration(1, 4)]
            [Duration(1, 4)]
            [Duration(1, 4)]

        >>> pairs = [(3, 4), (6, 4)]
        >>> lists = [baca.sequence.quarters([_], compound=True) for _ in pairs]
        >>> for list_ in lists:
        ...     print("list:")
        ...     for pair in list_:
        ...         print(f"\t{repr(pair)}")
        ...
        list:
            [Duration(1, 4)]
            [Duration(1, 4)]
            [Duration(1, 4)]
        list:
            [Duration(3, 8)]
            [Duration(3, 8)]
            [Duration(3, 8)]
            [Duration(3, 8)]

    ..  container:: example

        Splits each duration into quarters and positions remainder at right:

        >>> durations = baca.durations([(7, 8), (3, 8), (5, 8)])
        >>> lists = [baca.sequence.quarters([_]) for _ in durations]
        >>> for list_ in lists: list_
        [[Duration(1, 4)], [Duration(1, 4)], [Duration(1, 4)], [Duration(1, 8)]]
        [[Duration(1, 4)], [Duration(1, 8)]]
        [[Duration(1, 4)], [Duration(1, 4)], [Duration(1, 8)]]

        Splits each durations into quarters and positions remainder at left:

        >>> duration = baca.durations([(7, 8), (3, 8), (5, 8)])
        >>> lists = [
        ...     baca.sequence.quarters([_], remainder=abjad.LEFT) for _ in durations
        ... ]
        >>> for list_ in lists: list_
        [[Duration(1, 8)], [Duration(1, 4)], [Duration(1, 4)], [Duration(1, 4)]]
        [[Duration(1, 8)], [Duration(1, 4)]]
        [[Duration(1, 8)], [Duration(1, 4)], [Duration(1, 4)]]

    """
    assert isinstance(sequence, list), repr(sequence)
    prototype = (tuple, abjad.Duration, abjad.TimeSignature)
    assert all(isinstance(_, prototype) for _ in sequence), repr(sequence)
    assert isinstance(compound, bool), repr(compound)
    assert remainder in (abjad.LEFT, abjad.RIGHT, None), repr(remainder)
    lists = split(
        sequence, [(1, 4)], cyclic=True, compound=compound, remainder=remainder
    )
    return lists


def ratios(
    sequence,
    ratio: tuple[int, int],
    *,
    rounded: bool = False,
):
    r"""
    Splits sequence by ``ratio``.

    ..  container:: example

        Splits sequence by exact ``2:1`` ratio:

        >>> durations = baca.durations([(5, 8), (6, 8)])
        >>> lists = baca.sequence.ratios(durations, (2, 1))
        >>> for list_ in lists: list_
        [(5, 8), (7, 24)]
        [(11, 24)]

        Works with durations:

        >>> durations = [abjad.Duration(_) for _ in [(5, 8), (6, 8)]]
        >>> lists = baca.sequence.ratios(durations, (2, 1))
        >>> for list_ in lists: list_
        [(5, 8), (7, 24)]
        [(11, 24)]

        Splits durations by rounded ``2:1`` ratio:

        >>> durations = baca.durations([(5, 8), (6, 8)])
        >>> lists = baca.sequence.ratios(durations, (2, 1), rounded=True)
        >>> for list_ in lists: list_
        [(5, 8), (1, 4)]
        [(1, 2)]

    ..  container:: example

        Splits each duration by exact ``2:1`` ratio:

        >>> durations = baca.durations([(5, 8), (6, 8)])
        >>> lists = [baca.sequence.ratios([_], (2, 1)) for _ in durations]
        >>> for list_ in lists: list_
        [[(5, 12)], [(5, 24)]]
        [[(1, 2)], [(1, 4)]]

        Splits each duration by rounded ``2:1`` ratio:

        >>> durations = baca.durations([(5, 8), (6, 8)])
        >>> lists = [
        ...     baca.sequence.ratios([_], (2, 1), rounded=True)
        ...     for _ in durations
        ... ]
        >>> for list_ in lists: list_
        [[(3, 8)], [(1, 4)]]
        [[(1, 2)], [(1, 4)]]

    ..  container:: example

        Splits durations with alternating exact ``2:1`` and ``1:1:1`` ratios:

        >>> ratios = abjad.CyclicTuple([(2, 1), (1, 1, 1)])
        >>> durations = baca.durations([(5, 8), (6, 8)])
        >>> for i, duration in enumerate(durations):
        ...     ratio = ratios[i]
        ...     baca.sequence.ratios([duration], ratio)
        [[(5, 12)], [(5, 24)]]
        [[(1, 4)], [(1, 4)], [(1, 4)]]

        Splits durations with alternating rounded ``2:1`` and ``1:1:1`` ratios:

        >>> ratios = abjad.CyclicTuple([(2, 1), (1, 1, 1)])
        >>> durations = baca.durations([(5, 8), (6, 8)])
        >>> for i, duration in enumerate(durations):
        ...     ratio = ratios[i]
        ...     baca.sequence.ratios([duration], ratio, rounded=True)
        [[(3, 8)], [(1, 4)]]
        [[(1, 4)], [(1, 4)], [(1, 4)]]

    """
    pairs = [_.pair for _ in sequence]
    assert isinstance(rounded, bool), repr(rounded)
    pairs_weight = (0, 1)
    for pair in pairs:
        pairs_weight = abjad.duration.add_pairs(pairs_weight, pair)
    numerator, denominator = pairs_weight
    assert isinstance(ratio, tuple), repr(ratio)
    ratio_ = tuple(ratio)
    if rounded is True:
        numerators = abjad.math.partition_integer_by_ratio(numerator, ratio_)
        durations = [
            abjad.Duration((numerator, denominator)) for numerator in numerators
        ]
    else:
        durations = []
        ratio_weight = sum(ratio_)
        for number in ratio:
            multiplier = abjad.Fraction(number, ratio_weight)
            numerator_ = multiplier.numerator * pairs_weight[0]
            denominator_ = multiplier.denominator * pairs_weight[1]
            duration = abjad.Duration(numerator_, denominator_)
            durations.append(duration)
    sequence = [abjad.Duration(_) for _ in sequence]
    sequence = abjad.sequence.split(sequence, durations)
    assert isinstance(sequence, list)
    assert isinstance(sequence[0], list)
    lists = [[_.pair for _ in list_] for list_ in sequence]
    return lists


def repeat_by(sequence, counts=None, cyclic=None):
    r"""
    Repeat sequence elements at ``counts``.

    ..  container:: example

        With no counts:

        ..  container:: example

            >>> baca.sequence.repeat_by([[1, 2, 3], 4, [5, 6]])
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
    if counts is None:
        return type(sequence)(sequence)
    counts = counts or [1]
    assert isinstance(counts, collections.abc.Iterable)
    if cyclic is True:
        counts = abjad.CyclicTuple(counts)
    items = []
    for i, item in enumerate(sequence):
        try:
            count = counts[i]
        except IndexError:
            count = 1
        items.extend(count * [item])
    return type(sequence)(items)


def reveal(sequence, count=None):
    r"""
    Reveals contents of sequence.

    ..  container:: example

        With no count:

        ..  container:: example

            >>> baca.sequence.reveal([[1, 2, 3], 4, [5, 6]])
            [[1, 2, 3], 4, [5, 6]]

    ..  container:: example

        With zero count:

        ..  container:: example

            >>> baca.sequence.reveal([[1, 2, 3], 4, [5, 6]], count=0)
            []

    ..  container:: example

        With positive count:

        ..  container:: example

            >>> baca.sequence.reveal([[1, 2, 3], 4, [5, 6]], count=1)
            [[1]]

            >>> baca.sequence.reveal([[1, 2, 3], 4, [5, 6]], count=2)
            [[1, 2]]

            >>> baca.sequence.reveal([[1, 2, 3], 4, [5, 6]], count=3)
            [[1, 2, 3]]

            >>> baca.sequence.reveal([[1, 2, 3], 4, [5, 6]], count=4)
            [[1, 2, 3], 4]

            >>> baca.sequence.reveal([[1, 2, 3], 4, [5, 6]], count=5)
            [[1, 2, 3], 4, [5]]

            >>> baca.sequence.reveal([[1, 2, 3], 4, [5, 6]], count=6)
            [[1, 2, 3], 4, [5, 6]]

            >>> baca.sequence.reveal([[1, 2, 3], 4, [5, 6]], count=99)
            [[1, 2, 3], 4, [5, 6]]

    ..  container:: example

        With negative count:

        ..  container:: example

            >>> baca.sequence.reveal([[1, 2, 3], 4, [5, 6]], count=-1)
            [[6]]

            >>> baca.sequence.reveal([[1, 2, 3], 4, [5, 6]], count=-2)
            [[5, 6]]

            >>> baca.sequence.reveal([[1, 2, 3], 4, [5, 6]], count=-3)
            [4, [5, 6]]

            >>> baca.sequence.reveal([[1, 2, 3], 4, [5, 6]], count=-4)
            [[3], 4, [5, 6]]

            >>> baca.sequence.reveal([[1, 2, 3], 4, [5, 6]], count=-5)
            [[2, 3], 4, [5, 6]]

            >>> baca.sequence.reveal([[1, 2, 3], 4, [5, 6]], count=-6)
            [[1, 2, 3], 4, [5, 6]]

            >>> baca.sequence.reveal([[1, 2, 3], 4, [5, 6]], count=-99)
            [[1, 2, 3], 4, [5, 6]]

    Returns new sequence.
    """
    if count is None:
        return type(sequence)(sequence)
    if count == 0:
        return type(sequence)()
    if count < 0:
        result = type(sequence)(abjad.sequence.reverse(sequence, recurse=True))
        result = reveal(result, count=abs(count))
        result = type(sequence)(abjad.sequence.reverse(result, recurse=True))
        return result
    current = 0
    items_ = []
    for item in sequence:
        if isinstance(item, collections.abc.Iterable):
            subitems_ = []
            for subitem in item:
                subitems_.append(subitem)
                current += 1
                if current == count:
                    item_ = type(item)(subitems_)
                    items_.append(item_)
                    return type(sequence)(items_)
            item_ = type(item)(subitems_)
            items_.append(item_)
        else:
            items_.append(item)
            current += 1
            if current == count:
                return type(sequence)(items_)
    return type(sequence)(items_)


def split(
    sequence: typing.Sequence[tuple[int, int] | abjad.Duration],
    weights: list[tuple[int, int] | abjad.Duration],
    *,
    compound: bool = False,
    cyclic: bool = False,
    remainder: abjad.enums.Horizontal | None = None,
    remainder_fuse_threshold: tuple[int, int] | abjad.Duration | None = None,
) -> list[list[tuple[int, int] | abjad.Duration]]:
    r"""
    Splits ``sequence`` by ``weights``.

    ..  container:: example

        Splits every five sixteenths:

        >>> durations = baca.durations(10 * [(1, 8)])
        >>> lists = baca.sequence.split(durations, [(5, 16)], cyclic=True)
        >>> for list_ in lists: list_
        [Duration(1, 8), Duration(1, 8), Duration(1, 16)]
        [Duration(1, 16), Duration(1, 8), Duration(1, 8)]
        [Duration(1, 8), Duration(1, 8), Duration(1, 16)]
        [Duration(1, 16), Duration(1, 8), Duration(1, 8)]

    ..  container:: example

        Fuses durations and then splits by ``1/4`` with remainder on right:

        >>> durations = baca.durations([(7, 8), (3, 8), (5, 8)])
        >>> durations = [sum(durations)]
        >>> lists = baca.sequence.split(durations, [(1, 4)], cyclic=True)
        >>> for list_ in lists: list_
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 8)]

        Fuses remainder:

        >>> durations = baca.durations([(7, 8), (3, 8), (5, 8)])
        >>> durations = [sum(durations)]
        >>> lists = baca.sequence.split(
        ...     durations,
        ...     [(1, 4)],
        ...     cyclic=True,
        ...     remainder_fuse_threshold=(1, 8),
        ... )
        >>> for list_ in lists: list_
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(3, 8)]

    ..  container:: example

        Fuses durations and then splits by ``1/4`` with remainder on left:

        >>> durations = baca.durations([(7, 8), (3, 8), (5, 8)])
        >>> durations = [sum(durations)]
        >>> lists = baca.sequence.split(
        ...     durations,
        ...     [(1, 4)],
        ...     cyclic=True,
        ...     remainder=abjad.LEFT,
        ... )
        >>> for list_ in lists: list_
        [Duration(1, 8)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]

        Fuses remainder:

        >>> durations = baca.durations([(7, 8), (3, 8), (5, 8)])
        >>> durations = [sum(durations)]
        >>> lists = baca.sequence.split(
        ...     durations,
        ...     [(1, 4)],
        ...     cyclic=True,
        ...     remainder=abjad.LEFT,
        ...     remainder_fuse_threshold=(1, 8),
        ... )
        >>> for list_ in lists: list_
        [Duration(3, 8)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]
        [Duration(1, 4)]

    ..  container:: example

        Splits each duration; rotates durations one to the left at each new
        duration:

        >>> durations = baca.durations([(7, 16), (7, 16), (7, 16)])
        >>> lists = []
        >>> for i, duration in enumerate(durations):
        ...     durations_ = abjad.sequence.rotate([(1, 16), (1, 8), (1, 4)], n=-i)
        ...     list_ = baca.sequence.split([duration], durations_)
        ...     list_ = abjad.sequence.flatten(list_, depth=-1)
        ...     lists.append(list_)
        ...
        >>> for list_ in lists: list_
        [Duration(1, 16), Duration(1, 8), Duration(1, 4)]
        [Duration(1, 8), Duration(1, 4), Duration(1, 16)]
        [Duration(1, 4), Duration(1, 16), Duration(1, 8)]

    """
    assert isinstance(sequence, list), repr(sequence)
    weights = [abjad.Duration(_) for _ in weights]
    prototype = (tuple, abjad.Duration, abjad.TimeSignature)
    assert all(isinstance(_, prototype) for _ in sequence), repr(sequence)
    assert isinstance(compound, bool), repr(compound)
    assert remainder in (abjad.LEFT, abjad.RIGHT, None), repr(remainder)
    assert isinstance(compound, bool), repr(bool)
    if compound is True and all([abjad.Meter(_).is_compound for _ in sequence]):
        weights = [abjad.Fraction(3, 2) * _ for _ in weights]
    if cyclic is not None:
        cyclic = bool(cyclic)
    if remainder is not None:
        assert remainder in (abjad.LEFT, abjad.RIGHT), repr(remainder)
    if remainder_fuse_threshold is not None:
        remainder_fuse_threshold = abjad.Duration(remainder_fuse_threshold)
    sequence_ = abjad.sequence.split(
        [abjad.Duration(_) for _ in sequence], weights, cyclic=cyclic, overhang=True
    )
    without_overhang = abjad.sequence.split(
        [abjad.Duration(_) for _ in sequence], weights, cyclic=cyclic, overhang=False
    )
    if sequence_ != without_overhang:
        items = list(sequence_)
        remaining_item = items.pop()
        if remainder == abjad.LEFT:
            if remainder_fuse_threshold is None:
                items.insert(0, remaining_item)
            elif sum(remaining_item) <= remainder_fuse_threshold:
                fused_value = [remaining_item, items[0]]
                fused_value_ = abjad.sequence.flatten(fused_value, depth=-1)
                fused_value = [sum(fused_value_)]
                items[0] = fused_value
            else:
                items.insert(0, remaining_item)
        else:
            if remainder_fuse_threshold is None:
                items.append(remaining_item)
            elif sum(remaining_item) <= remainder_fuse_threshold:
                fused_value = [items[-1], remaining_item]
                fused_value_ = abjad.sequence.flatten(fused_value, depth=-1)
                fused_value = [sum(fused_value_)]
                items[-1] = fused_value
            else:
                items.append(remaining_item)
        sequence_ = items[:]
    assert isinstance(sequence_, list), repr(sequence_)
    return sequence_
