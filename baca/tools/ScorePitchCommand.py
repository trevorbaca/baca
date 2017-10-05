import abjad
import collections


# TODO: write comprehensive tests
class ScorePitchCommand(abjad.AbjadObject):
    r'''Score pitch command.

    ..  container:: example

        With pitch numbers:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_commands(
            ...     'Violin Music Voice',
            ...     baca.select_stages(1),
            ...     baca.even_runs(),
            ...     baca.ScorePitchCommand(
            ...         source=[19, 13, 15, 16, 17, 23],
            ...         ),
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Score])
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

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Commands'

    __slots__ = (
        '_acyclic',
        '_allow_repeat_pitches',
        '_counts',
        '_operators',
        '_repetition_intervals',
        '_reverse',
        '_source',
        '_start_index',
        '_use_exact_spelling',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        acyclic=None,
        allow_repeat_pitches=None,
        counts=None,
        operators=None,
        repetition_intervals=None,
        reverse=None,
        source=None,
        start_index=None,
        ):
        if acyclic is not None:
            acyclic = bool(acyclic)
        self._acyclic = acyclic
        if allow_repeat_pitches is not None:
            allow_repeat_pitches = bool(allow_repeat_pitches)
        self._allow_repeat_pitches = allow_repeat_pitches
        if counts is not None:
            assert abjad.mathtools.all_are_positive_integers(counts)
        self._counts = counts
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
            isinstance(source[0], abjad.NamedPitch)):
            self._use_exact_spelling = True
        elif (isinstance(source, collections.Iterable) and
            isinstance(source[0], abjad.Segment)):
            self._use_exact_spelling = True
        elif (isinstance(source, collections.Iterable) and
            isinstance(source[0], abjad.Set)):
            self._use_exact_spelling = True
        else:
            self._use_exact_spelling = False
        if source is not None:
            if isinstance(source, str):
                source = source.split()
            source_ = []
            for element in source:
                try:
                    element = abjad.NamedPitch(element)
                except ValueError:
                    pass
                source_.append(element)
            source = source_
            source = abjad.CyclicTuple(source)
        self._source = source
        if start_index is not None:
            assert isinstance(start_index, int), repr(start_index)
        self._start_index = start_index

    ### SPECIAL METHODS ###

    # TODO: write comprehensive tests
    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        ..  note:: Write comprehensive tests.

        ..  container:: example

            Calls command on Abjad container:

            ::

                >>> command = baca.ScorePitchCommand(
                ...     source=[19, 13, 15, 16, 17, 23],
                ...     )

            ::

                >>> staff = abjad.Staff("c'8 c' c' c' c' c' c' c'")
                >>> command(staff)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
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
        if isinstance(argument[0], abjad.LogicalTie):
            logical_ties = argument
        else:
            logical_ties = list(abjad.iterate(argument).by_logical_tie())
        for logical_tie in logical_ties:
            assert isinstance(logical_tie, abjad.LogicalTie)
        counts = self.counts or [1]
        counts = abjad.CyclicTuple(counts)
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
                source = abjad.CyclicTuple(source)
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
                    repetition_intervals = abjad.CyclicTuple(
                        self.repetition_intervals)
                    repetition_intervals = repetition_intervals[
                        :repetition_count]
                    repetition_interval = sum(repetition_intervals)
                    if isinstance(repetition_interval, int):
                        pitch_number = pitch_expression.number
                        pitch_number += repetition_interval
                        pitch_expression = type(pitch_expression)(pitch_number)
                    else:
                        message = 'named repetition intervals'
                        message += ' not yet implemented.'
                        raise NotImplementedError(message)
                if self.operators:
                    for operator_ in self.operators:
                        pitch_expression = operator_(pitch_expression)
                if isinstance(pitch_expression, abjad.Pitch):
                    if self._use_exact_spelling:
                        pitch = pitch_expression
                        assert isinstance(pitch, abjad.NamedPitch)
                    else:
                        pitch_expression = abjad.NumberedPitch(
                            pitch_expression)
                        pitch = abjad.NamedPitch(pitch_expression)
                elif isinstance(pitch_expression, abjad.Segment):
                    pitch = pitch_expression
                else:
                    message = 'must be pitch or pitch segment: {!r}.'
                    message = message.format(pitch_expression)
                    raise Exception(message)
                for note in logical_tie:
                    if isinstance(pitch, abjad.Pitch):
                        self._set_pitch(note, pitch)
                    elif isinstance(pitch, abjad.PitchSegment):
                        assert isinstance(pitch, collections.Iterable)
                        chord = abjad.Chord(pitch, note.written_duration)
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
                        pitch_expression = written_pitch.pitch_class
                        pitch_expression = operator_(pitch_expression)
                        written_pitch = abjad.NamedPitch(pitch_expression)
                        self._set_pitch(note, written_pitch)

    ### PRIVATE METHODS ###

    def _mutates_score(self):
        for item in self.source or []:
            if isinstance(item, abjad.PitchSegment):
                return True
        return False

    def _set_pitch(self, leaf, pitch):
        string = 'not yet pitched'
        if abjad.inspect(leaf).has_indicator(string):
            abjad.detach(string, leaf)
        if isinstance(leaf, abjad.Note):
            leaf.written_pitch = pitch
        elif isinstance(leaf, abjad.Chord):
            raise NotImplementedError
        if self.allow_repeat_pitches:
            abjad.attach('repeat pitch allowed', leaf)

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
        r'''Gets command counts.

        ..  container:: example

            Gets counts:

            ::

                >>> command = baca.ScorePitchCommand(
                ...     counts=[20, 12, 12, 6],
                ...     operators=[
                ...         abjad.Inversion(),
                ...         abjad.Transposition(n=2),
                ...         ],
                ...     source=[19, 13, 15, 16, 17, 23],
                ...     )

            ::

                >>> command.counts
                [20, 12, 12, 6]

        Defaults to none.

        Set to positive integers or none.

        Returns positive integers or none.
        '''
        return self._counts

    @property
    def operators(self):
        r"""Gets operators.

        ..  container:: example

            Transposes input pitches:

            ::

                >>> command = baca.ScorePitchCommand(
                ...     operators=[abjad.Transposition(n=2)],
                ...     )

            ::

                >>> staff = abjad.Staff("c'8 c' c' c' c' c' c' c'")
                >>> command(staff)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    d'8
                    d'8
                    d'8
                    d'8
                    d'8
                    d'8
                    d'8
                    d'8
                }

        ..  container:: example

            Applies source to input pitches and then transposes:

            ::

                >>> command = baca.ScorePitchCommand(
                ...     operators=[
                ...         abjad.Transposition(n=2),
                ...         ],
                ...     source=[19, 13, 15, 16, 17, 23],
                ...     )

            ::

                >>> staff = abjad.Staff("c'8 c' c' c' c' c' c' c'")
                >>> command(staff)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    a''8
                    ef''8
                    f''8
                    fs''8
                    g''8
                    cs'''8
                    a''8
                    ef''8
                }

        ..  container:: example

            Transposes pitches twice:

            ::

                >>> operator = abjad.CompoundOperator()
                >>> operator = operator.transpose(n=2)
                >>> operator = operator.transpose(n=-12)
                >>> command = baca.ScorePitchCommand(
                ...     operators=[operator],
                ...     source=[19, 13, 15, 16, 17, 23],
                ...     )

            ::

                >>> staff = abjad.Staff("c'8 c' c' c' c' c' c' c'")
                >>> command(staff)
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    a'8
                    ef'8
                    f'8
                    fs'8
                    g'8
                    cs''8
                    a'8
                    ef'8
                }

        Defaults to none.

        Set to operators or none.

        ..  container:: example

            Returns list of operators or none:

            ::

                >>> command.operators
                [CompoundOperator(operators=[Transposition(n=2), Transposition(n=-12)])]

        """
        if self._operators:
            return list(self._operators)

    @property
    def repetition_intervals(self):
        r'''Gets repetition intervals.


        ..  container:: example

            With no repetition intervals:

            ::

                >>> command = baca.ScorePitchCommand(
                ...     source=[0, 1, 2, 3],
                ...     )

            ::

                >>> command.repetition_intervals is None
                True

            ::

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

            ::

                >>> command = baca.ScorePitchCommand(
                ...     repetition_intervals=[12],
                ...     source=[0, 1, 2, 3],
                ...     )

            ::

                >>> command.repetition_intervals
                [12]

            ::

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

            ::

                >>> command = baca.ScorePitchCommand(
                ...     repetition_intervals=[12, 1],
                ...     source=[0, 1, 2, 3],
                ...     )

            ::

                >>> command.repetition_intervals
                [12, 1]

            ::

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
    def reverse(self):
        r'''Is true when command reads pitches in reverse.

        ..  container:: example

            Reverses command:

            ::

                >>> command = baca.ScorePitchCommand(
                ...     reverse=True,
                ...     source=[19, 13, 15, 16, 17, 23],
                ...     start_index=-1,
                ...     )

            ::

                >>> command.reverse
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

                >>> command = baca.ScorePitchCommand(
                ...     source=[19, 13, 15, 16, 17, 23],
                ...     )

            ::

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

    @property
    def start_index(self):
        r'''Gets start index.

        ..  container:: example

            Gets start index:

            ::

                >>> command = baca.ScorePitchCommand(
                ...     reverse=True,
                ...     source=[19, 13, 15, 16, 17, 23],
                ...     start_index=-1,
                ...     )

            ::

                >>> command.start_index
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

                >>> command = baca.ScorePitchCommand(
                ...     source=[12, 13, 14, 15]
                ...     )

            ::

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
        start_index = self.start_index or 0
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
        if self.operators:
            for operator_ in self.operators:
                pitch_expression = operator_(pitch_expression)
        return pitch_expression
