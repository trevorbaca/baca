# -*- coding: utf-8 -*-
import abjad
import baca
import collections as collections_module


class CollectionList(abjad.AbjadValueObject):
    r'''Collection list.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Initializes numbered pitch segments:

        ::

            >>> for collection in baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     ]):
            ...     collection
            ...
            PitchSegment([12, 14, 18, 17])
            PitchSegment([16, 20, 19])

    ..  container:: example

        Initializes named pitch segments:

        ::

            >>> for collection in baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     ],
            ...     item_class=abjad.NamedPitch,
            ...     ):
            ...     collection
            ...
            PitchSegment("c'' d'' fs'' f''")
            PitchSegment("e'' af'' g''")

    ..  container:: example

        Initializes numbered pitch-class segments:

        ::

            >>> for collection in baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     ],
            ...     item_class=abjad.NumberedPitchClass,
            ...     ):
            ...     collection
            ...
            PitchClassSegment([0, 2, 6, 5])
            PitchClassSegment([4, 8, 7])

    ..  container:: example

        Initializes named pitch-class segments:

        ::

            >>> for collection in baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     ],
            ...     item_class=abjad.NamedPitchClass,
            ...     ):
            ...     collection
            ...
            PitchClassSegment("c d fs f")
            PitchClassSegment("e af g")

    ..  container:: example

        Initializes mixed numbered and named pitch segments:

        ::

            >>> for collection in baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     "ff'' gs'' g''",
            ...     ]):
            ...     collection
            ...
            PitchSegment([12, 14, 18, 17])
            PitchSegment("ff'' gs'' g''")

    ..  container:: example

        Initializes numbered pitch sets:

        ::

            >>> for collection in baca.CollectionList([
            ...     {12, 14, 18, 17},
            ...     {16, 20, 19},
            ...     ]):
            ...     collection
            ...
            PitchSet([12, 14, 17, 18])
            PitchSet([16, 19, 20])

    ..  container:: example

        Initializes named pitch sets:

        ::

            >>> for collection in baca.CollectionList([
            ...     {12, 14, 18, 17},
            ...     {16, 20, 19},
            ...     ],
            ...     item_class=abjad.NamedPitch,
            ...     ):
            ...     collection
            ...
            PitchSet(["c''", "d''", "f''", "fs''"])
            PitchSet(["e''", "g''", "af''"])

    ..  container:: example

        Initializes numbered pitch-class sets:

        ::

            >>> for collection in baca.CollectionList([
            ...     {12, 14, 18, 17},
            ...     {16, 20, 19},
            ...     ],
            ...     item_class=abjad.NumberedPitchClass,
            ...     ):
            ...     collection
            ...
            PitchClassSet([0, 2, 5, 6])
            PitchClassSet([4, 7, 8])

    ..  container:: example

        Initializes named pitch-class sets:

        ::

            >>> for collection in baca.CollectionList([
            ...     {12, 14, 18, 17},
            ...     {16, 20, 19},
            ...     ],
            ...     item_class=abjad.NamedPitchClass,
            ...     ):
            ...     collection
            ...
            PitchClassSet(['c', 'd', 'f', 'fs'])
            PitchClassSet(['e', 'g', 'af'])

    ..  container:: example

        Initializes mixed numbered and named pitch segments:

        ::

            >>> for collection in baca.CollectionList([
            ...     [12, 14, 18, 17],
            ...     "ff'' gs'' g''",
            ...     ]):
            ...     collection
            ...
            PitchSegment([12, 14, 18, 17])
            PitchSegment("ff'' gs'' g''")

    ..  container:: example

        Initializes mixed segments and sets:

        ::

            >>> for collection in baca.CollectionList([
            ...     {12, 14, 18, 17},
            ...     [16, 20, 19],
            ...     ]):
            ...     collection
            ...
            PitchSet([12, 14, 17, 18])
            PitchSegment([16, 20, 19])

    ..  container:: example

        Initializes from collection list:

        ::

            >>> collections = baca.CollectionList([[12, 13, 14], [15, 16, 17]])
            >>> baca.CollectionList(collections)
            CollectionList([<12, 13, 14>, <15, 16, 17>])

    ..  container:: example

        Initializes from list of collection lists:

        ::

            >>> collection_list_1 = baca.CollectionList([[12, 13, 14]])
            >>> collection_list_2 = baca.CollectionList([[15, 16, 17]])
            >>> baca.CollectionList([collection_list_1, collection_list_2])
            CollectionList([<12, 13, 14>, <15, 16, 17>])

    ..  container:: example

        Initializes empty:

        ::

            >>> baca.CollectionList()
            CollectionList([])

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        '_collections',
        '_expression',
        '_item_class',
        )

    _item_class_prototype = (
        abjad.NumberedPitch,
        abjad.NumberedPitchClass,
        abjad.NamedPitch,
        abjad.NamedPitchClass,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        collections=None,
        item_class=None,
        ):
        self._expression = None
        if item_class is not None:
            if item_class not in self._item_class_prototype:
                message = 'must be pitch or pitch-class: {!r}.'
                message = message.format(item_class)
                raise TypeError(message)
        self._item_class = item_class
        collections = self._coerce(collections)
        collections = collections or []
        self._collections = tuple(collections)

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        r'''Adds `argument` to collections.

        ..  container:: example

                >>> collections_1 = baca.CollectionList([[12, 14, 18, 17]])
                >>> collections_2 = baca.CollectionList([[16, 20, 19]])
                >>> collections_1 + collections_2
                CollectionList([<12, 14, 18, 17>, <16, 20, 19>])

        Returns new collection list.
        '''
        if not isinstance(argument, collections_module.Iterable):
            message = 'must be collection list: {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        argument_collections = [
            self._initialize_collection(_) for _ in argument
            ]
        collections = self.collections + argument_collections
        return abjad.new(self, collections=collections)

    def __eq__(self, argument):
        r'''Is true when `argument` is a collection list with collections
        equal to those of this collection list. Otherwise false.

        ..  container:: example

            ::

                >>> collections_1 = baca.CollectionList([[12, 13, 14], [15, 16, 17]])
                >>> collections_2 = baca.CollectionList([[12, 13, 14], [15, 16, 17]])
                >>> collections_3 = baca.CollectionList([[12, 13, 14]])

            ::

                >>> collections_1 == collections_1
                True

            ::

                >>> collections_1 == collections_2
                True

            ::

                >>> collections_1 == collections_3
                False

            ::

                >>> collections_2 == collections_1
                True

            ::

                >>> collections_2 == collections_2
                True

            ::

                >>> collections_2 == collections_3
                False

            ::

                >>> collections_3 == collections_1
                False

            ::

                >>> collections_3 == collections_2
                False

            ::

                >>> collections_3 == collections_3
                True

        ..  container:: example

            Ignores item class:

            ::

                >>> collections_1 = baca.CollectionList(
                ...     collections=[[12, 13, 14], [15, 16, 17]],
                ...     item_class=None,
                ...     )
                >>> collections_2 = baca.CollectionList(
                ...     collections=[[12, 13, 14], [15, 16, 17]],
                ...     item_class=abjad.NumberedPitch,
                ...     )

            ::

                >>> collections_1.item_class == collections_2.item_class
                False

            ::

                >>> collections_1 == collections_2
                True

        Returns true or false.
        '''
        if not isinstance(argument, type(self)):
            return False
        return self.collections == argument.collections

    def __format__(self, format_specification=''):
        r'''Gets storage format of collections.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([
                ...     [12, 14, 18, 17],
                ...     [16, 20, 19],
                ...     ])

            ::

                >>> f(collections)
                baca.tools.CollectionList(
                    collections=[
                        baca.tools.PitchSegment(
                            (
                                abjad.NumberedPitch(12),
                                abjad.NumberedPitch(14),
                                abjad.NumberedPitch(18),
                                abjad.NumberedPitch(17),
                                ),
                            item_class=abjad.NumberedPitch,
                            ),
                        baca.tools.PitchSegment(
                            (
                                abjad.NumberedPitch(16),
                                abjad.NumberedPitch(20),
                                abjad.NumberedPitch(19),
                                ),
                            item_class=abjad.NumberedPitch,
                            ),
                        ],
                    )

        Returns string.
        '''
        superclass = super(CollectionList, self)
        return superclass.__format__()

    def __getitem__(self, argument):
        r'''Gets collection or collection slice identified by `argument`.

        ..  container:: example

            Gets collections:

            ::

                >>> collections = baca.CollectionList([
                ...     [12, 14, 18, 17],
                ...     [16, 20, 19],
                ...     ])

            ::

                >>> collections[0]
                PitchSegment([12, 14, 18, 17])

            ::

                >>> collections[-1]
                PitchSegment([16, 20, 19])

        ..  container:: example

            Gets collections lists:

            ::

                >>> collections = baca.CollectionList([
                ...     [12, 14, 18, 17],
                ...     [16, 20, 19],
                ...     ])

            ::

                >>> collections[:1]
                CollectionList([<12, 14, 18, 17>])

            ::

                >>> collections[-1:]
                CollectionList([<16, 20, 19>])

        Returns collection.
        '''
        collections = self.collections or []
        result = collections.__getitem__(argument)
        try:
            return abjad.new(self, collections=result)
        except TypeError:
            return result

    # TODO: reimplement to show all four types of collection
    def __illustrate__(self):
        r'''Illustrates collections.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([
                ...     [12, 14, 18, 17],
                ...     [16, 20, 19],
                ...     ])

            ::

                >>> show(collections) # doctest: +SKIP

            ..  docs::

                >>> lilypond_file = collections.__illustrate__()
                >>> f(lilypond_file[abjad.Score])
                \new Score \with {
                    \override BarLine.transparent = ##t
                    \override BarNumber.stencil = ##f
                    \override Beam.stencil = ##f
                    \override Flag.stencil = ##f
                    \override HorizontalBracket.staff-padding = #4
                    \override SpacingSpanner.strict-grace-spacing = ##t
                    \override SpacingSpanner.strict-note-spacing = ##t
                    \override SpacingSpanner.uniform-stretching = ##t
                    \override Stem.stencil = ##f
                    \override TextScript.X-extent = ##f
                    \override TextScript.staff-padding = #2
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 16)
                } <<
                    \new Staff {
                        \new Voice \with {
                            \consists Horizontal_bracket_engraver
                        } {
                            \time 1/8
                            c''8 \startGroup ^ \markup { 0 }
                            d''8
                            fs''8
                            f''8 \stopGroup
                            s8
                            e''8 \startGroup ^ \markup { 1 }
                            af''8
                            g''8 \stopGroup
                            s8
                            \bar "|."
                            \override Score.BarLine.transparent = ##f
                        }
                    }
                >>

        Returns LilyPond file.
        '''
        tree = baca.PitchTree(list(self))
        return tree.__illustrate__()

    def __len__(self):
        r'''Gets length of collections.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([
                ...     [12, 14, 18, 17],
                ...     [16, 20, 19],
                ...     ])

            ::

                >>> len(collections)
                2

        Returns nonnegative integer.
        '''
        return len(self.collections)

    def __repr__(self):
        r'''Gets interpreter representation of collections.

        ..  container:: example

            ::

                >>> baca.CollectionList([
                ...     [12, 14, 18, 17],
                ...     [16, 20, 19],
                ...     ])
                CollectionList([<12, 14, 18, 17>, <16, 20, 19>])

        Returns string.
        '''
        collections = self.collections or []
        collections = ', '.join([str(_) for _ in collections])
        string = '{}([{}])'
        string = string.format(type(self).__name__, collections)
        if self._expression:
            string = '*' + string
        return string

    ### PRIVATE METHODS ###

    def _coerce(self, collections):
        prototype = (
            baca.PitchSegment,
            baca.PitchSet,
            baca.PitchClassSegment,
            baca.PitchClassSet,
            )
        collections_ = []
        for item in collections or []:
            if isinstance(item, type(self)):
                for collection in item:
                    collection_ = self._initialize_collection(collection)
                    collections_.append(collection_)
            else:
                collection_ = self._initialize_collection(item)
                collections_.append(collection_)
        collections_ = [self._to_baca_collection(_) for _ in collections_]
        assert all(isinstance(_, prototype) for _ in collections_)
        return collections_

    def _get_pitch_class_class(self):
        item_class = self.item_class or abjad.NumberedPitch
        if item_class in (abjad.NumberedPitchClass, abjad.NamedPitchClass):
            return item_class
        elif item_class is abjad.NumberedPitch:
            return abjad.NumberedPitchClass
        elif item_class is abjad.NamedPitch:
            return abjad.NamedPitchClass
        else:
            message = 'must be pitch or pitch-class class: {!r}.'
            message = message.format(item_class)
            raise TypeError(message)

    def _initialize_collection(self, argument, prototype=None):
        items = argument
        item_class = self.item_class or abjad.NumberedPitch
        if prototype is not None:
            return abjad.new(prototype, items=items)
        elif isinstance(argument, abjad.Segment):
            return argument
        elif isinstance(argument, abjad.Set):
            return argument
        elif isinstance(argument, set):
            if item_class in (abjad.NumberedPitch, abjad.NamedPitch):
                return abjad.PitchSet(items=items, item_class=item_class)
            elif item_class in (
                abjad.NumberedPitchClass,
                abjad.NamedPitchClass,
                ):
                return baca.PitchClassSet(
                    items=items,
                    item_class=item_class,
                    )
            else:
                raise TypeError(item_class)
        elif self.item_class is not None:
            if item_class in (abjad.NumberedPitch, abjad.NamedPitch):
                return baca.PitchSegment(items=items, item_class=item_class)
            elif item_class in (
                abjad.NumberedPitchClass,
                abjad.NamedPitchClass,
                ):
                return baca.PitchClassSegment(
                    items=items,
                    item_class=item_class,
                    )
            else:
                raise TypeError(item_class)
        else:
            if isinstance(argument, str):
                return baca.PitchSegment(
                    items=items,
                    item_class=abjad.NamedPitch,
                    )
            elif isinstance(argument, collections_module.Iterable):
                return baca.PitchSegment(
                    items=items,
                    item_class=abjad.NumberedPitch,
                    )
            else:
                message = 'must be string or other iterable: {!r}.'
                message = message.format(argument)
                raise TypeError(message)

    @staticmethod
    def _to_baca_collection(collection):
        abjad_prototype = (
            abjad.PitchClassSegment,
            abjad.PitchClassSet,
            abjad.PitchSegment,
            abjad.PitchSet,
            )
        assert isinstance(collection, abjad_prototype), repr(collection)
        baca_prototype = (
            baca.PitchClassSegment,
            baca.PitchClassSet,
            baca.PitchSegment,
            baca.PitchSet,
            )
        if isinstance(collection, baca_prototype):
            pass
        elif isinstance(collection, abjad.PitchClassSegment):
            collection = baca.PitchClassSegment(
                items=collection,
                item_class=collection.item_class,
                )
        elif isinstance(collection, abjad.PitchClassSet):
            collection = baca.PitchClassSet(
                items=collection,
                item_class=collection.item_class,
                )
        elif isinstance(collection, abjad.PitchSegment):
            collection = baca.PitchSegment(
                items=collection,
                item_class=collection.item_class,
                )
        elif isinstance(collection, abjad.PitchSet):
            collection = baca.PitchSet(
                items=collection,
                item_class=collection.item_class,
                )
        elif isinstance(collection, abjad.PitchSet):
            collection = baca.PitchSet(
                items=collection,
                item_class=collection.item_class,
                )
        else:
            raise TypeError(collection)
        assert isinstance(collection, baca_prototype)
        return collection

    @staticmethod
    def _to_pitch_class_item_class(item_class):
        item_class = item_class or abjad.NumberedPitch
        if item_class in (abjad.NamedPitchClass, abjad.NumberedPitchClass):
            return item_class
        elif item_class is abjad.NamedPitch:
            return abjad.NamedPitchClass
        elif item_class is abjad.NumberedPitch:
            return abjad.NumberedPitchClass
        else:
            raise TypeError(item_class)

    @staticmethod
    def _to_pitch_item_class(item_class):
        item_class = item_class or abjad.NumberedPitch
        if item_class in (abjad.NamedPitch, abjad.NumberedPitch):
            return item_class
        elif item_class is abjad.NamedPitchClass:
            return abjad.NamedPitch
        elif item_class is abjad.NumberedPitchClass:
            return abjad.NumberedPitch
        else:
            raise TypeError(item_class)

    ### PUBLIC PROPERTIES ###

    @property
    def collections(self):
        r'''Gets collections in list.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([
                ...     [12, 14, 18, 17],
                ...     [16, 20, 19],
                ...     ])

            ::

                >>> collections.collections
                [PitchSegment([12, 14, 18, 17]), PitchSegment([16, 20, 19])]

        Returns list.
        '''
        if self._collections:
            return list(self._collections)

    @property
    def item_class(self):
        r'''Gets item class of collections in list.

        Set to class modeling pitch or pitch-class.

        Returns class or none.
        '''
        return self._item_class

    ### PUBLIC METHODS ###

    def accumulate(self, operands=None):
        r'''Accumulates `operands` against collections to identity.

        ..  container:: example

            Accumulates transposition:

            ::

                >>> collections = baca.CollectionList(
                ...     [[0, 2, 6, 5], [4, 8, 7]],
                ...     item_class=abjad.NumberedPitchClass,
                ...     )

            ::

                >>> transposition = baca.pitch_class_segment().transpose(n=3)
                >>> for collection in collections.accumulate([transposition]):
                ...     collection
                ...
                PitchClassSegment([0, 2, 6, 5])
                PitchClassSegment([4, 8, 7])
                PitchClassSegment([3, 5, 9, 8])
                PitchClassSegment([7, 11, 10])
                PitchClassSegment([6, 8, 0, 11])
                PitchClassSegment([10, 2, 1])
                PitchClassSegment([9, 11, 3, 2])
                PitchClassSegment([1, 5, 4])

        ..  container:: example

            Accumulates transposition followed by alpha:

            ::

                >>> collections = baca.CollectionList(
                ...     [[0, 2, 6, 5], [4, 8, 7]],
                ...     item_class=abjad.NumberedPitchClass,
                ...     )

            ::

                >>> transposition = baca.pitch_class_segment().transpose(n=3)
                >>> alpha = baca.pitch_class_segment().alpha()
                >>> operands = [transposition, alpha]
                >>> for collection in collections.accumulate(operands):
                ...     collection
                ...
                PitchClassSegment([0, 2, 6, 5])
                PitchClassSegment([4, 8, 7])
                PitchClassSegment([3, 5, 9, 8])
                PitchClassSegment([7, 11, 10])
                PitchClassSegment([2, 4, 8, 9])
                PitchClassSegment([6, 10, 11])
                PitchClassSegment([5, 7, 11, 0])
                PitchClassSegment([9, 1, 2])
                PitchClassSegment([4, 6, 10, 1])
                PitchClassSegment([8, 0, 3])
                PitchClassSegment([7, 9, 1, 4])
                PitchClassSegment([11, 3, 6])
                PitchClassSegment([6, 8, 0, 5])
                PitchClassSegment([10, 2, 7])
                PitchClassSegment([9, 11, 3, 8])
                PitchClassSegment([1, 5, 10])
                PitchClassSegment([8, 10, 2, 9])
                PitchClassSegment([0, 4, 11])
                PitchClassSegment([11, 1, 5, 0])
                PitchClassSegment([3, 7, 2])
                PitchClassSegment([10, 0, 4, 1])
                PitchClassSegment([2, 6, 3])
                PitchClassSegment([1, 3, 7, 4])
                PitchClassSegment([5, 9, 6])

        Returns new collection list.
        '''
        sequence = baca.Sequence(items=self)
        collections = []
        for sequence_ in sequence.accumulate(operands=operands):
            collections.extend(sequence_)
        return abjad.new(self, collections=collections)

    def arpeggiate_down(self, pattern=None):
        r'''Apreggiates collections down according to `pattern`.

        ..  container:: example

            Down-arpeggiates all collections:

            ::

                >>> collections = baca.CollectionList(
                ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
                ...     )

            ::

                >>> collections.arpeggiate_down()
                CollectionList([<29, 24, 14, 6, 5>, <28, 17, 7>, <3, 2, 1, 0>])

        ..  container:: example

            Down-arpeggiates collection -1:

            ::

                >>> collections = baca.CollectionList(
                ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
                ...     )

            ::

                >>> collections.arpeggiate_down(pattern=[-1])
                CollectionList([<5, 12, 14, 18, 17>, <16, 17, 19>, <3, 2, 1, 0>])

        Returns new collection list.
        '''
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                if isinstance(collection, abjad.PitchSegment):
                    collection = collection.to_pitch_classes()
                    collection = baca.PitchClassSegment(
                        items=collection,
                        item_class=collection.item_class,
                        )
                collection = collection.arpeggiate_down()
            collections.append(collection)
        return abjad.new(self, collections=collections)

    def arpeggiate_up(self, pattern=None):
        r'''Apreggiates collections up according to `pattern`.

        ..  container:: example

            Up-arpeggiates all collections:

            ::

                >>> collections = baca.CollectionList(
                ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
                ...     )

            ::

                >>> collections.arpeggiate_up()
                CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

        ..  container:: example

            Up-arpeggiates collection -1:

            ::

                >>> collections = baca.CollectionList(
                ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
                ...     )

            ::

                >>> collections.arpeggiate_up(pattern=[-1])
                CollectionList([<5, 12, 14, 18, 17>, <16, 17, 19>, <3, 14, 25, 36>])

        Returns new collection list.
        '''
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                if isinstance(collection, abjad.PitchSegment):
                    collection = collection.to_pitch_classes()
                    collection = baca.PitchClassSegment(
                        items=collection,
                        item_class=collection.item_class,
                        )
                collection = collection.arpeggiate_up()
            collections.append(collection)
        return abjad.new(self, collections=collections)

    def bass_to_octave(self, n=4, pattern=None):
        r'''Octave-transposes collections to bass in octave `n`.

        ..  container:: example

            Octave-transposes all collections:

            ::

                >>> collections = baca.CollectionList(
                ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
                ...     )
                >>> collections = collections.arpeggiate_up()

            ::

                >>> collections
                CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

            ::

                >>> collections.bass_to_octave(n=3)
                CollectionList([<-7, 0, 2, 6, 17>, <-8, -7, -5>, <-9, 2, 13, 24>])

        ..  container:: example

            Octave-transposes collection -1:

            ::

                >>> collections = baca.CollectionList(
                ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
                ...     )
                >>> collections = collections.arpeggiate_up()

            ::

                >>> collections
                CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

            ::

                >>> collections.bass_to_octave(n=3, pattern=[-1])
                CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <-9, 2, 13, 24>])

        Returns new collection list.
        '''
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                collection = collection.bass_to_octave(n=n)
            collections.append(collection)
        return abjad.new(self, collections=collections)

    def center_to_octave(self, n=4, pattern=None):
        r'''Octave-transposes collections to center in octave `n`.

        ..  container:: example

            Octave-transposes all collections:

            ::

                >>> collections = baca.CollectionList(
                ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
                ...     )
                >>> collections = collections.arpeggiate_up()

            ::

                >>> collections
                CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

            ::

                >>> collections.center_to_octave(n=3)
                CollectionList([<-19, -12, -10, -6, 5>, <-8, -7, -5>, <-21, -10, 1, 12>])

        ..  container:: example

            Octave-transposes collection -1:

            ::

                >>> collections = baca.CollectionList(
                ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
                ...     )
                >>> collections = collections.arpeggiate_up()

            ::

                >>> collections
                CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

            ::

                >>> collections.center_to_octave(n=3, pattern=[-1])
                CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <-21, -10, 1, 12>])

        Returns new collection list.
        '''
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                collection = collection.center_to_octave(n=n)
            collections.append(collection)
        return abjad.new(self, collections=collections)

    def chords(self, pattern=None):
        r'''Turns collections into chords according to `pattern`.

        ..  container:: example

            Without pattern:

            ::

                >>> collections = baca.CollectionList([
                ...     [12, 14, 18, 17],
                ...     [16, 20, 19],
                ...     [12, 14, 18, 17],
                ...     [16, 20, 19],
                ...     ])

            ::

                >>> for collection in collections:
                ...     collection
                ...
                PitchSegment([12, 14, 18, 17])
                PitchSegment([16, 20, 19])
                PitchSegment([12, 14, 18, 17])
                PitchSegment([16, 20, 19])

            ::

                >>> for collection in collections.chords():
                ...     collection
                ...
                PitchSet([12, 14, 17, 18])
                PitchSet([16, 19, 20])
                PitchSet([12, 14, 17, 18])
                PitchSet([16, 19, 20])

        ..  container:: example

            With pattern:

            ::

                >>> collections = baca.CollectionList([
                ...     [12, 14, 18, 17],
                ...     [16, 20, 19],
                ...     [12, 14, 18, 17],
                ...     [16, 20, 19],
                ...     ])


            ::

                >>> pattern = abjad.index_every([1], period=2)
                >>> for collection in collections.chords(pattern=pattern):
                ...     collection
                ...
                PitchSegment([12, 14, 18, 17])
                PitchSet([16, 19, 20])
                PitchSegment([12, 14, 18, 17])
                PitchSet([16, 19, 20])

        Returns new collection list.
        '''
        collections = []
        length = len(self)
        pattern = pattern or abjad.index_all()
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                collections.append(collection.chord())
            else:
                collections.append(collection)
        return abjad.new(self, collections=collections)

    def cursor(self, cyclic=None, singletons=None):
        r'''Wraps collections in cursor.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([[5, 12, 14, 18], [16, 17]])
                >>> cursor = collections.cursor()

            ::

                >>> f(cursor)
                baca.tools.Cursor(
                    source=baca.tools.CollectionList(
                        collections=[
                            baca.tools.PitchSegment(
                                (
                                    abjad.NumberedPitch(5),
                                    abjad.NumberedPitch(12),
                                    abjad.NumberedPitch(14),
                                    abjad.NumberedPitch(18),
                                    ),
                                item_class=abjad.NumberedPitch,
                                ),
                            baca.tools.PitchSegment(
                                (
                                    abjad.NumberedPitch(16),
                                    abjad.NumberedPitch(17),
                                    ),
                                item_class=abjad.NumberedPitch,
                                ),
                            ],
                        ),
                    )

            ::

                >>> cursor.next()
                [PitchSegment([5, 12, 14, 18])]

            ::

                >>> cursor.next()
                [PitchSegment([16, 17])]

        Returns cursor.
        '''
        return baca.Cursor(self, cyclic=cyclic, singletons=singletons)

    def flatten(self):
        r'''Flattens collections.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList(
                ...     [[5, 12, 14, 18, 17], [16, 17, 19]],
                ...     )

            ::

                >>> str(collections.flatten())
                '<5, 12, 14, 18, 17, 16, 17, 19>'

        ..  container:: example

            ::

                >>> collections = baca.CollectionList(
                ...     [[5, 12, 14, 18, 17], [16, 17, 19]],
                ...     item_class=abjad.NamedPitch,
                ...     )

            ::

                >>> str(collections.flatten())
                "<f' c'' d'' fs'' f'' e'' f'' g''>"

        Returns collection.
        '''
        return self.join()[0]

    def has_duplicate_pitch_classes(self, level=-1):
        r'''Is true when collections have duplicate pitch-classes at `level`.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([
                ...     [4, 5, 7],
                ...     [15, 16, 17, 19]
                ...     ])

            ::

                >>> collections.has_duplicate_pitch_classes(level=1)
                False

            ::

                >>> collections.has_duplicate_pitch_classes(level=-1)
                True

        Set `level` to 1 or -1.

        Returns true or false.
        '''
        pitch_class_class = self._get_pitch_class_class()
        if level == 1:
            for collection in self:
                known_pitch_classes = []
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class in known_pitch_classes:
                        return True
                    known_pitch_classes.append(pitch_class)
        elif level == -1:
            known_pitch_classes = []
            for collection in self:
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class in known_pitch_classes:
                        return True
                    known_pitch_classes.append(pitch_class)
        else:
            message = 'level must be 1 or -1: {!r}.'
            message = message.format(level)
            raise ValueError(message)
        return False

    def has_duplicates(self, level=-1):
        r'''Is true when collections have duplicates at `level`.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([
                ...     [16, 17], [13], [16, 17],
                ...     ])

            ::

                >>> collections.has_duplicates(level=0)
                True

            ::

                >>> collections.has_duplicates(level=1)
                False

            ::

                >>> collections.has_duplicates(level=-1)
                True

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([[16, 17], [14, 20, 14]])

            ::

                >>> collections.has_duplicates(level=0)
                False

            ::

                >>> collections.has_duplicates(level=1)
                True

            ::

                >>> collections.has_duplicates(level=-1)
                True

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([
                ...     [16, 17], [14, 20], [14],
                ...     ])

            ::

                >>> collections.has_duplicates(level=0)
                False

            ::

                >>> collections.has_duplicates(level=1)
                False

            ::

                >>> collections.has_duplicates(level=-1)
                True

        Set `level` to 0, 1 or -1.

        Returns true or false.
        '''
        if level == 0:
            known_items = []
            for collection in self:
                if collection in known_items:
                    return True
                known_items.append(collection)
        elif level == 1:
            for collection in self:
                known_items = []
                for item in collection:
                    if item in known_items:
                        return True
                    known_items.append(item)
        elif level == -1:
            known_items = []
            for collection in self:
                items = []
                for item in collection:
                    if item in known_items:
                        return True
                    known_items.append(item)
        else:
            message = 'level must be 0, 1 or -1: {!r}.'
            message = message.format(level)
            raise ValueError(message)
        return False

    def has_repeat_pitch_classes(self, level=-1):
        r'''Is true when collections have repeat pitch-classes as `level`.

        ..  container:: example

                >>> collections = baca.CollectionList([[4, 5, 4, 5], [17, 18]])

            ::

                >>> collections.has_repeat_pitch_classes(level=1)
                False

            ::

                >>> collections.has_repeat_pitch_classes(level=-1)
                True

        Set `level` to 0 or -1.

        Returns true or false.
        '''
        pitch_class_class = self._get_pitch_class_class()
        if level == 1:
            for collection in self:
                previous_pitch_class = None
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class == previous_pitch_class:
                        return True
                    previous_pitch_class = pitch_class
        elif level == -1:
            previous_pitch_class = None
            for collection in self:
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class == previous_pitch_class:
                        return True
                    previous_pitch_class = pitch_class
        else:
            message = 'level must be 0 or -1: {!r}.'
            message = message.format(level)
            raise ValueError(message)
        return False

    def has_repeats(self, level=-1):
        r'''Is true when collections have repeats at `level`.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([[4, 5], [4, 5]])

            ::

                >>> collections.has_repeats(level=0)
                True

            ::

                >>> collections.has_repeats(level=1)
                False

            ::

                >>> collections.has_repeats(level=-1)
                False

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([
                ...     [4, 5], [18, 18], [4, 5],
                ...     ])

            ::

                >>> collections.has_repeats(level=0)
                False

            ::

                >>> collections.has_repeats(level=1)
                True

            ::

                >>> collections.has_repeats(level=-1)
                True

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([
                ...     [4, 5], [5, 18], [4, 5],
                ...     ])

            ::

                >>> collections.has_repeats(level=0)
                False

            ::

                >>> collections.has_repeats(level=1)
                False

            ::

                >>> collections.has_repeats(level=-1)
                True

        Set `level` to 0, 1 or -1.

        Returns true or false.
        '''
        if level == 0:
            previous_collection = None
            for collection in self:
                if collection == previous_collection:
                    return True
                previous_collection = collection
        elif level == 1:
            for collection in self:
                previous_item = None
                for item in collection:
                    if item == previous_item:
                        return True
                    previous_item = item
        elif level == -1:
            previous_item = None
            for collection in self:
                for item in collection:
                    if item == previous_item:
                        return True
                    previous_item = item
        else:
            message = 'level must be 0, 1 or -1: {!r}.'
            message = message.format(level)
            raise ValueError(message)
        return False

    def helianthate(self, n=0, m=0):
        r'''Helianthates collections.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([[1, 2, 3], [4, 5], [6, 7, 8]])
                >>> for collection in collections.helianthate(n=-1, m=1):
                ...     collection
                ...
                PitchSegment([1, 2, 3])
                PitchSegment([4, 5])
                PitchSegment([6, 7, 8])
                PitchSegment([5, 4])
                PitchSegment([8, 6, 7])
                PitchSegment([3, 1, 2])
                PitchSegment([7, 8, 6])
                PitchSegment([2, 3, 1])
                PitchSegment([4, 5])
                PitchSegment([1, 2, 3])
                PitchSegment([5, 4])
                PitchSegment([6, 7, 8])
                PitchSegment([4, 5])
                PitchSegment([8, 6, 7])
                PitchSegment([3, 1, 2])
                PitchSegment([7, 8, 6])
                PitchSegment([2, 3, 1])
                PitchSegment([5, 4])

        Returns new collection list.
        '''
        collections = baca.Sequence(items=self)
        collections = collections.helianthate(n=n, m=m)
        return abjad.new(self, collections=collections)

    def join(self):
        r'''Joins collections.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([
                ...     [5, 12, 14, 18, 17],
                ...     [16, 17, 19],
                ...     ])

            ::

                >>> collections.join()
                CollectionList([<5, 12, 14, 18, 17, 16, 17, 19>])

        Returns new collection list.
        '''
        collections = []
        if self:
            collection = self[0]
            for collection_ in self[1:]:
                collection = collection + collection_
            collections.append(collection)
        return abjad.new(self, collections=collections)

    def partition(self, argument, cyclic=False, join=False, overhang=False):
        r'''Partitions collections according to `argument`.

        ..  container:: example

            Returns sequence:

            ::

                >>> collections = baca.CollectionList([
                ...     [5, 12, 14, 18, 17],
                ...     [16, 17, 19],
                ...     [16, 17, 19],
                ...     ])

            ::

                >>> sequence = collections.partition([1, 2], overhang=Exact)
                >>> for collection_list in sequence:
                ...     collection_list
                ...
                CollectionList([<5, 12, 14, 18, 17>])
                CollectionList([<16, 17, 19>, <16, 17, 19>])

            ::

                >>> isinstance(sequence, baca.Sequence)
                True

        ..  container:: example

            Joins parts. Returns new collection list:

            ::

                >>> collections = baca.CollectionList([
                ...     [5, 12, 14, 18, 17],
                ...     [16, 17, 19],
                ...     [16, 17, 19],
                ...     ])

            ::

                >>> collections
                CollectionList([<5, 12, 14, 18, 17>, <16, 17, 19>, <16, 17, 19>])

            ::

                >>> collections.partition([1, 2], join=True, overhang=Exact)
                CollectionList([<5, 12, 14, 18, 17>, <16, 17, 19, 16, 17, 19>])

        ..  container:: example

            Repeats, partitions, joins parts. Returns new collection list:

            ::

                >>> collections = baca.CollectionList([
                ...     [5, 12, 14, 18, 17],
                ...     [16, 17, 19],
                ...     [16, 17, 19],
                ...     ])

            ::

                >>> collections = collections.repeat(2)
                >>> for collection in collections.partition(
                ...     [2],
                ...     cyclic=True,
                ...     join=True,
                ...     ):
                ...     collection
                ...
                PitchSegment([5, 12, 14, 18, 17, 16, 17, 19])
                PitchSegment([16, 17, 19, 5, 12, 14, 18, 17])
                PitchSegment([16, 17, 19, 16, 17, 19])

        Returns sequence.
        '''
        if isinstance(argument, abjad.Ratio):
            message = 'implement ratio-partition at some point.'
            raise NotImplementedError(message)
        sequence = baca.Sequence(self)
        parts = sequence.partition_by_counts(
            argument,
            cyclic=cyclic,
            overhang=overhang,
            )
        collection_lists = [abjad.new(self, collections=_) for _ in parts]
        if join:
            collections = [_.join()[0] for _ in collection_lists]
            result = abjad.new(self, collections=collections)
        else:
            result = baca.Sequence(collection_lists)
        return result

    def read(self, counts=None, check=None):
        r'''Reads collections by `counts`.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([
                ...     [5, 12, 14, 18, 17],
                ...     [16, 17, 19],
                ...     ])

            ::

                >>> for collection in collections.read([3, 3, 3, 5, 5, 5]):
                ...     collection
                ...
                PitchSegment([5, 12, 14])
                PitchSegment([18, 17, 16])
                PitchSegment([17, 19, 5])
                PitchSegment([12, 14, 18, 17, 16])
                PitchSegment([17, 19, 5, 12, 14])
                PitchSegment([18, 17, 16, 17, 19])

        ..  container:: example

            Raises exception on inexact read:

            ::

                >>> collections = baca.CollectionList([
                ...     [5, 12, 14, 18, 17],
                ...     [16, 17, 19],
                ...     ])

            ::

                >>> len(collections.flatten())
                8

            ::

                >>> collections.read([10, 10, 10], check=Exact)
                Traceback (most recent call last):
                    ...
                ValueError: call reads 30 items; not a multiple of 8 items.

        Returns new collection list.
        '''
        if counts in (None, []):
            return abjad.new(self)
        counts = list(counts)
        assert all(isinstance(_, int) for _ in counts), repr(counts)
        collection = self.join()[0]
        source = abjad.CyclicTuple(collection)
        i = 0
        collections = []
        for count in counts:
            stop = i + count
            items = source[i:stop]
            collection = self._initialize_collection(items)
            collections.append(collection)
            i += count
        result = abjad.new(self, collections=collections)
        if check is Exact:
            self_item_count = len(self.flatten())
            result_item_count = len(result.flatten())
            quotient = result_item_count / self_item_count
            if quotient != int(quotient):
                message = 'call reads {} items; not a multiple of {} items.'
                message = message.format(result_item_count, self_item_count)
                raise ValueError(message)
        return result

    # TODO: change indices to pattern
    # TODO: add level=-1 keyword
    def remove(self, indices=None, period=None):
        r'''Removes collections at `indices`.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([[0, 1], [2, 3], [4], [5, 6]])
                >>> collections.remove([0, -1])
                CollectionList([<2, 3>, <4>])

        Returns new collection list.
        '''
        sequence = baca.Sequence(items=self)
        collections = sequence.remove(indices=indices, period=period)
        return abjad.new(self, collections=collections)

    def remove_duplicate_pitch_classes(self, level=-1):
        r'''Removes duplicate pitch-classes at `level`.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([[4, 5, 7], [16, 17, 16, 18]])

            ::

                >>> collections.remove_duplicate_pitch_classes(level=1)
                CollectionList([<4, 5, 7>, <16, 17, 18>])

            ::

                >>> collections.remove_duplicate_pitch_classes(level=-1)
                CollectionList([<4, 5, 7>, <18>])

        Set `level` to 1 or -1.

        Returns new collection list.
        '''
        pitch_class_class = self._get_pitch_class_class()
        collections_ = []
        if level == 1:
            for collection in self:
                items, known_pitch_classes = [], []
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class in known_pitch_classes:
                        continue
                    known_pitch_classes.append(pitch_class)
                    items.append(item)
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        elif level == -1:
            known_pitch_classes = []
            for collection in self:
                items = []
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class in known_pitch_classes:
                        continue
                    known_pitch_classes.append(pitch_class)
                    items.append(item)
                if items:
                    collection_ = self._initialize_collection(items, collection)
                    collections_.append(collection_)
        else:
            message = 'level must be 1 or -1: {!r}.'
            message = message.format(level)
            raise ValueError(message)
        return abjad.new(self, collections=collections_)

    def remove_duplicates(self, level=-1):
        r'''Removes duplicates at `level`.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList(
                ...     [[16, 17, 16], [13, 14, 16], [16, 17, 16]],
                ...     )

            ::

                >>> collections.remove_duplicates(level=0)
                CollectionList([<16, 17, 16>, <13, 14, 16>])

            ::

                >>> collections.remove_duplicates(level=1)
                CollectionList([<16, 17>, <13, 14, 16>, <16, 17>])

            ::

                >>> collections.remove_duplicates(level=-1)
                CollectionList([<16, 17>, <13, 14>])

        Set `level` to 0, 1 or -1.

        Returns new collection list.
        '''
        collections_ = []
        if level == 0:
            collections_, known_items = [], []
            for collection in self:
                if collection in known_items:
                    continue
                known_items.append(collection)
                collections_.append(collection)
        elif level == 1:
            for collection in self:
                items, known_items = [], []
                for item in collection:
                    if item in known_items:
                        continue
                    known_items.append(item)
                    items.append(item)
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        elif level == -1:
            known_items = []
            for collection in self:
                items = []
                for item in collection:
                    if item in known_items:
                        continue
                    known_items.append(item)
                    items.append(item)
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        else:
            message = 'level must be 0, 1 or -1: {!r}.'
            message = message.format(level)
            raise ValueError(message)
        return abjad.new(self, collections=collections_)

    def remove_repeat_pitch_classes(self, level=-1):
        r'''Removes repeat pitch-classes at `level`.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([[4, 4, 4, 5], [17, 18]])

            ::

                >>> collections.remove_repeat_pitch_classes(level=1)
                CollectionList([<4, 5>, <17, 18>])

            ::

                >>> collections.remove_repeat_pitch_classes(level=-1)
                CollectionList([<4, 5>, <18>])

        Set `level` to 1 or -1.

        Returns new collection list.
        '''
        pitch_class_class = self._get_pitch_class_class()
        collections_ = []
        if level == 1:
            for collection in self:
                items, previous_pitch_class = [], None
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class == previous_pitch_class:
                        continue
                    items.append(item)
                    previous_pitch_class = pitch_class
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        elif level == -1:
            previous_pitch_class = None
            for collection in self:
                items = []
                for item in collection:
                    pitch_class = pitch_class_class(item)
                    if pitch_class == previous_pitch_class:
                        continue
                    items.append(item)
                    previous_pitch_class = pitch_class
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        else:
            message = 'level must be 1 or -1: {!r}.'
            message = message.format(level)
            raise ValueError(message)
        return abjad.new(self, collections=collections_)

    def remove_repeats(self, level=-1):
        r'''Removes repeats at `level`.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([[4, 5], [4, 5], [5, 7, 7]])

            ::

                >>> collections.remove_repeats(level=0)
                CollectionList([<4, 5>, <5, 7, 7>])

            ::

                >>> collections.remove_repeats(level=1)
                CollectionList([<4, 5>, <4, 5>, <5, 7>])

            ::

                >>> collections.remove_repeats(level=-1)
                CollectionList([<4, 5>, <4, 5>, <7>])

        Set `level` to 0, 1 or -1.

        Returns true or false.
        '''
        collections_ = []
        if level == 0:
            previous_collection = None
            for collection in self:
                if collection == previous_collection:
                    continue
                collections_.append(collection)
                previous_collection = collection
        elif level == 1:
            for collection in self:
                items, previous_item = [], None
                for item in collection:
                    if item == previous_item:
                        continue
                    items.append(item)
                    previous_item = item
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        elif level == -1:
            previous_item = None
            for collection in self:
                items = []
                for item in collection:
                    if item == previous_item:
                        continue
                    items.append(item)
                    previous_item = item
                if items:
                    collection_ = self._initialize_collection(items)
                    collections_.append(collection_)
        else:
            message = 'level must be 0, 1 or -1: {!r}.'
            message = message.format(level)
            raise ValueError(message)
        return abjad.new(self, collections=collections_)

    def repeat(self, n=1):
        r'''Repeats collections.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([[12, 14, 18, 17], [16, 19]])
                >>> for collection in collections.repeat(n=3):
                ...     collection
                ...
                PitchSegment([12, 14, 18, 17])
                PitchSegment([16, 19])
                PitchSegment([12, 14, 18, 17])
                PitchSegment([16, 19])
                PitchSegment([12, 14, 18, 17])
                PitchSegment([16, 19])

        Returns new collection list.
        '''
        collections = baca.Sequence(items=self)
        collections = collections.repeat(n=n)
        collections = collections.flatten(depth=1)
        return abjad.new(self, collections=collections)

    # TODO: change indices to pattern
    # TODO: add level=-1 keyword
    def retain(self, indices=None, period=None):
        r'''Retains collections at `indices`.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList([[0, 1], [2, 3], [4], [5, 6]])
                >>> collections.retain([0, -1])
                CollectionList([<0, 1>, <5, 6>])

        ..  container:: example

            ::

                >>> collections = baca.CollectionList(
                ...     [[0, 1], [2, 3], [4], [5, 6], [7], [8]],
                ...     )
                >>> collections.retain([0], period=2)
                CollectionList([<0, 1>, <4>, <7>])

        Returns new collection list.
        '''
        sequence = baca.Sequence(items=self)
        collections = sequence.retain(indices=indices, period=period)
        return abjad.new(self, collections=collections)

    def soprano_to_octave(self, n=4, pattern=None):
        r'''Octave-transposes collections to soprano in octave `n`.

        ..  container:: example

            Octave-transposes all collections:

            ::

                >>> collections = baca.CollectionList(
                ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
                ...     )
                >>> collections = collections.arpeggiate_up()

            ::

                >>> collections
                CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

            ::

                >>> collections.soprano_to_octave(n=4)
                CollectionList([<-19, -12, -10, -6, 5>, <4, 5, 7>, <-33, -22, -11, 0>])

        ..  container:: example

            Octave-transposes collection -1:

            ::

                >>> collections = baca.CollectionList(
                ...     [[5, 12, 14, 18, 17], [16, 17, 19], [3, 2, 1, 0]],
                ...     )
                >>> collections = collections.arpeggiate_up()

            ::

                >>> collections
                CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <3, 14, 25, 36>])

            ::

                >>> collections.soprano_to_octave(n=4, pattern=[-1])
                CollectionList([<5, 12, 14, 18, 29>, <4, 5, 7>, <-33, -22, -11, 0>])

        Returns new collection list.
        '''
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                collection = collection.soprano_to_octave(n=n)
            collections.append(collection)
        return abjad.new(self, collections=collections)

    def space_down(
        self,
        bass=None,
        pattern=None,
        semitones=None,
        soprano=None,
        ):
        r'''Spaces collections down.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList(
                ...     [[5, 12, 14, 18, 17], [16, 17, 19]],
                ...     )

            ::

                >>> collections.space_down(bass=5)
                CollectionList([<24, 18, 14, 5>, <16, 7, 5>])

        '''
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                collection = collection.space_down(
                    bass=bass,
                    semitones=semitones,
                    soprano=soprano,
                    )
            collections.append(collection)
        return abjad.new(self, collections=collections)

    def space_up(
        self,
        bass=None,
        pattern=None,
        semitones=None,
        soprano=None,
        ):
        r'''Spaces collections up.

        ..  container:: example

            ::

                >>> collections = baca.CollectionList(
                ...     [[5, 12, 14, 18, 17], [16, 17, 19]],
                ...     )

            ::

                >>> collections.space_up(bass=5)
                CollectionList([<5, 6, 12, 14>, <5, 7, 16>])

        '''
        if isinstance(pattern, list):
            pattern = abjad.Pattern(indices=pattern)
        pattern = pattern or abjad.index_all()
        length = len(self)
        collections = []
        for i, collection in enumerate(self):
            if pattern.matches_index(i, length):
                collection = collection.space_up(
                    bass=bass,
                    semitones=semitones,
                    soprano=soprano,
                    )
            collections.append(collection)
        return abjad.new(self, collections=collections)

    def to_pitch_classes(self):
        r'''Changes to pitch-class collections.

        ..  container:: example

            To numbered pitch-class collections:

            ..  container:: example

                ::

                    >>> collections = baca.CollectionList(
                    ...     [[12, 14, 18, 17], [16, 20, 19]],
                    ...     item_class=abjad.NumberedPitch,
                    ...     )

                ::

                    >>> collections.to_pitch_classes()
                    CollectionList([PC<0, 2, 6, 5>, PC<4, 8, 7>])

            ..  container:: example

                ::

                    >>> collections = baca.CollectionList(
                    ...     [[0, 2, 6, 5], [4, 8, 7]],
                    ...     item_class=abjad.NumberedPitchClass,
                    ...     )

                ::

                    >>> collections.to_pitch_classes()
                    CollectionList([PC<0, 2, 6, 5>, PC<4, 8, 7>])

        ..  container:: example

            To named pitch-class collections:

            ..  container:: example

                ::

                    >>> collections = baca.CollectionList(
                    ...     [[12, 14, 18, 17], [16, 20, 19]],
                    ...     item_class=abjad.NamedPitch,
                    ...     )

                ::

                    >>> collections.to_pitch_classes()
                    CollectionList([PC<c d fs f>, PC<e af g>])

            ..  container:: example

                ::

                    >>> collections = baca.CollectionList(
                    ...     [[0, 2, 6, 5], [4, 8, 7]],
                    ...     item_class=abjad.NamedPitchClass,
                    ...     )

                ::

                    >>> collections.to_pitch_classes()
                    CollectionList([PC<c d fs f>, PC<e af g>])

        Returns new collection list.
        '''
        item_class = self._to_pitch_class_item_class(self.item_class)
        collections_ = []
        for collection in self:
            collection_ = collection.to_pitch_classes()
            collections_.append(collection_)
        return abjad.new(self, collections=collections_, item_class=item_class)

    def to_pitches(self):
        r'''Changes to pitch collections.

        ..  container:: example

            To numbered pitch collections:

            ..  container:: example

                ::

                    >>> collections = baca.CollectionList(
                    ...     [[12, 14, 18, 17], [16, 20, 19]],
                    ...     item_class=abjad.NumberedPitch,
                    ...     )

                ::

                    >>> collections.to_pitches()
                    CollectionList([<12, 14, 18, 17>, <16, 20, 19>])

            ..  container:: example

                ::

                    >>> collections = baca.CollectionList(
                    ...     [[0, 2, 6, 5], [4, 8, 7]],
                    ...     item_class=abjad.NumberedPitchClass,
                    ...     )

                ::

                    >>> collections.to_pitches()
                    CollectionList([<0, 2, 6, 5>, <4, 8, 7>])

        ..  container:: example

            To named pitch collections:

            ..  container:: example

                ::

                    >>> collections = baca.CollectionList(
                    ...     [[12, 14, 18, 17], [16, 20, 19]],
                    ...     item_class=abjad.NamedPitch,
                    ...     )

                ::

                    >>> collections.to_pitches()
                    CollectionList([<c'' d'' fs'' f''>, <e'' af'' g''>])

            ..  container:: example

                ::

                    >>> collections = baca.CollectionList(
                    ...     [[0, 2, 6, 5], [4, 8, 7]],
                    ...     item_class=abjad.NamedPitchClass,
                    ...     )

                ::

                    >>> collections.to_pitches()
                    CollectionList([<c' d' fs' f'>, <e' af' g'>])

        Returns new collection list.
        '''
        item_class = self._to_pitch_item_class(self.item_class)
        collections_ = []
        for collection in self:
            collection_ = collection.to_pitches()
            collections_.append(collection_)
        return abjad.new(self, collections=collections_, item_class=item_class)


collections_module.Sequence.register(CollectionList)
