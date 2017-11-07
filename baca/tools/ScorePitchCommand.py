import abjad
import collections
import functools
from .Command import Command


# TODO: write comprehensive tests
class ScorePitchCommand(Command):
    r'''Score pitch command.

    ..  container:: example

        With pitch numbers:

        >>> segment_maker = baca.SegmentMaker(
        ...     score_template=baca.ViolinSoloScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> segment_maker(
        ...     baca.scope('Violin Music Voice', 1),
        ...     baca.even_runs(),
        ...     baca.pitches([19, 13, 15, 16, 17, 23]),
        ...     )

        >>> result = segment_maker.run(is_doc_example=True)
        >>> lilypond_file, metadata = result
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context GlobalContext = "Global Context" <<
                    \context GlobalRests = "Global Rests" {
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                    }
                    \context GlobalSkips = "Global Skips" {
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
                                g''8 [
                                cs''8
                                ef''8
                                e''8 ]
                            }
                            {
                                f''8 [
                                b''8
                                g''8 ]
                            }
                            {
                                cs''8 [
                                ef''8
                                e''8
                                f''8 ]
                            }
                            {
                                b''8 [
                                g''8
                                cs''8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        With pitch numbers:

        >>> segment_maker = baca.SegmentMaker(
        ...     score_template=baca.ViolinSoloScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> segment_maker(
        ...     baca.scope('Violin Music Voice', 1),
        ...     baca.even_runs(),
        ...     baca.pitches('C4 F4 F#4 <B4 C#5> D5'), 
        ...     )

        >>> result = segment_maker.run(is_doc_example=True)
        >>> lilypond_file, metadata = result
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context GlobalContext = "Global Context" <<
                    \context GlobalRests = "Global Rests" {
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                    }
                    \context GlobalSkips = "Global Skips" {
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
                                c'8 [
                                f'8
                                fs'8
                                <b' cs''>8 ]
                            }
                            {
                                d''8 [
                                c'8
                                f'8 ]
                            }
                            {
                                fs'8 [
                                <b' cs''>8
                                d''8
                                c'8 ]
                            }
                            {
                                f'8 [
                                fs'8
                                <b' cs''>8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Large chord:

        >>> segment_maker = baca.SegmentMaker(
        ...     score_template=baca.ViolinSoloScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> segment_maker(
        ...     baca.scope('Violin Music Voice', 1),
        ...     baca.even_runs(),
        ...     baca.pitches('<C4 D4 E4 F4 G4 A4 B4 C4>'),
        ...     )

        >>> result = segment_maker.run(is_doc_example=True)
        >>> lilypond_file, metadata = result
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
                \context GlobalContext = "Global Context" <<
                    \context GlobalRests = "Global Rests" {
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                    }
                    \context GlobalSkips = "Global Skips" {
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
                                <c' d' e' f' g' a' b'>8 [
                                <c' d' e' f' g' a' b'>8
                                <c' d' e' f' g' a' b'>8
                                <c' d' e' f' g' a' b'>8 ]
                            }
                            {
                                <c' d' e' f' g' a' b'>8 [
                                <c' d' e' f' g' a' b'>8
                                <c' d' e' f' g' a' b'>8 ]
                            }
                            {
                                <c' d' e' f' g' a' b'>8 [
                                <c' d' e' f' g' a' b'>8
                                <c' d' e' f' g' a' b'>8
                                <c' d' e' f' g' a' b'>8 ]
                            }
                            {
                                <c' d' e' f' g' a' b'>8 [
                                <c' d' e' f' g' a' b'>8
                                <c' d' e' f' g' a' b'>8 ]
                                \bar "|"
                            }
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_acyclic',
        '_allow_repeat_pitches',
        '_counts',
        '_repetition_intervals',
        '_source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        acyclic=None,
        allow_repeat_pitches=None,
        counts=None,
        repetition_intervals=None,
        selector=None,
        source=None,
        ):
        Command.__init__(self, selector=selector)
        if acyclic is not None:
            acyclic = bool(acyclic)
        self._acyclic = acyclic
        if allow_repeat_pitches is not None:
            allow_repeat_pitches = bool(allow_repeat_pitches)
        self._allow_repeat_pitches = allow_repeat_pitches
        if counts is not None:
            assert abjad.mathtools.all_are_positive_integers(counts)
        self._counts = counts
        self._repetition_intervals = repetition_intervals
        if source is not None:
            if isinstance(source, str):
                source = self._parse_string(source)
            source = self._coerce_source(source)
            source = abjad.CyclicTuple(source)
        self._source = source

    ### SPECIAL METHODS ###

    # TODO: write comprehensive tests
    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        ..  note:: Write comprehensive tests.

        ..  container:: example

            Calls command on Abjad container:

            >>> command = baca.ScorePitchCommand(
            ...     source=[19, 13, 15, 16, 17, 23],
            ...     )

            >>> staff = abjad.Staff("c'8 c' c' c' c' c' c' c'")
            >>> command(staff)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff {
                    g''8
                    cs''8
                    ef''8
                    e''8
                    f''8
                    b''8
                    g''8
                    cs''8
                }

        Returns none.
        '''
        if argument is None:
            return
        pleaves = []
        for pleaf in abjad.select(argument).leaves(pitched=True):
            if abjad.inspect(pleaf).get_logical_tie().head is pleaf:
                pleaves.append(pleaf)
        pleaves = abjad.select(pleaves)
        pleaves = self._sort_by_timeline(pleaves)
        plts = []
        for pleaf in pleaves:
            plt = abjad.inspect(pleaf).get_logical_tie()
            if plt.head is pleaf:
                plts.append(plt)
        counts = self.counts or [1]
        counts = abjad.CyclicTuple(counts)
        start_index = 0
        source_length = len(self.source)
        logical_tie_count = len(plts)
        if self.acyclic and source_length < logical_tie_count:
            message = f'only {source_length} pitches'
            message += f' for {logical_tie_count} logical ties:'
            message += f' {self!r} and {plts!r}.'
            raise Exception(message)
        absolute_start_index = start_index
        source = self.source
        current_count_index = 0
        current_count = counts[current_count_index]
        current_logical_tie_index = 0
        source_length = len(self.source)
        for plt in plts:
            index = absolute_start_index + current_logical_tie_index
            pitch_expression = source[index]
            repetition_count = index // len(self.source)
            if (self.repetition_intervals is not None and
                0 < repetition_count):
                repetition_intervals = abjad.CyclicTuple(
                    self.repetition_intervals)
                repetition_intervals = repetition_intervals[:repetition_count]
                repetition_interval = sum(repetition_intervals)
                if isinstance(repetition_interval, int):
                    pitch_number = pitch_expression.number
                    pitch_number += repetition_interval
                    pitch_expression = type(pitch_expression)(pitch_number)
                else:
                    message = 'named repetition intervals not implemented.'
                    raise NotImplementedError(message)

#            if isinstance(pitch_expression, abjad.Pitch):
#                if self._use_exact_spelling:
#                    pitch = pitch_expression
#                    assert isinstance(pitch, abjad.NamedPitch)
#                else:
#                    pitch_expression = abjad.NumberedPitch(
#                        pitch_expression)
#                    pitch = abjad.NamedPitch(pitch_expression)
#            elif isinstance(pitch_expression, (abjad.Segment, abjad.Set)):
#                pitch = pitch_expression
#            else:
#                raise Exception(f'pitch or segment: {pitch_expression!r}.')

            pitch = pitch_expression
            
            allow_repeat_pitches = self.allow_repeat_pitches
            for pleaf in plt:
                if isinstance(pitch, abjad.Pitch):
                    self._set_pitch(pleaf, pitch, allow_repeat_pitches)
                elif isinstance(pitch, collections.Iterable):
                    chord = abjad.Chord(pitch, pleaf.written_duration)
                    # TODO: *overrides* and *indicators* are lost!
                    abjad.mutate(pleaf).replace(chord)
                else:
                    raise Exception(f'pitch or segment: {pitch!r}.')

            current_count -= 1
            if current_count == 0:
                current_logical_tie_index += 1
                current_count_index += 1
                current_count = counts[current_count_index]

    ### PRIVATE METHODS ###

    @staticmethod
    def _coerce_source(source):
        items = []
        for item in source:
            if isinstance(item, str) and '<' in item and '>' in item:
                item = item.strip('<')
                item = item.strip('>')
                item = abjad.PitchSet(item, abjad.NamedPitch)
            elif isinstance(item, str):
                item = abjad.NamedPitch(item)
            elif isinstance(item, collections.Iterable):
                item = abjad.PitchSet(item, abjad.NamedPitch)
            else:
                item = abjad.NamedPitch(item)
            items.append(item)
        return items

    def _mutates_score(self):
        source = self.source or []
        return any(isinstance(_, collections.Iterable) for _ in source)

    @staticmethod
    def _parse_string(string):
        items, current_chord = [], []
        for part in string.split():
            if '<' in part:
                assert not current_chord
                current_chord.append(part)
            elif '>' in part:
                assert current_chord
                current_chord.append(part)
                item = ' '.join(current_chord)
                items.append(item)
                current_chord = []
            elif current_chord:
                current_chord.append(part)
            else:
                items.append(part)
        assert not current_chord, repr(current_chord)
        return items

    @staticmethod
    def _set_pitch(leaf, pitch, allow_repeat_pitches=None):
        string = 'not yet pitched'
        if abjad.inspect(leaf).has_indicator(string):
            abjad.detach(string, leaf)
        if isinstance(leaf, abjad.Note):
            leaf.written_pitch = pitch
        elif isinstance(leaf, abjad.Chord):
            raise NotImplementedError
        if allow_repeat_pitches:
            abjad.attach('repeat pitch allowed', leaf)

    @staticmethod
    def _sort_by_timeline(leaves):
        assert leaves.are_leaves(), repr(leaves)
        def compare(leaf_1, leaf_2):
            start_offset_1 = abjad.inspect(leaf_1).get_timespan().start_offset
            start_offset_2 = abjad.inspect(leaf_2).get_timespan().start_offset
            if start_offset_1 < start_offset_2:
                return -1
            if start_offset_2 < start_offset_1:
                return 1
            index_1 = abjad.inspect(leaf_1).get_parentage().score_index
            index_2 = abjad.inspect(leaf_2).get_parentage().score_index
            if index_1 < index_2:
                return -1
            if index_2 < index_1:
                return 1
            return 0
        leaves = list(leaves)
        leaves.sort(key=functools.cmp_to_key(compare))
        return abjad.select(leaves)

    ### PUBLIC PROPERTIES ###

    @property
    def acyclic(self):
        r'''Is true when command reads pitches once only.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._acyclic

    @property
    def allow_repeat_pitches(self):
        r'''Is true when command allows repeat pitches.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._allow_repeat_pitches

    @property
    def counts(self):
        r'''Gets counts.

        Defaults to none.

        Set to positive integers or none.

        Returns positive integers or none.
        '''
        return self._counts

    @property
    def repetition_intervals(self):
        r'''Gets repetition intervals.


        ..  container:: example

            With no repetition intervals:

            >>> command = baca.ScorePitchCommand(
            ...     source=[0, 1, 2, 3],
            ...     )

            >>> command.repetition_intervals is None
            True

            >>> for index in range(12):
            ...     pitch = command.get_pitch(index)
            ...     pitch.number
            0
            1
            2
            3
            0
            1
            2
            3
            0
            1
            2
            3

        ..  container:: example

            With fixed repetition interval:

            >>> command = baca.ScorePitchCommand(
            ...     repetition_intervals=[12],
            ...     source=[0, 1, 2, 3],
            ...     )

            >>> command.repetition_intervals
            [12]

            >>> for index in range(12):
            ...     pitch = command.get_pitch(index)
            ...     pitch.number
            0
            1
            2
            3
            12
            13
            14
            15
            24
            25
            26
            27

        ..  container:: example

            With patterned repetition intervals:

            >>> command = baca.ScorePitchCommand(
            ...     repetition_intervals=[12, 1],
            ...     source=[0, 1, 2, 3],
            ...     )

            >>> command.repetition_intervals
            [12, 1]

            >>> for index in range(12):
            ...     pitch = command.get_pitch(index)
            ...     pitch.number
            0
            1
            2
            3
            12
            13
            14
            15
            13
            14
            15
            16

        Defaults to none.

        Set to intervals or none.

        Returns intervals or none.
        '''
        return self._repetition_intervals

    @property
    def source(self):
        r'''Gets source.

        ..  container:: example

            Gets source:

            >>> command = baca.ScorePitchCommand(
            ...     source=[19, 13, 15, 16, 17, 23],
            ...     )

            >>> for pitch in command.source:
            ...     pitch
            NamedPitch("g''")
            NamedPitch("cs''")
            NamedPitch("ef''")
            NamedPitch("e''")
            NamedPitch("f''")
            NamedPitch("b''")

        Defaults to none.

        Set to pitch source or none.

        Returns pitch source or none.
        '''
        return self._source

    ### PUBLIC METHODS ###

    def get_pitch(self, index):
        r'''Gets pitch at `index`.

        ..  container:: example

            Gets pitches:

            >>> command = baca.ScorePitchCommand(
            ...     source=[12, 13, 14, 15]
            ...     )

            >>> for index in range(12):
            ...     command.get_pitch(index)
            ...
            NamedPitch("c''")
            NamedPitch("cs''")
            NamedPitch("d''")
            NamedPitch("ef''")
            NamedPitch("c''")
            NamedPitch("cs''")
            NamedPitch("d''")
            NamedPitch("ef''")
            NamedPitch("c''")
            NamedPitch("cs''")
            NamedPitch("d''")
            NamedPitch("ef''")

        Returns pitch.
        '''
        if not self.source:
            message = 'no source pitches.'
            raise Exception(message)
        if self.acyclic:
            source = list(self.source)
        else:
            source = abjad.CyclicTuple(self.source)
        start_index = 0
        index += start_index
        pitch_expression = source[index]
        repetition_count = index // len(self.source)
        if self.repetition_intervals is not None and 0 < repetition_count:
            repetition_intervals = abjad.CyclicTuple(
                self.repetition_intervals)
            repetition_intervals = repetition_intervals[:repetition_count]
            repetition_interval = sum(repetition_intervals)
            if isinstance(repetition_interval, int):
                pitch_number = pitch_expression.number
                pitch_number += repetition_interval
                pitch_expression = type(pitch_expression)(pitch_number)
            else:
                message = 'named repetition intervals not yet implemented.'
                raise NotImplementedError(message)
        return pitch_expression
