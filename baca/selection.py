import typing

import abjad


class Selection(abjad.Selection):
    """
    Selection.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PUBLIC METHODS ###

    def chead(self, n: int, *, exclude: abjad.Strings = None) -> abjad.Note:
        r"""
        Selects chord head ``n``.

        ..  container:: example

            Selects chord head -1:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).chead(-1)
            >>> result
            Chord("<fs' gs'>4")

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        \abjad-color-music #'green
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        return self.cheads(exclude=exclude)[n]

    def cheads(self, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects chord heads.

        ..  container:: example

            Selects chord heads:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).cheads()
            >>> for item in result:
            ...     item
            ...
            Chord("<a'' b''>16")
            Chord("<d' e'>4")
            Chord("<a'' b''>16")
            Chord("<e' fs'>4")
            Chord("<a'' b''>16")
            Chord("<fs' gs'>4")

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        e'16
                        \abjad-color-music #'blue
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        return super().leaves(abjad.Chord, exclude=exclude, head=True)

    def clparts(
        self, counts: typing.Sequence[int], *, exclude: abjad.Strings = None
    ) -> abjad.Selection:
        r"""
        Selects leaves cyclically partitioned by ``counts`` (with overhang).

        ..  container:: example

            Selects leaves cyclically partitioned 2, 3, 4:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).clparts([2, 3, 4])
            >>> for item in result:
            ...     item
            ...
            Selection([Rest('r16'), Note("bf'16")])
            Selection([Chord("<a'' b''>16"), Note("c'16"), Chord("<d' e'>4")])
            Selection([Chord("<d' e'>16"), Rest('r16'), Note("bf'16"), Chord("<a'' b''>16")])
            Selection([Note("d'16"), Chord("<e' fs'>4")])
            Selection([Chord("<e' fs'>16"), Rest('r16'), Note("bf'16")])
            Selection([Chord("<a'' b''>16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'blue
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'red
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'blue
                        e'16
                        \abjad-color-music #'blue
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'blue
                        <fs' gs'>16
                    }
                }

        """
        return (
            super()
            .leaves(exclude=exclude)
            .partition_by_counts(counts=counts, cyclic=True, overhang=True)
        )

    def cmgroups(
        self, counts: typing.List[int] = [1], *, exclude: abjad.Strings = None
    ) -> "Selection":
        r"""
        Partitions measure-grouped leaves (cyclically).

        ..  container:: example

            Partitions measure-grouped leaves into pairs:

            >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r d''")
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
            >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

            >>> result = baca.Selection(staff).cmgroups([2])
            >>> for item in result:
            ...     item
            ...
            Selection([Rest('r8'), Note("d'8"), Note("e'8"), Note("f'8")])
            Selection([Note("g'8"), Note("a'8"), Note("b'8"), Rest('r8')])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'red
                    f'8
                    \time 3/8
                    \abjad-color-music #'blue
                    g'8
                    \abjad-color-music #'blue
                    a'8
                    \abjad-color-music #'blue
                    b'8
                    \time 1/8
                    \abjad-color-music #'blue
                    r8
                    d''8
                }

        """
        result = self.leaves(exclude=exclude)
        result = result.group_by_measure()
        result = result.partition_by_counts(counts, cyclic=True)
        assert isinstance(result, Selection)
        items = [Selection(_).flatten() for _ in result]
        result_ = Selection(items)
        assert isinstance(result_, Selection), repr(result_)
        return result_

    def enchain(self, counts: typing.Sequence[int]) -> abjad.Selection:
        r"""
        Enchains items in selection.

        ..  container:: example

            Enchains leaves in alternating groups of 5:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).leaves().enchain([5])
            >>> for item in result:
            ...     item
            Selection([Rest('r16'), Note("bf'16"), Chord("<a'' b''>16"), Note("c'16"), Chord("<d' e'>4")])
            Selection([Chord("<d' e'>4"), Chord("<d' e'>16"), Rest('r16'), Note("bf'16"), Chord("<a'' b''>16")])
            Selection([Chord("<a'' b''>16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16"), Rest('r16')])
            Selection([Rest('r16'), Note("bf'16"), Chord("<a'' b''>16"), Note("e'16"), Chord("<fs' gs'>4")])
            Selection([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            >>> for i, selection in enumerate(result):
            ...     if i % 2 == 0:
            ...         color, direction = "#red", abjad.Up
            ...     else:
            ...         color, direction = "#blue", abjad.Down
            ...     string = rf'\markup {{ \bold \with-color {color} * }}'
            ...     for leaf in selection:
            ...         markup = abjad.Markup(string)
            ...         markup = abjad.new(markup, direction=direction)
            ...         abjad.attach(markup, leaf)

            >>> abjad.override(staff).TextScript.staff_padding = 6
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TextScript.staff-padding = 6
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        ^ \markup { \bold \with-color #red * }
                        bf'16
                        ^ \markup { \bold \with-color #red * }
                        <a'' b''>16
                        ^ \markup { \bold \with-color #red * }
                        c'16
                        ^ \markup { \bold \with-color #red * }
                        <d' e'>4
                        ^ \markup { \bold \with-color #red * }
                        _ \markup { \bold \with-color #blue * }
                        ~
                        <d' e'>16
                        _ \markup { \bold \with-color #blue * }
                    }
                    \times 8/9
                    {
                        r16
                        _ \markup { \bold \with-color #blue * }
                        bf'16
                        _ \markup { \bold \with-color #blue * }
                        <a'' b''>16
                        ^ \markup { \bold \with-color #red * }
                        _ \markup { \bold \with-color #blue * }
                        d'16
                        ^ \markup { \bold \with-color #red * }
                        <e' fs'>4
                        ^ \markup { \bold \with-color #red * }
                        ~
                        <e' fs'>16
                        ^ \markup { \bold \with-color #red * }
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        ^ \markup { \bold \with-color #red * }
                        _ \markup { \bold \with-color #blue * }
                        bf'16
                        _ \markup { \bold \with-color #blue * }
                        <a'' b''>16
                        _ \markup { \bold \with-color #blue * }
                        e'16
                        _ \markup { \bold \with-color #blue * }
                        <fs' gs'>4
                        ^ \markup { \bold \with-color #red * }
                        _ \markup { \bold \with-color #blue * }
                        ~
                        <fs' gs'>16
                        ^ \markup { \bold \with-color #red * }
                    }
                }

        Returns new selection.
        """
        return self.partition_by_counts(
            counts=counts, cyclic=True, enchain=True, overhang=True
        )

    def grace(self, n: int = 0, *, exclude: abjad.Strings = None) -> abjad.Leaf:
        r"""
        Selects grace ``n``.

        ..  container:: example

            Selects grace -1:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.AfterGraceContainer("af'16 gf'16")
            >>> abjad.attach(container, staff[1])
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = baca.Selection(staff).grace(-1)
            >>> result
            Note("gf'16")

            >>> abjad.label.by_selector(result, lone=True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    \grace {
                        cf''16
                        bf'16
                    }
                    \afterGrace
                    d'8
                    {
                        af'16
                        \abjad-color-music #'green
                        gf'16
                    }
                    e'8
                    f'8
                }

        """
        return self.graces(exclude=exclude)[n]

    def graces(self, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects graces.

        ..  container:: example

            Selects graces:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.AfterGraceContainer("af'16 gf'16")
            >>> abjad.attach(container, staff[1])
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = baca.Selection(staff).graces()
            >>> for item in result:
            ...     item
            ...
            Note("cf''16")
            Note("bf'16")
            Note("af'16")
            Note("gf'16")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    \grace {
                        \abjad-color-music #'red
                        cf''16
                        \abjad-color-music #'blue
                        bf'16
                    }
                    \afterGrace
                    d'8
                    {
                        \abjad-color-music #'red
                        af'16
                        \abjad-color-music #'blue
                        gf'16
                    }
                    e'8
                    f'8
                }

        """
        return self.leaves(exclude=exclude, grace=True)

    def hleaf(self, n: int = 0, *, exclude: abjad.Strings = None) -> abjad.Leaf:
        r"""
        Selects haupt leaf ``n``.

        ..  container:: example

            Selects haupt leaf 1:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.AfterGraceContainer("af'16 gf'16")
            >>> abjad.attach(container, staff[1])
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = baca.Selection(staff).hleaf(1)
            >>> result
            Note("d'8")

            >>> abjad.label.by_selector(result, lone=True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    c'8
                    \grace {
                        cf''16
                        bf'16
                    }
                    \abjad-color-music #'green
                    \afterGrace
                    d'8
                    {
                        af'16
                        gf'16
                    }
                    e'8
                    f'8
                }

        """
        return self.hleaves(exclude=exclude)[n]

    def hleaves(self, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects haupt leaves.

        ..  container:: example

            Selects haupt leaves:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
            >>> abjad.attach(container, staff[1])
            >>> container = abjad.AfterGraceContainer("af'16 gf'16")
            >>> abjad.attach(container, staff[1])
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = baca.Selection(staff).hleaves()
            >>> for item in result:
            ...     item
            ...
            Note("c'8")
            Note("d'8")
            Note("e'8")
            Note("f'8")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \grace {
                        cf''16
                        bf'16
                    }
                    \abjad-color-music #'blue
                    \afterGrace
                    d'8
                    {
                        af'16
                        gf'16
                    }
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'blue
                    f'8
                }

        """
        return self.leaves(exclude=exclude, grace=False)

    def lleaf(self, n: int = 0, *, exclude: abjad.Strings = None) -> abjad.Leaf:
        r"""
        Selects leaf ``n`` from leaves leaked to the left.

        ..  container:: example

            Selects leaf 0 from leaves (leaked to the left) in tuplet 1:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).tuplets()[1:2].lleaf(0)
            >>> result
            Chord("<d' e'>16")

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        \abjad-color-music #'green
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        return self.lleaves(exclude=exclude)[n]

    def lleak(self) -> abjad.Selection:
        r"""
        Leaks to the left.

        ..  container:: example

            Selects runs (each leaked to the left):

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = baca.Selection(staff).runs()
            >>> result = [baca.Selection(_).lleak() for _ in result]
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8")])
            Selection([Rest('r8'), Note("d'8"), Note("e'8")])
            Selection([Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'red
                    f'8
                    \abjad-color-music #'red
                    g'8
                    \abjad-color-music #'red
                    a'8
                }

        Returns new selection.
        """
        return self.with_previous_leaf()

    def lleaves(self, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects leaves, leaked to the left.

        ..  container:: example

            Selects leaves (leaked to the left) in tuplet 1:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).tuplets()[1:2].lleaves()
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

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        \abjad-color-music #'blue
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'red
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        return self.leaves(exclude=exclude).with_previous_leaf()

    def lparts(
        self, counts: typing.Sequence[int], *, exclude: abjad.Strings = None
    ) -> abjad.Selection:
        r"""
        Selects leaves partitioned by ``counts``.

        ..  container:: example

            Selects leaves partitioned 2, 3, 4:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).lparts([2, 3, 4])
            >>> for item in result:
            ...     item
            ...
            Selection([Rest('r16'), Note("bf'16")])
            Selection([Chord("<a'' b''>16"), Note("c'16"), Chord("<d' e'>4")])
            Selection([Chord("<d' e'>16"), Rest('r16'), Note("bf'16"), Chord("<a'' b''>16")])

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'blue
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        return super().leaves(exclude=exclude).partition_by_counts(counts=counts)

    def lt(self, n: int, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects logical tie ``n``.

        ..  container:: example

            Selects logical tie -1:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).lt(-1)
            >>> result
            LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        \abjad-color-music #'green
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'green
                        <fs' gs'>16
                    }
                }

        """
        return self.lts(exclude=exclude)[n]

    def ltleaf(self, n: int = 0, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects left-trimmed leaf ``n``.

        ..  container:: example

            Selects left-trimmed leaf 0:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 r4 r16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).ltleaf(0)
            >>> result
            Note("bf'16")

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        \abjad-color-music #'green
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        r4
                        r16
                    }
                }

        """
        return self.ltleaves(exclude=exclude)[n]

    def ltleaves(self, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects left-trimmed leaves.

        ..  container:: example

            Selects left-trimmed leaves:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 r4 r16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).ltleaves()
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
            Rest('r4')
            Rest('r16')

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        \abjad-color-music #'blue
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'red
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \abjad-color-music #'blue
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'blue
                        r4
                        \abjad-color-music #'red
                        r16
                    }
                }

        """
        return super().leaves(exclude=exclude, trim=abjad.Left)

    def ltqrun(self, n: int, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects logical tie equipitch run ``n``.

        ..  container:: example

            Selects logical tie equipitch run -1:

            >>> tuplets = [
            ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).ltqrun(-1)
            >>> result
            Selection([LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        c'16
                        c'16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        d'16
                        d'16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        e'16
                        e'16
                        e'16
                        \abjad-color-music #'green
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'green
                        <fs' gs'>16
                    }
                }

        """
        return self.ltqruns(exclude=exclude)[n]

    def ltqruns(self, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects logical tie equipitch runs.

        ..  container:: example

            Selects logical tie equipitch runs:

            >>> tuplets = [
            ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).ltqruns()
            >>> for item in result:
            ...     item
            ...
            Selection([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")])])
            Selection([LogicalTie([Chord("<d' e'>4"), Chord("<d' e'>16")])])
            Selection([LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")])])
            Selection([LogicalTie([Chord("<e' fs'>4"), Chord("<e' fs'>16")])])
            Selection([LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")])])
            Selection([LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        \abjad-color-music #'blue
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'blue
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'blue
                        <fs' gs'>16
                    }
                }

        """
        result = self.plts(exclude=exclude)
        result = result.group_by_pitch()
        assert isinstance(result, Selection)
        items = [Selection(_).group_by_contiguity() for _ in result]
        result = Selection(items)
        result = result.flatten(depth=1)
        assert isinstance(result, Selection)
        result = Selection([Selection(_) for _ in result])
        return result

    def ltrun(self, n: int, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects logical tie run ``n``.

        ..  container:: example

            Selects logical tie run -1:

            >>> tuplets = [
            ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).ltrun(-1)
            >>> result
            Selection([LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        c'16
                        c'16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        d'16
                        d'16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'green
                        <fs' gs'>16
                    }
                }

        """
        return self.ltruns(exclude=exclude)[n]

    def ltruns(self, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects logical tie runs.

        ..  container:: example

            Selects logical tie runs:

            >>> tuplets = [
            ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).ltruns()
            >>> for item in result:
            ...     item
            ...
            Selection([LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")]), LogicalTie([Note("c'16")]), LogicalTie([Chord("<d' e'>4"), Chord("<d' e'>16")])])
            Selection([LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")]), LogicalTie([Note("d'16")]), LogicalTie([Chord("<e' fs'>4"), Chord("<e' fs'>16")])])
            Selection([LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Note("e'16")]), LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])])

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'red
                        <fs' gs'>16
                    }
                }

        """
        result = self.logical_ties(exclude=exclude, pitched=True)
        result = result.group_by_contiguity()
        assert isinstance(result, Selection)
        result = Selection([Selection(_) for _ in result])
        return result

    def lts(
        self, *, exclude: abjad.Strings = None, nontrivial: bool = None
    ) -> abjad.Selection:
        r"""
        Selects logical ties.

        ..  container:: example

            Selects logical ties:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).lts()
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

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'blue
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        \abjad-color-music #'blue
                        c'16
                        \abjad-color-music #'red
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        \abjad-color-music #'blue
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'blue
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        \abjad-color-music #'blue
                        e'16
                        \abjad-color-music #'red
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'red
                        <fs' gs'>16
                    }
                }

        """
        return self.logical_ties(exclude=exclude, nontrivial=nontrivial)

    def mgroups(
        self,
        counts: typing.Sequence[int] = [1],
        *,
        exclude: abjad.Strings = None,
    ) -> "Selection":
        r"""
        Partitions measure-grouped leaves.

        ..  container:: example

            Partitions measure-grouped leaves into one part of length 2:

            >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r d''")
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
            >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

            >>> result = baca.Selection(staff).mgroups([2])
            >>> for item in result:
            ...     item
            ...
            Selection([Rest('r8'), Note("d'8"), Note("e'8"), Note("f'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'red
                    f'8
                    \time 3/8
                    g'8
                    a'8
                    b'8
                    \time 1/8
                    r8
                    d''8
                }

        """
        result = self.leaves(exclude=exclude)
        result = result.group_by_measure()
        result = result.partition_by_counts(counts)
        assert isinstance(result, Selection)
        result_ = Selection(Selection(_).flatten() for _ in result)
        assert isinstance(result_, Selection), repr(result_)
        return result_

    def mleaves(self, count: int, *, exclude: abjad.Strings = None) -> "Selection":
        r"""
        Selects all leaves in ``count`` measures.

        ..  container:: example

            Selects leaves in first three measures:

            >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r")
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
            >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

            >>> result = baca.Selection(staff).mleaves(3)
            >>> for item in result:
            ...     item
            ...
            Rest('r8')
            Note("d'8")
            Note("e'8")
            Note("f'8")
            Note("g'8")
            Note("a'8")
            Note("b'8")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'blue
                    f'8
                    \time 3/8
                    \abjad-color-music #'red
                    g'8
                    \abjad-color-music #'blue
                    a'8
                    \abjad-color-music #'red
                    b'8
                    \time 1/8
                    r8
                }

        ..  container:: example

            Selects leaves in last three measures:

            >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r")
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
            >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

            >>> result = baca.Selection(staff).mleaves(-3)
            >>> for item in result:
            ...     item
            ...
            Note("e'8")
            Note("f'8")
            Note("g'8")
            Note("a'8")
            Note("b'8")
            Rest('r8')

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    r8
                    d'8
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'blue
                    f'8
                    \time 3/8
                    \abjad-color-music #'red
                    g'8
                    \abjad-color-music #'blue
                    a'8
                    \abjad-color-music #'red
                    b'8
                    \time 1/8
                    \abjad-color-music #'blue
                    r8
                }

        """
        assert isinstance(count, int), repr(count)
        result = self.leaves(exclude=exclude).group_by_measure()
        if 0 < count:
            result = result[:count].flatten()
        elif count < 0:
            result = result[count:].flatten()
        else:
            raise Exception(count)
        return result

    def mmrest(
        self, n: int, *, exclude: abjad.Strings = None
    ) -> abjad.MultimeasureRest:
        r"""
        Selects multimeasure rest ``n``.

        ..  container:: example

            Selects multimeasure rest -1:

            >>> staff = abjad.Staff("R1 R1 R1")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = baca.Selection(staff).mmrest(-1)
            >>> result
            MultimeasureRest('R1')

            >>> abjad.label.by_selector(result, lone=True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    R1
                    R1
                    \abjad-color-music #'green
                    R1
                }

        """
        return self.mmrests(exclude=exclude)[n]

    def mmrests(self, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects multimeasure rests.

        ..  container:: example

            Selects multimeasure rests:

            >>> staff = abjad.Staff("R1 R1 R1")
            >>> abjad.setting(staff).autoBeaming = False
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).mmrests()
            >>> for item in result:
            ...     item
            ...
            MultimeasureRest('R1')
            MultimeasureRest('R1')
            MultimeasureRest('R1')

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    R1
                    \abjad-color-music #'blue
                    R1
                    \abjad-color-music #'red
                    R1
                }

        """
        return super().leaves(abjad.MultimeasureRest, exclude=exclude)

    def ntrun(self, n: int, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects nontrivial run ``n``.

        ..  container:: example

            Selects nontrivial run -1:

            >>> tuplets = [
            ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).ntrun(-1)
            >>> result
            Selection([Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        c'16
                        c'16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        d'16
                        d'16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        e'16
                        \abjad-color-music #'green
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'green
                        <fs' gs'>16
                    }
                }

        """
        return self.ntruns(exclude=exclude)[n]

    def ntruns(self, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects nontrivial runs.

        ..  container:: example

            Selects nontrivial runs:

            >>> tuplets = [
            ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).ntruns()
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'16"), Note("c'16"), Note("c'16"), Chord("<d' e'>4"), Chord("<d' e'>16")])
            Selection([Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16")])
            Selection([Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'red
                        <fs' gs'>16
                    }
                }

        """
        return self.runs(exclude=exclude).nontrivial()

    def omgroups(
        self,
        counts: typing.Sequence[int] = [1],
        *,
        exclude: abjad.Strings = None,
    ) -> "Selection":
        r"""
        Partitions measure-grouped leaves (with overhang).

        ..  container:: example

            Partitions measure-grouped leaves into one part of length 2 followed by an
            overhang part of remaining measures:

            >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r d''")
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
            >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

            >>> result = baca.Selection(staff).omgroups([2])
            >>> for item in result:
            ...     item
            ...
            Selection([Rest('r8'), Note("d'8"), Note("e'8"), Note("f'8")])
            Selection([Note("g'8"), Note("a'8"), Note("b'8"), Rest('r8'), Note("d''8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'red
                    d'8
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'red
                    f'8
                    \time 3/8
                    \abjad-color-music #'blue
                    g'8
                    \abjad-color-music #'blue
                    a'8
                    \abjad-color-music #'blue
                    b'8
                    \time 1/8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'blue
                    d''8
                }

        """
        result = self.leaves(exclude=exclude)
        result = result.group_by_measure()
        result = result.partition_by_counts(counts, overhang=True)
        assert isinstance(result, Selection)
        result_ = Selection(Selection(_).flatten() for _ in result)
        assert isinstance(result_, Selection), repr(result_)
        return result_

    def ompltgroups(
        self,
        counts: typing.Sequence[int] = [1],
        *,
        exclude: abjad.Strings = None,
    ) -> "Selection":
        """
        Partitions measure-grouped plts (with overhang).
        """
        result = self.plts(exclude=exclude)
        result = result.group_by_measure()
        result = result.partition_by_counts(counts, overhang=True)
        assert isinstance(result, Selection)
        result_ = Selection(Selection(_).flatten() for _ in result)
        assert isinstance(result_, Selection), repr(result_)
        return result_

    def phead(
        self, n: int, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Note, abjad.Chord]:
        r"""
        Selects pitched head ``n``.

        ..  container:: example

            Selects pitched head -1:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).phead(-1)
            >>> result
            Chord("<fs' gs'>4")

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        \abjad-color-music #'green
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        return self.pheads(exclude=exclude)[n]

    def pheads(
        self, *, exclude: abjad.Strings = None, grace: bool = None
    ) -> abjad.Selection:
        r"""
        Selects pitched heads.

        ..  container:: example

            Selects pitched heads:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).pheads()
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

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'blue
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        result = self.plts(exclude=exclude, grace=grace)
        assert isinstance(result, Selection)
        result = Selection(Selection(_)[0] for _ in result)
        return result

    def pleaf(
        self, n: int, *, exclude: abjad.Strings = None, grace: bool = None
    ) -> typing.Union[abjad.Note, abjad.Chord]:
        r"""
        Selects pitched leaf ``n``.

        ..  container:: example

            Selects pitched leaf -1:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).pleaf(-1)
            >>> result
            Chord("<fs' gs'>16")

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'green
                        <fs' gs'>16
                    }
                }

        """
        return self.pleaves(exclude=exclude, grace=grace)[n]

    def pleaves(
        self, *, exclude: abjad.Strings = None, grace: bool = None
    ) -> abjad.Selection:
        r"""
        Selects pitched leaves.

        ..  container:: example

            Selects pitched leaves:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).pleaves()
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

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        \abjad-color-music #'blue
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'red
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'blue
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'red
                        <fs' gs'>16
                    }
                }

        """
        return super().leaves(exclude=exclude, grace=grace, pitched=True)

    def plt(
        self, n: int, *, exclude: abjad.Strings = None, grace: bool = None
    ) -> abjad.Selection:
        r"""
        Selects pitched logical tie ``n``.

        ..  container:: example

            Selects pitched logical tie -1:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).plt(-1)
            >>> result
            LogicalTie([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        \abjad-color-music #'green
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'green
                        <fs' gs'>16
                    }
                }

        """
        return self.plts(exclude=exclude, grace=grace)[n]

    def plts(
        self, *, exclude: abjad.Strings = None, grace: bool = None
    ) -> abjad.Selection:
        r"""
        Selects pitched logical ties.

        ..  container:: example

            Selects pitched logical ties:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).plts()
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

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        \abjad-color-music #'blue
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'blue
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'blue
                        <fs' gs'>16
                    }
                }

        """
        return self.logical_ties(exclude=exclude, grace=grace, pitched=True)

    def ptail(
        self, n: int, *, exclude: abjad.Strings = None
    ) -> typing.Union[abjad.Note, abjad.Chord]:
        r"""
        Selects pitched tail ``n``.

        ..  container:: example

            Selects pitched tail -1:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).ptail(-1)
            >>> result
            Chord("<fs' gs'>16")

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'green
                        <fs' gs'>16
                    }
                }

        """
        return self.ptails(exclude=exclude)[n]

    def ptails(self, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects pitched tails.

        ..  container:: example

            Selects pitched tails:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).ptails()
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

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        c'16
                        <d' e'>4
                        ~
                        \abjad-color-music #'blue
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        d'16
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        e'16
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'blue
                        <fs' gs'>16
                    }
                }

        """
        result = self.plts(exclude=exclude)
        assert isinstance(result, Selection)
        result = Selection(Selection(_)[-1] for _ in result)
        return result

    def ptlt(self, n: int, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects pitched trivial logical tie ``n``.

        ..  container:: example

            Selects pitched trivial logical tie -1:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).ptlt(-1)
            >>> result
            LogicalTie([Note("e'16")])

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        \abjad-color-music #'green
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        return self.ptlts(exclude=exclude)[n]

    def ptlts(self, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects pitched trivial logical ties.

        ..  container:: example

            Selects pitched trivial logical ties:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).ptlts()
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

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        \abjad-color-music #'blue
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        \abjad-color-music #'blue
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        return self.logical_ties(exclude=exclude, nontrivial=False, pitched=True)

    def qrun(self, n: int, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects equipitch run ``n``.

        ..  container:: example

            Selects equipitch run -1:

            >>> tuplets = [
            ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).qrun(-1)
            >>> result
            Selection([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        c'16
                        c'16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        d'16
                        d'16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        e'16
                        e'16
                        e'16
                        \abjad-color-music #'green
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'green
                        <fs' gs'>16
                    }
                }

        """
        return self.qruns(exclude=exclude)[n]

    def qruns(self, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects equipitch runs.

        ..  container:: example

            Selects equipitch runs:

            >>> tuplets = [
            ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).qruns()
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'16"), Note("c'16"), Note("c'16")])
            Selection([Chord("<d' e'>4"), Chord("<d' e'>16")])
            Selection([Note("d'16"), Note("d'16"), Note("d'16")])
            Selection([Chord("<e' fs'>4"), Chord("<e' fs'>16")])
            Selection([Note("e'16"), Note("e'16"), Note("e'16")])
            Selection([Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        \abjad-color-music #'blue
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'blue
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'blue
                        <fs' gs'>16
                    }
                }

        """
        result = self.pleaves(exclude=exclude)
        result = result.group_by_pitch()
        assert isinstance(result, Selection)
        result = Selection(Selection(_).group_by_contiguity() for _ in result)
        result = result.flatten(depth=1)
        assert isinstance(result, Selection)
        result = Selection(Selection(_) for _ in result)
        return result

    def rleaf(self, n: int = 0, *, exclude: abjad.Strings = None) -> abjad.Leaf:
        r"""
        Selects leaf ``n`` from leaves leaked to the right.

        ..  container:: example

            Selects leaf -1 from leaves (leaked to the right) in tuplet 1:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).tuplets()[1:2].rleaf(-1)
            >>> result
            Rest('r16')

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \abjad-color-music #'green
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        return self.rleaves(exclude=exclude)[n]

    def rleak(self, *, grace: bool = None) -> abjad.Selection:
        r"""
        Leaks to the right.

        ..  container:: example

            Selects runs (each leaked to the right):

            >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
            >>> abjad.setting(staff).autoBeaming = False

            >>> result = baca.Selection(staff).runs()
            >>> result = [baca.Selection(_).rleak() for _ in result]
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'8"), Rest('r8')])
            Selection([Note("d'8"), Note("e'8"), Rest('r8')])
            Selection([Note("f'8"), Note("g'8"), Note("a'8")])

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \abjad-color-music #'red
                    c'8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'blue
                    e'8
                    \abjad-color-music #'blue
                    r8
                    \abjad-color-music #'red
                    f'8
                    \abjad-color-music #'red
                    g'8
                    \abjad-color-music #'red
                    a'8
                }

        Returns new selection.
        """
        return self.with_next_leaf(grace=grace)

    def rleaves(self, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects leaves, leaked to the right.

        ..  container:: example

            Selects leaves (leaked to the right) in tuplet 1:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).tuplets()[1:2].rleaves()
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

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'blue
                        bf'16
                        \abjad-color-music #'red
                        <a'' b''>16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'red
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \abjad-color-music #'red
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        return self.leaves(exclude=exclude).with_next_leaf()

    def rmleaves(self, count: int, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects all leaves in ``count`` measures, leaked one leaf to the right.

        ..  container:: example

            Selects leaves in first two measures, leaked on leaf to the right:

            >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r")
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
            >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

            >>> result = baca.Selection(staff).rmleaves(2)
            >>> for item in result:
            ...     item
            ...
            Rest('r8')
            Note("d'8")
            Note("e'8")
            Note("f'8")
            Note("g'8")

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                \with
                {
                    autoBeaming = ##f
                }
                {
                    \time 2/8
                    \abjad-color-music #'red
                    r8
                    \abjad-color-music #'blue
                    d'8
                    \abjad-color-music #'red
                    e'8
                    \abjad-color-music #'blue
                    f'8
                    \time 3/8
                    \abjad-color-music #'red
                    g'8
                    a'8
                    b'8
                    \time 1/8
                    r8
                }

        """
        assert isinstance(count, int), repr(count)
        return self.mleaves(count, exclude=exclude).rleak()

    def rrun(self, n: int, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects run ``n`` (leaked to the right).

        ..  container:: example

            Selects run 1 (leaked to the right):

            >>> tuplets = [
            ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).rrun(1)
            >>> result
            Selection([Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16"), Rest('r16')])

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        c'16
                        c'16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        \abjad-color-music #'green
                        d'16
                        \abjad-color-music #'green
                        d'16
                        \abjad-color-music #'green
                        d'16
                        \abjad-color-music #'green
                        <e' fs'>4
                        ~
                        \abjad-color-music #'green
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \abjad-color-music #'green
                        r16
                        e'16
                        e'16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        return self.rruns(exclude=exclude)[n]

    def rruns(self, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects runs (leaked to the right).

        ..  container:: example

            Selects runs (leaked to the right):

            >>> tuplets = [
            ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).rruns()
            >>> for item in result:
            ...     item
            ...
            Selection([Note("c'16"), Note("c'16"), Note("c'16"), Chord("<d' e'>4"), Chord("<d' e'>16"), Rest('r16')])
            Selection([Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16"), Rest('r16')])
            Selection([Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'red
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        \abjad-color-music #'red
                        r16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'blue
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \abjad-color-music #'blue
                        r16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'red
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'red
                        <fs' gs'>16
                    }
                }

        """
        result = self.runs(exclude=exclude)
        assert isinstance(result, Selection)
        result = Selection(Selection(_).rleak() for _ in result)
        return result

    def skip(self, n: int, *, exclude: abjad.Strings = None) -> abjad.Skip:
        r"""
        Selects skip ``n``.

        ..  container:: example

            Selects skip -1:

            >>> staff = abjad.Staff("c'8 s e' f' g' s b' s")
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
            >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

            >>> result = baca.Selection(staff).skip(-1)
            >>> result
            Skip('s8')

            >>> abjad.label.by_selector(result, lone=True)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
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

        """
        return self.skips(exclude=exclude)[n]

    def skips(self, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects skips.

        ..  container:: example

            Selects skips:

            >>> staff = abjad.Staff("c'8 s e' f' g' s b' s")
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
            >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
            >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

            >>> result = baca.Selection(staff).skips()
            >>> for item in result:
            ...     item
            Skip('s8')
            Skip('s8')
            Skip('s8')

            >>> abjad.label.by_selector(result)
            >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
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

        """
        return self.components(abjad.Skip, exclude=exclude)

    def tleaf(
        self, n: int = 0, *, exclude: abjad.Strings = None, grace: bool = None
    ) -> abjad.Leaf:
        r"""
        Selects trimmed leaf ``n``.

        ..  container:: example

            Selects trimmed leaf 0:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).tleaf(0)
            >>> result
            Note("bf'16")

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        \abjad-color-music #'green
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        return self.tleaves(exclude=exclude, grace=grace)[n]

    def tleaves(
        self, *, exclude: abjad.Strings = None, grace: bool = None
    ) -> abjad.Selection:
        r"""
        Selects trimmed leaves.

        ..  container:: example

            Selects trimmed leaves:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).tleaves()
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

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        c'16
                        \abjad-color-music #'blue
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        \abjad-color-music #'blue
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'red
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \abjad-color-music #'blue
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        e'16
                        \abjad-color-music #'blue
                        <fs' gs'>4
                        ~
                        \abjad-color-music #'red
                        <fs' gs'>16
                    }
                }

        """
        return super().leaves(exclude=exclude, grace=grace, trim=True)

    def wleaf(self, n: int = 0, *, exclude: abjad.Strings = None) -> abjad.Leaf:
        r"""
        Selects leaf ``n`` from leaves leaked wide.

        ..  container:: example

            Selects leaf 0 from leaves (leaked to both the left and right) in tuplet 1:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).tuplets()[1:2].wleaf(0)
            >>> result
            Chord("<d' e'>16")

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        \abjad-color-music #'green
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        ..  container:: example

            Selects leaf -1 from leaves (leaked to both the left and right) in tuplet 1:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).tuplets()[1:2].wleaf(-1)
            >>> result
            Rest('r16')

            >>> abjad.label.by_selector(result, lone=True)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        d'16
                        <e' fs'>4
                        ~
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \abjad-color-music #'green
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        return self.wleaves(exclude=exclude)[n]

    def wleaves(self, *, exclude: abjad.Strings = None) -> abjad.Selection:
        r"""
        Selects leaves, leaked "wide" (to both the left and right).

        ..  container:: example

            Selects leaves (leaked wide) in tuplet 1:

            >>> tuplets = [
            ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
            ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
            ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
            ... ]
            >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
            >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
            >>> tuplets = [abjad.select(tuplets)]

            >>> lilypond_file = abjad.illustrators.selection(tuplets)
            >>> staff = lilypond_file["Staff"]
            >>> abjad.setting(staff).autoBeaming = False
            >>> abjad.override(staff).TupletBracket.direction = abjad.Up
            >>> abjad.override(staff).TupletBracket.staff_padding = 3
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            >>> result = baca.Selection(staff).tuplets()[1:2].wleaves()
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

            >>> abjad.label.by_selector(result)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \context Staff = "Staff"
                \with
                {
                    \override TupletBracket.direction = #up
                    \override TupletBracket.staff-padding = 3
                    autoBeaming = ##f
                }
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \time 7/4
                        r16
                        bf'16
                        <a'' b''>16
                        c'16
                        <d' e'>4
                        ~
                        \abjad-color-music #'red
                        <d' e'>16
                    }
                    \times 8/9
                    {
                        \abjad-color-music #'blue
                        r16
                        \abjad-color-music #'red
                        bf'16
                        \abjad-color-music #'blue
                        <a'' b''>16
                        \abjad-color-music #'red
                        d'16
                        \abjad-color-music #'blue
                        <e' fs'>4
                        ~
                        \abjad-color-music #'red
                        <e' fs'>16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 10/9
                    {
                        \abjad-color-music #'blue
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        <fs' gs'>4
                        ~
                        <fs' gs'>16
                    }
                }

        """
        return self.leaves(exclude=exclude).with_previous_leaf().with_next_leaf()
