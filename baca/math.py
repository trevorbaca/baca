import collections
import math

import abjad

from .classes import Sequence


def increase_elements(sequence, addenda, indices=None):
    """
    Increases ``sequence`` cyclically by ``addenda``.

    ..  container:: example

        Increases range elements by ``10`` and ``-10`` in alternation:

        >>> baca.increase_elements(range(10), [10, -10])
        [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]


    ..  container:: example

        Increases list elements by 10 and -10 in alternation:

        >>> baca.increase_elements(list(range(10)), [10, -10])
        [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]

    ..  container:: example

        Increases tuple elements by 10 and -10 in alternation:

        >>> baca.increase_elements(tuple(range(10)), [10, -10])
        [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]

    ..  container:: example

        Increases pairs of elements by ``0.5`` starting at indices 0, 4, 8:

        >>> sequence = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
        >>> addenda = [0.5, 0.5]
        >>> indices = [0, 4, 8]
        >>> baca.increase_elements(sequence, addenda, indices)
        [1.5, 1.5, 2, 3, 5.5, 5.5, 1, 2, 5.5, 5.5, 6]

    ..  container:: example

        >>> baca.increase_elements(range(10), [2, 0])
        [2, 1, 4, 3, 6, 5, 8, 7, 10, 9]

    ..  container:: example

        >>> sequence_1 = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
        >>> baca.increase_elements(
        ...     sequence_1, [0.5, 0.5], indices=[0, 4, 8]
        ...     )
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
        tmp = Sequence(tmp).flatten()
        assert len(tmp) == len(set(tmp))
        result = sequence[:]
        for i in indices:
            for j in range(len(addenda)):
                result[i + j] += addenda[j]
    assert isinstance(result, list)
    return result


def insert_and_transpose(notes, subrun_tokens):
    """
    Inserts and transposes nested subruns in ``notes`` according to
    ``subrun_tokens``.

    >>> notes = [abjad.Note(_, (1, 4)) for _ in [0, 2, 7, 9, 5, 11, 4]]
    >>> subrun_tokens = [(0, [2, 4]), (4, [3, 1])]
    >>> baca.insert_and_transpose(notes, subrun_tokens)

    >>> result = []
    >>> for note in notes:
    ...   try:
    ...        result.append(note.written_pitch.number)
    ...   except AttributeError:
    ...        result.append([_.written_pitch.number for _ in note])

    >>> result
    [0, [5, 7], 2, [4, 0, 6, 11], 7, 9, 5, [10, 6, 8], 11, [7], 4]

    Set ``subrun_tokens`` to a list of zero or more ``(index, length_list)``
    pairs.

    For each ``(index, length_list)`` pair in *subrun_tokens* the function will
    read *index* mod ``len(notes)`` and insert a subrun of length
    ``length_list[0]`` immediately after ``notes[index]``, a subrun of length
    ``length_list[1]`` immediately after ``notes[index+1]``, and, in general, a
    subrun of ``length_list[i]`` immediately after ``notes[index+i]``, for ``i
    < length(length_list)``.

    New subruns are wrapped with lists. These wrapper lists are designed to
    allow inspection of the structural changes to ``notes`` immediately after
    the function returns. For this reason most calls to this function will be
    followed by flattening.

    >>> for note in notes:
    ...     note
    ...
    Note("c'4")
    [Note("f'4"), Note("g'4")]
    Note("d'4")
    [Note("e'4"), Note("c'4"), Note("fs'4"), Note("b'4")]
    Note("g'4")
    Note("a'4")
    Note("f'4")
    [Note("bf'4"), Note("fs'4"), Note("af'4")]
    Note("b'4")
    [Note("g'4")]
    Note("e'4")

    This function is designed to work on a built-in Python list of notes. This
    function is **not** designed to work on Abjad voices, staves or other
    containers because the function currently implements no spanner-handling.
    That is, this function is designed to be used during precomposition.

    Returns list of integers and / or floats.
    """
    assert isinstance(notes, list)
    assert all(isinstance(x, abjad.Note) for x in notes)
    assert isinstance(subrun_tokens, list)
    len_notes = len(notes)
    instructions = []
    for subrun_token in subrun_tokens:
        pairs = _make_index_length_pairs(subrun_token)
        for anchor_index, subrun_length in pairs:
            anchor_note = notes[anchor_index % len_notes]
            anchor_pitch = abjad.NamedPitch(anchor_note)
            anchor_written_duration = anchor_note.written_duration
            source_start_index = anchor_index + 1
            source_stop_index = source_start_index + subrun_length + 1
            cyclic_notes = abjad.CyclicTuple(notes)
            subrun_source = cyclic_notes[source_start_index:source_stop_index]
            subrun_intervals = _get_intervals_in_subrun(subrun_source)
            new_notes = _make_new_notes(
                anchor_pitch, anchor_written_duration, subrun_intervals
            )
            instruction = (anchor_index, new_notes)
            instructions.append(instruction)
    for anchor_index, new_notes in reversed(sorted(instructions)):
        notes.insert(anchor_index + 1, new_notes)


def _get_intervals_in_subrun(subrun_source):
    subrun_source = list(subrun_source)
    result = [0]
    for first, second in abjad.Sequence(subrun_source).nwise():
        first_pitch = abjad.NamedPitch(first)
        second_pitch = abjad.NamedPitch(second)
        interval = (
            abjad.NumberedPitch(second_pitch).number
            - abjad.NumberedPitch(first_pitch).number
        )
        result.append(interval + result[-1])
    result.pop(0)
    return result


def _make_index_length_pairs(subrun_token):
    anchor_index, subrun_lengths = subrun_token
    num_subruns = len(subrun_lengths)
    pairs = []
    for i in range(num_subruns):
        start_index = anchor_index + i
        subrun_length = subrun_lengths[i]
        pair = (start_index, subrun_length)
        pairs.append(pair)
    return pairs


def _make_new_notes(anchor_pitch, anchor_written_duration, subrun_intervals):
    new_notes = []
    for subrun_interval in subrun_intervals:
        new_pc = abjad.NumberedPitch(anchor_pitch).number
        new_pc += subrun_interval
        new_pc %= 12
        new_note = abjad.Note(new_pc, anchor_written_duration)
        new_notes.append(new_note)
    return new_notes


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


def overwrite_elements(sequence, pairs):
    """
    Overwrites ``sequence`` elements at indices according to ``pairs``.

    ..  container:: example

        Overwrites range elements:

        >>> pairs = [(0, 3), (5, 3)]
        >>> baca.overwrite_elements(range(10), pairs)
        [0, 0, 0, 3, 4, 5, 5, 5, 8, 9]

        Returns list.

    ..  container:: example

        Overwrites list elements:

        >>> pairs = [(0, 3), (5, 3)]
        >>> baca.overwrite_elements(list(range(10)), pairs)
        [0, 0, 0, 3, 4, 5, 5, 5, 8, 9]

        Returns new list.

    ..  container:: example

        Overwrites tuple elements:

        >>> pairs = [(0, 3), (5, 3)]
        >>> baca.overwrite_elements(tuple(range(10)), pairs)
        [0, 0, 0, 3, 4, 5, 5, 5, 8, 9]

        Returns list.

    ..  container:: example

        Overwrites all items:

        >>> baca.overwrite_elements(range(10), [(0, 99)])
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


# TODO: replace string-valued even='allowed' with constant-valued keyword
def partition_integer_into_halves(n, bigger=abjad.Left, even="allowed"):
    """
    Partitions ``n`` into halves.

    Writes positive integer ``n`` as the pair ``(left, right)`` such that
    ``n == left + right``.

    ..   container:: example

        When ``n`` is odd the greater part of pair corresponds to the value of
        ``bigger``

        >>> baca.partition_integer_into_halves(7, bigger=abjad.Left)
        (4, 3)

        >>> baca.partition_integer_into_halves(7, bigger=abjad.Right)
        (3, 4)

    ..  container:: example

        Likewise when ``n`` is even and ``even = 'disallowed'``:

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

        But when ``n`` is even and ``even = 'allowed'`` then ``left == right``
        and ``bigger`` is ignored:

        >>> baca.partition_integer_into_halves(8)
        (4, 4)

        >>> baca.partition_integer_into_halves(8, bigger=abjad.Left)
        (4, 4)

        >>> baca.partition_integer_into_halves(8, bigger=abjad.Right)
        (4, 4)

    ..  container:: example

        When ``n`` is ``0`` returns ``(0, 0)``:

        >>> baca.partition_integer_into_halves(0)
        (0, 0)

    When ``n`` is ``0`` and ``even = 'disallowed'`` raises partition error.

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


def partition_nested_into_inward_pointing_parts(list_, target="negative"):
    """
    Partitions integers in ``list_`` into inward-pointing parts.

    ..  container:: example

        >>> list_ = [[1, 1, 5]]
        >>> baca.partition_nested_into_inward_pointing_parts(list_)
        [[1, 1, 5]]

        >>> list_ = [[1, 1, -5]]
        >>> baca.partition_nested_into_inward_pointing_parts(list_)
        [[1, 1, 1, -4]]

        >>> list_ = [[1], [5], [5, 1], [1, 5], [5, 5], [1, 5, 1]]
        >>> baca.partition_nested_into_inward_pointing_parts(
        ...    list_, target='positive')
        [[1], [4, 1], [4, 1, 1], [1, 1, 4], [4, 1, 1, 4], [1, 4, 1, 1]]

        >>> list_ = [[1, 1, -5]]
        >>> baca.partition_nested_into_inward_pointing_parts(
        ...    list_, target='positive')
        [[1, 1, -5]]

    """
    result = []
    if target == "negative":
        for element in list_:
            # -5 at beginning
            if element[0] == -5:
                result.append([-4, 1] + element[1:])
            # -5 at end
            elif element[-1] == -5:
                result.append(element[:-1] + [1, -4])
            # -5 in middle
            elif -5 in element:
                new = []
                for x in element:
                    if x != -5:
                        new.append(x)
                    else:
                        new.append(-4)
                        new.append(1)
            # no -5
            else:
                result.append(element)
    if target == "positive":
        for sublist in list_:
            new = sublist
            # 5 at beginning
            if new[0] == 5:
                new = [4, 1] + new[1:]
            # 5 at end
            if new[-1] == 5:
                new = new[:-1] + [1, 4]
            # 5 in middle
            if 5 in new:
                new = [(4, 1) if element == 5 else element for element in new]
                new = Sequence(new).flatten()
                new = list(new)
            result.append(new)
    return result


def repeat_subruns_to_length(notes, pairs, history=False):
    """
    Repeats ``notes`` according to ``pairs``.

    ..  container:: example

        >>> list_ = [abjad.Note(_, (1, 4)) for _ in [0, 2, 4, 5, 7, 9, 11]]
        >>> baca.repeat_subruns_to_length(list_, [(0, 4, 1), (2, 4, 1)])
        [Note("c'4"), Note("d'4"), Note("e'4"), Note("f'4"), Note("c'4"),
        Note("d'4"), Note("e'4"), Note("f'4"), Note("g'4"), Note("a'4"),
        Note("e'4"), Note("f'4"), Note("g'4"), Note("a'4"), Note("b'4")]

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
            pitch_number = source.written_pitch.number
            new_note = abjad.Note(pitch_number, source.written_duration)
            if history:
                abjad.attach(history, new_note)
            new_notes.append(new_note)
        reps = pair[-1]
        instruction = (pair[0] + pair[1], new_notes, reps)
        instructions.append(instruction)
    for index, new_notes, reps in reversed(sorted(instructions)):
        new_notes = abjad.select(new_notes)
        # new_notes = abjad.mutate.copy(new_notes, n=reps)
        total = []
        for _ in range(reps):
            abjad.mutate.copy(new_notes)
            total.extend(new_notes)
        total = abjad.select(total)
        notes[index:index] = total
    return notes
