"""
Classes.
"""
import collections
import dataclasses
import typing

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
    cyclic: bool = False
    position: int | None = None
    singletons: bool = False
    suppress_exception: bool = False

    def __post_init__(self):
        self.cyclic = bool(self.cyclic)
        self.source = self.source or ()
        assert isinstance(self.source, collections.abc.Iterable), repr(self.source)
        if self.cyclic:
            self.source = abjad.CyclicTuple(self.source)
        assert isinstance(self.position, (int, type(None))), repr(self.position)
        self.singletons = bool(self.singletons)
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
            Cursor(source=CyclicTuple(items=(NumberedPitchClassSegment([1, 1.5, 11]), NumberedPitchClassSegment([10, 2, 1.5]))), cyclic=True, position=None, singletons=False, suppress_exception=False)

        Coerces numeric ``pitch_class_segments``

        Returns cursor.
        """
        cells = []
        for pitch_class_segment in pitch_class_segments:
            pitch_class_segment = abjad.NumberedPitchClassSegment(pitch_class_segment)
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
