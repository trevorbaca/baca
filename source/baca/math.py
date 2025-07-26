"""
Math.
"""

import math

import abjad


def insert_and_transpose(notes, subrun_tokens):
    """
    Inserts and transposes nested subruns in ``notes`` according to
    ``subrun_tokens``.

    >>> notes = [abjad.Note(_, (1, 4)) for _ in [0, 2, 7, 9, 5, 11, 4]]
    >>> subrun_tokens = [(0, [2, 4]), (4, [3, 1])]
    >>> baca.math.insert_and_transpose(notes, subrun_tokens)

    >>> result = []
    >>> for note in notes:
    ...   try:
    ...        result.append(note.get_written_pitch().get_number())
    ...   except AttributeError:
    ...        result.append([_.get_written_pitch().get_number() for _ in note])

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

    This function is designed to work on a built-in Python list of notes. This function
    is **not** designed to work on Abjad voices, staves or other containers because the
    function currently implements no spanner-handling. That is, this function is designed
    to be used during precomposition.

    Returns list of integers and / or floats.
    """
    assert isinstance(notes, list)
    assert all(isinstance(_, abjad.Note) for _ in notes)
    assert isinstance(subrun_tokens, list)
    len_notes = len(notes)
    instructions = []
    for subrun_token in subrun_tokens:
        pairs = _make_index_length_pairs(subrun_token)
        for anchor_index, subrun_length in pairs:
            anchor_note = notes[anchor_index % len_notes]
            anchor_pitch = abjad.NamedPitch(anchor_note)
            anchor_written_duration = anchor_note.get_written_duration()
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
    for first, second in abjad.sequence.nwise(subrun_source):
        first_pitch = abjad.NamedPitch(first)
        second_pitch = abjad.NamedPitch(second)
        interval = (
            abjad.NumberedPitch(second_pitch).get_number()
            - abjad.NumberedPitch(first_pitch).get_number()
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
        new_pc = abjad.NumberedPitch(anchor_pitch).get_number()
        new_pc += subrun_interval
        new_pc %= 12
        new_note = abjad.Note(new_pc, anchor_written_duration)
        new_notes.append(new_note)
    return new_notes


def partition_integer_into_halves(n, bigger=abjad.LEFT, allow_even=True):
    """
    Partitions ``n`` into halves.

    Writes positive integer ``n`` as the pair ``(left, right)`` such that ``n == left +
    right``.

    ..   container:: example

        When ``n`` is odd the greater part of pair corresponds to the value of ``bigger``

        >>> baca.math.partition_integer_into_halves(7, bigger=abjad.LEFT)
        (4, 3)

        >>> baca.math.partition_integer_into_halves(7, bigger=abjad.RIGHT)
        (3, 4)

    ..  container:: example

        Likewise when ``n`` is even and ``allow_even`` is false:

        >>> baca.math.partition_integer_into_halves(8, bigger=abjad.LEFT, allow_even=False)
        (5, 3)

        >>> baca.math.partition_integer_into_halves(8, bigger=abjad.RIGHT, allow_even=False)
        (3, 5)

    ..  container:: example

        But when ``n`` is even and ``allow_even`` is true then ``left == right`` and
        ``bigger`` is ignored:

        >>> baca.math.partition_integer_into_halves(8)
        (4, 4)

        >>> baca.math.partition_integer_into_halves(8, bigger=abjad.LEFT)
        (4, 4)

        >>> baca.math.partition_integer_into_halves(8, bigger=abjad.RIGHT)
        (4, 4)

    ..  container:: example

        When ``n`` is ``0`` returns ``(0, 0)``:

        >>> baca.math.partition_integer_into_halves(0)
        (0, 0)

    Raises excepton when ``n`` is ``0`` and ``allow_even`` is false.
    """
    assert isinstance(n, int), repr(n)
    assert 0 <= n, repr(n)
    assert bigger in (abjad.LEFT, abjad.RIGHT), repr(bigger)
    assert allow_even in (True, False), repr(allow_even)
    if n == 0:
        if not allow_even:
            raise Exception(f"even number disallowed: {n!r}.")
        return (0, 0)
    smaller_half = int(math.floor(n / 2))
    bigger_half = n - smaller_half
    if smaller_half == bigger_half and not allow_even:
        smaller_half -= 1
        bigger_half += 1
    if bigger == abjad.LEFT:
        return (bigger_half, smaller_half)
    else:
        return (smaller_half, bigger_half)


def list_related_tempos(
    metronome_mark,
    maximum_numerator=None,
    maximum_denominator=None,
    integer_tempos_only=False,
) -> list[tuple[abjad.MetronomeMark, tuple[int, int]]]:
    r"""
    Lists related tempos.

    Rewrites tempo ``4=58`` by ratios ``n:d`` such that ``1 <= n <= 8`` and ``1 <= d
    <= 8``:

    ..  container:: example

        >>> pairs = baca.math.list_related_tempos(
        ...     abjad.MetronomeMark(abjad.Duration(1, 4), 58),
        ...     maximum_numerator=8,
        ...     maximum_denominator=8,
        ...  )

        >>> for tempo, ratio in pairs:
        ...     print(f"{tempo}:")
        ...     print(f"    {ratio!r}")
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(29, 1), textual_indication=None, custom_markup=None, decimal=False):
            (1, 2)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(232, 7), textual_indication=None, custom_markup=None, decimal=False):
            (4, 7)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(174, 5), textual_indication=None, custom_markup=None, decimal=False):
            (3, 5)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(145, 4), textual_indication=None, custom_markup=None, decimal=False):
            (5, 8)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(116, 3), textual_indication=None, custom_markup=None, decimal=False):
            (2, 3)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(290, 7), textual_indication=None, custom_markup=None, decimal=False):
            (5, 7)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(87, 2), textual_indication=None, custom_markup=None, decimal=False):
            (3, 4)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(232, 5), textual_indication=None, custom_markup=None, decimal=False):
            (4, 5)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(145, 3), textual_indication=None, custom_markup=None, decimal=False):
            (5, 6)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(348, 7), textual_indication=None, custom_markup=None, decimal=False):
            (6, 7)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(203, 4), textual_indication=None, custom_markup=None, decimal=False):
            (7, 8)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(58, 1), textual_indication=None, custom_markup=None, decimal=False):
            (1, 1)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(464, 7), textual_indication=None, custom_markup=None, decimal=False):
            (8, 7)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(203, 3), textual_indication=None, custom_markup=None, decimal=False):
            (7, 6)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(348, 5), textual_indication=None, custom_markup=None, decimal=False):
            (6, 5)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(145, 2), textual_indication=None, custom_markup=None, decimal=False):
            (5, 4)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(232, 3), textual_indication=None, custom_markup=None, decimal=False):
            (4, 3)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(406, 5), textual_indication=None, custom_markup=None, decimal=False):
            (7, 5)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(87, 1), textual_indication=None, custom_markup=None, decimal=False):
            (3, 2)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(464, 5), textual_indication=None, custom_markup=None, decimal=False):
            (8, 5)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(290, 3), textual_indication=None, custom_markup=None, decimal=False):
            (5, 3)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(203, 2), textual_indication=None, custom_markup=None, decimal=False):
            (7, 4)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(116, 1), textual_indication=None, custom_markup=None, decimal=False):
            (2, 1)

    ..  container:: example

        Integer-valued tempos only:

        >>> pairs = baca.math.list_related_tempos(
        ...     abjad.MetronomeMark(abjad.Duration(1, 4), 58),
        ...     maximum_numerator=16,
        ...     maximum_denominator=16,
        ...     integer_tempos_only=True,
        ...  )

        >>> for tempo, ratio in pairs:
        ...     print(f"{tempo}:")
        ...     print(f"    {ratio!r}")
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(29, 1), textual_indication=None, custom_markup=None, decimal=False):
            (1, 2)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(58, 1), textual_indication=None, custom_markup=None, decimal=False):
            (1, 1)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(87, 1), textual_indication=None, custom_markup=None, decimal=False):
            (3, 2)
        MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=Fraction(116, 1), textual_indication=None, custom_markup=None, decimal=False):
            (2, 1)

    Constrains ratios such that ``1:2 <= n:d <= 2:1``.
    """
    allowable_numerators = range(1, maximum_numerator + 1)
    allowable_denominators = range(1, maximum_denominator + 1)
    numbers = [allowable_numerators, allowable_denominators]
    pairs = abjad.enumerate.outer_product(numbers)
    multipliers = [abjad.Fraction(*_) for _ in pairs]
    multipliers = [
        _ for _ in multipliers if abjad.Fraction(1, 2) <= _ <= abjad.Fraction(2)
    ]
    multipliers.sort()
    multipliers_ = abjad.sequence.remove_repeats(multipliers)
    pairs = []
    for multiplier in multipliers_:
        new_units_per_minute = multiplier * metronome_mark.units_per_minute
        if integer_tempos_only and not abjad.math.is_integer_equivalent_number(
            new_units_per_minute
        ):
            continue
        metronome_mark_ = abjad.MetronomeMark(
            reference_duration=metronome_mark.reference_duration,
            units_per_minute=new_units_per_minute,
        )
        pair = abjad.duration.pair(multiplier)
        pairs.append((metronome_mark_, pair))
    return pairs
