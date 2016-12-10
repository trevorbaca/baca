# -*- coding: utf-8 -*-
import abjad
import collections


class Cursor(abjad.abctools.AbjadObject):
    r'''Cursor.

    ::

        >>> import baca

    ..  container:: example

        Gets elements one at a time:

        ::

            >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
            >>> source = datastructuretools.CyclicTuple(source)
            >>> cursor = baca.tools.Cursor(source=source)

        ::

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

        ::

            >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
            >>> source = datastructuretools.CyclicTuple(source)
            >>> cursor = baca.tools.Cursor(source=source)

        ::

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

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        '_lone_items',
        '_position',
        '_singletons',
        '_source',
        '_suppress_exception',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        source=None,
        position=None,
        singletons=None,
        suppress_exception=None,
        ):
        source = source or ()
        assert isinstance(source, collections.Iterable), repr(source)
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

    def __eq__(self, expr):
        r'''Is true when `expr` is a cursor with keyword
        arguments equal to this cursor. Otherwise false.

        Returns true or false.
        '''
        superclass = super(Cursor, self)
        return superclass.__eq__(expr)

    def __hash__(self):
        r'''Hashes cursor.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(Cursor, self).__hash__()

    def __iter__(self, count=1):
        r'''Iterates cursor.

        ..  container:: example

            Iterates acyclic cursor:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> cursor = baca.tools.Cursor(source=source)
                >>> for item in cursor:
                ...     item
                13
                'da capo'
                Note("cs'8.")
                'rit.'

        ..  container:: example

            Iterates cyclic cursor:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = baca.tools.Cursor(source=source)
                >>> for item in cursor:
                ...     item
                13
                'da capo'
                Note("cs'8.")
                'rit.'

        Returns generator.
        '''
        return iter(self.source)

    def __len__(self):
        r'''Gets length of cursor.

        ..  container:: example

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> cursor = baca.tools.Cursor(source=source)
                >>> len(cursor)
                4

        Defined equal to length of cursor source.

        Returns nonnegative integer.
        '''
        return len(self.source)

    ### PUBLIC PROPERTIES ###

    @property
    def is_exhausted(self):
        r'''Is true when cursor is exhausted.

        ..  container:: example

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> cursor = baca.tools.Cursor(source=source)
                >>> cursor.is_exhausted
                False

            ::

                >>> cursor.next(), cursor.is_exhausted
                ([13], False)

            ::

                >>> cursor.next(), cursor.is_exhausted
                (['da capo'], False)

            ::

                >>> cursor.next(), cursor.is_exhausted
                ([Note("cs'8.")], False)

            ::

                >>> cursor.next(), cursor.is_exhausted
                (['rit.'], True)

        Returns true or false.
        '''
        if self.position is None:
            return False
        try:
            self.source[self.position]
        except IndexError:
            return True
        return False

    @property
    def position(self):
        r'''Gets position.

        ..  container:: example

            Position starting at none:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = baca.tools.Cursor(source=source)

            ::

                >>> cursor.position is None
                True

            ::

                >>> cursor.next()
                [13]
                >>> cursor.next()
                ['da capo']
                >>> cursor.next()
                [Note("cs'8.")]
                >>> cursor.next()
                ['rit.']

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = baca.tools.Cursor(
                ...     source=source,
                ...     position=None,
                ...     )

            ::

                >>> cursor.position is None
                True

            ::

                >>> cursor.next(count=-1)
                ['rit.']
                >>> cursor.next(count=-1)
                [Note("cs'8.")]
                >>> cursor.next(count=-1)
                ['da capo']
                >>> cursor.next(count=-1)
                [13]

            This is default behavior.

        ..  container:: example

            Position starting at 0:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = baca.tools.Cursor(
                ...     source=source,
                ...     position=0,
                ...     )

            ::

                >>> cursor.position
                0

            ::

                >>> cursor.next()
                [13]
                >>> cursor.next()
                ['da capo']
                >>> cursor.next()
                [Note("cs'8.")]
                >>> cursor.next()
                ['rit.']

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = baca.tools.Cursor(
                ...     source=source,
                ...     position=0,
                ...     )

            ::

                >>> cursor.position
                0

            ::

                >>> cursor.next(count=-1)
                ['rit.']
                >>> cursor.next(count=-1)
                [Note("cs'8.")]
                >>> cursor.next(count=-1)
                ['da capo']
                >>> cursor.next(count=-1)
                [13]

            This is default behavior.

        ..  container:: example

            Position starting at -1:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = baca.tools.Cursor(
                ...     source=source,
                ...     position=-1,
                ...     )

            ::

                >>> cursor.position
                -1

            ::

                >>> cursor.next()
                ['rit.']
                >>> cursor.next()
                [13]
                >>> cursor.next()
                ['da capo']
                >>> cursor.next()
                [Note("cs'8.")]

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = baca.tools.Cursor(
                ...     source=source,
                ...     position=-1,
                ...     )

            ::

                >>> cursor.position
                -1

            ::

                >>> cursor.next(count=-1)
                [Note("cs'8.")]
                >>> cursor.next(count=-1)
                ['da capo']
                >>> cursor.next(count=-1)
                [13]
                >>> cursor.next(count=-1)
                ['rit.']

        Returns tuple.
        '''
        return self._position

    @property
    def singletons(self):
        r'''Is true when cursor returns singletons not enclosed within a list.
        If false when cursor returns singletons enclosed within a list.

        ..  container:: example

            Returns singletons enclosed within a list:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> cursor = baca.tools.Cursor(
                ...     source=source,
                ...     suppress_exception=True,
                ...     )

            ::

                >>> cursor.next()
                [13]

            ::

                >>> cursor.next()
                ['da capo']

            ::

                >>> cursor.next()
                [Note("cs'8.")]

            ::

                >>> cursor.next()
                ['rit.']

            ::

                >>> cursor.next()
                []

            ::

                >>> cursor.next()
                []

        ..  container:: example

            Returns singletons free of enclosing list:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> cursor = baca.tools.Cursor(
                ...     source=source,
                ...     singletons=True,
                ...     suppress_exception=True,
                ...     )

            ::

                >>> cursor.next()
                13

            ::

                >>> cursor.next()
                'da capo'

            ::

                >>> cursor.next()
                Note("cs'8.")

            ::

                >>> cursor.next()
                'rit.'

            ::

                >>> cursor.next() is None
                True

            ::

                >>> cursor.next() is None
                True

        '''
        return self._singletons

    @property
    def source(self):
        r'''Gets source.

        ..  container:: example

            List source:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> cursor = baca.tools.Cursor(source=source)

            ::

                >>> cursor.source
                [13, 'da capo', Note("cs'8."), 'rit.']

        ..  container:: example

            Cyclic tuple source:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = baca.tools.Cursor(source=source)

            ::

                >>> cursor.source
                CyclicTuple([13, 'da capo', Note("cs'8."), 'rit.'])

        Returns source.
        '''
        return self._source

    @property
    def suppress_exception(self):
        r'''Is true when cursor returns none on exhaustion.
        Is false when cursor raises exception on exhaustion.

        ..  container:: example

            Exhausted cursor raises exception:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> cursor = baca.tools.Cursor(source=source)
                >>> cursor.is_exhausted
                False

            ::

                >>> cursor.next()
                [13]

            ::

                >>> cursor.next()
                ['da capo']

            ::

                >>> cursor.next()
                [Note("cs'8.")]

            ::

                >>> cursor.next()
                ['rit.']

            ::

                >>> cursor.next()
                Traceback (most recent call last):
                ...
                Exception: cursor length only 4.

            ::

                >>> cursor.next()
                Traceback (most recent call last):
                ...
                Exception: cursor length only 4.

        ..  container:: example

            Exhausted cursor returns none:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> cursor = baca.tools.Cursor(
                ...     source=source,
                ...     suppress_exception=True,
                ...     )
                >>> cursor.is_exhausted
                False

            ::

                >>> cursor.next()
                [13]

            ::

                >>> cursor.next()
                ['da capo']

            ::

                >>> cursor.next()
                [Note("cs'8.")]

            ::

                >>> cursor.next()
                ['rit.']

            ::

                >>> cursor.next()
                []

            ::

                >>> cursor.next()
                []

        '''
        return self._suppress_exception

    ### PUBLIC METHODS ###

    @staticmethod
    def from_pitch_class_segments(pitch_class_segments):
        r'''Makes cursor from `pitch_class_segments`.

        ..  container:: example

            Makes cursor from pitch-class segments:

            ::

                >>> number_lists = [[13, 13.5, 11], [-2, 2, 1.5]]
                >>> baca.tools.Cursor.from_pitch_class_segments(
                ...     number_lists,
                ...     )
                Cursor(source=CyclicTuple([PitchClassSegment([1, 1.5, 11]), PitchClassSegment([10, 2, 1.5])]))

        Coerces numeric `pitch_class_segments`.

        Returns cursor.
        '''
        cells = []
        for pitch_class_segment in pitch_class_segments:
                pitch_class_segment = abjad.pitchtools.PitchClassSegment(
                    pitch_class_segment,
                    )
                cells.append(pitch_class_segment)
        cells = abjad.datastructuretools.CyclicTuple(cells)
        cursor = Cursor(source=cells)
        return cursor

    def next(self, count=1):
        r'''Gets next `count` elements in source.

        ..  container:: example

            Gets elements one at a time:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = baca.tools.Cursor(source=source)

            ::

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

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = baca.tools.Cursor(source=source)

            ::

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

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = baca.tools.Cursor(source=source)

            ::

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

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = baca.tools.Cursor(source=source)

            ::

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

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = baca.tools.Cursor(source=source)

            ::

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

        ..  container:: example

            Raises exception when cursor is exhausted:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> cursor = baca.tools.Cursor(source=source)

            ::

                >>> cursor.next(count=99)
                Traceback (most recent call last):
                ...
                Exception: cursor length only 4.

        Returns tuple.
        '''
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
                        message = 'cursor length only {}.'
                        message = message.format(len(self.source))
                        raise Exception(message)
                self._position += 1
        elif count < 0:
            for i in range(abs(count)):
                self._position -= 1
                try:
                    element = self.source[self.position]
                    result.append(element)
                except IndexError:
                    if not self.suppress_exception:
                        message = 'cursor length only {}.'
                        message = message.format(len(self.source))
                        raise Exception(message)
        if self.singletons:
            if len(result) == 0:
                result = None
            elif len(result) == 1:
                result = result[0]
        return result
