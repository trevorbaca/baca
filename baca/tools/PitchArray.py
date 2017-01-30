# -*- coding: utf-8 -*-
import abjad
import baca


class PitchArray(abjad.abctools.AbjadObject):
    r'''Pitch array.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        A two-by-three pitch array:

        ::

            >>> pitch_array = baca.tools.PitchArray([[1, 2, 1], [2, 1, 1]])
            >>> print(pitch_array)
            [ ] [     ] [ ]
            [     ] [ ] [ ]

        ::

            >>> f(pitch_array)
            baca.tools.PitchArray(
                rows=(
                    baca.tools.PitchArrayRow(
                        cells=(
                            baca.tools.PitchArrayCell(
                                width=1,
                                ),
                            baca.tools.PitchArrayCell(
                                width=2,
                                ),
                            baca.tools.PitchArrayCell(
                                width=1,
                                ),
                            ),
                        ),
                    baca.tools.PitchArrayRow(
                        cells=(
                            baca.tools.PitchArrayCell(
                                width=2,
                                ),
                            baca.tools.PitchArrayCell(
                                width=1,
                                ),
                            baca.tools.PitchArrayCell(
                                width=1,
                                ),
                            ),
                        ),
                    ),
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        '_columns',
        '_rows',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, rows=None):
        import baca
        self._rows = []
        self._columns = []
        if not rows:
            return
        for row in rows:
            row_ = baca.tools.PitchArrayRow([])
            for cell in row:
                if isinstance(cell, int):
                    cell = baca.tools.PitchArrayCell(width=cell)
                elif isinstance(cell, tuple):
                    assert len(cell) == 2, repr(cell)
                    pitches, width = cell
                    if isinstance(pitches, int):
                        pitches = [pitches]
                    cell = baca.tools.PitchArrayCell(
                        pitches=pitches,
                        width=width,
                        )
                row_.append(cell)
            self.append_row(row_)

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        r'''Concatenates `argument` to pitch array.

        Returns new pitch array.
        '''
        if not isinstance(argument, baca.tools.PitchArray):
            message = 'must be pitch array.'
            raise TypeError(message)
        if not self.depth == argument.depth:
            message = 'array depth must match.'
            raise ValueError(message)
        new_array = baca.tools.PitchArray([])
        for self_row, arg_row in zip(self.rows, argument.rows):
            new_row = self_row + arg_row
            new_array.append_row(new_row)
        return new_array

    def __contains__(self, argument):
        r'''Is true when pitch array contains `argument`. Otherwise false.

        Returns true or false.
        '''
        if isinstance(argument, baca.tools.PitchArrayRow):
            return argument in self.rows
        elif isinstance(argument, baca.tools.PitchArrayColumn):
            return argument in self.columns
        elif isinstance(argument, baca.tools.PitchArrayCell):
            return argument in self.cells
        elif isinstance(argument, abjad.NamedPitch):
            for pitch in self.pitches:
                if argument == pitch:
                    return True
            return False
        else:
            message = 'must be row, column, pitch or pitch cell.'
            raise ValueError(message)

    def __copy__(self):
        r'''Copies pitch array.

        Returns new pitch array.
        '''
        return type(self)(self.cell_tokens_by_row)

    def __eq__(self, argument):
        r'''Is true when `argument` is a pitch aarray with contents equal to that of
        this pitch array. Otherwise false.

        Returns true or false.
        '''
        if isinstance(argument, type(self)):
            for self_row, arg_row in zip(self.rows, argument.rows):
                if not self_row == arg_row:
                    return False
                return True
        return False

    def __getitem__(self, argument):
        r'''Gets row `argument` from pitch array.

        Returns pitch array row.
        '''
        return self.rows[argument]

    def __hash__(self):
        r'''Hashes pitch array.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(type(self), self).__hash__()

    def __iadd__(self, argument):
        r'''Adds `argument` to pitch array in place.

            >>> array_1 = baca.tools.PitchArray([[1, 2, 1], [2, 1, 1]])
            >>> print(array_1)
            [ ] [     ] [ ]
            [     ] [ ] [ ]

        ::

            >>> array_2 = baca.tools.PitchArray([[3, 4], [4, 3]])
            >>> print(array_2)
            [     ] [           ]
            [           ] [     ]

        ::

            >>> array_3 = baca.tools.PitchArray([[1, 1], [1, 1]])
            >>> print(array_3)
            [ ] [ ]
            [ ] [ ]

        ::

            >>> array_1 += array_2
            >>> print(array_1)
            [ ] [     ] [ ] [     ] [         ]
            [     ] [ ] [ ] [         ] [     ]

        ::

            >>> array_1 += array_3
            >>> print(array_1)
            [ ] [     ] [ ] [     ] [         ] [ ] [ ]
            [     ] [ ] [ ] [         ] [     ] [ ] [ ]

        Returns pitch array.
        '''
        if not isinstance(argument, type(self)):
            message = 'must be pitch array.'
            raise TypeError(message)
        for self_row, arg_row in zip(self.rows, argument.rows):
            self_row += arg_row
        return self

    def __ne__(self, argument):
        r'''Is true when pitch array does not equal `argument`. Otherwise false.

        Returns true or false.
        '''
        return not self == argument

    def __setitem__(self, i, argument):
        r'''Sets pitch array row `i` to `argument`.

        Retunrs none.
        '''
        if isinstance(i, int):
            if not isinstance(argument, baca.tools.PitchArrayRow):
                message = 'can assign only pitch array row to pitch array.'
                raise TypeError(message)
            self._rows[i]._parent_array = None
            argument._parent_array = self
            self._rows[i] = argument
        else:
            message = 'must be integer index.'
            raise ValueError(message)

    def __str__(self):
        r'''String representation of pitch array.

        Returns string.
        '''
        return self._two_by_two_format_string

    ### PRIVATE PROPERTIES ###

    @property
    def _two_by_two_format_string(self):
        return '\n'.join([str(x) for x in self.rows])

    ### PRIVATE METHODS ###

    def _column_format_width_at_index(self, index):
        columns = self.columns
        column = columns[index]
        return column._column_format_width

    def _format_cells(self, cells):
        result = [str(cell) for cell in cells]
        result = ' '.join(result)
        return result

    @staticmethod
    def _get_leaf_offsets(argment):
        offsets = []
        for leaf in abjad.iterate(argment).by_leaf():
            start_offset = leaf._get_timespan().start_offset
            if start_offset not in offsets:
                offsets.append(start_offset)
            stop_offset = leaf._get_timespan().stop_offset
            if stop_offset not in offsets:
                offsets.append(stop_offset)
        offsets.sort()
        return list(abjad.mathtools.difference_series(offsets))

    ### PUBLIC PROPERTIES ###

    @property
    def cell_tokens_by_row(self):
        r'''Gets cells tokens of pitch array by row.

        Returns tuple.
        '''
        return tuple([row.cell_tokens for row in self.rows])

    @property
    def cell_widths_by_row(self):
        r'''Gets cell widths of pitch array by row.

        Returns tuple.
        '''
        return tuple([row.cell_widths for row in self.rows])

    @property
    def cells(self):
        r'''Gets cells of pitch array.

        Returns set.
        '''
        cells = set([])
        for row in self.rows:
            cells.update(row.cells)
        return cells

    @property
    def columns(self):
        r'''Gets columns of pitch array.

        Returns tuple.
        '''
        columns = []
        cells = baca.Sequence(self.rows).zip(truncate=False)
        for i, cells in enumerate(cells):
            column = baca.tools.PitchArrayColumn(cells)
            column._parent_array = self
            column._column_index = i
            columns.append(column)
        return tuple(columns)

    @property
    def depth(self):
        r'''Gets depth of pitch array.

        Defined equal to number of pitch array rows in pitch array.

        Returns nonnegative integer.
        '''
        return len(self.rows)

    @property
    def dimensions(self):
        r'''Gets dimensions of pitch array.

        Returns pair.
        '''
        return self.depth, self.width

    @property
    def has_voice_crossing(self):
        r'''Is true when pitch array has voice crossing. Otherwise false.

        Returns true or false.
        '''
        for column in self.columns:
            if column.has_voice_crossing:
                return True
        return False

    @property
    def is_rectangular(self):
        r'''Is true when no rows in pitch array are defective. Otherwise false.

        Returns true or false.
        '''
        return all(not row.is_defective for row in self.rows)

    @property
    def pitches(self):
        r'''Gets pitches in pitch array.

        Returns tuple.
        '''
        return baca.Sequence(self.pitches_by_row).flatten()

    @property
    def pitches_by_row(self):
        r'''Gets pitches in pitch array by row.

        Returns tuple.
        '''
        pitches = []
        for row in self.rows:
            pitches.append(row.pitches)
        return tuple(pitches)

    @property
    def rows(self):
        r'''Gets rows in pitch array.

        Returns tuple.
        '''
        return tuple(self._rows)

    @property
    def size(self):
        r'''Gets size of pitch array.

        Defined equal to the product of depth and width.

        Returns nonnegative integer.
        '''
        return self.depth * self.width

    @property
    def voice_crossing_count(self):
        r'''Gets voice crossing count of pitch array.

        Returns nonnegative integer.
        '''
        count = 0
        for column in self.columns:
            if column.has_voice_crossing:
                count += 1
        return count

    @property
    def weight(self):
        r'''Gets weight of pitch array.

        Defined equal to the sum of the weight of the rows in pitch array.

        Returns nonnegative integer.
        '''
        return sum([row.weight for row in self.rows])

    @property
    def width(self):
        r'''Gets width of pitch array.

        Defined equal to the width of the widest row in pitch array.

        Returns nonnegative integer.
        '''
        try:
            return max([row.width for row in self.rows])
        except ValueError:
            return 0

    ### PUBLIC METHODS ###

    def append_column(self, column):
        r'''Appends `column` to pitch array.

        Returns none.
        '''
        if not isinstance(column, baca.tools.PitchArrayColumn):
            message = 'must be column.'
            raise TypeError(message)
        column._parent_array = self
        column_depth = column.depth
        if self.depth < column_depth:
            self.pad_to_depth(column_depth)
        self.pad_to_width(self.width)
        for row, cell in zip(self.rows, column):
            row.append(cell)

    def append_row(self, row):
        r'''Appends `row` to pitch array.

        Returns none.
        '''
        if not isinstance(row, baca.tools.PitchArrayRow):
            message = 'must be row.'
            raise TypeError(message)
        row._parent_array = self
        self._rows.append(row)

    def apply_pitches_by_row(self, pitch_lists):
        r'''Applies `pitch_lists` to pitch array by row.

        Returns none.
        '''
        for row, pitch_list in zip(self.rows, pitch_lists):
            row.apply_pitches(pitch_list)

    def copy_subarray(self, upper_left_pair, lower_right_pair):
        r'''Copies subarray of pitch array.

        Returns new pitch array.
        '''
        if not isinstance(upper_left_pair, tuple):
            raise TypeError
        if not isinstance(lower_right_pair, tuple):
            raise TypeError
        start_i, start_j = upper_left_pair
        stop_i, stop_j = lower_right_pair
        if not start_i <= stop_i:
            message = 'start row must not be greater than stop row.'
            raise ValueError(message)
        if not start_j <= stop_j:
            message = 'start column must not be greater than stop column.'
            raise ValueError(message)
        new_array = type(self)([])
        rows = self.rows
        row_indices = range(start_i, stop_i)
        for row_index in row_indices:
            new_row = rows[row_index].copy_subrow(start_j, stop_j)
            new_array.append_row(new_row)
        return new_array

    @classmethod
    def from_counts(class_, row_count, column_count):
        r'''Makes pitch array from row and column counts.

        Returns pitch array.
        '''
        array = class_()
        for i in range(row_count):
            row = baca.tools.PitchArrayRow([])
            for j in range(column_count):
                cell = baca.tools.PitchArrayCell()
                row.append(cell)
            array.append_row(row)
        return array

    @classmethod
    def from_score(class_, score, populate=True):
        r'''Makes pitch array from `score`.

        ..  container:: example

            Makes empty pitch array from score:

            ::

                >>> score = Score([])
                >>> score.append(Staff("c'8 d'8 e'8 f'8"))
                >>> score.append(Staff("c'4 d'4"))
                >>> score.append(
                ...     Staff(
                ...     abjad.scoretools.FixedDurationTuplet(
                ...     Duration(2, 8), "c'8 d'8 e'8") * 2)
                ...     )

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        c'8
                        d'8
                        e'8
                        f'8
                    }
                    \new Staff {
                        c'4
                        d'4
                    }
                    \new Staff {
                        \times 2/3 {
                            c'8
                            d'8
                            e'8
                        }
                        \times 2/3 {
                            c'8
                            d'8
                            e'8
                        }
                    }
                >>

            ::

                >>> show(score) # doctest: +SKIP

            ::

                >>> array = baca.tools.PitchArray.from_score(
                ...     score, populate=False)

            ::

                >>> print(array)
                [     ] [     ] [     ] [     ]
                [                 ] [                 ]
                [ ] [     ] [ ] [ ] [     ] [ ]

        ..  container:: example

            Makes populated pitch array from `score`:

            ::

                >>> score = Score([])
                >>> score.append(Staff("c'8 d'8 e'8 f'8"))
                >>> score.append(Staff("c'4 d'4"))
                >>> score.append(
                ...     Staff(
                ...     abjad.scoretools.FixedDurationTuplet(
                ...     Duration(2, 8), "c'8 d'8 e'8") * 2))

            ..  doctest::

                >>> f(score)
                \new Score <<
                    \new Staff {
                        c'8
                        d'8
                        e'8
                        f'8
                    }
                    \new Staff {
                        c'4
                        d'4
                    }
                    \new Staff {
                        \times 2/3 {
                            c'8
                            d'8
                            e'8
                        }
                        \times 2/3 {
                            c'8
                            d'8
                            e'8
                        }
                    }
                >>

            ::

                >>> show(score) # doctest: +SKIP

            ::

                >>> array = baca.tools.PitchArray.from_score(
                ...     score, populate=True)

            ::

                >>> print(array)
                [c'     ] [d'     ] [e'     ] [f'     ]
                [c'                   ] [d'                   ]
                [c'] [d'     ] [e'] [c'] [d'     ] [e']

        Returns pitch array.
        '''
        time_intervals = class_._get_leaf_offsets(score)
        array_width = len(time_intervals)
        array_depth = len(score)
        pitch_array = class_.from_counts(array_depth, array_width)
        items = abjad.scoretools.make_multiplied_quarter_notes(
            [0], time_intervals)
        for leaf_iterable, pitch_array_row in zip(score, pitch_array.rows):
            durations = []
            leaves = abjad.iterate(leaf_iterable).by_leaf()
            for leaf in leaves:
                durations.append(leaf._get_duration())
            parts = abjad.mutate(items).split(
                durations,
                cyclic=False,
                fracture_spanners=False,
                )
            part_lengths = [len(part) for part in parts]
            cells = pitch_array_row.cells
            grouped_cells = baca.Sequence(cells).partition_by_counts(
                part_lengths,
                cyclic=False,
                overhang=False,
                )
            for group in grouped_cells:
                pitch_array_row.merge(group)
            leaves = abjad.iterate(leaf_iterable).by_leaf()
            if populate:
                for cell, leaf in zip(pitch_array_row.cells, leaves):
                    cell.pitches.extend(abjad.iterate(leaf).by_pitch())
        return pitch_array

    def has_spanning_cell_over_index(self, index):
        r'''Is true when pitch array has one or more spanning cells over
        `index`. Otherwise false.

        Returns true or false.
        '''
        rows = self.rows
        return any(row.has_spanning_cell_over_index(index) for row in rows)

    def list_nonspanning_subarrays(self):
        r'''Lists nonspanning subarrays of pitch array.

        ..  container:: example

            Lists three nonspanning subarrays:

            ::

                >>> array = baca.tools.PitchArray([
                ...     [2, 2, 3, 1],
                ...     [1, 2, 1, 1, 2, 1],
                ...     [1, 1, 1, 1, 1, 1, 1, 1]])
                >>> print(array)
                [     ] [     ] [         ] [ ]
                [ ] [     ] [ ] [ ] [     ] [ ]
                [ ] [ ] [ ] [ ] [ ] [ ] [ ] [ ]

            ::

                >>> subarrays = array.list_nonspanning_subarrays()
                >>> len(subarrays)
                3

            ::

                >>> print(subarrays[0])
                [     ] [     ]
                [ ] [     ] [ ]
                [ ] [ ] [ ] [ ]

            ::

                >>> print(subarrays[1])
                [         ]
                [ ] [     ]
                [ ] [ ] [ ]

            ::

                >>> print(subarrays[2])
                [ ]
                [ ]
                [ ]

        Returns list.
        '''
        unspanned_indices = []
        for i in range(self.width + 1):
            if not self.has_spanning_cell_over_index(i):
                unspanned_indices.append(i)
        array_depth = self.depth
        subarrays = []
        pairs = abjad.Sequence(unspanned_indices).nwise()
        for start_column, stop_column in pairs:
            upper_left_pair = (0, start_column)
            lower_right_pair = (array_depth, stop_column)
            subarray = self.copy_subarray(upper_left_pair, lower_right_pair)
            subarrays.append(subarray)
        return subarrays

    def pad_to_depth(self, depth):
        r'''Pads pitch array to `depth`.

        Returns none.
        '''
        self_depth = self.depth
        if depth < self_depth:
            message = 'pad depth must be not less than array depth.'
            raise ValueError(message)
        self_width = self.width
        missing_rows = depth - self_depth
        for i in range(missing_rows):
            row = baca.tools.PitchArrayRow([])
            row.pad_to_width(self_width)
            self.append_row(row)

    def pad_to_width(self, width):
        r'''Pads pitch array to `width`.

        Returns none.
        '''
        self_width = self.width
        if width < self_width:
            message = 'pad width must not be less than array width.'
            raise ValueError(message)
        for row in self.rows:
            row.pad_to_width(width)

    def pop_column(self, column_index):
        r'''Pops column `column_index` from pitch array.

        Returns pitch array column.
        '''
        column = self.columns[column_index]
        column._parent_array = None
        for cell in column.cells:
            cell.withdraw()
        return column

    def pop_row(self, row_index=-1):
        r'''Pops row `row_index` from pitch array.

        Returns pitch array row.
        '''
        row = self._rows.pop(row_index)
        row._parent_array = None
        return row

    def remove_row(self, row):
        r'''Removes `row` from pitch array.

        Returns none.
        '''
        if row not in self.rows:
            message = 'row not in array.'
            raise ValueError(message)
        self._rows.remove(row)
        row._parent_array = None

    def to_measures(self, cell_duration_denominator=8):
        r'''Changes pitch array  to measures.

        Makes time signatures with numerators equal to row width and
        denominators equal to `cell_duration_denominator` for each row in pitch
        array.

        ..  container:: example

            Changes two-by-three pitch array to measures:

            ::

                >>> array = baca.tools.PitchArray([
                ...     [1, (2, 1), ([-2, -1.5], 2)],
                ...     [(7, 2), (6, 1), 1],
                ...     ])

            ::

                >>> print(array)
                [  ] [d'] [bf bqf    ]
                [g'     ] [fs'   ] [ ]

            ::

                >>> measures = array.to_measures()
                >>> staff = Staff(measures)
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> f(staff)
                \new Staff {
                    {
                        \time 4/8
                        r8
                        d'8
                        <bf bqf>4
                    }
                    {
                        g'4
                        fs'8
                        r8
                    }
                }

        Returns list of measures.
        '''
        measures = []
        for row in self.rows:
            measure = row.to_measure(cell_duration_denominator)
            measures.append(measure)
        return measures
