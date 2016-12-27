# -*- coding: utf-8 -*-
import abjad


def repeat_runs_in_sequence_to_count(sequence_, tokens):
    '''Repeats subruns in `sequence_` according to `tokens`.

    ::

        >>> import abjad
        >>> import baca

    The `tokens` input parameter must be a list of zero or more ``(start,
    length, count)`` triples.  For every ``(start, length, count)`` token in
    `tokens`, the function copies ``sequence_[start:start+length]`` and inserts
    ``count`` new copies of ``sequence_[start:start+length]`` immediately after
    ``sequence_[start:start+length]`` in `sequence_`.

    Reads the value of ``count`` in every ``(start, length, count)`` triple not
    as the total number of occurrences of ``sequence_[start:start+length]`` to
    appear in `sequence_` after execution, but rather as the number of new
    occurrences of ``sequence_[start:start+length]`` to appear in `sequence_`
    after execution.

    Wraps newly created subruns in tuples.  That is, returns output with one
    more level of nesting than given in input.

    ..  container:: example

        Inserts ``10`` count of ``sequence_[:2]`` at ``sequence_[2:2]``:

        ::

            >>> baca.tools.repeat_runs_in_sequence_to_count(
            ...     range(20), [(0, 2, 10)])
            [0, 1, (0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1),
            2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    ..  container:: example

        Inserts ``5`` count of ``sequence_[10:12]`` at ``sequence_[12:12]`` and
        then inserts ``5`` count of ``sequence_[:2]`` at ``sequence_[2:2]``:

        ::

            >>> numbers = range(20)

        ::

            >>> baca.tools.repeat_runs_in_sequence_to_count(
            ...     numbers,
            ...     [(0, 2, 5), (10, 2, 5)],
            ...     )
            [0, 1, (0, 1, 0, 1, 0, 1, 0, 1, 0, 1), 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
            (10, 11, 10, 11, 10, 11, 10, 11, 10, 11), 12, 13, 14, 15, 16, 17, 18, 
            19]

    Wraps around the end of `sequence_` whenever ``len(sequence_) < start +
    length``.

    Inserts ``2`` count of ``[18, 19, 0, 1]`` at ``sequence_[2:2]``:

    ::

        >>> baca.tools.repeat_runs_in_sequence_to_count(
        ...     numbers,
        ...     [(18, 4, 2)],
        ...     )
        [0, 1, (18, 19, 0, 1, 18, 19, 0, 1), 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 
        12, 13, 14, 15, 16, 17, 18, 19]

    Inserts ``2`` count of ``[18, 19, 0, 1, 2, 3, 4]`` at ``sequence_[4:4]``:

    ::

        >>> baca.tools.repeat_runs_in_sequence_to_count(
        ...     numbers,
        ...     [(18, 8, 2)],
        ...     )
        [0, 1, 2, 3, 4, 5, (18, 19, 0, 1, 2, 3, 4, 5, 18, 19, 0, 1, 2, 3, 
        4, 5), 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    .. todo:: Implement an optional `wrap` keyword to specify whether
        this function should wrap around the ened of `sequence_` whenever
        ``len(sequence_) < start + length`` or not.

    Generalizations of this function would include functions to repeat subruns
    in `sequence_` to not only a certain count, as implemented here, but to a
    certain length, weight or sum. That is,
    ``sequencetools.repeat_subruns_to_length()``,
    ``sequencetools.repeat_subruns_to_weight()``  and
    ``sequencetools.repeat_subruns_to_sum()``.
    '''
    assert all(not isinstance(x, abjad.scoretools.Component) for x in sequence_)
    assert isinstance(tokens, list)
    assert all(len(x) == 3 for x in tokens)
    sequence_ = list(sequence_)
    len_l = len(sequence_)
    instructions = []
    for start, length, count in tokens:
        new_slice = []
        stop = start + length
        for i in range(start, stop):
            new_slice.append(sequence_[i % len_l])
        index = stop % len_l
        instruction = (index, new_slice, count)
        instructions.append(instruction)
    result = sequence_[:]
    for index, new_slice, count in reversed(sorted(instructions)):
        insert = []
        for i in range(count):
            insert.extend(new_slice)
        insert = tuple(insert)
        result.insert(index, insert)
    return result
