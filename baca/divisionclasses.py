"""
Division library.
"""
import abjad
import collections
import inspect
import typing
from . import classes


### CLASSES ###


class Division(abjad.NonreducedFraction):
    r"""
    Division.

    >>> from abjadext import rmakers

    ..  container:: example

        Initializes empty:

        >>> baca.Division()
        Division((0, 1))

    ..  container:: example

        Initializes without start offset:

        >>> baca.Division((4, 8))
        Division((4, 8))

    ..  container:: example

        Initializes with start offset:

        >>> baca.Division((4, 8), start_offset=(6, 4))
        Division((4, 8), start_offset=Offset(3, 2))

    ..  container:: example

        Initializes from other division:

        >>> division = baca.Division((4, 8), start_offset=(6, 4))
        >>> new_division = baca.Division(division)
        >>> division == new_division
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_start_offset",)

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, *arguments, **keywords) -> None:
        """
        Dummy initializer to satisfy mypy.
        """
        pass

    # Rational.__new__() docstring raises Sphinx warning;
    # custom docstring provided here prevents Sphinx warning.
    def __new__(class_, argument=None, start_offset=None):
        """
        Constructs division.
        """
        argument = argument or (0, 1)
        if isinstance(argument, str):
            division = eval(argument)
            argument = division
            if start_offset is None:
                start_offset = argument.start_offset
        if isinstance(argument, abjad.NonreducedFraction):
            if start_offset is None:
                start_offset = getattr(argument, "start_offset", None)
        self = abjad.NonreducedFraction.__new__(class_, argument)
        if start_offset is not None:
            start_offset = abjad.Offset(start_offset)
        self._start_offset = start_offset
        return self

    ### SPECIAL METHODS###

    def __add__(self, argument) -> "Division":
        """
        Adds ``argument`` to division.

        ..  container:: example

            No start offsets:

            >>> division_1 = baca.Division((2, 4))
            >>> division_2 = baca.Division((4, 4))
            >>> division_1 + division_2
            Division((6, 4))

        ..  container:: example

            One start offset:

            >>> division_1 = baca.Division((2, 4), start_offset=1)
            >>> division_2 = baca.Division((4, 4))
            >>> division_1 + division_2
            Division((6, 4), start_offset=Offset(1, 1))

        ..  container:: example

            Contiguous start offsets:

            >>> division_1 = baca.Division((2, 4), start_offset=1)
            >>> division_2 = baca.Division((4, 4), start_offset=(3, 2))
            >>> division_1 + division_2
            Division((6, 4), start_offset=Offset(1, 1))

        ..  container:: example

            Noncontiguous start offsets:

            >>> division_1 = baca.Division((2, 4), start_offset=1)
            >>> division_2 = baca.Division((4, 4), start_offset=10)
            >>> division_1 + division_2
            Division((40, 4), start_offset=Offset(1, 1))

        ..  container:: example

            Identical start offsets:

            >>> division_1 = baca.Division((2, 4), start_offset=1)
            >>> division_2 = baca.Division((4, 4), start_offset=1)
            >>> division_1 + division_2
            Division((4, 4), start_offset=Offset(1, 1))

        ..  container:: example

            Overlapping start offsets:

            >>> division_1 = baca.Division((2, 4), start_offset=1)
            >>> division_2 = baca.Division((4, 4), start_offset=(5, 4))
            >>> division_1 + division_2
            Division((5, 4), start_offset=Offset(1, 1))

        """
        if not isinstance(argument, type(self)):
            argument = type(self)(argument)
        start_offsets = []
        stop_offsets = []
        if self.start_offset is not None:
            start_offsets.append(self.start_offset)
            stop_offsets.append(self.stop_offset)
        if argument.start_offset is not None:
            start_offsets.append(argument.start_offset)
            stop_offsets.append(argument.stop_offset)
        sum_ = super().__add__(argument)
        if not start_offsets:
            division = type(self)(sum_)
        elif len(start_offsets) == 1:
            start_offset = start_offsets[0]
            division = type(self)(sum_, start_offset=start_offset)
        elif len(start_offsets) == 2:
            start_offset = min(start_offsets)
            stop_offset = max(stop_offsets)
            duration = stop_offset - start_offset
            division = type(self)(duration)
            division = division.with_denominator(self.denominator)
            if not division.denominator == self.denominator:
                division = division.with_denominator(argument.denominator)
            division = type(self)(division, start_offset=start_offset)
        else:
            raise Exception(f"invalid start offsets: {start_offsets!r}.")
        return division

    def __copy__(self, *arguments) -> "Division":
        """
        Copies division.
        """
        arguments = self.__getnewargs__()
        return type(self)(*arguments)

    def __deepcopy__(self, *arguments) -> "Division":
        """
        Deep copies division.
        """
        return self.__copy__(*arguments)

    def __getnewargs__(self) -> typing.Tuple:
        """
        Gets new arguments.
        """
        return (self.pair, self.start_offset)

    def __str__(self) -> str:
        """
        Gets string representation of division.
        """
        return repr(self)

    def __sub__(self, argument) -> "Division":
        """
        Subtracts ``argument`` from division.

        ..  container:: example

            No timespans:

            >>> division_1 = baca.Division((6, 2))
            >>> division_2 = baca.Division((4, 2))

            >>> division_1 - division_2
            Division((2, 2))

            >>> division_2 - division_1
            Division((-2, 2))

        ..  container:: example

            Overlapping timespans that start at the same time:

            >>> division_1 = baca.Division((4, 1), start_offset=10)
            >>> division_2 = baca.Division((2, 1), start_offset=10)

            >>> division_1 - division_2
            Division((2, 1), start_offset=Offset(12, 1))

            >>> division_2 - division_1
            Division((-2, 1), start_offset=Offset(12, 1))

        ..  container:: example

            Overlapping timespans that start at different times:

            >>> division_1 = baca.Division((4, 1), start_offset=10)
            >>> division_2 = baca.Division((4, 1), start_offset=12)

            >>> division_1 - division_2
            Division((2, 1), start_offset=Offset(10, 1))

            >>> division_2 - division_1
            Division((2, 1), start_offset=Offset(14, 1))

        ..  container:: example

            Nonoverlapping timespans:

            >>> division_1 = baca.Division((6, 2), start_offset=0)
            >>> division_2 = baca.Division((4, 2), start_offset=20)

            >>> division_1 - division_2
            Division((6, 2), start_offset=Offset(0, 1))

            >>> division_2 - division_1
            Division((4, 2), start_offset=Offset(20, 1))

        ..  container:: example exception

             Raises exception when one division has a start offset and the
             other does not:

            >>> division_1 = baca.Division((6, 4), start_offset=5)
            >>> division_2 = baca.Division((2, 4))

            >>> division_1 - division_2
            Traceback (most recent call last):
                ...
            Exception: both divisions must have (or not have) start offsets.

            >>> division_2 - division_1
            Traceback (most recent call last):
                ...
            Exception: both divisions must have (or not have) start offsets.

        Uses timespan arithmetic when both divisions have a start offset.
        """
        if not isinstance(argument, type(self)):
            argument = type(self)(argument, start_offset=self.start_offset)
        self_has_start_offset = bool(self.start_offset is not None)
        expr_has_start_offset = bool(argument.start_offset is not None)
        if not self_has_start_offset == expr_has_start_offset:
            message = "both divisions must have (or not have) start offsets."
            raise Exception(message)
        if self.start_offset is argument.start_offset is None:
            difference = super().__sub__(argument)
            return self._from_pair(difference)
        my_timespan = self.timespan
        expr_timespan = argument.timespan
        timespans = my_timespan - expr_timespan
        negate_result = False
        if len(timespans) == 0:
            timespans = expr_timespan - my_timespan
            negate_result = True
        assert 0 < len(timespans), repr(timespans)
        if len(timespans) == 1:
            result_timespan = timespans[0]
            duration = result_timespan.duration
            nonreduced_fraction = duration.with_denominator(self.denominator)
            pair = nonreduced_fraction.pair
            start_offset = result_timespan.start_offset
            division = type(self)(pair, start_offset=start_offset)
            if negate_result:
                division = -division
            return division
        else:
            message = "timespan subtraction creates more than one division."
            raise Exception(message)

    ### PRIVATE METHODS ###

    def _from_pair(self, pair):
        return type(self)(pair, start_offset=self.start_offset)

    def _get_format_specification(self):
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=[self.pair],
            storage_format_kwargs_names=["start_offset"],
        )

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self) -> abjad.Duration:
        """
        Gets duration.

        ..  container:: example

            >>> baca.Division((6, 4)).duration
            Duration(3, 2)

        """
        return abjad.Duration(self)

    @property
    def start_offset(self) -> typing.Optional[abjad.Offset]:
        """
        Gets start offset.

        ..  container:: example

            >>> baca.Division((3, 8)).start_offset is None
            True

            >>> baca.Division((3, 8), start_offset=(5, 4)).start_offset
            Offset(5, 4)

        """
        return self._start_offset

    @property
    def stop_offset(self) -> typing.Optional[abjad.Offset]:
        """
        Gets stop offset.

        ..  container:: example

            >>> baca.Division((3, 8)).stop_offset is None
            True

            >>> baca.Division((3, 8), start_offset=(5, 4)).stop_offset
            Offset(13, 8)

        """
        if self.start_offset is None:
            return None
        return self.start_offset + self.duration

    @property
    def timespan(self) -> typing.Optional[abjad.Timespan]:
        """
        Gets timespan.

        ..  container:: example

            >>> baca.Division((3, 8)).timespan is None
            True

            >>> baca.Division((3, 8), start_offset=(5, 4)).timespan
            Timespan(start_offset=Offset(5, 4), stop_offset=Offset(13, 8))

        """
        if self.start_offset is None:
            return None
        stop_offset = self.start_offset + self
        return abjad.Timespan(
            start_offset=self.start_offset, stop_offset=stop_offset
        )

    ### PUBLIC METHODS ###

    def find_equivalent_durations(
        self, minimum_written_duration=(1, 128)
    ) -> typing.List[typing.Tuple[abjad.Multiplier, abjad.Duration]]:
        """
        Finds all multiplier-duration pairs equivalent to this duration.

        Returns output in Cantor diagonalized order.

        Ensures written duration never less than ``minimum_written_duration``.

        ..  container:: example

            Finds durations equivalent to ``1/8``:

            >>> pairs = baca.Division(1, 8).find_equivalent_durations()
            >>> for pair in pairs: pair
            ...
            (Multiplier(1, 1), Duration(1, 1))
            (Multiplier(2, 3), Duration(3, 2))
            (Multiplier(4, 3), Duration(3, 4))
            (Multiplier(4, 7), Duration(7, 4))
            (Multiplier(8, 7), Duration(7, 8))
            (Multiplier(8, 15), Duration(15, 8))
            (Multiplier(16, 15), Duration(15, 16))
            (Multiplier(16, 31), Duration(31, 16))
            (Multiplier(32, 31), Duration(31, 32))
            (Multiplier(32, 63), Duration(63, 32))
            (Multiplier(64, 63), Duration(63, 64))
            (Multiplier(64, 127), Duration(127, 64))
            (Multiplier(128, 127), Duration(127, 128))

        ..  container:: example

            Finds durations equivalent to ``1/12``:

            >>> pairs = baca.Division(1, 12).find_equivalent_durations()
            >>> for pair in pairs: pair
            ...
            (Multiplier(1, 1), Duration(1, 1))
            (Multiplier(2, 3), Duration(3, 2))
            (Multiplier(4, 3), Duration(3, 4))
            (Multiplier(4, 7), Duration(7, 4))
            (Multiplier(8, 7), Duration(7, 8))
            (Multiplier(8, 15), Duration(15, 8))
            (Multiplier(16, 15), Duration(15, 16))
            (Multiplier(16, 31), Duration(31, 16))
            (Multiplier(32, 31), Duration(31, 32))
            (Multiplier(32, 63), Duration(63, 32))
            (Multiplier(64, 63), Duration(63, 64))
            (Multiplier(64, 127), Duration(127, 64))
            (Multiplier(128, 127), Duration(127, 128))

        ..  container:: example

            Finds durations equivalent to ``5/48``:

            >>> pairs = baca.Division(5, 48).find_equivalent_durations()
            >>> for pair in pairs: pair
            ...
            (Multiplier(5, 3), Duration(3, 1))
            (Multiplier(5, 4), Duration(4, 1))
            (Multiplier(5, 6), Duration(6, 1))
            (Multiplier(5, 7), Duration(7, 1))
            (Multiplier(5, 8), Duration(8, 1))
            (Multiplier(10, 7), Duration(7, 2))
            (Multiplier(2, 3), Duration(15, 2))
            (Multiplier(4, 3), Duration(15, 4))
            (Multiplier(20, 31), Duration(31, 4))
            (Multiplier(40, 31), Duration(31, 8))
            (Multiplier(40, 63), Duration(63, 8))
            (Multiplier(80, 63), Duration(63, 16))
            (Multiplier(80, 127), Duration(127, 16))
            (Multiplier(160, 127), Duration(127, 32))

        """
        duration = abjad.Duration(self)
        minimum_written_duration = abjad.Duration(minimum_written_duration)
        generator = Division.yield_durations(unique=True)
        pairs: typing.List[typing.Tuple[abjad.Multiplier, abjad.Duration]] = []
        while True:
            written_duration = next(generator)
            if not written_duration.is_assignable:
                continue
            if written_duration < minimum_written_duration:
                return pairs
            multiplier = duration / written_duration
            if multiplier.normalized():
                pair = (multiplier, written_duration)
                pairs.append(pair)

    @staticmethod
    def yield_durations(unique=False) -> typing.Generator:
        """
        Yields all positive durations.

        ..  container:: example

            Yields all positive durations in Cantor diagonalized order:

            >>> generator = baca.Division.yield_durations()
            >>> for i in range(16):
            ...     next(generator)
            ...
            Duration(1, 1)
            Duration(2, 1)
            Duration(1, 2)
            Duration(1, 3)
            Duration(1, 1)
            Duration(3, 1)
            Duration(4, 1)
            Duration(3, 2)
            Duration(2, 3)
            Duration(1, 4)
            Duration(1, 5)
            Duration(1, 2)
            Duration(1, 1)
            Duration(2, 1)
            Duration(5, 1)
            Duration(6, 1)

        ..  container:: example

            Yields all positive durations in Cantor diagonalized order
            uniquely:

            >>> generator = baca.Division.yield_durations(unique=True)
            >>> for i in range(16):
            ...     next(generator)
            ...
            Duration(1, 1)
            Duration(2, 1)
            Duration(1, 2)
            Duration(1, 3)
            Duration(3, 1)
            Duration(4, 1)
            Duration(3, 2)
            Duration(2, 3)
            Duration(1, 4)
            Duration(1, 5)
            Duration(5, 1)
            Duration(6, 1)
            Duration(5, 2)
            Duration(4, 3)
            Duration(3, 4)
            Duration(2, 5)

        """
        generator = Division.yield_nonreduced_fractions()
        while True:
            integer_pair = next(generator)
            duration = abjad.Duration(integer_pair)
            if not unique:
                yield duration
            elif duration.pair == integer_pair:
                yield duration

    @staticmethod
    def yield_nonreduced_fractions() -> typing.Generator:
        """
        Yields positive nonreduced fractions in Cantor diagonalized order.

        ..  container:: example

            >>> generator = baca.Division.yield_nonreduced_fractions()
            >>> for i in range(16):
            ...     next(generator)
            ...
            (1, 1)
            (2, 1)
            (1, 2)
            (1, 3)
            (2, 2)
            (3, 1)
            (4, 1)
            (3, 2)
            (2, 3)
            (1, 4)
            (1, 5)
            (2, 4)
            (3, 3)
            (4, 2)
            (5, 1)
            (6, 1)

        """
        number = 2
        while True:
            if number % 2 == 0:
                lhs = 1
                while lhs < number:
                    rhs = number - lhs
                    yield lhs, rhs
                    lhs += 1
            else:
                lhs = number - 1
                while 0 < lhs:
                    rhs = number - lhs
                    yield lhs, rhs
                    lhs -= 1
            number += 1


class DivisionSequence(abjad.Sequence):
    r"""
    Division sequence.

    ..  container:: example

        >>> baca.DivisionSequence([(3, 8), (3, 8), (2, 8)])
        DivisionSequence([Division((3, 8)), Division((3, 8)), Division((2, 8))])

    ..  container:: example

        Partitions by ratio of lengths:

        >>> divisions = baca.DivisionSequence(
        ...     10 * [(1, 8)], start_offset=(0, 1)
        ... )

        >>> for division in divisions:
        ...     print(division)
        ...
        Division((1, 8), start_offset=Offset(0, 1))
        Division((1, 8), start_offset=Offset(1, 8))
        Division((1, 8), start_offset=Offset(1, 4))
        Division((1, 8), start_offset=Offset(3, 8))
        Division((1, 8), start_offset=Offset(1, 2))
        Division((1, 8), start_offset=Offset(5, 8))
        Division((1, 8), start_offset=Offset(3, 4))
        Division((1, 8), start_offset=Offset(7, 8))
        Division((1, 8), start_offset=Offset(1, 1))
        Division((1, 8), start_offset=Offset(9, 8))

        Partitions divisions into thirds:

        >>> ratio = abjad.Ratio((1, 1, 1))
        >>> parts = divisions.partition_by_ratio_of_lengths(ratio)

        Gets middle third:

        >>> for division in parts[1]:
        ...     division
        Division((1, 8), start_offset=Offset(3, 8))
        Division((1, 8), start_offset=Offset(1, 2))
        Division((1, 8), start_offset=Offset(5, 8))
        Division((1, 8), start_offset=Offset(3, 4))

        Gets start offset of middle third:

        >>> parts[1][0].start_offset
        Offset(3, 8)

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None, *, start_offset=None) -> None:
        items = items or []
        if not isinstance(items, collections.abc.Iterable):
            items = [items]
        items = list(items)
        if start_offset is None and items:
            start_offset = getattr(items[0], "start_offset", None)
        if start_offset is not None:
            start_offset = abjad.Offset(start_offset)
        items_ = []
        for item in items:
            try:
                item = Division(item, start_offset=start_offset)
            except (TypeError, ValueError):
                item = DivisionSequence(item, start_offset=start_offset)
            start_offset = item.stop_offset
            items_.append(item)
        super().__init__(items=items_)

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self) -> abjad.Duration:
        """
        Gets duration.

        ..  container:: example

            >>> baca.DivisionSequence().duration
            Duration(0, 1)

            >>> baca.DivisionSequence([(2, 8), (2, 8), (2, 8)]).duration
            Duration(3, 4)

        """
        duration = sum(self.flatten(depth=-1))
        return abjad.Duration(duration)

    @property
    def start_offset(self) -> typing.Optional[abjad.Offset]:
        """
        Gets start offset.

        ..  container:: example

            >>> sequence = baca.DivisionSequence(
            ...     [(2, 8), (2, 8), (2, 8)],
            ...     start_offset=(1, 1),
            ...     )
            >>> sequence.start_offset
            Offset(1, 1)

        """
        if 0 < len(self):
            return self[0].start_offset
        return None

    @property
    def stop_offset(self) -> typing.Optional[abjad.Offset]:
        """
        Gets stop offset.

        ..  container:: example

            >>> sequence = baca.DivisionSequence(
            ...     [(2, 8), (2, 8), (2, 8)],
            ...     start_offset=(1, 1),
            ...     )
            >>> sequence.stop_offset
            Offset(7, 4)

        """
        if 0 < len(self):
            return self[-1].stop_offset
        return None

    @property
    def timespan(self) -> typing.Optional[abjad.Timespan]:
        """
        Gets timespan.

        ..  container:: example

            >>> sequence = baca.DivisionSequence(
            ...     [(2, 8), (2, 8), (2, 8)],
            ...     start_offset=(1, 1),
            ...     )
            >>> sequence.timespan
            Timespan(start_offset=Offset(1, 1), stop_offset=Offset(7, 4))

        """
        if self.start_offset is None:
            return None
        return abjad.Timespan(
            start_offset=self.start_offset, stop_offset=self.stop_offset
        )

    ### PUBLIC METHODS ###

    @abjad.Signature()
    def fuse(
        self, counts: typing.List[int] = None, *, cyclic: bool = None
    ) -> "DivisionSequence":
        r"""
        Fuses divisions by ``counts``.

        ..  container:: example expression

            Fuses divisions:

            >>> expression = baca.divisions().fuse()

            >>> input_divisions = [(7, 8), (3, 8), (5, 8)]
            >>> sequence = expression(input_divisions)
            >>> divisions = sequence.flatten(depth=-1)
            >>> divisions
            DivisionSequence([Division((15, 8))])

            >>> rhythm_maker = rmakers.NoteRhythmMaker()
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music, divisions)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 15/8
                        s1 * 15/8
                    }
                    \new RhythmicStaff
                    {
                        c'1...
                    }
                >>

        ..  container:: example expression

            Fuses first two divisions and then remaining divisions:

            >>> expression = baca.divisions().fuse([2])

            >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
            >>> sequence = expression(input_divisions)
            >>> sequence
            DivisionSequence([Division((4, 8)), Division((12, 8))])
            >>> rhythm_maker = rmakers.NoteRhythmMaker()
            >>> music = rhythm_maker(sequence)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 2/1
                        s1 * 2
                    }
                    \new RhythmicStaff
                    {
                        c'2
                        c'1.
                    }
                >>

        ..  container:: example expression

            Fuses divisions together two at a time:

            >>> expression = baca.divisions().fuse([2], cyclic=True)

            >>> input_divisions = [(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)]
            >>> sequence = expression(input_divisions)
            >>> sequence
            DivisionSequence([Division((4, 8)), Division((8, 8)), Division((2, 4))])

            >>> rhythm_maker = rmakers.NoteRhythmMaker()
            >>> music = rhythm_maker(sequence)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 2/1
                        s1 * 2
                    }
                    \new RhythmicStaff
                    {
                        c'2
                        c'1
                        c'2
                    }
                >>

        ..  container:: example expression

            Splits each division by ``3/8``;  then flattens; then fuses into
            differently sized groups:

            >>> expression = baca.divisions()
            >>> expression = expression.split_each(
            ...     [(3, 8)],
            ...     cyclic=True,
            ...     )
            >>> expression = expression.flatten(depth=-1)
            >>> expression = expression.fuse([2, 3, 1])

            >>> divisions = [(7, 8), (3, 8), (5, 8)]
            >>> divisions = [baca.Division(_) for _ in divisions]
            >>> divisions[0]._start_offset = abjad.Offset(1, 4)
            >>> sequence = expression(divisions)
            >>> for division in sequence:
            ...     division
            Division((6, 8), start_offset=Offset(1, 4))
            Division((7, 8), start_offset=Offset(1, 1))
            Division((2, 8), start_offset=Offset(15, 8))

            >>> rhythm_maker = rmakers.NoteRhythmMaker()
            >>> music = rhythm_maker(sequence)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 15/8
                        s1 * 15/8
                    }
                    \new RhythmicStaff
                    {
                        c'2.
                        c'2..
                        c'4
                    }
                >>

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        counts = counts or []
        sequence = self.partition_by_counts(
            counts, cyclic=cyclic, overhang=True
        )
        sequence = sequence.map(_divisions().sum())
        sequence = sequence.flatten(depth=-1)
        return sequence

    @abjad.Signature()
    def quarters_each(
        self,
        *,
        compound: abjad.DurationTyping = None,
        remainder: abjad.VerticalAlignment = None,
    ) -> "DivisionSequence":
        r"""
        Splits each division into quarters.

        ..  container:: example

            >>> expression = baca.divisions().quarters_each()
            >>> for item in expression([(2, 4), (6, 4)]):
            ...     item
            ...
            Division((1, 4))
            Division((1, 4))
            Division((1, 4))
            Division((1, 4))
            Division((1, 4))
            Division((1, 4))
            Division((1, 4))
            Division((1, 4))

        ..  container:: example

            >>> expression = baca.divisions().quarters_each(compound=(3, 2))
            >>> for item in expression([(2, 4), (6, 4)]):
            ...     item
            ...
            Division((1, 4))
            Division((1, 4))
            Division((3, 8))
            Division((3, 8))
            Division((3, 8))
            Division((3, 8))

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        sequence = self.split_each(
            [(1, 4)], compound=compound, cyclic=True, remainder=remainder
        )
        sequence = sequence.flatten(depth=-1)
        return sequence

    @abjad.Signature(is_operator=True, method_name="r", subscript="n")
    def rotate(self, n=0) -> "DivisionSequence":
        r"""
        Rotates division list by index ``n``.

        ..  container:: example

            Rotates divisions to the left:

            ..  container:: example

                >>> sequence = baca.DivisionSequence([
                ...     baca.Division((10, 16), start_offset=(0, 1)),
                ...     baca.Division((12, 16), start_offset=(5, 8)),
                ...     baca.Division((12, 16), start_offset=(11, 8)),
                ...     baca.Division((12, 16), start_offset=(17, 8)),
                ...     baca.Division((8, 16), start_offset=(23, 8)),
                ...     baca.Division((15, 16), start_offset=(27, 8)),
                ...     ])

                >>> for division in sequence.rotate(n=-1):
                ...     division
                ...
                Division((12, 16), start_offset=Offset(0, 1))
                Division((12, 16), start_offset=Offset(3, 4))
                Division((12, 16), start_offset=Offset(3, 2))
                Division((8, 16), start_offset=Offset(9, 4))
                Division((15, 16), start_offset=Offset(11, 4))
                Division((10, 16), start_offset=Offset(59, 16))

            ..  container:: example expression

                >>> expression = baca.divisions(name='J')
                >>> expression = expression.rotate(n=-1)

                >>> for division in expression(sequence):
                ...     division
                ...
                Division((12, 16), start_offset=Offset(0, 1))
                Division((12, 16), start_offset=Offset(3, 4))
                Division((12, 16), start_offset=Offset(3, 2))
                Division((8, 16), start_offset=Offset(9, 4))
                Division((15, 16), start_offset=Offset(11, 4))
                Division((10, 16), start_offset=Offset(59, 16))

                >>> expression.get_string()
                'r-1(J)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup) # doctest: +SKIP

                ..  docs::

                    >>> abjad.f(markup)
                    \markup {
                        \concat
                            {
                                r
                                \sub
                                    -1
                                \bold
                                    J
                            }
                        }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        start_offset = self.start_offset
        items = abjad.Sequence(self).rotate(n=n)
        return type(self)(items=items, start_offset=start_offset)

    @abjad.Signature()
    def split(
        self,
        durations: typing.List[abjad.DurationTyping],
        *,
        # TODO: maybe add back in?
        ###compound: abjad.DurationTyping = None,
        cyclic: bool = None,
        rotate_indexed: int = None,
        remainder: abjad.HorizontalAlignment = None,
        remainder_fuse_threshold: abjad.DurationTyping = None,
    ) -> "DivisionSequence":
        r"""
        Splits division list by ``durations``.

        ..  container:: example

            Splits every five sixteenths:

            >>> divisions = 10 * [(1, 8)]
            >>> sequence = baca.DivisionSequence(divisions, start_offset=0)

            >>> for division in sequence:
            ...     print(division)
            ...
            Division((1, 8), start_offset=Offset(0, 1))
            Division((1, 8), start_offset=Offset(1, 8))
            Division((1, 8), start_offset=Offset(1, 4))
            Division((1, 8), start_offset=Offset(3, 8))
            Division((1, 8), start_offset=Offset(1, 2))
            Division((1, 8), start_offset=Offset(5, 8))
            Division((1, 8), start_offset=Offset(3, 4))
            Division((1, 8), start_offset=Offset(7, 8))
            Division((1, 8), start_offset=Offset(1, 1))
            Division((1, 8), start_offset=Offset(9, 8))

            Splits division sequence every five sixteenths:

            >>> sequence = sequence.split([(5, 16)], cyclic=True)
            >>> for i, sequence_ in enumerate(sequence):
            ...     print(f"sequence {i}")
            ...     for division in sequence_:
            ...         print('\t' + str(division))
            ...
            sequence 0
                Division((1, 8), start_offset=Offset(0, 1))
                Division((1, 8), start_offset=Offset(1, 8))
                Division((1, 16), start_offset=Offset(1, 4))
            sequence 1
                Division((1, 16), start_offset=Offset(5, 16))
                Division((1, 8), start_offset=Offset(3, 8))
                Division((1, 8), start_offset=Offset(1, 2))
            sequence 2
                Division((1, 8), start_offset=Offset(5, 8))
                Division((1, 8), start_offset=Offset(3, 4))
                Division((1, 16), start_offset=Offset(7, 8))
            sequence 3
                Division((1, 16), start_offset=Offset(15, 16))
                Division((1, 8), start_offset=Offset(1, 1))
                Division((1, 8), start_offset=Offset(9, 8))

            Gets start offset of last sequence:

            >>> sequence[-1].start_offset
            Offset(15, 16)

            Gets start offset of first division in last sequence:

            >>> sequence[-1][0].start_offset
            Offset(15, 16)

        ..  container:: example expression

            Fuses divisions and then splits by ``1/4`` with remainder on right:

            >>> expression = baca.divisions().fuse()
            >>> expression = expression.split([(1, 4)], cyclic=True)

            >>> divisions = [(7, 8), (3, 8), (5, 8)]
            >>> input_divisions = baca.divisions(divisions, start_offset=0)
            >>> sequence = expression(input_divisions)
            >>> for item in sequence:
            ...     item
            DivisionSequence([Division((2, 8), start_offset=Offset(0, 1))])
            DivisionSequence([Division((2, 8), start_offset=Offset(1, 4))])
            DivisionSequence([Division((2, 8), start_offset=Offset(1, 2))])
            DivisionSequence([Division((2, 8), start_offset=Offset(3, 4))])
            DivisionSequence([Division((2, 8), start_offset=Offset(1, 1))])
            DivisionSequence([Division((2, 8), start_offset=Offset(5, 4))])
            DivisionSequence([Division((2, 8), start_offset=Offset(3, 2))])
            DivisionSequence([Division((1, 8), start_offset=Offset(7, 4))])

            >>> rhythm_maker = rmakers.NoteRhythmMaker()
            >>> divisions = sequence.flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 15/8
                        s1 * 15/8
                    }
                    \new RhythmicStaff
                    {
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'8
                    }
                >>

            Fuses remainder:

            >>> expression = baca.divisions().fuse()
            >>> expression = expression.split(
            ...     [(1, 4)], cyclic=True, remainder_fuse_threshold=(1, 8)
            ... )

            >>> divisions = [(7, 8), (3, 8), (5, 8)]
            >>> input_divisions = baca.divisions(divisions, start_offset=0)
            >>> sequence = expression(input_divisions)
            >>> for item in sequence:
            ...     item
            DivisionSequence([Division((2, 8), start_offset=Offset(0, 1))])
            DivisionSequence([Division((2, 8), start_offset=Offset(1, 4))])
            DivisionSequence([Division((2, 8), start_offset=Offset(1, 2))])
            DivisionSequence([Division((2, 8), start_offset=Offset(3, 4))])
            DivisionSequence([Division((2, 8), start_offset=Offset(1, 1))])
            DivisionSequence([Division((2, 8), start_offset=Offset(5, 4))])
            DivisionSequence([Division((3, 8), start_offset=Offset(3, 2))])

            >>> rhythm_maker = rmakers.NoteRhythmMaker()
            >>> divisions = sequence.flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 15/8
                        s1 * 15/8
                    }
                    \new RhythmicStaff
                    {
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4.
                    }
                >>

        ..  container:: example expression

            Fuses divisions and then splits by ``1/4`` with remainder on left:

            >>> expression = baca.divisions().fuse()
            >>> expression = expression.split(
            ...     [(1, 4)], cyclic=True, remainder=abjad.Left
            ... )

            >>> divisions = [(7, 8), (3, 8), (5, 8)]
            >>> input_divisions = baca.divisions(divisions, start_offset=0)
            >>> sequence = expression(input_divisions)
            >>> for item in sequence:
            ...     item
            DivisionSequence([Division((1, 8), start_offset=Offset(0, 1))])
            DivisionSequence([Division((2, 8), start_offset=Offset(1, 8))])
            DivisionSequence([Division((2, 8), start_offset=Offset(3, 8))])
            DivisionSequence([Division((2, 8), start_offset=Offset(5, 8))])
            DivisionSequence([Division((2, 8), start_offset=Offset(7, 8))])
            DivisionSequence([Division((2, 8), start_offset=Offset(9, 8))])
            DivisionSequence([Division((2, 8), start_offset=Offset(11, 8))])
            DivisionSequence([Division((2, 8), start_offset=Offset(13, 8))])

            >>> rhythm_maker = rmakers.NoteRhythmMaker()
            >>> divisions = sequence.flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 15/8
                        s1 * 15/8
                    }
                    \new RhythmicStaff
                    {
                        c'8
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                    }
                >>

            Fuses remainder:

            >>> expression = baca.divisions().fuse()
            >>> expression = expression.split(
            ...     [(1, 4)],
            ...     cyclic=True,
            ...     remainder=abjad.Left,
            ...     remainder_fuse_threshold=(1, 8),
            ... )

            >>> divisions = [(7, 8), (3, 8), (5, 8)]
            >>> input_divisions = baca.divisions(divisions, start_offset=0)
            >>> sequence = expression(input_divisions)
            >>> for item in sequence:
            ...     item
            DivisionSequence([Division((3, 8), start_offset=Offset(0, 1))])
            DivisionSequence([Division((2, 8), start_offset=Offset(3, 8))])
            DivisionSequence([Division((2, 8), start_offset=Offset(5, 8))])
            DivisionSequence([Division((2, 8), start_offset=Offset(7, 8))])
            DivisionSequence([Division((2, 8), start_offset=Offset(9, 8))])
            DivisionSequence([Division((2, 8), start_offset=Offset(11, 8))])
            DivisionSequence([Division((2, 8), start_offset=Offset(13, 8))])

            >>> rhythm_maker = rmakers.NoteRhythmMaker()
            >>> divisions = sequence.flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 15/8
                        s1 * 15/8
                    }
                    \new RhythmicStaff
                    {
                        c'4.
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                        c'4
                    }
                >>

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        durations = [abjad.Duration(_) for _ in durations]
        ###if compound is not None:
        ###    compound = abjad.Multiplier(compound)
        if cyclic is not None:
            cyclic = bool(cyclic)
        if rotate_indexed is not None:
            assert isinstance(rotate_indexed, int)
        if remainder is not None:
            assert remainder in (abjad.Left, abjad.Right), repr(remainder)
        if remainder_fuse_threshold is not None:
            remainder_fuse_threshold = abjad.Duration(remainder_fuse_threshold)
        start_offset = self.start_offset
        sequence = abjad.Sequence.split(
            self, durations, cyclic=cyclic, overhang=True
        )
        without_overhang = abjad.Sequence.split(
            self, durations, cyclic=cyclic, overhang=False
        )
        if sequence != without_overhang:
            items = list(sequence)
            remaining_item = items.pop()
            if remainder == abjad.Left:
                if remainder_fuse_threshold is None:
                    items.insert(0, remaining_item)
                elif remaining_item.duration <= remainder_fuse_threshold:
                    fused_value = DivisionSequence([remaining_item, items[0]])
                    fused_value = fused_value.flatten(depth=-1)
                    fused_value = fused_value.fuse()
                    items[0] = fused_value
                else:
                    items.insert(0, remaining_item)
            else:
                if remainder_fuse_threshold is None:
                    items.append(remaining_item)
                elif remaining_item.duration <= remainder_fuse_threshold:
                    fused_value = DivisionSequence([items[-1], remaining_item])
                    fused_value = fused_value.flatten(depth=-1)
                    fused_value = fused_value.fuse()
                    items[-1] = fused_value
                else:
                    items.append(remaining_item)
            sequence = DivisionSequence(items, start_offset=start_offset)
        return sequence

    @abjad.Signature()
    def split_each(
        self,
        durations: typing.List[abjad.DurationTyping],
        *,
        compound: abjad.DurationTyping = None,
        cyclic: bool = None,
        rotate_indexed: int = None,
        remainder: abjad.HorizontalAlignment = None,
        remainder_fuse_threshold: abjad.DurationTyping = None,
    ) -> "DivisionSequence":
        r"""
        Splits each division by ``durations``.

        ..  container:: example expression

            Splits each division into quarters and positions remainder at
            right:

            >>> expression = baca.divisions()
            >>> expression = expression.split_each(
            ...     [(1, 4)],
            ...     cyclic=True,
            ...     )

            >>> input_divisions = [(7, 8), (7, 8), (7, 16)]
            >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
            >>> sequence = expression(time_signatures)
            >>> for sequence_ in sequence:
            ...     sequence_
            DivisionSequence([Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 8))])
            DivisionSequence([Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 8))])
            DivisionSequence([Division((1, 4)), Division((3, 16))])

            >>> rhythm_maker = rmakers.NoteRhythmMaker()
            >>> divisions = sequence.flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music, input_divisions)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 7/8
                        s1 * 7/8
                        \time 7/8
                        s1 * 7/8
                        \time 7/16
                        s1 * 7/16
                    }
                    \new RhythmicStaff
                    {
                        c'4
                        c'4
                        c'4
                        c'8
                        c'4
                        c'4
                        c'4
                        c'8
                        c'4
                        c'8.
                    }
                >>

        ..  container:: example expression

            Splits each division into quarters and positions remainder at left:

            >>> expression = baca.divisions()
            >>> expression = expression.split_each(
            ...     [(1, 4)],
            ...     cyclic=True,
            ...     remainder=abjad.Left,
            ...     )

            >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
            >>> sequence = expression(time_signatures)
            >>> for sequence_ in sequence:
            ...     sequence_
            DivisionSequence([Division((1, 8)), Division((1, 4)), Division((1, 4)), Division((1, 4))])
            DivisionSequence([Division((1, 8)), Division((1, 4)), Division((1, 4)), Division((1, 4))])
            DivisionSequence([Division((3, 16)), Division((1, 4))])

            >>> rhythm_maker = rmakers.NoteRhythmMaker()
            >>> divisions = sequence.flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music, input_divisions)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 7/8
                        s1 * 7/8
                        \time 7/8
                        s1 * 7/8
                        \time 7/16
                        s1 * 7/16
                    }
                    \new RhythmicStaff
                    {
                        c'8
                        c'4
                        c'4
                        c'4
                        c'8
                        c'4
                        c'4
                        c'4
                        c'8.
                        c'4
                    }
                >>

        ..  container:: example expression

            Splits each division into quarters and fuses remainder less than or
            equal to ``1/8`` to the right:

            >>> expression = baca.divisions()
            >>> expression = expression.split_each(
            ...     [(1, 4)],
            ...     cyclic=True,
            ...     remainder_fuse_threshold=(1, 8),
            ...     )

            >>> time_signatures = [(5, 8)]
            >>> sequence = expression(time_signatures)
            >>> for sequence_ in sequence:
            ...     sequence_
            ...
            DivisionSequence([Division((1, 4)), Division((3, 8))])

            >>> rhythm_maker = rmakers.NoteRhythmMaker()
            >>> divisions = sequence.flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music, time_signatures)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 5/8
                        s1 * 5/8
                    }
                    \new RhythmicStaff
                    {
                        c'4
                        c'4.
                    }
                >>

        ..  container:: example expression

            Splits each division into quarters and fuses remainder less than or
            equal to ``1/8`` to the left:

            >>> expression = baca.divisions()
            >>> expression = expression.split_each(
            ...     [(1, 4)],
            ...     cyclic=True,
            ...     remainder=abjad.Left,
            ...     remainder_fuse_threshold=(1, 8),
            ...     )

            >>> time_signatures = [(5, 8)]
            >>> sequence = expression(time_signatures)
            >>> for sequence_ in sequence:
            ...     sequence_
            ...
            DivisionSequence([Division((3, 8)), Division((1, 4))])

            >>> rhythm_maker = rmakers.NoteRhythmMaker()
            >>> divisions = sequence.flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music, time_signatures)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 5/8
                        s1 * 5/8
                    }
                    \new RhythmicStaff
                    {
                        c'4.
                        c'4
                    }
                >>

            Works with start offset:

            >>> expression = baca.divisions()
            >>> expression = expression.ratios_each(
            ...     ratios=[abjad.Ratio([1, 1])],
            ...     )

            >>> divisions = [(7, 4), (6, 4)]
            >>> divisions = [baca.Division(_) for _ in divisions]
            >>> divisions[0]._start_offset = abjad.Offset(1, 4)
            >>> divisions
            [Division((7, 4), start_offset=Offset(1, 4)), Division((6, 4))]

            >>> sequence = expression(divisions)
            >>> len(sequence)
            2

            >>> for division in sequence[0]:
            ...     division
            ...
            Division((4, 4), start_offset=Offset(1, 4))
            Division((3, 4), start_offset=Offset(5, 4))

            >>> for division in sequence[1]:
            ...     division
            ...
            Division((3, 4), start_offset=Offset(2, 1))
            Division((3, 4), start_offset=Offset(11, 4))

        ..  container:: example expression

            Splits each division by durations and rotates durations one to the
            left at each new division:

            >>> expression = baca.divisions()
            >>> expression = expression.split_each(
            ...     [(1, 16), (1, 8), (1, 4)],
            ...     cyclic=True,
            ...     rotate_indexed=-1,
            ...     )

            >>> time_signatures = [(7, 16), (7, 16), (7, 16)]
            >>> sequence = expression([(7, 16), (7, 16), (7, 16)])
            >>> for sequence_ in sequence:
            ...     sequence_
            ...
            DivisionSequence([Division((1, 16)), Division((1, 8)), Division((1, 4))])
            DivisionSequence([Division((1, 8)), Division((1, 4)), Division((1, 16))])
            DivisionSequence([Division((1, 4)), Division((1, 16)), Division((1, 8))])

            >>> rhythm_maker = rmakers.NoteRhythmMaker()
            >>> divisions = sequence.flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music, time_signatures)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 7/16
                        s1 * 7/16
                        \time 7/16
                        s1 * 7/16
                        \time 7/16
                        s1 * 7/16
                    }
                    \new RhythmicStaff
                    {
                        c'16
                        c'8
                        c'4
                        c'8
                        c'4
                        c'16
                        c'4
                        c'16
                        c'8
                    }
                >>

        ..  container:: example expression

            Splits each division into compound quarters:

            >>> expression = baca.divisions()
            >>> expression = expression.split_each(
            ...     [(1, 4)],
            ...     compound=(3, 2),
            ...     cyclic=True,
            ...     )

            >>> time_signatures = [(3, 4), (6, 8)]
            >>> sequence = expression(time_signatures)
            >>> for sequence_ in sequence:
            ...     sequence_
            ...
            DivisionSequence([Division((1, 4)), Division((1, 4)), Division((1, 4))])
            DivisionSequence([Division((3, 8)), Division((3, 8))])

            >>> rhythm_maker = rmakers.NoteRhythmMaker()
            >>> divisions = sequence.flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music, time_signatures)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 3/4
                        s1 * 3/4
                        \time 6/8
                        s1 * 3/4
                    }
                    \new RhythmicStaff
                    {
                        c'4
                        c'4
                        c'4
                        c'4.
                        c'4.
                    }
                >>

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        durations = [abjad.Duration(_) for _ in durations]
        if compound is not None:
            compound = abjad.Multiplier(compound)
        if cyclic is not None:
            cyclic = bool(cyclic)
        if rotate_indexed is not None:
            assert isinstance(rotate_indexed, int)
        if remainder is not None:
            assert remainder in (abjad.Left, abjad.Right), repr(remainder)
        if remainder_fuse_threshold is not None:
            remainder_fuse_threshold = abjad.Duration(remainder_fuse_threshold)
        start_offset = self[0].start_offset
        sequences = []
        rotate_indexed = rotate_indexed or 0
        for i, division in enumerate(self):
            input_division = Division(division)
            input_duration = abjad.Duration(division)
            input_meter = abjad.Meter(division)
            assert 0 < input_division, repr(input_division)
            if not durations:
                sequence = DivisionSequence([input_division])
                sequences.append(sequence)
                continue
            if input_meter.is_simple or not durations:
                durations_ = durations[:]
            elif input_meter.is_compound:
                multiplier = compound or 1
                durations_ = [
                    abjad.Duration(multiplier * _) for _ in durations
                ]
            else:
                raise Exception
            n = i * rotate_indexed
            divisions_ = classes.Sequence(durations_).rotate(n=n)
            if cyclic:
                divisions_ = divisions_.repeat_to_weight(
                    input_division, allow_total=abjad.Less
                )
            divisions = list(divisions_)
            total_duration = abjad.Duration(sum(divisions))
            if total_duration == input_duration:
                sequence = DivisionSequence(divisions)
                sequences.append(sequence)
                continue
            remaining_division = input_division - total_duration
            remaining_division = Division(remaining_division)
            if remainder == abjad.Left:
                if remainder_fuse_threshold is None:
                    divisions.insert(0, remaining_division)
                elif remaining_division <= remainder_fuse_threshold:
                    fused_value = divisions[0] + remaining_division
                    fused_value = Division(fused_value)
                    divisions[0] = fused_value
                else:
                    divisions.insert(0, remaining_division)
            else:
                if remainder_fuse_threshold is None:
                    divisions.append(remaining_division)
                elif remaining_division <= remainder_fuse_threshold:
                    fused_value = divisions[-1] + remaining_division
                    fused_value = Division(fused_value)
                    divisions[-1] = fused_value
                else:
                    divisions.append(remaining_division)
            total_duration = abjad.Duration(sum(divisions))
            pair = total_duration, input_duration
            assert total_duration == input_duration, pair
            sequence = DivisionSequence(divisions)
            sequences.append(sequence)
        for _ in sequences:
            assert isinstance(_, DivisionSequence), repr(_)
        sequence = DivisionSequence(sequences, start_offset=start_offset)
        return sequence

    @abjad.Signature()
    def ratios_each(self, ratios) -> "DivisionSequence":
        r"""
        Splits each division by rounded ``ratios``.

        ..  container:: example expression

            Splits each division by ``2:1`` rounded ratio:

            >>> expression = baca.divisions()
            >>> expression = expression.ratios_each([(2, 1)])

            >>> input_divisions = [(5, 8), (6, 8)]
            >>> sequence = expression(input_divisions)
            >>> for sequence_ in sequence:
            ...     sequence_
            DivisionSequence([Division((3, 8)), Division((2, 8))])
            DivisionSequence([Division((4, 8)), Division((2, 8))])

            >>> rhythm_maker = rmakers.NoteRhythmMaker()
            >>> divisions = sequence.flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music, input_divisions)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 5/8
                        s1 * 5/8
                        \time 6/8
                        s1 * 3/4
                    }
                    \new RhythmicStaff
                    {
                        c'4.
                        c'4
                        c'2
                        c'4
                    }
                >>

        ..  container:: example expression

            Splits divisions with alternating ``2:1`` and ``1:1:1`` rounded
            ratios:

            >>> expression = baca.divisions()
            >>> expression = expression.ratios_each(
            ...     [(2, 1), (1, 1, 1)]
            ... )

            >>> input_divisions = [(5, 8), (6, 8)]
            >>> sequence = expression(input_divisions)
            >>> for sequence_ in sequence:
            ...     sequence_
            DivisionSequence([Division((3, 8)), Division((2, 8))])
            DivisionSequence([Division((2, 8)), Division((2, 8)), Division((2, 8))])

            >>> rhythm_maker = rmakers.NoteRhythmMaker()
            >>> divisions = sequence.flatten(depth=-1)
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music, input_divisions)
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 5/8
                        s1 * 5/8
                        \time 6/8
                        s1 * 3/4
                    }
                    \new RhythmicStaff
                    {
                        c'4.
                        c'4
                        c'4
                        c'4
                        c'4
                    }
                >>

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        start_offset = self[0].start_offset
        sequences = []
        if not ratios:
            ratios = (abjad.Ratio([1]),)
        ratios = abjad.CyclicTuple(ratios)
        for i, division in enumerate(self):
            ratio = ratios[i]
            numerators = abjad.mathtools.partition_integer_by_ratio(
                division.numerator, ratio
            )
            divisions = [
                Division((numerator, division.denominator))
                for numerator in numerators
            ]
            sequence = DivisionSequence(divisions)
            sequences.append(sequence)
        sequence = DivisionSequence(sequences, start_offset=start_offset)
        return sequence


### EXPRESSION CONSTRUCTORS ###


def _divisions(items=None, **keywords):
    if items:
        return DivisionSequence(items=items, **keywords)
    name = keywords.pop("name", None)
    expression = classes.Expression(name=name)
    callback = expression._make_initializer_callback(
        DivisionSequence,
        module_names=["baca"],
        string_template="{}",
        **keywords,
    )
    expression = expression.append_callback(callback)
    return abjad.new(expression, proxy_class=DivisionSequence)
