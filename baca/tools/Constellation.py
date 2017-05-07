# -*- coding: utf-8 -*-
import abjad
import baca


class Constellation(abjad.abctools.AbjadObject):
    r'''Constellation.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> cells = [
            ...     [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]],
            ...     [[-12, -10, -2], [4, 11, 27, 33, 37], [8, 17, 19, 30]],
            ...     [[-8, 2, 15, 25], [-1, 20, 29, 31], [0, 10, 21, 42]],
            ...     [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]],
            ...     [[-12, -9, 1, 4], [-1, 18, 20, 33], [14, 19, 22, 29]],
            ...     [[-10, -2, 0, 5], [-5, 3, 13, 16], [11, 30, 32, 45]],
            ...     [[-10, -2, 5, 15, 25], [-1, 7, 18, 20], [0, 28, 33]],
            ...     [[-12, 17, 27, 37], [-1, 7, 18, 21], [2, 10, 16, 20]],
            ...     ]
            >>> range_ = abjad.PitchRange('[A0, C8]')
            >>> constellation_circuit = baca.ConstellationCircuit(
            ...     cells,
            ...     range_,
            ...     )

        ::

            >>> for constellation in constellation_circuit:
            ...     constellation
            Constellation(180)
            Constellation(140)
            Constellation(80)
            Constellation(100)
            Constellation(180)
            Constellation(150)
            Constellation(120)
            Constellation(108)

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    ### INITIALIZER ###

    def __init__(self, circuit, partitioned_generator_pitch_numbers):
        self._circuit = circuit
        self._partitioned_generator_pitch_numbers = \
            partitioned_generator_pitch_numbers
        self._constellate_partitioned_generator_pitch_numbers()
        self._chord_duration = abjad.Duration(1, 4)
        self._chords = []

    ### SPECIAL METHODS ###

    def __contains__(self, pitch_set):
        r'''Is true when constellation contains `pitch_set`.

        ..  container:: example

            ::

                >>> pitch_numbers = [
                ...     -38, -36, -34, -29, -28, -25,
                ...     -21, -20, -19, -18, -15, -11,
                ...     ]
                >>> pitch_set = baca.Sequence(items=pitch_numbers)
                >>> constellation = constellation_circuit[0]
                >>> pitch_set in constellation
                True

        ..  container:: example

            ::

                >>> constellation = constellation_circuit[0]
                >>> [-38] in constellation
                False

        Returns true or false.
        '''
        return pitch_set in self._pitch_number_lists

    def __getitem__(self, argument):
        r'''Gets item or slice identified by `argument`.

        ..  container:: example

            ::

                >>> constellation = constellation_circuit[0]
                >>> constellation[0]
                Sequence([-38, -36, -34, -29, -28, -25, -21, -20, -19, -18, -15, -11])

        Returns list.
        '''
        return self._pitch_number_lists.__getitem__(argument)

    def __len__(self):
        r'''Gets length of constellation.

        ..  container::

            ::

                >>> constellation = constellation_circuit[0]
                >>> len(constellation)
                180

        Returns nonnegative integer.
        '''
        return len(self._pitch_number_lists)

    def __repr__(self):
        r'''Gets interpreter representation of constellation.

        ..  container:: example

            ::

                >>> constellation = constellation_circuit[0]
                >>> constellation
                Constellation(180)


        '''
        string = '{}({})'
        string = string.format(type(self).__name__, len(self))
        return string

    ### PRIVATE PROPERTIES ###

    @property
    def _color_map(self):
        pitches = self._partitioned_generator_pitch_numbers
        colors = ['red', 'blue', 'green']
        return abjad.pitchtools.NumberedPitchClassColorMap(pitches, colors)

    @property
    def _colored_generator(self):
        generator_chord = self.generator_chord
        abjad.label(generator_chord).color_note_heads(self._color_map)
        return generator_chord

    @property
    def _constellation_number(self):
        constellation_index = self._circuit._constellations.index(self)
        constellation_number = constellation_index + 1
        return constellation_number

    @property
    def _generator_chord_number(self):
        return self.get_number_of_chord(self.generator_chord)

    @property
    def _generator_pitch_numbers(self):
        result = self._partitioned_generator_pitch_numbers
        result = baca.Sequence(result).flatten()
        return list(sorted(result))

    @property
    def _next(self):
        return self._advance(1)

    @property
    def _pivot_chord_number(self):
        pivot = self.pivot_chord
        return self.get_number_of_chord(pivot)

    @property
    def _prev(self):
        return self._advance(-1)

    ### PRIVATE METHODS ###

    def _advance(self, i):
        my_idx = self._circuit._constellations.index(self)
        len_circuit = len(self._circuit)
        next_idx = (my_idx + i) % len_circuit
        next_constellation = self._circuit._constellations[next_idx]
        return next_constellation

    def _constellate_partitioned_generator_pitch_numbers(self):
        self._pitch_number_lists = baca.constellate(
            self._partitioned_generator_pitch_numbers, 
            self.pitch_range,
            )

    def _label_chord(self, chord):
        chord_number = self.get_number_of_chord(chord)
        label = '%s-%s' % (self._constellation_number, chord_number)
        markup = abjad.Markup(label)
        abjad.attach(markup, chord)

    def _make_lilypond_file_and_score_from_chords(self, chords):
        score, treble, bass = \
            scoretools.make_piano_sketch_score_from_leaves(chords)
        score.override.text_script.staff_padding = 10
        score.set.proportional_notation_duration = \
            abjad.schemetools.SchemeMoment(1, 30)
        lilypond_file = abjad.lilypondfiletools.LilyPondFile.new(score)
        lilypond_file.default_paper_size = 'letter', 'landscape'
        lilypond_file.global_staff_size = 18
        lilypond_file.layout_block.indent = 0
        lilypond_file.layout_block.ragged_right = True
        lilypond_file.paper_block.system_system_spacing = \
            abjad.schemetools.SchemeVector(
            abjad.schemetools.SchemePair('basic_distance', 0),
            abjad.schemetools.SchemePair('minimum_distance', 0),
            abjad.schemetools.SchemePair('padding', 12),
            abjad.schemetools.SchemePair('stretchability', 0))
        lilypond_file.paper_block.top_margin = 24
        return lilypond_file, score

    def _show_chords(self, chords):
        lilypond_file, score = \
            self._make_lilypond_file_and_score_from_chords(chords)
        abjad.show(lilypond_file)

    ### PUBLIC PROPERTIES ###

    @property
    def constellation_number(self):
        r'''Gets constellation number.

        ..  container:: example

            ::

                >>> constellation = constellation_circuit[0]
                >>> constellation.constellation_number
                1

        Returns positive integer.
        '''
        return self._circuit._constellations.index(self) + 1

    @property
    def generator_chord(self):
        r"""Gets generator chord.

        ..  container:: example

            ::

                >>> constellation = constellation_circuit[0]
                >>> show(constellation.generator_chord) # doctest: +SKIP

            ..  doctest::

                >>> f(constellation.generator_chord)
                <c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4 - \markup { 1-80 }

        """
        pitch_numbers = self._generator_pitch_numbers
        generator_chord = abjad.Chord(pitch_numbers, (1, 4))
        self._label_chord(generator_chord)
        return generator_chord

    @property
    def partitioned_generator_pitch_numbers(self):
        r'''Gets partitioned generator pitch numbers.

        ..  container:: example

            ::

                >>> for constellation in constellation_circuit:
                ...     constellation.partitioned_generator_pitch_numbers
                [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
                [[-12, -10, -2], [4, 11, 27, 33, 37], [8, 17, 19, 30]]
                [[-8, 2, 15, 25], [-1, 20, 29, 31], [0, 10, 21, 42]]
                [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]]
                [[-12, -9, 1, 4], [-1, 18, 20, 33], [14, 19, 22, 29]]
                [[-10, -2, 0, 5], [-5, 3, 13, 16], [11, 30, 32, 45]]
                [[-10, -2, 5, 15, 25], [-1, 7, 18, 20], [0, 28, 33]]
                [[-12, 17, 27, 37], [-1, 7, 18, 21], [2, 10, 16, 20]]

        Returns list of lists.
        '''
        return self._partitioned_generator_pitch_numbers

    @property
    def pitch_range(self):
        r'''Gets pitch range of constellation.

        ..  container:: example

            ::

                >>> constellation = constellation_circuit[0]
                >>> constellation.pitch_range
                PitchRange(range_string='[A0, C8]')

        '''
        return self._circuit.pitch_range

    @property
    def pivot_chord(self):
        r"""Gets pivot chord.

        ..  container:: example

            ::

                >>> constellation = constellation_circuit[0]
                >>> show(constellation.pivot_chord) # doctest: +SKIP

            ..  doctest::

                >>> f(constellation.pivot_chord)
                <c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4 - \markup { 1-80 }

        """
        next_pitch_number_list = self._next._generator_pitch_numbers
        pivot_chord = abjad.Chord(next_pitch_number_list, (1, 4))
        self._label_chord(pivot_chord)
        return pivot_chord

    ### PUBLIC METHODS ###

    def get_chord(self, chord_number):
        '''Gets chord with 1-indexed chord number.

        ..  container:: example

            ::

                >>> constellation = constellation_circuit[0]
                >>> constellation.get_chord(1)
                Sequence([-38, -36, -34, -29, -28, -25, -21, -20, -19, -18, -15, -11])

        Returns list of numbers.
        '''
        assert 1 <= chord_number
        chord_index = chord_number - 1
        return self._pitch_number_lists[chord_index]

    def get_number_of_chord(self, chord):
        r'''Gets number of chord.
        
        ..  container:: example

            ::

                >>> constellation = constellation_circuit[0]
                >>> chord = constellation.get_chord(17)
                >>> constellation.get_number_of_chord(chord)
                17

        Returns positive integer.
        '''
        chord = abjad.Chord(chord, (1, 4))
        pitch_numbers = [_.pitch_number for _ in chord.written_pitches]
        pitch_numbers = baca.Sequence(items=pitch_numbers)
        for i, pitch_number_list in enumerate(self):
            if pitch_number_list == pitch_numbers:
                return i + 1
        message = '{} not in {}'
        message = message.format(chord, self)
        raise ValueError(message)

    def make_chords(self):
        result = []
        for pitch_number_list in self._pitch_number_lists:
            chord = abjad.Chord(pitch_number_list, self._chord_duration)
            result.append(chord)
        return result

    def make_labeled_chords(self):
        result = self.make_chords()
        for chord in result:
            self._label_chord(chord)
        return result

    def make_labeled_colored_chords(self):
        result = self.make_labeled_chords()
        for chord in result:
            labeltools.color_chord_note_heads_by_pitch_class_color_map(
            chord, self._color_map)
        return result

    def show_colored_generator_chord(self):
        colored_generator = self._colored_generator
        self._label_chord(colored_generator)
        self._show_chords([colored_generator])

    def show_colored_generator_chord_and_pivot_chord(self):
        colored_generator = self._colored_generator
        self._label_chord(colored_generator)
        pivot = self.pivot_chord
        self._label_chord(pivot)
        self._show_chords([colored_generator, pivot])

    def show_generator_chord(self):
        generator = self.generator_chord
        self._label_chord(generator)
        self._show_chords([generator])

    def show_generator_chord_and_pivot_chord(self):
        generator = self.generator_chord
        self._label_chord(generator)
        pivot = self.pivot_chord
        self._label_chord(pivot)
        self._show_chords([generator, pivot])

    def show_pivot_chord(self):
        pivot = self.pivot_chord
        self._label_chord(pivot)
        self._show_chords([pivot])
