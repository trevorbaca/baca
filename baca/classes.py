import collections
import copy
import inspect
import itertools
import typing

import uqbar

import abjad

### CLASSES ###


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

    ### CLASS VARIABLES ###

    __slots__ = ("_current", "_start")

    ### INITIALIZER ###

    def __init__(self, *, start=0):
        self._start = start
        self._current = start

    ### SPECIAL METHODS ###

    def __call__(self, count=1):
        """
        Calls counter.

        Returns new value.
        """
        current = self.current + count
        self._current = current
        return count

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def current(self):
        """
        Gets current value.

        Returns integer.
        """
        return self._current

    @property
    def start(self):
        """
        Gets start value.

        Set to integer.

        Returns integer.
        """
        return self._start


class Cursor:
    """
    Cursor.

    ..  container:: example

        Gets elements one at a time:

        >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
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

        >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
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

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_cyclic",
        "_lone_items",
        "_position",
        "_singletons",
        "_source",
        "_suppress_exception",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        source=None,
        *,
        cyclic=None,
        position=None,
        singletons=None,
        suppress_exception=None,
    ):
        if cyclic is not None:
            cyclic = bool(cyclic)
        self._cyclic = cyclic
        source = source or ()
        assert isinstance(source, collections.abc.Iterable), repr(source)
        if cyclic:
            source = abjad.CyclicTuple(source)
        self._source = source
        assert isinstance(position, (int, type(None))), repr(position)
        self._position = position
        if singletons is not None:
            singletons = bool(singletons)
        self._singletons = singletons
        if suppress_exception is not None:
            suppress_exception = bool(suppress_exception)
        self._suppress_exception = suppress_exception

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a cursor with keyword
        arguments equal to this cursor.

        Returns true or false.
        """
        return super().__eq__(argument)

    def __getitem__(self, argument):
        """
        Gets item from cursor.

        ..  container:: example

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
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

    def __hash__(self):
        """
        Hashes cursor.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super().__hash__()

    def __iter__(self, count=1):
        """
        Iterates cursor.

        ..  container:: example

            Iterates acyclic cursor:

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
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

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
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

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
            >>> cursor = baca.Cursor(source=source)
            >>> len(cursor)
            4

        Defined equal to length of cursor source.

        Returns nonnegative integer.
        """
        return len(self.source)

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PUBLIC PROPERTIES ###

    @property
    def cyclic(self):
        """
        Is true when cursor is cyclic.

        Set to true, false or none.

        Defaults to none.

        Returns true, false or none.
        """
        return self._cyclic

    @property
    def is_exhausted(self):
        """
        Is true when cursor is exhausted.

        ..  container:: example

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
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

    @property
    def position(self):
        """
        Gets position.

        ..  container:: example

            Position starts at none by default:

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
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

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
            >>> cursor = baca.Cursor(
            ...     source=source,
            ...     cyclic=True,
            ...     position=None,
            ...     )

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

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
            >>> cursor = baca.Cursor(
            ...     source=source,
            ...     cyclic=True,
            ...     position=0,
            ...     )

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

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
            >>> cursor = baca.Cursor(
            ...     source=source,
            ...     cyclic=True,
            ...     position=0,
            ...     )

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

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
            >>> cursor = baca.Cursor(
            ...     source=source,
            ...     cyclic=True,
            ...     position=-1,
            ...     )

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

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
            >>> cursor = baca.Cursor(
            ...     source=source,
            ...     cyclic=True,
            ...     position=-1,
            ...     )

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

        Returns tuple.
        """
        return self._position

    @property
    def singletons(self):
        """
        Is true when cursor returns singletons not enclosed within a list.
        If false when cursor returns singletons enclosed within a list.

        ..  container:: example

            Returns singletons enclosed within a list:

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
            >>> cursor = baca.Cursor(
            ...     source=source,
            ...     suppress_exception=True,
            ...     )

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

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
            >>> cursor = baca.Cursor(
            ...     source=source,
            ...     singletons=True,
            ...     suppress_exception=True,
            ...     )

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
        return self._singletons

    @property
    def source(self):
        """
        Gets source.

        ..  container:: example

            List source:

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
            >>> cursor = baca.Cursor(source=source)

            >>> cursor.source
            [13, 'da capo', Note("cs'8."), 'rit.']

        ..  container:: example

            Cyclic tuple source:

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
            >>> cursor = baca.Cursor(source=source, cyclic=True)

            >>> cursor.source
            CyclicTuple([13, 'da capo', Note("cs'8."), 'rit.'])

        Returns source.
        """
        return self._source

    @property
    def suppress_exception(self):
        """
        Is true when cursor returns none on exhaustion.
        Is false when cursor raises exception on exhaustion.

        ..  container:: example

            Exhausted cursor raises exception:

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
            >>> cursor = baca.Cursor(source=source)
            >>> cursor.is_exhausted
            False

            >>> cursor.next()
            [13]

            >>> cursor.next()
            ['da capo']

            >>> cursor.next()
            [Note("cs'8.")]

            >>> cursor.next()
            ['rit.']

            >>> cursor.next()
            Traceback (most recent call last):
                ...
            Exception: cursor only 4.

            >>> cursor.next()
            Traceback (most recent call last):
                ...
            Exception: cursor only 4.

        ..  container:: example

            Exhausted cursor returns none:

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
            >>> cursor = baca.Cursor(
            ...     source=source,
            ...     suppress_exception=True,
            ...     )
            >>> cursor.is_exhausted
            False

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

        """
        return self._suppress_exception

    ### PUBLIC METHODS ###

    @staticmethod
    def from_pitch_class_segments(pitch_class_segments):
        """
        Makes cursor from ``pitch_class_segments``

        ..  container:: example

            Makes cursor from pitch-class segments:

            >>> number_lists = [[13, 13.5, 11], [-2, 2, 1.5]]
            >>> cursor = baca.Cursor.from_pitch_class_segments(
            ...     number_lists,
            ...     )

            >>> string = abjad.storage(cursor)
            >>> print(string)
            baca.Cursor(
                source=abjad.CyclicTuple(
                    [
                        abjad.PitchClassSegment(
                            (
                                abjad.NumberedPitchClass(1),
                                abjad.NumberedPitchClass(1.5),
                                abjad.NumberedPitchClass(11),
                                ),
                            item_class=abjad.NumberedPitchClass,
                            ),
                        abjad.PitchClassSegment(
                            (
                                abjad.NumberedPitchClass(10),
                                abjad.NumberedPitchClass(2),
                                abjad.NumberedPitchClass(1.5),
                                ),
                            item_class=abjad.NumberedPitchClass,
                            ),
                        ]
                    ),
                cyclic=True,
                )

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

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
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

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
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

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
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

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
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

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
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

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
            >>> cursor = baca.Cursor(source=source)

            >>> cursor.next(count=99)
            Traceback (most recent call last):
                ...
            Exception: cursor only 4.

        Returns tuple.
        """
        result = []
        if self.position is None:
            self._position = 0
        if 0 < count:
            for i in range(count):
                try:
                    element = self.source[self.position]
                    result.append(element)
                except IndexError:
                    if not self.suppress_exception:
                        raise Exception(f"cursor only {len(self.source)}.")
                self._position += 1
        elif count < 0:
            for i in range(abs(count)):
                self._position -= 1
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

            >>> source = [13, 'da capo', abjad.Note("cs'8."), 'rit.']
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
        self._position = 0


class Expression(abjad.Expression):
    r"""
    Expression.

    ..  container:: example expression

        Transposes collections:

        >>> collections = [
        ...     abjad.PitchClassSegment([0, 1, 2, 3]),
        ...     abjad.PitchClassSegment([6, 7, 8, 9]),
        ...     ]

        >>> transposition = baca.pitch_class_segment()
        >>> transposition = transposition.transpose(n=3)
        >>> expression = baca.sequence(name='J')
        >>> expression = expression.map(transposition)

        >>> for collection in expression(collections):
        ...     collection
        ...
        PitchClassSegment([3, 4, 5, 6])
        PitchClassSegment([9, 10, 11, 0])

        >>> expression.get_string()
        'T3(X) /@ J'

        >>> markup = expression.get_markup()
        >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(markup)
            >>> print(string)
            \markup {
                \line
                    {
                        \concat
                            {
                                T
                                \sub
                                    3
                                \bold
                                    X
                            }
                        /@
                        \bold
                            J
                    }
                }

    ..  container:: example expression

        Transposes and joins:

        >>> collections = [
        ...     abjad.PitchClassSegment([0, 1, 2, 3]),
        ...     abjad.PitchClassSegment([6, 7, 8, 9]),
        ...     ]

        >>> transposition = baca.pitch_class_segment()
        >>> transposition = transposition.transpose(n=3)
        >>> expression = baca.sequence(name='J')
        >>> expression = expression.map(transposition)
        >>> expression = expression.join()

        >>> expression(collections)
        Sequence([PitchClassSegment([3, 4, 5, 6, 9, 10, 11, 0])])

        >>> expression.get_string()
        'join(T3(X) /@ J)'

        >>> markup = expression.get_markup()
        >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(markup)
            >>> print(string)
            \markup {
                \concat
                    {
                        join(
                        \line
                            {
                                \concat
                                    {
                                        T
                                        \sub
                                            3
                                        \bold
                                            X
                                    }
                                /@
                                \bold
                                    J
                            }
                        )
                    }
                }

    ..  container:: example expression

        Transposes and flattens:

        >>> collections = [
        ...     abjad.PitchClassSegment([0, 1, 2, 3]),
        ...     abjad.PitchClassSegment([6, 7, 8, 9]),
        ...     ]

        >>> transposition = baca.pitch_class_segment()
        >>> transposition = transposition.transpose(n=3)
        >>> expression = baca.sequence(name='J')
        >>> expression = expression.map(transposition)
        >>> expression = expression.flatten(depth=-1)

        >>> for collection in expression(collections):
        ...     collection
        ...
        NumberedPitchClass(3)
        NumberedPitchClass(4)
        NumberedPitchClass(5)
        NumberedPitchClass(6)
        NumberedPitchClass(9)
        NumberedPitchClass(10)
        NumberedPitchClass(11)
        NumberedPitchClass(0)

        >>> expression.get_string()
        'flatten(T3(X) /@ J, depth=-1)'

        >>> markup = expression.get_markup()
        >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(markup)
            >>> print(string)
            \markup {
                \concat
                    {
                        flatten(
                        \line
                            {
                                \concat
                                    {
                                        T
                                        \sub
                                            3
                                        \bold
                                            X
                                    }
                                /@
                                \bold
                                    J
                            }
                        ", depth=-1)"
                    }
                }

    ..  container:: example expression

        Transposes and repartitions:

        >>> collections = [
        ...     abjad.PitchClassSegment([0, 1, 2, 3]),
        ...     abjad.PitchClassSegment([6, 7, 8, 9]),
        ...     ]

        >>> transposition = baca.pitch_class_segment().transpose(n=3)
        >>> expression = baca.sequence(name='J').map(transposition)
        >>> expression = expression.flatten(depth=-1).partition([3])
        >>> expression = expression.map(baca.pitch_class_segment())

        >>> for collection in expression(collections):
        ...     collection
        ...
        PitchClassSegment([3, 4, 5])
        PitchClassSegment([6, 9, 10])
        PitchClassSegment([11, 0])

        >>> expression.get_string()
        'X /@ P[3](flatten(T3(X) /@ J, depth=-1))'

        >>> markup = expression.get_markup()
        >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(markup)
            >>> print(string)
            \markup {
                \line
                    {
                        \bold
                            X
                        /@
                        \concat
                            {
                                P
                                \sub
                                    [3]
                                \concat
                                    {
                                        flatten(
                                        \line
                                            {
                                                \concat
                                                    {
                                                        T
                                                        \sub
                                                            3
                                                        \bold
                                                            X
                                                    }
                                                /@
                                                \bold
                                                    J
                                            }
                                        ", depth=-1)"
                                    }
                            }
                    }
                }

    ..  container:: example expression

        Transposes, repartitions and ox-plows:

        >>> collections = [
        ...     abjad.PitchClassSegment([0, 1, 2, 3]),
        ...     abjad.PitchClassSegment([6, 7, 8, 9]),
        ...     ]

        >>> transposition = baca.pitch_class_segment().transpose(n=3)
        >>> expression = baca.sequence(name='J').map(transposition)
        >>> expression = expression.flatten(depth=-1).partition([3])
        >>> expression = expression.map(baca.pitch_class_segment())
        >>> expression = expression.boustrophedon()

        >>> for collection in expression(collections):
        ...     collection
        ...
        PitchClassSegment([3, 4, 5])
        PitchClassSegment([6, 9, 10])
        PitchClassSegment([11, 0])
        PitchClassSegment([11])
        PitchClassSegment([10, 9, 6])
        PitchClassSegment([5, 4, 3])

        >>> expression.get_string()
        'β2(X /@ P[3](flatten(T3(X) /@ J, depth=-1)))'

        >>> markup = expression.get_markup()
        >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(markup)
            >>> print(string)
            \markup {
                \concat
                    {
                        β
                        \super
                            2
                        \line
                            {
                                \bold
                                    X
                                /@
                                \concat
                                    {
                                        P
                                        \sub
                                            [3]
                                        \concat
                                            {
                                                flatten(
                                                \line
                                                    {
                                                        \concat
                                                            {
                                                                T
                                                                \sub
                                                                    3
                                                                \bold
                                                                    X
                                                            }
                                                        /@
                                                        \bold
                                                            J
                                                    }
                                                ", depth=-1)"
                                            }
                                    }
                            }
                    }
                }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Classes"

    ### PRIVATE METHODS ###

    def _evaluate_accumulate(self, *arguments):
        assert len(arguments) == 1, repr(arguments)
        globals_ = self._make_globals()
        assert "__argument_0" not in globals_
        __argument_0 = arguments[0]
        assert isinstance(__argument_0, Sequence), repr(__argument_0)
        class_ = type(__argument_0)
        operands = self.map_operand
        globals_["__argument_0"] = __argument_0
        globals_["class_"] = class_
        globals_["operands"] = operands
        statement = "__argument_0.accumulate(operands=operands)"
        try:
            result = eval(statement, globals_)
        except (NameError, SyntaxError, TypeError) as e:
            raise Exception(f"{statement!r} raises {e!r}.")
        return result

    ### PUBLIC METHODS ###


#    def select(self, **keywords) -> "Expression":
#        r"""
#        Makes select expression.
#
#        ..  container:: example
#
#            Makes expression to select leaves:
#
#            ..  container:: example
#
#                >>> staff = abjad.Staff()
#                >>> staff.extend("<c' bf'>8 <g' a'>8")
#                >>> staff.extend("af'8 r8")
#                >>> staff.extend("r8 gf'8")
#                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
#                >>> abjad.show(staff, align_tags=89) # doctest: +SKIP
#
#                ..  docs::
#
#                    >>> string = abjad.lilypond(staff)
#                    >>> print(string)
#                    \new Staff
#                    {
#                        \time 2/8
#                        <c' bf'>8
#                        <g' a'>8
#                        af'8
#                        r8
#                        r8
#                        gf'8
#                    }
#
#            ..  container:: example expression
#
#                >>> expression = baca.Expression()
#                >>> expression = expression.select()
#                >>> expression = expression.leaves()
#
#                >>> for leaf in expression(staff):
#                ...     leaf
#                ...
#                Chord("<c' bf'>8")
#                Chord("<g' a'>8")
#                Note("af'8")
#                Rest('r8')
#                Rest('r8')
#                Note("gf'8")
#
#        """
#        class_ = Selection
#        callback = self._make_initializer_callback(
#            class_, callback_class=Expression, module_names=["baca"], **keywords
#        )
#        expression = self.append_callback(callback)
#        return abjad.new(expression, proxy_class=class_, template="baca")


class PaddedTuple:
    """
    Padded tuple.

    ..  container:: example

        >>> tuple_ = baca.PaddedTuple('abcd', pad=2)

        >>> tuple_
        PaddedTuple(['a', 'b', 'c', 'd'], pad=2)

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

    Padded tuples overload the item-getting method of built-in tuples.

    Padded tuples return a value for any integer index.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_items", "_pad")

    ### INITIALIZER ###

    def __init__(self, items: typing.Sequence = None, pad: int = 1) -> None:
        items = items or ()
        items = tuple(items)
        self._items: typing.Tuple = items
        assert isinstance(pad, int), repr(pad)
        assert 1 <= pad, repr(pad)
        self._pad = pad

    ### SPECIAL METHODS ###

    def __contains__(self, item) -> bool:
        """
        Is true when padded tuple contains ``item``.
        """
        return self._items.__contains__(item)

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a tuple with ``items`` and ``pad`` equal
        to those of this padded tuple.
        """
        if isinstance(argument, tuple):
            return self._items == argument
        elif isinstance(argument, type(self)):
            return self._items == argument._items
        return False

    def __getitem__(self, argument) -> typing.Any:
        """
        Gets item or slice identified by ``argument``.

        ..  container:: example

            Gets slice open at right:

            >>> baca.PaddedTuple('abcd', pad=3)[2:]
            ('c', 'd')

            Gets slice closed at right:

            >>> slice_ = baca.PaddedTuple('abcd', pad=3)[:15]
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
        return self._items.__getitem__(argument)

    def __hash__(self) -> int:
        """
        Hashes padded tuple.

        Redefined in tandem with __eq__.
        """
        return super().__hash__()

    def __iter__(self) -> typing.Iterator:
        """
        Iterates padded tuple.

        Iterates items only once.

        Does not iterate infinitely.
        """
        return self._items.__iter__()

    def __len__(self) -> int:
        """
        Gets length of padded tuple.

        ..  container:: example

            >>> len(baca.PaddedTuple('abcd', pad=3))
            4

        """
        assert isinstance(self._items, tuple)
        return self._items.__len__()

    def __repr__(self):
        """
        Gets interpreter representation.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=[list(self._items)],
        )

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

    ### PUBLIC PROPERTIES ###

    @property
    def items(self) -> typing.Tuple:
        """
        Gets items.

        ..  container:: example

            >>> baca.PaddedTuple('abcd', pad=1).items
            ('a', 'b', 'c', 'd')

            >>> baca.PaddedTuple([1, 2, 3, 4], pad=1).items
            (1, 2, 3, 4)

        """
        return self._items

    @property
    def pad(self) -> typing.Optional[int]:
        """
        Gets pad.

        ..  container:: example

            With nonnegative indices:

            >>> tuple_ = baca.PaddedTuple('abcd', pad=1)
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

            >>> tuple_ = baca.PaddedTuple('abcd', pad=2)
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

            >>> tuple_ = baca.PaddedTuple('abcd', pad=3)
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

            >>> tuple_ = baca.PaddedTuple('abcd', pad=4)
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

            >>> tuple_ = baca.PaddedTuple('abcd', pad=1)
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

            >>> tuple_ = baca.PaddedTuple('abcd', pad=2)
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

            >>> tuple_ = baca.PaddedTuple('abcd', pad=3)
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

            >>> tuple_ = baca.PaddedTuple('abcd', pad=4)
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

        """
        return self._pad


class SchemeManifest:
    """
    Scheme manifest.

    New functions defined in ``~/baca/lilypond/baca.ily`` must
    currently be added here by hand.

    TODO: eliminate duplication. Define custom Scheme functions here
    (``SchemeManifest``) and teach ``SchemeManifest`` to write
    ``~/baca/lilypond/baca.ily`` automatically.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Classes"

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
            >>> scheme_manifest.dynamic_to_steady_state('sfz-p')
            'p'

        Returns string.
        """
        for dynamic_, steady_state in self._dynamics:
            if dynamic_ == dynamic:
                return steady_state
            if dynamic_ == "baca-" + dynamic:
                return steady_state
        raise KeyError(dynamic)


class Selection(abjad.Selection):
    """
    Selection.

    ..  container:: example

        >>> baca.select()
        baca

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Classes"

    __slots__ = ()

    ### PUBLIC METHODS ###

    def chead(
        self, n: int, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Note, abjad.Expression]:
        r"""
        Selects chord head ``n``.

        ..  container:: example

            Selects chord head -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).chead(-1)

                >>> result
                Chord("<fs' gs'>4")

            ..  container:: example expression

                >>> selector = baca.chead(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<fs' gs'>4")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        \abjad-color-music #'green
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.cheads(exclude=exclude)[n]

    def cheads(
        self, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects chord heads.

        ..  container:: example

            Selects chord heads:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).cheads()

                >>> for item in result:
                ...     item
                ...
                Chord("<a'' b''>16")
                Chord("<d' e'>4")
                Chord("<a'' b''>16")
                Chord("<e' fs'>4")
                Chord("<a'' b''>16")
                Chord("<fs' gs'>4")

            ..  container:: example expression

                >>> selector = baca.cheads()
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<a'' b''>16")
                Chord("<d' e'>4")
                Chord("<a'' b''>16")
                Chord("<e' fs'>4")
                Chord("<a'' b''>16")
                Chord("<fs' gs'>4")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        e'16
                        \abjad-color-music #'blue
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return super().leaves(abjad.Chord, exclude=exclude, head=True)

    def clparts(
        self, counts: typing.Sequence[int], *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects leaves cyclically partitioned by ``counts`` (with overhang).

        ..  container:: example

            Selects leaves cyclically partitioned 2, 3, 4:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).clparts([2, 3, 4])

                >>> for item in result:
                ...     item
                ...
                Selection([Rest('r16'), Note("bf'16")])
                Selection([Chord("<a'' b''>16"), Note("c'16"), Chord("<d' e'>4")])
                Selection([Chord("<d' e'>16"), Rest('r16'), Note("bf'16"), Chord("<a'' b''>16")])
                Selection([Note("d'16"), Chord("<e' fs'>4")])
                Selection([Chord("<e' fs'>16"), Rest('r16'), Note("bf'16")])
                Selection([Chord("<a'' b''>16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.clparts([2, 3, 4])
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Rest('r16'), Note("bf'16")])
                Selection([Chord("<a'' b''>16"), Note("c'16"), Chord("<d' e'>4")])
                Selection([Chord("<d' e'>16"), Rest('r16'), Note("bf'16"), Chord("<a'' b''>16")])
                Selection([Note("d'16"), Chord("<e' fs'>4")])
                Selection([Chord("<e' fs'>16"), Rest('r16'), Note("bf'16")])
                Selection([Chord("<a'' b''>16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'blue
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9 {
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'red
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'blue
                        e'16
                        \abjad-color-music #'blue
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'blue
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return (
            super()
            .leaves(exclude=exclude)
            .partition_by_counts(counts=counts, cyclic=True, overhang=True)
        )

    def cmgroups(
        self, counts: typing.List[int] = [1], *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Expression, "Selection"]:
        r"""
        Partitions measure-grouped leaves (cyclically).

        ..  container:: example

            Partitions measure-grouped leaves into pairs:

            ..  container:: example

                >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r d''")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
                >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = baca.select(staff).cmgroups([2])

                >>> for item in result:
                ...     item
                ...
                Selection([Rest('r8'), Note("d'8"), Note("e'8"), Note("f'8")])
                Selection([Note("g'8"), Note("a'8"), Note("b'8"), Rest('r8')])

            ..  container:: example expression

                >>> selector = baca.select().cmgroups([2])
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Rest('r8'), Note("d'8"), Note("e'8"), Note("f'8")])
                Selection([Note("g'8"), Note("a'8"), Note("b'8"), Rest('r8')])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'red
                    f'8
                    \time 3/8
                    \abjad-color-music #'blue
                    g'8
                    \abjad-color-music #'blue
                    a'8
                    \abjad-color-music #'blue
                    b'8
                    \time 1/8
                    \abjad-color-music #'blue
                    r8
                    d''8
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = self.leaves(exclude=exclude)
        result = result.group_by_measure()
        result = result.partition_by_counts(counts, cyclic=True)
        result_ = result.map(select().flatten())
        assert isinstance(result_, Selection), repr(result_)
        return result_

    def enchain(
        self, counts: typing.Sequence[int]
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Enchains items in selection.

        ..  container:: example

            Enchains leaves in alternating groups of 5:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).leaves().enchain([5])

                >>> for item in result:
                ...     item
                Selection([Rest('r16'), Note("bf'16"), Chord("<a'' b''>16"), Note("c'16"), Chord("<d' e'>4")])
                Selection([Chord("<d' e'>4"), Chord("<d' e'>16"), Rest('r16'), Note("bf'16"), Chord("<a'' b''>16")])
                Selection([Chord("<a'' b''>16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16"), Rest('r16')])
                Selection([Rest('r16'), Note("bf'16"), Chord("<a'' b''>16"), Note("e'16"), Chord("<fs' gs'>4")])
                Selection([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.leaves().enchain([5])
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Rest('r16'), Note("bf'16"), Chord("<a'' b''>16"), Note("c'16"), Chord("<d' e'>4")])
                Selection([Chord("<d' e'>4"), Chord("<d' e'>16"), Rest('r16'), Note("bf'16"), Chord("<a'' b''>16")])
                Selection([Chord("<a'' b''>16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16"), Rest('r16')])
                Selection([Rest('r16'), Note("bf'16"), Chord("<a'' b''>16"), Note("e'16"), Chord("<fs' gs'>4")])
                Selection([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> for i, selection in enumerate(result):
                ...     if i % 2 == 0:
                ...         color, direction = 'red', abjad.Up
                ...     else:
                ...         color, direction = 'blue', abjad.Down
                ...     string = rf'\markup {{ \bold \with-color #{color} * }}'
                ...     for leaf in selection:
                ...         markup = abjad.Markup(string, literal=True)
                ...         markup = abjad.new(markup, direction=direction)
                ...         abjad.attach(markup, leaf)

                >>> abjad.override(staff).TextScript.staff_padding = 6
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #6
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        ^ \markup {
                            \bold
                                \with-color
                                    #red
                                    *
                            }
                        bf'16
                        ^ \markup {
                            \bold
                                \with-color
                                    #red
                                    *
                            }
                        <a'' b''>16
                        ^ \markup {
                            \bold
                                \with-color
                                    #red
                                    *
                            }
                        c'16
                        ^ \markup {
                            \bold
                                \with-color
                                    #red
                                    *
                            }
                        <d' e'>4
                        ^ \markup {
                            \bold
                                \with-color
                                    #red
                                    *
                            }
                        _ \markup {
                            \bold
                                \with-color
                                    #blue
                                    *
                            }
                        ~
                        <d' e'>16
                        _ \markup {
                            \bold
                                \with-color
                                    #blue
                                    *
                            }
                    }
                    \times 8/9 {
                        r16
                        _ \markup {
                            \bold
                                \with-color
                                    #blue
                                    *
                            }
                        bf'16
                        _ \markup {
                            \bold
                                \with-color
                                    #blue
                                    *
                            }
                        <a'' b''>16
                        ^ \markup {
                            \bold
                                \with-color
                                    #red
                                    *
                            }
                        _ \markup {
                            \bold
                                \with-color
                                    #blue
                                    *
                            }
                        d'16
                        ^ \markup {
                            \bold
                                \with-color
                                    #red
                                    *
                            }
                        <e' fs'>4
                        ^ \markup {
                            \bold
                                \with-color
                                    #red
                                    *
                            }
                        ~
                        <e' fs'>16
                        ^ \markup {
                            \bold
                                \with-color
                                    #red
                                    *
                            }
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        ^ \markup {
                            \bold
                                \with-color
                                    #red
                                    *
                            }
                        _ \markup {
                            \bold
                                \with-color
                                    #blue
                                    *
                            }
                        bf'16
                        _ \markup {
                            \bold
                                \with-color
                                    #blue
                                    *
                            }
                        <a'' b''>16
                        _ \markup {
                            \bold
                                \with-color
                                    #blue
                                    *
                            }
                        e'16
                        _ \markup {
                            \bold
                                \with-color
                                    #blue
                                    *
                            }
                        <fs' gs'>4
                        ^ \markup {
                            \bold
                                \with-color
                                    #red
                                    *
                            }
                        _ \markup {
                            \bold
                                \with-color
                                    #blue
                                    *
                            }
                        ~
                        <fs' gs'>16
                        ^ \markup {
                            \bold
                                \with-color
                                    #red
                                    *
                            }
                    }
                }

        Returns new selection (or expression).
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.partition_by_counts(
            counts=counts, cyclic=True, enchain=True, overhang=True
        )

    def grace(
        self, n: int = 0, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Leaf, abjad.Expression]:
        r"""
        Selects grace ``n``.

        ..  container:: example

            Selects grace -1:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
                >>> abjad.attach(container, staff[1])
                >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                >>> abjad.attach(container, staff[1])
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        autoBeaming = ##f
                    }
                    {
                        c'8
                        \grace {
                            cf''16
                            bf'16
                        }
                        \afterGrace
                        d'8
                        {
                            af'16
                            gf'16
                        }
                        e'8
                        f'8
                    }

                >>> baca.select(staff).grace(-1)
                Note("gf'16")

            ..  container:: example expression

                >>> selector = baca.select().grace(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("gf'16")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    \grace {
                        cf''16
                        bf'16
                    }
                    \afterGrace
                    d'8
                    {
                        af'16
                        \abjad-color-music #'green
                        gf'16
                    }
                    e'8
                    f'8
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.graces(exclude=exclude)[n]

    def graces(
        self, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects graces.

        ..  container:: example

            Selects graces:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
                >>> abjad.attach(container, staff[1])
                >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                >>> abjad.attach(container, staff[1])
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        autoBeaming = ##f
                    }
                    {
                        c'8
                        \grace {
                            cf''16
                            bf'16
                        }
                        \afterGrace
                        d'8
                        {
                            af'16
                            gf'16
                        }
                        e'8
                        f'8
                    }

                >>> result = baca.select(staff).graces()

                >>> for item in result:
                ...     item
                ...
                Note("cf''16")
                Note("bf'16")
                Note("af'16")
                Note("gf'16")

            ..  container:: example expression

                >>> selector = baca.select().graces()
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("cf''16")
                Note("bf'16")
                Note("af'16")
                Note("gf'16")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    \grace {
                        \abjad-color-music #'red
                        cf''16
                        \abjad-color-music #'blue
                        bf'16
                    }
                    \afterGrace
                    d'8
                    {
                        \abjad-color-music #'red
                        af'16
                        \abjad-color-music #'blue
                        gf'16
                    }
                    e'8
                    f'8
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.leaves(exclude=exclude, grace=True)

    def hleaf(
        self, n: int = 0, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Leaf, abjad.Expression]:
        r"""
        Selects haupt leaf ``n``.

        ..  container:: example

            Selects haupt leaf 1:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
                >>> abjad.attach(container, staff[1])
                >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                >>> abjad.attach(container, staff[1])
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        autoBeaming = ##f
                    }
                    {
                        c'8
                        \grace {
                            cf''16
                            bf'16
                        }
                        \afterGrace
                        d'8
                        {
                            af'16
                            gf'16
                        }
                        e'8
                        f'8
                    }

                >>> baca.select(staff).hleaf(1)
                Note("d'8")

            ..  container:: example expression

                >>> selector = baca.select().hleaf(1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("d'8")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    \grace {
                        cf''16
                        bf'16
                    }
                    \abjad-color-music #'green
                    \afterGrace
                    d'8
                    {
                        af'16
                        gf'16
                    }
                    e'8
                    f'8
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.hleaves(exclude=exclude)[n]

    def hleaves(
        self, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects haupt leaves.

        ..  container:: example

            Selects haupt leaves:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
                >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
                >>> abjad.attach(container, staff[1])
                >>> container = abjad.AfterGraceContainer("af'16 gf'16")
                >>> abjad.attach(container, staff[1])
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(staff)
                    >>> print(string)
                    \new Staff
                    \with
                    {
                        autoBeaming = ##f
                    }
                    {
                        c'8
                        \grace {
                            cf''16
                            bf'16
                        }
                        \afterGrace
                        d'8
                        {
                            af'16
                            gf'16
                        }
                        e'8
                        f'8
                    }

                >>> result = baca.select(staff).hleaves()

                >>> for item in result:
                ...     item
                ...
                Note("c'8")
                Note("d'8")
                Note("e'8")
                Note("f'8")

            ..  container:: example expression

                >>> selector = baca.select().hleaves()
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("c'8")
                Note("d'8")
                Note("e'8")
                Note("f'8")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \grace {
                        cf''16
                        bf'16
                    }
                    \abjad-color-music #'blue
                    \afterGrace
                    d'8
                    {
                        af'16
                        gf'16
                    }
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'blue
                    f'8
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.leaves(exclude=exclude, grace=False)

    def lleaf(
        self, n: int = 0, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Leaf, abjad.Expression]:
        r"""
        Selects leaf ``n`` from leaves leaked to the left.

        ..  container:: example

            Selects leaf 0 from leaves (leaked to the left) in tuplet 1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> baca.select(staff).tuplets()[1:2].lleaf(0)
                Chord("<d' e'>16")

            ..  container:: example expression

                >>> selector = baca.tuplets()[1:2].lleaf(0)
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<d' e'>16")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        \abjad-color-music #'green
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.lleaves(exclude=exclude)[n]

    def lleak(self) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Leaks to the left.

        ..  container:: example

            Selects runs (each leaked to the left):

            ..  container:: example

                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).runs().map(baca.lleak())

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8")])
                Selection([Rest('r8'), Note("d'8"), Note("e'8")])
                Selection([Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")])

            ..  container:: example expression

                >>> selector = baca.select().runs().map(baca.lleak())
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8")])
                Selection([Rest('r8'), Note("d'8"), Note("e'8")])
                Selection([Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(staff, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'red
                    f'8
                    \abjad-color-music #'red
                    g'8
                    \abjad-color-music #'red
                    a'8
                }

        Returns new selection (or expression).
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.with_previous_leaf()

    def lleaves(
        self, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects leaves, leaked to the left.

        ..  container:: example

            Selects leaves (leaked to the left) in tuplet 1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).tuplets()[1:2].lleaves()

                >>> for item in result:
                ...     item
                ...
                Chord("<d' e'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")

            ..  container:: example expression

                >>> selector = baca.tuplets()[1:2].lleaves()
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<d' e'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9 {
                        \abjad-color-music #'blue
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'red
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.leaves(exclude=exclude).with_previous_leaf()

    def lparts(
        self, counts: typing.Sequence[int], *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects leaves partitioned by ``counts``.

        ..  container:: example

            Selects leaves partitioned 2, 3, 4:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).lparts([2, 3, 4])

                >>> for item in result:
                ...     item
                ...
                Selection([Rest('r16'), Note("bf'16")])
                Selection([Chord("<a'' b''>16"), Note("c'16"), Chord("<d' e'>4")])
                Selection([Chord("<d' e'>16"), Rest('r16'), Note("bf'16"), Chord("<a'' b''>16")])

            ..  container:: example expression

                >>> selector = baca.lparts([2, 3, 4])
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Rest('r16'), Note("bf'16")])
                Selection([Chord("<a'' b''>16"), Note("c'16"), Chord("<d' e'>4")])
                Selection([Chord("<d' e'>16"), Rest('r16'), Note("bf'16"), Chord("<a'' b''>16")])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'blue
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9 {
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return super().leaves(exclude=exclude).partition_by_counts(counts=counts)

    def lt(
        self, n: int, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects logical tie ``n``.

        ..  container:: example

            Selects logical tie -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).lt(-1)

                >>> result
                LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.lt(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        \abjad-color-music #'green
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'green
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.lts(exclude=exclude)[n]

    def ltleaf(
        self, n: int = 0, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects left-trimmed leaf ``n``.

        ..  container:: example

            Selects left-trimmed leaf 0:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 r4 r16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).ltleaf(0)

                >>> result
                Note("bf'16")

            ..  container:: example expression

                >>> selector = baca.ltleaf(0)
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("bf'16")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'green
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        r4
                        r16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.ltleaves(exclude=exclude)[n]

    def ltleaves(
        self, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects left-trimmed leaves.

        ..  container:: example

            Selects left-trimmed leaves:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 r4 r16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).ltleaves()

                >>> for item in result:
                ...     item
                ...
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("c'16")
                Chord("<d' e'>4")
                Chord("<d' e'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("e'16")
                Rest('r4')
                Rest('r16')

            ..  container:: example expression

                >>> selector = baca.ltleaves()
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("c'16")
                Chord("<d' e'>4")
                Chord("<d' e'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("e'16")
                Rest('r4')
                Rest('r16')

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9 {
                        \abjad-color-music #'blue
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'red
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        \abjad-color-music #'blue
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'blue
                        r4
                        \abjad-color-music #'red
                        r16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return super().leaves(exclude=exclude, trim=abjad.Left)

    def ltqrun(
        self, n: int, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects logical tie equipitch run ``n``.

        ..  container:: example

            Selects logical tie equipitch run -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).ltqrun(-1)

                >>> result
                Selection([LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

            ..  container:: example expression

                >>> selector = baca.ltqrun(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        c'16
                        c'16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        d'16
                        d'16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        e'16
                        e'16
                        e'16
                        \abjad-color-music #'green
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'green
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.ltqruns(exclude=exclude)[n]

    def ltqruns(
        self, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects logical tie equipitch runs.

        ..  container:: example

            Selects logical tie equipitch runs:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).ltqruns()

                >>> for item in result:
                ...     item
                ...
                Selection([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")])])
                Selection([LogicalTie([Chord("<d' e'>4"), Chord("<d' e'>16")])])
                Selection([LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")])])
                Selection([LogicalTie([Chord("<e' fs'>4"), Chord("<e' fs'>16")])])
                Selection([LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")])])
                Selection([LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

            ..  container:: example expression

                >>> selector = baca.ltqruns()
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")])])
                Selection([LogicalTie([Chord("<d' e'>4"), Chord("<d' e'>16")])])
                Selection([LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")])])
                Selection([LogicalTie([Chord("<e' fs'>4"), Chord("<e' fs'>16")])])
                Selection([LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")])])
                Selection([LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        \abjad-color-music #'blue
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'blue
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'blue
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = self.plts(exclude=exclude)
        result = result.group_by_pitch()
        result = result.map(select().group_by_contiguity())
        result = result.flatten(depth=1)
        result = result.map(Selection)
        return result

    def ltrun(
        self, n: int, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects logical tie run ``n``.

        ..  container:: example

            Selects logical tie run -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).ltrun(-1)

                >>> result
                Selection([LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

            ..  container:: example expression

                >>> selector = baca.ltrun(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        c'16
                        c'16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        d'16
                        d'16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'green
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.ltruns(exclude=exclude)[n]

    def ltruns(
        self, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects logical tie runs.

        ..  container:: example

            Selects logical tie runs:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).ltruns()

                >>> for item in result:
                ...     item
                ...
                Selection([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")]), LogicalTie([Chord("<d' e'>4"), Chord("<d' e'>16")])])
                Selection([LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")]), LogicalTie([Chord("<e' fs'>4"), Chord("<e' fs'>16")])])
                Selection([LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

            ..  container:: example expression

                >>> selector = baca.ltruns()
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")]), LogicalTie([Chord("<d' e'>4"), Chord("<d' e'>16")])])
                Selection([LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")]), LogicalTie([Chord("<e' fs'>4"), Chord("<e' fs'>16")])])
                Selection([LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'red
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = self.logical_ties(exclude=exclude, pitched=True)
        result = result.group_by_contiguity()
        return result.map(Selection)

    def lts(
        self, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects logical ties.

        ..  container:: example

            Selects logical ties:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).lts()

                >>> for item in result:
                ...     item
                ...
                LogicalTie([Rest('r16')])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("c'16")])
                LogicalTie([Chord("<d' e'>4"), Chord("<d' e'>16")])
                LogicalTie([Rest('r16')])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("d'16")])
                LogicalTie([Chord("<e' fs'>4"), Chord("<e' fs'>16")])
                LogicalTie([Rest('r16')])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("e'16")])
                LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.lts()
                >>> result = selector(staff)

                >>> selector.print(result)
                LogicalTie([Rest('r16')])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("c'16")])
                LogicalTie([Chord("<d' e'>4"), Chord("<d' e'>16")])
                LogicalTie([Rest('r16')])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("d'16")])
                LogicalTie([Chord("<e' fs'>4"), Chord("<e' fs'>16")])
                LogicalTie([Rest('r16')])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("e'16")])
                LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'blue
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        \abjad-color-music #'blue
                        c'16
                        \abjad-color-music #'red
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9 {
                        \abjad-color-music #'blue
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'blue
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        \abjad-color-music #'blue
                        e'16
                        \abjad-color-music #'red
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'red
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.logical_ties(exclude=exclude)

    def mgroups(
        self,
        counts: typing.Sequence[int] = [1],
        *,
        exclude: abjad.Strings = None,
    ) -> typing.Union[abjad.Expression, "Selection"]:
        r"""
        Partitions measure-grouped leaves.

        ..  container:: example

            Partitions measure-grouped leaves into one part of length 2:

            ..  container:: example

                >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r d''")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
                >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = baca.select(staff).mgroups([2])

                >>> for item in result:
                ...     item
                ...
                Selection([Rest('r8'), Note("d'8"), Note("e'8"), Note("f'8")])

            ..  container:: example expression

                >>> selector = baca.select().mgroups([2])
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Rest('r8'), Note("d'8"), Note("e'8"), Note("f'8")])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'red
                    f'8
                    \time 3/8
                    g'8
                    a'8
                    b'8
                    \time 1/8
                    r8
                    d''8
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = self.leaves(exclude=exclude)
        result = result.group_by_measure()
        result = result.partition_by_counts(counts)
        result_ = result.map(select().flatten())
        assert isinstance(result_, Selection), repr(result_)
        return result_

    def mleaves(
        self, count: int, *, exclude: abjad.Strings = None
    ) -> typing.Union["Selection", abjad.Expression]:
        r"""
        Selects all leaves in ``count`` measures.

        ..  container:: example

            Selects leaves in first three measures:

            ..  container:: example

                >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
                >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = baca.select(staff).mleaves(3)

                >>> for item in result:
                ...     item
                ...
                Rest('r8')
                Note("d'8")
                Note("e'8")
                Note("f'8")
                Note("g'8")
                Note("a'8")
                Note("b'8")

            ..  container:: example expression

                >>> selector = baca.select().mleaves(3)
                >>> result = selector(staff)

                >>> selector.print(result)
                Rest('r8')
                Note("d'8")
                Note("e'8")
                Note("f'8")
                Note("g'8")
                Note("a'8")
                Note("b'8")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'blue
                    f'8
                    \time 3/8
                    \abjad-color-music #'red
                    g'8
                    \abjad-color-music #'blue
                    a'8
                    \abjad-color-music #'red
                    b'8
                    \time 1/8
                    r8
                }

        ..  container:: example

            Selects leaves in last three measures:

            ..  container:: example

                >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
                >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = baca.select(staff).mleaves(-3)

                >>> for item in result:
                ...     item
                ...
                Note("e'8")
                Note("f'8")
                Note("g'8")
                Note("a'8")
                Note("b'8")
                Rest('r8')

            ..  container:: example expression

                >>> selector = baca.select().mleaves(-3)
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("e'8")
                Note("f'8")
                Note("g'8")
                Note("a'8")
                Note("b'8")
                Rest('r8')

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    r8
                    d'8
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'blue
                    f'8
                    \time 3/8
                    \abjad-color-music #'red
                    g'8
                    \abjad-color-music #'blue
                    a'8
                    \abjad-color-music #'red
                    b'8
                    \time 1/8
                    \abjad-color-music #'blue
                    r8
                }

        """
        assert isinstance(count, int), repr(count)
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = self.leaves(exclude=exclude).group_by_measure()
        if 0 < count:
            result = result[:count].flatten()
        elif count < 0:
            result = result[count:].flatten()
        else:
            raise Exception(count)
        return result

    def mmrest(
        self, n: int, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Note, abjad.Expression]:
        r"""
        Selects multimeasure rest ``n``.

        ..  container:: example

            Selects multimeasure rest -1:

            ..  container:: example

                >>> staff = abjad.Staff("R1 R1 R1")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = baca.select(staff).mmrest(-1)

                >>> result
                MultimeasureRest('R1')

            ..  container:: example expression

                >>> selector = baca.select().mmrest(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                MultimeasureRest('R1')

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    R1
                    R1
                    \abjad-color-music #'green
                    R1
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.mmrests(exclude=exclude)[n]

    def mmrests(
        self, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects multimeasure rests.

        ..  container:: example

            Selects multimeasure rests:

            ..  container:: example

                >>> staff = abjad.Staff("R1 R1 R1")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = baca.select(staff).mmrests()

                >>> for item in result:
                ...     item
                ...
                MultimeasureRest('R1')
                MultimeasureRest('R1')
                MultimeasureRest('R1')

            ..  container:: example expression

                >>> selector = baca.select().mmrests()
                >>> result = selector(staff)

                >>> selector.print(result)
                MultimeasureRest('R1')
                MultimeasureRest('R1')
                MultimeasureRest('R1')

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    R1
                    \abjad-color-music #'blue
                    R1
                    \abjad-color-music #'red
                    R1
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return super().leaves(abjad.MultimeasureRest, exclude=exclude)

    def ntrun(
        self, n: int, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects nontrivial run ``n``.

        ..  container:: example

            Selects nontrivial run -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).ntrun(-1)

                >>> result
                Selection([Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.ntrun(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        c'16
                        c'16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        d'16
                        d'16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'green
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.ntruns(exclude=exclude)[n]

    def ntruns(
        self, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects nontrivial runs.

        ..  container:: example

            Selects nontrivial runs:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).ntruns()

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'16"), Note("c'16"), Note("c'16"), Chord("<d' e'>4"), Chord("<d' e'>16")])
                Selection([Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16")])
                Selection([Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.ntruns()
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'16"), Note("c'16"), Note("c'16"), Chord("<d' e'>4"), Chord("<d' e'>16")])
                Selection([Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16")])
                Selection([Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'red
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.runs(exclude=exclude).nontrivial()

    def omgroups(
        self,
        counts: typing.Sequence[int] = [1],
        *,
        exclude: abjad.Strings = None,
    ) -> typing.Union[abjad.Expression, "Selection"]:
        r"""
        Partitions measure-grouped leaves (with overhang).

        ..  container:: example

            Partitions measure-grouped leaves into one part of length 2
            followed by an overhang part of remaining measures:

            ..  container:: example

                >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r d''")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
                >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = baca.select(staff).omgroups([2])

                >>> for item in result:
                ...     item
                ...
                Selection([Rest('r8'), Note("d'8"), Note("e'8"), Note("f'8")])
                Selection([Note("g'8"), Note("a'8"), Note("b'8"), Rest('r8'), Note("d''8")])

            ..  container:: example expression

                >>> selector = baca.select().omgroups([2])
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Rest('r8'), Note("d'8"), Note("e'8"), Note("f'8")])
                Selection([Note("g'8"), Note("a'8"), Note("b'8"), Rest('r8'), Note("d''8")])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'red
                    f'8
                    \time 3/8
                    \abjad-color-music #'blue
                    g'8
                    \abjad-color-music #'blue
                    a'8
                    \abjad-color-music #'blue
                    b'8
                    \time 1/8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'blue
                    d''8
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = self.leaves(exclude=exclude)
        result = result.group_by_measure()
        result = result.partition_by_counts(counts, overhang=True)
        result_ = result.map(select().flatten())
        assert isinstance(result_, Selection), repr(result_)
        return result_

    def ompltgroups(
        self,
        counts: typing.Sequence[int] = [1],
        *,
        exclude: abjad.Strings = None,
    ) -> typing.Union[abjad.Expression, "Selection"]:
        r"""
        Partitions measure-grouped plts (with overhang).
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = self.plts(exclude=exclude)
        result = result.group_by_measure()
        result = result.partition_by_counts(counts, overhang=True)
        result_ = result.map(select().flatten())
        assert isinstance(result_, Selection), repr(result_)
        return result_

    def phead(
        self, n: int, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Note, abjad.Chord, abjad.Expression]:
        r"""
        Selects pitched head ``n``.

        ..  container:: example

            Selects pitched head -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).phead(-1)

                >>> result
                Chord("<fs' gs'>4")

            ..  container:: example expression

                >>> selector = baca.phead(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<fs' gs'>4")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        \abjad-color-music #'green
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.pheads(exclude=exclude)[n]

    def pheads(
        self, *, exclude: abjad.Strings = None, grace: bool = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects pitched heads.

        ..  container:: example

            Selects pitched heads:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).pheads()

                >>> for item in result:
                ...     item
                ...
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("c'16")
                Chord("<d' e'>4")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("e'16")
                Chord("<fs' gs'>4")

            ..  container:: example expression

                >>> selector = baca.pheads()
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("c'16")
                Chord("<d' e'>4")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("e'16")
                Chord("<fs' gs'>4")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'blue
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.plts(exclude=exclude, grace=grace).map(select()[0])

    def pleaf(
        self, n: int, *, exclude: abjad.Strings = None, grace: bool = None
    ) -> typing.Union[abjad.Note, abjad.Chord, abjad.Expression]:
        r"""
        Selects pitched leaf ``n``.

        ..  container:: example

            Selects pitched leaf -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).pleaf(-1)

                >>> result
                Chord("<fs' gs'>16")

            ..  container:: example expression

                >>> selector = baca.pleaf(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<fs' gs'>16")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'green
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.pleaves(exclude=exclude, grace=grace)[n]

    def pleaves(
        self, *, exclude: abjad.Strings = None, grace: bool = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects pitched leaves.

        ..  container:: example

            Selects pitched leaves:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).pleaves()

                >>> for item in result:
                ...     item
                ...
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("c'16")
                Chord("<d' e'>4")
                Chord("<d' e'>16")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("e'16")
                Chord("<fs' gs'>4")
                Chord("<fs' gs'>16")

            ..  container:: example expression

                >>> selector = baca.pleaves()
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("c'16")
                Chord("<d' e'>4")
                Chord("<d' e'>16")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("e'16")
                Chord("<fs' gs'>4")
                Chord("<fs' gs'>16")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        \abjad-color-music #'blue
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'red
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'blue
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'red
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return super().leaves(exclude=exclude, grace=grace, pitched=True)

    def plt(
        self, n: int, *, exclude: abjad.Strings = None, grace: bool = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects pitched logical tie ``n``.

        ..  container:: example

            Selects pitched logical tie -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).plt(-1)

                >>> result
                LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.plt(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        \abjad-color-music #'green
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'green
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.plts(exclude=exclude, grace=grace)[n]

    def plts(
        self, *, exclude: abjad.Strings = None, grace: bool = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects pitched logical ties.

        ..  container:: example

            Selects pitched logical ties:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).plts()

                >>> for item in result:
                ...     item
                ...
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("c'16")])
                LogicalTie([Chord("<d' e'>4"), Chord("<d' e'>16")])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("d'16")])
                LogicalTie([Chord("<e' fs'>4"), Chord("<e' fs'>16")])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("e'16")])
                LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.plts()
                >>> result = selector(staff)

                >>> selector.print(result)
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("c'16")])
                LogicalTie([Chord("<d' e'>4"), Chord("<d' e'>16")])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("d'16")])
                LogicalTie([Chord("<e' fs'>4"), Chord("<e' fs'>16")])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("e'16")])
                LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        \abjad-color-music #'blue
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'blue
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'blue
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.logical_ties(exclude=exclude, grace=grace, pitched=True)

    def ptail(
        self, n: int, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Note, abjad.Chord, abjad.Expression]:
        r"""
        Selects pitched tail ``n``.

        ..  container:: example

            Selects pitched tail -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).ptail(-1)

                >>> result
                Chord("<fs' gs'>16")

            ..  container:: example expression

                >>> selector = baca.ptail(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<fs' gs'>16")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'green
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.ptails(exclude=exclude)[n]

    def ptails(
        self, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects pitched tails.

        ..  container:: example

            Selects pitched tails:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).ptails()

                >>> for item in result:
                ...     item
                ...
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("c'16")
                Chord("<d' e'>16")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>16")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("e'16")
                Chord("<fs' gs'>16")

            ..  container:: example expression

                >>> selector = baca.ptails()
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("c'16")
                Chord("<d' e'>16")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>16")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("e'16")
                Chord("<fs' gs'>16")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        c'16
                        <d' e'>4
                        ~
                        \abjad-color-music #'blue
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        d'16
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        e'16
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'blue
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.plts(exclude=exclude).map(select()[-1])

    def ptlt(
        self, n: int, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects pitched trivial logical tie ``n``.

        ..  container:: example

            Selects pitched trivial logical tie -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).ptlt(-1)

                >>> result
                LogicalTie([Note("e'16")])

            ..  container:: example expression

                >>> selector = baca.ptlt(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                LogicalTie([Note("e'16")])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        \abjad-color-music #'green
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.ptlts(exclude=exclude)[n]

    def ptlts(
        self, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects pitched trivial logical ties.

        ..  container:: example

            Selects pitched trivial logical ties:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).ptlts()

                >>> for item in result:
                ...     item
                ...
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("c'16")])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("d'16")])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("e'16")])

            ..  container:: example expression

                >>> selector = baca.ptlts()
                >>> result = selector(staff)

                >>> selector.print(result)
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("c'16")])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("d'16")])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("e'16")])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        \abjad-color-music #'blue
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        \abjad-color-music #'blue
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.logical_ties(exclude=exclude, nontrivial=False, pitched=True)

    def qrun(
        self, n: int, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects equipitch run ``n``.

        ..  container:: example

            Selects equipitch run -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).qrun(-1)

                >>> result
                Selection([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.qrun(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        c'16
                        c'16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        d'16
                        d'16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        e'16
                        e'16
                        e'16
                        \abjad-color-music #'green
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'green
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.qruns(exclude=exclude)[n]

    def qruns(
        self, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects equipitch runs.

        ..  container:: example

            Selects equipitch runs:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).qruns()

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'16"), Note("c'16"), Note("c'16")])
                Selection([Chord("<d' e'>4"), Chord("<d' e'>16")])
                Selection([Note("d'16"), Note("d'16"), Note("d'16")])
                Selection([Chord("<e' fs'>4"), Chord("<e' fs'>16")])
                Selection([Note("e'16"), Note("e'16"), Note("e'16")])
                Selection([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.qruns()
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'16"), Note("c'16"), Note("c'16")])
                Selection([Chord("<d' e'>4"), Chord("<d' e'>16")])
                Selection([Note("d'16"), Note("d'16"), Note("d'16")])
                Selection([Chord("<e' fs'>4"), Chord("<e' fs'>16")])
                Selection([Note("e'16"), Note("e'16"), Note("e'16")])
                Selection([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        \abjad-color-music #'blue
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'blue
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'blue
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = self.pleaves(exclude=exclude)
        result = result.group_by_pitch()
        result = result.map(select().group_by_contiguity())
        result = result.flatten(depth=1)
        result = result.map(Selection)
        return result

    def rleaf(
        self, n: int = 0, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Leaf, abjad.Expression]:
        r"""
        Selects leaf ``n`` from leaves leaked to the right.

        ..  container:: example

            Selects leaf -1 from leaves (leaked to the right) in tuplet 1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> baca.select(staff).tuplets()[1:2].rleaf(-1)
                Rest('r16')

            ..  container:: example expression

                >>> selector = baca.tuplets()[1:2].rleaf(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Rest('r16')

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        \abjad-color-music #'green
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.rleaves(exclude=exclude)[n]

    def rleak(
        self, *, grace: bool = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Leaks to the right.

        ..  container:: example

            Selects runs (each leaked to the right):

            ..  container:: example

                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).runs().map(baca.rleak())

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Rest('r8')])
                Selection([Note("d'8"), Note("e'8"), Rest('r8')])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])

            ..  container:: example expression

                >>> selector = baca.select().runs().map(baca.rleak())
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Rest('r8')])
                Selection([Note("d'8"), Note("e'8"), Rest('r8')])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(staff, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'red
                    f'8
                    \abjad-color-music #'red
                    g'8
                    \abjad-color-music #'red
                    a'8
                }

        Returns new selection (or expression).
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.with_next_leaf(grace=grace)

    def rleaves(
        self, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects leaves, leaked to the right.

        ..  container:: example

            Selects leaves (leaked to the right) in tuplet 1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).tuplets()[1:2].rleaves()

                >>> for item in result:
                ...     item
                ...
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Rest('r16')

            ..  container:: example expression

                >>> selector = baca.tuplets()[1:2].rleaves()
                >>> result = selector(staff)

                >>> selector.print(result)
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Rest('r16')

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'blue
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'red
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        \abjad-color-music #'red
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.leaves(exclude=exclude).with_next_leaf()

    def rmleaves(
        self, count: int, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects all leaves in ``count`` measures, leaked one leaf to the right.

        ..  container:: example

            Selects leaves in first two measures, leaked on leaf to the right:

            ..  container:: example

                >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
                >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])
                >>> abjad.show(staff) # doctest: +SKIP

                >>> result = baca.select(staff).rmleaves(2)

                >>> for item in result:
                ...     item
                ...
                Rest('r8')
                Note("d'8")
                Note("e'8")
                Note("f'8")
                Note("g'8")

            ..  container:: example expression

                >>> selector = baca.select().rmleaves(2)
                >>> result = selector(staff)

                >>> selector.print(result)
                Rest('r8')
                Note("d'8")
                Note("e'8")
                Note("f'8")
                Note("g'8")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'blue
                    f'8
                    \time 3/8
                    \abjad-color-music #'red
                    g'8
                    a'8
                    b'8
                    \time 1/8
                    r8
                }

        """
        assert isinstance(count, int), repr(count)
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.mleaves(count, exclude=exclude).rleak()

    def rrun(
        self, n: int, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects run ``n`` (leaked to the right).

        ..  container:: example

            Selects run 1 (leaked to the right):

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).rrun(1)

                >>> result
                Selection([Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16"), Rest('r16')])

            ..  container:: example expression

                >>> selector = baca.rrun(1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16"), Rest('r16')])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        c'16
                        c'16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        \abjad-color-music #'green
                        d'16
                        \abjad-color-music #'green
                        d'16
                        \abjad-color-music #'green
                        d'16
                        \abjad-color-music #'green
                        <e' fs'>4
                        ~
                        \abjad-color-music #'green
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        \abjad-color-music #'green
                        r16
                        e'16
                        e'16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.rruns(exclude=exclude)[n]

    def rruns(
        self, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects runs (leaked to the right).

        ..  container:: example

            Selects runs (leaked to the right):

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).rruns()

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'16"), Note("c'16"), Note("c'16"), Chord("<d' e'>4"), Chord("<d' e'>16"), Rest('r16')])
                Selection([Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16"), Rest('r16')])
                Selection([Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.rruns()
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'16"), Note("c'16"), Note("c'16"), Chord("<d' e'>4"), Chord("<d' e'>16"), Rest('r16')])
                Selection([Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16"), Rest('r16')])
                Selection([Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9 {
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        \abjad-color-music #'blue
                        r16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'red
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = self.runs(exclude=exclude).map(select().rleak())
        return result.map(Selection)

    def skip(
        self, n: int, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Skip, abjad.Expression]:
        r"""
        Selects skip ``n``.

        ..  container:: example

            Selects skip -1:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 s e' f' g' s b' s")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
                >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])
                >>> abjad.show(staff, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).skip(-1)

                >>> result
                Skip('s8')

            ..  container:: example expression

                >>> selector = baca.select().skip(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Skip('s8')

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(staff, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    c'8
                    s8
                    e'8
                    f'8
                    \time 3/8
                    g'8
                    s8
                    b'8
                    % green
                    \time 1/8
                    s8
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.skips(exclude=exclude)[n]

    def skips(
        self, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects skips.

        ..  container:: example

            Selects skips:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 s e' f' g' s b' s")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
                >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])
                >>> abjad.show(staff, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).skips()

                >>> for item in result:
                ...     item
                Skip('s8')
                Skip('s8')
                Skip('s8')

            ..  container:: example expression

                >>> selector = baca.select().skips()
                >>> result = selector(staff)

                >>> selector.print(result)
                Skip('s8')
                Skip('s8')
                Skip('s8')

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(staff, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    c'8
                    % red
                    s8
                    e'8
                    f'8
                    \time 3/8
                    g'8
                    % blue
                    s8
                    b'8
                    % red
                    \time 1/8
                    s8
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.components(abjad.Skip, exclude=exclude)

    def tleaf(
        self, n: int = 0, *, exclude: abjad.Strings = None, grace: bool = None
    ) -> typing.Union[abjad.Leaf, abjad.Expression]:
        r"""
        Selects trimmed leaf ``n``.

        ..  container:: example

            Selects trimmed leaf 0:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).tleaf(0)

                >>> result
                Note("bf'16")

            ..  container:: example expression

                >>> selector = baca.tleaf(0)
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("bf'16")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'green
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.tleaves(exclude=exclude, grace=grace)[n]

    def tleaves(
        self, *, exclude: abjad.Strings = None, grace: bool = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects trimmed leaves.

        ..  container:: example

            Selects trimmed leaves:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).tleaves()

                >>> for item in result:
                ...     item
                ...
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("c'16")
                Chord("<d' e'>4")
                Chord("<d' e'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("e'16")
                Chord("<fs' gs'>4")
                Chord("<fs' gs'>16")

            ..  container:: example expression

                >>> selector = baca.tleaves()
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("c'16")
                Chord("<d' e'>4")
                Chord("<d' e'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("e'16")
                Chord("<fs' gs'>4")
                Chord("<fs' gs'>16")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9 {
                        \abjad-color-music #'blue
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'red
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        \abjad-color-music #'blue
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'blue
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'red
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return super().leaves(exclude=exclude, grace=grace, trim=True)

    def wleaf(
        self, n: int = 0, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Leaf, abjad.Expression]:
        r"""
        Selects leaf ``n`` from leaves leaked wide.

        ..  container:: example

            Selects leaf 0 from leaves (leaked to both the left and right) in
            tuplet 1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> baca.select(staff).tuplets()[1:2].wleaf(0)
                Chord("<d' e'>16")

            ..  container:: example expression

                >>> selector = baca.tuplets()[1:2].wleaf(0)
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<d' e'>16")

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        \abjad-color-music #'green
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        ..  container:: example

            Selects leaf -1 from leaves (leaked to both the left and right) in
            tuplet 1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> baca.select(staff).tuplets()[1:2].wleaf(-1)
                Rest('r16')

            ..  container:: example expression

                >>> selector = baca.tuplets()[1:2].wleaf(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Rest('r16')

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        \abjad-color-music #'green
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.wleaves(exclude=exclude)[n]

    def wleaves(
        self, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Selection, abjad.Expression]:
        r"""
        Selects leaves, leaked "wide" (to both the left and right).

        ..  container:: example

            Selects leaves (leaked wide) in tuplet 1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).TupletBracket.direction = abjad.Up
                >>> abjad.override(staff).TupletBracket.staff_padding = 3
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

                >>> result = baca.select(staff).tuplets()[1:2].wleaves()

                >>> for item in result:
                ...     item
                ...
                Chord("<d' e'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Rest('r16')

            ..  container:: example expression

                >>> selector = baca.tuplets()[1:2].wleaves()
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<d' e'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Rest('r16')

                >>> abjad.label(result).by_selector(selector)
                >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9 {
                        \abjad-color-music #'blue
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'red
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9 {
                        \abjad-color-music #'blue
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.leaves(exclude=exclude).with_previous_leaf().with_next_leaf()


class Sequence(abjad.Sequence):
    r"""
    Sequence.

    ..  container:: example

        Initializes from numbers:

        ..  container:: example

            >>> baca.sequence([1, 2, 3, 4, 5, 6])
            Sequence([1, 2, 3, 4, 5, 6])

        ..  container:: example expression

            >>> expression = baca.sequence()

            >>> expression([1, 2, 3, 4, 5, 6])
            Sequence([1, 2, 3, 4, 5, 6])

    ..  container:: example

        Initializes from collection:

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> collection = abjad.PitchClassSegment(items=items)
            >>> lilypond_file = abjad.illustrate(collection)
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    bf'8
                    bqf'8
                    fs'8
                    g'8
                    bqf'8
                    g'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

            >>> baca.sequence(collection)
            Sequence([NumberedPitchClass(10), NumberedPitchClass(10.5), NumberedPitchClass(6), NumberedPitchClass(7), NumberedPitchClass(10.5), NumberedPitchClass(7)])

        ..  container:: example expression

            >>> expression = baca.sequence()

            >>> expression(collection)
            Sequence([NumberedPitchClass(10), NumberedPitchClass(10.5), NumberedPitchClass(6), NumberedPitchClass(7), NumberedPitchClass(10.5), NumberedPitchClass(7)])

    ..  container:: example

        Maps transposition to multiple collections:

        ..  container:: example

            >>> items = [-2, -1.5, 6, 7, -1.5, 7]
            >>> collection = abjad.PitchClassSegment(items=items)
            >>> collections = [
            ...     abjad.PitchClassSegment(items=[-2, -1.5, 6]),
            ...     abjad.PitchClassSegment(items=[7, -1.5, 7]),
            ...     ]

            >>> expression = baca.pitch_class_segment()
            >>> expression = expression.transpose(n=1)

            >>> sequence = baca.sequence(collections)
            >>> sequence = sequence.map(expression)
            >>> sequence.join()
            Sequence([PitchClassSegment([11, 11.5, 7, 8, 11.5, 8])])

            >>> collection = sequence.join()[0]
            >>> lilypond_file = abjad.illustrate(collection)
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    b'8
                    bqs'8
                    g'8
                    af'8
                    bqs'8
                    af'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

        ..  container:: example expression

            >>> collections = [
            ...     baca.PitchClassSegment(items=[-2, -1.5, 6]),
            ...     baca.PitchClassSegment(items=[7, -1.5, 7]),
            ...     ]

            >>> transposition = baca.pitch_class_segment()
            >>> transposition = transposition.transpose(n=1)
            >>> expression = baca.sequence(name='J')
            >>> expression = expression.map(transposition)
            >>> expression = expression.join()

            >>> expression(collections)
            Sequence([PitchClassSegment([11, 11.5, 7, 8, 11.5, 8])])

            >>> expression.get_string()
            'join(T1(X) /@ J)'

            >>> collection = expression(collections)[0]
            >>> markup = expression.get_markup()
            >>> lilypond_file = abjad.illustrate(collection, figure_name=markup)
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> voice = lilypond_file[abjad.Score][0][0]
                >>> string = abjad.lilypond(voice)
                >>> print(string)
                \new Voice
                {
                    b'8
                    ^ \markup {
                        \concat
                            {
                                join(
                                \line
                                    {
                                        \concat
                                            {
                                                T
                                                \sub
                                                    1
                                                \bold
                                                    X
                                            }
                                        /@
                                        \bold
                                            J
                                    }
                                )
                            }
                        }
                    bqs'8
                    g'8
                    af'8
                    bqs'8
                    af'8
                    \bar "|."
                    \override Score.BarLine.transparent = ##f
                }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Classes"

    __slots__ = ()

    ### PRIVATE METHODS ###

    @staticmethod
    def _make_accumulate_markup(markup, operands=None, count=None):
        if count is None:
            count = abjad.Exact
        operands = operands or [abjad.Exact]
        operand_strings = []
        for operand in operands:
            if hasattr(operand, "get_markup"):
                operand_string = operand.get_markup(name="X")
                assert len(operand_string.contents) == 1
                operand_string = str(operand_string.contents[0])
            else:
                operand_string = str(operand)
            operand_strings.append(operand_string)
        string = "\n".join(operand_strings)
        operand_string = rf"\concat {{ {string} }}"
        infix = "Φ"
        if count != abjad.Exact:
            infix += "/" + str(count)
        string = rf"\line {{ {operand_string} {infix} {markup.contents[0]} }}"
        try:
            markup = abjad.Markup(string)
        except Exception:
            raise Exception(string)
        return markup

    @staticmethod
    def _make_accumulate_string_template(operands=None, count=None):
        if count is None:
            count = abjad.Exact
        operands = operands or [abjad.Exact]
        operand_strings = []
        for operand in operands:
            if hasattr(operand, "get_string"):
                operand_string = operand.get_string(name="X")
            else:
                operand_string = str(operand)
            operand_strings.append(operand_string)
        if len(operand_strings) == 1:
            operands = operand_strings[0]
        else:
            operands = ", ".join(operand_strings)
            operands = "[" + operands + "]"
        if count == abjad.Exact:
            string_template = f"{operands} Φ {{}}"
        else:
            string_template = f"{operands} Φ/{count} {{}}"
        return string_template

    def _update_expression(
        self,
        frame,
        evaluation_template=None,
        map_operand=None,
        subclass_hook=None,
    ):
        callback = Expression._frame_to_callback(
            frame,
            evaluation_template=evaluation_template,
            map_operand=map_operand,
            subclass_hook=subclass_hook,
        )
        return self._expression.append_callback(callback)

    ### PUBLIC METHODS ###

    @abjad.Signature(
        markup_maker_callback="_make_accumulate_markup",
        string_template_callback="_make_accumulate_string_template",
    )
    def accumulate(self, operands=None, count=None):
        r"""
        Accumulates ``operands`` calls against sequence to identity.

        ..  container:: example

            Accumulates identity operator:

            ..  container:: example

                >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                >>> collection_2 = baca.PitchClassSegment([4, 5])
                >>> baca.sequence([collection_1, collection_2])
                Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])

                >>> sequence = baca.sequence([collection_1, collection_2])
                >>> for item in sequence.accumulate():
                ...     item
                ...
                Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])

            ..  container:: example expression

                >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                >>> collection_2 = baca.PitchClassSegment([4, 5])

                >>> expression = baca.sequence(name='J').accumulate()

                >>> for item in expression([collection_1, collection_2]):
                ...     item
                ...
                Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])

                >>> expression.get_string()
                'Exact Φ J'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(markup)
                    >>> print(string)
                    \markup {
                        \line
                            {
                                \concat
                                    {
                                        Exact
                                    }
                                Φ
                                \bold
                                    J
                            }
                        }

        ..  container:: example

            Accumulates alpha:

            ..  container:: example

                >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                >>> collection_2 = baca.PitchClassSegment([4, 5])
                >>> baca.sequence([collection_1, collection_2])
                Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])

                >>> alpha = baca.pitch_class_segment().alpha()

                >>> sequence = baca.sequence([collection_1, collection_2])
                >>> for item in sequence.accumulate([alpha]):
                ...     item
                ...
                Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                Sequence([PitchClassSegment([1, 0, 3, 2]), PitchClassSegment([5, 4])])

            ..  container:: example expression

                >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                >>> collection_2 = baca.PitchClassSegment([4, 5])

                >>> alpha = baca.pitch_class_segment().alpha()
                >>> expression = baca.sequence(name='J').accumulate([alpha])

                >>> for sequence in expression([collection_1, collection_2]):
                ...     sequence
                ...
                Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                Sequence([PitchClassSegment([1, 0, 3, 2]), PitchClassSegment([5, 4])])

                >>> expression.get_string()
                'A(X) Φ J'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(markup)
                    >>> print(string)
                    \markup {
                        \line
                            {
                                \concat
                                    {
                                        \concat
                                            {
                                                A
                                                \bold
                                                    X
                                            }
                                    }
                                Φ
                                \bold
                                    J
                            }
                        }

        ..  container:: example

            Accumulates transposition:

            ..  container:: example

                >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                >>> collection_2 = baca.PitchClassSegment([4, 5])
                >>> baca.sequence([collection_1, collection_2])
                Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])

                >>> transposition = baca.pitch_class_segment()
                >>> transposition = transposition.transpose(n=3)

                >>> sequence = baca.sequence([collection_1, collection_2])
                >>> for item in sequence.accumulate([transposition]):
                ...     item
                ...
                Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                Sequence([PitchClassSegment([3, 4, 5, 6]), PitchClassSegment([7, 8])])
                Sequence([PitchClassSegment([6, 7, 8, 9]), PitchClassSegment([10, 11])])
                Sequence([PitchClassSegment([9, 10, 11, 0]), PitchClassSegment([1, 2])])

            ..  container:: example expression

                >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                >>> collection_2 = baca.PitchClassSegment([4, 5])

                >>> transposition = baca.pitch_class_segment().transpose(n=3)
                >>> expression = baca.sequence(name='J').accumulate(
                ...     [transposition],
                ...     )

                >>> for sequence in expression([collection_1, collection_2]):
                ...     sequence
                ...
                Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                Sequence([PitchClassSegment([3, 4, 5, 6]), PitchClassSegment([7, 8])])
                Sequence([PitchClassSegment([6, 7, 8, 9]), PitchClassSegment([10, 11])])
                Sequence([PitchClassSegment([9, 10, 11, 0]), PitchClassSegment([1, 2])])

                >>> expression.get_string()
                'T3(X) Φ J'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(markup)
                    >>> print(string)
                    \markup {
                        \line
                            {
                                \concat
                                    {
                                        \concat
                                            {
                                                T
                                                \sub
                                                    3
                                                \bold
                                                    X
                                            }
                                    }
                                Φ
                                \bold
                                    J
                            }
                        }

        ..  container:: example

            Accumulates alpha followed by transposition:

            ..  container:: example

                >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                >>> collection_2 = baca.PitchClassSegment([4, 5])
                >>> baca.sequence([collection_1, collection_2])
                Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])

                >>> transposition = baca.pitch_class_segment()
                >>> transposition = transposition.transpose(n=3)
                >>> alpha = baca.pitch_class_segment()
                >>> alpha = alpha.alpha()

                >>> sequence = baca.sequence([collection_1, collection_2])
                >>> for item in sequence.accumulate([alpha, transposition]):
                ...     item
                ...
                Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                Sequence([PitchClassSegment([1, 0, 3, 2]), PitchClassSegment([5, 4])])
                Sequence([PitchClassSegment([4, 3, 6, 5]), PitchClassSegment([8, 7])])
                Sequence([PitchClassSegment([5, 2, 7, 4]), PitchClassSegment([9, 6])])
                Sequence([PitchClassSegment([8, 5, 10, 7]), PitchClassSegment([0, 9])])
                Sequence([PitchClassSegment([9, 4, 11, 6]), PitchClassSegment([1, 8])])
                Sequence([PitchClassSegment([0, 7, 2, 9]), PitchClassSegment([4, 11])])
                Sequence([PitchClassSegment([1, 6, 3, 8]), PitchClassSegment([5, 10])])
                Sequence([PitchClassSegment([4, 9, 6, 11]), PitchClassSegment([8, 1])])
                Sequence([PitchClassSegment([5, 8, 7, 10]), PitchClassSegment([9, 0])])
                Sequence([PitchClassSegment([8, 11, 10, 1]), PitchClassSegment([0, 3])])
                Sequence([PitchClassSegment([9, 10, 11, 0]), PitchClassSegment([1, 2])])

            ..  container:: example expression

                >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                >>> collection_2 = baca.PitchClassSegment([4, 5])

                >>> alpha = baca.pitch_class_segment().alpha()
                >>> transposition = baca.pitch_class_segment().transpose(n=3)
                >>> expression = baca.sequence(name='J').accumulate(
                ...     [alpha, transposition],
                ...     )

                >>> for sequence in expression([collection_1, collection_2]):
                ...     sequence
                ...
                Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                Sequence([PitchClassSegment([1, 0, 3, 2]), PitchClassSegment([5, 4])])
                Sequence([PitchClassSegment([4, 3, 6, 5]), PitchClassSegment([8, 7])])
                Sequence([PitchClassSegment([5, 2, 7, 4]), PitchClassSegment([9, 6])])
                Sequence([PitchClassSegment([8, 5, 10, 7]), PitchClassSegment([0, 9])])
                Sequence([PitchClassSegment([9, 4, 11, 6]), PitchClassSegment([1, 8])])
                Sequence([PitchClassSegment([0, 7, 2, 9]), PitchClassSegment([4, 11])])
                Sequence([PitchClassSegment([1, 6, 3, 8]), PitchClassSegment([5, 10])])
                Sequence([PitchClassSegment([4, 9, 6, 11]), PitchClassSegment([8, 1])])
                Sequence([PitchClassSegment([5, 8, 7, 10]), PitchClassSegment([9, 0])])
                Sequence([PitchClassSegment([8, 11, 10, 1]), PitchClassSegment([0, 3])])
                Sequence([PitchClassSegment([9, 10, 11, 0]), PitchClassSegment([1, 2])])

                >>> expression.get_string()
                '[A(X), T3(X)] Φ J'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(markup)
                    >>> print(string)
                    \markup {
                        \line
                            {
                                \concat
                                    {
                                        \concat
                                            {
                                                A
                                                \bold
                                                    X
                                            }
                                        \concat
                                            {
                                                T
                                                \sub
                                                    3
                                                \bold
                                                    X
                                            }
                                    }
                                Φ
                                \bold
                                    J
                            }
                        }

        ..  container:: example

            Accumulates permutation:

            ..  container:: example

                >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                >>> collection_2 = baca.PitchClassSegment([4, 5])
                >>> baca.sequence([collection_1, collection_2])
                Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])

                >>> permutation = baca.pitch_class_segment()
                >>> row = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
                >>> permutation = permutation.permute(row)

                >>> sequence = baca.sequence([collection_1, collection_2])
                >>> for item in sequence.accumulate([permutation]):
                ...     item
                ...
                Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                Sequence([PitchClassSegment([10, 0, 2, 6]), PitchClassSegment([8, 7])])
                Sequence([PitchClassSegment([4, 10, 2, 5]), PitchClassSegment([1, 3])])
                Sequence([PitchClassSegment([8, 4, 2, 7]), PitchClassSegment([0, 6])])
                Sequence([PitchClassSegment([1, 8, 2, 3]), PitchClassSegment([10, 5])])
                Sequence([PitchClassSegment([0, 1, 2, 6]), PitchClassSegment([4, 7])])
                Sequence([PitchClassSegment([10, 0, 2, 5]), PitchClassSegment([8, 3])])
                Sequence([PitchClassSegment([4, 10, 2, 7]), PitchClassSegment([1, 6])])
                Sequence([PitchClassSegment([8, 4, 2, 3]), PitchClassSegment([0, 5])])
                Sequence([PitchClassSegment([1, 8, 2, 6]), PitchClassSegment([10, 7])])
                Sequence([PitchClassSegment([0, 1, 2, 5]), PitchClassSegment([4, 3])])
                Sequence([PitchClassSegment([10, 0, 2, 7]), PitchClassSegment([8, 6])])
                Sequence([PitchClassSegment([4, 10, 2, 3]), PitchClassSegment([1, 5])])
                Sequence([PitchClassSegment([8, 4, 2, 6]), PitchClassSegment([0, 7])])
                Sequence([PitchClassSegment([1, 8, 2, 5]), PitchClassSegment([10, 3])])
                Sequence([PitchClassSegment([0, 1, 2, 7]), PitchClassSegment([4, 6])])
                Sequence([PitchClassSegment([10, 0, 2, 3]), PitchClassSegment([8, 5])])
                Sequence([PitchClassSegment([4, 10, 2, 6]), PitchClassSegment([1, 7])])
                Sequence([PitchClassSegment([8, 4, 2, 5]), PitchClassSegment([0, 3])])
                Sequence([PitchClassSegment([1, 8, 2, 7]), PitchClassSegment([10, 6])])

            ..  container:: example expression

                >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                >>> collection_2 = baca.PitchClassSegment([4, 5])

                >>> row = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
                >>> permutation = baca.pitch_class_segment().permute(row)
                >>> expression = baca.sequence(name='J').accumulate(
                ...     [permutation],
                ...     )

                >>> for sequence in expression([collection_1, collection_2]):
                ...     sequence
                ...
                Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                Sequence([PitchClassSegment([10, 0, 2, 6]), PitchClassSegment([8, 7])])
                Sequence([PitchClassSegment([4, 10, 2, 5]), PitchClassSegment([1, 3])])
                Sequence([PitchClassSegment([8, 4, 2, 7]), PitchClassSegment([0, 6])])
                Sequence([PitchClassSegment([1, 8, 2, 3]), PitchClassSegment([10, 5])])
                Sequence([PitchClassSegment([0, 1, 2, 6]), PitchClassSegment([4, 7])])
                Sequence([PitchClassSegment([10, 0, 2, 5]), PitchClassSegment([8, 3])])
                Sequence([PitchClassSegment([4, 10, 2, 7]), PitchClassSegment([1, 6])])
                Sequence([PitchClassSegment([8, 4, 2, 3]), PitchClassSegment([0, 5])])
                Sequence([PitchClassSegment([1, 8, 2, 6]), PitchClassSegment([10, 7])])
                Sequence([PitchClassSegment([0, 1, 2, 5]), PitchClassSegment([4, 3])])
                Sequence([PitchClassSegment([10, 0, 2, 7]), PitchClassSegment([8, 6])])
                Sequence([PitchClassSegment([4, 10, 2, 3]), PitchClassSegment([1, 5])])
                Sequence([PitchClassSegment([8, 4, 2, 6]), PitchClassSegment([0, 7])])
                Sequence([PitchClassSegment([1, 8, 2, 5]), PitchClassSegment([10, 3])])
                Sequence([PitchClassSegment([0, 1, 2, 7]), PitchClassSegment([4, 6])])
                Sequence([PitchClassSegment([10, 0, 2, 3]), PitchClassSegment([8, 5])])
                Sequence([PitchClassSegment([4, 10, 2, 6]), PitchClassSegment([1, 7])])
                Sequence([PitchClassSegment([8, 4, 2, 5]), PitchClassSegment([0, 3])])
                Sequence([PitchClassSegment([1, 8, 2, 7]), PitchClassSegment([10, 6])])

                >>> expression.get_string()
                'permute(X, row=[10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]) Φ J'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(markup)
                    >>> print(string)
                    \markup {
                        \line
                            {
                                \concat
                                    {
                                        \concat
                                            {
                                                permute(
                                                \bold
                                                    X
                                                ", row=[10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])"
                                            }
                                    }
                                Φ
                                \bold
                                    J
                            }
                        }

        ..  container:: example

            Accumulates permutation followed by transposition:

            ..  container:: example

                >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                >>> collection_2 = baca.PitchClassSegment([4, 5])
                >>> baca.sequence([collection_1, collection_2])
                Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])

                >>> permutation = baca.pitch_class_segment()
                >>> row = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
                >>> permutation = permutation.permute(row)
                >>> transposition = baca.pitch_class_segment()
                >>> transposition = transposition.transpose(n=3)

                >>> sequence = baca.sequence([collection_1, collection_2])
                >>> for item in sequence.accumulate(
                ...     [permutation, transposition],
                ...     ):
                ...     item
                ...
                Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                Sequence([PitchClassSegment([10, 0, 2, 6]), PitchClassSegment([8, 7])])
                Sequence([PitchClassSegment([1, 3, 5, 9]), PitchClassSegment([11, 10])])
                Sequence([PitchClassSegment([0, 6, 7, 9]), PitchClassSegment([11, 4])])
                Sequence([PitchClassSegment([3, 9, 10, 0]), PitchClassSegment([2, 7])])
                Sequence([PitchClassSegment([6, 9, 4, 10]), PitchClassSegment([2, 3])])
                Sequence([PitchClassSegment([9, 0, 7, 1]), PitchClassSegment([5, 6])])
                Sequence([PitchClassSegment([9, 10, 3, 0]), PitchClassSegment([7, 5])])
                Sequence([PitchClassSegment([0, 1, 6, 3]), PitchClassSegment([10, 8])])
                Sequence([PitchClassSegment([10, 0, 5, 6]), PitchClassSegment([4, 1])])
                Sequence([PitchClassSegment([1, 3, 8, 9]), PitchClassSegment([7, 4])])
                Sequence([PitchClassSegment([0, 6, 1, 9]), PitchClassSegment([3, 8])])
                Sequence([PitchClassSegment([3, 9, 4, 0]), PitchClassSegment([6, 11])])
                Sequence([PitchClassSegment([6, 9, 8, 10]), PitchClassSegment([5, 11])])
                Sequence([PitchClassSegment([9, 0, 11, 1]), PitchClassSegment([8, 2])])
                Sequence([PitchClassSegment([9, 10, 11, 0]), PitchClassSegment([1, 2])])

            ..  container:: example expression

                >>> collection_1 = baca.PitchClassSegment([0, 1, 2, 3])
                >>> collection_2 = baca.PitchClassSegment([4, 5])

                >>> row = [10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]
                >>> permutation = baca.pitch_class_segment().permute(row)
                >>> transposition = baca.pitch_class_segment().transpose(n=3)
                >>> expression = baca.sequence(name='J').accumulate(
                ...     [permutation, transposition],
                ...     )

                >>> for sequence in expression([collection_1, collection_2]):
                ...     sequence
                ...
                Sequence([PitchClassSegment([0, 1, 2, 3]), PitchClassSegment([4, 5])])
                Sequence([PitchClassSegment([10, 0, 2, 6]), PitchClassSegment([8, 7])])
                Sequence([PitchClassSegment([1, 3, 5, 9]), PitchClassSegment([11, 10])])
                Sequence([PitchClassSegment([0, 6, 7, 9]), PitchClassSegment([11, 4])])
                Sequence([PitchClassSegment([3, 9, 10, 0]), PitchClassSegment([2, 7])])
                Sequence([PitchClassSegment([6, 9, 4, 10]), PitchClassSegment([2, 3])])
                Sequence([PitchClassSegment([9, 0, 7, 1]), PitchClassSegment([5, 6])])
                Sequence([PitchClassSegment([9, 10, 3, 0]), PitchClassSegment([7, 5])])
                Sequence([PitchClassSegment([0, 1, 6, 3]), PitchClassSegment([10, 8])])
                Sequence([PitchClassSegment([10, 0, 5, 6]), PitchClassSegment([4, 1])])
                Sequence([PitchClassSegment([1, 3, 8, 9]), PitchClassSegment([7, 4])])
                Sequence([PitchClassSegment([0, 6, 1, 9]), PitchClassSegment([3, 8])])
                Sequence([PitchClassSegment([3, 9, 4, 0]), PitchClassSegment([6, 11])])
                Sequence([PitchClassSegment([6, 9, 8, 10]), PitchClassSegment([5, 11])])
                Sequence([PitchClassSegment([9, 0, 11, 1]), PitchClassSegment([8, 2])])
                Sequence([PitchClassSegment([9, 10, 11, 0]), PitchClassSegment([1, 2])])

                >>> expression.get_string()
                '[permute(X, row=[10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11]), T3(X)] Φ J'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(markup)
                    >>> print(string)
                    \markup {
                        \line
                            {
                                \concat
                                    {
                                        \concat
                                            {
                                                permute(
                                                \bold
                                                    X
                                                ", row=[10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])"
                                            }
                                        \concat
                                            {
                                                T
                                                \sub
                                                    3
                                                \bold
                                                    X
                                            }
                                    }
                                Φ
                                \bold
                                    J
                            }
                        }

        Returns sequence of accumulated sequences.

        Returns sequence of length ``count`` + 1 with integer ``count``.

        Returns sequence of orbit length with ``count`` set to identity.
        """
        if count is None:
            count = abjad.Exact
        if self._expression:
            return self._update_expression(
                inspect.currentframe(),
                evaluation_template="accumulate",
                subclass_hook="_evaluate_accumulate",
                map_operand=operands,
            )
        operands = operands or [Expression()]
        if not isinstance(operands, list):
            operands = [operands]
        items = [self]
        if count == abjad.Exact:
            for i in range(1000):
                sequence = items[-1]
                for operand in operands:
                    sequence = sequence.map(operand)
                    items.append(sequence)
                if sequence == items[0]:
                    items.pop(-1)
                    break
            else:
                message = "1000 iterations without identity:"
                message += f" {items[0]!r} to {items[-1]!r}."
                raise Exception(message)
        else:
            for i in range(count - 1):
                sequence = items[-1]
                for operand in operands:
                    sequence = sequence.map(operand)
                    items.append(sequence)
        return type(self)(items=items)

    @abjad.Signature(method_name="β", is_operator=True, superscript="count")
    def boustrophedon(self, count=2):
        r"""
        Iterates sequence boustrophedon.

        ..  container:: example

            Iterates atoms boustrophedon:

            >>> sequence = baca.sequence([1, 2, 3, 4, 5])

            >>> sequence.boustrophedon(count=0)
            Sequence([])

            >>> sequence.boustrophedon(count=1)
            Sequence([1, 2, 3, 4, 5])

            >>> sequence.boustrophedon(count=2)
            Sequence([1, 2, 3, 4, 5, 4, 3, 2, 1])

            >>> sequence.boustrophedon(count=3)
            Sequence([1, 2, 3, 4, 5, 4, 3, 2, 1, 2, 3, 4, 5])

        ..  container:: example

            Iterates collections boustrophedon:

            >>> collections = [
            ...     baca.PitchClassSegment([1, 2, 3]),
            ...     baca.PitchClassSegment([4, 5, 6]),
            ...     ]
            >>> sequence = baca.sequence(collections)

            >>> sequence.boustrophedon(count=0)
            Sequence([])

            >>> for collection in sequence.boustrophedon(count=1):
            ...     collection
            ...
            PitchClassSegment([1, 2, 3])
            PitchClassSegment([4, 5, 6])

            >>> for collection in sequence.boustrophedon(count=2):
            ...     collection
            ...
            PitchClassSegment([1, 2, 3])
            PitchClassSegment([4, 5, 6])
            PitchClassSegment([5, 4])
            PitchClassSegment([3, 2, 1])

            >>> for collection in sequence.boustrophedon(count=3):
            ...     collection
            ...
            PitchClassSegment([1, 2, 3])
            PitchClassSegment([4, 5, 6])
            PitchClassSegment([5, 4])
            PitchClassSegment([3, 2, 1])
            PitchClassSegment([2, 3])
            PitchClassSegment([4, 5, 6])

        ..  container:: example

            Iterates mixed items boustrophedon:

            >>> collection = baca.PitchClassSegment([1, 2, 3])
            >>> sequence = baca.sequence([collection, 4, 5])
            >>> for item in sequence.boustrophedon(count=3):
            ...     item
            ...
            PitchClassSegment([1, 2, 3])
            4
            5
            4
            PitchClassSegment([3, 2, 1])
            PitchClassSegment([2, 3])
            4
            5

        ..  container:: example expression

            >>> collections = [
            ...     baca.PitchClassSegment([1, 2, 3]),
            ...     baca.PitchClassSegment([4, 5, 6]),
            ...     ]

            >>> expression = baca.sequence(name='J')
            >>> expression = expression.boustrophedon(count=3)

            >>> for collection in expression(collections):
            ...     collection
            ...
            PitchClassSegment([1, 2, 3])
            PitchClassSegment([4, 5, 6])
            PitchClassSegment([5, 4])
            PitchClassSegment([3, 2, 1])
            PitchClassSegment([2, 3])
            PitchClassSegment([4, 5, 6])

            >>> expression.get_string()
            'β3(J)'

            >>> markup = expression.get_markup()
            >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(markup)
                >>> print(string)
                \markup {
                    \concat
                        {
                            β
                            \super
                                3
                            \bold
                                J
                        }
                    }

        Returns new sequence.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = []
        for i in range(count):
            if i == 0:
                for item in self:
                    result.append(copy.copy(item))
            elif i % 2 == 0:
                if isinstance(self[0], collections.abc.Iterable):
                    result.append(self[0][1:])
                else:
                    pass
                for item in self[1:]:
                    result.append(copy.copy(item))
            else:
                if isinstance(self[-1], collections.abc.Iterable):
                    item = type(self[-1])(list(reversed(self[-1]))[1:])
                    result.append(item)
                else:
                    pass
                for item in reversed(self[:-1]):
                    if isinstance(item, collections.abc.Iterable):
                        item = type(item)(list(reversed(item)))
                        result.append(item)
                    else:
                        result.append(item)
        return type(self)(items=result)

    def degree_of_rotational_symmetry(self):
        """
        Gets degree of rotational symmetry.

        ..  container:: example

            >>> baca.sequence([1, 1, 1, 1, 1, 1]).degree_of_rotational_symmetry()
            6

            >>> baca.sequence([1, 2, 1, 2, 1, 2]).degree_of_rotational_symmetry()
            3

            >>> baca.sequence([1, 2, 3, 1, 2, 3]).degree_of_rotational_symmetry()
            2

            >>> baca.sequence([1, 2, 3, 4, 5, 6]).degree_of_rotational_symmetry()
            1

            >>> baca.sequence().degree_of_rotational_symmetry()
            1

        Returns positive integer.
        """
        degree_of_rotational_symmetry = 0
        for index in range(len(self)):
            rotation = self[index:] + self[:index]
            if rotation == self:
                degree_of_rotational_symmetry += 1
        degree_of_rotational_symmetry = degree_of_rotational_symmetry or 1
        return degree_of_rotational_symmetry

    # TODO: remove ``counts`` in favor of partition-then-``indices`` recipe
    # TODO: generalize ``indices`` to pattern
    @abjad.Signature()
    def fuse(
        self,
        counts: typing.List[int] = None,
        *,
        cyclic: bool = None,
        indices: typing.Sequence[int] = None,
    ):
        r"""
        Fuses sequence by ``counts``.

        ..  container:: example expression

            Fuses items:

            >>> expression = baca.sequence().fuse()

            >>> divisions = baca.fractions([(7, 8), (3, 8), (5, 8)])
            >>> divisions = baca.sequence(divisions)
            >>> divisions = expression(divisions)
            >>> divisions = divisions.flatten(depth=-1)
            >>> divisions
            Sequence([NonreducedFraction(15, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music, divisions)
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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

            Fuses first two items and then remaining items:

            >>> expression = baca.sequence().fuse([2])

            >>> divisions = baca.fractions([(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)])
            >>> divisions = baca.sequence(divisions)
            >>> divisions = expression(divisions)
            >>> for division in divisions:
            ...     division
            NonreducedFraction(4, 8)
            NonreducedFraction(12, 8)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music)
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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

            Fuses items two at a time:

            >>> expression = baca.sequence().fuse([2], cyclic=True)

            >>> divisions = baca.fractions([(2, 8), (2, 8), (4, 8), (4, 8), (2, 4)])
            >>> divisions = baca.sequence(divisions)
            >>> divisions = expression(divisions)
            >>> for division in divisions:
            ...     division
            NonreducedFraction(4, 8)
            NonreducedFraction(8, 8)
            NonreducedFraction(2, 4)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music)
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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

            Splits each item by ``3/8``;  then flattens; then fuses into
            differently sized groups:

            >>> split = expression.split_divisions([(3, 8)], cyclic=True)
            >>> expression = baca.sequence().map(split)
            >>> expression = expression.flatten(depth=-1)
            >>> expression = expression.fuse([2, 3, 1])

            >>> divisions = baca.fractions([(7, 8), (3, 8), (5, 8)])
            >>> divisions = baca.sequence(divisions)
            >>> divisions = expression(divisions)
            >>> for division in divisions:
            ...     division
            NonreducedFraction(6, 8)
            NonreducedFraction(7, 8)
            NonreducedFraction(2, 8)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music)
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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

        ..  container:: example expression

            Splits into sixteenths; partitions; then fuses every other part:

            >>> split = baca.sequence().split_divisions([(1, 16)], cyclic=True)
            >>> expression = baca.sequence().fuse()
            >>> expression = expression.map(split)
            >>> expression = expression.flatten(depth=-1)
            >>> expression = expression.partition_by_ratio_of_lengths(
            ...     (1, 1, 1, 1, 1, 1),
            ... )
            >>> expression = expression.fuse(indices=[1, 3, 5])
            >>> expression = expression.flatten(depth=-1)

            >>> divisions = baca.fractions([(7, 8), (3, 8), (5, 8)])
            >>> divisions = baca.sequence(divisions)
            >>> divisions = expression(divisions)
            >>> for division in divisions:
            ...     division
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(5, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(5, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(1, 16)
            NonreducedFraction(5, 16)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions)
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music)
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
                \new Score
                <<
                    \new GlobalContext
                    {
                        \time 15/8
                        s1 * 15/8
                    }
                    \new RhythmicStaff
                    {
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'4
                        ~
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'4
                        ~
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'16
                        c'4
                        ~
                        c'16
                    }
                >>

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if indices is not None:
            assert all(isinstance(_, int) for _ in indices), repr(indices)
        if indices and counts:
            raise Exception("do not set indices and counts together.")
        if not indices:
            counts = counts or []
            sequence = self.partition_by_counts(counts, cyclic=cyclic, overhang=True)
        else:
            sequence = self
        items_ = []
        for i, item in enumerate(sequence):
            if indices and i not in indices:
                item_ = item
            else:
                # item_ = _divisions(item).sum()
                item_ = Sequence(item).sum()
            items_.append(item_)
        # sequence = _divisions(items_)
        sequence = Sequence(items_)
        sequence = sequence.flatten(depth=-1)
        return sequence

    def group_by_sign(self, sign=(-1, 0, 1)):
        r"""
        Groups sequence by sign of items.

        >>> sequence = baca.sequence(
        ...     [0, 0, -1, -1, 2, 3, -5, 1, 2, 5, -5, -6],
        ...     )

        ..  container:: example

            >>> for item in sequence.group_by_sign():
            ...     item
            ...
            Sequence([0, 0])
            Sequence([-1, -1])
            Sequence([2, 3])
            Sequence([-5])
            Sequence([1, 2, 5])
            Sequence([-5, -6])

        ..  container:: example

            >>> for item in sequence.group_by_sign([-1]):
            ...     item
            ...
            Sequence([0])
            Sequence([0])
            Sequence([-1, -1])
            Sequence([2])
            Sequence([3])
            Sequence([-5])
            Sequence([1])
            Sequence([2])
            Sequence([5])
            Sequence([-5, -6])

        ..  container:: example

            >>> for item in sequence.group_by_sign([0]):
            ...     item
            ...
            Sequence([0, 0])
            Sequence([-1])
            Sequence([-1])
            Sequence([2])
            Sequence([3])
            Sequence([-5])
            Sequence([1])
            Sequence([2])
            Sequence([5])
            Sequence([-5])
            Sequence([-6])

        ..  container:: example

            >>> for item in sequence.group_by_sign([1]):
            ...     item
            ...
            Sequence([0])
            Sequence([0])
            Sequence([-1])
            Sequence([-1])
            Sequence([2, 3])
            Sequence([-5])
            Sequence([1, 2, 5])
            Sequence([-5])
            Sequence([-6])

        ..  container:: example

            >>> for item in sequence.group_by_sign([-1, 0]):
            ...     item
            ...
            Sequence([0, 0])
            Sequence([-1, -1])
            Sequence([2])
            Sequence([3])
            Sequence([-5])
            Sequence([1])
            Sequence([2])
            Sequence([5])
            Sequence([-5, -6])

        ..  container:: example

            >>> for item in sequence.group_by_sign([-1, 1]):
            ...     item
            ...
            Sequence([0])
            Sequence([0])
            Sequence([-1, -1])
            Sequence([2, 3])
            Sequence([-5])
            Sequence([1, 2, 5])
            Sequence([-5, -6])

        ..  container:: example

            >>> for item in sequence.group_by_sign([0, 1]):
            ...     item
            ...
            Sequence([0, 0])
            Sequence([-1])
            Sequence([-1])
            Sequence([2, 3])
            Sequence([-5])
            Sequence([1, 2, 5])
            Sequence([-5])
            Sequence([-6])

        ..  container:: example

            >>> for item in sequence.group_by_sign([-1, 0, 1]):
            ...     item
            ...
            Sequence([0, 0])
            Sequence([-1, -1])
            Sequence([2, 3])
            Sequence([-5])
            Sequence([1, 2, 5])
            Sequence([-5, -6])

        Groups negative elements when ``-1`` in ``sign``.

        Groups zero-valued elements When ``0`` in ``sign``.

        Groups positive elements when ``1`` in ``sign``.

        Returns nested sequence.
        """
        items = []
        pairs = itertools.groupby(self, abjad.math.sign)
        for current_sign, group in pairs:
            if current_sign in sign:
                items.append(type(self)(group))
            else:
                for item in group:
                    items.append(type(self)([item]))
        return type(self)(items=items)

    @abjad.Signature(method_name="H")
    def helianthate(self, n=0, m=0):
        r"""
        Helianthates sequence.

        ..  container:: example

            Helianthates list of lists:

            ..  container:: example

                >>> sequence = baca.sequence([[1, 2, 3], [4, 5], [6, 7, 8]])
                >>> sequence = sequence.helianthate(n=-1, m=1)
                >>> for item in sequence:
                ...     item
                ...
                [1, 2, 3]
                [4, 5]
                [6, 7, 8]
                [5, 4]
                [8, 6, 7]
                [3, 1, 2]
                [7, 8, 6]
                [2, 3, 1]
                [4, 5]
                [1, 2, 3]
                [5, 4]
                [6, 7, 8]
                [4, 5]
                [8, 6, 7]
                [3, 1, 2]
                [7, 8, 6]
                [2, 3, 1]
                [5, 4]

            ..  container:: example expression


                >>> expression = baca.sequence()
                >>> expression = expression.helianthate(n=-1, m=1)

                >>> sequence = expression([[1, 2, 3], [4, 5], [6, 7, 8]])
                >>> for item in sequence:
                ...     item
                [1, 2, 3]
                [4, 5]
                [6, 7, 8]
                [5, 4]
                [8, 6, 7]
                [3, 1, 2]
                [7, 8, 6]
                [2, 3, 1]
                [4, 5]
                [1, 2, 3]
                [5, 4]
                [6, 7, 8]
                [4, 5]
                [8, 6, 7]
                [3, 1, 2]
                [7, 8, 6]
                [2, 3, 1]
                [5, 4]

        ..  container:: example

            Helianthates list of collections:

            ..  container:: example

                >>> J = baca.PitchClassSegment(items=[0, 2, 4])
                >>> K = baca.PitchClassSegment(items=[5, 6])
                >>> L = baca.PitchClassSegment(items=[7, 9, 11])
                >>> sequence = baca.sequence([J, K, L])
                >>> sequence = sequence.helianthate(n=-1, m=1)
                >>> for collection in sequence:
                ...     collection
                ...
                PitchClassSegment([0, 2, 4])
                PitchClassSegment([5, 6])
                PitchClassSegment([7, 9, 11])
                PitchClassSegment([6, 5])
                PitchClassSegment([11, 7, 9])
                PitchClassSegment([4, 0, 2])
                PitchClassSegment([9, 11, 7])
                PitchClassSegment([2, 4, 0])
                PitchClassSegment([5, 6])
                PitchClassSegment([0, 2, 4])
                PitchClassSegment([6, 5])
                PitchClassSegment([7, 9, 11])
                PitchClassSegment([5, 6])
                PitchClassSegment([11, 7, 9])
                PitchClassSegment([4, 0, 2])
                PitchClassSegment([9, 11, 7])
                PitchClassSegment([2, 4, 0])
                PitchClassSegment([6, 5])

            ..  container:: example expression

                >>> J = baca.PitchClassSegment(items=[0, 2, 4])
                >>> K = baca.PitchClassSegment(items=[5, 6])
                >>> L = baca.PitchClassSegment(items=[7, 9, 11])

                >>> expression = baca.sequence()
                >>> expression = expression.helianthate(n=-1, m=1)

                >>> for collection in expression([J, K, L]):
                ...     collection
                ...
                PitchClassSegment([0, 2, 4])
                PitchClassSegment([5, 6])
                PitchClassSegment([7, 9, 11])
                PitchClassSegment([6, 5])
                PitchClassSegment([11, 7, 9])
                PitchClassSegment([4, 0, 2])
                PitchClassSegment([9, 11, 7])
                PitchClassSegment([2, 4, 0])
                PitchClassSegment([5, 6])
                PitchClassSegment([0, 2, 4])
                PitchClassSegment([6, 5])
                PitchClassSegment([7, 9, 11])
                PitchClassSegment([5, 6])
                PitchClassSegment([11, 7, 9])
                PitchClassSegment([4, 0, 2])
                PitchClassSegment([9, 11, 7])
                PitchClassSegment([2, 4, 0])
                PitchClassSegment([6, 5])

        ..  container:: example

            Trivial helianthation:

            ..  container:: example

                >>> items = [[1, 2, 3], [4, 5], [6, 7, 8]]
                >>> sequence = baca.sequence(items)
                >>> sequence.helianthate()
                Sequence([[1, 2, 3], [4, 5], [6, 7, 8]])

            ..  container:: example expression

                >>> expression = baca.sequence()
                >>> expression = expression.helianthate()

                >>> expression([[1, 2, 3], [4, 5], [6, 7, 8]])
                Sequence([[1, 2, 3], [4, 5], [6, 7, 8]])

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        start = list(self[:])
        result = list(self[:])
        assert isinstance(n, int), repr(n)
        assert isinstance(m, int), repr(m)
        original_n = n
        original_m = m

        def _generalized_rotate(argument, n=0):
            if hasattr(argument, "rotate"):
                return argument.rotate(n=n)
            argument_type = type(argument)
            argument = type(self)(argument).rotate(n=n)
            argument = argument_type(argument)
            return argument

        i = 0
        while True:
            inner = [_generalized_rotate(_, m) for _ in self]
            candidate = _generalized_rotate(inner, n)
            if candidate == start:
                break
            result.extend(candidate)
            n += original_n
            m += original_m
            i += 1
            if i == 1000:
                message = "1000 iterations without identity."
                raise Exception(message)
        return type(self)(items=result)

    @abjad.Signature(is_operator=True, method_name="P", subscript="counts")
    def partition(self, counts=None):
        r"""
        Partitions sequence cyclically by ``counts`` with overhang.

        ..  container:: example

            ..  container:: example

                >>> sequence = baca.sequence(range(16))
                >>> parts = sequence.partition([3])

                >>> for part in parts:
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4, 5])
                Sequence([6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14])
                Sequence([15])

            ..  container:: example expression

                >>> expression = baca.sequence(name='J').partition([3])

                >>> for part in expression(range(16)):
                ...     part
                Sequence([0, 1, 2])
                Sequence([3, 4, 5])
                Sequence([6, 7, 8])
                Sequence([9, 10, 11])
                Sequence([12, 13, 14])
                Sequence([15])

                >>> expression.get_string()
                'P[3](J)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(markup)
                    >>> print(string)
                    \markup {
                        \concat
                            {
                                P
                                \sub
                                    [3]
                                \bold
                                    J
                            }
                        }

        Returns new sequence.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.partition_by_counts(counts=counts, cyclic=True, overhang=True)

    def period_of_rotation(self):
        """
        Gets period of rotation.

        ..  container:: example

            >>> baca.sequence([1, 2, 3, 4, 5, 6]).period_of_rotation()
            6

            >>> baca.sequence([1, 2, 3, 1, 2, 3]).period_of_rotation()
            3

            >>> baca.sequence([1, 2, 1, 2, 1, 2]).period_of_rotation()
            2

            >>> baca.sequence([1, 1, 1, 1, 1, 1]).period_of_rotation()
            1

            >>> baca.sequence().period_of_rotation()
            0

        Defined equal to length of sequence divided by degree of rotational
        symmetry of sequence.

        Returns positive integer.
        """
        return len(self) // self.degree_of_rotational_symmetry()

    @abjad.Signature()
    def quarters(
        self,
        *,
        compound: abjad.DurationTyping = None,
        remainder: abjad.VerticalAlignment = None,
    ):
        r"""
        Splits sequence into quarter-note durations.

        ..  container:: example expression

            >>> expression = baca.sequence().quarters()
            >>> for item in expression(baca.fractions([(2, 4), (6, 4)])):
            ...     item
            ...
            Sequence([NonreducedFraction(1, 4)])
            Sequence([NonreducedFraction(1, 4)])
            Sequence([NonreducedFraction(1, 4)])
            Sequence([NonreducedFraction(1, 4)])
            Sequence([NonreducedFraction(1, 4)])
            Sequence([NonreducedFraction(1, 4)])
            Sequence([NonreducedFraction(1, 4)])
            Sequence([NonreducedFraction(1, 4)])

        ..  container:: example expression

            >>> expression = baca.sequence().quarters(compound=(3, 2))
            >>> for item in expression(baca.fractions([(6, 4)])):
            ...     item
            ...
            Sequence([NonreducedFraction(3, 8)])
            Sequence([NonreducedFraction(3, 8)])
            Sequence([NonreducedFraction(3, 8)])
            Sequence([NonreducedFraction(3, 8)])

        ..  container:: example expression

            Maps to each division: splits by ``1/4`` with remainder on right:

            >>> expression = baca.sequence().map(baca.sequence().quarters())

            >>> divisions = baca.fractions([(7, 8), (3, 8), (5, 8)])
            >>> divisions = baca.sequence(divisions)
            >>> divisions = expression(divisions)
            >>> for sequence in divisions:
            ...     print("sequence:")
            ...     for division in sequence:
            ...         print(f"\t{repr(division)}")
            sequence:
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(1, 8)])
            sequence:
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(1, 8)])
            sequence:
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(1, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music)
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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
                        c'8
                        c'4
                        c'8
                        c'4
                        c'4
                        c'8
                    }
                >>

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        sequence = self.split_divisions(
            [(1, 4)], cyclic=True, compound=compound, remainder=remainder
        )
        return sequence

    @abjad.Signature()
    def ratios(
        self,
        ratios: typing.Sequence[abjad.RatioTyping],
        *,
        rounded: bool = None,
        _map_index: int = None,
    ):
        r"""
        Splits sequence by ``ratios``.

        ..  container:: example expression

            Splits sequence by exact ``2:1`` ratio:

            >>> expression = baca.sequence()
            >>> expression = expression.ratios([(2, 1)])

            >>> time_signatures = baca.fractions([(5, 8), (6, 8)])
            >>> divisions = baca.sequence(time_signatures)
            >>> divisions = expression(divisions)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                NonreducedFraction(5, 8)
                NonreducedFraction(7, 24)
            sequence:
                NonreducedFraction(11, 24)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     music, time_signatures
            ... )
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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
                        c'2
                        ~
                        c'8
                        \tweak edge-height #'(0.7 . 0)
                        \times 16/24 {
                            c'4..
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 16/24 {
                            c'2
                            ~
                            c'8.
                        }
                    }
                >>

            Splits divisions by rounded ``2:1`` ratio:

            >>> expression = baca.sequence()
            >>> expression = expression.ratios([(2, 1)], rounded=True)

            >>> time_signatures = baca.fractions([(5, 8), (6, 8)])
            >>> divisions = baca.sequence(time_signatures)
            >>> divisions = expression(divisions)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                NonreducedFraction(5, 8)
                NonreducedFraction(2, 8)
            sequence:
                NonreducedFraction(4, 8)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     music, time_signatures
            ... )
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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
                        c'2
                        ~
                        c'8
                        c'4
                        c'2
                    }
                >>

        ..  container:: example expression

            Splits each division by exact ``2:1`` ratio:

            >>> split = baca.sequence().ratios([(2, 1)])
            >>> expression = baca.sequence().map(split)

            >>> time_signatures = baca.fractions([(5, 8), (6, 8)])
            >>> divisions = baca.sequence(time_signatures)
            >>> divisions = expression(divisions)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                Sequence([NonreducedFraction(10, 24)])
                Sequence([NonreducedFraction(5, 24)])
            sequence:
                Sequence([NonreducedFraction(4, 8)])
                Sequence([NonreducedFraction(2, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     music, time_signatures
            ... )
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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
                        \tweak edge-height #'(0.7 . 0)
                        \times 16/24 {
                            c'2
                            ~
                            c'8
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 16/24 {
                            c'4
                            ~
                            c'16
                        }
                        c'2
                        c'4
                    }
                >>

            Splits each division by rounded ``2:1`` ratio:

            >>> split = baca.sequence().ratios([(2, 1)], rounded=True)
            >>> expression = baca.sequence().map(split)

            >>> time_signatures = baca.fractions([(5, 8), (6, 8)])
            >>> divisions = baca.sequence(time_signatures)
            >>> divisions = expression(divisions)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                Sequence([NonreducedFraction(3, 8)])
                Sequence([NonreducedFraction(2, 8)])
            sequence:
                Sequence([NonreducedFraction(4, 8)])
                Sequence([NonreducedFraction(2, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     music, time_signatures
            ... )
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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

            Splits divisions with alternating exact ``2:1`` and ``1:1:1``
            ratios:

            >>> split = baca.sequence().ratios([(2, 1), (1, 1, 1)])
            >>> expression = baca.sequence().map(split)

            >>> time_signatures = baca.fractions([(5, 8), (6, 8)])
            >>> divisions = baca.sequence(time_signatures)
            >>> divisions = expression(divisions)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                Sequence([NonreducedFraction(10, 24)])
                Sequence([NonreducedFraction(5, 24)])
            sequence:
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(2, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     music, time_signatures
            ...     )
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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
                        \tweak edge-height #'(0.7 . 0)
                        \times 16/24 {
                            c'2
                            ~
                            c'8
                        }
                        \tweak edge-height #'(0.7 . 0)
                        \times 16/24 {
                            c'4
                            ~
                            c'16
                        }
                        c'4
                        c'4
                        c'4
                    }
                >>

            Splits divisions with alternating rounded ``2:1`` and ``1:1:1``
            ratios:

            >>> split = baca.sequence().ratios(
            ...     [(2, 1), (1, 1, 1)], rounded=True
            ... )
            >>> expression = baca.sequence().map(split)

            >>> time_signatures = baca.fractions([(5, 8), (6, 8)])
            >>> divisions = baca.sequence(time_signatures)
            >>> divisions = expression(divisions)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                Sequence([NonreducedFraction(3, 8)])
                Sequence([NonreducedFraction(2, 8)])
            sequence:
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(2, 8)])
                Sequence([NonreducedFraction(2, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     music, time_signatures
            ...     )
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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
        ratios_ = abjad.CyclicTuple([abjad.Ratio(_) for _ in ratios])
        if rounded is not None:
            rounded = bool(rounded)
        _map_index = _map_index or 0
        weight = sum(self)
        assert isinstance(weight, abjad.NonreducedFraction)
        numerator, denominator = weight.pair
        ratio = ratios_[_map_index]
        if rounded is True:
            numerators = ratio.partition_integer(numerator)
            divisions = [
                abjad.NonreducedFraction((numerator, denominator))
                for numerator in numerators
            ]
        else:
            divisions = []
            ratio_weight = sum(ratio)
            for number in ratio:
                multiplier = abjad.Fraction(number, ratio_weight)
                division = multiplier * weight
                divisions.append(division)
        sequence = self.split(divisions)
        sequence = Sequence(sequence)
        return sequence

    @abjad.Signature()
    def repeat_by(self, counts=None, cyclic=None):
        r"""
        Repeat sequence elements at ``counts``.

        ..  container:: example

            With no counts:

            ..  container:: example

                >>> baca.sequence([[1, 2, 3], 4, [5, 6]]).repeat_by()
                Sequence([[1, 2, 3], 4, [5, 6]])

            ..  container:: example expression

                >>> expression = baca.sequence(name='J').repeat_by()

                >>> expression([[1, 2, 3], 4, [5, 6]])
                Sequence([[1, 2, 3], 4, [5, 6]])

                >>> expression.get_string()
                'repeat_by(J)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(markup)
                    >>> print(string)
                    \markup {
                        \concat
                            {
                                repeat_by(
                                \bold
                                    J
                                )
                            }
                        }

        ..  container:: example

            With acyclic counts:

            >>> sequence = baca.sequence([[1, 2, 3], 4, [5, 6]])

            ..  container:: example

                >>> sequence.repeat_by([0])
                Sequence([4, [5, 6]])

                >>> sequence.repeat_by([1])
                Sequence([[1, 2, 3], 4, [5, 6]])

                >>> sequence.repeat_by([2])
                Sequence([[1, 2, 3], [1, 2, 3], 4, [5, 6]])

                >>> sequence.repeat_by([3])
                Sequence([[1, 2, 3], [1, 2, 3], [1, 2, 3], 4, [5, 6]])

            ..  container:: example

                >>> sequence.repeat_by([1, 0])
                Sequence([[1, 2, 3], [5, 6]])

                >>> sequence.repeat_by([1, 1])
                Sequence([[1, 2, 3], 4, [5, 6]])

                >>> sequence.repeat_by([1, 2])
                Sequence([[1, 2, 3], 4, 4, [5, 6]])

                >>> sequence.repeat_by([1, 3])
                Sequence([[1, 2, 3], 4, 4, 4, [5, 6]])

            ..  container:: example

                >>> sequence.repeat_by([1, 1, 0])
                Sequence([[1, 2, 3], 4])

                >>> sequence.repeat_by([1, 1, 1])
                Sequence([[1, 2, 3], 4, [5, 6]])

                >>> sequence.repeat_by([1, 1, 2])
                Sequence([[1, 2, 3], 4, [5, 6], [5, 6]])

                >>> sequence.repeat_by([1, 1, 3])
                Sequence([[1, 2, 3], 4, [5, 6], [5, 6], [5, 6]])

            ..  container:: example expression

                >>> expression = baca.sequence(name='J').repeat_by([2])

                >>> expression([[1, 2, 3], 4, [5, 6]])
                Sequence([[1, 2, 3], [1, 2, 3], 4, [5, 6]])

                >>> expression.get_string()
                'repeat_by(J, counts=[2])'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(markup)
                    >>> print(string)
                    \markup {
                        \concat
                            {
                                repeat_by(
                                \bold
                                    J
                                ", counts=[2])"
                            }
                        }

        ..  container:: example

            With cyclic counts:

            ..  container:: example

                >>> sequence.repeat_by([0], cyclic=True)
                Sequence([])

                >>> sequence.repeat_by([1], cyclic=True)
                Sequence([[1, 2, 3], 4, [5, 6]])

                >>> sequence.repeat_by([2], cyclic=True)
                Sequence([[1, 2, 3], [1, 2, 3], 4, 4, [5, 6], [5, 6]])

                >>> sequence.repeat_by([3], cyclic=True)
                Sequence([[1, 2, 3], [1, 2, 3], [1, 2, 3], 4, 4, 4, [5, 6], [5, 6], [5, 6]])

            ..  container:: example

                >>> sequence.repeat_by([2, 0], cyclic=True)
                Sequence([[1, 2, 3], [1, 2, 3], [5, 6], [5, 6]])

                >>> sequence.repeat_by([2, 1], cyclic=True)
                Sequence([[1, 2, 3], [1, 2, 3], 4, [5, 6], [5, 6]])

                >>> sequence.repeat_by([2, 2], cyclic=True)
                Sequence([[1, 2, 3], [1, 2, 3], 4, 4, [5, 6], [5, 6]])

                >>> sequence.repeat_by([2, 3], cyclic=True)
                Sequence([[1, 2, 3], [1, 2, 3], 4, 4, 4, [5, 6], [5, 6]])

            ..  container:: example expression

                >>> expression = baca.sequence(name='J')
                >>> expression = expression.repeat_by([2], cyclic=True)

                >>> expression([[1, 2, 3], 4, [5, 6]])
                Sequence([[1, 2, 3], [1, 2, 3], 4, 4, [5, 6], [5, 6]])

                >>> expression.get_string()
                'repeat_by(J, counts=[2], cyclic=True)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(markup)
                    >>> print(string)
                    \markup {
                        \concat
                            {
                                repeat_by(
                                \bold
                                    J
                                ", counts=[2], cyclic=True)"
                            }
                        }

        Raises exception on negative counts.

        Returns new sequence.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if counts is None:
            return type(self)(self)
        counts = counts or [1]
        assert isinstance(counts, collections.abc.Iterable)
        if cyclic is True:
            counts = abjad.CyclicTuple(counts)
        items = []
        for i, item in enumerate(self):
            try:
                count = counts[i]
            except IndexError:
                count = 1
            items.extend(count * [item])
        return type(self)(items)

    @abjad.Signature()
    def reveal(self, count=None):
        r"""
        Reveals contents of sequence.

        ..  container:: example

            With no count:

            ..  container:: example

                >>> baca.sequence([[1, 2, 3], 4, [5, 6]]).reveal()
                Sequence([[1, 2, 3], 4, [5, 6]])

            ..  container:: example expression

                >>> expression = baca.sequence(name='J').reveal()

                >>> expression([[1, 2, 3], 4, [5, 6]])
                Sequence([[1, 2, 3], 4, [5, 6]])

                >>> expression.get_string()
                'reveal(J)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(markup)
                    >>> print(string)
                    \markup {
                        \concat
                            {
                                reveal(
                                \bold
                                    J
                                )
                            }
                        }

        ..  container:: example

            With zero count:

            ..  container:: example expression

                >>> baca.sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=0)
                Sequence([])

            ..  container:: example expression

                >>> expression = baca.sequence(name='J').reveal(count=0)

                >>> expression([[1, 2, 3], 4, [5, 6]])
                Sequence([])

                >>> expression.get_string()
                'reveal(J, count=0)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(markup)
                    >>> print(string)
                    \markup {
                        \concat
                            {
                                reveal(
                                \bold
                                    J
                                ", count=0)"
                            }
                        }

        ..  container:: example

            With positive count:

            ..  container:: example

                >>> baca.sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=1)
                Sequence([[1]])

                >>> baca.sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=2)
                Sequence([[1, 2]])

                >>> baca.sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=3)
                Sequence([[1, 2, 3]])

                >>> baca.sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=4)
                Sequence([[1, 2, 3], 4])

                >>> baca.sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=5)
                Sequence([[1, 2, 3], 4, [5]])

                >>> baca.sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=6)
                Sequence([[1, 2, 3], 4, [5, 6]])

                >>> baca.sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=99)
                Sequence([[1, 2, 3], 4, [5, 6]])

            ..  container:: example expression

                >>> expression = baca.sequence(name='J').reveal(count=2)

                >>> expression([[1, 2, 3], 4, [5, 6]])
                Sequence([[1, 2]])

                >>> expression.get_string()
                'reveal(J, count=2)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(markup)
                    >>> print(string)
                    \markup {
                        \concat
                            {
                                reveal(
                                \bold
                                    J
                                ", count=2)"
                            }
                        }

        ..  container:: example

            With negative count:

            ..  container:: example

                >>> baca.sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-1)
                Sequence([[6]])

                >>> baca.sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-2)
                Sequence([[5, 6]])

                >>> baca.sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-3)
                Sequence([4, [5, 6]])

                >>> baca.sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-4)
                Sequence([[3], 4, [5, 6]])

                >>> baca.sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-5)
                Sequence([[2, 3], 4, [5, 6]])

                >>> baca.sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-6)
                Sequence([[1, 2, 3], 4, [5, 6]])

                >>> baca.sequence([[1, 2, 3], 4, [5, 6]]).reveal(count=-99)
                Sequence([[1, 2, 3], 4, [5, 6]])

            ..  container:: example expression

                >>> expression = baca.sequence(name='J').reveal(count=-2)

                >>> expression([[1, 2, 3], 4, [5, 6]])
                Sequence([[5, 6]])

                >>> expression.get_string()
                'reveal(J, count=-2)'

                >>> markup = expression.get_markup()
                >>> abjad.show(markup, align_tags=89) # doctest: +SKIP

                ..  docs::

                    >>> string = abjad.lilypond(markup)
                    >>> print(string)
                    \markup {
                        \concat
                            {
                                reveal(
                                \bold
                                    J
                                ", count=-2)"
                            }
                        }

        Returns new sequence.
        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        if count is None:
            return type(self)(items=self)
        if count == 0:
            return type(self)()
        if count < 0:
            result = self.reverse(recurse=True)
            result = result.reveal(count=abs(count))
            result = result.reverse(recurse=True)
            return result
        current = 0
        items_ = []
        for item in self:
            if isinstance(item, collections.abc.Iterable):
                subitems_ = []
                for subitem in item:
                    subitems_.append(subitem)
                    current += 1
                    if current == count:
                        item_ = type(item)(subitems_)
                        items_.append(item_)
                        return type(self)(items=items_)
                item_ = type(item)(subitems_)
                items_.append(item_)
            else:
                items_.append(item)
                current += 1
                if current == count:
                    return type(self)(items=items_)
        return type(self)(items=items_)

    @abjad.Signature()
    def split_divisions(
        self,
        durations: typing.List[abjad.DurationTyping],
        *,
        compound: abjad.DurationTyping = None,
        cyclic: bool = None,
        remainder: abjad.HorizontalAlignment = None,
        remainder_fuse_threshold: abjad.DurationTyping = None,
        rotate_indexed: int = None,
        _map_index: int = None,
    ):
        r"""
        Splits sequence divisions by ``durations``.

        ..  container:: example

            Splits every five sixteenths:

            >>> divisions = baca.fractions(10 * [(1, 8)])
            >>> divisions = baca.sequence(divisions)

            Splits division sequence every five sixteenths:

            >>> divisions = divisions.split_divisions([(5, 16)], cyclic=True)
            >>> for i, sequence_ in enumerate(divisions):
            ...     print(f"sequence {i}")
            ...     for division in sequence_:
            ...         print("\t" + repr(division))
            sequence 0
                NonreducedFraction(1, 8)
                NonreducedFraction(1, 8)
                NonreducedFraction(1, 16)
            sequence 1
                NonreducedFraction(1, 16)
                NonreducedFraction(1, 8)
                NonreducedFraction(1, 8)
            sequence 2
                NonreducedFraction(1, 8)
                NonreducedFraction(1, 8)
                NonreducedFraction(1, 16)
            sequence 3
                NonreducedFraction(1, 16)
                NonreducedFraction(1, 8)
                NonreducedFraction(1, 8)

        ..  container:: example expression

            Fuses divisions and then splits by ``1/4`` with remainder on right:

            >>> expression = baca.sequence().fuse()
            >>> expression = expression.split_divisions([(1, 4)], cyclic=True)

            >>> divisions = [(7, 8), (3, 8), (5, 8)]
            >>> divisions = [abjad.NonreducedFraction(_) for _ in divisions]
            >>> divisions = baca.sequence(divisions)
            >>> divisions = expression(divisions)
            >>> for item in divisions:
            ...     item
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(1, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music)
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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

            >>> expression = baca.sequence().fuse()
            >>> expression = expression.split_divisions(
            ...     [(1, 4)], cyclic=True, remainder_fuse_threshold=(1, 8)
            ... )

            >>> divisions = [(7, 8), (3, 8), (5, 8)]
            >>> divisions = [abjad.NonreducedFraction(_) for _ in divisions]
            >>> divisions = baca.sequence(divisions)
            >>> divisions = expression(divisions)
            >>> for item in divisions:
            ...     item
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(3, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music)
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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

            >>> expression = baca.sequence().fuse()
            >>> expression = expression.split_divisions(
            ...     [(1, 4)], cyclic=True, remainder=abjad.Left
            ... )

            >>> divisions = [(7, 8), (3, 8), (5, 8)]
            >>> divisions = [abjad.NonreducedFraction(_) for _ in divisions]
            >>> divisions = baca.sequence(divisions)
            >>> divisions = expression(divisions)
            >>> for item in divisions:
            ...     item
            Sequence([NonreducedFraction(1, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music)
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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

            >>> expression = baca.sequence().fuse()
            >>> expression = expression.split_divisions(
            ...     [(1, 4)],
            ...     cyclic=True,
            ...     remainder=abjad.Left,
            ...     remainder_fuse_threshold=(1, 8),
            ... )

            >>> divisions = [(7, 8), (3, 8), (5, 8)]
            >>> divisions = [abjad.NonreducedFraction(_) for _ in divisions]
            >>> divisions = baca.sequence(divisions)
            >>> divisions = expression(divisions)
            >>> for item in divisions:
            ...     item
            Sequence([NonreducedFraction(3, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])
            Sequence([NonreducedFraction(2, 8)])

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))
            >>> lilypond_file = abjad.LilyPondFile.rhythm(music)
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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

        ..  container:: example expression

            Splits each division into quarters and positions remainder at
            right:

            >>> expression = baca.sequence()
            >>> quarters = baca.sequence().quarters().flatten(depth=-1)
            >>> expression = expression.map(quarters)

            >>> time_signatures = baca.fractions([(7, 8), (7, 8), (7, 16)])
            >>> time_signatures = [abjad.NonreducedFraction(_) for _ in time_signatures]
            >>> divisions = baca.sequence(time_signatures)
            >>> divisions = expression(divisions)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                NonreducedFraction(2, 8)
                NonreducedFraction(2, 8)
                NonreducedFraction(2, 8)
                NonreducedFraction(1, 8)
            sequence:
                NonreducedFraction(2, 8)
                NonreducedFraction(2, 8)
                NonreducedFraction(2, 8)
                NonreducedFraction(1, 8)
            sequence:
                NonreducedFraction(4, 16)
                NonreducedFraction(3, 16)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     music, time_signatures
            ... )
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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

            >>> quarters = baca.sequence().quarters(remainder=abjad.Left)
            >>> quarters = quarters.flatten(depth=-1)
            >>> expression = expression.map(quarters)

            >>> time_signatures = [(7, 8), (7, 8), (7, 16)]
            >>> time_signatures = [abjad.NonreducedFraction(_) for _ in time_signatures]
            >>> divisions = baca.sequence(time_signatures)
            >>> divisions = expression(divisions)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                NonreducedFraction(1, 8)
                NonreducedFraction(2, 8)
                NonreducedFraction(2, 8)
                NonreducedFraction(2, 8)
            sequence:
                NonreducedFraction(1, 8)
                NonreducedFraction(2, 8)
                NonreducedFraction(2, 8)
                NonreducedFraction(2, 8)
            sequence:
                NonreducedFraction(3, 16)
                NonreducedFraction(4, 16)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     music, time_signatures
            ...     )
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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

            >>> quarters = baca.sequence().split_divisions(
            ...     [(1, 4)],
            ...     cyclic=True,
            ...     remainder_fuse_threshold=(1, 8)
            ... )
            >>> quarters = quarters.flatten(depth=-1)
            >>> expression = baca.sequence().map(quarters)

            >>> time_signatures = [abjad.NonreducedFraction(5, 8)]
            >>> divisions = baca.sequence(time_signatures)
            >>> divisions = expression(divisions)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                NonreducedFraction(2, 8)
                NonreducedFraction(3, 8)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     music, time_signatures
            ...     )
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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

            >>> quarters = baca.sequence().split_divisions(
            ...     [(1, 4)],
            ...     cyclic=True,
            ...     remainder=abjad.Left,
            ...     remainder_fuse_threshold=(1, 8)
            ... )
            >>> quarters = quarters.flatten(depth=-1)
            >>> expression = baca.sequence().map(quarters)

            >>> time_signatures = [abjad.NonreducedFraction(5, 8)]
            >>> divisions = baca.sequence(time_signatures)
            >>> divisions = expression(divisions)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                NonreducedFraction(3, 8)
                NonreducedFraction(2, 8)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     music, time_signatures
            ...     )
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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

        ..  container:: example expression

            Splits each division into compound quarters:

            >>> quarters = baca.sequence().quarters(compound=(3, 2))
            >>> quarters = quarters.flatten(depth=-1)
            >>> expression = baca.sequence().map(quarters)

            >>> time_signatures = baca.fractions([(3, 4), (6, 8)])
            >>> divisions = baca.sequence(time_signatures)
            >>> divisions = expression(divisions)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                NonreducedFraction(1, 4)
                NonreducedFraction(1, 4)
                NonreducedFraction(1, 4)
            sequence:
                NonreducedFraction(3, 8)
                NonreducedFraction(3, 8)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     music, time_signatures
            ...     )
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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

        ..  container:: example expression

            Splits each division by durations and rotates durations one to the
            left at each new division:

            >>> split = baca.sequence().split_divisions(
            ...     [(1, 16), (1, 8), (1, 4)],
            ...     cyclic=True,
            ...     rotate_indexed=-1,
            ...     )
            >>> split = split.flatten(depth=-1)
            >>> expression = baca.sequence().map(split)

            >>> time_signatures = baca.fractions([(7, 16), (7, 16), (7, 16)])
            >>> divisions = baca.sequence(time_signatures)
            >>> divisions = expression(divisions)
            >>> for item in divisions:
            ...     print("sequence:")
            ...     for division in item:
            ...         print(f"\t{repr(division)}")
            sequence:
                NonreducedFraction(1, 16)
                NonreducedFraction(2, 16)
                NonreducedFraction(4, 16)
            sequence:
                NonreducedFraction(2, 16)
                NonreducedFraction(4, 16)
                NonreducedFraction(1, 16)
            sequence:
                NonreducedFraction(4, 16)
                NonreducedFraction(1, 16)
                NonreducedFraction(2, 16)

            >>> rhythm_maker = rmakers.note()
            >>> music = rhythm_maker(divisions.flatten(depth=-1))
            >>> lilypond_file = abjad.LilyPondFile.rhythm(
            ...     music, time_signatures
            ... )
            >>> abjad.show(lilypond_file, align_tags=89) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
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

        """
        if self._expression:
            return self._update_expression(inspect.currentframe())
        durations = [abjad.Duration(_) for _ in durations]
        if compound is not None:
            compound = abjad.Multiplier(compound)
        if compound is not None:
            divisions = self.flatten(depth=-1)
            meters = [abjad.Meter(_) for _ in divisions]
            if all(_.is_compound for _ in meters):
                durations = [compound * _ for _ in durations]
        if cyclic is not None:
            cyclic = bool(cyclic)
        if rotate_indexed is not None:
            assert isinstance(rotate_indexed, int)
        rotate_indexed = rotate_indexed or 0
        if remainder is not None:
            assert remainder in (abjad.Left, abjad.Right), repr(remainder)
        if remainder_fuse_threshold is not None:
            remainder_fuse_threshold = abjad.Duration(remainder_fuse_threshold)
        if _map_index is not None:
            assert isinstance(_map_index, int), repr(_map_index)
            n = rotate_indexed * _map_index
            durations_ = abjad.sequence(durations).rotate(n=n)
            durations = list(durations_)
        sequence = abjad.Sequence.split(self, durations, cyclic=cyclic, overhang=True)
        without_overhang = abjad.Sequence.split(
            self, durations, cyclic=cyclic, overhang=False
        )
        if sequence != without_overhang:
            items = list(sequence)
            remaining_item = items.pop()
            if remainder == abjad.Left:
                if remainder_fuse_threshold is None:
                    items.insert(0, remaining_item)
                elif sum(remaining_item) <= remainder_fuse_threshold:
                    fused_value = Sequence([remaining_item, items[0]])
                    fused_value = fused_value.flatten(depth=-1)
                    fused_value = fused_value.fuse()
                    items[0] = fused_value
                else:
                    items.insert(0, remaining_item)
            else:
                if remainder_fuse_threshold is None:
                    items.append(remaining_item)
                elif sum(remaining_item) <= remainder_fuse_threshold:
                    fused_value = Sequence([items[-1], remaining_item])
                    fused_value = fused_value.flatten(depth=-1)
                    fused_value = fused_value.fuse()
                    items[-1] = fused_value
                else:
                    items.append(remaining_item)
            sequence = Sequence(items)
        return sequence


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
        Tree(items=[Tree(items=4), Tree(items=5)])

        >>> string = abjad.storage(tree[1])
        >>> print(string)
        baca.Tree(
            items=[
                baca.Tree(
                    items=4,
                    ),
                baca.Tree(
                    items=5,
                    ),
                ],
            )

        >>> tree[1].get_payload(nested=True)
        [4, 5]

        >>> tree[1].get_payload()
        [4, 5]

    ..  container:: example

        Here's a leaf:

        >>> tree[1][0]
        Tree(items=4)

        >>> string = abjad.storage(tree[1][0])
        >>> print(string)
        baca.Tree(
            items=4,
            )

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
        "_equivalence_markup",
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

            >>> for node in tree:
            ...     node
            Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])])
            Tree(items=[Tree(items=4), Tree(items=5)])

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
        Is true when ``argument`` is the same type as tree and when the payload
        of all subtrees are equal.

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

            Gets node:

            >>> items = [[[0, 1], [2, 3]], [4, 5]]
            >>> tree = baca.Tree(items=items)

            >>> tree[-1]
            Tree(items=[Tree(items=4), Tree(items=5)])

        ..  container:: example

            Gets slice:

            >>> tree[-1:]
            [Tree(items=[Tree(items=4), Tree(items=5)])]

        Returns node or slice of nodes.
        """
        return self._children.__getitem__(argument)

    def __graph__(self, **keywords):
        """
        Graphs tree.

        ..  container:: example

            Graphs tree:

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

        Required to be explicitly redefined on Python 3 if __eq__ changes.

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

            Gets length of tree:

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
            Tree(items=[Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])]), Tree(items=[Tree(items=4), Tree(items=5)])])

        ..  container:: example

            Gets interpreter representation of leaf:

            >>> baca.Tree(0)
            Tree(items=0)

        ..  container:: example

            Gets interpreter representation of empty tree:

            >>> baca.Tree()
            Tree()

        Returns string.
        """
        return abjad.StorageFormatManager(self).get_repr_format()

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

    def _get_format_specification(self):
        return abjad.FormatSpecification(client=self)

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
            [Tree(items=1), Tree(items=2), Tree(items=3), Tree(items=4), Tree(items=5), Tree(items=6), Tree(items=7)]

            Gets all nodes at level -1:

            >>> tree[0][0]._get_next_n_nodes_at_level(None, -1)
            [Tree(items=1), Tree(items=2), Tree(items=3), Tree(items=4), Tree(items=5), Tree(items=6), Tree(items=7)]

            Gets next 4 nodes at level 2:

            >>> tree[0][0]._get_next_n_nodes_at_level(4, 2)
            [Tree(items=1), Tree(items=2), Tree(items=3), Tree(items=4)]

            Gets next 3 nodes at level 1:

            >>> tree[0][0]._get_next_n_nodes_at_level(3, 1)
            [Tree(items=[Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)]), Tree(items=[Tree(items=4), Tree(items=5)])]

            Gets next node at level 0:

            >>> tree[0][0]._get_next_n_nodes_at_level(1, 0)
            [Tree(items=[Tree(items=[Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)]), Tree(items=[Tree(items=4), Tree(items=5)]), Tree(items=[Tree(items=6), Tree(items=7)])])]

            Gets next 4 nodes at level -1:

            >>> tree[0][0]._get_next_n_nodes_at_level(4, -1)
            [Tree(items=1), Tree(items=2), Tree(items=3), Tree(items=4)]

            Gets next 3 nodes at level -2:

            >>> tree[0][0]._get_next_n_nodes_at_level(3, -2)
            [Tree(items=[Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)]), Tree(items=[Tree(items=4), Tree(items=5)])]

            Gets previous 4 nodes at level 2:

            >>> tree[-1][-1]._get_next_n_nodes_at_level(-4, 2)
            [Tree(items=6), Tree(items=5), Tree(items=4), Tree(items=3)]

            Gets previous 3 nodes at level 1:

            >>> tree[-1][-1]._get_next_n_nodes_at_level(-3, 1)
            [Tree(items=[Tree(items=6)]), Tree(items=[Tree(items=4), Tree(items=5)]), Tree(items=[Tree(items=2), Tree(items=3)])]

            Gets previous node at level 0:

            >>> tree[-1][-1]._get_next_n_nodes_at_level(-1, 0)
            [Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)]), Tree(items=[Tree(items=4), Tree(items=5)]), Tree(items=[Tree(items=6)])])]

            Gets previous 4 nodes at level -1:

            >>> tree[-1][-1]._get_next_n_nodes_at_level(-4, -1)
            [Tree(items=6), Tree(items=5), Tree(items=4), Tree(items=3)]

            Gets previous 3 nodes at level -2:

            >>> tree[-1][-1]._get_next_n_nodes_at_level(-3, -2)
            [Tree(items=[Tree(items=6)]), Tree(items=[Tree(items=4), Tree(items=5)]), Tree(items=[Tree(items=2), Tree(items=3)])]

        ..  container:: example

            Tree of length greater than ``1`` for examples with positive ``n``:

            >>> items = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = baca.Tree(items=items)

            Gets next 4 nodes at level 2:

            >>> for node in tree[0][0]._get_next_n_nodes_at_level(
            ...     4, 2,
            ...     nodes_must_be_complete=True,
            ...     ):
            ...     node
            ...
            Tree(items=1)
            Tree(items=2)
            Tree(items=3)
            Tree(items=4)

            Gets next 3 nodes at level 1:

            >>> for node in tree[0][0]._get_next_n_nodes_at_level(
            ...     3, 1,
            ...     nodes_must_be_complete=True,
            ...     ):
            ...     node
            Tree(items=[Tree(items=1)])
            Tree(items=[Tree(items=2), Tree(items=3)])
            Tree(items=[Tree(items=4), Tree(items=5)])
            Tree(items=[Tree(items=6), Tree(items=7)])

            Gets next 4 nodes at level -1:

            >>> for node in tree[0][0]._get_next_n_nodes_at_level(4, -1):
            ...     node
            Tree(items=1)
            Tree(items=2)
            Tree(items=3)
            Tree(items=4)

            Gets next 3 nodes at level -2:

            >>> for node in tree[0][0]._get_next_n_nodes_at_level(
            ...     3, -2,
            ...     nodes_must_be_complete=True,
            ...     ):
            ...     node
            Tree(items=[Tree(items=1)])
            Tree(items=[Tree(items=2), Tree(items=3)])
            Tree(items=[Tree(items=4), Tree(items=5)])
            Tree(items=[Tree(items=6), Tree(items=7)])

        ..  container:: example

            Tree of length greater than ``1`` for examples with negative ``n``:

            >>> items = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = baca.Tree(items=items)

            Gets previous 4 nodes at level 2:

            >>> for node in tree[-1][-1]._get_next_n_nodes_at_level(
            ...     -4, 2,
            ...     nodes_must_be_complete=True,
            ...     ):
            ...     node
            Tree(items=6)
            Tree(items=5)
            Tree(items=4)
            Tree(items=3)

            Gets previous 3 nodes at level 1:

            >>> for node in tree[-1][-1]._get_next_n_nodes_at_level(
            ...     -3, 1,
            ...     nodes_must_be_complete=True,
            ...     ):
            ...     node
            Tree(items=[Tree(items=6)])
            Tree(items=[Tree(items=4), Tree(items=5)])
            Tree(items=[Tree(items=2), Tree(items=3)])
            Tree(items=[Tree(items=0), Tree(items=1)])

            Gets previous 4 nodes at level -1:

            >>> for node in tree[-1][-1]._get_next_n_nodes_at_level(
            ...     -4, -1,
            ...     nodes_must_be_complete=True,
            ...     ):
            ...     node
            Tree(items=6)
            Tree(items=5)
            Tree(items=4)
            Tree(items=3)

            Gets previous 3 nodes at level -2:

            >>> for node in tree[-1][-1]._get_next_n_nodes_at_level(
            ...     -3, -2,
            ...     nodes_must_be_complete=True,
            ...     ):
            ...     node
            Tree(items=[Tree(items=6)])
            Tree(items=[Tree(items=4), Tree(items=5)])
            Tree(items=[Tree(items=2), Tree(items=3)])
            Tree(items=[Tree(items=0), Tree(items=1)])

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
            Tree(items=[Tree(items=4), Tree(items=5)])
            Tree(items=[Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])]), Tree(items=[Tree(items=4), Tree(items=5)])])

            Gets parentage without self:

            >>> items = [[[0, 1], [2, 3]], [4, 5]]
            >>> tree = baca.Tree(items=items)
            >>> for tree in tree[1]._get_parentage()[1:]:
            ...     tree
            Tree(items=[Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])]), Tree(items=[Tree(items=4), Tree(items=5)])])

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
        Gets position of ``descendent`` relative to node rather than relative
        to root.

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
            equivalence_markup = getattr(item, "_equivalence_markup", None)
            child = type(self)(items=item, item_class=self.item_class)
            child._expression = expression
            child._equivalence_markup = equivalence_markup
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
            ...
            Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)]), Tree(items=[Tree(items=4), Tree(items=5)]), Tree(items=[Tree(items=6), Tree(items=7)])])
            Tree(items=[Tree(items=0), Tree(items=1)])
            Tree(items=0)
            Tree(items=1)
            Tree(items=[Tree(items=2), Tree(items=3)])
            Tree(items=2)
            Tree(items=3)
            Tree(items=[Tree(items=4), Tree(items=5)])
            Tree(items=4)
            Tree(items=5)
            Tree(items=[Tree(items=6), Tree(items=7)])
            Tree(items=6)
            Tree(items=7)

        ..  container::

            Iterates tree depth-first from right to left:

            >>> for node in tree._iterate_depth_first(reverse=True): node
            ...
            Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)]), Tree(items=[Tree(items=4), Tree(items=5)]), Tree(items=[Tree(items=6), Tree(items=7)])])
            Tree(items=[Tree(items=6), Tree(items=7)])
            Tree(items=7)
            Tree(items=6)
            Tree(items=[Tree(items=4), Tree(items=5)])
            Tree(items=5)
            Tree(items=4)
            Tree(items=[Tree(items=2), Tree(items=3)])
            Tree(items=3)
            Tree(items=2)
            Tree(items=[Tree(items=0), Tree(items=1)])
            Tree(items=1)
            Tree(items=0)

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
            Tree(items=1, item_class=int)
            Tree(items=2, item_class=int)
            Tree(items=8, item_class=int)
            Tree(items=9, item_class=int)

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
            Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])])
            Tree(items=[Tree(items=4), Tree(items=5)])

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
            Tree(items=[Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])]), Tree(items=[Tree(items=4), Tree(items=5)])])
            Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])])
            Tree(items=[Tree(items=0), Tree(items=1)])
            Tree(items=0)
            Tree(items=1)
            Tree(items=[Tree(items=2), Tree(items=3)])
            Tree(items=2)
            Tree(items=3)
            Tree(items=[Tree(items=4), Tree(items=5)])
            Tree(items=4)
            Tree(items=5)

            Iterates all levels in reverse:

            >>> for node in tree.iterate(reverse=True):
            ...     node
            Tree(items=[Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])]), Tree(items=[Tree(items=4), Tree(items=5)])])
            Tree(items=[Tree(items=4), Tree(items=5)])
            Tree(items=5)
            Tree(items=4)
            Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])])
            Tree(items=[Tree(items=2), Tree(items=3)])
            Tree(items=3)
            Tree(items=2)
            Tree(items=[Tree(items=0), Tree(items=1)])
            Tree(items=1)
            Tree(items=0)

            Iterates select levels:

            >>> for node in tree.iterate(level=0):
            ...     node
            Tree(items=[Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])]), Tree(items=[Tree(items=4), Tree(items=5)])])

            >>> for node in tree.iterate(level=1):
            ...     node
            Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])])
            Tree(items=[Tree(items=4), Tree(items=5)])

            >>> for node in tree.iterate(level=2):
            ...     node
            Tree(items=[Tree(items=0), Tree(items=1)])
            Tree(items=[Tree(items=2), Tree(items=3)])
            Tree(items=4)
            Tree(items=5)

            >>> for node in tree.iterate(level=3):
            ...     node
            Tree(items=0)
            Tree(items=1)
            Tree(items=2)
            Tree(items=3)

            >>> for node in tree.iterate(level=-4):
            ...     node
            Tree(items=[Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])]), Tree(items=[Tree(items=4), Tree(items=5)])])

            >>> for node in tree.iterate(level=-3):
            ...     node
            Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])])

            >>> for node in tree.iterate(level=-2):
            ...     node
            Tree(items=[Tree(items=0), Tree(items=1)])
            Tree(items=[Tree(items=2), Tree(items=3)])
            Tree(items=[Tree(items=4), Tree(items=5)])

            >>> for node in tree.iterate(level=-1):
            ...     node
            Tree(items=0)
            Tree(items=1)
            Tree(items=2)
            Tree(items=3)
            Tree(items=4)
            Tree(items=5)

            Iterates select levels in reverse:

            >>> for node in tree.iterate(level=0, reverse=True):
            ...     node
            Tree(items=[Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])]), Tree(items=[Tree(items=4), Tree(items=5)])])

            >>> for node in tree.iterate(level=1, reverse=True):
            ...     node
            Tree(items=[Tree(items=4), Tree(items=5)])
            Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])])

            >>> for node in tree.iterate(level=2, reverse=True):
            ...     node
            Tree(items=5)
            Tree(items=4)
            Tree(items=[Tree(items=2), Tree(items=3)])
            Tree(items=[Tree(items=0), Tree(items=1)])

            >>> for node in tree.iterate(level=3, reverse=True):
            ...     node
            Tree(items=3)
            Tree(items=2)
            Tree(items=1)
            Tree(items=0)

            >>> for node in tree.iterate(level=-4, reverse=True):
            ...     node
            Tree(items=[Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])]), Tree(items=[Tree(items=4), Tree(items=5)])])

            >>> for node in tree.iterate(level=-3, reverse=True):
            ...     node
            Tree(items=[Tree(items=[Tree(items=0), Tree(items=1)]), Tree(items=[Tree(items=2), Tree(items=3)])])

            >>> for node in tree.iterate(level=-2, reverse=True):
            ...     node
            Tree(items=[Tree(items=4), Tree(items=5)])
            Tree(items=[Tree(items=2), Tree(items=3)])
            Tree(items=[Tree(items=0), Tree(items=1)])

            >>> for node in tree.iterate(level=-1, reverse=True):
            ...     node
            Tree(items=5)
            Tree(items=4)
            Tree(items=3)
            Tree(items=2)
            Tree(items=1)
            Tree(items=0)

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


### FUNCTIONS ####


def select(items=None):
    if items is not None:
        return Selection(items=items)
    expression = Expression(proxy_class=Selection)
    callback = Expression._make_initializer_callback(
        Selection, callback_class=Expression, module_names=["baca"]
    )
    expression = expression.append_callback(callback)
    return abjad.new(expression, template="baca")
