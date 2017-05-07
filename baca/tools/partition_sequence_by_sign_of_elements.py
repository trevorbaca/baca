# -*- coding: utf-8 -*-
import abjad
import itertools


def partition_sequence_by_sign_of_elements(sequence, sign=(-1, 0, 1)):
    '''Partitions `sequence` by sign of elements.

    ::

        >>> import baca

    ::

        >>> sequence = [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

    ..  container:: example

        ::

            >>> baca.partition_sequence_by_sign_of_elements(sequence)
            [[0, 0], [-1, -1], [2, 3], [-5], [1, 2, 5], [-5, -6]]

    ..  container:: example

        ::

            >>> baca.partition_sequence_by_sign_of_elements(
            ...     sequence,
            ...     sign=[-1],
            ...     )
            [0, 0, [-1, -1], 2, 3, [-5], 1, 2, 5, [-5, -6]]

    ..  container:: example

        ::

            >>> baca.partition_sequence_by_sign_of_elements(
            ...     sequence,
            ...     sign=[0],
            ...     )
            [[0, 0], -1, -1, 2, 3, -5, 1, 2, 5, -5, -6]

    ..  container:: example

        ::

            >>> baca.partition_sequence_by_sign_of_elements(
            ...     sequence,
            ...     sign=[1],
            ...     )
            [0, 0, -1, -1, [2, 3], -5, [1, 2, 5], -5, -6]

    ..  container:: example

        ::

            >>> baca.partition_sequence_by_sign_of_elements(
            ...     sequence,
            ...     sign=[-1, 0],
            ...     )
            [[0, 0], [-1, -1], 2, 3, [-5], 1, 2, 5, [-5, -6]]

    ..  container:: example

        ::

            >>> baca.partition_sequence_by_sign_of_elements(
            ...     sequence,
            ...     sign=[-1, 1],
            ...     )
            [0, 0, [-1, -1], [2, 3], [-5], [1, 2, 5], [-5, -6]]

    ..  container:: example

        ::

            >>> baca.partition_sequence_by_sign_of_elements(
            ...     sequence,
            ...     sign=[0, 1],
            ...     )
            [[0, 0], -1, -1, [2, 3], -5, [1, 2, 5], -5, -6]

    ..  container:: example

        ::

            >>> baca.partition_sequence_by_sign_of_elements(
            ...     sequence,
            ...     sign=[-1, 0, 1],
            ...     )
            [[0, 0], [-1, -1], [2, 3], [-5], [1, 2, 5], [-5, -6]]

    Groups negative elements when ``-1`` in `sign`.

    Groups zero-valued elements When ``0`` in `sign`.

    Groups positive elements when ``1`` in `sign`.

    Returns list of tuples of `sequence` element references.
    '''
    result = []
    groups = itertools.groupby(sequence, abjad.mathtools.sign)
    for current_sign, group in groups:
        if current_sign in sign:
            result.append(type(sequence)(group))
        else:
            for item in group:
                result.append(item)
    return result
