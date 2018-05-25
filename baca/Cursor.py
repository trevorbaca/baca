import abjad
import collections


class Cursor(abjad.AbjadObject):
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

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_cyclic',
        '_lone_items',
        '_position',
        '_singletons',
        '_source',
        '_suppress_exception',
        )

    _publish_storage_format = True

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
        assert isinstance(source, collections.Iterable), repr(source)
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
        superclass = super(Cursor, self)
        return superclass.__eq__(argument)

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
        return super(Cursor, self).__hash__()

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
        Makes cursor from `pitch_class_segments`.

        ..  container:: example

            Makes cursor from pitch-class segments:

            >>> number_lists = [[13, 13.5, 11], [-2, 2, 1.5]]
            >>> cursor = baca.Cursor.from_pitch_class_segments(
            ...     number_lists,
            ...     )

            >>> abjad.f(cursor, strict=89)
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

        Coerces numeric `pitch_class_segments`.

        Returns cursor.
        """
        cells = []
        for pitch_class_segment in pitch_class_segments:
                pitch_class_segment = abjad.PitchClassSegment(
                    items=pitch_class_segment,
                    )
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

        ..  container:: example

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
                        raise Exception(f'cursor only {len(self.source)}.')
                self._position += 1
        elif count < 0:
            for i in range(abs(count)):
                self._position -= 1
                try:
                    element = self.source[self.position]
                    result.append(element)
                except IndexError:
                    if not self.suppress_exception:
                        raise Exception(f'cursor only {len(self.source)}.')
        if self.singletons:
            if len(result) == 0:
                result = None
            elif len(result) == 1:
                result = result[0]
        if exhausted and not self.is_exhausted:
            raise Exception(f'cusor not exhausted: {self!r}.')
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
