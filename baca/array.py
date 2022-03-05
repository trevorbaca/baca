"""
Array.
"""
import copy
import numbers
import typing

import abjad


def _get_leaf_offsets(argment):
    offsets = []
    for leaf in abjad.iterate.leaves(argment):
        start_offset = abjad.get.timespan(leaf).start_offset
        if start_offset not in offsets:
            offsets.append(start_offset)
        stop_offset = abjad.get.timespan(leaf).stop_offset
        if stop_offset not in offsets:
            offsets.append(stop_offset)
    offsets.sort()
    return list(abjad.math.difference_series(offsets))


def _make_multiplied_quarter_notes(durations):
    notes = []
    written_duration = abjad.Duration(1, 4)
    for duration in durations:
        multiplier = duration / written_duration
        note = abjad.Note(0, written_duration, multiplier=multiplier)
        notes.append(note)
    return notes


class PitchArray:
    """
    Pitch array.

    ..  container:: example

        A two-by-three pitch array:

        >>> pitch_array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])
        >>> print(pitch_array)
        [ ] [     ] [ ]
        [     ] [ ] [ ]

        >>> pitch_array
        PitchArray(rows=(PitchArrayRow(cells=(PitchArrayCell(width=1), PitchArrayCell(width=2), PitchArrayCell(width=1))), PitchArrayRow(cells=(PitchArrayCell(width=2), PitchArrayCell(width=1), PitchArrayCell(width=1)))))

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_columns", "_rows")

    ### INITIALIZER ###

    def __init__(self, rows=None):
        self._rows = []
        self._columns = []
        if not rows:
            return
        for row in rows:
            row_ = PitchArrayRow([])
            for cell in row:
                if isinstance(cell, int):
                    cell = PitchArrayCell(width=cell)
                elif isinstance(cell, tuple):
                    assert len(cell) == 2, repr(cell)
                    if isinstance(cell[0], tuple):
                        assert len(cell[0]) == 2, repr(cell)
                        pitch = abjad.NamedPitch(cell[0])
                        width = cell[1]
                        cell = PitchArrayCell(pitches=[pitch], width=width)
                    elif isinstance(cell[0], str):
                        pitch = abjad.NamedPitch(cell)
                        pitches = [pitch]
                        cell = PitchArrayCell(pitches=pitches)
                    elif isinstance(cell[0], (int, float)):
                        pitch_number, width = cell
                        pitch = abjad.NamedPitch(pitch_number)
                        cell = PitchArrayCell(pitches=[pitch], width=width)
                    elif isinstance(cell[0], list):
                        assert all(isinstance(_, (int, float)) for _ in cell[0])
                        pitch_numbers, width = cell
                        pitches = [abjad.NamedPitch(_) for _ in pitch_numbers]
                        cell = PitchArrayCell(pitches=pitches, width=width)
                    else:
                        raise Exception(cell)
                else:
                    assert isinstance(cell, PitchArrayCell), repr(cell)
                row_.append(cell)
            self.append_row(row_)

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        """
        Concatenates ``argument`` to pitch array.

        Returns new pitch array.
        """
        assert isinstance(argument, PitchArray), repr(argument)
        assert self.depth == argument.depth, repr((self.depth, argument.depth))
        new_array = PitchArray([])
        for self_row, arg_row in zip(self.rows, argument.rows):
            new_row = self_row + arg_row
            new_array.append_row(new_row)
        return new_array

    def __contains__(self, argument):
        """
        Is true when pitch array contains ``argument``.

        Returns true or false.
        """
        if isinstance(argument, PitchArrayRow):
            return argument in self.rows
        elif isinstance(argument, PitchArrayColumn):
            return argument in self.columns
        elif isinstance(argument, PitchArrayCell):
            return argument in self.cells
        elif isinstance(argument, abjad.NamedPitch):
            for pitch in self.pitches:
                if argument == pitch:
                    return True
            return False
        else:
            raise Exception("must be row, column, pitch or pitch cell.")

    def __copy__(self):
        """
        Copies pitch array.

        Returns new pitch array.
        """
        return type(self)(self.cell_tokens_by_row)

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a pitch aarray with contents equal to that of this
        pitch array.

        Returns true or false.
        """
        if isinstance(argument, type(self)):
            for self_row, arg_row in zip(self.rows, argument.rows):
                if not self_row == arg_row:
                    return False
                return True
        return False

    def __getitem__(self, argument):
        """
        Gets row ``argument`` from pitch array.

        Returns pitch array row.
        """
        return self.rows.__getitem__(argument)

    def __hash__(self):
        """
        Hashes pitch array.
        """
        return super().__hash__()

    def __iadd__(self, argument):
        """
        Adds ``argument`` to pitch array in place.

        ..  container:: example

            >>> array_1 = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])
            >>> print(array_1)
            [ ] [     ] [ ]
            [     ] [ ] [ ]

            >>> array_2 = baca.array.PitchArray([[3, 4], [4, 3]])
            >>> print(array_2)
            [   ] [   ]
            [     ] [   ]

            >>> array_3 = baca.array.PitchArray([[1, 1], [1, 1]])
            >>> print(array_3)
            [ ] [ ]
            [ ] [ ]

            >>> array_1 += array_2
            >>> print(array_1)
            [ ] [     ] [ ] [   ] [   ]
            [     ] [ ] [ ] [     ] [   ]

            >>> array_1 += array_3
            >>> print(array_1)
            [ ] [     ] [ ] [   ] [   ] [ ] [ ]
            [     ] [ ] [ ] [     ] [   ] [ ] [ ]

        Returns pitch array.
        """
        assert isinstance(argument, PitchArray), repr(argument)
        for self_row, arg_row in zip(self.rows, argument.rows):
            self_row += arg_row
        return self

    def __ne__(self, argument):
        """
        Is true when pitch array does not equal ``argument``.

        Returns true or false.
        """
        return not self == argument

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}(rows={self.rows})"

    def __setitem__(self, i, argument):
        """
        Sets pitch array row ``i`` to ``argument``.

        Retunrs none.
        """
        assert isinstance(i, int), repr(i)
        assert isinstance(argument, PitchArrayRow), repr(argument)
        self._rows[i]._parent_array = None
        argument._parent_array = self
        self._rows[i] = argument

    def __str__(self):
        """
        String representation of pitch array.

        Returns string.
        """
        return self._two_by_two_format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _two_by_two_format_string(self):
        return "\n".join([str(_) for _ in self.rows])

    ### PRIVATE METHODS ###

    def _column_format_width_at_index(self, index):
        columns = self.columns
        column = columns[index]
        return column._column_format_width

    def _format_cells(self, cells):
        result = [str(cell) for cell in cells]
        result = " ".join(result)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def cell_tokens_by_row(self):
        """
        Gets cells tokens of pitch array by row.

        Returns tuple.
        """
        return tuple([row.cell_tokens for row in self.rows])

    @property
    def cell_widths_by_row(self):
        """
        Gets cell widths of pitch array by row.

        Returns tuple.
        """
        return tuple([row.cell_widths for row in self.rows])

    @property
    def cells(self):
        """
        Gets cells of pitch array.

        Returns set.
        """
        cells = set([])
        for row in self.rows:
            cells.update(row.cells)
        return cells

    @property
    def columns(self):
        """
        Gets columns of pitch array.

        Returns tuple.
        """
        columns = []
        cells = abjad.sequence.zip(self.rows, truncate=False)
        for i, cells in enumerate(cells):
            column = PitchArrayColumn(cells)
            column._parent_array = self
            column._column_index = i
            columns.append(column)
        return tuple(columns)

    @property
    def depth(self):
        """
        Gets depth of pitch array.

        Defined equal to number of pitch array rows in pitch array.

        Returns nonnegative integer.
        """
        return len(self.rows)

    @property
    def dimensions(self):
        """
        Gets dimensions of pitch array.

        Returns pair.
        """
        return self.depth, self.width

    @property
    def has_voice_crossing(self):
        """
        Is true when pitch array has voice crossing.

        ..  container:: example

            >>> array = baca.array.PitchArray([
            ...     [1, (2, 1), (-1.5, 2)],
            ...     [(7, 2), (6, 1), 1],
            ... ])

            >>> print(array)
            [  ] [d'] [bqf    ]
            [g'     ] [fs'] [ ]

            >>> array.has_voice_crossing
            True

        Returns true or false.
        """
        for column in self.columns:
            if column.has_voice_crossing:
                return True
        return False

    @property
    def is_rectangular(self):
        """
        Is true when no rows in pitch array are defective.

        Returns true or false.
        """
        return all(not row.is_defective for row in self.rows)

    @property
    def pitches(self):
        """
        Gets pitches in pitch array.

        Returns tuple.
        """
        return abjad.sequence.flatten(self.pitches_by_row, depth=-1)

    @property
    def pitches_by_row(self):
        """
        Gets pitches in pitch array by row.

        Returns tuple.
        """
        pitches = []
        for row in self.rows:
            pitches.append(row.pitches)
        return tuple(pitches)

    @property
    def rows(self):
        """
        Gets rows in pitch array.

        Returns tuple.
        """
        return tuple(self._rows)

    @property
    def size(self):
        """
        Gets size of pitch array.

        Defined equal to the product of depth and width.

        Returns nonnegative integer.
        """
        return self.depth * self.width

    @property
    def voice_crossing_count(self):
        """
        Gets voice crossing count of pitch array.

        Returns nonnegative integer.
        """
        count = 0
        for column in self.columns:
            if column.has_voice_crossing:
                count += 1
        return count

    @property
    def weight(self):
        """
        Gets weight of pitch array.

        Defined equal to the sum of the weight of the rows in pitch array.

        Returns nonnegative integer.
        """
        return sum([row.weight for row in self.rows])

    @property
    def width(self):
        """
        Gets width of pitch array.

        Defined equal to the width of the widest row in pitch array.

        Returns nonnegative integer.
        """
        try:
            return max([row.width for row in self.rows])
        except ValueError:
            return 0

    ### PUBLIC METHODS ###

    def append_column(self, column):
        """
        Appends ``column`` to pitch array.

        Returns none.
        """
        assert isinstance(column, PitchArrayColumn), repr(column)
        column._parent_array = self
        column_depth = column.depth
        if self.depth < column_depth:
            self.pad_to_depth(column_depth)
        self.pad_to_width(self.width)
        for row, cell in zip(self.rows, column):
            row.append(cell)

    def append_row(self, row):
        """
        Appends ``row`` to pitch array.

        Returns none.
        """
        assert isinstance(row, PitchArrayRow), repr(row)
        row._parent_array = self
        self._rows.append(row)

    def apply_pitches_by_row(self, pitch_lists):
        """
        Applies ``pitch_lists`` to pitch array by row.

        ..  container:: example

            >>> array = baca.array.PitchArray([
            ...     [1, (0, 1), (0, 2)],
            ...     [(0, 2), (0, 1), 1],
            ... ])

            >>> print(array)
            [  ] [c'] [c'    ]
            [c'     ] [c'] [ ]

            >>> array.apply_pitches_by_row([[-2, -1.5], [7, 6]])

            >>> print(array)
            [  ] [bf] [bqf    ]
            [g'     ] [fs'] [ ]

        Returns none.
        """
        for row, pitch_list in zip(self.rows, pitch_lists):
            row.apply_pitches(pitch_list)

    def copy_subarray(self, upper_left_pair, lower_right_pair):
        """
        Copies subarray of pitch array.

        ..  container:: example

            >>> array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])
            >>> array[0].cells[0].append_pitch(0)
            >>> array[0].cells[1].append_pitch(2)
            >>> array[1].cells[2].append_pitch(4)

            >>> print(array)
            [c'] [d'    ] [  ]
            [       ] [ ] [e']

            >>> subarray = array.copy_subarray((0, 0), (2, 2))

            >>> print(subarray)
            [c'] [d']
            [       ]

        Returns new pitch array.
        """
        assert isinstance(upper_left_pair, tuple), repr(upper_left_pair)
        assert isinstance(lower_right_pair, tuple), repr(lower_right_pair)
        start_i, start_j = upper_left_pair
        stop_i, stop_j = lower_right_pair
        if not start_i <= stop_i:
            raise Exception("start row must not be greater than stop row.")
        if not start_j <= stop_j:
            raise Exception("start column must not be greater than stop column.")
        new_array = type(self)([])
        rows = self.rows
        row_indices = range(start_i, stop_i)
        for row_index in row_indices:
            new_row = rows[row_index].copy_subrow(start_j, stop_j)
            new_array.append_row(new_row)
        return new_array

    @classmethod
    def from_counts(class_, row_count, column_count):
        """
        Makes pitch array from row and column counts.

        Returns pitch array.
        """
        array = class_()
        for i in range(row_count):
            row = PitchArrayRow([])
            for j in range(column_count):
                cell = PitchArrayCell()
                row.append(cell)
            array.append_row(row)
        return array

    @classmethod
    def from_score(class_, score, populate=True):
        r"""
        Makes pitch array from ``score``.

        ..  container:: example

            Makes empty pitch array from score:

            >>> score = abjad.Score(name="Score")
            >>> score.append(abjad.Staff("c'8 d'8 e'8 f'8", name="Staff_1"))
            >>> score.append(abjad.Staff("c'4 d'4", name="Staff_2"))
            >>> tuplet = abjad.Tuplet((2, 3), "c'8 d'8 e'8")
            >>> staff = abjad.Staff(
            ...     [
            ...         abjad.Tuplet((2, 3), "c'8 d'8 e'8"),
            ...         abjad.Tuplet((2, 3), "c'8 d'8 e'8"),
            ...     ],
            ...     name="Staff_3",
            ... )
            >>> score.append(staff)

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff_1"
                    {
                        c'8
                        d'8
                        e'8
                        f'8
                    }
                    \context Staff = "Staff_2"
                    {
                        c'4
                        d'4
                    }
                    \context Staff = "Staff_3"
                    {
                        \times 2/3
                        {
                            c'8
                            d'8
                            e'8
                        }
                        \times 2/3
                        {
                            c'8
                            d'8
                            e'8
                        }
                    }
                >>

            >>> abjad.show(score) # doctest: +SKIP

            >>> array = baca.array.PitchArray.from_score(score, populate=False)

            >>> print(array)
            [     ] [     ] [     ] [     ]
            [     ] [     ]
            [ ] [     ] [ ] [ ] [     ] [ ]

        ..  container:: example

            Makes populated pitch array from ``score``:

            >>> score = abjad.Score(name="Score")
            >>> score.append(abjad.Staff("c'8 d'8 e'8 f'8", name="Staff_1"))
            >>> score.append(abjad.Staff("c'4 d'4", name="Staff_2"))
            >>> staff = abjad.Staff(
            ...     [
            ...         abjad.Tuplet((2, 3), "c'8 d'8 e'8"),
            ...         abjad.Tuplet((2, 3), "c'8 d'8 e'8"),
            ...     ],
            ...     name="Staff_3",
            ... )
            >>> score.append(staff)

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \context Score = "Score"
                <<
                    \context Staff = "Staff_1"
                    {
                        c'8
                        d'8
                        e'8
                        f'8
                    }
                    \context Staff = "Staff_2"
                    {
                        c'4
                        d'4
                    }
                    \context Staff = "Staff_3"
                    {
                        \times 2/3
                        {
                            c'8
                            d'8
                            e'8
                        }
                        \times 2/3
                        {
                            c'8
                            d'8
                            e'8
                        }
                    }
                >>

            >>> abjad.show(score) # doctest: +SKIP

            >>> array = baca.array.PitchArray.from_score(score, populate=True)

            >>> print(array)
            [c'     ] [d'     ] [e'     ] [f'     ]
            [c'     ] [d'     ]
            [c'] [d'     ] [e'] [c'] [d'     ] [e']

        Returns pitch array.
        """
        offsets = _get_leaf_offsets(score)
        array_width = len(offsets)
        array_depth = len(score)
        pitch_array = class_.from_counts(array_depth, array_width)
        items = _make_multiplied_quarter_notes(offsets)
        for leaf_iterable, pitch_array_row in zip(score, pitch_array.rows):
            durations = []
            leaves = abjad.iterate.leaves(leaf_iterable)
            for leaf in leaves:
                durations.append(abjad.get.duration(leaf))
            parts = abjad.mutate.split(items, durations, cyclic=False)
            part_lengths = [len(part) for part in parts]
            cells = pitch_array_row.cells
            grouped_cells = abjad.sequence.partition_by_counts(
                cells, part_lengths, cyclic=False, overhang=False
            )
            for group in grouped_cells:
                pitch_array_row.merge(group)
            leaves = abjad.iterate.leaves(leaf_iterable)
            if populate:
                for cell, leaf in zip(pitch_array_row.cells, leaves):
                    cell.pitches.extend(abjad.iterate.pitches(leaf))
        return pitch_array

    def has_spanning_cell_over_index(self, index) -> bool:
        """
        Is true when pitch array has one or more spanning cells over ``index``.
        """
        rows = self.rows
        return any(row.has_spanning_cell_over_index(index) for row in rows)

    def list_nonspanning_subarrays(self):
        """
        Lists nonspanning subarrays of pitch array.

        ..  container:: example

            Lists three nonspanning subarrays:

            >>> array = baca.array.PitchArray([
            ...     [2, 2, 3, 1],
            ...     [1, 2, 1, 1, 2, 1],
            ...     [1, 1, 1, 1, 1, 1, 1, 1],
            ... ])

            >>> print(array)
            [     ] [     ] [     ] [ ]
            [ ] [     ] [ ] [ ] [     ] [ ]
            [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]

            >>> subarrays = array.list_nonspanning_subarrays()
            >>> len(subarrays)
            3

            >>> print(subarrays[0])
            [     ] [     ]
            [ ] [     ] [ ]
            [ ] [ ] [ ] [ ]

            >>> print(subarrays[1])
            [     ]
            [ ] [     ]
            [ ] [ ] [ ]

            >>> print(subarrays[2])
            [ ]
            [ ]
            [ ]

        Returns list.
        """
        unspanned_indices = []
        for i in range(self.width + 1):
            if not self.has_spanning_cell_over_index(i):
                unspanned_indices.append(i)
        array_depth = self.depth
        subarrays = []
        pairs = abjad.sequence.nwise(unspanned_indices)
        for start_column, stop_column in pairs:
            upper_left_pair = (0, start_column)
            lower_right_pair = (array_depth, stop_column)
            subarray = self.copy_subarray(upper_left_pair, lower_right_pair)
            subarrays.append(subarray)
        return subarrays

    def pad_to_depth(self, depth):
        """
        Pads pitch array to ``depth``.

        Returns none.
        """
        self_depth = self.depth
        if depth < self_depth:
            raise Exception("pad depth must be not less than array depth.")
        self_width = self.width
        missing_rows = depth - self_depth
        for i in range(missing_rows):
            row = PitchArrayRow([])
            row.pad_to_width(self_width)
            self.append_row(row)

    def pad_to_width(self, width):
        """
        Pads pitch array to ``width``.

        Returns none.
        """
        self_width = self.width
        if width < self_width:
            raise Exception("pad width must not be less than array width.")
        for row in self.rows:
            row.pad_to_width(width)

    def pop_column(self, column_index):
        """
        Pops column ``column_index`` from pitch array.

        Returns pitch array column.
        """
        column = self.columns[column_index]
        column._parent_array = None
        for cell in column.cells:
            cell.withdraw()
        return column

    def pop_row(self, row_index=-1):
        """
        Pops row ``row_index`` from pitch array.

        Returns pitch array row.
        """
        row = self._rows.pop(row_index)
        row._parent_array = None
        return row

    def remove_row(self, row):
        """
        Removes ``row`` from pitch array.

        Returns none.
        """
        if row not in self.rows:
            raise Exception("row not in array.")
        self._rows.remove(row)
        row._parent_array = None

    def to_measures(self, cell_duration_denominator=8) -> typing.List[abjad.Container]:
        r"""
        Changes pitch array  to measures.

        Makes time signatures with numerators equal to row width and denominators equal
        to ``cell_duration_denominator`` for each row in pitch array.

        ..  container:: example

            Changes two-by-three pitch array to measures:

            >>> array = baca.array.PitchArray([
            ...     [1, (2, 1), ([-2, -1.5], 2)],
            ...     [(7, 2), (6, 1), 1],
            ... ])

            >>> print(array)
            [  ] [d'] [bf bqf    ]
            [g'     ] [fs'   ] [ ]

            >>> measures = array.to_measures()
            >>> staff = abjad.Staff(measures)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    {
                        \time 4/8
                        r8
                        d'8
                        <bf bqf>4
                    }
                    {
                        \time 4/8
                        g'4
                        fs'8
                        r8
                    }
                }

        """
        containers = []
        for row in self.rows:
            container = row.to_measure(cell_duration_denominator)
            containers.append(container)
        return containers


class PitchArrayCell:
    """
    Pitch array cell.

    ..  container:: example

        A pitch array cell:

        >>> array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])
        >>> print(array)
        [ ] [     ] [ ]
        [     ] [ ] [ ]

        >>> cell = array[0][1]

        >>> cell
        PitchArrayCell(width=2)

        >>> cell.column_indices
        (1, 2)

        >>> cell.indices
        (0, (1, 2))

        >>> cell.is_first_in_row
        False

        >>> cell.is_final_in_row
        False

        >>> cell.next
        PitchArrayCell(width=1)

        >>> cell.parent_array
        PitchArray(rows=(PitchArrayRow(cells=(PitchArrayCell(width=1), PitchArrayCell(width=2), PitchArrayCell(width=1))), PitchArrayRow(cells=(PitchArrayCell(width=2), PitchArrayCell(width=1), PitchArrayCell(width=1)))))

        >>> cell.parent_column
        PitchArrayColumn(cells=(PitchArrayCell(width=2), PitchArrayCell(width=2)))

        >>> cell.parent_row
        PitchArrayRow(cells=(PitchArrayCell(width=1), PitchArrayCell(width=2), PitchArrayCell(width=1)))

        >>> cell.pitches is None
        True

        >>> cell.previous
        PitchArrayCell(width=1)

        >>> cell.row_index
        0

        >>> cell.item
        2

        >>> cell.width
        2

    ..  container:: example

        Initializes empty:

        >>> baca.array.PitchArrayCell()
        PitchArrayCell(width=1)

        Initializes with width:

        >>> baca.array.PitchArrayCell(width=2)
        PitchArrayCell(width=2)

        Initializes with pitch:

        >>> baca.array.PitchArrayCell(pitches=[abjad.NamedPitch(0)])
        PitchArrayCell(pitches="c'", width=1)

        Initializes with pitch numbers:

        >>> baca.array.PitchArrayCell(pitches=[0, 2, 4])
        PitchArrayCell(pitches="c' d' e'", width=1)

        Initializes with pitches:

        >>> pitches = [abjad.NamedPitch(_) for _ in [0, 2, 4]]
        >>> baca.array.PitchArrayCell(pitches)
        PitchArrayCell(pitches="c' d' e'", width=1)

        Initializes with pitch number and width:

        >>> baca.array.PitchArrayCell(pitches=0, width=2)
        PitchArrayCell(pitches="c'", width=2)

        Initializes with pitch and width:

        >>> baca.array.PitchArrayCell(pitches=[abjad.NamedPitch(0)], width=2)
        PitchArrayCell(pitches="c'", width=2)

        Initializes with pitch numbers and width:

        >>> baca.array.PitchArrayCell(pitches=[0, 2, 4], width=2)
        PitchArrayCell(pitches="c' d' e'", width=2)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_parent_row", "_pitches", "_row_parent", "_width")

    ### INTIALIZER ###

    def __init__(self, pitches=None, *, width=1):
        self._pitches = None
        if pitches is not None:
            if isinstance(pitches, str):
                pitches = pitches.split()
            elif isinstance(pitches, numbers.Number):
                pitches = [pitches]
            elif isinstance(pitches, tuple):
                assert len(pitches) == 2
                assert width == 1
                if isinstance(pitches[0], str):
                    assert isinstance(pitches[1], int)
                    pitch = abjad.NamedPitch(pitches)
                    pitches = [pitch]
                elif isinstance(pitches[0], tuple):
                    assert len(pitches[0]) == 2
                    assert isinstance(pitches[0][0], str)
                    assert isinstance(pitches[0][1], int)
                    assert isinstance(pitches[1], int)
                    width = pitches[1]
                    pitch = abjad.NamedPitch(pitches[0])
                    pitches = [pitch]
                else:
                    raise Exception
            # assert isinstance(pitches, (tuple, list)), repr(pitches)
            assert isinstance(pitches, list), repr(pitches)
            pitches = [abjad.NamedPitch(_) for _ in pitches]
            self._pitches = pitches
        assert isinstance(width, int), repr(width)
        assert 1 <= width, repr(width)
        self._width = width
        self._parent_row = None

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation of pitch array cell.
        """
        if self.pitches:
            pitches = " ".join([str(_) for _ in self.pitches or []])
            return f'PitchArrayCell(pitches="{pitches}", width={self.width})'
        else:
            return f"PitchArrayCell(width={self.width})"

    def __str__(self):
        """
        Gets string representation of pitch array cell.

        Returns string.
        """
        return self._format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _composite_column_width(self):
        composite_column_width = 0
        columns = self.parent_array.columns
        for column_index in self.column_indices:
            composite_column_width += columns[column_index]._column_format_width
        return composite_column_width

    @property
    def _conditional_pitch_string(self):
        if self.pitches:
            return self._pitch_string
        else:
            return " "

    @property
    def _format_pitch_width_string(self):
        if self.pitches:
            if self.width == 1:
                return self._pitch_string
            else:
                return f"{self._pitch_string} {self._width_string}"
        else:
            return self._width_string

    @property
    def _format_row_column_repr_string(self):
        return self._format_pitch_width_string

    @property
    def _format_string(self):
        if self.parent_column is not None:
            if self._is_final_cell_in_row:
                cell_width = self._composite_column_width - 2
            else:
                cell_width = self._composite_column_width - 3
            return f"[{self._conditional_pitch_string.ljust(cell_width)}]"
        else:
            return f"[{self._conditional_pitch_string}]"

    @property
    def _is_final_cell_in_row(self):
        if self.parent_row is not None:
            if self.column_indices[-1] == (self.parent_row.width - 1):
                return True
            return False
        return True

    @property
    def _pitch_string(self):
        if self.pitches:
            return " ".join([str(pitch) for pitch in self.pitches])
        else:
            return ""

    @property
    def _width_string(self):
        return f"x{self.width}"

    ### PRIVATE METHODS ###

    def _parse_cell_token(self, cell_token):
        if cell_token is None:
            pitches, width = [], 1
        elif isinstance(cell_token, int):
            if 0 < cell_token:
                pitches, width = [], cell_token
            else:
                raise Exception("integer width item must be positive.")
        elif isinstance(cell_token, abjad.NamedPitch):
            pitches, width = [cell_token], 1
        elif isinstance(cell_token, list):
            pitch_token, width = cell_token, 1
            pitches = self._parse_pitch_token(pitch_token)
        elif isinstance(cell_token, tuple):
            if not len(cell_token) == 2:
                raise Exception("tuple item must be of length two.")
            if isinstance(cell_token[0], str):
                pitches = self._parse_pitch_token(cell_token)
                width = 1
            else:
                pitch_token, width = cell_token
                pitches = self._parse_pitch_token(pitch_token)
        elif isinstance(cell_token, type(self)):
            pitches, width = cell_token.pitches, cell_token.width
        else:
            raise Exception("cell item must be integer width, pitch or pair.")
        return pitches, width

    def _parse_pitch_token(self, pitch_token):
        pitches = []
        if isinstance(pitch_token, (int, float, abjad.NamedPitch)):
            pitch = abjad.NamedPitch(pitch_token)
            pitches.append(pitch)
        elif isinstance(pitch_token, tuple):
            pitches.append(abjad.NamedPitch(*pitch_token))
        elif isinstance(pitch_token, list):
            for element in pitch_token:
                pitch = abjad.NamedPitch(element)
                pitches.append(pitch)
        else:
            raise Exception("pitch item must be number, pitch or list.")
        return pitches

    def _withdraw(self):
        parent_row = self.parent_row
        parent_row.remove(self)
        return self

    ### PUBLIC PROPERTIES ###

    @property
    def column_indices(self):
        """
        Gets column start and stop indices.

        ..  container:: example

            Gets column start and stop indices of cell in array:

            >>> array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])
            >>> cell = array[0][1]
            >>> cell.column_indices
            (1, 2)

        ..  container:: example

            Gets column start and stop indices of cell outside array:

            >>> cell = baca.array.PitchArrayCell()
            >>> cell.column_indices is None
            True

        Returns tuple or none.
        """
        if self.parent_row is not None:
            if self.width == 1:
                return (self.column_start_index,)
            elif 1 < self.width:
                return self.column_start_index, self.column_stop_index

    @property
    def column_start_index(self):
        """
        Gets column start index.

        ..  container:: example

            Gets column start index of cell in array:

            >>> array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])
            >>> cell = array[0][1]
            >>> cell.column_start_index
            1

        ..  container:: example

            Gets column start index of cell outside array:

            >>> cell = baca.array.PitchArrayCell()
            >>> cell.column_start_index is None
            True

        Returns nonnegative integer or none.
        """
        if self.parent_row is None:
            return
        start_index = 0
        for cell in self.parent_row.cells:
            if cell is self:
                return start_index
            start_index += cell.width

    @property
    def column_stop_index(self):
        """
        Gets column stop index.

        ..  container:: example

            Gets column stop index of cell in array:

            >>> array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])
            >>> cell = array[0][1]
            >>> cell.column_stop_index
            2

        ..  container:: example

            Gets column stop index of cell outside array:

            >>> cell = baca.array.PitchArrayCell()
            >>> cell.column_stop_index is None
            True

        Returns nonnegative integer or none.
        """
        if self.parent_row is not None:
            return self.column_start_index + self.width - 1

    @property
    def indices(self):
        """
        Gets indices.

        ..  container:: example

            >>> array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])

            >>> print(array)
            [ ] [     ] [ ]
            [     ] [ ] [ ]

            >>> for row in array:
            ...     for cell in row:
            ...         cell.indices
            ...
            (0, (0,))
            (0, (1, 2))
            (0, (3,))
            (1, (0, 1))
            (1, (2,))
            (1, (3,))

        Returns pair.
        """
        return self.row_index, self.column_indices

    @property
    def is_final_in_row(self):
        """
        Is true when pitch array cell is last in row.

        ..  container:: example

            >>> array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])

            >>> print(array)
            [ ] [     ] [ ]
            [     ] [ ] [ ]

            >>> for row in array:
            ...     for cell in row:
            ...         cell, cell.is_final_in_row
            ...
            (PitchArrayCell(width=1), False)
            (PitchArrayCell(width=2), False)
            (PitchArrayCell(width=1), True)
            (PitchArrayCell(width=2), False)
            (PitchArrayCell(width=1), False)
            (PitchArrayCell(width=1), True)

        Returns true or false.
        """
        if self.parent_row is not None:
            if self.column_indices[-1] == self.parent_row.width - 1:
                return True
        return False

    @property
    def is_first_in_row(self):
        """
        Is true when pitch array cell is first in row.

        ..  container:: example

            >>> array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])

            >>> print(array)
            [ ] [     ] [ ]
            [     ] [ ] [ ]

            >>> for row in array:
            ...     for cell in row:
            ...         cell, cell.is_first_in_row
            ...
            (PitchArrayCell(width=1), True)
            (PitchArrayCell(width=2), False)
            (PitchArrayCell(width=1), False)
            (PitchArrayCell(width=2), True)
            (PitchArrayCell(width=1), False)
            (PitchArrayCell(width=1), False)

        Returns true or false.
        """
        if self.parent_row is not None:
            if self.column_indices[0] == 0:
                return True
        return False

    @property
    def item(self):
        """
        Gets item.

        ..  container:: example

            >>> baca.array.PitchArrayCell(width=1).item
            1

            >>> baca.array.PitchArrayCell(width=2).item
            2

            >>> baca.array.PitchArrayCell("c'").item
            ('c', 4)

            >>> baca.array.PitchArrayCell("c'", width=2).item
            (('c', 4), 2)

            >>> baca.array.PitchArrayCell("c' d'").item
            [('c', 4), ('d', 4)]

            >>> baca.array.PitchArrayCell("c' d'", width=2).item
            ([('c', 4), ('d', 4)], 2)

        """
        if not self.pitches:
            return self.width
        elif len(self.pitches) == 1:
            if self.width == 1:
                return (
                    str(self.pitches[0].pitch_class),
                    self.pitches[0].octave.number,
                )
            else:
                return (
                    (str(self.pitches[0].pitch_class), self.pitches[0].octave.number),
                    self.width,
                )
        else:
            if self.width == 1:
                return [
                    (str(pitch.pitch_class), pitch.octave.number)
                    for pitch in self.pitches
                ]
            else:
                return (
                    [
                        (str(pitch.pitch_class), pitch.octave.number)
                        for pitch in self.pitches
                    ],
                    self.width,
                )

    @property
    def next(self):
        """
        Gets next pitch array cell in row after this pitch array cell.

        ..  container:: example

            >>> array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])

            >>> print(array)
            [ ] [     ] [ ]
            [     ] [ ] [ ]

            >>> for row in array:
            ...     for cell in row.cells[:-1]:
            ...         cell, cell.next
            ...
            (PitchArrayCell(width=1), PitchArrayCell(width=2))
            (PitchArrayCell(width=2), PitchArrayCell(width=1))
            (PitchArrayCell(width=2), PitchArrayCell(width=1))
            (PitchArrayCell(width=1), PitchArrayCell(width=1))

        Returns pitch array cell.
        """
        if self.parent_row is not None:
            if self.is_final_in_row:
                raise Exception("cell is last in row.")
            return self.parent_row[self.column_indices[-1] + 1]
        raise Exception("cell has no parent row.")

    @property
    def parent_array(self):
        """
        Gets parent array.

        Return pitch array.
        """
        parent_row = self.parent_row
        if parent_row is not None:
            return parent_row.parent_array
        return None

    @property
    def parent_column(self):
        """
        Gets parent column.

        Returns pitch array column.
        """
        parent_array = self.parent_array
        if parent_array is not None:
            start_column_index = self.column_indices[0]
            return parent_array.columns[start_column_index]
        return None

    @property
    def parent_row(self):
        """
        Gets parent row.

        Returns pitch array row.
        """
        return self._parent_row

    @property
    def pitches(self):
        """
        Gets and sets pitches of pitch array cell.

        Returns list.
        """
        return self._pitches

    @pitches.setter
    def pitches(self, pitches):
        if pitches is None:
            self._pitches = None
            return
        if isinstance(pitches, str):
            pitches = pitches.split()
        assert isinstance(pitches, (tuple, list)), repr(pitches)
        pitches = [abjad.NamedPitch(_) for _ in pitches]
        self._pitches = pitches

    @property
    def previous(self):
        """
        Gets pitch array cell in row prior to this pitch array cell.

        ..  container:: example

            >>> array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])

            >>> print(array)
            [ ] [     ] [ ]
            [     ] [ ] [ ]

            >>> for row in array:
            ...     for cell in row.cells[1:]:
            ...         cell, cell.previous
            ...
            (PitchArrayCell(width=2), PitchArrayCell(width=1))
            (PitchArrayCell(width=1), PitchArrayCell(width=2))
            (PitchArrayCell(width=1), PitchArrayCell(width=2))
            (PitchArrayCell(width=1), PitchArrayCell(width=1))

        Returns pitch array cell.
        """
        if self.parent_row is not None:
            if self.is_first_in_row:
                raise Exception("cell is first in row.")
            return self.parent_row[self.column_indices[0] - 1]
        raise Exception("cell has no parent row.")

    @property
    def row_index(self):
        """
        Gets row index.

        Returns nonnegative integer or none.
        """
        parent_row = self.parent_row
        if parent_row is not None:
            return parent_row.row_index
        return None

    @property
    def weight(self):
        """
        Gets weight.

        Weight defined equal to number of pitches in cell.

        Returns nonnegative integer.
        """
        return len(self.pitches or [])

    @property
    def width(self):
        """
        Gets width.

        Width defined equal to number of columns spanned by cell.

        Returns positive integer.
        """
        return self._width

    ### PUBLIC METHODS ###

    def append_pitch(self, pitch):
        """
        Appends ``pitch`` to cell.

        Returns none.
        """
        if self.pitches is None:
            self._pitches = []
        pitch = abjad.NamedPitch(pitch)
        self._pitches.append(pitch)

    def matches_cell(self, argument):
        """
        Is true when pitch array cell matches ``argument``.

        ..  container:: example

            >>> array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])
            >>> array[0].cells[0].append_pitch(0)
            >>> array[0].cells[1].append_pitch(2)
            >>> array[0].cells[1].append_pitch(4)

            >>> print(array)
            [c'] [d' e'    ] [ ]
            [          ] [ ] [ ]

            >>> array[0].cells[0].matches_cell(array[0].cells[0])
            True

            >>> array[0].cells[0].matches_cell(array[0].cells[1])
            False

        Returns true or false.
        """
        if isinstance(argument, type(self)):
            if self.pitches == argument.pitches:
                if self.width == argument.width:
                    return True
        return False


class PitchArrayColumn:
    """
    Pitch array column.

    ..  container:: example

        A pitch array column:

        >>> array = baca.array.PitchArray([
        ...     [1, (2, 1), (-1.5, 2)],
        ...     [(7, 2), (6, 1), 1],
        ... ])

        >>> print(array)
        [  ] [d'] [bqf    ]
        [g'     ] [fs'] [ ]

        >>> array.columns[0]
        PitchArrayColumn(cells=(PitchArrayCell(width=1), PitchArrayCell(pitches="g'", width=2)))

        >>> print(array.columns[0])
        [  ]
        [g'     ]

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_cells", "_column_index", "_parent_array")

    ### INITIALIZER ###

    def __init__(self, cells=None):
        self._cells = []
        self._column_index = None
        self._parent_array = None
        cells = cells or []
        self.extend(cells)

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a pitch array column with pitch array cells equal to
        those of this pitch array column.

        Returns true or false.
        """
        if isinstance(argument, PitchArrayColumn):
            for self_cell, arg_cell in zip(self.cells, argument.cells):
                if not self_cell == arg_cell:
                    return False
            return True
        return False

    def __getitem__(self, argument):
        """
        Gets cell or cell slice identified by ``argument``.

        Returns pitch array cell or slice or pitch array cells.
        """
        return self.cells.__getitem__(argument)

    def __hash__(self):
        """
        Hashes pitch array column.

        Returns integer.
        """
        return super().__hash__()

    def __ne__(self, argument):
        """
        Is true when pitch array column does not equal ``argument``.

        Returns true or false.
        """
        return not self == argument

    def __repr__(self):
        """
        Gets repr.
        """
        return f"{type(self).__name__}(cells={self.cells})"

    def __str__(self):
        """
        Gets string representation of pitch array column.

        Returns string.
        """
        result = [str(cell) for cell in self.cells]
        result = "\n".join(result)
        return result

    ### PRIVATE METHODS ###

    def _cells_starting_at_index(self, index):
        result = []
        for cell in self.cells:
            if cell.column_indices[0] == index:
                result.append(cell)
        result = tuple(result)
        return result

    ### PUBLIC METHODS ###

    def append(self, cell):
        """
        Appends ``cell`` to pitch array column.

        Returns none.
        """
        if not isinstance(cell, PitchArrayCell):
            raise Exception("must be cell.")
        cell._row_parent = self
        self._cells.append(cell)

    def extend(self, cells):
        """
        Extends ``cells`` against pitch array column.

        Returns none.
        """
        if not all(isinstance(cell, PitchArrayCell) for cell in cells):
            raise Exception("must be cells.")
        for cell in cells:
            self.append(cell)

    def remove_pitches(self):
        r"""
        Removes pitches from pitch array cells in pitch array column.

        Returns none.
        """
        for cell in self.cells:
            cell.pitch = None

    ### PRIVATE PROPERTIES ###

    @property
    def _column_format_max_string_width(self):
        strings = self._start_cell_conditional_pitch_strings
        if strings:
            return max([len(string) for string in strings])
        else:
            return 0

    @property
    def _column_format_width(self):
        format_width = 0
        if self._has_closed_cell_on_left:
            format_width += 1
        max_string_width = self._column_format_max_string_width
        format_width += max_string_width
        if self._has_closed_cell_on_right:
            format_width += 1
        if not self._is_final_column_in_array:
            format_width += 1
        return format_width

    @property
    def _format_contents_string(self):
        result = []
        for cell in self.cells:
            result.append(cell._format_row_column_repr_string)
        result = ", ".join(result)
        return result

    @property
    def _has_closed_cell_on_left(self):
        if self.column_index is not None:
            for cell in self.cells:
                if cell.column_indices[0] == self.column_index:
                    return True
            return False
        return True

    @property
    def _has_closed_cell_on_right(self):
        if self.column_index is not None:
            for cell in self.cells:
                if cell.column_indices[-1] == self.column_index:
                    return True
            return True
        return True

    @property
    def _is_final_column_in_array(self):
        if self.parent_array is not None:
            if self.column_index == (self.parent_array.width - 1):
                return True
        return False

    @property
    def _start_cell_conditional_pitch_strings(self):
        result = [cell._conditional_pitch_string for cell in self._start_cells]
        result = tuple(result)
        return result

    @property
    def _start_cells(self):
        column_index = self.column_index
        return self._cells_starting_at_index(column_index)

    ### PUBLIC PROPERTIES ###

    @property
    def cell_tokens(self):
        """
        Gets cells items of pitch array column.

        Returns tuple.
        """
        return tuple([cell.item for cell in self.cells])

    @property
    def cell_widths(self):
        """
        Gets cell widths of pitch array column.

        Returns tuple.
        """
        return tuple([cell.width for cell in self.cells])

    @property
    def cells(self):
        """
        Gets cells of pitch array column.

        Returns tuple.
        """
        return tuple(self._cells)

    @property
    def column_index(self):
        """
        Gets column index of pitch array column.

        Returns nonnegative integer.
        """
        return self._column_index

    @property
    def depth(self):
        """
        Gets depth of pitch array column.

        Defined equal to number of pitch array cells in pitch array column.

        Returns nonnegative integer.
        """
        return len(self.cells)

    @property
    def dimensions(self):
        """
        Gets dimensions of pitch array column.

        Returns pair.
        """
        return self.depth, self.width

    @property
    def has_voice_crossing(self):
        """
        Is true when pitch array column has voice crossing.

        ..  container:: example

            >>> array = baca.array.PitchArray([
            ...     [1, (2, 1), (-1.5, 2)],
            ...     [(7, 2), (6, 1), 1],
            ... ])

            >>> print(array)
            [  ] [d'] [bqf    ]
            [g'     ] [fs'] [ ]

            >>> for column in array.columns:
            ...     column.has_voice_crossing
            ...
            False
            True
            True
            False

        Returns true or false.
        """
        for upper, lower in abjad.sequence.nwise(self.cells):
            lower_pitches = lower.pitches or ()
            for lower_pitch in lower_pitches:
                upper_pitches = upper.pitches or ()
                for upper_pitch in upper_pitches:
                    if upper_pitch < lower_pitch:
                        return True
        return False

    @property
    def is_defective(self):
        """
        Is true when pitch array column depth does not equal depth of parent array.

        Returns true or false.
        """
        if self.parent_array is not None:
            return not self.depth == self.parent_array.depth

    @property
    def parent_array(self):
        """
        Gets parent array that houses pitch array column.

        Returns pitch array.
        """
        return self._parent_array

    @property
    def pitches(self):
        """
        Gets pitches in pitch array column.

        Returns tuple.
        """
        pitches = []
        for cell in self.cells:
            pitches.extend(cell.pitches or [])
        return tuple(pitches)

    @property
    def start_cells(self):
        """
        Gets start cells in pitch array column.

        ..  container:: example

            >>> array = baca.array.PitchArray([
            ...     [1, (2, 1), ([-2, -1.5], 2)],
            ...     [(7, 2), (6, 1), 1],
            ... ])

            >>> print(array)
            [  ] [d'] [bf bqf    ]
            [g'     ] [fs'   ] [ ]

            >>> for column in array.columns:
            ...     column.start_cells
            ...
            [PitchArrayCell(width=1), PitchArrayCell(pitches="g'", width=2)]
            [PitchArrayCell(pitches="d'", width=1)]
            [PitchArrayCell(pitches="bf bqf", width=2), PitchArrayCell(pitches="fs'", width=1)]
            [PitchArrayCell(width=1)]

        Returns list.
        """
        start_cells = []
        column_index = self.column_index
        for cell in self.cells:
            if cell.column_indices[0] == column_index:
                start_cells.append(cell)
        return list(start_cells)

    @property
    def start_pitches(self):
        """
        Gets start pitches in pitch array column.

        ..  container:: example

            >>> array = baca.array.PitchArray([
            ...     [1, (2, 1), ([-2, -1.5], 2)],
            ...     [(7, 2), (6, 1), 1],
            ... ])

            >>> for column in array.columns:
            ...     column.start_pitches
            ...
            [NamedPitch("g'")]
            [NamedPitch("d'")]
            [NamedPitch('bf'), NamedPitch('bqf'), NamedPitch("fs'")]
            []

        Returns list.
        """
        start_pitches = []
        for cell in self.start_cells:
            if cell.pitches is not None:
                start_pitches.extend(cell.pitches)
        return list(start_pitches)

    @property
    def stop_cells(self):
        """
        Gets stop cells in pitch array column.

        Returns tuple.
        """
        start_cells = []
        column_index = self.column_index
        for cell in self.cells:
            if cell.column_indices[-1] == column_index:
                start_cells.append(cell)
        return tuple(start_cells)

    @property
    def stop_pitches(self):
        """
        Gets stop pitches in pitch array column.

        Returns tuple.
        """
        stop_pitches = []
        for cell in self.stop_cells:
            stop_pitches.extend(cell.pitches or [])
        return tuple(stop_pitches)

    @property
    def weight(self):
        """
        Gets weight of pitch array column.

        Defined equal to the sum of the weight of pitch array cells in pitch array
        column.

        Returns nonnegative integer.
        """
        return sum([cell.weight for cell in self.cells])

    @property
    def width(self):
        """
        Gets width of pitch array column.

        Defined equal to 1 when pitch array column contains cells.

        Defined equal to 0 when pitch array column contains no cells.

        Returns 1 or 0.
        """
        if 1 <= len(self.cells):
            return 1
        else:
            return 0


class PitchArrayRow:
    """
    Pitch array row.

    ..  container:: example

        A pitch array row:

        >>> array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])
        >>> array[0].cells[0].append_pitch(0)
        >>> array[0].cells[1].append_pitch(2)
        >>> array[1].cells[2].append_pitch(4)
        >>> print(array)
        [c'] [d'    ] [  ]
        [       ] [ ] [e']

        >>> array[0]
        PitchArrayRow(cells=(PitchArrayCell(pitches="c'", width=1), PitchArrayCell(pitches="d'", width=2), PitchArrayCell(width=1)))

        >>> array[0].cell_widths
        (1, 2, 1)

        >>> array[0].dimensions
        (1, 4)

        >>> array[0].pitches
        (NamedPitch("c'"), NamedPitch("d'"))

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_cells", "_parent_array", "_pitch_range", "name")

    ### INITIALIZER ###

    def __init__(self, cells=None):
        self._parent_array = None
        self._pitch_range = abjad.PitchRange()
        self._cells = []
        cells = cells or []
        self.extend(cells)
        self.name = None

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        """
        Concatenates ``argument`` to pitch array row.

        ..  container:: example

            >>> array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])
            >>> array[0].cells[0].append_pitch(0)
            >>> array[0].cells[1].append_pitch(2)
            >>> array[1].cells[2].append_pitch(4)

            >>> print(array)
            [c'] [d'    ] [  ]
            [       ] [ ] [e']

            >>> new_row = array[0] + array[1]

            >>> print(new_row)
            [c'] [d'] [ ] [ ] [ ] [e']

        Returns new pitch array row.
        """
        if not isinstance(argument, PitchArrayRow):
            message = "must be pitch array row."
            raise Exception(message)
        self_copy = copy.copy(self)
        arg_copy = copy.copy(argument)
        new_row = PitchArrayRow([])
        new_row.extend(self_copy.cells)
        new_row.extend(arg_copy.cells)
        return new_row

    def __copy__(self):
        """
        Copies pitch array row.

        Returns new pitch array row.
        """
        new_cells = []
        for cell in self.cells:
            new_cell = copy.copy(cell)
            new_cells.append(new_cell)
        return PitchArrayRow(new_cells)

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a pitch array row with contents equal to that of
        this pitch array row.

        Returns true or false.
        """
        if isinstance(argument, PitchArrayRow):
            for self_cell, arg_cell in zip(self.cells, argument.cells):
                if not self_cell.matches_cell(arg_cell):
                    return False
                return True
        return False

    def __getitem__(self, argument):
        """
        Gets cell or cell slice identified by ``argument``.

        Returns pitch array cell or slice of pitch array cells.
        """
        if isinstance(argument, int):
            if 0 <= argument < self.width:
                accumulated_width = 0
                for cell in self.cells:
                    total_width = accumulated_width + cell.width
                    if accumulated_width <= argument < total_width:
                        return cell
                    accumulated_width = total_width
            elif 0 < abs(argument) < self.width:
                accumulated_width = 0
                abs_arg = abs(argument)
                for cell in reversed(self.cells):
                    total_width = accumulated_width + cell.width
                    if accumulated_width < abs_arg <= total_width:
                        return cell
                    accumulated_width = total_width
            else:
                raise Exception("no such cell in row.")
        elif isinstance(argument, slice):
            cells = []
            start, stop, step = argument.indices(self.width)
            for cell_index in range(start, stop, step):
                cell = self[cell_index]
                if len(cells) == 0:
                    cells.append(cell)
                else:
                    if cells[-1] is not cell:
                        cells.append(cell)
            cells = tuple(cells)
            return cells
        else:
            raise Exception("must be int or slice.")

    def __hash__(self):
        """
        Hashes pitch array row.

        Returns integer.
        """
        return super().__hash__()

    def __iadd__(self, argument):
        """
        Adds ``argument`` to pitch array row in place.

        ..  container:: example

            >>> array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])
            >>> array[0].cells[0].append_pitch(0)
            >>> array[0].cells[1].append_pitch(2)
            >>> array[1].cells[2].append_pitch(4)

            >>> print(array)
            [c'] [d'    ] [  ]
            [       ] [ ] [e']

            >>> row = array[0].withdraw()
            >>> row += row

            >>> print(row)
            [c'] [d'] [ ] [c'] [d'] [ ]

        Returns pitch array row.
        """
        if not isinstance(argument, PitchArrayRow):
            raise Exception("must be pitch array row.")
        copy_arg = copy.copy(argument)
        self.extend(copy_arg.cells)
        return self

    def __iter__(self):
        """
        Iterates pitch array row.

        Returns generator.
        """
        return iter(self.cells)

    def __len__(self):
        """
        Gets length of pitch array row.

        Length defined equal to the width of pitch array row.

        Returns nonnegative integer.
        """
        return self.width

    def __ne__(self, argument):
        """
        Is true when pitch array row does not equal ``argument``.

        Returns true or false.
        """
        return not self == argument

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}(cells={self.cells})"

    def __str__(self):
        """
        Gets string representation of pitch array row.

        Returns string.
        """
        result = [str(cell) for cell in self.cells]
        result = " ".join(result)
        return result

    ### PRIVATE PROPERTIES ###

    @property
    def _compact_summary(self):
        len_self = len(self.cells)
        if not len_self:
            return ""
        elif 0 < len_self <= 8:
            result = [cell._format_row_column_repr_string for cell in self.cells]
            return ", ".join(result)
        else:
            left = ", ".join([_._format_row_column_repr_string for _ in self.cells[:2]])
            right = ", ".join(
                [_._format_row_column_repr_string for _ in self.cells[-2:]]
            )
            number_in_middle = len_self - 4
            middle = f", ... [{number_in_middle}] ..., "
            return left + middle + right

    @property
    def _format_contents_string(self):
        result = []
        for cell in self.cells:
            result.append(cell._format_row_column_repr_string)
        result = ", ".join(result)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def cell_tokens(self):
        """
        Gets cell items of pitch array row.

        Returns tuple.
        """
        return tuple([cell.item for cell in self.cells])

    @property
    def cell_widths(self):
        """
        Gets cell widths of pitch array row.

        Returns tuple.
        """
        return tuple([cell.width for cell in self.cells])

    @property
    def cells(self):
        """
        Gets cells of pitch array row.

        Returns tuple.
        """
        return tuple(self._cells)

    @property
    def depth(self):
        """
        Gets depth of pitch array row.

        Defined equal to ``1``.

        Returns ``1``.
        """
        return 1

    @property
    def dimensions(self):
        """
        Gets dimensions of pitch array row.

        Returns pair.
        """
        return self.depth, self.width

    @property
    def is_defective(self):
        """
        Is true when width of pitch array row does not equal width of parent pitch array.

        Returns true or false.
        """
        if self.parent_array is not None:
            return not self.width == self.parent_array.width
        return False

    @property
    def is_in_range(self):
        """
        Is true when all pitches in pitch array row are in pitch range of pitch array
        row.

        Returns true or false.
        """
        return all(pitch in self.pitch_range for pitch in self.pitches)

    @property
    def parent_array(self):
        """
        Gets parent pitch array housing pitch array row.

        Returns pitch array or none.
        """
        return self._parent_array

    @property
    def pitch_range(self):
        """
        Gets and sets pitch range of pitch array row.

        Returns pitch range.
        """
        return self._pitch_range

    @pitch_range.setter
    def pitch_range(self, argument):
        if not isinstance(argument, abjad.PitchRange):
            raise Exception("must be pitch range.")
        self._pitch_range = argument

    @property
    def pitches(self):
        """
        Gets pitches in pitch array row.

        Returns tuple.
        """
        pitches = []
        for cell in self.cells:
            if cell.pitches is not None:
                pitches.extend(cell.pitches)
        return tuple(pitches)

    @property
    def row_index(self):
        """
        Gets row index of pitch array row in parent pitch array.

        Returns nonnegative integer.
        """
        parent_array = self.parent_array
        if parent_array is not None:
            return parent_array._rows.index(self)
        raise Exception("row has no parent array.")

    @property
    def weight(self):
        """
        Gets weight of pitch array row.

        Defined equal to sum of weights of pitch array cells in pitch array row.

        Returns nonnegative integer.
        """
        return sum([cell.weight for cell in self.cells])

    @property
    def width(self):
        """
        Gets width of pitch array row.

        Defined equal to sum of widths of pitch array cells in pitch array row.

        Returns nonnegative integer.
        """
        return sum([cell.width for cell in self.cells])

    ### PUBLIC METHODS ###

    def append(self, cell):
        """
        Appends ``cell`` to pitch array row.

        ..  container:: example

            >>> array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])
            >>> array[0].cells[0].append_pitch(abjad.NamedPitch(0))
            >>> array[0].cells[1].append_pitch(abjad.NamedPitch(2))
            >>> array[0].cells[1].append_pitch(abjad.NamedPitch(4))

            >>> print(array)
            [c'] [d' e'    ] [ ]
            [          ] [ ] [ ]

            >>> cell = baca.array.PitchArrayCell(width=1)
            >>> array[0].append(cell)
            >>> cell = baca.array.PitchArrayCell(width=1)
            >>> array[1].append(cell)

            >>> print(array)
            [c'] [d' e'    ] [ ] [ ]
            [          ] [ ] [ ] [ ]

        Returns none.
        """
        assert isinstance(cell, PitchArrayCell), repr(cell)
        cell._parent_row = self
        self._cells.append(cell)

    def apply_pitches(self, pitch_tokens):
        """
        Applies ``pitch_tokens`` to pitch cells in pitch array row.

        ..  container:: example

            >>> array = baca.array.PitchArray([
            ...     [1, (0, 1), (0, 2)],
            ...     [(0, 2), (0, 1), 1],
            ... ])

            >>> print(array)
            [  ] [c'] [c'    ]
            [c'     ] [c'] [ ]

            >>> array[0].apply_pitches([-2, -1.5])

            >>> print(array)
            [  ] [bf] [bqf    ]
            [c'     ] [c' ] [ ]

        Returns none.
        """
        pitch_tokens = list(pitch_tokens[:])
        if pitch_tokens:
            for cell in self.cells:
                if cell.pitches:
                    cell.pitches = [pitch_tokens.pop(0)]
        else:
            self.empty_pitches()

    def copy_subrow(self, start=None, stop=None):
        """
        Copies subrow of pitch array row from ``start`` to ``stop``.

        ..  container:: example

            >>> array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])
            >>> array[0].cells[0].append_pitch(0)
            >>> array[0].cells[1].append_pitch(2)
            >>> array[1].cells[2].append_pitch(4)

            >>> print(array)
            [c'] [d'    ] [  ]
            [       ] [ ] [e']

            >>> subrow = array[0].copy_subrow(2, None)

            >>> print(subrow)
            [d'] [ ]

        Returns new pitch array row.
        """
        argument = slice(start, stop)
        start, stop, step = argument.indices(self.width)
        if not step == 1:
            raise Exception("step no implemented.")
        column_indices = set(range(start, stop, step))
        row = PitchArrayRow([])
        cells = self[argument]
        new_cells = []
        for cell in cells:
            if cell not in new_cells:
                trim = [_ for _ in cell.column_indices if _ not in column_indices]
                new_width = cell.width - len(trim)
                new_cell = copy.copy(cell)
                new_cell._width = new_width
                new_cells.append(new_cell)
        row.extend(new_cells)
        return row

    def empty_pitches(self):
        """
        Empties pitches in pitch array row.

        ..  container:: example

            >>> array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])
            >>> array[0].cells[0].append_pitch(0)
            >>> array[0].cells[1].append_pitch(2)
            >>> array[1].cells[2].append_pitch(4)

            >>> print(array)
            [c'] [d'    ] [  ]
            [       ] [ ] [e']

            >>> array[0].empty_pitches()

            >>> print(array)
            [ ] [     ] [  ]
            [     ] [ ] [e']

        Returns none.
        """
        for cell in self.cells:
            cell.pitches = []

    def extend(self, cells):
        """
        Extends pitch array row with ``cells``.

        ..  container:: example

            >>> array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])
            >>> array[0].cells[0].append_pitch(0)
            >>> array[0].cells[1].append_pitch(2)
            >>> array[1].cells[2].append_pitch(4)

            >>> print(array)
            [c'] [d'    ] [  ]
            [       ] [ ] [e']

            >>> cells = [baca.array.PitchArrayCell(width=_) for _ in [1, 1, 1]]
            >>> array[0].extend(cells)
            >>> cell = baca.array.PitchArrayCell(width=3)
            >>> array[1].append(cell)

            >>> print(array)
            [c'] [d'    ] [  ] [ ] [ ] [ ]
            [       ] [ ] [e'] [     ]

        Returns none.
        """
        for cell in cells:
            self.append(cell)

    def has_spanning_cell_over_index(self, i):
        """
        Is true when pitch array row has one or more cells spanning over index ``i``.

        ..  container:: example

            >>> array = baca.array.PitchArray([[1, 2, 1], [2, 1, 1]])
            >>> array[0].cells[0].append_pitch(0)
            >>> array[0].cells[1].append_pitch(2)
            >>> array[1].cells[2].append_pitch(4)

            >>> print(array)
            [c'] [d'    ] [  ]
            [       ] [ ] [e']

            >>> for row in array:
            ...     for i in range(4):
            ...         i, row.has_spanning_cell_over_index(i)
            ...
            (0, False)
            (1, False)
            (2, True)
            (3, False)
            (0, False)
            (1, True)
            (2, False)
            (3, False)

        Returns true or false.
        """
        try:
            cell = self[i]
        except Exception:
            return False
        return cell.column_indices[0] < i

    def index(self, cell):
        """
        Gets index of pitch array ``cell`` in pitch array row.

        Retunrs nonnegative integer.
        """
        return self._cells.index(cell)

    def merge(self, cells):
        """
        Merges ``cells``.

        Returns pitch array cell.
        """
        column_indices = []
        pitches = []
        width = 0
        for cell in cells:
            assert isinstance(cell, PitchArrayCell), repr(cell)
            if cell.parent_row is not self:
                raise Exception("cells must belong to row.")
            column_indices.extend(cell.column_indices)
            if cell.pitches is not None:
                pitches.extend(cell.pitches)
            width += cell.width
        start = min(column_indices)
        stop = start + len(column_indices)
        strict_series = list(range(start, stop))
        if not column_indices == strict_series:
            raise Exception("cells must be contiguous.")
        first_cell = cells[0]
        for cell in cells[1:]:
            self.remove(cell)
        first_cell._pitches = pitches
        first_cell._width = width
        return first_cell

    def pad_to_width(self, width):
        """
        Pads pitch array row to ``width``.

        Returns none.
        """
        self_width = self.width
        if width < self_width:
            raise Exception("pad width must not be less than row width.")
        missing_width = width - self_width
        for i in range(missing_width):
            cell = PitchArrayCell()
            self.append(cell)

    def pop(self, cell_index):
        """
        Pops cell ``cell_index`` from pitch array row.

        Returns pitch array cell.
        """
        cell = self.pop(cell_index)
        cell._parent_row = None
        return cell

    def remove(self, cell):
        """
        Removes ``cell`` form pitch array row.

        Returns none.
        """
        for i, item in enumerate(self.cells):
            if item is cell:
                self._cells.pop(i)
                break
        cell._parent_row = None

    def to_measure(self, cell_duration_denominator=8) -> typing.Container:
        r"""
        Changes pitch array row to measures.

        Sets time signature numerators equal to pitch array row widths and time signature
        denominators equal to ``cell_duration_denominator``.

        ..  container:: example

            Changes row to measure:

            >>> array = baca.array.PitchArray([
            ...     [1, (2, 1), ([-2, -1.5], 2)],
            ...     [(7, 2), (6, 1), 1],
            ... ])

            >>> print(array)
            [  ] [d'] [bf bqf    ]
            [g'     ] [fs'   ] [ ]

            >>> measure = array.rows[0].to_measure()
            >>> staff = abjad.Staff([measure])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    {
                        \time 4/8
                        r8
                        d'8
                        <bf bqf>4
                    }
                }

        """
        pair = (self.width, cell_duration_denominator)
        time_signature = abjad.TimeSignature(pair)
        basic_cell_duration = abjad.Duration(1, cell_duration_denominator)
        measure_pitches: typing.List[typing.Optional[int]] = []
        measure_durations = []
        for cell in self.cells:
            cell_pitches = cell.pitches
            if not cell_pitches:
                measure_pitches.append(None)
            elif len(cell_pitches) == 1:
                measure_pitches.append(cell_pitches[0])
            else:
                measure_pitches.append(cell_pitches)
            measure_duration = cell.width * basic_cell_duration
            measure_durations.append(measure_duration)
        maker = abjad.LeafMaker()
        leaves = maker(measure_pitches, measure_durations)
        abjad.attach(time_signature, leaves[0])
        container = abjad.Container(leaves)
        return container

    def withdraw(self):
        """
        Withdraws pitch array row from parent pitch array.

        Returns pitch array row.
        """
        if self.parent_array is not None:
            self.parent_array.remove_row(self)
        return self


def pitch_arrays_to_score(pitch_arrays) -> abjad.Score:
    r"""
    Makes score from pitch arrays.

    ..  container:: example

        >>> array_1 = baca.array.PitchArray([
        ...   [1, (2, 1), ([-2, -1.5], 2)],
        ...   [(7, 2), (6, 1), 1],
        ... ])

        >>> array_2 = baca.array.PitchArray([
        ...   [1, 1, 1],
        ...   [1, 1, 1],
        ... ])

        >>> arrays = [array_1, array_2]
        >>> score = baca.array.pitch_arrays_to_score(arrays)
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context StaffGroup = "Staff_Group"
                <<
                    \context Staff = "Staff"
                    {
                        {
                            \time 4/8
                            r8
                            d'8
                            <bf bqf>4
                        }
                        {
                            \time 3/8
                            r8
                            r8
                            r8
                        }
                    }
                    \context Staff = "Staff"
                    {
                        {
                            \time 4/8
                            g'4
                            fs'8
                            r8
                        }
                        {
                            \time 3/8
                            r8
                            r8
                            r8
                        }
                    }
                >>
            >>

    """
    score = abjad.Score(name="Score")
    staff_group = abjad.StaffGroup(name="Staff_Group")
    score.append(staff_group)
    number_staves = pitch_arrays[0].depth
    staff = abjad.Staff(name="Staff")
    staves = abjad.mutate.copy(staff, number_staves)
    staff_group.extend(staves)
    for pitch_array in pitch_arrays:
        measures = pitch_array.to_measures()
        for staff, measure in zip(staves, measures):
            staff.append(measure)
    return score
