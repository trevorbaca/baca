import abjad
import baca
import inspect


class Selection(abjad.Selection):
    r'''Selection.

    ..  container:: example

        >>> baca.select()
        baca.select()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    def chord(self, n):
        r'''Selects chord `n`.

        ..  container:: example

            Selects chord -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                >>> result = baca.select(staff).chord(-1)

                >>> result
                Chord("<fs' gs'>16")

            ..  container:: example expression

                >>> selector = baca.select().chord(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<fs' gs'>16")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                } {
                    {
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4 ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4 ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4 ~
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            <fs' gs'>16
                        }
                    }
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.chords()[n]

    def chead(self, n):
        r'''Selects chord head `n`.

        ..  container:: example

            Selects chord head -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                >>> result = baca.select(staff).chead(-1)

                >>> result
                Chord("<fs' gs'>4")

            ..  container:: example expression

                >>> selector = baca.select().chead(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<fs' gs'>4")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                } {
                    {
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4 ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4 ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            e'16
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            <fs' gs'>4 ~
                            <fs' gs'>16
                        }
                    }
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.cheads()[n]

    def cheads(self):
        r'''Selects chord heads.

        ..  container:: example

            Selects chord heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{16, 18}, [0, 2], {16, 18}, [4, 5], {16, 18}],
            ...     baca.color(baca.select().cheads()),
            ...     baca.rests_around([2], [4]),
            ...     counts=[5, 1, -1],
            ...     thread=True,
            ...     )

            >>> contribution.print_color_selector_result()
            Chord("<e'' fs''>4")
            Chord("<e'' fs''>16")
            Chord("<e'' fs''>4")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                r8
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <e'' fs''>4 ~
                                <e'' fs''>16
                            }
                            {
                                c'16
                                r16
                                d'4 ~
                                d'16
                            }
                            {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                <e'' fs''>16
                                r16
                            }
                            {
                                e'4 ~
                                e'16 [
                                f'16 ]
                                r16
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <e'' fs''>4 ~
                                <e'' fs''>16
                                r4
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.by_leaf(abjad.Chord, head=True, with_grace_notes=False)

    def chords(self):
        r'''Selects chords.

        ..  container:: example

            Selects chords:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     3 * [{16, 18}, [0, 2, 10]],
            ...     baca.color(baca.select().chords()),
            ...     baca.rests_around([2], [3]),
            ...     counts=[1, 5, -1],
            ...     )

            >>> contribution.print_color_selector_result()
            Chord("<e'' fs''>16")
            Chord("<e'' fs''>16")
            Chord("<e'' fs''>16")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                r8
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <e'' fs''>16
                            }
                            {
                                c'16
                                d'4 ~
                                d'16
                                r16
                                bf'16
                            }
                            {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                <e'' fs''>16
                            }
                            {
                                c'16
                                d'4 ~
                                d'16
                                r16
                                bf'16
                            }
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <e'' fs''>16
                            }
                            {
                                c'16
                                d'4 ~
                                d'16
                                r16
                                bf'16
                                r8.
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.by_class(abjad.Chord)

    def leaf(self, n):
        r'''Selects leaf `n`.

        ..  container:: example

            Selects leaf 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().leaf(0)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Rest('r8')

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Dots.color = #green
                                \once \override Rest.color = #green
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Selects leaf -4:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().leaf(-4)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Note("fs''16")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.leaves()[n]

    def leaves(self):
        r'''Selects leaves.

        ..  container:: example

            Selects leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().tuplets()[1:2].leaves()),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Note("bf'16")
            Note("e''16")
            Note("e''4")
            Note("e''16")
            Rest('r16')
            Note("fs''16")
            Note("af''16")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                bf'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                e''4 ~
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                r16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                fs''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.by_leaf(with_grace_notes=False)

    def lleaves(self):
        r'''Selects leaves, leaked to the left.

        ..  container:: example

            Selects leaves (leaked to the left) in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().tuplets()[1:2].lleaves()),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Rest('r16')
            Note("bf'16")
            Note("e''16")
            Note("e''4")
            Note("e''16")
            Rest('r16')
            Note("fs''16")
            Note("af''16")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                bf'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                e''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''4 ~
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                e''16
                                \once \override Dots.color = #blue
                                \once \override Rest.color = #blue
                                r16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                fs''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.leaves().with_previous_leaf()

    def lrleaves(self):
        r'''Selects leaves, leaked to both the left and right.

        ..  container:: example

            Selects leaves (leaked to both the left and right ) in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().tuplets()[1:2].lrleaves()),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Rest('r16')
            Note("bf'16")
            Note("e''16")
            Note("e''4")
            Note("e''16")
            Rest('r16')
            Note("fs''16")
            Note("af''16")
            Note("a'16")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                bf'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                e''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''4 ~
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                e''16
                                \once \override Dots.color = #blue
                                \once \override Rest.color = #blue
                                r16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                fs''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                af''16
                            }
                            \times 4/5 {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.leaves().with_previous_leaf().with_next_leaf()

    def lt(self, n):
        r'''Selects logical tie `n`.

        ..  container:: example

            Selects LT 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().lt(3)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            LogicalTie([Note("bf'4"), Note("bf'16")])

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                bf'4 ~
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Selects LT -4:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().lt(-4)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            LogicalTie([Note("fs''16")])

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.lts()[n]

    def lts(self):
        r'''Selects logical ties.

        ..  container:: example

            Selects LTs:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().lts()),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            LogicalTie([Rest('r8')])
            LogicalTie([Note("c'16")])
            LogicalTie([Note("c'16")])
            LogicalTie([Note("bf'4"), Note("bf'16")])
            LogicalTie([Rest('r16')])
            LogicalTie([Note("bf'16")])
            LogicalTie([Note("e''16")])
            LogicalTie([Note("e''4"), Note("e''16")])
            LogicalTie([Rest('r16')])
            LogicalTie([Note("fs''16")])
            LogicalTie([Note("af''16")])
            LogicalTie([Note("a'16")])
            LogicalTie([Rest('r4')])

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                \override TupletBracket.staff-padding = #5
                                r8
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                c'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                bf'4 ~
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                bf'16
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                bf'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                e''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''4 ~
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                r16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                fs''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                af''16
                            }
                            \times 4/5 {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                a'16
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.by_logical_tie(with_grace_notes=True)

    def note(self, n):
        r'''Selects note `n`.

        ..  container:: example

            Selects note 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().note(0)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Note("c'16")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Selects note -1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().note(-1)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Note("a'16")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.notes()[n]

    def notes(self):
        r'''Selects notes.

        ..  container:: example

            Selects notes:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().notes()),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Note("c'16")
            Note("c'16")
            Note("bf'4")
            Note("bf'16")
            Note("bf'16")
            Note("e''16")
            Note("e''4")
            Note("e''16")
            Note("fs''16")
            Note("af''16")
            Note("a'16")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                c'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                bf'4 ~
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                bf'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                e''4 ~
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                r16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                fs''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                af''16
                            }
                            \times 4/5 {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.by_class(abjad.Note)

    def phead(self, n):
        r'''Selects pitched head `n`.

        ..  container:: example

            Selects pitched head 2:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().phead(2)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Note("bf'4")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Selects pitched head -4:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().phead(-4)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Note("e''4")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                e''4 ~
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.pheads()[n]

    def pheads(self):
        r'''Selects pitched heads.

        ..  container:: example

            Selects pitched heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().pheads()),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Note("c'16")
            Note("c'16")
            Note("bf'4")
            Note("bf'16")
            Note("e''16")
            Note("e''4")
            Note("fs''16")
            Note("af''16")
            Note("a'16")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                c'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                bf'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                e''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''4 ~
                                e''16
                                r16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                fs''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                af''16
                            }
                            \times 4/5 {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.plts().map(baca.select()[0])

    def pleaf(self, n):
        r'''Selects pitched leaf `n`.

        ..  container:: example

            Selects pitched leaf 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().pleaf(0)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Note("c'16")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Selects pitched leaf -1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().pleaf(-1)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Note("a'16")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.pleaves()[n]

    def pleaves(self):
        r'''Selects pitched leaves.

        ..  container:: example

            Selects pitched leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().pleaves()),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Note("c'16")
            Note("c'16")
            Note("bf'4")
            Note("bf'16")
            Note("bf'16")
            Note("e''16")
            Note("e''4")
            Note("e''16")
            Note("fs''16")
            Note("af''16")
            Note("a'16")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                c'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                bf'4 ~
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                bf'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                e''4 ~
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                r16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                fs''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                af''16
                            }
                            \times 4/5 {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.by_leaf(pitched=True, with_grace_notes=False)

    def plt(self, n):
        r'''Selects pitched logical tie `n`.

        ..  container:: example

            Selects PLT 2:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().plt(2)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            LogicalTie([Note("bf'4"), Note("bf'16")])

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                bf'4 ~
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Selects PLT -1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().plt(-1)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            LogicalTie([Note("a'16")])

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.plts()[n]

    def plt_nprun(self, n):
        r'''Selects pitched logical tie np-run `n`.

        ..  container:: example

            Selects PLT np-run 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().plt_nprun(0)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Selection([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")])])

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                c'16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Selects PLT np-run -1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().plt_nprun(-1)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Selection([LogicalTie([Note("e''16")]), LogicalTie([Note("e''4"), Note("e''16")])])

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                e''16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                e''4 ~
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.plt_npruns()[n]

    def plt_npruns(self):
        r'''Selects pitched logical tie np-runs.

        ..  container:: example

            Selects PLT np-runs:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().plt_npruns()),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Selection([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")])])
            Selection([LogicalTie([Note("e''16")]), LogicalTie([Note("e''4"), Note("e''16")])])

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                c'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''4 ~
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>


        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = self.plts()
        result = result.group(baca.select().get_pitches())
        result = result.map(baca.select().by_contiguity())
        result = result.flatten(depth=1)
        result = result.filter(abjad.length('>', 1))
        return result

    def plt_prun(self, n):
        r'''Selects pitched logical tie p-run `n`.

        ..  container:: example

            Selects PLT p-run 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().plt_prun(0)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Selection([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")])])

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                c'16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Selects PLT p-run -1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().plt_prun(-1)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Selection([LogicalTie([Note("a'16")])])

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.plt_pruns()[n]

    def plt_pruns(self):
        r'''Selects pitched logical tie p-runs.

        ..  container:: example

            Selects PLT p-runs:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().plt_pruns()),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Selection([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")])])
            Selection([LogicalTie([Note("bf'4"), Note("bf'16")])])
            Selection([LogicalTie([Note("bf'16")])])
            Selection([LogicalTie([Note("e''16")]), LogicalTie([Note("e''4"), Note("e''16")])])
            Selection([LogicalTie([Note("fs''16")])])
            Selection([LogicalTie([Note("af''16")])])
            Selection([LogicalTie([Note("a'16")])])

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                c'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                c'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                bf'4 ~
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                bf'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''4 ~
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                r16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                fs''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                af''16
                            }
                            \times 4/5 {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = self.plts()
        result = result.group(baca.select().get_pitches())
        result = result.map(baca.select().by_contiguity())
        result = result.flatten(depth=1)
        return result

    def plt_run(self, n):
        r'''Selects pitched logical tie run `n`.

        ..  container:: example

            Selects PLT run 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().plt_run(0)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Selection([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")]), LogicalTie([Note("bf'4"), Note("bf'16")])])

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                c'16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                c'16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                bf'4 ~
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Selects PLT run -1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().plt_run(-1)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Selection([LogicalTie([Note("fs''16")]), LogicalTie([Note("af''16")]), LogicalTie([Note("a'16")])])

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                fs''16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                af''16
                            }
                            \times 4/5 {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.plt_runs()[n]

    def plt_runs(self):
        r'''Selects pitched logical tie runs.

        ..  container:: example

            Selects PLT runs:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().plt_runs()),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Selection([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")]), LogicalTie([Note("bf'4"), Note("bf'16")])])
            Selection([LogicalTie([Note("bf'16")]), LogicalTie([Note("e''16")]), LogicalTie([Note("e''4"), Note("e''16")])])
            Selection([LogicalTie([Note("fs''16")]), LogicalTie([Note("af''16")]), LogicalTie([Note("a'16")])])

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                c'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                c'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                bf'4 ~
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                bf'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''4 ~
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                r16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                fs''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                af''16
                            }
                            \times 4/5 {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.plts().by_contiguity()

    def plt_tail(self, n):
        r'''Selects pitched logical tie tail `n`.

        ..  container:: example

            Selects PLT tail 2:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().plt_tail(2)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Note("bf'16")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Selects PLT tail -4:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().plt_tail(-4)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Note("e''16")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.plt_tails()[n]

    def plt_tails(self):
        r'''Selects pitched logical tie tails.

        ..  container:: example

            Selects PLT tails:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().plt_tails()),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Note("c'16")
            Note("c'16")
            Note("bf'16")
            Note("bf'16")
            Note("e''16")
            Note("e''16")
            Note("fs''16")
            Note("af''16")
            Note("a'16")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                c'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'16
                                bf'4 ~
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                bf'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                e''16
                                e''4 ~
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                r16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                fs''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                af''16
                            }
                            \times 4/5 {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.plts().map(baca.select()[-1])

    def plts(self):
        r'''Selects pitched logical ties.

        ..  container:: example

            Selects PLTs:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().plts()),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            LogicalTie([Note("c'16")])
            LogicalTie([Note("c'16")])
            LogicalTie([Note("bf'4"), Note("bf'16")])
            LogicalTie([Note("bf'16")])
            LogicalTie([Note("e''16")])
            LogicalTie([Note("e''4"), Note("e''16")])
            LogicalTie([Note("fs''16")])
            LogicalTie([Note("af''16")])
            LogicalTie([Note("a'16")])

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                c'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                bf'4 ~
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                bf'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                e''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''4 ~
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                r16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                fs''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                af''16
                            }
                            \times 4/5 {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.by_logical_tie(pitched=True, with_grace_notes=True)

    def rest(self, n):
        r'''Selects rest `n`.

        ..  container:: example

            Selects rest 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().rest(0)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Rest('r8')

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Dots.color = #green
                                \once \override Rest.color = #green
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Selects rest -1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().rest(-1)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Rest('r4')

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                \once \override Dots.color = #green
                                \once \override Rest.color = #green
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return  self.rests()[n]

    def rests(self):
        r'''Selects rests.

        ..  container:: example

            Selects rests:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().rests()),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Rest('r8')
            Rest('r16')
            Rest('r16')
            Rest('r4')

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                \once \override Dots.color = #blue
                                \once \override Rest.color = #blue
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                \once \override Dots.color = #blue
                                \once \override Rest.color = #blue
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.by_class((abjad.MultimeasureRest, abjad.Rest))

    def rleaves(self):
        r'''Selects leaves, leaked to the right.

        ..  container:: example

            Selects leaves (leaked to the right) in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().tuplets()[1:2].rleaves()),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Note("bf'16")
            Note("e''16")
            Note("e''4")
            Note("e''16")
            Rest('r16')
            Note("fs''16")
            Note("af''16")
            Note("a'16")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                bf'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                e''4 ~
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                r16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                fs''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                af''16
                            }
                            \times 4/5 {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.leaves().with_next_leaf()

    def stages(self, start, stop=None):
        r'''Selects stages.
        '''
        if stop is None:
            stop = start
        return baca.StageSpecifier(
            start=start,
            stop=stop,
            )

    def tleaves(self):
        r'''Selects trimmed leaves.

        ..  container:: example

            Selects trimmed leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().tleaves()),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Note("c'16")
            Note("c'16")
            Note("bf'4")
            Note("bf'16")
            Rest('r16')
            Note("bf'16")
            Note("e''16")
            Note("e''4")
            Note("e''16")
            Rest('r16')
            Note("fs''16")
            Note("af''16")
            Note("a'16")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                c'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                bf'4 ~
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                bf'16
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                bf'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                e''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''4 ~
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                e''16
                                \once \override Dots.color = #blue
                                \once \override Rest.color = #blue
                                r16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                fs''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                af''16
                            }
                            \times 4/5 {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.by_leaf(trim=True, with_grace_notes=False)

#    def top(self):
#        r'''Selects top-level components.
#
#        ..  container:: example
#
#            Colors nothing because segment-maker passes leaves (not tuplets):
#
#            >>> segment_maker = baca.SegmentMaker(
#            ...     allow_empty_selections=True,
#            ...     score_template=baca.ViolinSoloScoreTemplate(),
#            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
#            ...     )
#
#            >>> segment_maker(
#            ...     baca.scope('Violin Music Voice', 1),
#            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
#            ...     baca.RhythmBuilder(
#            ...         rhythm_maker=abjad.rhythmmakertools.TaleaRhythmMaker(
#            ...             extra_counts_per_division=[1],
#            ...             talea=abjad.rhythmmakertools.Talea(
#            ...                 counts=[1, 1, 1, -1],
#            ...                 denominator=8,
#            ...                 ),
#            ...             ),
#            ...         ),
#            ...     baca.color(baca.select().tuplet(1)),
#            ...     )
#
#            >>> result = segment_maker.run(is_doc_example=True)
#            >>> lilypond_file, metadata = result
#            >>> show(lilypond_file) # doctest: +SKIP
#
#            ..  docs::
#
#                >>> f(lilypond_file[abjad.Score])
#                \context Score = "Score" <<
#                    \tag violin
#                    \context GlobalContext = "Global Context" <<
#                        \context GlobalRests = "Global Rests" {
#                            {
#                                \time 4/8
#                                R1 * 1/2
#                            }
#                            {
#                                \time 3/8
#                                R1 * 3/8
#                            }
#                            {
#                                \time 4/8
#                                R1 * 1/2
#                            }
#                            {
#                                \time 3/8
#                                R1 * 3/8
#                            }
#                        }
#                        \context GlobalSkips = "Global Skips" {
#                            {
#                                \time 4/8
#                                s1 * 1/2
#                            }
#                            {
#                                \time 3/8
#                                s1 * 3/8
#                            }
#                            {
#                                \time 4/8
#                                s1 * 1/2
#                            }
#                            {
#                                \time 3/8
#                                s1 * 3/8
#                            }
#                        }
#                    >>
#                    \context MusicContext = "Music Context" <<
#                        \tag violin
#                        \context ViolinMusicStaff = "Violin Music Staff" {
#                            \context ViolinMusicVoice = "Violin Music Voice" {
#                                \times 4/5 {
#                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
#                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
#                                    \clef "treble"
#                                    e'8 [
#                                    d''8
#                                    f'8 ]
#                                    r8
#                                    e''8
#                                }
#                                \tweak text #tuplet-number::calc-fraction-text
#                                \times 3/4 {
#                                    g'8 [
#                                    f''8 ]
#                                    r8
#                                    e'8
#                                }
#                                \times 4/5 {
#                                    d''8 [
#                                    f'8 ]
#                                    r8
#                                    e''8 [
#                                    g'8 ]
#                                }
#                                \tweak text #tuplet-number::calc-fraction-text
#                                \times 3/4 {
#                                    f''8
#                                    r8
#                                    e'8 [
#                                    d''8 ]
#                                    \bar "|"
#                                }
#                            }
#                        }
#                    >>
#                >>
#
#        ..  container:: example
#
#            Accesses tuplets and colors tuplet 1:
#
#            >>> segment_maker = baca.SegmentMaker(
#            ...     score_template=baca.ViolinSoloScoreTemplate(),
#            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
#            ...     )
#
#            >>> segment_maker(
#            ...     baca.scope('Violin Music Voice', 1),
#            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
#            ...     baca.RhythmBuilder(
#            ...         rhythm_maker=abjad.rhythmmakertools.TaleaRhythmMaker(
#            ...             extra_counts_per_division=[1],
#            ...             talea=abjad.rhythmmakertools.Talea(
#            ...                 counts=[1, 1, 1, -1],
#            ...                 denominator=8,
#            ...                 ),
#            ...             ),
#            ...         ),
#            ...     baca.color(baca.select().top().tuplet(1)),
#            ...     )
#
#            >>> result = segment_maker.run(is_doc_example=True)
#            >>> lilypond_file, metadata = result
#            >>> show(lilypond_file) # doctest: +SKIP
#
#            ..  docs::
#
#                >>> f(lilypond_file[abjad.Score])
#                \context Score = "Score" <<
#                    \tag violin
#                    \context GlobalContext = "Global Context" <<
#                        \context GlobalRests = "Global Rests" {
#                            {
#                                \time 4/8
#                                R1 * 1/2
#                            }
#                            {
#                                \time 3/8
#                                R1 * 3/8
#                            }
#                            {
#                                \time 4/8
#                                R1 * 1/2
#                            }
#                            {
#                                \time 3/8
#                                R1 * 3/8
#                            }
#                        }
#                        \context GlobalSkips = "Global Skips" {
#                            {
#                                \time 4/8
#                                s1 * 1/2
#                            }
#                            {
#                                \time 3/8
#                                s1 * 3/8
#                            }
#                            {
#                                \time 4/8
#                                s1 * 1/2
#                            }
#                            {
#                                \time 3/8
#                                s1 * 3/8
#                            }
#                        }
#                    >>
#                    \context MusicContext = "Music Context" <<
#                        \tag violin
#                        \context ViolinMusicStaff = "Violin Music Staff" {
#                            \context ViolinMusicVoice = "Violin Music Voice" {
#                                \times 4/5 {
#                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
#                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
#                                    \clef "treble"
#                                    e'8 [
#                                    d''8
#                                    f'8 ]
#                                    r8
#                                    e''8
#                                }
#                                \tweak text #tuplet-number::calc-fraction-text
#                                \times 3/4 {
#                                    \once \override Accidental.color = #green
#                                    \once \override Beam.color = #green
#                                    \once \override Dots.color = #green
#                                    \once \override NoteHead.color = #green
#                                    \once \override Stem.color = #green
#                                    g'8 [
#                                    \once \override Accidental.color = #green
#                                    \once \override Beam.color = #green
#                                    \once \override Dots.color = #green
#                                    \once \override NoteHead.color = #green
#                                    \once \override Stem.color = #green
#                                    f''8 ]
#                                    \once \override Dots.color = #green
#                                    \once \override Rest.color = #green
#                                    r8
#                                    \once \override Accidental.color = #green
#                                    \once \override Beam.color = #green
#                                    \once \override Dots.color = #green
#                                    \once \override NoteHead.color = #green
#                                    \once \override Stem.color = #green
#                                    e'8
#                                }
#                                \times 4/5 {
#                                    d''8 [
#                                    f'8 ]
#                                    r8
#                                    e''8 [
#                                    g'8 ]
#                                }
#                                \tweak text #tuplet-number::calc-fraction-text
#                                \times 3/4 {
#                                    f''8
#                                    r8
#                                    e'8 [
#                                    d''8 ]
#                                    \bar "|"
#                                }
#                            }
#                        }
#                    >>
#                >>
#
#        '''
#        if self._expression:
#            return self._update_expression(inspect.currentframe())
#        return self.top()

    def tuplet(self, n):
        r'''Selects tuplet `n`.

        ..  container:: example

            Selects tuplet 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().tuplet(0)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Tuplet(Multiplier(9, 10), "r8 c'16 c'16 bf'4 ~ bf'16 r16")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Dots.color = #green
                                \once \override Rest.color = #green
                                \override TupletBracket.staff-padding = #5
                                r8
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                c'16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                c'16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                bf'4 ~
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                bf'16
                                \once \override Dots.color = #green
                                \once \override Rest.color = #green
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        ..  container:: example

            Selects tuplet -1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.color(baca.select().tuplet(-1)),
            ...     baca.flags(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     counts=[1, 1, 5, -1],
            ...     time_treatments=[-1],
            ...     )

            >>> contribution.print_color_selector_result()
            Tuplet(Multiplier(4, 5), "a'16 r4")

            >>> lilypond_file = music_maker.show(contribution)
            >>> show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5
                                r8
                                c'16
                                c'16
                                bf'4 ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                e''16
                                e''4 ~
                                e''16
                                r16
                                fs''16
                                af''16
                            }
                            \times 4/5 {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a'16
                                \once \override Dots.color = #green
                                \once \override Rest.color = #green
                                r4
                                \revert TupletBracket.staff-padding
                            }
                        }
                    }
                >>

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.tuplets()[n]

    def tuplets(self):
        r'''Selects tuplets.

        ..  container:: example

            ..  container:: example

                >>> tuplets = [
                ...     "r8 c'16 c'16 bf'4 ~ bf'16 r16",
                ...     "bf'16 e''16 e''4 ~ e''16 r16 fs''16 af''16",
                ...     "a'16 r4",
                ...     ]
                >>> tuplets = zip([(9, 10), (9, 10), (4, 5)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file) # doctest: +SKIP

                >>> result = baca.select(staff).tuplets()

                >>> for item in result:
                ...     item
                ...
                Tuplet(Multiplier(9, 10), "r8 c'16 c'16 bf'4 ~ bf'16 r16")
                Tuplet(Multiplier(9, 10), "bf'16 e''16 e''4 ~ e''16 r16 fs''16 af''16")
                Tuplet(Multiplier(4, 5), "a'16 r4")

            ..  container:: example expression

                >>> selector = baca.select().tuplets()
                >>> result = selector(staff)

                >>> selector.print(result)
                Tuplet(Multiplier(9, 10), "r8 c'16 c'16 bf'4 ~ bf'16 r16")
                Tuplet(Multiplier(9, 10), "bf'16 e''16 e''4 ~ e''16 r16 fs''16 af''16")
                Tuplet(Multiplier(4, 5), "a'16 r4")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff \with {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                } {
                    {
                        \time 11/8
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \once \override Dots.color = #red
                            \once \override Rest.color = #red
                            r8
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            c'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            c'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            bf'4 ~
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            bf'16
                            \once \override Dots.color = #red
                            \once \override Rest.color = #red
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            bf'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            e''16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            e''4 ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            e''16
                            \once \override Dots.color = #blue
                            \once \override Rest.color = #blue
                            r16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            fs''16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            af''16
                        }
                        \times 4/5 {
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            a'16
                            \once \override Dots.color = #red
                            \once \override Rest.color = #red
                            r4
                        }
                    }
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.by_class(abjad.Tuplet)


def _select(items=None):
    if items is None:
        return baca.Expression().select()
    return baca.Selection(items=items)
