import abjad
import baca
import inspect


class Selection(abjad.Selection):
    r'''Selection.

    Selection.

    ..  container:: example

        >>> baca.select()
        baca

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        )

    ### PUBLIC METHODS ###

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
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).chead(-1)

                >>> result
                Chord("<fs' gs'>4")

            ..  container:: example expression

                >>> selector = baca.chead(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<fs' gs'>4")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
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
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.cheads()[n]

    def cheads(self):
        r'''Selects chord heads.

        ..  container:: example

            Selects chord heads:

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
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).cheads()

                >>> for item in result:
                ...     item
                ...
                Chord("<a'' b''>16")
                Chord("<d' e'>4")
                Chord("<a'' b''>16")
                Chord("<e' fs'>4")
                Chord("<a'' b''>16")
                Chord("<fs' gs'>4")

            ..  container:: example expression

                >>> selector = baca.cheads()
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<a'' b''>16")
                Chord("<d' e'>4")
                Chord("<a'' b''>16")
                Chord("<e' fs'>4")
                Chord("<a'' b''>16")
                Chord("<fs' gs'>4")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <a'' b''>16
                            c'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            bf'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <a'' b''>16
                            d'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <a'' b''>16
                            e'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return super(Selection, self).leaves(
            abjad.Chord,
            head=True,
            grace_notes=False,
            )

    def enchain(self, counts):
        r'''Enchains items in selection.

        ..  container:: example

            Enchains leaves in alternating groups of 5:

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
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).leaves().enchain([5])

                >>> for item in result:
                ...     item
                Selection([Rest('r16'), Note("bf'16"), Chord("<a'' b''>16"), Note("c'16"), Chord("<d' e'>4")])
                Selection([Chord("<d' e'>4"), Chord("<d' e'>16"), Rest('r16'), Note("bf'16"), Chord("<a'' b''>16")])
                Selection([Chord("<a'' b''>16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16"), Rest('r16')])
                Selection([Rest('r16'), Note("bf'16"), Chord("<a'' b''>16"), Note("e'16"), Chord("<fs' gs'>4")])
                Selection([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.leaves().enchain([5])
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Rest('r16'), Note("bf'16"), Chord("<a'' b''>16"), Note("c'16"), Chord("<d' e'>4")])
                Selection([Chord("<d' e'>4"), Chord("<d' e'>16"), Rest('r16'), Note("bf'16"), Chord("<a'' b''>16")])
                Selection([Chord("<a'' b''>16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16"), Rest('r16')])
                Selection([Rest('r16'), Note("bf'16"), Chord("<a'' b''>16"), Note("e'16"), Chord("<fs' gs'>4")])
                Selection([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> for i, selection in enumerate(result):
                ...     if i % 2 == 0:
                ...         color, direction = 'red', abjad.Up
                ...     else:
                ...         color, direction = 'blue', abjad.Down
                ...     for leaf in selection:
                ...         markup = abjad.Markup('*').with_color(color).bold()
                ...         markup = abjad.new(markup, direction=direction)
                ...         abjad.attach(markup, leaf)

                >>> abjad.override(staff).text_script.staff_padding = 6
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TextScript.staff-padding = #6
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            ^ \markup {
                                \bold
                                    \with-color
                                        #red
                                        *
                                }
                            bf'16
                            ^ \markup {
                                \bold
                                    \with-color
                                        #red
                                        *
                                }
                            <a'' b''>16
                            ^ \markup {
                                \bold
                                    \with-color
                                        #red
                                        *
                                }
                            c'16
                            ^ \markup {
                                \bold
                                    \with-color
                                        #red
                                        *
                                }
                            <d' e'>4
                            ~
                            ^ \markup {
                                \bold
                                    \with-color
                                        #red
                                        *
                                }
                            _ \markup {
                                \bold
                                    \with-color
                                        #blue
                                        *
                                }
                            <d' e'>16
                            _ \markup {
                                \bold
                                    \with-color
                                        #blue
                                        *
                                }
                        }
                        \times 8/9 {
                            r16
                            _ \markup {
                                \bold
                                    \with-color
                                        #blue
                                        *
                                }
                            bf'16
                            _ \markup {
                                \bold
                                    \with-color
                                        #blue
                                        *
                                }
                            <a'' b''>16
                            ^ \markup {
                                \bold
                                    \with-color
                                        #red
                                        *
                                }
                            _ \markup {
                                \bold
                                    \with-color
                                        #blue
                                        *
                                }
                            d'16
                            ^ \markup {
                                \bold
                                    \with-color
                                        #red
                                        *
                                }
                            <e' fs'>4
                            ~
                            ^ \markup {
                                \bold
                                    \with-color
                                        #red
                                        *
                                }
                            <e' fs'>16
                            ^ \markup {
                                \bold
                                    \with-color
                                        #red
                                        *
                                }
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            ^ \markup {
                                \bold
                                    \with-color
                                        #red
                                        *
                                }
                            _ \markup {
                                \bold
                                    \with-color
                                        #blue
                                        *
                                }
                            bf'16
                            _ \markup {
                                \bold
                                    \with-color
                                        #blue
                                        *
                                }
                            <a'' b''>16
                            _ \markup {
                                \bold
                                    \with-color
                                        #blue
                                        *
                                }
                            e'16
                            _ \markup {
                                \bold
                                    \with-color
                                        #blue
                                        *
                                }
                            <fs' gs'>4
                            ~
                            ^ \markup {
                                \bold
                                    \with-color
                                        #red
                                        *
                                }
                            _ \markup {
                                \bold
                                    \with-color
                                        #blue
                                        *
                                }
                            <fs' gs'>16
                            ^ \markup {
                                \bold
                                    \with-color
                                        #red
                                        *
                                }
                        }
                    }   % measure
                }

        Returns new selection (or expression).
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.partition_by_counts(
            counts=counts,
            cyclic=True,
            enchain=True,
            overhang=True,
            )

    def group(self):
        r'''Groups selection.

        ..  container:: example

            ..  container:: example

                >>> staff = abjad.Staff(r"""
                ...     c'8 ~ c'16 c'16 r8 c'16 c'16
                ...     d'8 ~ d'16 d'16 r8 d'16 d'16
                ...     """)
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).pleaves().group()

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Note("c'16"), Note("c'16"), Note("c'16"), Note("c'16"), Note("d'8"), Note("d'16"), Note("d'16"), Note("d'16"), Note("d'16")])

            ..  container:: example expression

                >>> selector = baca.select().pleaves().group()
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Selection([Note("c'8"), Note("c'16"), Note("c'16"), Note("c'16"), Note("c'16"), Note("d'8"), Note("d'16"), Note("d'16"), Note("d'16"), Note("d'16")])])

                >>> selector.color(result)
                >>> abjad.show(staff, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \once \override Accidental.color = #green
                    \once \override Beam.color = #green
                    \once \override Dots.color = #green
                    \once \override NoteHead.color = #green
                    \once \override Stem.color = #green
                    c'8
                    ~
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
                    d'8
                    ~
                    \once \override Accidental.color = #green
                    \once \override Beam.color = #green
                    \once \override Dots.color = #green
                    \once \override NoteHead.color = #green
                    \once \override Stem.color = #green
                    d'16
                    \once \override Accidental.color = #green
                    \once \override Beam.color = #green
                    \once \override Dots.color = #green
                    \once \override NoteHead.color = #green
                    \once \override Stem.color = #green
                    d'16
                    r8
                    \once \override Accidental.color = #green
                    \once \override Beam.color = #green
                    \once \override Dots.color = #green
                    \once \override NoteHead.color = #green
                    \once \override Stem.color = #green
                    d'16
                    \once \override Accidental.color = #green
                    \once \override Beam.color = #green
                    \once \override Dots.color = #green
                    \once \override NoteHead.color = #green
                    \once \override Stem.color = #green
                    d'16
                }

        Returns nested selection (or expression).
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.group_by()

    def lleak(self):
        r'''Leaks to the left.

        ..  container:: example

            Selects runs (each leaked to the left):

            ..  container:: example

                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).runs().map(baca.lleak())

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8")])
                Selection([Rest('r8'), Note("d'8"), Note("e'8")])
                Selection([Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")])

            ..  container:: example expression

                >>> selector = baca.select().runs().map(baca.lleak())
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8")])
                Selection([Rest('r8'), Note("d'8"), Note("e'8")])
                Selection([Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")])

                >>> selector.color(result)
                >>> abjad.show(staff, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    \once \override Dots.color = #blue
                    \once \override Rest.color = #blue
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    e'8
                    \once \override Dots.color = #red
                    \once \override Rest.color = #red
                    r8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    f'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    g'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    a'8
                }

        Returns new selection (or expression).
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.with_previous_leaf()

    def lleaves(self):
        r'''Selects leaves, leaked to the left.

        ..  container:: example

            Selects leaves (leaked to the left) in tuplet 1:

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
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).tuplets()[1:2].lleaves()

                >>> for item in result:
                ...     item
                ...
                Chord("<d' e'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")

            ..  container:: example expression

                >>> selector = baca.tuplets()[1:2].lleaves()
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<d' e'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <d' e'>16
                        }
                        \times 8/9 {
                            \once \override Dots.color = #blue
                            \once \override Rest.color = #blue
                            r16
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
                            <a'' b''>16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            d'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>4
                            ~
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.leaves().with_previous_leaf()

    def lt(self, n):
        r'''Selects logical tie `n`.

        ..  container:: example

            Selects logical tie -1:

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
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).lt(-1)

                >>> result
                LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.lt(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
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
                            <fs' gs'>4
                            ~
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.lts()[n]

    def ltqrun(self, n):
        r'''Selects logical tie equipitch run `n`.

        ..  container:: example

            Selects logical tie equipitch run -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).ltqrun(-1)

                >>> result
                Run([LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

            ..  container:: example expression

                >>> selector = baca.ltqrun(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Run([LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            c'16
                            c'16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            d'16
                            d'16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            e'16
                            e'16
                            e'16
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            <fs' gs'>4
                            ~
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.ltqruns()[n]

    def ltqruns(self):
        r'''Selects logical tie equipitch runs.

        ..  container:: example

            Selects logical tie equipitch runs:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).ltqruns()

                >>> for item in result:
                ...     item
                ...
                Run([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")])])
                Run([LogicalTie([Chord("<d' e'>4"), Chord("<d' e'>16")])])
                Run([LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")])])
                Run([LogicalTie([Chord("<e' fs'>4"), Chord("<e' fs'>16")])])
                Run([LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")])])
                Run([LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

            ..  container:: example expression

                >>> selector = baca.ltqruns()
                >>> result = selector(staff)

                >>> selector.print(result)
                Run([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")])])
                Run([LogicalTie([Chord("<d' e'>4"), Chord("<d' e'>16")])])
                Run([LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")])])
                Run([LogicalTie([Chord("<e' fs'>4"), Chord("<e' fs'>16")])])
                Run([LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")])])
                Run([LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
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
                            c'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <d' e'>4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            d'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            d'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            d'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <fs' gs'>4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = self.plts()
        result = result.group_by_pitch()
        result = result.map(baca.group_by_contiguity())
        result = result.flatten(depth=1)
        result = result.map(abjad.Run)
        return result

    def ltrun(self, n):
        r'''Selects logical tie run `n`.

        ..  container:: example

            Selects logical tie run -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).ltrun(-1)

                >>> result
                Run([LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

            ..  container:: example expression

                >>> selector = baca.ltrun(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Run([LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            c'16
                            c'16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            d'16
                            d'16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            e'16
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            e'16
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            e'16
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            <fs' gs'>4
                            ~
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.ltruns()[n]

    def ltruns(self):
        r'''Selects logical tie runs.

        ..  container:: example

            Selects logical tie runs:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).ltruns()

                >>> for item in result:
                ...     item
                ...
                Run([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")]), LogicalTie([Chord("<d' e'>4"), Chord("<d' e'>16")])])
                Run([LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")]), LogicalTie([Chord("<e' fs'>4"), Chord("<e' fs'>16")])])
                Run([LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

            ..  container:: example expression

                >>> selector = baca.ltruns()
                >>> result = selector(staff)

                >>> selector.print(result)
                Run([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")]), LogicalTie([Chord("<d' e'>4"), Chord("<d' e'>16")])])
                Run([LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")]), LogicalTie([Chord("<e' fs'>4"), Chord("<e' fs'>16")])])
                Run([LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
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
                            c'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <d' e'>4
                            ~
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            d'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            d'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            d'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <fs' gs'>4
                            ~
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = self.logical_ties(pitched=True).group_by_contiguity()
        return result.map(abjad.Run)

    def lts(self):
        r'''Selects logical ties.

        ..  container:: example

            Selects logical ties:

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
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).lts()

                >>> for item in result:
                ...     item
                ...
                LogicalTie([Rest('r16')])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("c'16")])
                LogicalTie([Chord("<d' e'>4"), Chord("<d' e'>16")])
                LogicalTie([Rest('r16')])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("d'16")])
                LogicalTie([Chord("<e' fs'>4"), Chord("<e' fs'>16")])
                LogicalTie([Rest('r16')])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("e'16")])
                LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.lts()
                >>> result = selector(staff)

                >>> selector.print(result)
                LogicalTie([Rest('r16')])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("c'16")])
                LogicalTie([Chord("<d' e'>4"), Chord("<d' e'>16")])
                LogicalTie([Rest('r16')])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("d'16")])
                LogicalTie([Chord("<e' fs'>4"), Chord("<e' fs'>16")])
                LogicalTie([Rest('r16')])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("e'16")])
                LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            \once \override Dots.color = #red
                            \once \override Rest.color = #red
                            r16
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
                            <a'' b''>16
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
                            <d' e'>4
                            ~
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <d' e'>16
                        }
                        \times 8/9 {
                            \once \override Dots.color = #blue
                            \once \override Rest.color = #blue
                            r16
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
                            <a'' b''>16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            d'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            \once \override Dots.color = #red
                            \once \override Rest.color = #red
                            r16
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
                            <a'' b''>16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            e'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <fs' gs'>4
                            ~
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.logical_ties(grace_notes=None)

    def ntruns(self):
        r'''Selects nontrivial runs.

        ..  container:: example

            Selects nontrivial runs:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).ntruns()

                >>> for item in result:
                ...     item
                ...
                Run([Note("c'16"), Note("c'16"), Note("c'16"), Chord("<d' e'>4"), Chord("<d' e'>16")])
                Run([Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16")])
                Run([Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.ntruns()
                >>> result = selector(staff)

                >>> selector.print(result)
                Run([Note("c'16"), Note("c'16"), Note("c'16"), Chord("<d' e'>4"), Chord("<d' e'>16")])
                Run([Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16")])
                Run([Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
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
                            c'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <d' e'>4
                            ~
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            d'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            d'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            d'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <fs' gs'>4
                            ~
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.runs().nontrivial()

    def phead(self, n):
        r'''Selects pitched head `n`.

        ..  container:: example

            Selects pitched head -1:

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
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).phead(-1)

                >>> result
                Chord("<fs' gs'>4")

            ..  container:: example expression

                >>> selector = baca.phead(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<fs' gs'>4")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
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
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.pheads()[n]

    def pheads(self):
        r'''Selects pitched heads.

        ..  container:: example

            Selects pitched heads:

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
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).pheads()

                >>> for item in result:
                ...     item
                ...
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("c'16")
                Chord("<d' e'>4")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("e'16")
                Chord("<fs' gs'>4")

            ..  container:: example expression

                >>> selector = baca.pheads()
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("c'16")
                Chord("<d' e'>4")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("e'16")
                Chord("<fs' gs'>4")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
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
                            <a'' b''>16
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
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
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
                            <a'' b''>16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            d'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
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
                            <a'' b''>16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.plts().map(baca.select()[0])

    def pleaf(self, n):
        r'''Selects pitched leaf `n`.

        ..  container:: example

            Selects pitched leaf -1:

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
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).pleaf(-1)

                >>> result
                Chord("<fs' gs'>16")

            ..  container:: example expression

                >>> selector = baca.pleaf(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<fs' gs'>16")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.pleaves()[n]

    def pleaves(self):
        r'''Selects pitched leaves.

        ..  container:: example

            Selects pitched leaves:

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
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).pleaves()

                >>> for item in result:
                ...     item
                ...
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("c'16")
                Chord("<d' e'>4")
                Chord("<d' e'>16")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("e'16")
                Chord("<fs' gs'>4")
                Chord("<fs' gs'>16")

            ..  container:: example expression

                >>> selector = baca.pleaves()
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("c'16")
                Chord("<d' e'>4")
                Chord("<d' e'>16")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("e'16")
                Chord("<fs' gs'>4")
                Chord("<fs' gs'>16")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
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
                            <a'' b''>16
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
                            <d' e'>4
                            ~
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
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
                            <a'' b''>16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            d'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <e' fs'>4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
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
                            <a'' b''>16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <fs' gs'>4
                            ~
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return super(Selection, self).leaves(
            grace_notes=False,
            pitched=True,
            )

    def plt(self, n):
        r'''Selects pitched logical tie `n`.

        ..  container:: example

            Selects pitched logical tie -1:

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
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).plt(-1)

                >>> result
                LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.plt(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
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
                            <fs' gs'>4
                            ~
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.plts()[n]

    def plts(self):
        r'''Selects pitched logical ties.

        ..  container:: example

            Selects pitched logical ties:

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
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).plts()

                >>> for item in result:
                ...     item
                ...
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("c'16")])
                LogicalTie([Chord("<d' e'>4"), Chord("<d' e'>16")])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("d'16")])
                LogicalTie([Chord("<e' fs'>4"), Chord("<e' fs'>16")])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("e'16")])
                LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.plts()
                >>> result = selector(staff)

                >>> selector.print(result)
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("c'16")])
                LogicalTie([Chord("<d' e'>4"), Chord("<d' e'>16")])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("d'16")])
                LogicalTie([Chord("<e' fs'>4"), Chord("<e' fs'>16")])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("e'16")])
                LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
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
                            <a'' b''>16
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
                            <d' e'>4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
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
                            <a'' b''>16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            d'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
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
                            <a'' b''>16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <fs' gs'>4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.logical_ties(pitched=True, grace_notes=None)

    def ptail(self, n):
        r'''Selects pitched tail `n`.

        ..  container:: example

            Selects pitched tail -1:

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
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).ptail(-1)

                >>> result
                Chord("<fs' gs'>16")

            ..  container:: example expression

                >>> selector = baca.ptail(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<fs' gs'>16")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.ptails()[n]

    def ptails(self):
        r'''Selects pitched tails.

        ..  container:: example

            Selects pitched tails:

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
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).ptails()

                >>> for item in result:
                ...     item
                ...
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("c'16")
                Chord("<d' e'>16")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>16")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("e'16")
                Chord("<fs' gs'>16")

            ..  container:: example expression

                >>> selector = baca.ptails()
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("c'16")
                Chord("<d' e'>16")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>16")
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("e'16")
                Chord("<fs' gs'>16")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
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
                            <a'' b''>16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            c'16
                            <d' e'>4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
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
                            <a'' b''>16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            d'16
                            <e' fs'>4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
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
                            <a'' b''>16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            <fs' gs'>4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.plts().map(baca.select()[-1])

    def ptlt(self, n):
        r'''Selects pitched trivial logical tie `n`.

        ..  container:: example

            Selects pitched trivial logical tie -1:

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
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).ptlt(-1)

                >>> result
                LogicalTie([Note("e'16")])

            ..  container:: example expression

                >>> selector = baca.ptlt(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                LogicalTie([Note("e'16")])

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.ptlts()[n]

    def ptlts(self):
        r'''Selects pitched trivial logical ties.

        ..  container:: example

            Selects pitched trivial logical ties:

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
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).ptlts()

                >>> for item in result:
                ...     item
                ...
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("c'16")])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("d'16")])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("e'16")])

            ..  container:: example expression

                >>> selector = baca.ptlts()
                >>> result = selector(staff)

                >>> selector.print(result)
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("c'16")])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("d'16")])
                LogicalTie([Note("bf'16")])
                LogicalTie([Chord("<a'' b''>16")])
                LogicalTie([Note("e'16")])

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
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
                            <a'' b''>16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
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
                            <a'' b''>16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
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
                            <a'' b''>16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.logical_ties(
            grace_notes=None,
            nontrivial=False,
            pitched=True,
            )

    def qrun(self, n):
        r'''Selects equipitch run `n`.

        ..  container:: example

            Selects equipitch run -1:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).qrun(-1)

                >>> result
                Run([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.qrun(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Run([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            c'16
                            c'16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            d'16
                            d'16
                            d'16
                            <e' fs'>4
                            ~
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            e'16
                            e'16
                            e'16
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            <fs' gs'>4
                            ~
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.qruns()[n]

    def qruns(self):
        r'''Selects equipitch runs.

        ..  container:: example

            Selects equipitch runs:

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).qruns()

                >>> for item in result:
                ...     item
                ...
                Run([Note("c'16"), Note("c'16"), Note("c'16")])
                Run([Chord("<d' e'>4"), Chord("<d' e'>16")])
                Run([Note("d'16"), Note("d'16"), Note("d'16")])
                Run([Chord("<e' fs'>4"), Chord("<e' fs'>16")])
                Run([Note("e'16"), Note("e'16"), Note("e'16")])
                Run([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.qruns()
                >>> result = selector(staff)

                >>> selector.print(result)
                Run([Note("c'16"), Note("c'16"), Note("c'16")])
                Run([Chord("<d' e'>4"), Chord("<d' e'>16")])
                Run([Note("d'16"), Note("d'16"), Note("d'16")])
                Run([Chord("<e' fs'>4"), Chord("<e' fs'>16")])
                Run([Note("e'16"), Note("e'16"), Note("e'16")])
                Run([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
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
                            c'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <d' e'>4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            d'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            d'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            d'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <fs' gs'>4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = self.pleaves()
        result = result.group_by_pitch()
        result = result.map(baca.group_by_contiguity())
        result = result.flatten(depth=1)
        result = result.map(abjad.Run)
        return result

    def rleak(self):
        r'''Leaks to the right.

        ..  container:: example

            Selects runs (each leaked to the right):

            ..  container:: example

                >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.show(staff, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).runs().map(baca.rleak())

                >>> for item in result:
                ...     item
                ...
                Selection([Note("c'8"), Rest('r8')])
                Selection([Note("d'8"), Note("e'8"), Rest('r8')])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])

            ..  container:: example expression

                >>> selector = baca.select().runs().map(baca.rleak())
                >>> result = selector(staff)

                >>> selector.print(result)
                Selection([Note("c'8"), Rest('r8')])
                Selection([Note("d'8"), Note("e'8"), Rest('r8')])
                Selection([Note("f'8"), Note("g'8"), Note("a'8")])

                >>> selector.color(result)
                >>> abjad.show(staff, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    c'8
                    \once \override Dots.color = #red
                    \once \override Rest.color = #red
                    r8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    d'8
                    \once \override Accidental.color = #blue
                    \once \override Beam.color = #blue
                    \once \override Dots.color = #blue
                    \once \override NoteHead.color = #blue
                    \once \override Stem.color = #blue
                    e'8
                    \once \override Dots.color = #blue
                    \once \override Rest.color = #blue
                    r8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    f'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    g'8
                    \once \override Accidental.color = #red
                    \once \override Beam.color = #red
                    \once \override Dots.color = #red
                    \once \override NoteHead.color = #red
                    \once \override Stem.color = #red
                    a'8
                }

        Returns new selection (or expression).
        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.with_next_leaf()

    def rleaves(self):
        r'''Selects leaves, leaked to the right.

        ..  container:: example

            Selects leaves (leaked to the right) in tuplet 1:

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
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).tuplets()[1:2].rleaves()

                >>> for item in result:
                ...     item
                ...
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Rest('r16')

            ..  container:: example expression

                >>> selector = baca.tuplets()[1:2].rleaves()
                >>> result = selector(staff)

                >>> selector.print(result)
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Rest('r16')

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            \once \override Dots.color = #red
                            \once \override Rest.color = #red
                            r16
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
                            <a'' b''>16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            d'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <e' fs'>4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            \once \override Dots.color = #red
                            \once \override Rest.color = #red
                            r16
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.leaves().with_next_leaf()

    def rrun(self, n):
        r'''Selects run `n` (leaked to the right).

        ..  container:: example

            Selects run 1 (leaked to the right):

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).rrun(1)

                >>> result
                Run([Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16"), Rest('r16')])

            ..  container:: example expression

                >>> selector = baca.rrun(1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Run([Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16"), Rest('r16')])

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            c'16
                            c'16
                            c'16
                            <d' e'>4
                            ~
                            <d' e'>16
                        }
                        \times 8/9 {
                            r16
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            d'16
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            d'16
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            d'16
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            <e' fs'>4
                            ~
                            \once \override Accidental.color = #green
                            \once \override Beam.color = #green
                            \once \override Dots.color = #green
                            \once \override NoteHead.color = #green
                            \once \override Stem.color = #green
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            \once \override Dots.color = #green
                            \once \override Rest.color = #green
                            r16
                            e'16
                            e'16
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.rruns()[n]

    def rruns(self):
        r'''Selects runs (leaked to the right).

        ..  container:: example

            Selects runs (leaked to the right):

            ..  container:: example

                >>> tuplets = [
                ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
                ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
                ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
                ...     ]
                >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
                >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
                >>> tuplets = [abjad.select(tuplets)]
                >>> lilypond_file = abjad.LilyPondFile.rhythm(tuplets)
                >>> staff = lilypond_file[abjad.Staff]
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).rruns()

                >>> for item in result:
                ...     item
                ...
                Run([Note("c'16"), Note("c'16"), Note("c'16"), Chord("<d' e'>4"), Chord("<d' e'>16"), Rest('r16')])
                Run([Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16"), Rest('r16')])
                Run([Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            ..  container:: example expression

                >>> selector = baca.rruns()
                >>> result = selector(staff)

                >>> selector.print(result)
                Run([Note("c'16"), Note("c'16"), Note("c'16"), Chord("<d' e'>4"), Chord("<d' e'>16"), Rest('r16')])
                Run([Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16"), Rest('r16')])
                Run([Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
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
                            c'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <d' e'>4
                            ~
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <d' e'>16
                        }
                        \times 8/9 {
                            \once \override Dots.color = #red
                            \once \override Rest.color = #red
                            r16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            d'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            d'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            d'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>4
                            ~
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            \once \override Dots.color = #blue
                            \once \override Rest.color = #blue
                            r16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <fs' gs'>4
                            ~
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        result = self.runs().map(baca.with_next_leaf())
        return result.map(abjad.Run)

    def skip(self, n):
        r'''Selects skip `n`.

        ..  container:: example

            Selects skip -1:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 s e' f' g' s b' s")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
                >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])
                >>> abjad.show(staff, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).skip(-1)

                >>> result
                Skip('s8')

            ..  container:: example expression

                >>> selector = baca.select().skip(-1)
                >>> result = selector(staff)

                >>> selector.print(result)
                Skip('s8')

                >>> selector.color(result)
                >>> abjad.show(staff, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    c'8
                    s8
                    e'8
                    f'8
                    \time 3/8
                    g'8
                    s8
                    b'8
                    % green
                    \time 1/8
                    s8
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe(), lone=True)
        return self.skips()[n]

    def skips(self):
        r'''Selects skips.

        ..  container:: example

            Selects skips:

            ..  container:: example

                >>> staff = abjad.Staff("c'8 s e' f' g' s b' s")
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
                >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
                >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])
                >>> abjad.show(staff, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).skips()

                >>> for item in result:
                ...     item
                Skip('s8')
                Skip('s8')
                Skip('s8')

            ..  container:: example expression

                >>> selector = baca.select().skips()
                >>> result = selector(staff)

                >>> selector.print(result)
                Skip('s8')
                Skip('s8')
                Skip('s8')

                >>> selector.color(result)
                >>> abjad.show(staff, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    c'8
                    % red
                    s8
                    e'8
                    f'8
                    \time 3/8
                    g'8
                    % blue
                    s8
                    b'8
                    % red
                    \time 1/8
                    s8
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.components(abjad.Skip)

    def tleaves(self):
        r'''Selects trimmed leaves.

        ..  container:: example

            Selects trimmed leaves:

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
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).tleaves()

                >>> for item in result:
                ...     item
                ...
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("c'16")
                Chord("<d' e'>4")
                Chord("<d' e'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("e'16")
                Chord("<fs' gs'>4")
                Chord("<fs' gs'>16")

            ..  container:: example expression

                >>> selector = baca.tleaves()
                >>> result = selector(staff)

                >>> selector.print(result)
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("c'16")
                Chord("<d' e'>4")
                Chord("<d' e'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("e'16")
                Chord("<fs' gs'>4")
                Chord("<fs' gs'>16")

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
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
                            <a'' b''>16
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
                            <d' e'>4
                            ~
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <d' e'>16
                        }
                        \times 8/9 {
                            \once \override Dots.color = #blue
                            \once \override Rest.color = #blue
                            r16
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
                            <a'' b''>16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            d'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>4
                            ~
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            \once \override Dots.color = #blue
                            \once \override Rest.color = #blue
                            r16
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
                            <a'' b''>16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            e'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <fs' gs'>4
                            ~
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return super(Selection, self).leaves(trim=True, grace_notes=False)

    def wleaves(self):
        r'''Selects leaves, leaked "wide" (to both the left and right).

        ..  container:: example

            Selects leaves (leaked wide) in tuplet 1:

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
                >>> abjad.setting(staff).auto_beaming = False
                >>> abjad.override(staff).tuplet_bracket.direction = abjad.Up
                >>> abjad.override(staff).tuplet_bracket.staff_padding = 3
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

                >>> result = baca.select(staff).tuplets()[1:2].wleaves()

                >>> for item in result:
                ...     item
                ...
                Chord("<d' e'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Rest('r16')

            ..  container:: example expression

                >>> selector = baca.tuplets()[1:2].wleaves()
                >>> result = selector(staff)

                >>> selector.print(result)
                Chord("<d' e'>16")
                Rest('r16')
                Note("bf'16")
                Chord("<a'' b''>16")
                Note("d'16")
                Chord("<e' fs'>4")
                Chord("<e' fs'>16")
                Rest('r16')

                >>> selector.color(result)
                >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff, strict=89)
                \new Staff
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = #3
                    autoBeaming = ##f
                }
                {
                    {   % measure
                        \time 7/4
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            r16
                            bf'16
                            <a'' b''>16
                            c'16
                            <d' e'>4
                            ~
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <d' e'>16
                        }
                        \times 8/9 {
                            \once \override Dots.color = #blue
                            \once \override Rest.color = #blue
                            r16
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
                            <a'' b''>16
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            d'16
                            \once \override Accidental.color = #blue
                            \once \override Beam.color = #blue
                            \once \override Dots.color = #blue
                            \once \override NoteHead.color = #blue
                            \once \override Stem.color = #blue
                            <e' fs'>4
                            ~
                            \once \override Accidental.color = #red
                            \once \override Beam.color = #red
                            \once \override Dots.color = #red
                            \once \override NoteHead.color = #red
                            \once \override Stem.color = #red
                            <e' fs'>16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 10/9 {
                            \once \override Dots.color = #blue
                            \once \override Rest.color = #blue
                            r16
                            bf'16
                            <a'' b''>16
                            e'16
                            <fs' gs'>4
                            ~
                            <fs' gs'>16
                        }
                    }   % measure
                }

        '''
        if self._expression:
            return self._update_expression(inspect.currentframe())
        return self.leaves().with_previous_leaf().with_next_leaf()


def _select(items=None):
    if items is None:
        return baca.Expression().select()
    return baca.Selection(items=items)
