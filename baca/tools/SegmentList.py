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
        r'''Is true when segments interpret as chords.

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

    def accumulate(self, operands=None):
        r'''Accumulates `operands` against segments to identity.

        ..  container:: example

            Accumulates transposition:

            ::

                >>> segments = baca.SegmentList(
                ...     [[0, 2, 6, 5], [4, 8, 7]],
                ...     item_class=abjad.NumberedPitchClass,
                ...     )

            ::

                >>> transposition = baca.pitch_class_segment().transpose(n=3)
                >>> for segment in segments.accumulate([transposition]):
                ...     segment
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

                >>> segments = baca.SegmentList(
                ...     [[0, 2, 6, 5], [4, 8, 7]],
                ...     item_class=abjad.NumberedPitchClass,
                ...     )

            ::

                >>> transposition = baca.pitch_class_segment().transpose(n=3)
                >>> alpha = baca.pitch_class_segment().alpha()
                >>> operands = [transposition, alpha]
                >>> for segment in segments.accumulate(operands):
                ...     segment
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

        Returns new segment list.
        '''
        sequence = baca.Sequence(items=self)
        segments = []
        for sequence_ in sequence.accumulate(operands=operands):
            segments.extend(sequence_)
        return type(self)(segments=segments)

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

    def has_duplicate_pitch_classes(self, level=-1):
        r'''Is true when segments have duplicate pitch-classes at `level`.

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([[4, 5, 7], [15, 16, 17, 19]])

            ::

                >>> segments.has_duplicate_pitch_classes(level=1)
                False

            ::

                >>> segments.has_duplicate_pitch_classes(level=-1)
                True

        Set `level` to 1 or -1.

        Returns true or false.
        '''
        pitch_class_class = self._get_pitch_class_class()
        if level == 1:
            for segment in self:
                known_pitch_classes = []
                for item in segment:
                    pitch_class = pitch_class_class(item)
                    if pitch_class in known_pitch_classes:
                        return True
                    known_pitch_classes.append(pitch_class)
        elif level == -1:
            known_pitch_classes = []
            for segment in self:
                for item in segment:
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
        r'''Is true when segments have duplicates at `level`.

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([[16, 17], [13], [16, 17]])

            ::

                >>> segments.has_duplicates(level=0)
                True

            ::

                >>> segments.has_duplicates(level=1)
                False

            ::

                >>> segments.has_duplicates(level=-1)
                True

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([[16, 17], [14, 20, 14]])

            ::

                >>> segments.has_duplicates(level=0)
                False

            ::

                >>> segments.has_duplicates(level=1)
                True

            ::

                >>> segments.has_duplicates(level=-1)
                True

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([[16, 17], [14, 20], [14]])

            ::

                >>> segments.has_duplicates(level=0)
                False

            ::

                >>> segments.has_duplicates(level=1)
                False

            ::

                >>> segments.has_duplicates(level=-1)
                True

        Set `level` to 0, 1 or -1.

        Returns true or false.
        '''
        if level == 0:
            known_items = []
            for segment in self:
                if segment in known_items:
                    return True
                known_items.append(segment)
        elif level == 1:
            for segment in self:
                known_items = []
                for item in segment:
                    if item in known_items:
                        return True
                    known_items.append(item)
        elif level == -1:
            known_items = []
            for segment in self:
                items = []
                for item in segment:
                    if item in known_items:
                        return True
                    known_items.append(item)
        else:
            message = 'level must be 0, 1 or -1: {!r}.'
            message = message.format(level)
            raise ValueError(message)
        return False

    def has_repeat_pitch_classes(self, level=-1):
        r'''Is true when segments have repeat pitch-classes as `level`.

        ..  container:: example

                >>> segments = baca.SegmentList([[4, 5, 4, 5], [17, 18]])

            ::

                >>> segments.has_repeat_pitch_classes(level=1)
                False

            ::

                >>> segments.has_repeat_pitch_classes(level=-1)
                True

        Set `level` to 0 or -1.

        Returns true or false.
        '''
        pitch_class_class = self._get_pitch_class_class()
        if level == 1:
            for segment in self:
                previous_pitch_class = None
                for item in segment:
                    pitch_class = pitch_class_class(item)
                    if pitch_class == previous_pitch_class:
                        return True
                    previous_pitch_class = pitch_class
        elif level == -1:
            previous_pitch_class = None
            for segment in self:
                for item in segment:
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
        r'''Is true when segments have repeats at `level`.

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([[4, 5], [4, 5]])

            ::

                >>> segments.has_repeats(level=0)
                True

            ::

                >>> segments.has_repeats(level=1)
                False

            ::

                >>> segments.has_repeats(level=-1)
                False

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([[4, 5], [18, 18], [4, 5]])

            ::

                >>> segments.has_repeats(level=0)
                False

            ::

                >>> segments.has_repeats(level=1)
                True

            ::

                >>> segments.has_repeats(level=-1)
                True

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([[4, 5], [5, 18], [4, 5]])

            ::

                >>> segments.has_repeats(level=0)
                False

            ::

                >>> segments.has_repeats(level=1)
                False

            ::

                >>> segments.has_repeats(level=-1)
                True

        Set `level` to 0, 1 or -1.

        Returns true or false.
        '''
        if level == 0:
            previous_segment = None
            for segment in self:
                if segment == previous_segment:
                    return True
                previous_segment = segment
        elif level == 1:
            for segment in self:
                previous_item = None
                for item in segment:
                    if item == previous_item:
                        return True
                    previous_item = item
        elif level == -1:
            previous_item = None
            for segment in self:
                for item in segment:
                    if item == previous_item:
                        return True
                    previous_item = item
        else:
            message = 'level must be 0, 1 or -1: {!r}.'
            message = message.format(level)
            raise ValueError(message)
        return False

    def helianthate(self, n=0, m=0):
        r'''Helianthates segments.
        
        ..  container:: example

            ::

                >>> segments = baca.SegmentList([[1, 2, 3], [4, 5], [6, 7, 8]])
                >>> for segment in segments.helianthate(n=-1, m=1):
                ...     segment
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

        Returns new segment list.
        '''
        segments = baca.Sequence(items=self)
        segments = segments.helianthate(n=n, m=m)
        return abjad.new(self, segments=segments)


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

    def read(self, counts=None, check=None):
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

        ..  container:: example

            Raises exception on inexact read:

            ::

                >>> segments = baca.SegmentList([
                ...     [5, 12, 14, 18, 17],
                ...     [16, 17, 19],
                ...     ])

            ::

                >>> len(segments.flatten())
                8

            ::

                >>> segments.read([10, 10, 10], check=Exact)
                Traceback (most recent call last):
                    ...
                ValueError: call reads 30 items; not a multiple of 8 items.

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
        result = abjad.new(self, segments=segments)
        if check is Exact:
            self_item_count = len(self.flatten())
            result_item_count = len(result.flatten())
            factors = abjad.mathtools.factors(result_item_count)
            factors.append(result_item_count)
            if self_item_count not in factors:
                message = 'call reads {} items; not a multiple of {} items.'
                message = message.format(result_item_count, self_item_count)
                raise ValueError(message)
        return result

    # TODO: change indices to pattern
    # TODO: add level=-1 keyword
    def remove(self, indices=None):
        r'''Removes segments at `indices`.

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([[0, 1], [2, 3], [4], [5, 6]])
                >>> segments.remove([0, -1])
                SegmentList([<2, 3>, <4>])

        Returns new segment list.
        '''
        sequence = baca.Sequence(items=self)
        segments = sequence.remove(indices=indices)
        return abjad.new(self, segments=segments)
   
    def remove_duplicate_pitch_classes(self, level=-1):
        r'''Removes duplicate pitch-classes at `level`.

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([[4, 5, 7], [16, 17, 16, 18]])

            ::

                >>> segments.remove_duplicate_pitch_classes(level=1)
                SegmentList([<4, 5, 7>, <16, 17, 18>])

            ::

                >>> segments.remove_duplicate_pitch_classes(level=-1)
                SegmentList([<4, 5, 7>, <18>])

        Set `level` to 1 or -1.

        Returns new segment list.
        '''
        pitch_class_class = self._get_pitch_class_class()
        segments_ = []
        if level == 1:
            for segment in self:
                items, known_pitch_classes = [], []
                for item in segment:
                    pitch_class = pitch_class_class(item)
                    if pitch_class in known_pitch_classes:
                        continue
                    known_pitch_classes.append(pitch_class)
                    items.append(item)
                if items:
                    segment_ = self._initialize_segment(items)
                    segments_.append(segment_)
        elif level == -1:
            known_pitch_classes = []
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
        else:
            message = 'level must be 1 or -1: {!r}.'
            message = message.format(level)
            raise ValueError(message)
        return abjad.new(self, segments=segments_)

    def remove_duplicates(self, level=-1):
        r'''Removes duplicates at `level`.

        ..  container:: example

            ::

                >>> segments = baca.SegmentList(
                ...     [[16, 17, 16], [13, 14, 16], [16, 17, 16]],
                ...     )

            ::

                >>> segments.remove_duplicates(level=0)
                SegmentList([<16, 17, 16>, <13, 14, 16>])

            ::

                >>> segments.remove_duplicates(level=1)
                SegmentList([<16, 17>, <13, 14, 16>, <16, 17>])

            ::

                >>> segments.remove_duplicates(level=-1)
                SegmentList([<16, 17>, <13, 14>])

        Set `level` to 0, 1 or -1.

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

    def remove_repeat_pitch_classes(self, level=-1):
        r'''Removes repeat pitch-classes at `level`.

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([[4, 4, 4, 5], [17, 18]])

            ::

                >>> segments.remove_repeat_pitch_classes(level=1)
                SegmentList([<4, 5>, <17, 18>])

            ::

                >>> segments.remove_repeat_pitch_classes(level=-1)
                SegmentList([<4, 5>, <18>])

        Set `level` to 1 or -1.

        Returns new segment list.
        '''
        pitch_class_class = self._get_pitch_class_class()
        segments_ = []
        if level == 1:
            for segment in self:
                items, previous_pitch_class = [], None
                for item in segment:
                    pitch_class = pitch_class_class(item)
                    if pitch_class == previous_pitch_class:
                        continue
                    items.append(item)
                    previous_pitch_class = pitch_class
                if items:
                    segment_ = self._initialize_segment(items)
                    segments_.append(segment_)
        elif level == -1:
            previous_pitch_class = None
            for segment in self:
                items = []
                for item in segment:
                    pitch_class = pitch_class_class(item)
                    if pitch_class == previous_pitch_class:
                        continue
                    items.append(item)
                    previous_pitch_class = pitch_class
                if items:
                    segment_ = self._initialize_segment(items)
                    segments_.append(segment_)
        else:
            message = 'level must be 1 or -1: {!r}.'
            message = message.format(level)
            raise ValueError(message)
        return abjad.new(self, segments=segments_)

    def remove_repeats(self, level=-1):
        r'''Removes repeats at `level`.

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([[4, 5], [4, 5], [5, 7, 7]])

            ::

                >>> segments.remove_repeats(level=0)
                SegmentList([<4, 5>, <5, 7, 7>])

            ::

                >>> segments.remove_repeats(level=1)
                SegmentList([<4, 5>, <4, 5>, <5, 7>])

            ::

                >>> segments.remove_repeats(level=-1)
                SegmentList([<4, 5>, <4, 5>, <7>])

        Set `level` to 0, 1 or -1.

        Returns true or false.
        '''
        segments_ = []
        if level == 0:
            previous_segment = None
            for segment in self:
                if segment == previous_segment:
                    continue
                segments_.append(segment)
                previous_segment = segment
        elif level == 1:
            for segment in self:
                items, previous_item = [], None
                for item in segment:
                    if item == previous_item:
                        continue
                    items.append(item)
                    previous_item = item
                if items:
                    segment_ = self._initialize_segment(items)
                    segments_.append(segment_)
        elif level == -1:
            previous_item = None
            for segment in self:
                items = []
                for item in segment:
                    if item == previous_item:
                        continue
                    items.append(item)
                    previous_item = item
                if items:
                    segment_ = self._initialize_segment(items)
                    segments_.append(segment_)
        else:
            message = 'level must be 0, 1 or -1: {!r}.'
            message = message.format(level)
            raise ValueError(message)
        return abjad.new(self, segments=segments_)

    # TODO: change indices to pattern
    # TODO: add level=-1 keyword
    def retain(self, indices=None):
        r'''Retains segments at `indices`.

        ..  container:: example

            ::

                >>> segments = baca.SegmentList([[0, 1], [2, 3], [4], [5, 6]])
                >>> segments.retain([0, -1])
                SegmentList([<0, 1>, <5, 6>])

        Returns new segment list.
        '''
        sequence = baca.Sequence(items=self)
        segments = sequence.retain(indices=indices)
        return abjad.new(self, segments=segments)

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
