# -*- coding: utf-8 -*-
import abjad
import baca


class ChordalSpacingSpecifier(abjad.abctools.AbjadValueObject):
    r'''Chordal spacing specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> specifier = baca.tools.ChordalSpacingSpecifier(
            ...     bass=6,
            ...     soprano=7,
            ...     )
            >>> specifier([[-6, -3, -5, -1, -7]])
            CollectionList([<6, 9, 11, 17, 19>])

    ..  container:: example

        ::

            >>> specifier = baca.tools.ChordalSpacingSpecifier(
            ...     bass=6,
            ...     direction=Down,
            ...     soprano=7,
            ...     )
            >>> specifier([[-6, -3, -5, -1, -7]])
            CollectionList([<19, 17, 11, 9, 6>])

    ..  container:: example

        ::

            >>> specifier = baca.tools.ChordalSpacingSpecifier(
            ...     bass=11,
            ...     direction=Down,
            ...     soprano=7,
            ...     )
            >>> specifier([[-6, -3, -5, -1, -7]])
            CollectionList([<31, 30, 29, 21, 11>])

    ..  container:: example

        ::

            >>> specifier = baca.tools.ChordalSpacingSpecifier()
            >>> specifier([[0, 1, 2]])
            CollectionList([<0, 1, 2>])

        ::

            >>> specifier([[0, 2, 1]])
            CollectionList([<0, 1, 2>])

        ::

            >>> specifier([[1, 0, 2]])
            CollectionList([<1, 2, 12>])

        ::

            >>> specifier([[1, 2, 0]])
            CollectionList([<1, 2, 12>])

        ::

            >>> specifier([[2, 0, 1]])
            CollectionList([<2, 12, 13>])

        ::

            >>> specifier([[2, 1, 0]])
            CollectionList([<2, 12, 13>])

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_bass',
        '_direction',
        '_minimum_semitones',
        '_pattern',
        '_soprano',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        bass=None,
        direction=None,
        minimum_semitones=None,
        pattern=None,
        soprano=None,
        ):
        self._bass = bass
        if direction is not None:
            assert direction in (Up, Down)
        self._direction = direction
        if minimum_semitones is not None:
            assert isinstance(minimum_semitones, int)
            assert 1 <= minimum_semitones
        self._minimum_semitones = minimum_semitones
        if pattern is not None:
            assert isinstance(pattern, abjad.Pattern)
        self._pattern = pattern
        self._soprano = soprano

    ### SPECIAL METHODS ###

    def __call__(self, collections=None):
        r'''Calls specifier on `collections`.

        ..  container:: example

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier()
                >>> specifier([])
                PitchSegment([])

        ..  container:: example

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier()
                >>> specifier() is None
                True

        Returns pitch collection or none.
        '''
        if collections is None:
            return
        if collections == []:
            return baca.PitchSegment(item_class=abjad.NumberedPitch)
        if not isinstance(collections, baca.CollectionList):
            collections = baca.CollectionList(collections)
        pitch_class_segments = collections.to_pitch_classes()
        pattern = self.pattern or abjad.patterntools.select_all()
        collections_ = []
        total_length = len(collections)
        for i in range(total_length):
            if not pattern.matches_index(i, total_length):
                collections_.append(collections[i])
            else:
                pitch_class_segment = pitch_class_segments[i]
                segment_ = self._space_segment(pitch_class_segment)
                collections_.append(segment_)
        return baca.CollectionList(collections_)

    ### PRIVATE METHODS ###

    def _sort_pitch_classes_ascending(self, start, pitch_classes):
        pitch_classes, pitch_classes_, iterations = pitch_classes[:], [], 0
        if self.minimum_semitones is not None:
            candidate = start + self.minimum_semitones
        else:
            candidate = start + 1
        while pitch_classes:
            if candidate in pitch_classes:
                pitch_classes_.append(candidate)
                pitch_classes.remove(candidate)
                if self.minimum_semitones is not None:
                    candidate += self.minimum_semitones
            else:
                candidate += 1
            if 999 <= iterations:
                message = 'stuck in while-loop.'
                raise Exception(message)
            iterations += 1
        assert not pitch_classes, repr(pitch_classes)
        return pitch_classes_

    def _sort_pitch_classes_descending(self, start, pitch_classes):
        pitch_classes, pitch_classes_, iterations = pitch_classes[:], [], 0
        if self.minimum_semitones is not None:
            candidate = abjad.NumberedPitchClass(
                start.number - self.minimum_semitones
                )
        else:
            candidate = abjad.NumberedPitchClass(start.number - 1)
        while pitch_classes:
            if candidate in pitch_classes:
                pitch_classes_.append(candidate)
                pitch_classes.remove(candidate)
                if self.minimum_semitones is not None:
                    candidate = abjad.NumberedPitchClass(
                        candidate.number - self.minimum_semitones
                        )
            else:
                candidate = abjad.NumberedPitchClass(candidate.number - 1)
            if 999 <= iterations:
                message = 'stuck in while-loop.'
                raise Exception(message)
            iterations += 1
        assert not pitch_classes, repr(pitch_classes)
        return pitch_classes_

    def _space_segment(self, pitch_class_segment):
        original_input = pitch_class_segment
        pitch_classes = list(pitch_class_segment)
        bass, soprano = None, None
        if self.bass is not None:
            bass = abjad.NumberedPitchClass(self.bass)
            if bass not in pitch_classes:
                message = 'bass pitch-class {} not found in {}.'
                message = message.format(bass, pitch_classes)
                raise ValueError(message)
        if self.soprano is not None:
            soprano = abjad.NumberedPitchClass(self.soprano)
            if soprano not in pitch_classes:
                message = 'soprano pitch-class {} not found in {}.'
                message = message.format(soprano, pitch_classes)
                raise ValueError(message)
        inner = []
        for pitch_class in pitch_classes:
            if pitch_class not in (bass, soprano):
                inner.append(pitch_class)
        pitch_classes = []
        pitches = []
        direction = self.direction or Up
        if direction is Up:
            if bass is not None:
                pitch_classes.append(bass)
            elif inner:
                pitch_classes.append(inner.pop(0))
            elif soprano:
                pitch_classes.append(soprano)
                soprano = None
            start = pitch_classes[0]
            inner = self._sort_pitch_classes_ascending(start, inner)
            pitch_classes.extend(inner)
            if soprano:
                pitch_classes.append(soprano)
            pitches = self._to_tightly_spaced_pitches_ascending(pitch_classes)
        else:
            if soprano is not None:
                pitch_classes.append(soprano)
            elif inner:
                pitch_classes.append(inner.pop(0))
            elif bass:
                pitch_classes.append(bass)
                bass = None
            start = pitch_classes[0]
            inner = self._sort_pitch_classes_descending(start, inner)
            pitch_classes.extend(inner)
            if bass:
                pitch_classes.append(bass)
            pitches = self._to_tightly_spaced_pitches_descending(pitch_classes)
        if isinstance(original_input, abjad.pitchtools.Set):
            return baca.PitchSet(pitches)
        else:
            return baca.PitchSegment(pitches)

    @staticmethod
    def _to_tightly_spaced_pitches_ascending(pitch_classes):
        pitches = []
        pitch_class = pitch_classes[0]
        pitch = abjad.NumberedPitch.from_pitch_class_octave(pitch_class, 4)
        pitches.append(pitch)
        for pitch_class in pitch_classes[1:]:
            candidate_octave = pitches[-1].octave.number
            candidate = abjad.NumberedPitch.from_pitch_class_octave(
                pitch_class,
                candidate_octave,
                )
            if pitches[-1] <= candidate:
                pitches.append(candidate)
            else:
                octave = candidate_octave + 1
                pitch = abjad.NumberedPitch.from_pitch_class_octave(
                    pitch_class,
                    octave,
                    )
                assert pitches[-1] <= pitch
                pitches.append(pitch)
        return pitches

    @staticmethod
    def _to_tightly_spaced_pitches_descending(pitch_classes):
        pitches = []
        pitch_class = pitch_classes[0]
        pitch = abjad.NumberedPitch.from_pitch_class_octave(pitch_class, 4)
        pitches.append(pitch)
        for pitch_class in pitch_classes[1:]:
            candidate_octave = pitches[-1].octave.number
            candidate = abjad.NumberedPitch.from_pitch_class_octave(
                pitch_class,
                candidate_octave,
                )
            if candidate <= pitches[-1]:
                pitches.append(candidate)
            else:
                octave = candidate_octave - 1
                pitch = abjad.NumberedPitch.from_pitch_class_octave(
                    pitch_class,
                    octave,
                    )
                assert pitch <= pitches[-1]
                pitches.append(pitch)
        collection = baca.PitchSegment(pitches)
        while collection[-1].octave.number < 4:
            collection = collection.transpose(n=12)
        return collection
    
    ### PUBLIC PROPERTIES ###

    @property
    def bass(self):
        r'''Gets bass.

        ..  container:: example

            Up-directed bass specification:

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     bass=None,
                ...     )
                >>> specifier([[-6, -3, -5, -1, -7]])
                CollectionList([<6, 7, 9, 11, 17>])

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     bass=6,
                ...     )
                >>> specifier([[-6, -3, -5, -1, -7]])
                CollectionList([<6, 7, 9, 11, 17>])

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     bass=7,
                ...     )
                >>> specifier([[-6, -3, -5, -1, -7]])
                CollectionList([<7, 9, 11, 17, 18>])

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     bass=9,
                ...     )
                >>> specifier([[-6, -3, -5, -1, -7]])
                CollectionList([<9, 11, 17, 18, 19>])

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     bass=11,
                ...     )
                >>> specifier([[-6, -3, -5, -1, -7]])
                CollectionList([<11, 17, 18, 19, 21>])

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     bass=5,
                ...     )
                >>> specifier([[-6, -3, -5, -1, -7]])
                CollectionList([<5, 6, 7, 9, 11>])

        Returns pitch-class or none.
        '''
        return self._bass

    @property
    def direction(self):
        r'''Gets direction.

        ..  container:: example

            Up-directed joint control:

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     bass=6,
                ...     soprano=7,
                ...     )
                >>> specifier([[-6, -3, -5, -1, -7]])
                CollectionList([<6, 9, 11, 17, 19>])

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     bass=6,
                ...     soprano=9,
                ...     )
                >>> specifier([[-6, -3, -5, -1, -7]])
                CollectionList([<6, 7, 11, 17, 21>])

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     bass=6,
                ...     soprano=11,
                ...     )
                >>> specifier([[-6, -3, -5, -1, -7]])
                CollectionList([<6, 7, 9, 17, 23>])

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     bass=6,
                ...     soprano=5
                ...     )
                >>> specifier([[-6, -3, -5, -1, -7]])
                CollectionList([<6, 7, 9, 11, 17>])

        Returns up, down or none.
        '''
        return self._direction

    @property
    def minimum_semitones(self):
        r'''Gets minimum semitones.

        ..  container:: example

            Up-directed spacing with semitone constraints.

            First three examples give the same spacing:

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     bass=6,
                ...     soprano=7,
                ...     )
                >>> specifier([[5, 6, 7, 9, 11]])
                CollectionList([<6, 9, 11, 17, 19>])

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     bass=6,
                ...     minimum_semitones=1,
                ...     soprano=7,
                ...     )
                >>> specifier([[5, 6, 7, 9, 11]])
                CollectionList([<6, 9, 11, 17, 19>])

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     bass=6,
                ...     minimum_semitones=2,
                ...     soprano=7,
                ...     )
                >>> specifier([[5, 6, 7, 9, 11]])
                CollectionList([<6, 9, 11, 17, 19>])

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     bass=6,
                ...     minimum_semitones=3,
                ...     soprano=7,
                ...     )
                >>> specifier([[5, 6, 7, 9, 11]])
                CollectionList([<6, 9, 17, 23, 31>])

        ..  container:: example

            Down-directed spacing with semitone constraints.

            First three examples give the same spacing:

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     bass=6,
                ...     direction=Down,
                ...     soprano=7,
                ...     )
                >>> specifier([[5, 6, 7, 9, 11]])
                CollectionList([<19, 17, 11, 9, 6>])

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     bass=6,
                ...     direction=Down,
                ...     minimum_semitones=1,
                ...     soprano=7,
                ...     )
                >>> specifier([[5, 6, 7, 9, 11]])
                CollectionList([<19, 17, 11, 9, 6>])

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     bass=6,
                ...     direction=Down,
                ...     minimum_semitones=2,
                ...     soprano=7,
                ...     )
                >>> specifier([[5, 6, 7, 9, 11]])
                CollectionList([<19, 17, 11, 9, 6>])

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     bass=6,
                ...     direction=Down,
                ...     minimum_semitones=3,
                ...     soprano=7,
                ...     )
                >>> specifier([[5, 6, 7, 9, 11]])
                CollectionList([<31, 23, 17, 9, 6>])

        Set to positive integer or none.

        Returns positive integer or none.
        '''
        return self._minimum_semitones

    @property
    def pattern(self):
        r'''Gets pattern.

        Set to pattern or none.

        Returns pattern or none.
        '''
        return self._pattern

    @property
    def soprano(self):
        r'''Gets soprano.

        ..  container:: example

            Down-directed soprano control:

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     direction=Down,
                ...     soprano=None,
                ...     )
                >>> specifier([[-6, -3, -5, -1, -7]])
                CollectionList([<18, 17, 11, 9, 7>])

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     direction=Down,
                ...     soprano=6,
                ...     )
                >>> specifier([[-6, -3, -5, -1, -7]])
                CollectionList([<18, 17, 11, 9, 7>])

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     direction=Down,
                ...     soprano=5,
                ...     )
                >>> specifier([[-6, -3, -5, -1, -7]])
                CollectionList([<17, 11, 9, 7, 6>])

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     direction=Down,
                ...     soprano=11,
                ...     )
                >>> specifier([[-6, -3, -5, -1, -7]])
                CollectionList([<11, 9, 7, 6, 5>])

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     direction=Down,
                ...     soprano=9,
                ...     )
                >>> specifier([[-6, -3, -5, -1, -7]])
                CollectionList([<21, 19, 18, 17, 11>])

            ::

                >>> specifier = baca.tools.ChordalSpacingSpecifier(
                ...     direction=Down,
                ...     soprano=7,
                ...     )
                >>> specifier([[-6, -3, -5, -1, -7]])
                CollectionList([<19, 18, 17, 11, 9>])

        Returns pitch-class or none.
        '''
        return self._soprano
