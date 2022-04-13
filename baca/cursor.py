"""
Classes.
"""
import collections
import dataclasses
import typing

import abjad


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
        assert isinstance(self.position, int | type(None)), repr(self.position)
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
            Cursor(source=CyclicTuple(items=(PitchClassSegment([1, 1.5, 11]), PitchClassSegment([10, 2, 1.5]))), cyclic=True, position=None, singletons=False, suppress_exception=False)

        Coerces numeric ``pitch_class_segments``

        Returns cursor.
        """
        cells = []
        for pitch_class_segment in pitch_class_segments:
            pitch_class_segment = abjad.PitchClassSegment(pitch_class_segment)
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
