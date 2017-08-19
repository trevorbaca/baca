import abjad
import math


# TODO: replace string-valued even='allowed' with constant-valued keyword
def partition_integer_into_halves(n, bigger=abjad.Left, even='allowed'):
    r'''Partitions `n` into halves.

    ::

        >>> import baca

    Writes positive integer `n` as the pair ``(left, right)`` such that
    ``n == left + right``.

    ..   container:: example

        When `n` is odd the greater part of pair corresponds to the value of
        `bigger`:

        ::

            >>> baca.tools.partition_integer_into_halves(7, bigger=abjad.Left)
            (4, 3)

        ::

            >>> baca.tools.partition_integer_into_halves(7, bigger=abjad.Right)
            (3, 4)

    ..  container:: example

        Likewise when `n` is even and ``even = 'disallowed'``:

        ::

            >>> baca.tools.partition_integer_into_halves(
            ...     8,
            ...     bigger=abjad.Left,
            ...     even='disallowed',
            ...     )
            (5, 3)

        ::

            >>> baca.tools.partition_integer_into_halves(
            ...     8,
            ...     bigger=abjad.Right,
            ...     even='disallowed',
            ...     )
            (3, 5)

    ..  container:: example

        But when `n` is even and ``even = 'allowed'`` then ``left == right``
        and `bigger` is ignored:

        ::

            >>> baca.tools.partition_integer_into_halves(8)
            (4, 4)

        ::

            >>> baca.tools.partition_integer_into_halves(8, bigger=abjad.Left)
            (4, 4)

        ::

            >>> baca.tools.partition_integer_into_halves(8, bigger=abjad.Right)
            (4, 4)

    ..  container:: example

        When `n` is ``0`` returns ``(0, 0)``:

        ::

            >>> baca.tools.partition_integer_into_halves(0)
            (0, 0)

    When `n` is ``0`` and ``even = 'disallowed'`` raises partition error.

    Returns pair of positive integers.
    '''
    assert isinstance(n, int), repr(n)
    assert 0 <= n, repr(n)
    if n == 0:
        if even == 'disallowed':
            message = 'even number disallowed: {!r}.'
            message = message.format(n)
            raise Exception(message)
        return (0, 0)
    smaller_half = int(math.floor(n / 2))
    bigger_half = n - smaller_half
    if (smaller_half == bigger_half) and (even != 'allowed'):
        smaller_half -= 1
        bigger_half += 1
    if bigger == abjad.Left:
        return (bigger_half, smaller_half)
    else:
        return (smaller_half, bigger_half)
