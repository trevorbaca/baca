import abjad
import baca


class ConstellationCircuit(abjad.AbjadObject):
    r'''Constellation circuit.

    ..  container:: example

        >>> range_ = abjad.PitchRange('[A0, C8]')
        >>> constellation_circuit = baca.ConstellationCircuit(
        ...     baca.ConstellationCircuit.CC1,
        ...     range_,
        ...     )

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

    __documentation_section__ = '(5) Utilities'

    CC1 = [
        [[-12, -10, 4], [-2, 8, 11, 17], [19, 27, 30, 33, 37]],
        [[-12, -10, -2], [4, 11, 27, 33, 37], [8, 17, 19, 30]],
        [[-8, 2, 15, 25], [-1, 20, 29, 31], [0, 10, 21, 42]],
        [[-8, 2, 10, 21], [0, 11, 32, 41], [15, 25, 42, 43]],
        [[-12, -9, 1, 4], [-1, 18, 20, 33], [14, 19, 22, 29]],
        [[-10, -2, 0, 5], [-5, 3, 13, 16], [11, 30, 32, 45]],
        [[-10, -2, 5, 15, 25], [-1, 7, 18, 20], [0, 28, 33]],
        [[-12, 17, 27, 37], [-1, 7, 18, 21], [2, 10, 16, 20]],
        ]

    ### INITIALIZER ###

    def __init__(self, partitioned_generator_pnls, pitch_range):
        self._partitioned_generator_pnls = partitioned_generator_pnls
        self._pitch_range = pitch_range
        self._constellate_partitioned_generator_pnls()

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        r'''Gets item or slice identified by `argument`.

        ..  container:: example

            >>> constellation_circuit[-1]
            Constellation(108)

        Returns constellation.
        '''
        return self._constellations.__getitem__(argument)

    def __len__(self):
        r'''Gets length of circuit.

        ..  container:: example

            >>> len(constellation_circuit)
            8

        '''
        return len(self._constellations)

    def __repr__(self):
        r'''Gets interpreter representation of circuit.

        ..  container:: example

            >>> constellation_circuit
            ConstellationCircuit(8)

        Returns string.
        '''
        return f'{type(self).__name__}({len(self)})'

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
            constellation = baca.Constellation(
                self,
                partitioned_generator_pnl,
                )
            self._constellations.append(constellation)

    def _illustrate_chords(self, chords):
        result = abjad.Score.make_piano_score(leaves=chords, sketch=True)
        score, treble, bass = result
        abjad.override(score).text_script.staff_padding = 10
        moment = abjad.SchemeMoment((1, 30))
        abjad.setting(score).proportional_notation_duration = moment
        lilypond_file = abjad.LilyPondFile.new(
            score,
            global_staff_size=18,
            )
        lilypond_file.layout_block.indent = 0
        lilypond_file.layout_block.ragged_right = True
        vector = abjad.SpacingVector(0, 0, 12, 0)
        lilypond_file.paper_block.system_system_spacing = vector
        lilypond_file.paper_block.top_margin = 24
        return lilypond_file

    ### PUBLIC PROPERTIES ###

    @property
    def generator_chords(self):
        r"""Gets generator chords.

        ..  container:: example

            >>> for chord in constellation_circuit.generator_chords:
            ...     chord
            Chord("<c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4")
            Chord("<c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4")
            Chord("<e b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4")
            Chord("<e c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4")
            Chord("<c ef b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4")
            Chord("<d g bf c' ef' f' b' cs'' e'' fs''' af''' a''''>4")
            Chord("<d bf b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4")
            Chord("<c b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4")

        Returns list of chords.
        """
        result = []
        for constellation in self:
            result.append(constellation.generator_chord)
        return result

    @property
    def pitch_range(self):
        r'''Gets pitch range.

        ..  container:: example

            >>> constellation_circuit.pitch_range
            PitchRange('[A0, C8]')

        Returns pitch range.
        '''
        return self._pitch_range

    @property
    def pivot_chords(self):
        r"""Gets pivot chords.

        ..  container:: example

            >>> for chord in constellation_circuit.pivot_chords:
            ...     chord
            Chord("<c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4")
            Chord("<e b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4")
            Chord("<e c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4")
            Chord("<c ef b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4")
            Chord("<d g bf c' ef' f' b' cs'' e'' fs''' af''' a''''>4")
            Chord("<d bf b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4")
            Chord("<c b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4")
            Chord("<c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4")

        Returns list of chords.
        """
        result = []
        for constellation in self:
            result.append(constellation.pivot_chord)
        return result

    ### PUBLIC METHODS ###

    def get(self, *args):
        r'''Gets constellation in circuit.

        ..  container:: example

            >>> constellation_circuit.get(8)
            Constellation(108)

        ..  container:: example

            >>> constellation_circuit.get(8, 108)
            Sequence([-12, 17, 23, 26, 27, 31, 34, 37, 40, 42, 44, 45])

        Returns constellation or list.
        '''
        if len(args) == 1:
            constellation_number = args[0]
            constellation_index = constellation_number - 1
            return self._constellations[constellation_index]
        elif len(args) == 2:
            constellation_number, chord_number = args
            constellation_index = constellation_number - 1
            constellation = self._constellations[constellation_index]
            return constellation.get_chord(chord_number)

    def illustrate_colored_generator_chords(self):
        r"""Illustrates colored generator chords.

        ..  container:: example

            >>> lilypond_file = constellation_circuit.illustrate_colored_generator_chords()
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TextScript.staff-padding = #10
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 30)
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble Staff"
                        {
                            \clef "treble"
                            <
                                \tweak color #red
                                e'
                                \tweak color #blue
                                af'
                                \tweak color #blue
                                b'
                                \tweak color #blue
                                f''
                                \tweak color #green
                                g''
                                \tweak color #green
                                ef'''
                                \tweak color #green
                                fs'''
                                \tweak color #green
                                a'''
                                \tweak color #green
                                cs''''
                            >4
                            <
                                \tweak color #blue
                                e'
                                \tweak color #green
                                af'
                                \tweak color #blue
                                b'
                                \tweak color #green
                                f''
                                \tweak color #green
                                g''
                                \tweak color #blue
                                ef'''
                                \tweak color #green
                                fs'''
                                \tweak color #blue
                                a'''
                                \tweak color #blue
                                cs''''
                            >4
                            <
                                \tweak color #blue
                                b
                                \tweak color #green
                                c'
                                \tweak color #red
                                d'
                                \tweak color #green
                                bf'
                                \tweak color #red
                                ef''
                                \tweak color #blue
                                af''
                                \tweak color #green
                                a''
                                \tweak color #red
                                cs'''
                                \tweak color #blue
                                f'''
                                \tweak color #blue
                                g'''
                                \tweak color #green
                                fs''''
                            >4
                            <
                                \tweak color #blue
                                c'
                                \tweak color #red
                                d'
                                \tweak color #red
                                bf'
                                \tweak color #blue
                                b'
                                \tweak color #green
                                ef''
                                \tweak color #red
                                a''
                                \tweak color #green
                                cs'''
                                \tweak color #blue
                                af'''
                                \tweak color #blue
                                f''''
                                \tweak color #green
                                fs''''
                                \tweak color #green
                                g''''
                            >4
                            <
                                \tweak color #blue
                                b
                                \tweak color #red
                                cs'
                                \tweak color #red
                                e'
                                \tweak color #green
                                d''
                                \tweak color #blue
                                fs''
                                \tweak color #green
                                g''
                                \tweak color #blue
                                af''
                                \tweak color #green
                                bf''
                                \tweak color #green
                                f'''
                                \tweak color #blue
                                a'''
                            >4
                            <
                                \tweak color #red
                                c'
                                \tweak color #blue
                                ef'
                                \tweak color #red
                                f'
                                \tweak color #green
                                b'
                                \tweak color #blue
                                cs''
                                \tweak color #blue
                                e''
                                \tweak color #green
                                fs'''
                                \tweak color #green
                                af'''
                                \tweak color #green
                                a''''
                            >4
                            <
                                \tweak color #blue
                                b
                                \tweak color #green
                                c'
                                \tweak color #red
                                f'
                                \tweak color #blue
                                g'
                                \tweak color #red
                                ef''
                                \tweak color #blue
                                fs''
                                \tweak color #blue
                                af''
                                \tweak color #red
                                cs'''
                                \tweak color #green
                                e'''
                                \tweak color #green
                                a'''
                            >4
                            <
                                \tweak color #blue
                                b
                                \tweak color #green
                                d'
                                \tweak color #blue
                                g'
                                \tweak color #green
                                bf'
                                \tweak color #green
                                e''
                                \tweak color #red
                                f''
                                \tweak color #blue
                                fs''
                                \tweak color #green
                                af''
                                \tweak color #blue
                                a''
                                \tweak color #red
                                ef'''
                                \tweak color #red
                                cs''''
                            >4
                        }
                        \context Staff = "Bass Staff"
                        {
                            \clef "bass"
                            <
                                \tweak color #red
                                c
                                \tweak color #red
                                d
                                \tweak color #blue
                                bf
                            >4
                            <
                                \tweak color #red
                                c
                                \tweak color #red
                                d
                                \tweak color #red
                                bf
                            >4
                            e4
                            e4
                            <
                                \tweak color #red
                                c
                                \tweak color #red
                                ef
                            >4
                            <
                                \tweak color #red
                                d
                                \tweak color #blue
                                g
                                \tweak color #red
                                bf
                            >4
                            <
                                \tweak color #red
                                d
                                \tweak color #red
                                bf
                            >4
                            c4
                        }
                    >>
                >>

        Returns LilyPond file.
        """
        return self._illustrate_chords(self._colored_generator_chords)

    def illustrate_colored_generator_chords_and_pivot_chords(self):
        r"""Illustrates colored generator chords and pivot chords.

        ..  container:: example

            >>> lilypond_file = constellation_circuit.illustrate_colored_generator_chords_and_pivot_chords()
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TextScript.staff-padding = #10
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 30)
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble Staff"
                        {
                            \clef "treble"
                            <
                                \tweak color #red
                                e'
                                \tweak color #blue
                                af'
                                \tweak color #blue
                                b'
                                \tweak color #blue
                                f''
                                \tweak color #green
                                g''
                                \tweak color #green
                                ef'''
                                \tweak color #green
                                fs'''
                                \tweak color #green
                                a'''
                                \tweak color #green
                                cs''''
                            >4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                            <
                                \tweak color #blue
                                e'
                                \tweak color #green
                                af'
                                \tweak color #blue
                                b'
                                \tweak color #green
                                f''
                                \tweak color #green
                                g''
                                \tweak color #blue
                                ef'''
                                \tweak color #green
                                fs'''
                                \tweak color #blue
                                a'''
                                \tweak color #blue
                                cs''''
                            >4
                            <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                            <
                                \tweak color #blue
                                b
                                \tweak color #green
                                c'
                                \tweak color #red
                                d'
                                \tweak color #green
                                bf'
                                \tweak color #red
                                ef''
                                \tweak color #blue
                                af''
                                \tweak color #green
                                a''
                                \tweak color #red
                                cs'''
                                \tweak color #blue
                                f'''
                                \tweak color #blue
                                g'''
                                \tweak color #green
                                fs''''
                            >4
                            <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                            <
                                \tweak color #blue
                                c'
                                \tweak color #red
                                d'
                                \tweak color #red
                                bf'
                                \tweak color #blue
                                b'
                                \tweak color #green
                                ef''
                                \tweak color #red
                                a''
                                \tweak color #green
                                cs'''
                                \tweak color #blue
                                af'''
                                \tweak color #blue
                                f''''
                                \tweak color #green
                                fs''''
                                \tweak color #green
                                g''''
                            >4
                            <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                            <
                                \tweak color #blue
                                b
                                \tweak color #red
                                cs'
                                \tweak color #red
                                e'
                                \tweak color #green
                                d''
                                \tweak color #blue
                                fs''
                                \tweak color #green
                                g''
                                \tweak color #blue
                                af''
                                \tweak color #green
                                bf''
                                \tweak color #green
                                f'''
                                \tweak color #blue
                                a'''
                            >4
                            <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                            <
                                \tweak color #red
                                c'
                                \tweak color #blue
                                ef'
                                \tweak color #red
                                f'
                                \tweak color #green
                                b'
                                \tweak color #blue
                                cs''
                                \tweak color #blue
                                e''
                                \tweak color #green
                                fs'''
                                \tweak color #green
                                af'''
                                \tweak color #green
                                a''''
                            >4
                            <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                            <
                                \tweak color #blue
                                b
                                \tweak color #green
                                c'
                                \tweak color #red
                                f'
                                \tweak color #blue
                                g'
                                \tweak color #red
                                ef''
                                \tweak color #blue
                                fs''
                                \tweak color #blue
                                af''
                                \tweak color #red
                                cs'''
                                \tweak color #green
                                e'''
                                \tweak color #green
                                a'''
                            >4
                            <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                            <
                                \tweak color #blue
                                b
                                \tweak color #green
                                d'
                                \tweak color #blue
                                g'
                                \tweak color #green
                                bf'
                                \tweak color #green
                                e''
                                \tweak color #red
                                f''
                                \tweak color #blue
                                fs''
                                \tweak color #green
                                af''
                                \tweak color #blue
                                a''
                                \tweak color #red
                                ef'''
                                \tweak color #red
                                cs''''
                            >4
                            <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                        }
                        \context Staff = "Bass Staff"
                        {
                            \clef "bass"
                            <
                                \tweak color #red
                                c
                                \tweak color #red
                                d
                                \tweak color #blue
                                bf
                            >4
                            <c d bf>4
                            <
                                \tweak color #red
                                c
                                \tweak color #red
                                d
                                \tweak color #red
                                bf
                            >4
                            e4
                            e4
                            e4
                            e4
                            <c ef>4
                            <
                                \tweak color #red
                                c
                                \tweak color #red
                                ef
                            >4
                            <d g bf>4
                            <
                                \tweak color #red
                                d
                                \tweak color #blue
                                g
                                \tweak color #red
                                bf
                            >4
                            <d bf>4
                            <
                                \tweak color #red
                                d
                                \tweak color #red
                                bf
                            >4
                            c4
                            c4
                            <c d bf>4
                        }
                    >>
                >>

        Returns LilyPond file.
        """
        chords = list(zip(self._colored_generator_chords, self.pivot_chords))
        chords = baca.sequence(chords).flatten(depth=1)
        return self._illustrate_chords(chords)

    def illustrate_generator_chords(self):
        r"""Illustrates generator chords.

        ..  container:: example

            >>> lilypond_file = constellation_circuit.illustrate_generator_chords()
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TextScript.staff-padding = #10
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 30)
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble Staff"
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
                        \context Staff = "Bass Staff"
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

        Returns LilyPond file.
        """
        return self._illustrate_chords(self.generator_chords)

    def illustrate_generator_chords_and_pivot_chords(self):
        r"""Illustrates generator chords and pivot chords.

        ..  container:: example

            >>> lilypond_file = constellation_circuit.illustrate_generator_chords_and_pivot_chords()
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TextScript.staff-padding = #10
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 30)
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble Staff"
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
                        \context Staff = "Bass Staff"
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

        Returns LilyPond file.
        """
        chords = list(zip(self.generator_chords, self.pivot_chords))
        chords = baca.sequence(chords).flatten(depth=1)
        return self._illustrate_chords(chords)

    def illustrate_pivot_chords(self):
        r"""Illustrates pivot chords.

        ..  container:: example

            >>> lilypond_file = constellation_circuit.illustrate_pivot_chords()
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Score], strict=89)
                \new Score
                \with
                {
                    \override BarLine.stencil = ##f
                    \override BarNumber.transparent = ##t
                    \override SpanBar.stencil = ##f
                    \override TextScript.staff-padding = #10
                    \override TimeSignature.stencil = ##f
                    proportionalNotationDuration = #(ly:make-moment 1 30)
                }
                <<
                    \new PianoStaff
                    <<
                        \context Staff = "Treble Staff"
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
                        \context Staff = "Bass Staff"
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

        Returns LilyPond file.
        """
        return self._illustrate_chords(self.pivot_chords)

    @classmethod
    def make_constellation_circuit_1(class_):
        r'''Makes constellation circuit 1.

            >>> class_ = baca.ConstellationCircuit
            >>> constellation_circuit = class_.make_constellation_circuit_1()
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

        Returns constellation circuit.
        '''
        return class_(class_.CC1, abjad.PitchRange('[A0, C8]'))
