# -*- coding: utf-8 -*-
import abjad
import baca
import collections


class SegmentList(abjad.abctools.AbjadValueObject):
    r'''Segment list.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Initializes numbered pitch segments:

        ::

            >>> for segment in baca.SegmentList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     ]):
            ...     segment
            ...
            PitchSegment([12, 14, 18, 17])
            PitchSegment([16, 20, 19])

    ..  container:: example

        Initializes named pitch segments:

        ::

            >>> for segment in baca.SegmentList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     ],
            ...     item_class=abjad.NamedPitch,
            ...     ):
            ...     segment
            ...
            PitchSegment("c'' d'' fs'' f''")
            PitchSegment("e'' af'' g''")

    ..  container:: example

        Initializes numbered pitch-class segments:

        ::

            >>> for segment in baca.SegmentList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     ],
            ...     item_class=abjad.NumberedPitchClass,
            ...     ):
            ...     segment
            ...
            PitchClassSegment([0, 2, 6, 5])
            PitchClassSegment([4, 8, 7])

    ..  container:: example

        Initializes named pitch-class segments:

        ::

            >>> for segment in baca.SegmentList([
            ...     [12, 14, 18, 17],
            ...     [16, 20, 19],
            ...     ],
            ...     item_class=abjad.NamedPitchClass,
            ...     ):
            ...     segment
            ...
            PitchClassSegment("c d fs f")
            PitchClassSegment("e af g")

    ..  container:: example

        Initializes mixed numbered and named pitch segments:

        ::

            >>> for segment in baca.SegmentList([
            ...     [12, 14, 18, 17],
            ...     "ff'' gs'' g''",
            ...     ]):
            ...     segment
            ...
            PitchSegment([12, 14, 18, 17])
            PitchSegment("ff'' gs'' g''")

    ..  container:: example

        Initializes from segment list:

        ::

            >>> segments = baca.SegmentList([[12, 13, 14], [15, 16, 17]])
            >>> baca.SegmentList(segments)
            SegmentList([<12, 13, 14>, <15, 16, 17>])

    ..  container:: example

        Initializes from list of segment lists:

        ::

            >>> segment_list_1 = baca.SegmentList([[12, 13, 14]])
            >>> segment_list_2 = baca.SegmentList([[15, 16, 17]])
            >>> baca.SegmentList([segment_list_1, segment_list_2])
            SegmentList([<12, 13, 14>, <15, 16, 17>])

    ..  container:: example

        Initializes empty:

        ::

            >>> baca.SegmentList()
            SegmentList([])

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        '_as_chords',
        '_expression',
        '_item_class',
        '_segments',
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
        segments=None,
        as_chords=None,
        item_class=None,
        ):
        self._expression = None
        if item_class is not None:
            if item_class not in self._item_class_prototype:
                message = 'must be pitch or pitch-class: {!r}.'
                message = message.format(item_class)
                raise TypeError(message)
        self._item_class = item_class
        segments = self._coerce(segments)
        segments = segments or []
        self._segments = tuple(segments)
        if as_chords is not None:
            as_chords = bool(as_chords)
        self._as_chords = as_chords

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        r'''Adds `argument` to segments.

        ..  container:: example

                >>> segments_1 = baca.SegmentList([[12, 14, 18, 17]])
                >>> segments_2 = baca.SegmentList([[16, 20, 19]])
                >>> segments_1 + segments_2
                SegmentList([<12, 14, 18, 17>, <16, 20, 19>])

        Returns new segment list.
        '''
        if not isinstance(argument, collections.Iterable):
            message = 'must be segment list: {!r}.'
            message = message.format(argument)
            raise TypeError(message)
        argument_segments = [self._initialize_segment(_) for _ in argument]
        segments = self.segments + argument_segments
        return abjad.new(self, segments=segments)

    def __eq__(self, argument):
        r'''Is true when `argument` is a segment list with segments equal to
        those of this segment list. Otherwise false.

        ..  container:: example

            ::

                >>> segments_1 = baca.SegmentList([[12, 13, 14], [15, 16, 17]])
                >>> segments_2 = baca.SegmentList([[12, 13, 14], [15, 16, 17]])
                >>> segments_3 = baca.SegmentList([[12, 13, 14]])

            ::

                >>> segments_1 == segments_1
                True

            ::

                >>> segments_1 == segments_2
                True

            ::

                >>> segments_1 == segments_3
                False

            ::

                >>> segments_2 == segments_1
                True

            ::

                >>> segments_2 == segments_2
                True

            ::

                >>> segments_2 == segments_3
                False

            ::

                >>> segments_3 == segments_1
                False

            ::

                >>> segments_3 == segments_2
                False

            ::

                >>> segments_3 == segments_3
                True

        ..  container:: example

            Ignores item class:

            ::

                >>> segments_1 = baca.SegmentList(
                ...     segments=[[12, 13, 14], [15, 16, 17]],
                ...     item_class=None,
                ...     )
                >>> segments_2 = baca.SegmentList(
                ...     segments=[[12, 13, 14], [15, 16, 17]],
                ...     item_class=abjad.NumberedPitch,
                ...     )

            ::

                >>> segments_1.item_class == segments_2.item_class
                False

            ::

                >>> segments_1 == segments_2
                True

        Returns true or false.
        '''
        if not isinstance(argument, type(self)):
            return False
        return self.segments == argument.segments

    def __format__(self, format_specification=''):
        r'''Gets storage format of segments.

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([
                ...     [12, 14, 18, 17],
                ...     [16, 20, 19],
                ...     ])

            ::

                >>> f(segments)
                baca.tools.SegmentList(
                    segments=[
                        pitchtools.PitchSegment(
                            (
                                pitchtools.NumberedPitch(12),
                                pitchtools.NumberedPitch(14),
                                pitchtools.NumberedPitch(18),
                                pitchtools.NumberedPitch(17),
                                ),
                            item_class=pitchtools.NumberedPitch,
                            ),
                        pitchtools.PitchSegment(
                            (
                                pitchtools.NumberedPitch(16),
                                pitchtools.NumberedPitch(20),
                                pitchtools.NumberedPitch(19),
                                ),
                            item_class=pitchtools.NumberedPitch,
                            ),
                        ],
                    )

        Returns string.
        '''
        superclass = super(SegmentList, self)
        return superclass.__format__()

    def __getitem__(self, argument):
        r'''Gets segment or segment slice identified by `argument`.

        ..  container:: example

            Gets segments:

            ::

                >>> segments = baca.SegmentList([
                ...     [12, 14, 18, 17],
                ...     [16, 20, 19],
                ...     ])

            ::

                >>> segments[0]
                PitchSegment([12, 14, 18, 17])

            ::

                >>> segments[-1]
                PitchSegment([16, 20, 19])

        ..  container:: example

            Gets segment lists:

            ::

                >>> segments = baca.SegmentList([
                ...     [12, 14, 18, 17],
                ...     [16, 20, 19],
                ...     ])

            ::

                >>> segments[:1]
                SegmentList([<12, 14, 18, 17>])

            ::

                >>> segments[-1:]
                SegmentList([<16, 20, 19>])

        Returns segment.
        '''
        segments = self.segments or []
        result = segments.__getitem__(argument)
        try:
            return abjad.new(self, segments=result)
        except TypeError:
            return result

    def __illustrate__(self):
        r'''Illustrates segments.

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([
                ...     [12, 14, 18, 17],
                ...     [16, 20, 19],
                ...     ])

            ::

                >>> show(segments) # doctest: +SKIP

            ..  doctest::

                >>> lilypond_file = segments.__illustrate__()
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
        tree = baca.tools.PitchTree(list(self))
        return tree.__illustrate__()

    def __len__(self):
        r'''Gets length of segments.

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([
                ...     [12, 14, 18, 17],
                ...     [16, 20, 19],
                ...     ])

            ::

                >>> len(segments)
                2

        Returns nonnegative integer.
        '''
        return len(self.segments)

    def __repr__(self):
        r'''Gets interpreter representation of segments.

        ..  container:: example

            ::

                >>> baca.SegmentList([
                ...     [12, 14, 18, 17],
                ...     [16, 20, 19],
                ...     ])
                SegmentList([<12, 14, 18, 17>, <16, 20, 19>])

        Returns string.
        '''
        segments = self.segments or []
        segments = ', '.join([str(_) for _ in segments])
        string = '{}([{}])'
        string = string.format(type(self).__name__, segments)
        if self._expression:
            string = '*' + string
        return string

    ### PRIVATE METHODS ###

    def _coerce(self, segments):
        segments_ = []
        prototype = (abjad.PitchSegment, abjad.PitchClassSegment)
        for item in segments or []:
            if isinstance(item, type(self)):
                for segment in item:
                    segment_ = self._initialize_segment(segment)
                    assert isinstance(segment_, prototype), repr(segment_)
                    segments_.append(segment_)
            else:
                segment_ = self._initialize_segment(item)
                assert isinstance(segment_, prototype), repr(segment_)
                segments_.append(segment_)
        return segments_

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

    def _initialize_segment(self, argument):
        items = argument
        item_class = self.item_class or abjad.NumberedPitch
        if isinstance(argument, abjad.pitchtools.Segment):
            return argument
        elif self.item_class is not None:
            if item_class in (abjad.NumberedPitch, abjad.NamedPitch):
                return abjad.PitchSegment(items=items, item_class=item_class)
            elif item_class in (abjad.NumberedPitchClass, abjad.NamedPitchClass):
                return baca.PitchClassSegment(
                    items=items,
                    item_class=item_class,
                    )
            else:
                raise TypeError(item_class)
        else:
            if isinstance(argument, str):
                return abjad.PitchSegment(
                    items=items,
                    item_class=abjad.NamedPitch,
                    )
            elif isinstance(argument, collections.Iterable):
                return abjad.PitchSegment(
                    items=items,
                    item_class=abjad.NumberedPitch,
                    )
            else:
                message = 'must be string or other iterable: {!r}.'
                message = message.format(argument)
                raise TypeError(message)

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
    def as_chords(self):
        r'''Is true when segments in list interpret as chords.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._as_chords
            
    @property
    def item_class(self):
        r'''Gets item class of segments in list.

        Set to class modeling pitch or pitch-class.

        Returns class or none.
        '''
        return self._item_class

    @property
    def segments(self):
        r'''Gets segments in list.

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([
                ...     [12, 14, 18, 17],
                ...     [16, 20, 19],
                ...     ])

            ::

                >>> segments.segments
                [PitchSegment([12, 14, 18, 17]), PitchSegment([16, 20, 19])]

        Returns list.
        '''
        if self._segments:
            return list(self._segments)

    ### PUBLIC METHODS ###

    def flatten(self):
        r'''Flattens segments.

        ..  container:: example

            ::

                >>> segments = baca.SegmentList(
                ...     [[5, 12, 14, 18, 17], [16, 17, 19]],
                ...     )

            ::

                >>> str(segments.flatten())
                '<5, 12, 14, 18, 17, 16, 17, 19>'

        ..  container:: example

            ::

                >>> segments = baca.SegmentList(
                ...     [[5, 12, 14, 18, 17], [16, 17, 19]],
                ...     item_class=abjad.NamedPitch,
                ...     )

            ::

                >>> str(segments.flatten())
                "<f' c'' d'' fs'' f'' e'' f'' g''>"

        Returns segment.
        '''
        return self.join()[0]

    def join(self):
        r'''Joins segments.

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([
                ...     [5, 12, 14, 18, 17],
                ...     [16, 17, 19],
                ...     ])

            ::

                >>> segments.join()
                SegmentList([<5, 12, 14, 18, 17, 16, 17, 19>])

        Returns new segment list.
        '''
        segments = []
        if self:
            segment = self[0]
            for segment_ in self[1:]:
                segment = segment + segment_ 
            segments.append(segment)
        return abjad.new(self, segments=segments)

    def partition(self, argument, cyclic=False, overhang=False):
        r'''Partitions segments according to `argument`.

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([
                ...     [5, 12, 14, 18, 17],
                ...     [16, 17, 19],
                ...     [16, 17, 19],
                ...     ])

            ::

                >>> segments
                SegmentList([<5, 12, 14, 18, 17>, <16, 17, 19>, <16, 17, 19>])

            ::

                >>> sequence = segments.partition([1, 2], overhang=Exact)
                >>> for segments in sequence:
                ...     segments
                ...
                SegmentList([<5, 12, 14, 18, 17>])
                SegmentList([<16, 17, 19>, <16, 17, 19>])

            ::

                >>> isinstance(sequence, baca.Sequence)
                True

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
        segment_lists = [abjad.new(self, segments=_) for _ in parts]
        return baca.Sequence(segment_lists)

    def read(self, counts=None):
        r'''Reads segments by `counts`.

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([
                ...     [5, 12, 14, 18, 17],
                ...     [16, 17, 19],
                ...     ])

            ::

                >>> for segment in segments.read([3, 3, 3, 5, 5, 5]):
                ...     segment
                ...
                PitchSegment([5, 12, 14])
                PitchSegment([18, 17, 16])
                PitchSegment([17, 19, 5])
                PitchSegment([12, 14, 18, 17, 16])
                PitchSegment([17, 19, 5, 12, 14])
                PitchSegment([18, 17, 16, 17, 19])

        Returns new segment list.
        '''
        if counts in (None, []):
            return abjad.new(self)
        counts = list(counts)
        assert all(isinstance(_, int) for _ in counts), repr(counts)
        segment = self.join()[0]
        source = abjad.CyclicTuple(segment)
        i = 0
        segments = []
        for count in counts:
            items = source[i:i+count]
            segment = self._initialize_segment(items)
            segments.append(segment)
            i += count
        return abjad.new(self, segments=segments)

    def remove_duplicate_pitch_classes(self):
        r'''Removes duplicate pitch classes.

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([
                ...     [5, 12, 14, 18, 17],
                ...     [16, 17, 19],
                ...     ])

            ::

                >>> for segment in segments.remove_duplicate_pitch_classes():
                ...     segment
                ...
                PitchSegment([5, 12, 14, 18])
                PitchSegment([16, 19])

        Returns new segment list.
        '''
        pitch_class_class = self._get_pitch_class_class()
        known_pitch_classes = []
        segments_ = []
        for segment in self:
            items = []
            for item in segment:
                pitch_class = pitch_class_class(item)
                if pitch_class in known_pitch_classes:
                    continue
                known_pitch_classes.append(pitch_class)
                items.append(item)
            if items:
                segment_ = self._initialize_segment(items)
                segments_.append(segment_)
        return abjad.new(self, segments=segments_)

    def remove_duplicates(self, level=-1):
        r'''Removes duplicates.

        ..  container:: example

            At level 0:

            ::

                >>> segments = baca.SegmentList([
                ...     [5, 12, 14, 17, 18, 17],
                ...     [16, 17, 19, 17],
                ...     [16, 17, 19, 17],
                ...     ])

            ::

                >>> segments.remove_duplicates(level=0)
                SegmentList([<5, 12, 14, 17, 18, 17>, <16, 17, 19, 17>])

        ..  container:: example

            At level 1:

            ::

                >>> segments = baca.SegmentList([
                ...     [5, 12, 14, 17, 18, 17],
                ...     [16, 17, 19, 17],
                ...     [16, 17, 19, 17],
                ...     ])

            ::

                >>> segments.remove_duplicates(level=1)
                SegmentList([<5, 12, 14, 17, 18>, <16, 17, 19>, <16, 17, 19>])

        ..  container:: example

            At level -1:

            ::

                >>> segments = baca.SegmentList([
                ...     [5, 12, 14, 17, 18, 17],
                ...     [16, 17, 19, 17],
                ...     [16, 17, 19, 17],
                ...     ])

            ::

                >>> segments.remove_duplicates()
                SegmentList([<5, 12, 14, 17, 18>, <16, 19>])

        Returns new segment list.
        '''
        segments_ = []
        if level == 0:
            segments_, known_items = [], []
            for segment in self:
                if segment in known_items:
                    continue
                known_items.append(segment)
                segments_.append(segment)
        elif level == 1:
            for segment in self:
                items, known_items = [], []
                for item in segment:
                    if item in known_items:
                        continue
                    known_items.append(item)
                    items.append(item)
                if items:
                    segment_ = self._initialize_segment(items)
                    segments_.append(segment_)
        elif level == -1:
            known_items = []
            for segment in self:
                items = []
                for item in segment:
                    if item in known_items:
                        continue
                    known_items.append(item)
                    items.append(item)
                if items:
                    segment_ = self._initialize_segment(items)
                    segments_.append(segment_)
        else:
            message = 'level must be 0, 1 or -1: {!r}.'
            message = message.format(level)
            raise ValueError(message)
        return abjad.new(self, segments=segments_)

    def to_pitch_classes(self):
        r'''Changes to pitch-class segments.

        ..  container:: example

            To numbered pitch-class segments:

            ..  container:: example

                ::

                    >>> segments = baca.SegmentList(
                    ...     [[12, 14, 18, 17], [16, 20, 19]],
                    ...     item_class=abjad.NumberedPitch,
                    ...     )

                ::

                    >>> segments.to_pitch_classes()
                    SegmentList([PC<0, 2, 6, 5>, PC<4, 8, 7>])

            ..  container:: example

                ::

                    >>> segments = baca.SegmentList(
                    ...     [[0, 2, 6, 5], [4, 8, 7]],
                    ...     item_class=abjad.NumberedPitchClass,
                    ...     )

                ::

                    >>> segments.to_pitch_classes()
                    SegmentList([PC<0, 2, 6, 5>, PC<4, 8, 7>])

        ..  container:: example

            To named pitch-class segments:

            ..  container:: example

                ::

                    >>> segments = baca.SegmentList(
                    ...     [[12, 14, 18, 17], [16, 20, 19]],
                    ...     item_class=abjad.NamedPitch,
                    ...     )

                ::

                    >>> segments.to_pitch_classes()
                    SegmentList([PC<c d fs f>, PC<e af g>])

            ..  container:: example

                ::

                    >>> segments = baca.SegmentList(
                    ...     [[0, 2, 6, 5], [4, 8, 7]],
                    ...     item_class=abjad.NamedPitchClass,
                    ...     )

                ::

                    >>> segments.to_pitch_classes()
                    SegmentList([PC<c d fs f>, PC<e af g>])

        Returns new segment list.
        '''
        item_class = self._to_pitch_class_item_class(self.item_class)
        segments_ = []
        for segment in self:
            segment_ = segment.to_pitch_classes()
            segments_.append(segment_)
        return type(self)(segments=segments_, item_class=item_class)

    def to_pitches(self):
        r'''Changes to pitch segments.

        ..  container:: example

            To numbered pitch segments:

            ..  container:: example

                ::

                    >>> segments = baca.SegmentList(
                    ...     [[12, 14, 18, 17], [16, 20, 19]],
                    ...     item_class=abjad.NumberedPitch,
                    ...     )

                ::

                    >>> segments.to_pitches()
                    SegmentList([<12, 14, 18, 17>, <16, 20, 19>])

            ..  container:: example

                ::

                    >>> segments = baca.SegmentList(
                    ...     [[0, 2, 6, 5], [4, 8, 7]],
                    ...     item_class=abjad.NumberedPitchClass,
                    ...     )

                ::

                    >>> segments.to_pitches()
                    SegmentList([<0, 2, 6, 5>, <4, 8, 7>])

        ..  container:: example

            To named pitch segments:

            ..  container:: example

                ::

                    >>> segments = baca.SegmentList(
                    ...     [[12, 14, 18, 17], [16, 20, 19]],
                    ...     item_class=abjad.NamedPitch,
                    ...     )

                ::

                    >>> segments.to_pitches()
                    SegmentList([<c'' d'' fs'' f''>, <e'' af'' g''>])

            ..  container:: example

                ::

                    >>> segments = baca.SegmentList(
                    ...     [[0, 2, 6, 5], [4, 8, 7]],
                    ...     item_class=abjad.NamedPitchClass,
                    ...     )

                ::

                    >>> segments.to_pitches()
                    SegmentList([<c' d' fs' f'>, <e' af' g'>])

        Returns new segment list.
        '''
        item_class = self._to_pitch_item_class(self.item_class)
        segments_ = []
        for segment in self:
            segment_ = segment.to_pitches()
            segments_.append(segment_)
        return type(self)(segments=segments_, item_class=item_class)


collections.Sequence.register(SegmentList)
