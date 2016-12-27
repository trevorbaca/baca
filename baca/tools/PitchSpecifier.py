# -*- coding: utf-8 -*-
import abjad
import collections


# TODO: write comprehensive tests
class PitchSpecifier(abjad.abctools.AbjadObject):
    r'''Pitch specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        With pitch numbers:

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.tools.stages(1)),
            ...     [
            ...         baca.rhythm.make_even_run_rhythm_specifier(),
            ...         baca.tools.PitchSpecifier(
            ...             source=[19, 13, 15, 16, 17, 23],
            ...             ),
            ...         ],
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[Score])
            \context Score = "Score" <<
                \tag violin
                \context TimeSignatureContext = "Time Signature Context" <<
                    \context TimeSignatureContextMultimeasureRests = "Time Signature Context Multimeasure Rests" {
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
                    \context TimeSignatureContextSkips = "Time Signature Context Skips" {
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
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
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

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_acyclic',
        '_allow_repeated_pitches',
        '_counts',
        '_mutates_score',
        '_operators',
        '_repetition_intervals',
        '_reverse',
        '_source',
        '_start_index',
        '_use_exact_spelling',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        acyclic=None,
        allow_repeated_pitches=None,
        counts=None,
        mutates_score=None,
        operators=None,
        repetition_intervals=None,
        reverse=None,
        source=None,
        start_index=None,
        ):
        if acyclic is not None:
            acyclic = bool(acyclic)
        self._acyclic = acyclic
        if allow_repeated_pitches is not None:
            allow_repeated_pitches = bool(allow_repeated_pitches)
        self._allow_repeated_pitches = allow_repeated_pitches
        if counts is not None:
            assert abjad.mathtools.all_are_positive_integers(counts)
        self._counts = counts
        # because chords sometimes replace notes
        #self._mutates_score = True
        self._mutates_score = mutates_score
        if operators is not None:
            operators = tuple(operators)
        self._operators = operators
        self._repetition_intervals = repetition_intervals
        if reverse is not None:
            reverse = bool(reverse)
        self._reverse = reverse
        if isinstance(source, str):
            self._use_exact_spelling = True
        elif (isinstance(source, collections.Iterable) and 
            isinstance(source[0], abjad.pitchtools.NamedPitch)):
            self._use_exact_spelling = True
        elif (isinstance(source, collections.Iterable) and 
            isinstance(source[0], abjad.pitchtools.Segment)):
            self._use_exact_spelling = True
        elif (isinstance(source, collections.Iterable) and 
            isinstance(source[0], abjad.pitchtools.Set)):
            self._use_exact_spelling = True
        else:
            self._use_exact_spelling = False
        if source is not None:
            if isinstance(source, str):
                source = source.split()
            source_  = []
            for element in source:
                try:
                    element = abjad.pitchtools.NamedPitch(element)
                except ValueError:
                    pass
                source_.append(element)
            source = source_
            source = abjad.datastructuretools.CyclicTuple(source)
        self._source = source
        if start_index is not None:
            assert isinstance(start_index, int), repr(start_index)
        self._start_index = start_index

    ### SPECIAL METHODS ###

    def __call__(self, logical_ties):
        r'''Calls pitch specifier on `logical_ties`.

        ..  todo:: Write comprehensive tests.

        Returns none.
        '''
        if not logical_ties:
            message = '{!r} has no logical ties.'
            message = message.format(self)
            raise Exception(message)
        if not isinstance(logical_ties[0], abjad.selectiontools.LogicalTie):
            logical_ties = list(abjad.iterate(logical_ties).by_logical_tie())
        for logical_tie in logical_ties:
            assert isinstance(logical_tie, abjad.selectiontools.LogicalTie)
        counts = self.counts or [1]
        counts = abjad.datastructuretools.CyclicTuple(counts)
        start_index = self.start_index
        if start_index is None:
            start_index = 0
        if self.source:
            source_length = len(self.source)
            logical_tie_count = len(logical_ties)
            if self.acyclic and source_length < logical_tie_count:
                message = 'only {} pitches for {} logical ties: {!r} and {!r}.'
                message = message.format(
                    source_length, 
                    logical_tie_count, 
                    self,
                    logical_ties,
                    )
                raise Exception(message)
            if 0 <= start_index:
                absolute_start_index = start_index
            else:
                absolute_start_index = source_length - abs(start_index) + 1
            source = self.source
            if self.reverse:
                source = reversed(source)
                source = abjad.datastructuretools.CyclicTuple(source)
                absolute_start_index = source_length - absolute_start_index - 1
            current_count_index = 0
            current_count = counts[current_count_index]
            current_logical_tie_index = 0
            source_length = len(self.source)
            for logical_tie in logical_ties:
                index = absolute_start_index + current_logical_tie_index
                pitch_expression = source[index]
                repetition_count = index // len(self.source)
                if (self.repetition_intervals is not None and
                    0 < repetition_count):
                    repetition_intervals = abjad.datastructuretools.CyclicTuple(
                        self.repetition_intervals)
                    repetition_intervals = repetition_intervals[
                        :repetition_count]
                    repetition_interval = sum(repetition_intervals)
                    if isinstance(repetition_interval, int):
                        pitch_number = pitch_expression.pitch_number
                        pitch_number += repetition_interval
                        pitch_expression = type(pitch_expression)(pitch_number)
                    else:
                        message = 'named repetition intervals'
                        message += ' not yet implemented.'
                        raise NotImplementedError(message)
                if self.operators:
                    for operator_ in self.operators:
                        pitch_expression = operator_(pitch_expression)
                if isinstance(pitch_expression, abjad.pitchtools.Pitch):
                    if self._use_exact_spelling:
                        pitch = pitch_expression
                        assert isinstance(pitch, abjad.pitchtools.NamedPitch)
                    else:
                        pitch_expression = abjad.pitchtools.NumberedPitch(
                            pitch_expression)
                        pitch = abjad.pitchtools.NamedPitch(pitch_expression)
                elif isinstance(pitch_expression, abjad.pitchtools.Segment):
                    pitch = pitch_expression
                else:
                    message = 'must be pitch or pitch segment: {!r}.'
                    message = message.format(pitch_expression)
                    raise Exception(message)
                for note in logical_tie:
                    if isinstance(pitch, abjad.pitchtools.Pitch):
                        #note.written_pitch = pitch
                        self._set_pitch(note, pitch)
                    elif isinstance(pitch, abjad.pitchtools.PitchSegment):
                        assert isinstance(pitch, collections.Iterable)
                        chord = abjad.scoretools.Chord(
                            pitch,
                            note.written_duration,
                            )
                        # TODO: check and make sure *overrides* are preserved!
                        abjad.mutate(note).replace(chord)
                    else:
                        message = 'must be pitch or pitch segment: {!r}.'
                        message = message.format(pitch)
                        raise Exception(message)
                current_count -= 1
                if current_count == 0:
                    current_logical_tie_index += 1
                    current_count_index += 1
                    current_count = counts[current_count_index]
        else:
            assert self.operators, repr(self.operators)
            for logical_tie in logical_ties:
                for note in logical_tie:
                    for operator_ in self.operators:
                        written_pitch = note.written_pitch
                        pitch_expression = written_pitch.numbered_pitch_class
                        pitch_expression = operator_(pitch_expression)
                        written_pitch = abjad.pitchtools.NamedPitch(
                            pitch_expression)
                        #note.written_pitch = written_pitch
                        self._set_pitch(note, written_pitch)

    ### PRIVATE METHODS ###

    def _set_pitch(self, leaf, pitch):
        string = 'not yet pitched'
        if abjad.inspect_(leaf).has_indicator(string):
            abjad.detach(string, leaf)
        if isinstance(leaf, abjad.Note):
            leaf.written_pitch = pitch
        elif isinstance(leaf, abjad.Chord):
            raise NotImplementedError
        if self.allow_repeated_pitches:
            abjad.attach('repeated pitch allowed', leaf)
            
    ### PUBLIC PROPERTIES ###

    @property
    def acyclic(self):
        r'''Is true when pitch specifier reads pitches once only.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._acyclic

    @property
    def allow_repeated_pitches(self):
        r'''Is true when specifier allows repeated pitches.

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._allow_repeated_pitches

    @property
    def counts(self):
        r'''Gets counts of pitch specifier.

        ..  container:: example

            Gets counts:

            ::

                >>> specifier = baca.tools.PitchSpecifier(
                ...     counts=[20, 12, 12, 6],
                ...     operators=[
                ...         pitchtools.Inversion(),
                ...         pitchtools.Transposition(2),
                ...         ],
                ...     source=[19, 13, 15, 16, 17, 23],
                ...     )

            ::

                >>> specifier.counts
                [20, 12, 12, 6]

        Defaults to none.

        Set to positive integers or none.

        Returns positive integers or none.
        '''
        return self._counts

    @property
    def mutates_score(self):
        r'''Gets score mutation flag.

        Set to true, false or none.

        Set to true to cause segment-maker to recache all leaves in score.

        Returns true, false or none.
        '''
        return self._mutates_score

    @property
    def operators(self):
        r'''Gets operators.

        ..  container:: example

            Gets operators:

            ::

                >>> specifier = baca.tools.PitchSpecifier(
                ...     operators=[
                ...         pitchtools.Inversion(),
                ...         pitchtools.Transposition(n=2),
                ...         ],
                ...     source=[19, 13, 15, 16, 17, 23],
                ...     )

            ::

                >>> specifier.operators
                (Inversion(), Transposition(n=2))

        Defaults to none.

        Set to operators or none.

        Returns operators or none.
        '''
        return self._operators

    @property
    def repetition_intervals(self):
        r'''Gets repetition intervals.


        ..  container:: example

            With no repetition intervals:

            ::

                >>> specifier = baca.tools.PitchSpecifier(
                ...     source=[0, 1, 2, 3],
                ...     )

            ::

                >>> specifier.repetition_intervals is None
                True

            ::

                >>> for index in range(12):
                ...     pitch = specifier.get_pitch(index)
                ...     pitch.pitch_number
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

            ::

                >>> specifier = baca.tools.PitchSpecifier(
                ...     repetition_intervals=[12],
                ...     source=[0, 1, 2, 3],
                ...     )

            ::

                >>> specifier.repetition_intervals
                [12]

            ::

                >>> for index in range(12):
                ...     pitch = specifier.get_pitch(index)
                ...     pitch.pitch_number
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

            ::

                >>> specifier = baca.tools.PitchSpecifier(
                ...     repetition_intervals=[12, 1],
                ...     source=[0, 1, 2, 3],
                ...     )

            ::

                >>> specifier.repetition_intervals
                [12, 1]

            ::

                >>> for index in range(12):
                ...     pitch = specifier.get_pitch(index)
                ...     pitch.pitch_number
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
    def reverse(self):
        r'''Is true when pitch specifier reads pitches in reverse.

        ..  container:: example

            Reverses pitch specifier:

            ::

                >>> specifier = baca.tools.PitchSpecifier(
                ...     reverse=True,
                ...     source=[19, 13, 15, 16, 17, 23],
                ...     start_index=-1,
                ...     )

            ::

                >>> specifier.reverse
                True

        Defaults to none.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._reverse

    @property
    def source(self):
        r'''Gets source.

        ..  container:: example

            Gets source:

            ::

                >>> specifier = baca.tools.PitchSpecifier(
                ...     source=[19, 13, 15, 16, 17, 23],
                ...     )

            ::

                >>> for pitch in specifier.source:
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


    @property
    def start_index(self):
        r'''Gets start index.

        ..  container:: example

            Gets start index:

            ::

                >>> specifier = baca.tools.PitchSpecifier(
                ...     reverse=True,
                ...     source=[19, 13, 15, 16, 17, 23],
                ...     start_index=-1,
                ...     )

            ::

                >>> specifier.start_index
                -1

        Defaults to none.

        Set to integer or none.

        Returns integer or none.
        '''
        return self._start_index

    ### PUBLIC METHODS ###

    def get_pitch(self, index):
        r'''Gets pitch at index.

        ..  container:: example

            Gets pitches:

            ::
                
                >>> specifier = baca.tools.PitchSpecifier(
                ...     source=[12, 13, 14, 15]
                ...     )

            ::

                >>> for index in range(12):
                ...     specifier.get_pitch(index)
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
            source = abjad.datastructuretools.CyclicTuple(self.source)
        start_index = self.start_index or 0
        index += start_index
        pitch_expression = source[index]
        repetition_count = index // len(self.source)
        if self.repetition_intervals is not None and 0 < repetition_count:
            repetition_intervals = abjad.datastructuretools.CyclicTuple(
                self.repetition_intervals)
            repetition_intervals = repetition_intervals[:repetition_count]
            repetition_interval = sum(repetition_intervals)
            if isinstance(repetition_interval, int):
                pitch_number = pitch_expression.pitch_number
                pitch_number += repetition_interval
                pitch_expression = type(pitch_expression)(pitch_number)
            else:
                message = 'named repetition intervals not yet implemented.'
                raise NotImplementedError(message)
        if self.operators:
            for operator_ in self.operators:
                pitch_expression = operator_(pitch_expression)
        return pitch_expression
