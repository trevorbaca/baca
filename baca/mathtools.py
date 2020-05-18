import collections
import math

import abjad


def negate_elements(sequence, absolute=False, indices=None, period=None):
    """
    Negates ``sequence`` elements.

    ..  container:: example

        Negates all elements:

        >>> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
        >>> baca.negate_elements(sequence)
        [-1, -2, -3, -4, -5, 6, 7, 8, 9, 10]

    ..  container:: example

        Negates elements at indices 0, 1 and 2:

        >>> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
        >>> baca.negate_elements(sequence, indices=[0, 1, 2])
        [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]

    ..  container:: example

        Negates elements at indices congruent to 0, 1 or 2 mod 5:

        >>> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
        >>> baca.negate_elements(
        ...     sequence,
        ...     indices=[0, 1, 2],
        ...     period=5,
        ...     )
        [-1, -2, -3, 4, 5, 6, 7, 8, -9, -10]

    ..  container:: example

        Negates the absolute value of all elements:

        >>> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
        >>> baca.negate_elements(sequence, absolute=True)
        [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10]

    ..  container:: example

        Negates the absolute value elements at indices 0, 1 and 2:

        >>> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
        >>> baca.negate_elements(
        ...     sequence,
        ...     absolute=True,
        ...     indices=[0, 1, 2],
        ...     )
        [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]

    ..  container:: example

        Negates the absolute value elements at indices congruent to 0, 1 or 2
        mod 5:

        >>> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
        >>> baca.negate_elements(
        ...     sequence,
        ...     absolute=True,
        ...     indices=[0, 1, 2],
        ...     period=5,
        ...     )
        [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]

    Returns newly constructed list.
    """
    indices = indices or range(len(sequence))
    if not isinstance(sequence, collections.abc.Sequence):
        raise Exception(f"must be sequence: {sequence!r}.")
    period = period or len(sequence)
    result = []
    for i, element in enumerate(sequence):
        if (i in indices) or (period and i % period in indices):
            if absolute:
                result.append(-abs(element))
            else:
                result.append(-element)
        else:
            result.append(element)
    return result


# TODO: replace string-valued even='allowed' with constant-valued keyword
def partition_integer_into_halves(n, bigger=abjad.Left, even="allowed"):
    """
    Partitions `n` into halves.

    Writes positive integer `n` as the pair ``(left, right)`` such that
    ``n == left + right``.

    ..   container:: example

        When `n` is odd the greater part of pair corresponds to the value of
        `bigger`:

        >>> baca.partition_integer_into_halves(7, bigger=abjad.Left)
        (4, 3)

        >>> baca.partition_integer_into_halves(7, bigger=abjad.Right)
        (3, 4)

    ..  container:: example

        Likewise when `n` is even and ``even = 'disallowed'``:

        >>> baca.partition_integer_into_halves(
        ...     8,
        ...     bigger=abjad.Left,
        ...     even='disallowed',
        ...     )
        (5, 3)

        >>> baca.partition_integer_into_halves(
        ...     8,
        ...     bigger=abjad.Right,
        ...     even='disallowed',
        ...     )
        (3, 5)

    ..  container:: example

        But when `n` is even and ``even = 'allowed'`` then ``left == right``
        and `bigger` is ignored:

        >>> baca.partition_integer_into_halves(8)
        (4, 4)

        >>> baca.partition_integer_into_halves(8, bigger=abjad.Left)
        (4, 4)

        >>> baca.partition_integer_into_halves(8, bigger=abjad.Right)
        (4, 4)

    ..  container:: example

        When `n` is ``0`` returns ``(0, 0)``:

        >>> baca.partition_integer_into_halves(0)
        (0, 0)

    When `n` is ``0`` and ``even = 'disallowed'`` raises partition error.

    Returns pair of positive integers.
    """
    assert isinstance(n, int), repr(n)
    assert 0 <= n, repr(n)
    if n == 0:
        if even == "disallowed":
            raise Exception(f"even number disallowed: {n!r}.")
        return (0, 0)
    smaller_half = int(math.floor(n / 2))
    bigger_half = n - smaller_half
    if (smaller_half == bigger_half) and (even != "allowed"):
        smaller_half -= 1
        bigger_half += 1
    if bigger == abjad.Left:
        return (bigger_half, smaller_half)
    else:
        return (smaller_half, bigger_half)
