"""
Classes.
"""
import collections
import copy
import dataclasses
import typing

import uqbar

import abjad


@dataclasses.dataclass(slots=True)
class Counter:
    """
    Counter.

    ..  container:: example

        Initializes to zero and increments by 1:

        >>> counter = baca.Counter(start=0)
        >>> counter.start, counter.current
        (0, 0)

        >>> counter(count=1), counter.current
        (1, 1)
        >>> counter(count=1), counter.current
        (1, 2)
        >>> counter(count=1), counter.current
        (1, 3)
        >>> counter(count=1), counter.current
        (1, 4)

    ..  container:: example

        Initializes to zero and increments by 2:

        >>> counter = baca.Counter(start=0)
        >>> counter.start, counter.current
        (0, 0)

        >>> counter(2), counter.current
        (2, 2)
        >>> counter(2), counter.current
        (2, 4)
        >>> counter(2), counter.current
        (2, 6)
        >>> counter(2), counter.current
        (2, 8)

    ..  container:: example

        Initializes to 10 and increments by different values:

        >>> counter = baca.Counter(start=10)
        >>> counter.start, counter.current
        (10, 10)

        >>> counter(3), counter.current
        (3, 13)
        >>> counter(-6), counter.current
        (-6, 7)
        >>> counter(5.5), counter.current
        (5.5, 12.5)
        >>> counter(-2), counter.current
        (-2, 10.5)

    """

    start: int = 0
    current: int = dataclasses.field(init=False, repr=False)

    def __post_init__(self):
        self.current = self.start

    def __call__(self, count=1):
        current = self.current + count
        self.current = current
        return count


@dataclasses.dataclass(slots=True)
class Cursor:
    """
    Cursor.

    ..  container:: example

        Gets elements one at a time:

        >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
        >>> cursor = baca.Cursor(source=source, cyclic=True)

        >>> cursor.next()
        [13]
        >>> cursor.next()
        ['da capo']
        >>> cursor.next()
        [Note("cs'8.")]
        >>> cursor.next()
        ['rit.']
        >>> cursor.next()
        [13]
        >>> cursor.next()
        ['da capo']

    ..  container:: example

        Gets different numbers of elements at a time:

        >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
        >>> cursor = baca.Cursor(source=source, cyclic=True)

        >>> cursor.next(count=2)
        [13, 'da capo']
        >>> cursor.next(count=-1)
        ['da capo']
        >>> cursor.next(count=2)
        ['da capo', Note("cs'8.")]
        >>> cursor.next(count=-1)
        [Note("cs'8.")]
        >>> cursor.next(count=2)
        [Note("cs'8."), 'rit.']
        >>> cursor.next(count=-1)
        ['rit.']

    ..  container:: example

        Position starts at none by default:

        >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
        >>> cursor = baca.Cursor(source=source, cyclic=True)

        >>> cursor.position is None
        True

        >>> cursor.next()
        [13]
        >>> cursor.next()
        ['da capo']
        >>> cursor.next()
        [Note("cs'8.")]
        >>> cursor.next()
        ['rit.']

        >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
        >>> cursor = baca.Cursor(
        ...     source=source,
        ...     cyclic=True,
        ...     position=None,
        ... )

        >>> cursor.position is None
        True

        >>> cursor.next(count=-1)
        ['rit.']
        >>> cursor.next(count=-1)
        [Note("cs'8.")]
        >>> cursor.next(count=-1)
        ['da capo']
        >>> cursor.next(count=-1)
        [13]

    ..  container:: example

        Position starting at 0:

        >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
        >>> cursor = baca.Cursor(
        ...     source=source,
        ...     cyclic=True,
        ...     position=0,
        ... )

        >>> cursor.position
        0

        >>> cursor.next()
        [13]
        >>> cursor.next()
        ['da capo']
        >>> cursor.next()
        [Note("cs'8.")]
        >>> cursor.next()
        ['rit.']

        >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
        >>> cursor = baca.Cursor(
        ...     source=source,
        ...     cyclic=True,
        ...     position=0,
        ... )

        >>> cursor.position
        0

        >>> cursor.next(count=-1)
        ['rit.']
        >>> cursor.next(count=-1)
        [Note("cs'8.")]
        >>> cursor.next(count=-1)
        ['da capo']
        >>> cursor.next(count=-1)
        [13]

    ..  container:: example

        Position starting at -1:

        >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
        >>> cursor = baca.Cursor(
        ...     source=source,
        ...     cyclic=True,
        ...     position=-1,
        ... )

        >>> cursor.position
        -1

        >>> cursor.next()
        ['rit.']
        >>> cursor.next()
        [13]
        >>> cursor.next()
        ['da capo']
        >>> cursor.next()
        [Note("cs'8.")]

        >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
        >>> cursor = baca.Cursor(
        ...     source=source,
        ...     cyclic=True,
        ...     position=-1,
        ... )

        >>> cursor.position
        -1

        >>> cursor.next(count=-1)
        [Note("cs'8.")]
        >>> cursor.next(count=-1)
        ['da capo']
        >>> cursor.next(count=-1)
        [13]
        >>> cursor.next(count=-1)
        ['rit.']

    ..  container:: example

        Singletons Is true when cursor returns singletons not enclosed within a list.
        If false when cursor returns singletons enclosed within a list. Returns
        singletons enclosed within a list:

        >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
        >>> cursor = baca.Cursor(
        ...     source=source,
        ...     suppress_exception=True,
        ... )

        >>> cursor.next()
        [13]

        >>> cursor.next()
        ['da capo']

        >>> cursor.next()
        [Note("cs'8.")]

        >>> cursor.next()
        ['rit.']

        >>> cursor.next()
        []

        >>> cursor.next()
        []

    ..  container:: example

        Returns singletons free of enclosing list:

        >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
        >>> cursor = baca.Cursor(
        ...     source=source,
        ...     singletons=True,
        ...     suppress_exception=True,
        ... )

        >>> cursor.next()
        13

        >>> cursor.next()
        'da capo'

        >>> cursor.next()
        Note("cs'8.")

        >>> cursor.next()
        'rit.'

        >>> cursor.next() is None
        True

        >>> cursor.next() is None
        True

    """

    source: typing.Any
    cyclic: bool | None = None
    position: int | None = None
    singletons: bool | None = None
    suppress_exception: bool | None = None

    def __post_init__(self):
        if self.cyclic is not None:
            self.cyclic = bool(self.cyclic)
        self.source = self.source or ()
        assert isinstance(self.source, collections.abc.Iterable), repr(self.source)
        if self.cyclic:
            self.source = abjad.CyclicTuple(self.source)
        assert isinstance(self.position, (int, type(None))), repr(self.position)
        if self.singletons is not None:
            self.singletons = bool(self.singletons)
        if self.suppress_exception is not None:
            self.suppress_exception = bool(self.suppress_exception)

    def __getitem__(self, argument):
        """
        Gets item from cursor.

        ..  container:: example

            >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
            >>> cursor = baca.Cursor(source=source, cyclic=True)

            >>> cursor[0]
            13

            >>> cursor[:2]
            (13, 'da capo')

            >>> cursor[-1]
            'rit.'

        Returns item or slice.
        """
        return self.source.__getitem__(argument)

    def __iter__(self, count=1):
        """
        Iterates cursor.

        ..  container:: example

            Iterates acyclic cursor:

            >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
            >>> cursor = baca.Cursor(source=source)
            >>> for item in cursor:
            ...     item
            ...
            13
            'da capo'
            Note("cs'8.")
            'rit.'

        ..  container:: example

            Iterates cyclic cursor:

            >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
            >>> cursor = baca.Cursor(source=source, cyclic=True)
            >>> for item in cursor:
            ...     item
            ...
            13
            'da capo'
            Note("cs'8.")
            'rit.'

        Returns generator.
        """
        return iter(self.source)

    def __len__(self):
        """
        Gets length of cursor.

        ..  container:: example

            >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
            >>> cursor = baca.Cursor(source=source)
            >>> len(cursor)
            4

        Defined equal to length of cursor source.

        Returns nonnegative integer.
        """
        return len(self.source)

    @property
    def is_exhausted(self):
        """
        Is true when cursor is exhausted.

        ..  container:: example

            >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
            >>> cursor = baca.Cursor(source=source)
            >>> cursor.is_exhausted
            False

            >>> cursor.next(), cursor.is_exhausted
            ([13], False)

            >>> cursor.next(), cursor.is_exhausted
            (['da capo'], False)

            >>> cursor.next(), cursor.is_exhausted
            ([Note("cs'8.")], False)

            >>> cursor.next(), cursor.is_exhausted
            (['rit.'], True)

        Returns true or false.
        """
        if self.position is None:
            return False
        try:
            self.source[self.position]
        except IndexError:
            return True
        return False

    @staticmethod
    def from_pitch_class_segments(pitch_class_segments):
        """
        Makes cursor from ``pitch_class_segments``

        ..  container:: example

            Makes cursor from pitch-class segments:

            >>> number_lists = [[13, 13.5, 11], [-2, 2, 1.5]]
            >>> cursor = baca.Cursor.from_pitch_class_segments(number_lists)

            >>> cursor
            Cursor(source=CyclicTuple([PitchClassSegment([1, 1.5, 11]), PitchClassSegment([10, 2, 1.5])]), cyclic=True, position=None, singletons=None, suppress_exception=None)

        Coerces numeric ``pitch_class_segments``

        Returns cursor.
        """
        cells = []
        for pitch_class_segment in pitch_class_segments:
            pitch_class_segment = abjad.PitchClassSegment(items=pitch_class_segment)
            cells.append(pitch_class_segment)
        cursor = Cursor(source=cells, cyclic=True)
        return cursor

    def next(self, count=1, exhausted=False):
        """
        Gets next ``count`` elements in source.

        ..  container:: example

            Gets elements one at a time:

            >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
            >>> cursor = baca.Cursor(source=source, cyclic=True)

            >>> cursor.next()
            [13]
            >>> cursor.next()
            ['da capo']
            >>> cursor.next()
            [Note("cs'8.")]
            >>> cursor.next()
            ['rit.']
            >>> cursor.next()
            [13]
            >>> cursor.next()
            ['da capo']

        ..  container:: example

            Gets elements one at a time in reverse:

            >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
            >>> cursor = baca.Cursor(source=source, cyclic=True)

            >>> cursor.next(count=-1)
            ['rit.']
            >>> cursor.next(count=-1)
            [Note("cs'8.")]
            >>> cursor.next(count=-1)
            ['da capo']
            >>> cursor.next(count=-1)
            [13]

        ..  container:: example

            Gets same two elements forward and back:

            >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
            >>> cursor = baca.Cursor(source=source, cyclic=True)

            >>> cursor.next(count=2)
            [13, 'da capo']
            >>> cursor.next(count=-2)
            ['da capo', 13]
            >>> cursor.next(count=2)
            [13, 'da capo']
            >>> cursor.next(count=-2)
            ['da capo', 13]

        ..  container:: example

            Gets different numbers of elements at a time:

            >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
            >>> cursor = baca.Cursor(source=source, cyclic=True)

            >>> cursor.next(count=2)
            [13, 'da capo']
            >>> cursor.next(count=-1)
            ['da capo']
            >>> cursor.next(count=2)
            ['da capo', Note("cs'8.")]
            >>> cursor.next(count=-1)
            [Note("cs'8.")]
            >>> cursor.next(count=2)
            [Note("cs'8."), 'rit.']
            >>> cursor.next(count=-1)
            ['rit.']

        ..  container:: example

            Gets different numbers of elements at a time:

            >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
            >>> cursor = baca.Cursor(source=source, cyclic=True)

            >>> cursor.next(count=2)
            [13, 'da capo']
            >>> cursor.next(count=-3)
            ['da capo', 13, 'rit.']
            >>> cursor.next(count=2)
            ['rit.', 13]
            >>> cursor.next(count=-3)
            [13, 'rit.', Note("cs'8.")]
            >>> cursor.next(count=2)
            [Note("cs'8."), 'rit.']
            >>> cursor.next(count=-3)
            ['rit.', Note("cs'8."), 'da capo']

        ..  container:: example exception

            Raises exception when cursor is exhausted:

            >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
            >>> cursor = baca.Cursor(source=source)

            >>> cursor.next(count=99)
            Traceback (most recent call last):
                ...
            Exception: cursor only 4.

        Returns tuple.
        """
        result = []
        if self.position is None:
            self.position = 0
        if 0 < count:
            for i in range(count):
                try:
                    element = self.source[self.position]
                    result.append(element)
                except IndexError:
                    if not self.suppress_exception:
                        raise Exception(f"cursor only {len(self.source)}.")
                self.position += 1
        elif count < 0:
            for i in range(abs(count)):
                self.position -= 1
                try:
                    element = self.source[self.position]
                    result.append(element)
                except IndexError:
                    if not self.suppress_exception:
                        raise Exception(f"cursor only {len(self.source)}.")
        if self.singletons:
            if len(result) == 0:
                result = None
            elif len(result) == 1:
                result = result[0]
        if exhausted and not self.is_exhausted:
            raise Exception(f"cusor not exhausted: {self!r}.")
        return result

    def reset(self):
        """
        Resets cursor.

        ..  container:: example

            >>> source = [13, "da capo", abjad.Note("cs'8."), "rit."]
            >>> cursor = baca.Cursor(source=source)

            >>> cursor.next()
            [13]
            >>> cursor.next()
            ['da capo']

            >>> cursor.reset()

            >>> cursor.next()
            [13]
            >>> cursor.next()
            ['da capo']

        Returns none.
        """
        self.position = 0


@dataclasses.dataclass(slots=True)
class PaddedTuple:
    """
    Padded tuple.

    ..  container:: example

        >>> tuple_ = baca.PaddedTuple("abcd", pad=2)

        >>> tuple_
        PaddedTuple(items=('a', 'b', 'c', 'd'), pad=2)

        >>> for i in range(8):
        ...     print(i, tuple_[i])
        ...
        0 a
        1 b
        2 c
        3 d
        4 c
        5 d
        6 c
        7 d

    ..  container:: example

        With nonnegative indices:

        >>> tuple_ = baca.PaddedTuple("abcd", pad=1)
        >>> for i in range(8):
        ...     print(i, tuple_[i])
        ...
        0 a
        1 b
        2 c
        3 d
        4 d
        5 d
        6 d
        7 d

        >>> tuple_ = baca.PaddedTuple("abcd", pad=2)
        >>> for i in range(8):
        ...     print(i, tuple_[i])
        ...
        0 a
        1 b
        2 c
        3 d
        4 c
        5 d
        6 c
        7 d

        >>> tuple_ = baca.PaddedTuple("abcd", pad=3)
        >>> for i in range(8):
        ...     print(i, tuple_[i])
        ...
        0 a
        1 b
        2 c
        3 d
        4 b
        5 c
        6 d
        7 b

        >>> tuple_ = baca.PaddedTuple("abcd", pad=4)
        >>> for i in range(8):
        ...     print(i, tuple_[i])
        ...
        0 a
        1 b
        2 c
        3 d
        4 a
        5 b
        6 c
        7 d

    ..  container:: example

        With nonpositive indices:

        >>> tuple_ = baca.PaddedTuple("abcd", pad=1)
        >>> for i in range(-1, -9, -1):
        ...     print(i, tuple_[i])
        ...
        -1 d
        -2 c
        -3 b
        -4 a
        -5 a
        -6 a
        -7 a
        -8 a

        >>> tuple_ = baca.PaddedTuple("abcd", pad=2)
        >>> for i in range(-1, -9, -1):
        ...     print(i, tuple_[i])
        ...
        -1 d
        -2 c
        -3 b
        -4 a
        -5 b
        -6 a
        -7 b
        -8 a

        >>> tuple_ = baca.PaddedTuple("abcd", pad=3)
        >>> for i in range(-1, -9, -1):
        ...     print(i, tuple_[i])
        ...
        -1 d
        -2 c
        -3 b
        -4 a
        -5 c
        -6 b
        -7 a
        -8 c

        >>> tuple_ = baca.PaddedTuple("abcd", pad=4)
        >>> for i in range(-1, -9, -1):
        ...     print(i, tuple_[i])
        ...
        -1 d
        -2 c
        -3 b
        -4 a
        -5 d
        -6 c
        -7 b
        -8 a

    Padded tuples overload the item-getting method of built-in tuples.

    Padded tuples return a value for any integer index.
    """

    items: typing.Sequence | None = None
    pad: int = 1

    def __post_init__(self):
        self.items = self.items or ()
        self.items = tuple(self.items)
        assert isinstance(self.pad, int), repr(self.pad)
        assert 1 <= self.pad, repr(self.pad)

    def __contains__(self, item) -> bool:
        """
        Is true when padded tuple contains ``item``.
        """
        return self.items.__contains__(item)

    def __getitem__(self, argument) -> typing.Any:
        """
        Gets item or slice identified by ``argument``.

        ..  container:: example

            Gets slice open at right:

            >>> baca.PaddedTuple("abcd", pad=3)[2:]
            ('c', 'd')

            Gets slice closed at right:

            >>> slice_ = baca.PaddedTuple("abcd", pad=3)[:15]
            >>> slice_
            ('a', 'b', 'c', 'd', 'b', 'c', 'd', 'b', 'c', 'd', 'b', 'c', 'd', 'b', 'c')

            >>> len(slice_)
            15

        Raises index error when ``argument`` can not be found in padded tuple.
        """
        if isinstance(argument, slice):
            if argument.start is None:
                if argument.stop is None:
                    start, stop, stride = 0, len(self), 1
                elif 0 < argument.stop:
                    start, stop, stride = 0, argument.stop, 1
                elif argument.stop < 0:
                    start, stop, stride = -1, stop, -1
            elif argument.stop is None:
                if argument.start is None:
                    start, stop, stride = 0, len(self), 1
                elif 0 < argument.start:
                    start, stop, stride = argument.start, len(self), 1
                elif argument.start < 0:
                    start, stop, stride = argument.start, -len(self), -1
            elif 0 < argument.start and 0 < argument.stop:
                start, stop, stride = argument.start, argument.stop, 1
            elif argument.start < 0 and argument.stop < 0:
                start, stop, stride = argument.start, argument.stop, -1
            else:
                raise ValueError(argument)
            items = []
            for i in range(start, stop, stride):
                item = self[i]
                items.append(item)
            return tuple(items)
        if not self:
            raise IndexError(f"padded tuple is empty: {self!r}.")
        length = len(self)
        assert isinstance(self.pad, int)
        if 0 <= argument < len(self):
            pass
        elif length <= argument:
            right = self.pad
            left = length - right
            overage = argument - length
            argument = left + (overage % right)
        elif -length <= argument < 0:
            pass
        else:
            assert argument < -length
            left = self.pad
            right = length - left
            assert left + right == length
            overage = abs(argument) - length
            overage = overage % left
            if overage == 0:
                overage = left
            positive_argument = right + overage
            argument = -positive_argument
        return self.items.__getitem__(argument)

    def __iter__(self) -> typing.Iterator:
        """
        Iterates padded tuple.

        Iterates items only once.

        Does not iterate infinitely.
        """
        return self.items.__iter__()

    def __len__(self) -> int:
        """
        Gets length of padded tuple.

        ..  container:: example

            >>> len(baca.PaddedTuple("abcd", pad=3))
            4

        """
        assert isinstance(self.items, tuple)
        return self.items.__len__()

    def _get_slice(self, start_index, stop_index):
        if 0 < stop_index and start_index is None:
            start_index = 0
        elif stop_index < 0 and start_index is None:
            start_index = -1
        items = []
        if 0 <= start_index and 0 <= stop_index:
            for i in range(start_index, stop_index):
                item = self[i]
                items.append(item)
        elif start_index < 0 and stop_index < 0:
            for i in range(start_index, stop_index, -1):
                item = self[i]
                items.append(item)
        else:
            raise Exception("slice index signs must be equal.")
        return tuple(items)


class SchemeManifest:
    """
    Scheme manifest.

    New functions defined in ``~/baca/lilypond/baca.ily`` must currently be added here by
    hand.

    TODO: eliminate duplication. Define custom Scheme functions here (``SchemeManifest``)
    and teach ``SchemeManifest`` to write ``~/baca/lilypond/baca.ily`` automatically.
    """

    ### CLASS VARIABLES ###

    _dynamics = (
        ("baca-appena-udibile", "appena udibile"),
        ("baca-f-but-accents-sffz", "f"),
        ("baca-f-sub-but-accents-continue-sffz", "f"),
        ("baca-ffp", "p"),
        ("baca-fffp", "p"),
        ("niente", "niente"),
        ("baca-p-sub-but-accents-continue-sffz", "p"),
        #
        ("baca-pppf", "f"),
        ("baca-pppff", "ff"),
        ("baca-pppfff", "fff"),
        #
        ("baca-ppf", "f"),
        ("baca-ppff", "ff"),
        ("baca-ppfff", "fff"),
        #
        ("baca-pf", "f"),
        ("baca-pff", "ff"),
        ("baca-pfff", "fff"),
        #
        ("baca-ppp-ppp", "ppp"),
        ("baca-ppp-pp", "pp"),
        ("baca-ppp-p", "p"),
        ("baca-ppp-mp", "mp"),
        ("baca-ppp-mf", "mf"),
        ("baca-ppp-f", "f"),
        ("baca-ppp-ff", "ff"),
        ("baca-ppp-fff", "fff"),
        #
        ("baca-pp-ppp", "ppp"),
        ("baca-pp-pp", "pp"),
        ("baca-pp-p", "p"),
        ("baca-pp-mp", "mp"),
        ("baca-pp-mf", "mf"),
        ("baca-pp-f", "f"),
        ("baca-pp-ff", "ff"),
        ("baca-pp-fff", "fff"),
        #
        ("baca-p-ppp", "ppp"),
        ("baca-p-pp", "pp"),
        ("baca-p-p", "p"),
        ("baca-p-mp", "mp"),
        ("baca-p-mf", "mf"),
        ("baca-p-f", "f"),
        ("baca-p-ff", "ff"),
        ("baca-p-fff", "fff"),
        #
        ("baca-mp-ppp", "ppp"),
        ("baca-mp-pp", "pp"),
        ("baca-mp-p", "p"),
        ("baca-mp-mp", "mp"),
        ("baca-mp-mf", "mf"),
        ("baca-mp-f", "f"),
        ("baca-mp-ff", "ff"),
        ("baca-mp-fff", "fff"),
        #
        ("baca-mf-ppp", "ppp"),
        ("baca-mf-pp", "pp"),
        ("baca-mf-p", "p"),
        ("baca-mf-mp", "mp"),
        ("baca-mf-mf", "mf"),
        ("baca-mf-f", "f"),
        ("baca-mf-ff", "ff"),
        ("baca-mf-fff", "fff"),
        #
        ("baca-f-ppp", "ppp"),
        ("baca-f-pp", "pp"),
        ("baca-f-p", "p"),
        ("baca-f-mp", "mp"),
        ("baca-f-mf", "mf"),
        ("baca-f-f", "f"),
        ("baca-f-ff", "ff"),
        ("baca-f-fff", "fff"),
        #
        ("baca-ff-ppp", "ppp"),
        ("baca-ff-pp", "pp"),
        ("baca-ff-p", "p"),
        ("baca-ff-mp", "mp"),
        ("baca-ff-mf", "mf"),
        ("baca-ff-f", "f"),
        ("baca-ff-ff", "ff"),
        ("baca-ff-fff", "fff"),
        #
        ("baca-fff-ppp", "ppp"),
        ("baca-fff-pp", "pp"),
        ("baca-fff-p", "p"),
        ("baca-fff-mp", "mp"),
        ("baca-fff-mf", "mf"),
        ("baca-fff-f", "f"),
        ("baca-fff-ff", "ff"),
        ("baca-fff-fff", "fff"),
        #
        ("baca-sff", "ff"),
        ("baca-sffp", "p"),
        ("baca-sffpp", "pp"),
        ("baca-sfffz", "fff"),
        ("baca-sffz", "ff"),
        ("baca-sfpp", "pp"),
        ("baca-sfz-f", "f"),
        ("baca-sfz-p", "p"),
    )

    ### PUBLIC PROPERTIES ###

    @property
    def dynamics(self) -> typing.List[str]:
        """
        Gets dynamics.

        ..  container:: example

            >>> scheme_manifest = baca.SchemeManifest()
            >>> for dynamic in scheme_manifest.dynamics:
            ...     dynamic
            ...
            'baca-appena-udibile'
            'baca-f-but-accents-sffz'
            'baca-f-sub-but-accents-continue-sffz'
            'baca-ffp'
            'baca-fffp'
            'niente'
            'baca-p-sub-but-accents-continue-sffz'
            'baca-pppf'
            'baca-pppff'
            'baca-pppfff'
            'baca-ppf'
            'baca-ppff'
            'baca-ppfff'
            'baca-pf'
            'baca-pff'
            'baca-pfff'
            'baca-ppp-ppp'
            'baca-ppp-pp'
            'baca-ppp-p'
            'baca-ppp-mp'
            'baca-ppp-mf'
            'baca-ppp-f'
            'baca-ppp-ff'
            'baca-ppp-fff'
            'baca-pp-ppp'
            'baca-pp-pp'
            'baca-pp-p'
            'baca-pp-mp'
            'baca-pp-mf'
            'baca-pp-f'
            'baca-pp-ff'
            'baca-pp-fff'
            'baca-p-ppp'
            'baca-p-pp'
            'baca-p-p'
            'baca-p-mp'
            'baca-p-mf'
            'baca-p-f'
            'baca-p-ff'
            'baca-p-fff'
            'baca-mp-ppp'
            'baca-mp-pp'
            'baca-mp-p'
            'baca-mp-mp'
            'baca-mp-mf'
            'baca-mp-f'
            'baca-mp-ff'
            'baca-mp-fff'
            'baca-mf-ppp'
            'baca-mf-pp'
            'baca-mf-p'
            'baca-mf-mp'
            'baca-mf-mf'
            'baca-mf-f'
            'baca-mf-ff'
            'baca-mf-fff'
            'baca-f-ppp'
            'baca-f-pp'
            'baca-f-p'
            'baca-f-mp'
            'baca-f-mf'
            'baca-f-f'
            'baca-f-ff'
            'baca-f-fff'
            'baca-ff-ppp'
            'baca-ff-pp'
            'baca-ff-p'
            'baca-ff-mp'
            'baca-ff-mf'
            'baca-ff-f'
            'baca-ff-ff'
            'baca-ff-fff'
            'baca-fff-ppp'
            'baca-fff-pp'
            'baca-fff-p'
            'baca-fff-mp'
            'baca-fff-mf'
            'baca-fff-f'
            'baca-fff-ff'
            'baca-fff-fff'
            'baca-sff'
            'baca-sffp'
            'baca-sffpp'
            'baca-sfffz'
            'baca-sffz'
            'baca-sfpp'
            'baca-sfz-f'
            'baca-sfz-p'

        """
        return [_[0] for _ in self._dynamics]

    ### PUBLIC METHODS ###

    def dynamic_to_steady_state(self, dynamic):
        """
        Changes ``dynamic`` to steady state.

        ..  container:: example

            >>> scheme_manifest = baca.SchemeManifest()
            >>> scheme_manifest.dynamic_to_steady_state("sfz-p")
            'p'

        Returns string.
        """
        for dynamic_, steady_state in self._dynamics:
            if dynamic_ == dynamic:
                return steady_state
            if dynamic_ == "baca-" + dynamic:
                return steady_state
        raise KeyError(dynamic)


class Tree:
    """
    Tree.

    ..  container:: example

        Here's a tree:

        >>> items = [[[0, 1], [2, 3]], [4, 5]]
        >>> tree = baca.Tree(items=items)

        >>> abjad.graph(tree) # doctest: +SKIP

        >>> tree.get_payload(nested=True)
        [[[0, 1], [2, 3]], [4, 5]]

        >>> tree.get_payload()
        [0, 1, 2, 3, 4, 5]

    ..  container:: example

        Here's an internal node:

        >>> tree[1]
        Tree(<2>)

        >>> tree[1]
        Tree(<2>)

        >>> tree[1].get_payload(nested=True)
        [4, 5]

        >>> tree[1].get_payload()
        [4, 5]

    ..  container:: example

        Here's a leaf:

        >>> tree[1][0]
        Tree(<1>)

        >>> tree[1][0]
        Tree(<1>)

        >>> tree[1][0].get_payload(nested=True)
        4

        >>> tree[1][0].get_payload()
        [4]

    ..  container:: example

        Initializes from other trees:

        >>> tree_1 = baca.Tree(items=[0, 1])
        >>> tree_2 = baca.Tree(items=[2, 3])
        >>> tree_3 = baca.Tree(items=[4, 5])
        >>> tree = baca.Tree(items=[[tree_1, tree_2], tree_3])
        >>> abjad.graph(tree) # doctest: +SKIP

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_children",
        "_item_class",
        "_items",
        "_expression",
        "_parent",
        "_payload",
    )

    ### INITIALIZER ###

    def __init__(self, items=None, *, item_class=None):
        self._children = []
        self._expression = None
        self._item_class = item_class
        self._parent = None
        self._payload = None
        if self._are_internal_nodes(items):
            items = self._initialize_internal_nodes(items)
        else:
            items = self._initialize_payload(items)
        self._items = items

    ### SPECIAL METHODS ###

    def __contains__(self, argument):
        """
        Is true when tree contains ``argument``.

        ..  container:: example

            Tree contains node:

            >>> items = [[[0, 1], [2, 3]], [4, 5]]
            >>> tree = baca.Tree(items=items)

            >>> tree[-1] in tree
            True

        ..  container:: example

            Tree does not contain node:

            >>> tree[-1][-1] in tree
            False

        Returns true or false.
        """
        return argument in self._children

    def __eq__(self, argument):
        """
        Is true when ``argument`` is the same type as tree and when the payload of all
        subtrees are equal.

        ..  container:: example

            Is true when subtrees are equal:

            >>> sequence_1 = [[[0, 1], [2, 3]], [4, 5]]
            >>> tree_1 = baca.Tree(sequence_1)
            >>> sequence_2 = [[[0, 1], [2, 3]], [4, 5]]
            >>> tree_2 = baca.Tree(sequence_2)
            >>> sequence_3 = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree_3 = baca.Tree(sequence_3)

            >>> tree_1 == tree_1
            True
            >>> tree_1 == tree_2
            True
            >>> tree_1 == tree_3
            False
            >>> tree_2 == tree_1
            True
            >>> tree_2 == tree_2
            True
            >>> tree_2 == tree_3
            False
            >>> tree_3 == tree_1
            False
            >>> tree_3 == tree_2
            False
            >>> tree_3 == tree_3
            True

        Returns true or false.
        """
        if isinstance(argument, type(self)):
            if self._payload is not None or argument._payload is not None:
                return self._payload == argument._payload
            if len(self) == len(argument):
                for x, y in zip(self._noncyclic_children, argument._noncyclic_children):
                    if not x == y:
                        return False
                else:
                    return True
        return False

    def __getitem__(self, argument):
        """
        Gets node or node slice identified by ``argument``.

        ..  container:: example

            >>> items = [[[0, 1], [2, 3]], [4, 5]]
            >>> tree = baca.Tree(items=items)

            >>> tree[-1]
            Tree(<2>)

            >>> tree[-1:]
            [Tree(<2>)]

        Returns node or slice of nodes.
        """
        return self._children.__getitem__(argument)

    def __graph__(self, **keywords):
        """
        Graphs tree.

        ..  container:: example

            >>> items = [[[0, 1], [2, 3]], [4, 5]]
            >>> tree = baca.Tree(items=items)

            >>> abjad.graph(tree) # doctest: +SKIP

            >>> tree.__graph__()
            <uqbar.graphs.Graph.Graph object at 0x...>

        Returns uqbar graph.
        """
        graph = uqbar.graphs.Graph(
            attributes={"bgcolor": "transparent", "truecolor": True},
            name="G",
        )
        node_mapping = {}
        for node in self._iterate_depth_first():
            graphviz_node = uqbar.graphs.Node()
            if list(node):
                graphviz_node.attributes["shape"] = "circle"
                graphviz_node.attributes["label"] = ""
            else:
                graphviz_node.attributes["shape"] = "box"
                graphviz_node.attributes["label"] = str(node._payload)
            graph.append(graphviz_node)
            node_mapping[node] = graphviz_node
            if node._parent is not None:
                uqbar.graphs.Edge().attach(
                    node_mapping[node._parent],
                    node_mapping[node],
                )
        return graph

    def __hash__(self):
        """
        Hashes tree.

        Returns integer.
        """
        return super().__hash__()

    # TODO: make this work without recursion error
    #    def __iter__(self):
    #        """
    #        Iterates tree at level -1.
    #
    #        ..  container:: example
    #
    #            Gets node:
    #
    #                >>> items = [[[0, 1], [2, 3]], [4, 5]]
    #                >>> tree = baca.Tree(items=items)
    #
    #                >>> tree.__iter__()
    #
    #        """
    #        return self.iterate(level=-1)

    def __len__(self):
        """
        Gets length of tree.

        ..  container:: example

            >>> items = [[[0, 1], [2, 3]], [4, 5]]
            >>> tree = baca.Tree(items=items)

            >>> len(tree)
            2

        Defined equal to number of nodes in tree at level 1.

        Returns nonnegative integer.
        """
        return len(self._children)

    def __repr__(self):
        """
        Gets interpreter representation of tree.

        ..  container:: example

            Gets interpreter representation of tree:

            >>> items = [[[0, 1], [2, 3]], [4, 5]]
            >>> baca.Tree(items=items)
            Tree(<2>)

        ..  container:: example

            Gets interpreter representation of leaf:

            >>> baca.Tree(0)
            Tree(<1>)

        ..  container:: example

            Gets interpreter representation of empty tree:

            >>> baca.Tree()
            Tree(<0>)

        Returns string.
        """
        if isinstance(self.items, list):
            length = len(self.items)
        elif self.items is None:
            length = 0
        else:
            assert isinstance(self.items, int), repr(self.items)
            length = 1
        return f"Tree(<{length}>)"

    ### PRIVATE PROPERTIES ###

    @property
    def _noncyclic_children(self):
        return list(self._children)

    @property
    def _root(self):
        return self._get_parentage()[-1]

    ### PRIVATE METHODS ###

    def _apply_to_leaves_and_emit_new_tree(self, operator):
        result = abjad.new(self)
        for leaf in result.iterate(level=-1):
            assert not len(leaf), repr(leaf)
            pitch = leaf._items
            pitch = operator(pitch)
            leaf._set_leaf_item(pitch)
        return result

    def _are_internal_nodes(self, argument):
        if isinstance(argument, collections.abc.Iterable) and not isinstance(
            argument, str
        ):
            return True
        if isinstance(argument, type(self)) and len(argument):
            return True
        return False

    def _get_depth(self):
        """
        Gets depth.

        ..  container:: example

            Gets depth:

            >>> items = [[[0, 1], [2, 3]], [4, 5]]
            >>> tree = baca.Tree(items=items)

            >>> tree[1]._get_depth()
            2

        Returns nonnegative integer.
        """
        levels = set([])
        for node in self._iterate_depth_first():
            levels.add(node._get_level())
        return max(levels) - self._get_level() + 1

    def _get_index_in_parent(self):
        if self._parent is not None:
            return self._parent._index(self)
        else:
            return None

    def _get_level(self, negative=False):
        """
        Gets level.

        ..  container:: example

            Gets level:

                >>> items = [[[0, 1], [2, 3]], [4, 5]]
                >>> tree = baca.Tree(items=items)

            >>> tree._get_level()
            0

            >>> tree[1]._get_level()
            1

            >>> tree[1][1]._get_level()
            2

        ..  container:: example

            Gets negative level:

                >>> items = [[[0, 1], [2, 3]], [4, 5]]
                >>> tree = baca.Tree(items=items)

            >>> tree._get_level(negative=True)
            -4

            >>> tree[1]._get_level(negative=True)
            -2

            >>> tree[1][1]._get_level(negative=True)
            -1

            >>> tree[-1][-1]._get_level(negative=True)
            -1

            >>> tree[-1]._get_level(negative=True)
            -2

        Returns nonnegative integer when ``negative`` is false.

        Returns negative integer when ``negative`` is true.
        """
        if negative:
            return -self._get_depth()
        return len(self._get_parentage()[1:])

    def _get_next_n_nodes_at_level(self, n, level, nodes_must_be_complete=False):
        """
        Gets next ``n`` nodes ``level``.

        ..  container:: example

            Nodes don't need to be complete:

            >>> items = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = baca.Tree(items=items)

            Gets all nodes at level 2:

            >>> tree[0][0]._get_next_n_nodes_at_level(None, 2)
            [Tree(<1>), Tree(<1>), Tree(<1>), Tree(<1>), Tree(<1>), Tree(<1>), Tree(<1>)]

            Gets all nodes at level -1:

            >>> tree[0][0]._get_next_n_nodes_at_level(None, -1)
            [Tree(<1>), Tree(<1>), Tree(<1>), Tree(<1>), Tree(<1>), Tree(<1>), Tree(<1>)]

            Gets next 4 nodes at level 2:

            >>> tree[0][0]._get_next_n_nodes_at_level(4, 2)
            [Tree(<1>), Tree(<1>), Tree(<1>), Tree(<1>)]

            Gets next 3 nodes at level 1:

            >>> tree[0][0]._get_next_n_nodes_at_level(3, 1)
            [Tree(<1>), Tree(<2>), Tree(<2>)]

            Gets next node at level 0:

            >>> tree[0][0]._get_next_n_nodes_at_level(1, 0)
            [Tree(<4>)]

            Gets next 4 nodes at level -1:

            >>> tree[0][0]._get_next_n_nodes_at_level(4, -1)
            [Tree(<1>), Tree(<1>), Tree(<1>), Tree(<1>)]

            Gets next 3 nodes at level -2:

            >>> tree[0][0]._get_next_n_nodes_at_level(3, -2)
            [Tree(<1>), Tree(<2>), Tree(<2>)]

            Gets previous 4 nodes at level 2:

            >>> tree[-1][-1]._get_next_n_nodes_at_level(-4, 2)
            [Tree(<1>), Tree(<1>), Tree(<1>), Tree(<1>)]

            Gets previous 3 nodes at level 1:

            >>> tree[-1][-1]._get_next_n_nodes_at_level(-3, 1)
            [Tree(<1>), Tree(<2>), Tree(<2>)]

            Gets previous node at level 0:

            >>> tree[-1][-1]._get_next_n_nodes_at_level(-1, 0)
            [Tree(<4>)]

            Gets previous 4 nodes at level -1:

            >>> tree[-1][-1]._get_next_n_nodes_at_level(-4, -1)
            [Tree(<1>), Tree(<1>), Tree(<1>), Tree(<1>)]

            Gets previous 3 nodes at level -2:

            >>> tree[-1][-1]._get_next_n_nodes_at_level(-3, -2)
            [Tree(<1>), Tree(<2>), Tree(<2>)]

        ..  container:: example

            Tree of length greater than ``1`` for examples with positive ``n``:

            >>> items = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = baca.Tree(items=items)

            Gets next 4 nodes at level 2:

            >>> for node in tree[0][0]._get_next_n_nodes_at_level(
            ...     4, 2, nodes_must_be_complete=True,
            ...     ):
            ...     node
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)

            Gets next 3 nodes at level 1:

            >>> for node in tree[0][0]._get_next_n_nodes_at_level(
            ...     3, 1, nodes_must_be_complete=True
            ...     ):
            ...     node
            Tree(<1>)
            Tree(<2>)
            Tree(<2>)
            Tree(<2>)

            Gets next 4 nodes at level -1:

            >>> for node in tree[0][0]._get_next_n_nodes_at_level(4, -1):
            ...     node
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)

            Gets next 3 nodes at level -2:

            >>> for node in tree[0][0]._get_next_n_nodes_at_level(
            ...     3, -2, nodes_must_be_complete=True
            ...     ):
            ...     node
            Tree(<1>)
            Tree(<2>)
            Tree(<2>)
            Tree(<2>)

        ..  container:: example

            Tree of length greater than ``1`` for examples with negative ``n``:

            >>> items = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = baca.Tree(items=items)

            Gets previous 4 nodes at level 2:

            >>> for node in tree[-1][-1]._get_next_n_nodes_at_level(
            ...     -4, 2, nodes_must_be_complete=True
            ...     ):
            ...     node
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)

            Gets previous 3 nodes at level 1:

            >>> for node in tree[-1][-1]._get_next_n_nodes_at_level(
            ...     -3, 1, nodes_must_be_complete=True
            ...     ):
            ...     node
            Tree(<1>)
            Tree(<2>)
            Tree(<2>)
            Tree(<2>)

            Gets previous 4 nodes at level -1:

            >>> for node in tree[-1][-1]._get_next_n_nodes_at_level(
            ...     -4, -1, nodes_must_be_complete=True
            ...     ):
            ...     node
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)

            Gets previous 3 nodes at level -2:

            >>> for node in tree[-1][-1]._get_next_n_nodes_at_level(
            ...     -3, -2, nodes_must_be_complete=True
            ...     ):
            ...     node
            Tree(<1>)
            Tree(<2>)
            Tree(<2>)
            Tree(<2>)

        """
        if not self._is_valid_level(level):
            raise Exception(f"invalid level: {level!r}.")
        result = []
        self_is_found = False
        first_node_returned_is_trimmed = False
        all_nodes_at_level = False
        reverse = False
        if n is None:
            all_nodes_at_level = True
        elif n < 0:
            reverse = True
            n = abs(n)
        generator = self._root._iterate_depth_first(reverse=reverse)
        previous_node = None
        for node in generator:
            if not all_nodes_at_level and len(result) == n:
                if not first_node_returned_is_trimmed or not nodes_must_be_complete:
                    return result
            if not all_nodes_at_level and len(result) == n + 1:
                return result
            if node is self:
                self_is_found = True
                # test whether node to return is higher in tree than self;
                # or-clause allows for test of either nonnegative
                # or negative level
                if ((0 <= level) and level < self._get_level()) or (
                    (level < 0) and level < self._get_level(negative=True)
                ):
                    first_node_returned_is_trimmed = True
                    subtree_to_trim = node._parent
                    # find subtree to trim where level is nonnegative
                    if 0 <= level:
                        while level < subtree_to_trim._get_level():
                            subtree_to_trim = subtree_to_trim._parent
                    # find subtree to trim where level is negative
                    else:
                        while subtree_to_trim._get_level(negative=True) < level:
                            subtree_to_trim = subtree_to_trim._parent
                    position_of_descendant = (
                        subtree_to_trim._get_position_of_descendant(node)
                    )
                    first_subtree = copy.deepcopy(subtree_to_trim)
                    reference_node = first_subtree._get_node_at_position(
                        position_of_descendant
                    )
                    reference_node._remove_to_root(reverse=reverse)
                    result.append(first_subtree)
            if self_is_found:
                if node is not self:
                    if node._is_at_level(level):
                        result.append(node)
                    # special case to handle a cyclic tree of length 1
                    elif node._is_at_level(0) and len(node) == 1:
                        if previous_node._is_at_level(level):
                            result.append(node)
            previous_node = node
        else:
            if all_nodes_at_level:
                return result
            else:
                raise ValueError(f"not enough nodes at level {level!r}.")

    def _get_node_at_position(self, position):
        result = self
        for index in position:
            result = result[index]
        return result

    def _get_parentage(self):
        """
        Gets parentage.

        ..  container:: example

            Gets parentage with self:

            >>> items = [[[0, 1], [2, 3]], [4, 5]]
            >>> tree = baca.Tree(items=items)
            >>> parentage = tree[1]._get_parentage()
            >>> for tree in parentage:
            ...     tree
            Tree(<2>)
            Tree(<2>)

            Gets parentage without self:

            >>> items = [[[0, 1], [2, 3]], [4, 5]]
            >>> tree = baca.Tree(items=items)
            >>> for tree in tree[1]._get_parentage()[1:]:
            ...     tree
            Tree(<2>)

        Returns tuple.
        """
        result = []
        result.append(self)
        current = self._parent
        while current is not None:
            result.append(current)
            current = current._parent
        return tuple(result)

    def _get_position(self):
        """
        Gets position.

        ..  container:: example

            Gets position:

            >>> items = [[[0, 1], [2, 3]], [4, 5]]
            >>> tree = baca.Tree(items=items)

            >>> tree[1]._get_position()
            (1,)

        Position of node defined relative to root.

        Returns tuple of zero or more nonnegative integers.
        """
        result = []
        for node in self._get_parentage():
            if node._parent is not None:
                result.append(node._get_index_in_parent())
        result.reverse()
        return tuple(result)

    def _get_position_of_descendant(self, descendant):
        """
        Gets position of ``descendent`` relative to node rather than relative to root.

        ..  container:: example

            Gets position of descendant:

            >>> items = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = baca.Tree(items=items)

            >>> tree[3]._get_position_of_descendant(tree[3][0])
            (0,)

        Returns tuple of zero or more nonnegative integers.
        """
        if descendant is self:
            return ()
        else:
            return descendant._get_position()[len(self._get_position()) :]

    def _index(self, node):
        for i, current_node in enumerate(self):
            if current_node is node:
                return i
        raise ValueError(f"not in tree: {node!r}.")

    def _initialize_internal_nodes(self, items):
        children = []
        for item in items:
            expression = getattr(item, "_expression", None)
            child = type(self)(items=item, item_class=self.item_class)
            child._expression = expression
            child._parent = self
            children.append(child)
        self._children = children
        return children

    def _initialize_payload(self, payload):
        if isinstance(payload, type(self)):
            assert not len(payload)
            payload = payload._payload
        if self.item_class is not None:
            payload = self.item_class(payload)
        self._payload = payload
        return payload

    def _is_at_level(self, level):
        if (0 <= level and self._get_level() == level) or self._get_level(
            negative=True
        ) == level:
            return True
        else:
            return False

    def _is_leaf(self):
        return self._get_level(negative=True) == -1

    def _is_leftmost_leaf(self):
        if not self._is_leaf():
            return False
        return self._get_index_in_parent() == 0

    def _is_rightmost_leaf(self):
        if not self._is_leaf():
            return False
        index_in_parent = self._get_index_in_parent()
        parentage = self._get_parentage()
        parent = parentage[1]
        return index_in_parent == len(parent) - 1

    def _is_valid_level(self, level):
        maximum_absolute_level = self._get_depth() + 1
        if maximum_absolute_level < abs(level):
            return False
        return True

    def _iterate_depth_first(self, reverse=False):
        """
        Iterates depth-first.

        ..  container:: example

            Iterates tree depth-first from left to right:

            >>> items = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = baca.Tree(items=items)

            >>> for node in tree._iterate_depth_first(): node
            Tree(<4>)
            Tree(<2>)
            Tree(<1>)
            Tree(<1>)
            Tree(<2>)
            Tree(<1>)
            Tree(<1>)
            Tree(<2>)
            Tree(<1>)
            Tree(<1>)
            Tree(<2>)
            Tree(<1>)
            Tree(<1>)

        ..  container::

            Iterates tree depth-first from right to left:

            >>> for node in tree._iterate_depth_first(reverse=True): node
            Tree(<4>)
            Tree(<2>)
            Tree(<1>)
            Tree(<1>)
            Tree(<2>)
            Tree(<1>)
            Tree(<1>)
            Tree(<2>)
            Tree(<1>)
            Tree(<1>)
            Tree(<2>)
            Tree(<1>)
            Tree(<1>)

        Returns generator.
        """
        yield self
        iterable_self = self
        if reverse:
            iterable_self = reversed(self)
        for x in iterable_self:
            for y in x._iterate_depth_first(reverse=reverse):
                yield y

    def _remove_node(self, node):
        node._parent._children.remove(node)
        node._parent = None

    def _remove_to_root(self, reverse=False):
        """
        Removes node and all nodes left of node to root.

        ..container:: example

            Removes node and all nodes left of node to root:

            >>> items = [[0, 1], [2, 3], [4, 5], [6, 7]]

            >>> tree = baca.Tree(items=items)
            >>> tree[0][0]._remove_to_root()
            >>> tree.get_payload(nested=True)
            [[1], [2, 3], [4, 5], [6, 7]]

            >>> tree = baca.Tree(items=items)
            >>> tree[0][1]._remove_to_root()
            >>> tree.get_payload(nested=True)
            [[2, 3], [4, 5], [6, 7]]

            >>> tree = baca.Tree(items=items)
            >>> tree[1]._remove_to_root()
            >>> tree.get_payload(nested=True)
            [[4, 5], [6, 7]]

        Modifies in-place to root.

        Returns none.
        """
        # trim left-siblings of self and self
        parent = self._parent
        if reverse:
            iterable_parent = reversed(parent)
        else:
            iterable_parent = parent[:]
        for sibling in iterable_parent:
            sibling._parent._remove_node(sibling)
            # break and do not remove siblings to right of self
            if sibling is self:
                break
        # trim parentage
        for node in parent._get_parentage():
            if node._parent is not None:
                iterable_parent = node._parent[:]
                if reverse:
                    iterable_parent = reversed(node._parent)
                else:
                    iterable_parent = node._parent[:]
                for sibling in iterable_parent:
                    if sibling is node:
                        # remove node now if it was emptied earlier
                        if not len(sibling):
                            sibling._parent._remove_node(sibling)
                        break
                    else:
                        sibling._parent._remove_node(sibling)

    def _set_leaf_item(self, item):
        assert self._is_leaf(), repr(self)
        self._items = item
        self._payload = item

    ### PUBLIC PROPERTIES ###

    @property
    def item_class(self):
        """
        Gets item class.

        ..  container:: example

            Coerces input:

            >>> items = [[1.1, 2.2], [8.8, 9.9]]
            >>> tree = baca.Tree(items=items, item_class=int)

            >>> for node in tree.iterate(level=-1):
            ...     node
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)

            >>> tree.get_payload(nested=True)
            [[1, 2], [8, 9]]

        Defaults to none.

        Set to class or none.

        Returns class or none.
        """
        return self._item_class

    @property
    def items(self):
        """
        Gets items.

        ..  container:: example

            Gets items:

            >>> items = [[[0, 1], [2, 3]], [4, 5]]
            >>> tree = baca.Tree(items=items)

            >>> for item in tree.items:
            ...     item
            Tree(<2>)
            Tree(<2>)

        ..  container:: example

            Returns list:

            >>> isinstance(tree.items, list)
            True

        """
        return self._items

    ### PUBLIC METHODS ###

    def get_payload(self, nested=False, reverse=False):
        """
        Gets payload.

        ..  container:: example

            Gets payload:

            >>> items = [[[0, 1], [2, 3]], [4, 5]]
            >>> tree = baca.Tree(items=items)

            >>> tree.get_payload()
            [0, 1, 2, 3, 4, 5]

        ..  container:: example

            Gets nested payload:

            >>> tree.get_payload(nested=True)
            [[[0, 1], [2, 3]], [4, 5]]

        ..  container:: example

            Gets payload in reverse:

            >>> tree.get_payload(reverse=True)
            [5, 4, 3, 2, 1, 0]

        Nested payload in reverse is not yet implemented.

        Returns list.
        """
        result = []
        if nested:
            if reverse:
                raise NotImplementedError
            if self._payload is not None:
                return self._payload
            else:
                for child in self._noncyclic_children:
                    if child._payload is not None:
                        result.append(child._payload)
                    else:
                        result.append(child.get_payload(nested=True))
        else:
            for leaf_node in self.iterate(-1, reverse=reverse):
                result.append(leaf_node._payload)
        return result

    def iterate(self, level=None, reverse=False):
        """
        Iterates tree at optional ``level``.

        ..  container:: example

            Example tree:

            >>> items = [[[0, 1], [2, 3]], [4, 5]]
            >>> tree = baca.Tree(items=items)
            >>> abjad.graph(tree) # doctest: +SKIP

            Iterates all levels:

            >>> for node in tree.iterate():
            ...     node
            Tree(<2>)
            Tree(<2>)
            Tree(<2>)
            Tree(<1>)
            Tree(<1>)
            Tree(<2>)
            Tree(<1>)
            Tree(<1>)
            Tree(<2>)
            Tree(<1>)
            Tree(<1>)

            Iterates all levels in reverse:

            >>> for node in tree.iterate(reverse=True):
            ...     node
            Tree(<2>)
            Tree(<2>)
            Tree(<1>)
            Tree(<1>)
            Tree(<2>)
            Tree(<2>)
            Tree(<1>)
            Tree(<1>)
            Tree(<2>)
            Tree(<1>)
            Tree(<1>)

            Iterates select levels:

            >>> for node in tree.iterate(level=0):
            ...     node
            Tree(<2>)

            >>> for node in tree.iterate(level=1):
            ...     node
            Tree(<2>)
            Tree(<2>)

            >>> for node in tree.iterate(level=2):
            ...     node
            Tree(<2>)
            Tree(<2>)
            Tree(<1>)
            Tree(<1>)

            >>> for node in tree.iterate(level=3):
            ...     node
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)

            >>> for node in tree.iterate(level=-4):
            ...     node
            Tree(<2>)

            >>> for node in tree.iterate(level=-3):
            ...     node
            Tree(<2>)

            >>> for node in tree.iterate(level=-2):
            ...     node
            Tree(<2>)
            Tree(<2>)
            Tree(<2>)

            >>> for node in tree.iterate(level=-1):
            ...     node
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)

            Iterates select levels in reverse:

            >>> for node in tree.iterate(level=0, reverse=True):
            ...     node
            Tree(<2>)

            >>> for node in tree.iterate(level=1, reverse=True):
            ...     node
            Tree(<2>)
            Tree(<2>)

            >>> for node in tree.iterate(level=2, reverse=True):
            ...     node
            Tree(<1>)
            Tree(<1>)
            Tree(<2>)
            Tree(<2>)

            >>> for node in tree.iterate(level=3, reverse=True):
            ...     node
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)

            >>> for node in tree.iterate(level=-4, reverse=True):
            ...     node
            Tree(<2>)

            >>> for node in tree.iterate(level=-3, reverse=True):
            ...     node
            Tree(<2>)

            >>> for node in tree.iterate(level=-2, reverse=True):
            ...     node
            Tree(<2>)
            Tree(<2>)
            Tree(<2>)

            >>> for node in tree.iterate(level=-1, reverse=True):
            ...     node
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)
            Tree(<1>)

        Returns generator.
        """
        for node in self._iterate_depth_first(reverse=reverse):
            if level is None:
                yield node
            elif 0 <= level:
                if node._get_level() == level:
                    yield node
            else:
                if node._get_level(negative=True) == level:
                    yield node
