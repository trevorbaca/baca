import abjad
import baca


def increase_elements(sequence, addenda, indices=None):
    '''Increases `sequence` cyclically by `addenda`.

    ::

        >>> import baca

    ..  container:: example

        Increases range elements by ``10`` and ``-10`` in alternation:

        ::

            >>> baca.increase_elements(range(10), [10, -10])
            [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]


    ..  container:: example

        Increases list elements by 10 and -10 in alternation:

        ::

            >>> baca.increase_elements(list(range(10)), [10, -10])
            [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]

    ..  container:: example

        Increases tuple elements by 10 and -10 in alternation:

        ::

            >>> baca.increase_elements(tuple(range(10)), [10, -10])
            [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]

    ..  container:: example

        Increases pairs of elements by ``0.5`` starting at indices 0, 4, 8:

        ::

            >>> sequence = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
            >>> addenda = [0.5, 0.5]
            >>> indices = [0, 4, 8]
            >>> baca.increase_elements(sequence, addenda, indices)
            [1.5, 1.5, 2, 3, 5.5, 5.5, 1, 2, 5.5, 5.5, 6]

    ..  container:: example

        ::

            >>> baca.increase_elements(range(10), [2, 0])
            [2, 1, 4, 3, 6, 5, 8, 7, 10, 9]

    ..  container:: example

        ::


            >>> sequence_1 = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
            >>> baca.increase_elements(
            ...     sequence_1, [0.5, 0.5], indices=[0, 4, 8]
            ...     )
            [1.5, 1.5, 2, 3, 5.5, 5.5, 1, 2, 5.5, 5.5, 6]

    Returns list.
    '''
    sequence = list(sequence)
    if indices is None:
        result = []
        for i, element in enumerate(sequence):
            new = element + addenda[i % len(addenda)]
            result.append(new)
    else:
        # assert no overlaps
        tmp = [tuple(range(i, len(addenda))) for i in indices]
        tmp = baca.Sequence(tmp).flatten()
        assert len(tmp) == len(set(tmp))
        result = sequence[:]
        for i in indices:
            for j in range(len(addenda)):
                result[i + j] += addenda[j]
    assert isinstance(result, list)
    return result
