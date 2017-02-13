# -*- coding: utf-8 -*-
import abjad
import baca
import copy


class PitchArrayRow(abjad.abctools.AbjadObject):
    r'''Pitch array row.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        A pitch array row:

        ::

            >>> array = baca.tools.PitchArray([[1, 2, 1], [2, 1, 1]])
            >>> array[0].cells[0].append_pitch(0)
            >>> array[0].cells[1].append_pitch(2)
            >>> array[1].cells[2].append_pitch(4)
            >>> print(array)
            [c'] [d'    ] [  ]
            [       ] [ ] [e']

        ::

            >>> f(array[0])
            baca.tools.PitchArrayRow(
                cells=(
                    baca.tools.PitchArrayCell(
                        pitches=[
                            pitchtools.NamedPitch("c'"),
                            ],
                        width=1,
                        ),
                    baca.tools.PitchArrayCell(
                        pitches=[
                            pitchtools.NamedPitch("d'"),
                            ],
                        width=2,
                        ),
                    baca.tools.PitchArrayCell(
                        width=1,
                        ),
                    ),
                )

        ::

            >>> array[0].cell_widths
            (1, 2, 1)

        ::

            >>> array[0].dimensions
            (1, 4)

        ::

            >>> array[0].pitches
            (NamedPitch("c'"), NamedPitch("d'"))

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        '_cells',
        '_parent_array',
        '_pitch_range',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, cells=None):
        self._parent_array = None
        self._pitch_range = abjad.PitchRange()
        self._cells = []
        cells = cells or []
        self.extend(cells)

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        r'''Concatenates `argument` to pitch array row.

        ..  container:: example

            ::

                >>> array = baca.tools.PitchArray([[1, 2, 1], [2, 1, 1]])
                >>> array[0].cells[0].append_pitch(0)
                >>> array[0].cells[1].append_pitch(2)
                >>> array[1].cells[2].append_pitch(4)

            ::

                >>> print(array)
                [c'] [d'    ] [  ]
                [       ] [ ] [e']

            ::

                >>> new_row = array[0] + array[1]

            ::

                >>> print(new_row)
                [c'] [d'] [ ] [ ] [ ] [e']

        Returns new pitch array row.
        '''
        if not isinstance(argument, PitchArrayRow):
            message = 'must be pitch array row.'
            raise TypeError(message)
        self_copy = copy.copy(self)
        arg_copy = copy.copy(argument)
        new_row = PitchArrayRow([])
        new_row.extend(self_copy.cells)
        new_row.extend(arg_copy.cells)
        return new_row

    def __copy__(self):
        r'''Copies pitch array row.

        Returns new pitch array row.
        '''
        new_cells = []
        for cell in self.cells:
            new_cell = copy.copy(cell)
            new_cells.append(new_cell)
        return PitchArrayRow(new_cells)

    def __eq__(self, argument):
        r'''Is true when `argument` is a pitch array row with contents equal to that
        of this pitch array row. Otherwise false.

        Returns true or false.
        '''
        if isinstance(argument, PitchArrayRow):
            for self_cell, arg_cell in zip(self.cells, argument.cells):
                if not self_cell.matches_cell(arg_cell):
                    return False
                return True
        return False

    def __getitem__(self, argument):
        r'''Gets cell or cell slice identified by `argument`.

        Returns pitch array cell or slice of pitch array cells.
        '''
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
                message = 'no such cell in row.'
                raise IndexError(message)
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
            message = 'must be int or slice.'
            raise ValueError(message)

    def __hash__(self):
        r'''Hashes pitch array row.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(PitchArrayRow, self).__hash__()

    def __iadd__(self, argument):
        r'''Adds `argument` to pitch array row in place.

        ..  container:: example

            ::

                >>> array = baca.tools.PitchArray([[1, 2, 1], [2, 1, 1]])
                >>> array[0].cells[0].append_pitch(0)
                >>> array[0].cells[1].append_pitch(2)
                >>> array[1].cells[2].append_pitch(4)

            ::

                >>> print(array)
                [c'] [d'    ] [  ]
                [       ] [ ] [e']

            ::

                >>> row = array[0].withdraw()
                >>> row += row

            ::

                >>> print(row)
                [c'] [d'] [ ] [c'] [d'] [ ]

        Returns pitch array row.
        '''
        if not isinstance(argument, PitchArrayRow):
            message = 'must be pitch array row.'
            raise TypeError(message)
        copy_arg = copy.copy(argument)
        self.extend(copy_arg.cells)
        return self

    def __iter__(self):
        r'''Iterates pitch array row.

        Returns generator.
        '''
        return iter(self.cells)

    def __len__(self):
        r'''Gets length of pitch array row.

        Length defined equal to the width of pitch array row.

        Returns nonnegative integer.
        '''
        return self.width

    def __ne__(self, argument):
        r'''Is true when pitch array row does not equal `argument`. Otherwise false.

        Returns true or false.
        '''
        return not self == argument

    def __str__(self):
        r'''Gets string representation of pitch array row.

        Returns string.
        '''
        result = [str(cell) for cell in self.cells]
        result = ' '.join(result)
        return result

    ### PRIVATE PROPERTIES ###

    @property
    def _compact_summary(self):
        len_self = len(self.cells)
        if not len_self:
            return ''
        elif 0 < len_self <= 8:
            result = [
                cell._format_row_column_repr_string for cell in self.cells]
            return ', '.join(result)
        else:
            left = ', '.join(
                [x._format_row_column_repr_string for x in self.cells[:2]])
            right = ', '.join(
                [x._format_row_column_repr_string for x in self.cells[-2:]])
            number_in_middle = len_self - 4
            middle = ', ... [%s] ..., '% number_in_middle
            return left + middle + right

    @property
    def _format_contents_string(self):
        result = []
        for cell in self.cells:
            result.append(cell._format_row_column_repr_string)
        result = ', '.join(result)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def cell_tokens(self):
        r'''Gets cell items of pitch array row.

        Returns tuple.
        '''
        return tuple([cell.item for cell in self.cells])

    @property
    def cell_widths(self):
        r'''Gets cell widths of pitch array row.

        Returns tuple.
        '''
        return tuple([cell.width for cell in self.cells])

    @property
    def cells(self):
        r'''Gets cells of pitch array row.

        Returns tuple.
        '''
        return tuple(self._cells)

    @property
    def depth(self):
        r'''Gets depth of pitch array row.

        Defined equal to ``1``.

        Returns ``1``.
        '''
        return 1

    @property
    def dimensions(self):
        r'''Gets dimensions of pitch array row.

        Returns pair.
        '''
        return self.depth, self.width

    @property
    def is_defective(self):
        r'''Is true when width of pitch array row does not equal width of
        parent pitch array. Otherwise false.

        Returns true or false.
        '''
        if self.parent_array is not None:
            return not self.width == self.parent_array.width
        return False

    @property
    def is_in_range(self):
        r'''Is true when all pitches in pitch array row are in pitch range of
        pitch array row. Otherwise false.

        Returns true or false.
        '''
        return all(pitch in self.pitch_range for pitch in self.pitches)

    @property
    def parent_array(self):
        r'''Gets parent pitch array housing pitch array row.

        Returns pitch array or none.
        '''
        return self._parent_array

    @property
    def pitch_range(self):
        r'''Gets and sets pitch range of pitch array row.

        Returns pitch range.
        '''
        return self._pitch_range

    @pitch_range.setter
    def pitch_range(self, argument):
        if not isinstance(argument, abjad.PitchRange):
            message = 'must be pitch range.'
            raise TypeError(message)
        self._pitch_range = argument

    @property
    def pitches(self):
        r'''Gets pitches in pitch array row.

        Returns tuple.
        '''
        pitches = []
        for cell in self.cells:
            if cell.pitches is not None:
                pitches.extend(cell.pitches)
        return tuple(pitches)

    @property
    def row_index(self):
        r'''Gets row index of pitch array row in parent pitch array.

        Returns nonnegative integer.
        '''
        parent_array = self.parent_array
        if parent_array is not None:
            return parent_array._rows.index(self)
        message = 'row has no parent array.'
        raise IndexError(message)

    @property
    def weight(self):
        r'''Gets weight of pitch array row.

        Defined equal to sum of weights of pitch array cells in pitch array
        row.

        Returns nonnegative integer.
        '''
        return sum([cell.weight for cell in self.cells])

    @property
    def width(self):
        r'''Gets width of pitch array row.

        Defined equal to sum of widths of pitch array cells in pitch array row.

        Returns nonnegative integer.
        '''
        return sum([cell.width for cell in self.cells])

    ### PUBLIC METHODS ###

    def append(self, cell):
        r'''Appends `cell` to pitch array row.

        ..  container:: example

            ::

                >>> array = baca.tools.PitchArray([[1, 2, 1], [2, 1, 1]])
                >>> array[0].cells[0].append_pitch(abjad.NamedPitch(0))
                >>> array[0].cells[1].append_pitch(abjad.NamedPitch(2))
                >>> array[0].cells[1].append_pitch(abjad.NamedPitch(4))

            ::

                >>> print(array)
                [c'] [d' e'    ] [ ]
                [          ] [ ] [ ]

            ::

                >>> cell = baca.tools.PitchArrayCell(width=1)
                >>> array[0].append(cell)
                >>> cell = baca.tools.PitchArrayCell(width=1)
                >>> array[1].append(cell)

            ::

                >>> print(array)
                [c'] [d' e'    ] [ ] [ ]
                [          ] [ ] [ ] [ ]

        Returns none.
        '''
        assert isinstance(cell, baca.tools.PitchArrayCell), repr(cell)
        cell._parent_row = self
        self._cells.append(cell)

    def apply_pitches(self, pitch_tokens):
        r'''Applies `pitch_tokens` to pitch cells in pitch array row.

        ..  container:: example

            ::

                >>> array = baca.tools.PitchArray([
                ...     [1, (0, 1), (0, 2)],
                ...     [(0, 2), (0, 1), 1],
                ...     ])

            ::

                >>> print(array)
                [  ] [c'] [c'    ]
                [c'     ] [c'] [ ]

            ::

                >>> array[0].apply_pitches([-2, -1.5])

            ::

                >>> print(array)
                [  ] [bf] [bqf    ]
                [c'     ] [c' ] [ ]

        Returns none.
        '''
        pitch_tokens = pitch_tokens[:]
        if pitch_tokens:
            for cell in self.cells:
                if cell.pitches:
                    cell.pitches = [pitch_tokens.pop(0)]
        else:
            self.empty_pitches()

    def copy_subrow(self, start=None, stop=None):
        r'''Copies subrow of pitch array row from `start` to `stop`.

        ..  container:: example

            ::

                >>> array = baca.tools.PitchArray([[1, 2, 1], [2, 1, 1]])
                >>> array[0].cells[0].append_pitch(0)
                >>> array[0].cells[1].append_pitch(2)
                >>> array[1].cells[2].append_pitch(4)

            ::

                >>> print(array)
                [c'] [d'    ] [  ]
                [       ] [ ] [e']

            ::

                >>> subrow = array[0].copy_subrow(2, None)

            ::

                >>> print(subrow)
                [d'] [ ]

        Returns new pitch array row.
        '''
        argument = slice(start, stop)
        start, stop, step = argument.indices(self.width)
        if not step == 1:
            message = 'step no implemented.'
            raise NotImplementedError(message)
        column_indices = set(range(start, stop, step))
        row = PitchArrayRow([])
        cells = self[argument]
        new_cells = []
        for cell in cells:
            if not cell in new_cells:
                trim = [
                    x for x in cell.column_indices if x not in column_indices]
                new_width = cell.width - len(trim)
                new_cell = copy.copy(cell)
                new_cell._width = new_width
                new_cells.append(new_cell)
        row.extend(new_cells)
        return row

    def empty_pitches(self):
        r'''Empties pitches in pitch array row.

        ..  container:: example

            ::

                >>> array = baca.tools.PitchArray([[1, 2, 1], [2, 1, 1]])
                >>> array[0].cells[0].append_pitch(0)
                >>> array[0].cells[1].append_pitch(2)
                >>> array[1].cells[2].append_pitch(4)

            ::

                >>> print(array)
                [c'] [d'    ] [  ]
                [       ] [ ] [e']

            ::

                >>> array[0].empty_pitches()

            ::

                >>> print(array)
                [ ] [     ] [  ]
                [     ] [ ] [e']

        Returns none.
        '''
        for cell in self.cells:
            cell.pitches = []

    def extend(self, cells):
        r'''Extends pitch array row with `cells`.

        ..  container:: example

            ::

                >>> array = baca.tools.PitchArray([[1, 2, 1], [2, 1, 1]])
                >>> array[0].cells[0].append_pitch(0)
                >>> array[0].cells[1].append_pitch(2)
                >>> array[1].cells[2].append_pitch(4)

            ::

                >>> print(array)
                [c'] [d'    ] [  ]
                [       ] [ ] [e']

            ::

                >>> cells = [baca.tools.PitchArrayCell(width=_) for _ in [1, 1, 1]]
                >>> array[0].extend(cells)
                >>> cell = baca.tools.PitchArrayCell(width=3)
                >>> array[1].append(cell)

            ::

                >>> print(array)
                [c'] [d'    ] [  ] [ ] [ ] [ ]
                [       ] [ ] [e'] [     ]

        Returns none.
        '''
        for cell in cells:
            self.append(cell)

    def has_spanning_cell_over_index(self, i):
        r'''Is true when pitch array row has one or more cells spanning over
        index `i`. Otherwise false.

        ..  container:: example

            ::

                >>> array = baca.tools.PitchArray([[1, 2, 1], [2, 1, 1]])
                >>> array[0].cells[0].append_pitch(0)
                >>> array[0].cells[1].append_pitch(2)
                >>> array[1].cells[2].append_pitch(4)

            ::

                >>> print(array)
                [c'] [d'    ] [  ]
                [       ] [ ] [e']

            ::

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
        '''
        try:
            cell = self[i]
            return cell.column_indices[0] < i
        except IndexError:
            return False

    def index(self, cell):
        r'''Gets index of pitch array `cell` in pitch array row.

        Retunrs nonnegative integer.
        '''
        return self._cells.index(cell)

    def merge(self, cells):
        r'''Merges `cells`.

        Returns pitch array cell.
        '''
        column_indices = []
        pitches = []
        width = 0
        for cell in cells:
            if not isinstance(cell, baca.tools.PitchArrayCell):
                raise TypeError
            if not cell.parent_row is self:
                message = 'cells must belong to row.'
                raise ValueError(message)
            column_indices.extend(cell.column_indices)
            if cell.pitches is not None:
                pitches.extend(cell.pitches)
            width += cell.width
        start = min(column_indices)
        stop = start + len(column_indices)
        strict_series = list(range(start, stop))
        if not column_indices == strict_series:
            message = 'cells must be contiguous.'
            raise ValueError(message)
        first_cell = cells[0]
        for cell in cells[1:]:
            self.remove(cell)
        first_cell._pitches = pitches
        first_cell._width = width
        return first_cell

    def pad_to_width(self, width):
        r'''Pads pitch array row to `width`.

        Returns none.
        '''
        self_width = self.width
        if width < self_width:
            message = 'pad width must not be less than row width.'
            raise ValueError(message)
        missing_width = width - self_width
        for i in range(missing_width):
            cell = baca.tools.PitchArrayCell()
            self.append(cell)

    def pop(self, cell_index):
        r'''Pops cell `cell_index` from pitch array row.

        Returns pitch array cell.
        '''
        cell = self.pop(cell_index)
        cell._parent_row = None
        return cell

    def remove(self, cell):
        r'''Removes `cell` form pitch array row.

        Returns none.
        '''
        for i, x in enumerate(self.cells):
            if x is cell:
                self._cells.pop(i)
                break
        cell._parent_row = None

    def to_measure(self, cell_duration_denominator=8):
        r'''Changes pitch array row to measures.

        Sets time signature numerators equal to pitch array row widths and time
        signature denominators equal to `cell_duration_denominator`.

        ..  container:: example

            Changes row to measure:

            ::

                >>> array = baca.tools.PitchArray([
                ...     [1, (2, 1), ([-2, -1.5], 2)],
                ...     [(7, 2), (6, 1), 1]])

            ::

                >>> print(array)
                [  ] [d'] [bf bqf    ]
                [g'     ] [fs'   ] [ ]

            ::

                >>> measure = array.rows[0].to_measure()
                >>> show(measure) # doctest: +SKIP

            ..  doctest::

                >>> f(measure)
                {
                    \time 4/8
                    r8
                    d'8
                    <bf bqf>4
                }

        Returns measure.
        '''
        from abjad.tools import scoretools
        pair = (self.width, cell_duration_denominator)
        time_signature = abjad.TimeSignature(pair)
        measure = scoretools.Measure(time_signature, [])
        basic_cell_duration = abjad.Duration(1, cell_duration_denominator)
        measure_pitches, measure_durations = [], []
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
        leaves = scoretools.make_leaves(measure_pitches, measure_durations)
        measure.extend(leaves)
        return measure

    def withdraw(self):
        r'''Withdraws pitch array row from parent pitch array.

        Returns pitch array row.
        '''
        if self.parent_array is not None:
            self.parent_array.remove_row(self)
        return self
