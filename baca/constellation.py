"""
Constellation.
"""
import collections as collections_module
import copy

import abjad

from . import classes


def _list_numeric_octave_transpositions(range_, pitch_number_list):
    result = []
    pitch_number_set = set(pitch_number_list)
    start_pitch_number = range_.start_pitch.number
    stop_pitch_number = range_.stop_pitch.number
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


def _list_octave_transpositions(range_, pitch_carrier):
    if isinstance(pitch_carrier, collections_module.abc.Iterable):
        if all(isinstance(x, (int, float)) for x in pitch_carrier):
            return _list_numeric_octave_transpositions(range_, pitch_carrier)
    prototype = (abjad.Chord, abjad.PitchSet)
    if not isinstance(pitch_carrier, prototype):
        raise TypeError(f"must be chord or pitch-set: {pitch_carrier!r}")
    result = []
    interval = abjad.NumberedInterval(-12)
    while True:
        pitch_carrier_copy = copy.copy(pitch_carrier)
        candidate = interval.transpose(pitch_carrier_copy)
        if candidate in range_:
            result.append(candidate)
            interval -= 12
        else:
            break
    result.reverse()
    interval = abjad.NumberedInterval(0)
    while True:
        pitch_carrier_copy = copy.copy(pitch_carrier)
        candidate = interval.transpose(pitch_carrier_copy)
        if candidate in range_:
            result.append(candidate)
            interval += abjad.NumberedInterval(12)
        else:
            break
    return result


def constellate(generator, range_):
    """
    Constellates ``generator``.

    ..  container:: example

        >>> generator = [[0, 2, 10], [16, 19, 20]]
        >>> range_ = abjad.PitchRange("[C4, C#7]")
        >>> segments = baca.constellation.constellate(generator, range_)
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

        >>> generator = [[4, 8, 11], [7, 15, 17]]
        >>> range_ = abjad.PitchRange('[C4, C#7]')
        >>> segments = baca.constellation.constellate(generator, range_)
        >>> for segment in segments:
        ...     segment
        Sequence([4, 7, 8, 11, 15, 17])
        Sequence([4, 8, 11, 19, 27, 29])
        Sequence([7, 15, 16, 17, 20, 23])
        Sequence([16, 19, 20, 23, 27, 29])
        Sequence([7, 15, 17, 28, 32, 35])
        Sequence([19, 27, 28, 29, 32, 35])

    Takes outer product of octave transpositions of ``generator`` in ``range_``.
    """
    if not isinstance(range_, abjad.PitchRange):
        raise TypeError(f"pitch range only: {range_!r}.")
    transposition_list = []
    for cell in generator:
        transpositions = _list_octave_transpositions(range_, cell)
        transposition_list.append(transpositions)
    result = abjad.enumerate.yield_outer_product(transposition_list)
    result = list(result)
    for i, part in enumerate(result):
        result[i] = classes.Sequence(part).flatten(depth=-1)
    for i, cell in enumerate(result[:]):
        result[i] = cell.sort()
    return result


def make_constellation_circuit_1():
    """
    Makes constellation circuit 1.

    ..  container:: example

        >>> circuit = baca.constellation.make_constellation_circuit_1()
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
    generators = [
        [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]],
        [[-12, -10, -2], [4, 11, 27, 33, 37], [8, 17, 19, 30]],
        [[-8, 2, 15, 25], [-1, 20, 29, 31], [0, 10, 21, 42]],
        [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]],
        [[-12, -9, 1, 4], [-1, 18, 20, 33], [14, 19, 22, 29]],
        [[-10, -2, 0, 5], [-5, 3, 13, 16], [11, 30, 32, 45]],
        [[-10, -2, 5, 15, 25], [-1, 7, 18, 20], [0, 28, 33]],
        [[-12, 17, 27, 37], [-1, 7, 18, 21], [2, 10, 16, 20]],
    ]
    range_ = abjad.PitchRange("[A0, C8]")
    return ConstellationCircuit(generators, range_)


class Constellation:
    """
    Constellation.

    ..  container:: example

        >>> generators = [
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
        >>> circuit = baca.ConstellationCircuit(generators, range_)
        >>> circuit[0]
        Constellation(180)

    """

    ### INITIALIZER ###

    def __init__(self, circuit, generators):
        self._circuit = circuit
        self._generators = generators
        self._constellate_generators()
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
            >>> circuit = baca.constellation.make_constellation_circuit_1()
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

            >>> circuit = baca.constellation.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> constellation[0]
            Sequence([-38, -36, -34, -29, -28, -25, -21, -20, -19, -18, -15, -11])

        """
        return self._pitch_number_lists.__getitem__(argument)

    def __len__(self):
        """
        Gets length of constellation.

        ..  container::

            >>> circuit = baca.constellation.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> len(constellation)
            180

        """
        return len(self._pitch_number_lists)

    def __repr__(self):
        """
        Gets interpreter representation of constellation.

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> constellation
            Constellation(180)

        """
        return f"{type(self).__name__}({len(self)})"

    ### PRIVATE METHODS ###

    def _advance(self, i):
        my_idx = self._circuit._constellations.index(self)
        len_circuit = len(self._circuit)
        next_idx = (my_idx + i) % len_circuit
        next_constellation = self._circuit._constellations[next_idx]
        return next_constellation

    def _constellate_generators(self):
        self._pitch_number_lists = constellate(self._generators, self.range_)

    def _get_color_map(self):
        pitches = self._generators
        colors = ["#red", "#blue", "#green"]
        return abjad.ColorMap(colors=colors, pitch_iterables=pitches)

    def _get_colored_generator(self):
        generator_chord = self.generator_chord
        color_map = self._get_color_map()
        abjad.Label(generator_chord).color_note_heads(color_map)
        return generator_chord

    def _get_generator_pitch_numbers(self):
        result = self._generators
        result = classes.Sequence(result).flatten(depth=-1)
        return list(sorted(result))

    def _label_chord(self, chord):
        constellation_index = self._circuit._constellations.index(self)
        constellation_number = constellation_index + 1
        chord_number = self.get_number_of_chord(chord)
        string = rf"\markup {{ {constellation_number}-{chord_number} }}"
        markup = abjad.Markup(string, literal=True)
        abjad.attach(markup, chord)

    def _make_chords(self):
        result = []
        for pitch_number_list in self._pitch_number_lists:
            chord = abjad.Chord(pitch_number_list, (1, 4))
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
        color_map = self._get_color_map()
        for chord in result:
            abjad.Label(chord).color_note_heads(color_map)
        return result

    def _illustrate_chords(self, chords):
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

            >>> circuit = baca.constellation.make_constellation_circuit_1()
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

            >>> circuit = baca.constellation.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> abjad.show(constellation.generator_chord) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(constellation.generator_chord)
                >>> print(string)
                <c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                - \markup { 1-80 }

        """
        pitch_numbers = self._get_generator_pitch_numbers()
        generator_chord = abjad.Chord(pitch_numbers, (1, 4))
        self._label_chord(generator_chord)
        return generator_chord

    @property
    def generators(self):
        """
        Gets partitioned generator pitch numbers.

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
            >>> for constellation in circuit:
            ...     constellation.generators
            [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]]
            [[-12, -10, -2], [4, 11, 27, 33, 37], [8, 17, 19, 30]]
            [[-8, 2, 15, 25], [-1, 20, 29, 31], [0, 10, 21, 42]]
            [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]]
            [[-12, -9, 1, 4], [-1, 18, 20, 33], [14, 19, 22, 29]]
            [[-10, -2, 0, 5], [-5, 3, 13, 16], [11, 30, 32, 45]]
            [[-10, -2, 5, 15, 25], [-1, 7, 18, 20], [0, 28, 33]]
            [[-12, 17, 27, 37], [-1, 7, 18, 21], [2, 10, 16, 20]]

        """
        return self._generators

    @property
    def range_(self):
        """
        Gets pitch range of constellation.

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> constellation.range_
            PitchRange('[A0, C8]')

        """
        return self._circuit.range_

    @property
    def pivot_chord(self):
        r"""
        Gets pivot chord.

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> abjad.show(constellation.pivot_chord) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(constellation.pivot_chord)
                >>> print(string)
                <c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                - \markup { 1-80 }

        """
        next_pitch_number_list = self._advance(1)._get_generator_pitch_numbers()
        pivot_chord = abjad.Chord(next_pitch_number_list, (1, 4))
        self._label_chord(pivot_chord)
        return pivot_chord

    ### PUBLIC METHODS ###

    def get_chord(self, chord_number):
        """
        Gets chord with 1-indexed chord number.

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
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

            >>> circuit = baca.constellation.make_constellation_circuit_1()
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

    def illustrate_colored_generator_chord(self):
        r"""
        Shows colored generator chord.

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> lilypond_file = constellation.illustrate_colored_generator_chord()
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
                            <
                                \tweak Accidental.color #red
                                \tweak color #red
                                e'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                af'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                b'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                f''
                                \tweak Accidental.color #green
                                \tweak color #green
                                g''
                                \tweak Accidental.color #green
                                \tweak color #green
                                ef'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                fs'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                a'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                cs''''
                            >4
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            <
                                \tweak Accidental.color #red
                                \tweak color #red
                                c
                                \tweak Accidental.color #red
                                \tweak color #red
                                d
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                bf
                            >4
                        }
                    >>
                >>

        """
        colored_generator = self._get_colored_generator()
        self._label_chord(colored_generator)
        lilypond_file = self._illustrate_chords([colored_generator])
        return lilypond_file

    def illustrate_colored_generator_chord_and_pivot_chord(self):
        r"""
        Shows colored generator chord and pivot chord.

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> lilypond_file = constellation.illustrate_colored_generator_chord_and_pivot_chord()
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
                            <
                                \tweak Accidental.color #red
                                \tweak color #red
                                e'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                af'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                b'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                f''
                                \tweak Accidental.color #green
                                \tweak color #green
                                g''
                                \tweak Accidental.color #green
                                \tweak color #green
                                ef'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                fs'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                a'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                cs''''
                            >4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            <
                                \tweak Accidental.color #red
                                \tweak color #red
                                c
                                \tweak Accidental.color #red
                                \tweak color #red
                                d
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                bf
                            >4
                            <c d bf>4
                        }
                    >>
                >>

        """
        colored_generator = self._get_colored_generator()
        self._label_chord(colored_generator)
        pivot = self.pivot_chord
        self._label_chord(pivot)
        lilypond_file = self._illustrate_chords([colored_generator, pivot])
        return lilypond_file

    def illustrate_generator_chord(self):
        r"""
        Shows generator chord.

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> lilypond_file = constellation.illustrate_generator_chord()
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
        lilypond_file = self._illustrate_chords([generator])
        return lilypond_file

    def illustrate_generator_chord_and_pivot_chord(self):
        r"""
        Shows generator chord and pivot chord.

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> lilypond_file = constellation.illustrate_generator_chord_and_pivot_chord()
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
        lilypond_file = self._illustrate_chords([generator, pivot])
        return lilypond_file

    def illustrate_pivot_chord(self):
        r"""
        Shows pivot chord.

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
            >>> constellation = circuit[0]
            >>> lilypond_file = constellation.illustrate_pivot_chord()
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
        lilypond_file = self._illustrate_chords([pivot])
        return lilypond_file


class ConstellationCircuit:
    """
    Constellation circuit.

    ..  container:: example

        >>> circuit = baca.constellation.make_constellation_circuit_1()
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

    ### INITIALIZER ###

    def __init__(self, generators, range_):
        self._generators = generators
        self._range = range_
        self._constellate_generators()

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
            >>> circuit[-1]
            Constellation(108)

        """
        return self._constellations.__getitem__(argument)

    def __len__(self):
        """
        Gets length of circuit.

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
            >>> len(circuit)
            8

        """
        return len(self._constellations)

    def __repr__(self):
        """
        Gets interpreter representation of circuit.

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
            >>> circuit
            ConstellationCircuit(8)

        """
        return f"{type(self).__name__}({len(self)})"

    ### PRIVATE METHODS ###

    def _constellate_generators(self):
        self._constellations = []
        enumeration = enumerate(self._generators)
        for i, generator in enumeration:
            constellation = Constellation(self, generator)
            self._constellations.append(constellation)

    # FIXME
    def _get_colored_generator_chords(self):
        return [_._get_colored_generator() for _ in self]

    # TODO: unused?
    def _get_pivot_chord_numbers(self):
        result = []
        for constellation in self:
            pivot = constellation.pivot_chord
            number = constellation.get_number_of_chord(pivot)
            result.append(number)
        return result

    def _illustrate_chords(self, chords):
        result = abjad.illustrators.make_piano_score(leaves=chords, sketch=True)
        score, treble, bass = result
        lilypond_file = abjad.LilyPondFile(items=[score])
        return lilypond_file

    ### PUBLIC PROPERTIES ###

    @property
    def generator_chords(self):
        """
        Gets generator chords.

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
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
    def range_(self):
        """
        Gets pitch range.

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
            >>> circuit.range_
            PitchRange('[A0, C8]')

        """
        return self._range

    @property
    def pivot_chords(self):
        """
        Gets pivot chords.

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
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

    def get(self, *arguments):
        """
        Gets constellation in circuit.

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
            >>> circuit.get(8)
            Constellation(108)

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
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

            >>> circuit = baca.constellation.make_constellation_circuit_1()
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
                    \override TimeSignature.stencil = ##f
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            <
                                \tweak Accidental.color #red
                                \tweak color #red
                                e'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                af'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                b'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                f''
                                \tweak Accidental.color #green
                                \tweak color #green
                                g''
                                \tweak Accidental.color #green
                                \tweak color #green
                                ef'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                fs'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                a'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                cs''''
                            >4
                            <
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                e'
                                \tweak Accidental.color #green
                                \tweak color #green
                                af'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                b'
                                \tweak Accidental.color #green
                                \tweak color #green
                                f''
                                \tweak Accidental.color #green
                                \tweak color #green
                                g''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                ef'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                fs'''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                a'''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                cs''''
                            >4
                            <
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                b
                                \tweak Accidental.color #green
                                \tweak color #green
                                c'
                                \tweak Accidental.color #red
                                \tweak color #red
                                d'
                                \tweak Accidental.color #green
                                \tweak color #green
                                bf'
                                \tweak Accidental.color #red
                                \tweak color #red
                                ef''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                af''
                                \tweak Accidental.color #green
                                \tweak color #green
                                a''
                                \tweak Accidental.color #red
                                \tweak color #red
                                cs'''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                f'''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                g'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                fs''''
                            >4
                            <
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                c'
                                \tweak Accidental.color #red
                                \tweak color #red
                                d'
                                \tweak Accidental.color #red
                                \tweak color #red
                                bf'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                b'
                                \tweak Accidental.color #green
                                \tweak color #green
                                ef''
                                \tweak Accidental.color #red
                                \tweak color #red
                                a''
                                \tweak Accidental.color #green
                                \tweak color #green
                                cs'''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                af'''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                f''''
                                \tweak Accidental.color #green
                                \tweak color #green
                                fs''''
                                \tweak Accidental.color #green
                                \tweak color #green
                                g''''
                            >4
                            <
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                b
                                \tweak Accidental.color #red
                                \tweak color #red
                                cs'
                                \tweak Accidental.color #red
                                \tweak color #red
                                e'
                                \tweak Accidental.color #green
                                \tweak color #green
                                d''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                fs''
                                \tweak Accidental.color #green
                                \tweak color #green
                                g''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                af''
                                \tweak Accidental.color #green
                                \tweak color #green
                                bf''
                                \tweak Accidental.color #green
                                \tweak color #green
                                f'''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                a'''
                            >4
                            <
                                \tweak Accidental.color #red
                                \tweak color #red
                                c'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                ef'
                                \tweak Accidental.color #red
                                \tweak color #red
                                f'
                                \tweak Accidental.color #green
                                \tweak color #green
                                b'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                cs''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                e''
                                \tweak Accidental.color #green
                                \tweak color #green
                                fs'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                af'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                a''''
                            >4
                            <
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                b
                                \tweak Accidental.color #green
                                \tweak color #green
                                c'
                                \tweak Accidental.color #red
                                \tweak color #red
                                f'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                g'
                                \tweak Accidental.color #red
                                \tweak color #red
                                ef''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                fs''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                af''
                                \tweak Accidental.color #red
                                \tweak color #red
                                cs'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                e'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                a'''
                            >4
                            <
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                b
                                \tweak Accidental.color #green
                                \tweak color #green
                                d'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                g'
                                \tweak Accidental.color #green
                                \tweak color #green
                                bf'
                                \tweak Accidental.color #green
                                \tweak color #green
                                e''
                                \tweak Accidental.color #red
                                \tweak color #red
                                f''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                fs''
                                \tweak Accidental.color #green
                                \tweak color #green
                                af''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                a''
                                \tweak Accidental.color #red
                                \tweak color #red
                                ef'''
                                \tweak Accidental.color #red
                                \tweak color #red
                                cs''''
                            >4
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            <
                                \tweak Accidental.color #red
                                \tweak color #red
                                c
                                \tweak Accidental.color #red
                                \tweak color #red
                                d
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                bf
                            >4
                            <
                                \tweak Accidental.color #red
                                \tweak color #red
                                c
                                \tweak Accidental.color #red
                                \tweak color #red
                                d
                                \tweak Accidental.color #red
                                \tweak color #red
                                bf
                            >4
                            \tweak Accidental.color #red
                            \tweak color #red
                            e4
                            \tweak Accidental.color #red
                            \tweak color #red
                            e4
                            <
                                \tweak Accidental.color #red
                                \tweak color #red
                                c
                                \tweak Accidental.color #red
                                \tweak color #red
                                ef
                            >4
                            <
                                \tweak Accidental.color #red
                                \tweak color #red
                                d
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                g
                                \tweak Accidental.color #red
                                \tweak color #red
                                bf
                            >4
                            <
                                \tweak Accidental.color #red
                                \tweak color #red
                                d
                                \tweak Accidental.color #red
                                \tweak color #red
                                bf
                            >4
                            \tweak Accidental.color #red
                            \tweak color #red
                            c4
                        }
                    >>
                >>

        """
        chords = self._get_colored_generator_chords()
        return self._illustrate_chords(chords)

    def illustrate_colored_generator_chords_and_pivot_chords(self):
        r"""
        Illustrates colored generator chords and pivot chords.

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
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
                    \override TimeSignature.stencil = ##f
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble_Staff"
                        {
                            \clef "treble"
                            <
                                \tweak Accidental.color #red
                                \tweak color #red
                                e'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                af'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                b'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                f''
                                \tweak Accidental.color #green
                                \tweak color #green
                                g''
                                \tweak Accidental.color #green
                                \tweak color #green
                                ef'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                fs'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                a'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                cs''''
                            >4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                e'
                                \tweak Accidental.color #green
                                \tweak color #green
                                af'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                b'
                                \tweak Accidental.color #green
                                \tweak color #green
                                f''
                                \tweak Accidental.color #green
                                \tweak color #green
                                g''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                ef'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                fs'''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                a'''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                cs''''
                            >4
                            <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                            <
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                b
                                \tweak Accidental.color #green
                                \tweak color #green
                                c'
                                \tweak Accidental.color #red
                                \tweak color #red
                                d'
                                \tweak Accidental.color #green
                                \tweak color #green
                                bf'
                                \tweak Accidental.color #red
                                \tweak color #red
                                ef''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                af''
                                \tweak Accidental.color #green
                                \tweak color #green
                                a''
                                \tweak Accidental.color #red
                                \tweak color #red
                                cs'''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                f'''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                g'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                fs''''
                            >4
                            <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                            <
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                c'
                                \tweak Accidental.color #red
                                \tweak color #red
                                d'
                                \tweak Accidental.color #red
                                \tweak color #red
                                bf'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                b'
                                \tweak Accidental.color #green
                                \tweak color #green
                                ef''
                                \tweak Accidental.color #red
                                \tweak color #red
                                a''
                                \tweak Accidental.color #green
                                \tweak color #green
                                cs'''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                af'''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                f''''
                                \tweak Accidental.color #green
                                \tweak color #green
                                fs''''
                                \tweak Accidental.color #green
                                \tweak color #green
                                g''''
                            >4
                            <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                            <
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                b
                                \tweak Accidental.color #red
                                \tweak color #red
                                cs'
                                \tweak Accidental.color #red
                                \tweak color #red
                                e'
                                \tweak Accidental.color #green
                                \tweak color #green
                                d''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                fs''
                                \tweak Accidental.color #green
                                \tweak color #green
                                g''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                af''
                                \tweak Accidental.color #green
                                \tweak color #green
                                bf''
                                \tweak Accidental.color #green
                                \tweak color #green
                                f'''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                a'''
                            >4
                            <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                            <
                                \tweak Accidental.color #red
                                \tweak color #red
                                c'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                ef'
                                \tweak Accidental.color #red
                                \tweak color #red
                                f'
                                \tweak Accidental.color #green
                                \tweak color #green
                                b'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                cs''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                e''
                                \tweak Accidental.color #green
                                \tweak color #green
                                fs'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                af'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                a''''
                            >4
                            <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                            <
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                b
                                \tweak Accidental.color #green
                                \tweak color #green
                                c'
                                \tweak Accidental.color #red
                                \tweak color #red
                                f'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                g'
                                \tweak Accidental.color #red
                                \tweak color #red
                                ef''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                fs''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                af''
                                \tweak Accidental.color #red
                                \tweak color #red
                                cs'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                e'''
                                \tweak Accidental.color #green
                                \tweak color #green
                                a'''
                            >4
                            <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                            <
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                b
                                \tweak Accidental.color #green
                                \tweak color #green
                                d'
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                g'
                                \tweak Accidental.color #green
                                \tweak color #green
                                bf'
                                \tweak Accidental.color #green
                                \tweak color #green
                                e''
                                \tweak Accidental.color #red
                                \tweak color #red
                                f''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                fs''
                                \tweak Accidental.color #green
                                \tweak color #green
                                af''
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                a''
                                \tweak Accidental.color #red
                                \tweak color #red
                                ef'''
                                \tweak Accidental.color #red
                                \tweak color #red
                                cs''''
                            >4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                        }
                        \context Staff = "Bass_Staff"
                        {
                            \clef "bass"
                            <
                                \tweak Accidental.color #red
                                \tweak color #red
                                c
                                \tweak Accidental.color #red
                                \tweak color #red
                                d
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                bf
                            >4
                            <c d bf>4
                            <
                                \tweak Accidental.color #red
                                \tweak color #red
                                c
                                \tweak Accidental.color #red
                                \tweak color #red
                                d
                                \tweak Accidental.color #red
                                \tweak color #red
                                bf
                            >4
                            e4
                            \tweak Accidental.color #red
                            \tweak color #red
                            e4
                            e4
                            \tweak Accidental.color #red
                            \tweak color #red
                            e4
                            <c ef>4
                            <
                                \tweak Accidental.color #red
                                \tweak color #red
                                c
                                \tweak Accidental.color #red
                                \tweak color #red
                                ef
                            >4
                            <d g bf>4
                            <
                                \tweak Accidental.color #red
                                \tweak color #red
                                d
                                \tweak Accidental.color #blue
                                \tweak color #blue
                                g
                                \tweak Accidental.color #red
                                \tweak color #red
                                bf
                            >4
                            <d bf>4
                            <
                                \tweak Accidental.color #red
                                \tweak color #red
                                d
                                \tweak Accidental.color #red
                                \tweak color #red
                                bf
                            >4
                            c4
                            \tweak Accidental.color #red
                            \tweak color #red
                            c4
                            <c d bf>4
                        }
                    >>
                >>

        """
        chords = list(zip(self._get_colored_generator_chords(), self.pivot_chords))
        chords_ = classes.Sequence(chords).flatten(depth=1)
        return self._illustrate_chords(chords_)

    def illustrate_generator_chords(self):
        r"""
        Illustrates generator chords.

        ..  container:: example

            >>> circuit = baca.constellation.make_constellation_circuit_1()
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

            >>> circuit = baca.constellation.make_constellation_circuit_1()
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

            >>> circuit = baca.constellation.make_constellation_circuit_1()
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
                    \override TimeSignature.stencil = ##f
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
