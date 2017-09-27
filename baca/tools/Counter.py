import abjad


class Counter(abjad.AbjadObject):
    r'''Counter.

    ::

        >>> import baca

    ..  container:: example

        Initializes to zero and increments by 1:

            >>> counter = baca.Counter(start=0)
            >>> counter.start, counter.current
            (0, 0)

        ::

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

        ::

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

        ::

            >>> counter(3), counter.current
            (3, 13)
            >>> counter(-6), counter.current
            (-6, 7)
            >>> counter(5.5), counter.current
            (5.5, 12.5)
            >>> counter(-2), counter.current
            (-2, 10.5)

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        '_current',
        '_start',
        )

    ### INITIALIZER ###

    def __init__(self, start=0):
        self._start = start
        self._current = start

    ### SPECIAL METHODS ###

    def __call__(self, count=1):
        r'''Calls counter.

        Returns new value.
        '''
        current = self.current + count
        self._current = current
        return count

    ### PUBLIC PROPERTIES ###

    @property
    def current(self):
        r'''Gets current value.

        Returns integer.
        '''
        return self._current

    @property
    def start(self):
        r'''Gets start value.

        Set to integer.

        Returns integer.
        '''
        return self._start
