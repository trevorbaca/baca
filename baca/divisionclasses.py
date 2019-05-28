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

        Division with duration, start offset and payload:

        >>> division = baca.Division(
        ...     (3, 8),
        ...     payload=rmakers.NoteRhythmMaker(),
        ...     start_offset=abjad.Offset((5, 4)),
        ...     )

    ..  container:: example

        Division with duration and start offset:

        >>> division = baca.Division(
        ...     (3, 8),
        ...     start_offset=abjad.Offset((5, 4)),
        ...     )

        >>> abjad.f(division, strict=89)
        baca.Division(
            (3, 8),
            start_offset=abjad.Offset(5, 4),
            )

    ..  container:: example

        Division with duration:

        >>> division = baca.Division((3, 8))

        >>> abjad.f(division, strict=89)
        baca.Division(
            (3, 8)
            )

    ..  container:: example

        Initializes from other division:

        >>> division = baca.Division(
        ...     (3, 8),
        ...     payload=rmakers.NoteRhythmMaker(),
        ...     start_offset=abjad.Offset((5, 4)),
        ...     )
        >>> new_division = baca.Division(division)
        >>> division == new_division
        True

    ..  container:: example

        Initializes from nonreduced fraction:

        >>> fraction = abjad.NonreducedFraction((6, 4))
        >>> division = baca.Division(
        ...     fraction,
        ...     payload=rmakers.NoteRhythmMaker(),
        ...     start_offset=abjad.Offset((5, 4)),
        ...     )
        >>> new_division = baca.Division(division)
        >>> division == new_division
        True

    ..  container:: example

        Empty initialization:

        >>> division = baca.Division()

        >>> abjad.f(division, strict=89)
        baca.Division(
            (0, 1)
            )

    ..  container:: example

        Makes divisions from durations:

        >>> durations = 10 * [abjad.Duration(1, 8)]
        >>> start_offsets = abjad.mathtools.cumulative_sums(durations)[:-1]
        >>> divisions = []
        >>> for duration, start_offset in zip(durations, start_offsets):
        ...     division = baca.Division(
        ...         duration,
        ...         start_offset=start_offset,
        ...         )
        ...     divisions.append(division)
        >>> divisions = abjad.Sequence(divisions)

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

    ..  container:: example

        Makes divisions from durations:

        >>> durations = 10 * [abjad.Duration(1, 8)]
        >>> start_offsets = abjad.mathtools.cumulative_sums(durations)[:-1]
        >>> divisions = []
        >>> for duration, start_offset in zip(durations, start_offsets):
        ...     division = baca.Division(
        ...         duration,
        ...         start_offset=start_offset,
        ...         )
        ...     divisions.append(division)
        >>> divisions = abjad.Sequence(divisions)

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

        Splits divisions every five sixteenths:

        >>> parts = divisions.split([abjad.Fraction(5, 16)], cyclic=True)
        >>> for i, part in enumerate(parts):
        ...     message = 'part {}'.format(i)
        ...     print(message)
        ...     for division in part:
        ...         print('\t' + str(division))
        ...
        part 0
            Division((1, 8), start_offset=Offset(0, 1))
            Division((1, 8), start_offset=Offset(1, 8))
            Division((1, 16), start_offset=Offset(1, 4))
        part 1
            Division((1, 16), start_offset=Offset(5, 16))
            Division((1, 8), start_offset=Offset(3, 8))
            Division((1, 8), start_offset=Offset(1, 2))
        part 2
            Division((1, 8), start_offset=Offset(5, 8))
            Division((1, 8), start_offset=Offset(3, 4))
            Division((1, 16), start_offset=Offset(7, 8))
        part 3
            Division((1, 16), start_offset=Offset(15, 16))
            Division((1, 8), start_offset=Offset(1, 1))
            Division((1, 8), start_offset=Offset(9, 8))

        Gets start offset of first division of last part:

        >>> parts[-1][0].start_offset
        Offset(15, 16)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_payload", "_start_offset")

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, *arguments, **keywords) -> None:
        """
        Dummy initializer to satisfy mypy.
        """
        pass

    def __new__(class_, argument=None, payload=None, start_offset=None):
        argument = argument or (0, 1)
        if isinstance(argument, str):
            division = eval(argument)
            argument = division
            if payload is None:
                payload = argument.payload
            if start_offset is None:
                start_offset = argument.start_offset
        if isinstance(argument, abjad.NonreducedFraction):
            if payload is None:
                payload = getattr(argument, "payload", None)
            if start_offset is None:
                start_offset = getattr(argument, "start_offset", None)
        self = abjad.NonreducedFraction.__new__(class_, argument)
        self._payload = payload
        if start_offset is not None:
            start_offset = abjad.Offset(start_offset)
        self._start_offset = start_offset
        return self

    ### SPECIAL METHODS###

    def __add__(self, argument):
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

            >>> division_1 = baca.Division(
            ...     (2, 4),
            ...     start_offset=abjad.Offset(1),
            ...     )
            >>> division_2 = baca.Division((4, 4))
            >>> division_1 + division_2
            Division((6, 4), start_offset=Offset(1, 1))

        ..  container:: example

            Contiguous start offsets:

            >>> division_1 = baca.Division(
            ...     (2, 4),
            ...     start_offset=abjad.Offset(1),
            ...     )
            >>> division_2 = baca.Division(
            ...     (4, 4),
            ...     start_offset=abjad.Offset((3, 2)),
            ...     )
            >>> division_1 + division_2
            Division((6, 4), start_offset=Offset(1, 1))

        ..  container:: example

            Noncontiguous start offsets:

            >>> division_1 = baca.Division(
            ...     (2, 4),
            ...     start_offset=abjad.Offset(1),
            ...     )
            >>> division_2 = baca.Division(
            ...     (4, 4),
            ...     start_offset=abjad.Offset(10),
            ...     )
            >>> division_1 + division_2
            Division((40, 4), start_offset=Offset(1, 1))

        ..  container:: example

            Identical start offsets:

            >>> division_1 = baca.Division(
            ...     (2, 4),
            ...     start_offset=abjad.Offset(1),
            ...     )
            >>> division_2 = baca.Division(
            ...     (4, 4),
            ...     start_offset=abjad.Offset(1),
            ...     )
            >>> division_1 + division_2
            Division((4, 4), start_offset=Offset(1, 1))

        ..  container:: example

            Overlapping start offsets:

            >>> division_1 = baca.Division(
            ...     (2, 4),
            ...     start_offset=abjad.Offset(1),
            ...     )
            >>> division_2 = baca.Division(
            ...     (4, 4),
            ...     start_offset=abjad.Offset((5, 4)),
            ...     )
            >>> division_1 + division_2
            Division((5, 4), start_offset=Offset(1, 1))

        Returns new division.
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

    def __copy__(self, *arguments):
        """
        Copies division.

        Returns new division.
        """
        arguments = self.__getnewargs__()
        return type(self)(*arguments)

    def __deepcopy__(self, *arguments):
        """
        Deep copies division.

        Returns new division.
        """
        return self.__copy__(*arguments)

    def __getnewargs__(self):
        """
        Gets new arguments.

        Returns tuple.
        """
        return (self.pair, self.payload, self.start_offset)

    def __str__(self):
        """
        Gets string representation of division.

        Returns string.
        """
        return repr(self)

    def __sub__(self, argument):
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

            >>> division_1 = baca.Division(
            ...     (4, 1),
            ...     start_offset=abjad.Offset(10),
            ...     )
            >>> division_2 = baca.Division(
            ...     (2, 1),
            ...     start_offset=abjad.Offset(10),
            ...     )

            >>> division_1 - division_2
            Division((2, 1), start_offset=Offset(12, 1))

            >>> division_2 - division_1
            Division((-2, 1), start_offset=Offset(12, 1))

        ..  container:: example

            Overlapping timespans that start at different times:

            >>> division_1 = baca.Division(
            ...     (4, 1),
            ...     start_offset=abjad.Offset(10),
            ...     )
            >>> division_2 = baca.Division(
            ...     (4, 1),
            ...     start_offset=abjad.Offset(12),
            ...     )

            >>> division_1 - division_2
            Division((2, 1), start_offset=Offset(10, 1))

            >>> division_2 - division_1
            Division((2, 1), start_offset=Offset(14, 1))

        ..  container:: example

            Nonoverlapping timespans:

            >>> division_1 = baca.Division(
            ...     (6, 2),
            ...     start_offset=abjad.Offset(0),
            ...     )
            >>> division_2 = baca.Division(
            ...     (4, 2),
            ...     start_offset=abjad.Offset(20),
            ...     )

            >>> division_1 - division_2
            Division((6, 2), start_offset=Offset(0, 1))

            >>> division_2 - division_1
            Division((4, 2), start_offset=Offset(20, 1))

        ..  container:: example exception

             Raises exception when one division has a start offset and the
             other does not:

            >>> division_1 = baca.Division(
            ...     (6, 4),
            ...     start_offset=abjad.Offset(5),
            ...     )
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

        Returns new division.
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
        my_timespan = self._to_timespan()
        expr_timespan = argument._to_timespan()
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
            storage_format_kwargs_names=["payload", "start_offset"],
        )

    def _to_timespan(self):
        if self.start_offset is None:
            raise Exception(f"division must have start offset: {self!r}.")
        stop_offset = self.start_offset + self
        return abjad.Timespan(
            start_offset=self.start_offset, stop_offset=stop_offset
        )

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        """
        Gets duration of division.

        ..  container:: example

            Gets duration:

            >>> division = baca.Division((3, 8))

            >>> division.duration
            Duration(3, 8)

        ..  container:: example

            Gets duration:

            >>> division = baca.Division((6, 4))

            >>> division.duration
            Duration(3, 2)

        Returns duration.
        """
        return abjad.Duration(self)

    @property
    def payload(self):
        """
        Gets payload of division.

        ..  container:: example

            Division with payload:

            >>> division = baca.Division(
            ...     (3, 8),
            ...     payload=rmakers.NoteRhythmMaker(),
            ...     start_offset=abjad.Offset((5, 4)),
            ...     )

            >>> division.payload
            NoteRhythmMaker()

        ..  container:: example

            Division without duration:

            >>> division = baca.Division(
            ...     (3, 8),
            ...     start_offset=abjad.Offset((5, 4)),
            ...     )

            >>> division.payload is None
            True

        Set to object or none.

        Defaults to none.

        Returns object or none.
        """
        return self._payload

    @property
    def start_offset(self):
        """
        Gets start offset of division.

        ..  container:: example

            Division with start offset:

            >>> division = baca.Division(
            ...     (3, 8),
            ...     start_offset=abjad.Offset((5, 4)),
            ...     )

            >>> division.start_offset
            Offset(5, 4)

        ..  container:: example

            Division without start offset:

            >>> division = baca.Division((3, 8))

            >>> division.start_offset is None
            True

        Set to offset or none.

        Defaults to none.

        Returns offset or none.
        """
        return self._start_offset

    @property
    def stop_offset(self):
        """
        Gets stop offset of division.

        ..  container:: example

            Division with start offset:

            >>> division = baca.Division(
            ...     (3, 8),
            ...     start_offset=abjad.Offset((5, 4)),
            ...     )

            >>> division.stop_offset
            Offset(13, 8)

        ..  container:: example

            Division without start offset:

            >>> division = baca.Division((3, 8))

            >>> division.stop_offset is None
            True

            Returns none when start offset is none.

        Returns offset or none.
        """
        if self.start_offset is None:
            return
        return self.start_offset + self.duration

    ### PUBLIC METHODS ###

    @staticmethod
    def yield_durations(unique=False):
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

        Returns generator.
        """
        generator = Division.yield_nonreduced_fractions()
        while True:
            integer_pair = next(generator)
            duration = abjad.Duration(integer_pair)
            if not unique:
                yield duration
            elif duration.pair == integer_pair:
                yield duration

    def yield_equivalent_durations(self, minimum_written_duration=None):
        """
        Yields all durations equivalent to this duration.

        Returns output in Cantor diagonalized order.

        Ensures written duration never less than ``minimum_written_duration``.

        ..  container:: example

            Yields durations equivalent to ``1/8``:

            >>> pairs = baca.Division(1, 8).yield_equivalent_durations()
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

            Yields durations equivalent to ``1/12``:

            >>> pairs = baca.Division(1, 12).yield_equivalent_durations()
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

            Yields durations equivalent to ``5/48``:

            >>> pairs = baca.Division(5, 48).yield_equivalent_durations()
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

        Defaults ``minimum_written_duration`` to ``1/128``.

        Returns generator.
        """
        duration = abjad.Duration(self)
        if minimum_written_duration is None:
            minimum_written_duration = type(duration)(1, 128)
        else:
            minimum_written_duration = type(duration)(minimum_written_duration)
        generator = type(self).yield_durations(unique=True)
        pairs = []
        while True:
            written_duration = next(generator)
            if not written_duration.is_assignable:
                continue
            if written_duration < minimum_written_duration:
                pairs = tuple(pairs)
                return pairs
            prolation = duration / written_duration
            if prolation.normalized():
                pair = (prolation, written_duration)
                pairs.append(pair)

    @staticmethod
    def yield_nonreduced_fractions():
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

        Returns generator.
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

        Makes quarter-valued divisions with remainder at right:

        >>> expression = baca.divisions()
        >>> expression = expression.split_each_by_durations(
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

    ..  container:: example

        Makes quarter-valued divisions with remainder at left:

        >>> expression = baca.divisions()
        >>> expression = expression.split_each_by_durations(
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

    ..  container:: example

        Splits every division by ``1/4`` with remainder at right:

        >>> expression = baca.divisions()
        >>> expression = expression.split_each_by_durations(
        ...     [(1, 4)],
        ...     cyclic=True,
        ...     )

        >>> input_divisions = [(7, 8), (3, 8), (5, 8)]
        >>> sequence = expression(input_divisions)
        >>> for sequence_ in sequence:
        ...     sequence_
        DivisionSequence([Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 8))])
        DivisionSequence([Division((1, 4)), Division((1, 8))])
        DivisionSequence([Division((1, 4)), Division((1, 4)), Division((1, 8))])

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
                    \time 3/8
                    s1 * 3/8
                    \time 5/8
                    s1 * 5/8
                }
                \new RhythmicStaff
                {
                    c'4
                    c'4
                    c'4
                    c'8
                    c'4
                    c'8
                    c'4
                    c'4
                    c'8
                }
            >>

    ..  container:: example

        Fuses divisions:

        >>> expression = baca.divisions()
        >>> expression = expression.sum()
        >>> expression = expression.divisions()

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

        Fuses divisions and then splits by ``1/4`` with remainder on right:

        >>> expression = baca.divisions()
        >>> expression = expression.sum()
        >>> expression = expression.divisions()
        >>> expression = expression.split_each_by_durations(
        ...     [(1, 4)],
        ...     cyclic=True,
        ...     )

        >>> input_divisions = [(7, 8), (3, 8), (5, 8)]
        >>> sequence = expression(input_divisions)
        >>> for sequence_ in sequence:
        ...     sequence_
        DivisionSequence([Division((1, 4)), Division((1, 4)), Division((1, 4)),
        Division((1, 4)), Division((1, 4)), Division((1, 4)), Division((1, 4)),
        Division((1, 8))])

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

    ..  container:: example

        Fuses divisions together two at a time:

        >>> expression = baca.divisions()
        >>> expression = expression.partition_by_counts(
        ...     counts=[2],
        ...     cyclic=True,
        ...     overhang=True,
        ...     )
        >>> expression = expression.map(baca.sequence().sum())

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

    ..  container:: example

        Splits every division by ``3/8``:

        >>> expression = baca.divisions()
        >>> expression = expression.split_each_by_durations(
        ...     [(3, 8)],
        ...     cyclic=True,
        ...     )

        >>> input_divisions = [(7, 8), (3, 8), (5, 8)]
        >>> sequence = expression(input_divisions)
        >>> for sequence_ in sequence:
        ...     sequence_
        DivisionSequence([Division((3, 8)), Division((3, 8)), Division((1, 8))])
        DivisionSequence([Division((3, 8))])
        DivisionSequence([Division((3, 8)), Division((2, 8))])

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
                    \time 3/8
                    s1 * 3/8
                    \time 5/8
                    s1 * 5/8
                }
                \new RhythmicStaff
                {
                    c'4.
                    c'4.
                    c'8
                    c'4.
                    c'4.
                    c'4
                }
            >>

        Splits every division by ``3/8`` and then fuses flattened divisions
        into differently sized groups:

        >>> expression = baca.divisions()
        >>> expression = expression.split_each_by_durations(
        ...     [(3, 8)],
        ...     cyclic=True,
        ...     )
        >>> expression = expression.flatten(depth=-1)
        >>> expression = expression.partition_by_counts(counts=[2, 3, 1])
        >>> expression = expression.map(baca.sequence().sum())

        >>> input_divisions = [(7, 8), (3, 8), (5, 8)]
        >>> sequence = expression(input_divisions)
        >>> sequence
        DivisionSequence([Division((6, 8)), Division((7, 8)), Division((2, 8))])

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

    ..  container:: example

        Splits every division by ``3/8`` and then fuses flattened divisions
        into differently sized groups. Works with start offset:

        >>> expression = baca.divisions()
        >>> expression = expression.split_each_by_durations(
        ...     [(3, 8)],
        ...     cyclic=True,
        ...     )
        >>> expression = expression.flatten(depth=-1)
        >>> expression = expression.partition_by_counts(counts=[2, 3, 1])
        >>> expression = expression.map(baca.sequence().sum())

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

    ..  container:: example

        Makes divisions with ``2:1`` ratios:

        >>> expression = baca.divisions()
        >>> expression = expression.split_each_by_rounded_ratios(
        ...     ratios=[abjad.Ratio([2, 1])],
        ...     )

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

    ..  container:: example

        Makes divisions with alternating ``2:1`` and ``1:1:1`` ratios:

        >>> expression = baca.divisions()
        >>> expression = expression.split_each_by_rounded_ratios(
        ...     ratios=[
        ...         abjad.Ratio([2, 1]),
        ...         abjad.Ratio([1, 1, 1]),
        ...         ],
        ...     )

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

    ..  container:: example

        Compound meter multiplier equal to ``3/2``:

        >>> expression = baca.divisions()
        >>> expression = expression.split_each_by_durations(
        ...     [(1, 4)],
        ...     compound_meter_multiplier=abjad.Multiplier(3, 2),
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

    ..  container:: example

        Rotates durations one element to the left on each new input
        division:

        >>> expression = baca.divisions()
        >>> expression = expression.split_each_by_durations(
        ...     [(1, 16), (1, 8), (1, 4)],
        ...     cyclic=True,
        ...     pattern_rotation_index=-1,
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

    ..  container:: example

        Rotates durations one element to the right on each new input
        division:

        >>> expression = baca.divisions()
        >>> expression = expression.split_each_by_durations(
        ...     [(1, 16), (1, 8), (1, 4)],
        ...     cyclic=True,
        ...     pattern_rotation_index=1,
        ...     )

        >>> time_signatures = [(7, 16), (7, 16), (7, 16)]
        >>> sequence = expression(time_signatures)
        >>> for sequence_ in sequence:
        ...     sequence_
        ...
        DivisionSequence([Division((1, 16)), Division((1, 8)), Division((1, 4))])
        DivisionSequence([Division((1, 4)), Division((1, 16)), Division((1, 8))])
        DivisionSequence([Division((1, 8)), Division((1, 4)), Division((1, 16))])

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
                    c'4
                    c'16
                    c'8
                    c'8
                    c'4
                    c'16
                }
            >>

    ..  container:: example

        Remainder less than or equal to ``1/8`` fused to the right:

        >>> expression = baca.divisions()
        >>> expression = expression.split_each_by_durations(
        ...     [(1, 4)],
        ...     cyclic=True,
        ...     remainder_fuse_threshold=abjad.Duration(1, 8),
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

    ..  container:: example

        Remainder less than or equal to ``1/8`` fused to the left:

        >>> expression = baca.divisions()
        >>> expression = expression.split_each_by_durations(
        ...     [(1, 4)],
        ...     cyclic=True,
        ...     remainder=abjad.Left,
        ...     remainder_fuse_threshold=abjad.Duration(1, 8),
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

    ..  container:: example

        Works with start offset:

        >>> expression = baca.divisions()
        >>> expression = expression.split_each_by_rounded_ratios(
        ...     ratios=[abjad.Ratio([1, 1])],
        ...     )

        >>> divisions = [(7, 4), (6, 4)]
        >>> divisions = [baca.Division(_) for _ in divisions]
        >>> divisions[0]._start_offset = abjad.Offset(1, 4)
        >>> divisions
        [Division((7, 4), start_offset=Offset(1, 4)), Division((6, 4))]

        >>> division_lists = expression(divisions)
        >>> len(division_lists)
        2

        >>> for division in division_lists[0]:
        ...     division
        ...
        Division((4, 4), start_offset=Offset(1, 4))
        Division((3, 4), start_offset=Offset(5, 4))

        >>> for division in division_lists[1]:
        ...     division
        ...
        Division((3, 4), start_offset=Offset(2, 1))
        Division((3, 4), start_offset=Offset(11, 4))

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None) -> None:
        items = items or []
        if not isinstance(items, collections.abc.Iterable):
            items = [items]
        items_ = []
        for item in items:
            try:
                item = Division(item)
            except (TypeError, ValueError):
                pass
            items_.append(item)
        super().__init__(items=items_)

    ### PRIVATE METHODS ###

    def _get_ratios(self, ratios):
        if not ratios:
            ratios = (abjad.Ratio([1]),)
        ratios = abjad.CyclicTuple(ratios)
        return ratios

    def _split_each_by_durations(
        self,
        divisions,
        self_durations,
        *,
        self_cyclic=None,
        self_compound_meter_multiplier=None,
        self_pattern_rotation_index=None,
        self_remainder_direction=None,
        self_remainder_fuse_threshold=None,
    ):
        divisions = divisions or []
        if not divisions:
            return divisions
        divisions, start_offset = self._to_divisions(divisions)
        start_offset = divisions[0].start_offset
        division_lists = []
        for i, division in enumerate(divisions):
            input_division = Division(division)
            input_duration = abjad.Duration(input_division)
            input_meter = abjad.Meter(input_division)
            assert 0 < input_division, repr(input_division)
            if not self_durations:
                division_list = [input_division]
                division_lists.append(division_list)
                continue
            if input_meter.is_simple or not self_durations:
                durations = self_durations[:]
            elif input_meter.is_compound:
                multiplier = self_compound_meter_multiplier or 1
                durations = [
                    abjad.Duration(multiplier * _) for _ in self_durations
                ]
            division_list = list(durations)
            pattern_rotation_index = self_pattern_rotation_index or 0
            pattern_rotation_index *= i
            division_list = classes.Sequence(division_list).rotate(
                n=pattern_rotation_index
            )
            division_list = list(division_list)
            if self_cyclic:
                division_list = classes.Sequence(
                    division_list
                ).repeat_to_weight(input_division, allow_total=abjad.Less)
                division_list = list(division_list)
            total_duration = abjad.Duration(sum(division_list))
            if total_duration == input_duration:
                division_lists.append(division_list)
                continue
            remainder = input_division - total_duration
            remainder = Division(remainder)
            if self_remainder_direction == abjad.Left:
                if self_remainder_fuse_threshold is None:
                    division_list.insert(0, remainder)
                elif remainder <= self_remainder_fuse_threshold:
                    fused_value = division_list[0] + remainder
                    fused_value = Division(fused_value)
                    division_list[0] = fused_value
                else:
                    division_list.insert(0, remainder)
            else:
                if self_remainder_fuse_threshold is None:
                    division_list.append(remainder)
                elif remainder <= self_remainder_fuse_threshold:
                    fused_value = division_list[-1] + remainder
                    fused_value = Division(fused_value)
                    division_list[-1] = fused_value
                else:
                    division_list.append(remainder)
            total_duration = abjad.Duration(sum(division_list))
            pair = total_duration, input_duration
            assert total_duration == input_duration, pair
            division_lists.append(division_list)
        for _ in division_lists:
            assert isinstance(_, list), repr(_)
        division_lists, start_offset = self._to_divisions(
            division_lists, start_offset
        )
        return division_lists

    def _split_each_by_rounded_ratios(self, *, divisions=None, ratios=None):
        divisions = divisions or []
        if not divisions:
            return []
        divisions, start_offset = self._to_divisions(divisions)
        start_offset = divisions[0].start_offset
        division_lists = []
        ratios = self._get_ratios(ratios)
        for i, division in enumerate(divisions):
            ratio = ratios[i]
            numerators = abjad.mathtools.partition_integer_by_ratio(
                division.numerator, ratio
            )
            division_list = [
                Division((numerator, division.denominator))
                for numerator in numerators
            ]
            division_lists.append(division_list)
        division_lists, start_offset = self._to_divisions(
            division_lists, start_offset=start_offset
        )
        return division_lists

    def _to_divisions(self, argument, start_offset=None):
        if isinstance(argument, Division):
            result = Division(argument)
            if start_offset is not None:
                result._start_offset = start_offset
                start_offset += result.duration
        elif isinstance(argument, abjad.NonreducedFraction):
            result = Division(argument.pair)
            if start_offset is not None:
                result._start_offset = start_offset
                start_offset += result.duration
        elif hasattr(argument, "pair"):
            result = Division(argument.pair)
            if start_offset is not None:
                result._start_offset = start_offset
                start_offset += result.duration
        elif isinstance(argument, tuple):
            result = Division(argument)
            if start_offset is not None:
                result._start_offset = start_offset
                start_offset += result.duration
        elif isinstance(argument, (list, abjad.Sequence)):
            result = []
            for element in argument:
                new_element, start_offset = self._to_divisions(
                    element, start_offset=start_offset
                )
                result.append(new_element)
            result = type(argument)(result)
        else:
            raise TypeError(repr(argument))
        return result, start_offset

    ### PUBLIC METHODS ###

    @abjad.Signature(is_operator=True, method_name="r", subscript="n")
    def rotate(self, n=0) -> "DivisionSequence":
        r"""
        Rotates division sequence by index ``n``.

        ..  container:: example

            Rotates sequence to the left:

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
        n = n or 0
        items = []
        if len(self):
            first_start_offset = self[0].start_offset
            n = n % len(self)
            for item in self[-n : len(self)] + self[:-n]:
                items.append(item)
        start_offset = first_start_offset
        for item in items:
            duration = item.duration
            item._start_offset = start_offset
            start_offset += duration
        return type(self)(items=items)

    @abjad.Signature()
    def split_each_by_durations(
        self,
        durations,
        *,
        compound_meter_multiplier=None,
        cyclic=None,
        pattern_rotation_index=None,
        remainder=None,
        remainder_fuse_threshold=None,
    ) -> "DivisionSequence":
        """
        Splits each division in division sequence by ``durations``.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        durations = [abjad.Duration(_) for _ in durations]
        if compound_meter_multiplier is not None:
            compound_meter_multiplier = abjad.Multiplier(
                compound_meter_multiplier
            )
        if cyclic is not None:
            cyclic = bool(cyclic)
        if pattern_rotation_index is not None:
            assert isinstance(pattern_rotation_index, int)
        if remainder is not None:
            assert remainder in (abjad.Left, abjad.Right), repr(remainder)
        if remainder_fuse_threshold is not None:
            remainder_fuse_threshold = abjad.Duration(remainder_fuse_threshold)
        division_lists = self._split_each_by_durations(
            self,
            durations,
            self_compound_meter_multiplier=compound_meter_multiplier,
            self_cyclic=cyclic,
            self_pattern_rotation_index=pattern_rotation_index,
            self_remainder_direction=remainder,
            self_remainder_fuse_threshold=remainder_fuse_threshold,
        )
        sequences = [type(self)(_) for _ in division_lists]
        return type(self)(sequences)

    @abjad.Signature()
    def split_each_by_rounded_ratios(self, ratios) -> "DivisionSequence":
        """
        Splits each division in division sequence by rounded ``ratios``.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        division_lists = self._split_each_by_rounded_ratios(
            divisions=self, ratios=ratios
        )
        sequences = [type(self)(_) for _ in division_lists]
        return type(self)(sequences)


### FACTORY FUNCTIONS ###


def fuse_divisions(
    counts: typing.Sequence[int], *, cyclic: bool = None
) -> classes.Expression:
    """
    Fuses divisions by counts.

    ..  container:: example

        Fuses divisions once by counts:

        >>> expression = baca.fuse_divisions([1, 2])
        >>> divisions = [(2, 8), (2, 8), (2, 8), (2, 8), (2, 8), (2, 8)]
        >>> expression(divisions)
        DivisionSequence([Division((2, 8)), Division((4, 8)), Division((6, 8))])

    ..  container:: example

        Fuses divisions cyclically by counts:

        >>> expression = baca.fuse_divisions([1, 2], cyclic=True)
        >>> divisions = [(2, 8), (2, 8), (2, 8), (2, 8), (2, 8), (2, 8)]
        >>> expression(divisions)
        DivisionSequence([Division((2, 8)), Division((4, 8)), Division((2, 8)), Division((4, 8))])

    """
    expression = _divisions()
    expression = expression.partition_by_counts(
        counts, cyclic=cyclic, overhang=True
    )
    expression = expression.map(_divisions().sum())
    expression = expression.flatten(depth=-1)
    return expression


def fuse_compound_quarter_divisions(
    counts: typing.List[int], *, cyclic: bool = None
) -> classes.Expression:
    r"""
    Fuses compound quarter divisions.

    ..  container:: example

        Acyclic:

        >>> expression = baca.fuse_compound_quarter_divisions(
        ...     [1],
        ...     cyclic=False,
        ...     )

        >>> for item in expression([(2, 8), (2, 8), (2, 8)]):
        ...     item
        ...
        Division((1, 4))
        Division((2, 4))

        >>> for item in expression([(3, 8), (3, 8), (3, 8)]):
        ...     item
        ...
        Division((1, 4))
        Division((7, 8))

        Cyclic:

        >>> expression = baca.fuse_compound_quarter_divisions(
        ...     [1],
        ...     cyclic=True,
        ...     )

        >>> for item in expression([(2, 8), (2, 8), (2, 8)]):
        ...     item
        ...
        Division((1, 4))
        Division((1, 4))
        Division((1, 4))

        >>> for item in expression([(3, 8), (3, 8), (3, 8)]):
        ...     item
        ...
        Division((1, 4))
        Division((1, 8))
        Division((1, 4))
        Division((1, 8))
        Division((1, 4))
        Division((1, 8))

    ..  container:: example

        Cyclic:

        >>> expression = baca.fuse_compound_quarter_divisions(
        ...     [2],
        ...     cyclic=True,
        ...     )

        >>> for item in expression([(2, 8), (2, 8), (2, 8)]):
        ...     item
        ...
        Division((2, 4))
        Division((1, 4))

        >>> for item in expression([(3, 8), (3, 8), (3, 8)]):
        ...     item
        ...
        Division((3, 8))
        Division((3, 8))
        Division((3, 8))

        Acyclic:

        >>> expression = baca.fuse_compound_quarter_divisions(
        ...     [2],
        ...     cyclic=False,
        ...     )

        >>> for item in expression([(2, 8), (2, 8), (2, 8)]):
        ...     item
        ...
        Division((2, 4))
        Division((1, 4))

        >>> for item in expression([(3, 8), (3, 8), (3, 8)]):
        ...     item
        ...
        Division((3, 8))
        Division((6, 8))

    """
    if not all(isinstance(_, int) for _ in counts):
        raise Exception(counts)
    expression = quarter_split_each(compound=(3, 2))
    expression = expression.partition_by_counts(
        counts=counts, cyclic=cyclic, overhang=True
    )
    expression = expression.map(_divisions().sum())
    expression = expression.flatten(depth=-1)
    return expression


def quarter_split_each(
    *, compound: abjad.DurationTyping = None
) -> classes.Expression:
    """
    Quarter-split each division.

    ..  container:: example

        >>> expression = baca.quarter_split_each()
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

        >>> expression = baca.quarter_split_each(compound=(3, 2))
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
    expression = _divisions()
    expression = expression.split_each_by_durations(
        [(1, 4)], compound_meter_multiplier=compound, cyclic=True
    )
    expression = expression.flatten(depth=-1)
    return expression


def split_expanse(
    durations: typing.Sequence[abjad.DurationTyping],
    *,
    compound_meter_multiplier: abjad.DurationTyping = None,
    do_not_join: bool = None,
    cyclic: bool = None,
    pattern_rotation_index: int = None,
    remainder: abjad.HorizontalAlignment = abjad.Right,
    remainder_fuse_threshold: abjad.DurationTyping = None,
) -> classes.Expression:
    r"""
    Splits divisions by durations.

    ..  container:: example

        Cyclic:

        >>> expression = baca.split_expanse([(3, 8)], cyclic=True)

        >>> for item in expression([(2, 8), (2, 8)]):
        ...     item
        ...
        Division((3, 8))
        Division((1, 8))

        >>> for item in expression([(2, 8), (2, 8), (2, 8)]):
        ...     item
        ...
        Division((3, 8))
        Division((3, 8))

        >>> for item in expression([(2, 8), (2, 8), (2, 8), (2, 8)]):
        ...     item
        ...
        Division((3, 8))
        Division((3, 8))
        Division((2, 8))

        Acyclic:

        >>> expression = baca.split_expanse([(3, 8)], cyclic=False)

        >>> for item in expression([(2, 8), (2, 8)]):
        ...     item
        ...
        Division((3, 8))
        Division((1, 8))

        >>> for item in expression([(2, 8), (2, 8), (2, 8)]):
        ...     item
        ...
        Division((3, 8))
        Division((3, 8))

        >>> for item in expression([(2, 8), (2, 8), (2, 8), (2, 8)]):
        ...     item
        ...
        Division((3, 8))
        Division((5, 8))

    """
    expression = _divisions()
    if do_not_join:
        pass
    else:
        expression = expression.flatten(depth=-1)
        expression = expression.join()
    expression = expression.split_each_by_durations(
        durations,
        compound_meter_multiplier=compound_meter_multiplier,
        cyclic=cyclic,
        pattern_rotation_index=pattern_rotation_index,
        remainder=remainder,
        remainder_fuse_threshold=remainder_fuse_threshold,
    )
    expression = expression.flatten(depth=-1)
    return expression


def split_each_by_rounded_ratios(
    ratios: typing.Sequence[abjad.IntegerPair]
) -> classes.Expression:
    """
    Splits each division by rounded ratios.
    """
    expression = _divisions()
    expression = expression.split_each_by_rounded_ratios(ratios)
    expression = expression.flatten(depth=-1)
    return expression


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
