"""
Constellation.
"""
import collections as collections_module
import copy

import abjad

from . import classes


class Constellation:
    """
    Constellation.

    ..  container:: example

        >>> cells = [
        ...     [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]],
        ...     [[-12, -10, -2], [4, 11, 27, 33, 37], [8, 17, 19, 30]],
        ...     [[-8, 2, 15, 25], [-1, 20, 29, 31], [0, 10, 21, 42]],
        ...     [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]],
        ...     [[-12, -9, 1, 4], [-1, 18, 20, 33], [14, 19, 22, 29]],
        ...     [[-10, -2, 0, 5], [-5, 3, 13, 16], [11, 30, 32, 45]],
        ...     [[-10, -2, 5, 15, 25], [-1, 7, 18, 20], [0, 28, 33]],
        ...     [[-12, 17, 27, 37], [-1, 7, 18, 21], [2, 10, 16, 20]],
        ... ]
        >>> range_ = abjad.PitchRange("[A0, C8]")
        >>> circuit = baca.ConstellationCircuit(cells, range_)
        >>> for constellation in circuit:
        ...     print(constellation)
        Constellation(180)
        Constellation(140)
        Constellation(80)
        Constellation(100)
        Constellation(180)
        Constellation(150)
        Constellation(120)
        Constellation(108)

    """

    ### INITIALIZER ###

    def __init__(self, circuit, partitioned_generator_pitch_numbers):
        self._circuit = circuit
        self._partitioned_generator_pitch_numbers = partitioned_generator_pitch_numbers
        self._constellate_partitioned_generator_pitch_numbers()
        self._chord_duration = abjad.Duration(1, 4)
        self._chords = []

    ### SPECIAL METHODS ###

    def __contains__(self, pitch_set):
        """
        Is true when constellation contains ``pitch_set``.

        ..  container:: example

            >>> pitch_numbers = [
            ...     -38, -36, -34, -29, -28, -25,
            ...     -21, -20, -19, -18, -15, -11,
            ... ]
            >>> pitch_set = baca.Sequence(items=pitch_numbers)
            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> pitch_set in constellation
            True

        ..  container:: example

            >>> constellation = circuit[0]
            >>> [-38] in constellation
            False

        """
        return pitch_set in self._pitch_number_lists

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> constellation[0]
            Sequence([-38, -36, -34, -29, -28, -25, -21, -20, -19, -18, -15, -11])

        """
        return self._pitch_number_lists.__getitem__(argument)

    def __len__(self):
        """
        Gets length of constellation.

        ..  container::

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> len(constellation)
            180

        """
        return len(self._pitch_number_lists)

    def __repr__(self):
        """
        Gets interpreter representation of constellation.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> constellation
            Constellation(180)

        """
        return f"{type(self).__name__}({len(self)})"

    ### PRIVATE PROPERTIES ###

    @property
    def _color_map(self):
        pitches = self._partitioned_generator_pitch_numbers
        colors = ["#red", "#blue", "#green"]
        return abjad.ColorMap(colors=colors, pitch_iterables=pitches)

    @property
    def _colored_generator(self):
        generator_chord = self.generator_chord
        abjad.Label(generator_chord).color_note_heads(self._color_map)
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
        result = classes.Sequence(result).flatten(depth=-1)
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
        self._pitch_number_lists = self.constellate(
            self._partitioned_generator_pitch_numbers, self.pitch_range
        )

    def _label_chord(self, chord):
        chord_number = self.get_number_of_chord(chord)
        label = f"{self._constellation_number}-{chord_number}"
        # TODO: literal=True
        markup = abjad.Markup(label)
        abjad.attach(markup, chord)

    @staticmethod
    def _list_numeric_octave_transpositions(pitch_range, pitch_number_list):
        result = []
        pitch_number_set = set(pitch_number_list)
        start_pitch_number = pitch_range.start_pitch.number
        stop_pitch_number = pitch_range.stop_pitch.number
        range_set = set(range(start_pitch_number, stop_pitch_number + 1))
        while pitch_number_set.issubset(range_set):
            next_pitch_number = list(pitch_number_set)
            next_pitch_number.sort()
            result.extend([next_pitch_number])
            pitch_number_set = set([_ + 12 for _ in pitch_number_set])
        pitch_number_set = set([_ - 12 for _ in pitch_number_list])
        while pitch_number_set.issubset(range_set):
            next_pitch_number = list(pitch_number_set)
            next_pitch_number.sort()
            result.extend([next_pitch_number])
            pitch_number_set = set([_ - 12 for _ in pitch_number_set])
        result.sort()
        return result

    @staticmethod
    def _list_octave_transpositions(pitch_range, pitch_carrier):
        if isinstance(pitch_carrier, collections_module.abc.Iterable):
            if all(isinstance(x, (int, float)) for x in pitch_carrier):
                return Constellation._list_numeric_octave_transpositions(
                    pitch_range, pitch_carrier
                )
        prototype = (abjad.Chord, abjad.PitchSet)
        if not isinstance(pitch_carrier, prototype):
            raise TypeError(f"must be chord or pitch-set: {pitch_carrier!r}")
        result = []
        interval = abjad.NumberedInterval(-12)
        while True:
            pitch_carrier_copy = copy.copy(pitch_carrier)
            candidate = interval.transpose(pitch_carrier_copy)
            if candidate in pitch_range:
                result.append(candidate)
                interval -= 12
            else:
                break
        result.reverse()
        interval = abjad.NumberedInterval(0)
        while True:
            pitch_carrier_copy = copy.copy(pitch_carrier)
            candidate = interval.transpose(pitch_carrier_copy)
            if candidate in pitch_range:
                result.append(candidate)
                interval += abjad.NumberedInterval(12)
            else:
                break
        return result

    def _make_chords(self):
        result = []
        for pitch_number_list in self._pitch_number_lists:
            chord = abjad.Chord(pitch_number_list, self._chord_duration)
            result.append(chord)
        return result

    def _make_labeled_chords(self):
        result = self._make_chords()
        for chord in result:
            self._label_chord(chord)
        return result

    # TODO: unused?
    def _make_labeled_colored_chords(self):
        result = self._make_labeled_chords()
        for chord in result:
            abjad.Label(chord).color_note_heads(self._color_map)
        return result

    def _show_chords(self, chords):
        result = abjad.illustrators.make_piano_score(leaves=chords, sketch=True)
        score, treble, bass = result
        lilypond_file = abjad.LilyPondFile(items=[score])
        return lilypond_file

    ### PUBLIC PROPERTIES ###

    @property
    def constellation_number(self):
        """
        Gets constellation number.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> constellation.constellation_number
            1

        """
        return self._circuit._constellations.index(self) + 1

    @property
    def generator_chord(self):
        r"""
        Gets generator chord.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> abjad.show(constellation.generator_chord) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(constellation.generator_chord)
                >>> print(string)
                <c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                - \markup { 1-80 }

        """
        pitch_numbers = self._generator_pitch_numbers
        generator_chord = abjad.Chord(pitch_numbers, (1, 4))
        self._label_chord(generator_chord)
        return generator_chord

    @property
    def partitioned_generator_pitch_numbers(self):
        """
        Gets partitioned generator pitch numbers.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> for constellation in circuit:
            ...     constellation.partitioned_generator_pitch_numbers
            [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
            [[-12, -10, -2], [4, 11, 27, 33, 37], [8, 17, 19, 30]]
            [[-8, 2, 15, 25], [-1, 20, 29, 31], [0, 10, 21, 42]]
            [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]]
            [[-12, -9, 1, 4], [-1, 18, 20, 33], [14, 19, 22, 29]]
            [[-10, -2, 0, 5], [-5, 3, 13, 16], [11, 30, 32, 45]]
            [[-10, -2, 5, 15, 25], [-1, 7, 18, 20], [0, 28, 33]]
            [[-12, 17, 27, 37], [-1, 7, 18, 21], [2, 10, 16, 20]]

        """
        return self._partitioned_generator_pitch_numbers

    @property
    def pitch_range(self):
        """
        Gets pitch range of constellation.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> constellation.pitch_range
            PitchRange('[A0, C8]')

        """
        return self._circuit.pitch_range

    @property
    def pivot_chord(self):
        r"""
        Gets pivot chord.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> abjad.show(constellation.pivot_chord) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(constellation.pivot_chord)
                >>> print(string)
                <c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                - \markup { 1-80 }

        """
        next_pitch_number_list = self._next._generator_pitch_numbers
        pivot_chord = abjad.Chord(next_pitch_number_list, (1, 4))
        self._label_chord(pivot_chord)
        return pivot_chord

    ### PUBLIC METHODS ###

    @staticmethod
    def constellate(cells, range_):
        """
        Constellates ``cells``.

        ..  container:: example

            >>> pitches = [[0, 2, 10], [16, 19, 20]]
            >>> range_ = abjad.PitchRange('[C4, C#7]')
            >>> segments = baca.Constellation.constellate(pitches, range_)
            >>> for segment in segments:
            ...     segment
            Sequence([0, 2, 4, 7, 8, 10])
            Sequence([0, 2, 10, 16, 19, 20])
            Sequence([0, 2, 10, 28, 31, 32])
            Sequence([4, 7, 8, 12, 14, 22])
            Sequence([12, 14, 16, 19, 20, 22])
            Sequence([12, 14, 22, 28, 31, 32])
            Sequence([4, 7, 8, 24, 26, 34])
            Sequence([16, 19, 20, 24, 26, 34])
            Sequence([24, 26, 28, 31, 32, 34])

        ..  container:: example

            >>> pitches = [[4, 8, 11], [7, 15, 17]]
            >>> range_ = abjad.PitchRange('[C4, C#7]')
            >>> segments = baca.Constellation.constellate(pitches, range_)
            >>> for segment in segments:
            ...     segment
            Sequence([4, 7, 8, 11, 15, 17])
            Sequence([4, 8, 11, 19, 27, 29])
            Sequence([7, 15, 16, 17, 20, 23])
            Sequence([16, 19, 20, 23, 27, 29])
            Sequence([7, 15, 17, 28, 32, 35])
            Sequence([19, 27, 28, 29, 32, 35])

        Takes outer product of octave transpositions of ``cells`` in ``range_``.
        """
        if not isinstance(range_, abjad.PitchRange):
            raise TypeError(f"pitch range only: {range_!r}.")
        transposition_list = []
        for cell in cells:
            transpositions = Constellation._list_octave_transpositions(range_, cell)
            transposition_list.append(transpositions)
        result = abjad.enumerate.yield_outer_product(transposition_list)
        result = list(result)
        for i, part in enumerate(result):
            result[i] = classes.Sequence(part).flatten(depth=-1)
        for i, cell in enumerate(result[:]):
            result[i] = cell.sort()
        return result

    def get_chord(self, chord_number):
        """
        Gets chord with 1-indexed chord number.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> constellation.get_chord(1)
            Sequence([-38, -36, -34, -29, -28, -25, -21, -20, -19, -18, -15, -11])

        """
        assert 1 <= chord_number
        chord_index = chord_number - 1
        return self._pitch_number_lists[chord_index]

    def get_number_of_chord(self, chord):
        """
        Gets number of chord.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> chord = constellation.get_chord(17)
            >>> constellation.get_number_of_chord(chord)
            17

        """
        chord = abjad.Chord(chord, (1, 4))
        pitch_numbers = [_.number for _ in chord.written_pitches]
        pitch_numbers_ = classes.Sequence(items=pitch_numbers)
        for i, pitch_number_list in enumerate(self):
            if pitch_number_list == pitch_numbers_:
                return i + 1
        raise ValueError(f"{chord} not in {self}")

    def show_colored_generator_chord(self):
        r"""
        Shows colored generator chord.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> lilypond_file = constellation.show_colored_generator_chord()
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            <c d bf>4
                        }
                    >>
                >>

        """
        colored_generator = self._colored_generator
        self._label_chord(colored_generator)
        lilypond_file = self._show_chords([colored_generator])
        return lilypond_file

    def show_colored_generator_chord_and_pivot_chord(self):
        r"""
        Shows colored generator chord and pivot chord.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> lilypond_file = constellation.show_colored_generator_chord_and_pivot_chord()
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            <c d bf>4
                            <c d bf>4
                        }
                    >>
                >>

        """
        colored_generator = self._colored_generator
        self._label_chord(colored_generator)
        pivot = self.pivot_chord
        self._label_chord(pivot)
        lilypond_file = self._show_chords([colored_generator, pivot])
        return lilypond_file

    def show_generator_chord(self):
        r"""
        Shows generator chord.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> lilypond_file = constellation.show_generator_chord()
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            <c d bf>4
                        }
                    >>
                >>

        """
        generator = self.generator_chord
        self._label_chord(generator)
        lilypond_file = self._show_chords([generator])
        return lilypond_file

    def show_generator_chord_and_pivot_chord(self):
        r"""
        Shows generator chord and pivot chord.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> lilypond_file = constellation.show_generator_chord_and_pivot_chord()
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            <c d bf>4
                            <c d bf>4
                        }
                    >>
                >>

        """
        generator = self.generator_chord
        self._label_chord(generator)
        pivot = self.pivot_chord
        self._label_chord(pivot)
        lilypond_file = self._show_chords([generator, pivot])
        return lilypond_file

    def show_pivot_chord(self):
        r"""
        Shows pivot chord.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> lilypond_file = constellation.show_pivot_chord()
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TimeSignature.stencil = ##f
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            <c d bf>4
                        }
                    >>
                >>

        """
        pivot = self.pivot_chord
        self._label_chord(pivot)
        lilypond_file = self._show_chords([pivot])
        return lilypond_file


class ConstellationCircuit:
    """
    Constellation circuit.

    ..  container:: example

        >>> numbers = baca.ConstellationCircuit.CC1_numbers()
        >>> range_ = abjad.PitchRange("[A0, C8]")
        >>> circuit = baca.ConstellationCircuit(numbers, range_)
        >>> for constellation in circuit:
        ...     constellation
        Constellation(180)
        Constellation(140)
        Constellation(80)
        Constellation(100)
        Constellation(180)
        Constellation(150)
        Constellation(120)
        Constellation(108)

        >>> circuit[5 - 1][173 - 1]
        Sequence([-1, 14, 18, 19, 20, 22, 24, 27, 29, 33, 37, 40])

    """

    ### INITIALIZER ###

    def __init__(self, partitioned_generator_pnls, pitch_range):
        self._partitioned_generator_pnls = partitioned_generator_pnls
        self._pitch_range = pitch_range
        self._constellate_partitioned_generator_pnls()

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> circuit[-1]
            Constellation(108)

        """
        return self._constellations.__getitem__(argument)

    def __len__(self):
        """
        Gets length of circuit.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> len(circuit)
            8

        """
        return len(self._constellations)

    def __repr__(self):
        """
        Gets interpreter representation of circuit.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> circuit
            ConstellationCircuit(8)

        """
        return f"{type(self).__name__}({len(self)})"

    ### PRIVATE PROPERTIES ###

    # FIXME
    @property
    def _colored_generator_chords(self):
        result = []
        for constellation in self:
            result.append(constellation._colored_generator)
        return result

    @property
    def _generator_chord_numbers(self):
        result = []
        for constellation in self:
            result.append(constellation._generator_chord_number)
        return result

    @property
    def _pivot_chord_numbers(self):
        result = []
        for constellation in self:
            result.append(constellation._pivot_chord_number)
        return result

    ### PRIVATE METHODS ###

    def _constellate_partitioned_generator_pnls(self):
        self._constellations = []
        enumeration = enumerate(self._partitioned_generator_pnls)
        for i, partitioned_generator_pnl in enumeration:
            constellation = Constellation(self, partitioned_generator_pnl)
            self._constellations.append(constellation)

    def _illustrate_chords(self, chords):
        result = abjad.illustrators.make_piano_score(leaves=chords, sketch=True)
        score, treble, bass = result
        abjad.override(score).TextScript.staff_padding = 10
        abjad.setting(score).proportionalNotationDuration = "#(ly:make-moment 1 30)"
        preamble = r"""#(set-global-staff-size 18)

\layout {
    indent = 0
    ragged-right = True
}

\paper {
    system-system-spacing = #'((basic-distance . 0) (minimum-distance . 0) (padding . 12) (stretchability . 0))
    top-margin = 24
}"""
        lilypond_file = abjad.LilyPondFile(items=[preamble, score])
        return lilypond_file

    ### PUBLIC PROPERTIES ###

    @property
    def generator_chords(self):
        """
        Gets generator chords.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> for chord in circuit.generator_chords:
            ...     chord
            Chord("<c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4")
            Chord("<c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4")
            Chord("<e b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4")
            Chord("<e c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4")
            Chord("<c ef b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4")
            Chord("<d g bf c' ef' f' b' cs'' e'' fs''' af''' a''''>4")
            Chord("<d bf b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4")
            Chord("<c b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4")

        """
        result = []
        for constellation in self._constellations:
            result.append(constellation.generator_chord)
        return result

    @property
    def pitch_range(self):
        """
        Gets pitch range.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> circuit.pitch_range
            PitchRange('[A0, C8]')

        """
        return self._pitch_range

    @property
    def pivot_chords(self):
        """
        Gets pivot chords.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> for chord in circuit.pivot_chords:
            ...     chord
            ...
            Chord("<c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4")
            Chord("<e b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4")
            Chord("<e c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4")
            Chord("<c ef b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4")
            Chord("<d g bf c' ef' f' b' cs'' e'' fs''' af''' a''''>4")
            Chord("<d bf b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4")
            Chord("<c b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4")
            Chord("<c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4")

        """
        result = []
        for constellation in self._constellations:
            result.append(constellation.pivot_chord)
        return result

    ### PUBLIC METHODS ###

    @staticmethod
    def CC1_numbers():
        """
        Gets constellation circuit 1 numbers.

        ..  container:: example

            >>> for list_ in baca.ConstellationCircuit.CC1_numbers():
            ...     print(list_)
            [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
            [[-12, -10, -2], [4, 11, 27, 33, 37], [8, 17, 19, 30]]
            [[-8, 2, 15, 25], [-1, 20, 29, 31], [0, 10, 21, 42]]
            [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]]
            [[-12, -9, 1, 4], [-1, 18, 20, 33], [14, 19, 22, 29]]
            [[-10, -2, 0, 5], [-5, 3, 13, 16], [11, 30, 32, 45]]
            [[-10, -2, 5, 15, 25], [-1, 7, 18, 20], [0, 28, 33]]
            [[-12, 17, 27, 37], [-1, 7, 18, 21], [2, 10, 16, 20]]

        """
        return [
            [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]],
            [[-12, -10, -2], [4, 11, 27, 33, 37], [8, 17, 19, 30]],
            [[-8, 2, 15, 25], [-1, 20, 29, 31], [0, 10, 21, 42]],
            [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]],
            [[-12, -9, 1, 4], [-1, 18, 20, 33], [14, 19, 22, 29]],
            [[-10, -2, 0, 5], [-5, 3, 13, 16], [11, 30, 32, 45]],
            [[-10, -2, 5, 15, 25], [-1, 7, 18, 20], [0, 28, 33]],
            [[-12, 17, 27, 37], [-1, 7, 18, 21], [2, 10, 16, 20]],
        ]

    def get(self, *arguments):
        """
        Gets constellation in circuit.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> circuit.get(8)
            Constellation(108)

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> circuit.get(8, 108)
            Sequence([-12, 17, 23, 26, 27, 31, 34, 37, 40, 42, 44, 45])

        """
        if len(arguments) == 1:
            constellation_number = arguments[0]
            constellation_index = constellation_number - 1
            return self._constellations[constellation_index]
        elif len(arguments) == 2:
            constellation_number, chord_number = arguments
            constellation_index = constellation_number - 1
            constellation = self._constellations[constellation_index]
            return constellation.get_chord(chord_number)
        raise IndexError

    def illustrate_colored_generator_chords(self):
        r"""
        Illustrates colored generator chords.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> lilypond_file = circuit.illustrate_colored_generator_chords()
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TextScript.staff-padding = 10
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 30)
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                            <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                            <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                            <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                            <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                            <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            <c d bf>4
                            <c d bf>4
                            e4
                            e4
                            <c ef>4
                            <d g bf>4
                            <d bf>4
                            c4
                        }
                    >>
                >>

        """
        return self._illustrate_chords(self._colored_generator_chords)

    def illustrate_colored_generator_chords_and_pivot_chords(self):
        r"""
        Illustrates colored generator chords and pivot chords.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> lilypond_file = circuit.illustrate_colored_generator_chords_and_pivot_chords()
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TextScript.staff-padding = 10
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 30)
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                            <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                            <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                            <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                            <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                            <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                            <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                            <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                            <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                            <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                            <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                            <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            <c d bf>4
                            <c d bf>4
                            <c d bf>4
                            e4
                            e4
                            e4
                            e4
                            <c ef>4
                            <c ef>4
                            <d g bf>4
                            <d g bf>4
                            <d bf>4
                            <d bf>4
                            c4
                            c4
                            <c d bf>4
                        }
                    >>
                >>

        """
        chords = list(zip(self._colored_generator_chords, self.pivot_chords))
        chords_ = classes.Sequence(chords).flatten(depth=1)
        return self._illustrate_chords(chords_)

    def illustrate_generator_chords(self):
        r"""
        Illustrates generator chords.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> lilypond_file = circuit.illustrate_generator_chords()
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TextScript.staff-padding = 10
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 30)
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                            <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                            <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                            <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                            <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                            <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            <c d bf>4
                            <c d bf>4
                            e4
                            e4
                            <c ef>4
                            <d g bf>4
                            <d bf>4
                            c4
                        }
                    >>
                >>

        """
        return self._illustrate_chords(self.generator_chords)

    def illustrate_generator_chords_and_pivot_chords(self):
        r"""
        Illustrates generator chords and pivot chords.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> lilypond_file = circuit.illustrate_generator_chords_and_pivot_chords()
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TextScript.staff-padding = 10
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 30)
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                            <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                            <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                            <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                            <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                            <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                            <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                            <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                            <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                            <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                            <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                            <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            <c d bf>4
                            <c d bf>4
                            <c d bf>4
                            e4
                            e4
                            e4
                            e4
                            <c ef>4
                            <c ef>4
                            <d g bf>4
                            <d g bf>4
                            <d bf>4
                            <d bf>4
                            c4
                            c4
                            <c d bf>4
                        }
                    >>
                >>

        """
        chords = list(zip(self.generator_chords, self.pivot_chords))
        chords_ = classes.Sequence(chords).flatten(depth=1)
        return self._illustrate_chords(chords_)

    def illustrate_pivot_chords(self):
        r"""
        Illustrates pivot chords.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> lilypond_file = circuit.illustrate_pivot_chords()
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(lilypond_file[abjad.Score])
                >>> print(string)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TextScript.staff-padding = 10
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 30)
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                            <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                            <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                            <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                            <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                            <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            <c d bf>4
                            e4
                            e4
                            <c ef>4
                            <d g bf>4
                            <d bf>4
                            c4
                            <c d bf>4
                        }
                    >>
                >>

        """
        return self._illustrate_chords(self.pivot_chords)

    @classmethod
    def make_constellation_circuit_1(class_):
        """
        Makes constellation circuit 1.

        ..  container:: example

            >>> circuit = baca.ConstellationCircuit.make_constellation_circuit_1()
            >>> for constellation in circuit:
            ...     constellation
            Constellation(180)
            Constellation(140)
            Constellation(80)
            Constellation(100)
            Constellation(180)
            Constellation(150)
            Constellation(120)
            Constellation(108)

        """
        numbers = class_.CC1_numbers()
        range_ = abjad.PitchRange("[A0, C8]")
        return class_(numbers, range_)
