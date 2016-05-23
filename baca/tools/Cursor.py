# -*- coding: utf-8 -*-
import abjad
import collections


class Cursor(abjad.abctools.AbjadObject):
    r'''Cursor.

    ::

        >>> import baca

    ..  container:: example

        **Example 1.** Gets elements one at a time:

        ::

            >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
            >>> source = datastructuretools.CyclicTuple(source)
            >>> cursor = baca.tools.Cursor(source=source)

        ::

                >>> cursor.next()
                (13,)
                >>> cursor.next()
                ('da capo',)
                >>> cursor.next()
                (Note("cs'8."),)
                >>> cursor.next()
                ('rit.',)
                >>> cursor.next()
                (13,)
                >>> cursor.next()
                ('da capo',)

    ..  container:: example

        **Example 2.** Gets different numbers of elements at a time:

        ::

            >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
            >>> source = datastructuretools.CyclicTuple(source)
            >>> cursor = baca.tools.Cursor(source=source)

        ::

            >>> cursor.next(count=2)
            (13, 'da capo')
            >>> cursor.next(count=-1)
            ('da capo',)
            >>> cursor.next(count=2)
            ('da capo', Note("cs'8."))
            >>> cursor.next(count=-1)
            (Note("cs'8."),)
            >>> cursor.next(count=2)
            (Note("cs'8."), 'rit.')
            >>> cursor.next(count=-1)
            ('rit.',)

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        '_position',
        '_source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        source=None,
        position=None,
        ):
        source = source or ()
        assert isinstance(source, collections.Iterable), repr(source)
        self._source = source
        assert isinstance(position, (int, type(None))), repr(position)
        self._position = position

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a cursor with keyword
        arguments equal to this cursor. Otherwise false.

        Returns true or false.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.compare(self, expr)

    def __hash__(self):
        r'''Hashes cursor.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(Cursor, self).__hash__()

    def __iter__(self, count=1):
        r'''Iterates cursor.

        ..  container:: example

            **Example.** Iterates acyclic cursor:

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

            **Example.** Iterates cyclic cursor:

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

    ### PUBLIC PROPERTIES ###

    @property
    def is_exhausted(self):
        r'''Is true when cursor is exhausted.

        ..  container:: example

            **Example.**

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> cursor = baca.tools.Cursor(source=source)
                >>> cursor.is_exhausted
                False

            ::

                >>> cursor.next(), cursor.is_exhausted
                ((13,), False)

            ::

                >>> cursor.next(), cursor.is_exhausted
                (('da capo',), False)

            ::

                >>> cursor.next(), cursor.is_exhausted
                ((Note("cs'8."),), False)

            ::

                >>> cursor.next(), cursor.is_exhausted
                (('rit.',), True)

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

            **Example 1.** Position starting at none:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = baca.tools.Cursor(source=source)

            ::

                >>> cursor.position is None
                True

            ::

                >>> cursor.next()
                (13,)
                >>> cursor.next()
                ('da capo',)
                >>> cursor.next()
                (Note("cs'8."),)
                >>> cursor.next()
                ('rit.',)

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
                ('rit.',)
                >>> cursor.next(count=-1)
                (Note("cs'8."),)
                >>> cursor.next(count=-1)
                ('da capo',)
                >>> cursor.next(count=-1)
                (13,)

            This is default behavior.

        ..  container:: example

            **Example 1.** Position starting at 0:

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
                (13,)
                >>> cursor.next()
                ('da capo',)
                >>> cursor.next()
                (Note("cs'8."),)
                >>> cursor.next()
                ('rit.',)

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
                ('rit.',)
                >>> cursor.next(count=-1)
                (Note("cs'8."),)
                >>> cursor.next(count=-1)
                ('da capo',)
                >>> cursor.next(count=-1)
                (13,)

            This is default behavior.

        ..  container:: example

            **Example 3.** Position starting at -1:

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
                ('rit.',)
                >>> cursor.next()
                (13,)
                >>> cursor.next()
                ('da capo',)
                >>> cursor.next()
                (Note("cs'8."),)

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
                (Note("cs'8."),)
                >>> cursor.next(count=-1)
                ('da capo',)
                >>> cursor.next(count=-1)
                (13,)
                >>> cursor.next(count=-1)
                ('rit.',)

        Returns tuple.
        '''
        return self._position

    @property
    def source(self):
        r'''Gets source.

        ..  container:: example

            **Example 1.** List source:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> cursor = baca.tools.Cursor(source=source)

            ::

                >>> cursor.source
                [13, 'da capo', Note("cs'8."), 'rit.']

        ..  container:: example

            **Example 2.** Cyclic tuple source:

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

    ### PUBLIC METHODS ###

    def next(self, count=1):
        r'''Gets next `count` elements in source.

        ..  container:: example

            **Example 1.** Gets elements one at a time:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = baca.tools.Cursor(source=source)

            ::

                >>> cursor.next()
                (13,)
                >>> cursor.next()
                ('da capo',)
                >>> cursor.next()
                (Note("cs'8."),)
                >>> cursor.next()
                ('rit.',)
                >>> cursor.next()
                (13,)
                >>> cursor.next()
                ('da capo',)

        ..  container:: example

            **Example 2.** Gets elements one at a time in reverse:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = baca.tools.Cursor(source=source)

            ::

                >>> cursor.next(count=-1)
                ('rit.',)
                >>> cursor.next(count=-1)
                (Note("cs'8."),)
                >>> cursor.next(count=-1)
                ('da capo',)
                >>> cursor.next(count=-1)
                (13,)

        ..  container:: example

            **Example 3.** Gets same two elements forward and back:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = baca.tools.Cursor(source=source)

            ::

                >>> cursor.next(count=2)
                (13, 'da capo')
                >>> cursor.next(count=-2)
                ('da capo', 13)
                >>> cursor.next(count=2)
                (13, 'da capo')
                >>> cursor.next(count=-2)
                ('da capo', 13)

        ..  container:: example

            **Example 4.** Gets different numbers of elements at a time:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = baca.tools.Cursor(source=source)

            ::

                >>> cursor.next(count=2)
                (13, 'da capo')
                >>> cursor.next(count=-1)
                ('da capo',)
                >>> cursor.next(count=2)
                ('da capo', Note("cs'8."))
                >>> cursor.next(count=-1)
                (Note("cs'8."),)
                >>> cursor.next(count=2)
                (Note("cs'8."), 'rit.')
                >>> cursor.next(count=-1)
                ('rit.',)

        ..  container:: example

            **Example 5.** Gets different numbers of elements at a time:

            ::

                >>> source = [13, 'da capo', Note("cs'8."), 'rit.']
                >>> source = datastructuretools.CyclicTuple(source)
                >>> cursor = baca.tools.Cursor(source=source)

            ::

                >>> cursor.next(count=2)
                (13, 'da capo')
                >>> cursor.next(count=-3)
                ('da capo', 13, 'rit.')
                >>> cursor.next(count=2)
                ('rit.', 13)
                >>> cursor.next(count=-3)
                (13, 'rit.', Note("cs'8."))
                >>> cursor.next(count=2)
                (Note("cs'8."), 'rit.')
                >>> cursor.next(count=-3)
                ('rit.', Note("cs'8."), 'da capo')

        ..  container:: example

            **Example 6.** Raises exception when cursor is exhausted:

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
                except IndexError:
                    message = 'cursor length only {}.'
                    message = message.format(len(self.source))
                    raise Exception(message)
                result.append(element)
                self._position += 1
        elif count < 0:
            for i in range(abs(count)):
                self._position -= 1
                try:
                    element = self.source[self.position]
                except IndexError:
                    message = 'cursor length only {}.'
                    message = message.format(len(self.source))
                    raise Exception(message)
                result.append(element)
        result = tuple(result)
        return result