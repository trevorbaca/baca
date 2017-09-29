import abjad


def yield_all_partitions_of_integer(n):
    r'''Yields all partitions of positive integer `n` in descending lex order.

    ::

        >>> for partition in baca.tools.yield_all_partitions_of_integer(7):
        ...     partition
        ...
        (7,)
        (6, 1)
        (5, 2)
        (5, 1, 1)
        (4, 3)
        (4, 2, 1)
        (4, 1, 1, 1)
        (3, 3, 1)
        (3, 2, 2)
        (3, 2, 1, 1)
        (3, 1, 1, 1, 1)
        (2, 2, 2, 1)
        (2, 2, 1, 1, 1)
        (2, 1, 1, 1, 1, 1)
        (1, 1, 1, 1, 1, 1, 1)

    Returns generator of positive integer tuples of length at least 1.
    '''
    if not isinstance(n, int):
        message = 'must be integer.'
        raise TypeError(message)
    if not 0 < n:
        message = 'must be positive.'
        raise ValueError(message)
    partition = (n,)
    while partition is not None:
        yield partition
        partition = _next_integer_partition(partition)


def _next_integer_partition(integer_partition):
    _validate_input(integer_partition)
    left_half, right_half = _split_into_left_and_right_halves(
        integer_partition
        )
    # if input was all 1s like (1, 1, 1, 1) then we're done
    if not left_half:
        return None
    new_left_half = left_half[:-1] + [left_half[-1] - 1]
    new_right_weight = sum(right_half) + 1
    new_right_half = _rewrite(new_right_weight, new_left_half[-1])
    result = new_left_half + new_right_half
    result = tuple(result)
    return result


def _split_into_left_and_right_halves(integer_partition):
    r'''Splits not-1s (left half) from 1s (right half).

    _split_into_left_and_right_halves((8, 3))
    [8, 3], []

    _split_into_left_and_right_halves((8, 2, 1))
    [8, 2], [1, ]

    _split_into_left_and_right_halves((8, 1, 1, 1))
    [8], [1, 1, 1]
    '''
    left_half = []
    right_half = []
    for part in integer_partition:
        if not part == 1:
            left_half.append(part)
        else:
            right_half.append(part)
    return left_half, right_half


def _validate_input(integer_partition):
    r'''Ensures monotonically decreasing iterable of positive integers.

    (8, 2, 2, 1) is OK.
    (8, 1, 2, 2) is not.
    '''
    previous = None
    for current in integer_partition:
        if not isinstance(current, int):
            message = 'must be integer.'
            raise TypeError(message)
        if not 0 < current:
            message = 'must be positive.'
            raise ValueError(message)
        if previous is not None:
            if not current <= previous:
                message = 'parts must decrease monotonically.'
                raise ValueError(message)


def _rewrite(n, m):
    r'''Write positive integer n as the sum of many m in a row, followed
    either by nothing or by a final positive integer p such that p is
    strictly less than m.

        _rewrite(8, 4)
        (4, 4)

        _rewrite(8, 3)
        (3, 3, 2)

        _rewrite(8, 2)
        (2, 2, 2, 2)

        _rewrite(8, 1)
        (1, 1, 1, 1, 1, 1, 1, 1)

    '''
    quotient = int(n / m)
    remainder = n % m
    if remainder:
        return [m] * quotient + [remainder]
    else:
        return [m] * quotient
