import typing

import abjad


def _handle_pair(selection, pair):
    if isinstance(pair, tuple):
        if isinstance(pair[0], list):
            assert len(pair) == 2, repr(pair)
            indices, period = pair
            selection = abjad.select.get(selection, indices, period)
        else:
            start, stop = pair
            selection = selection[start:stop]
    elif isinstance(pair, list):
        selection = abjad.select.get(selection, pair)
    elif isinstance(pair, abjad.Pattern):
        selection = abjad.select.get(selection, pair)
    return selection


def chead(argument, n: int, *, exclude: abjad.Strings = None) -> abjad.Chord:
    r"""
    Selects chord head ``n`` in ``argument``.

    ..  container:: example

        Selects chord head -1:

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.chead(staff, -1)
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
    return cheads(argument, exclude=exclude)[n]


def cheads(argument, *, exclude: abjad.Strings = None) -> list[abjad.Chord]:
    r"""
    Selects chord heads in ``argument``.

    ..  container:: example

        Selects chord heads:

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip([(10, 9), (8, 9), (10, 9)], tuplets)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.cheads(staff)
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
    items = []
    prototype = abjad.Chord
    for item in abjad.select.leaves(argument, prototype, exclude=exclude, head=True):
        assert isinstance(item, prototype)
        items.append(item)
    return items


def clparts(
    argument, counts: typing.Sequence[int], *, exclude: abjad.Strings = None
) -> list[list[abjad.Leaf]]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.clparts(staff, [2, 3, 4])
        >>> for item in result:
        ...     item
        ...
        [Rest('r16'), Note("bf'16")]
        [Chord("<a'' b''>16"), Note("c'16"), Chord("<d' e'>4")]
        [Chord("<d' e'>16"), Rest('r16'), Note("bf'16"), Chord("<a'' b''>16")]
        [Note("d'16"), Chord("<e' fs'>4")]
        [Chord("<e' fs'>16"), Rest('r16'), Note("bf'16")]
        [Chord("<a'' b''>16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")]

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
    leaves = abjad.select.leaves(argument, exclude=exclude)
    selections = abjad.select.partition_by_counts(
        leaves, counts=counts, cyclic=True, overhang=True
    )
    lists_ = [list(_) for _ in selections]
    return lists_


def cmgroups(
    argument, counts: list[int] = [1], *, exclude: abjad.Strings = None
) -> list[list[abjad.Leaf]]:
    r"""
    Partitions measure-grouped leaves (cyclically).

    ..  container:: example

        Partitions measure-grouped leaves into pairs:

        >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r d''")
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
        >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

        >>> result = baca.select.cmgroups(staff, [2])
        >>> for item in result:
        ...     item
        ...
        [Rest('r8'), Note("d'8"), Note("e'8"), Note("f'8")]
        [Note("g'8"), Note("a'8"), Note("b'8"), Rest('r8')]

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
    leaves = abjad.select.leaves(argument, exclude=exclude)
    result = abjad.select.group_by_measure(leaves)
    result = abjad.select.partition_by_counts(result, counts, cyclic=True)
    items = [abjad.select.flatten(_) for _ in result]
    return items


def enchain(argument, counts: typing.Sequence[int]) -> list[list]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.leaves(staff)
        >>> result = baca.select.enchain(result, [5])
        >>> for item in result:
        ...     item
        [Rest('r16'), Note("bf'16"), Chord("<a'' b''>16"), Note("c'16"), Chord("<d' e'>4")]
        [Chord("<d' e'>4"), Chord("<d' e'>16"), Rest('r16'), Note("bf'16"), Chord("<a'' b''>16")]
        [Chord("<a'' b''>16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16"), Rest('r16')]
        [Rest('r16'), Note("bf'16"), Chord("<a'' b''>16"), Note("e'16"), Chord("<fs' gs'>4")]
        [Chord("<fs' gs'>4"), Chord("<fs' gs'>16")]

        >>> for i, selection in enumerate(result):
        ...     if i % 2 == 0:
        ...         color, direction = "#red", abjad.UP
        ...     else:
        ...         color, direction = "#blue", abjad.DOWN
        ...     string = rf'\markup {{ \bold \with-color {color} * }}'
        ...     for leaf in selection:
        ...         markup = abjad.Markup(string)
        ...         abjad.attach(markup, leaf, direction=direction)

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

    """
    selections = abjad.select.partition_by_counts(
        argument, counts=counts, cyclic=True, enchain=True, overhang=True
    )
    lists_ = [list(_) for _ in selections]
    return lists_


def grace(argument, n: int = 0, *, exclude: abjad.Strings = None) -> abjad.Leaf:
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

        >>> result = baca.select.grace(staff, -1)
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
    return graces(argument, exclude=exclude)[n]


def graces(argument, *, exclude: abjad.Strings = None) -> list[abjad.Leaf]:
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

        >>> result = baca.select.graces(staff)
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
    items = abjad.select.leaves(argument, exclude=exclude, grace=True)
    return items


def hleaf(argument, n: int = 0, *, exclude: abjad.Strings = None) -> abjad.Leaf:
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

        >>> result = baca.select.hleaf(staff, 1)
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
    return hleaves(argument, exclude=exclude)[n]


def hleaves(argument, *, exclude: abjad.Strings = None) -> list[abjad.Leaf]:
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

        >>> result = baca.select.hleaves(staff)
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
    return abjad.select.leaves(argument, exclude=exclude, grace=False)


def lleaf(
    argument, n: int = 0, *, count: int = 1, exclude: abjad.Strings = None
) -> abjad.Leaf:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.tuplet(staff, 1)
        >>> result = baca.select.lleaf(result, 0)
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
    return lleaves(argument, count=count, exclude=exclude)[n]


def lleak(argument, count: int = 1) -> list[abjad.Leaf]:
    r"""
    Leaks to the left.

    ..  container:: example

        Selects runs (each leaked to the left):

        >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.runs(staff)
        >>> result = [baca.select.lleak(_) for _ in result]
        >>> for item in result:
        ...     item
        ...
        [Note("c'8")]
        [Rest('r8'), Note("d'8"), Note("e'8")]
        [Rest('r8'), Note("f'8"), Note("g'8"), Note("a'8")]

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

    """
    for _ in range(count):
        argument = abjad.select.with_previous_leaf(argument)
    return argument


def lleaves(
    argument, *, count: int = 1, exclude: abjad.Strings = None
) -> list[abjad.Leaf]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.tuplet(staff, 1)
        >>> result = baca.select.lleaves(result)
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
    leaves = abjad.select.leaves(argument, exclude=exclude)
    for _ in range(count):
        leaves = abjad.select.with_previous_leaf(leaves)
    return leaves


def lparts(
    argument, counts: typing.Sequence[int], *, exclude: abjad.Strings = None
) -> list[list[abjad.Leaf]]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.lparts(staff, [2, 3, 4])
        >>> for item in result:
        ...     item
        ...
        [Rest('r16'), Note("bf'16")]
        [Chord("<a'' b''>16"), Note("c'16"), Chord("<d' e'>4")]
        [Chord("<d' e'>16"), Rest('r16'), Note("bf'16"), Chord("<a'' b''>16")]

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
    leaves = abjad.select.leaves(argument, exclude=exclude)
    selections = abjad.select.partition_by_counts(leaves, counts=counts)
    lists_ = [list(_) for _ in selections]
    return lists_


def lt(argument, n: int, *, exclude: abjad.Strings = None) -> abjad.LogicalTie:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.lt(staff, -1)
        >>> result
        LogicalTie(items=[Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

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
    return lts(argument, exclude=exclude)[n]


def ltleaf(argument, n: int = 0, *, exclude: abjad.Strings = None) -> abjad.Leaf:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.ltleaf(staff, 0)
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
    return ltleaves(argument, exclude=exclude)[n]


def ltleaves(argument, *, exclude: abjad.Strings = None) -> list[abjad.Leaf]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.ltleaves(staff)
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
    items = abjad.select.leaves(argument, exclude=exclude, trim=abjad.LEFT)
    return items


def ltqrun(
    argument, n: int, *, exclude: abjad.Strings = None
) -> list[abjad.LogicalTie]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.ltqrun(staff, -1)
        >>> result
        [LogicalTie(items=[Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])]

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
    return ltqruns(argument, exclude=exclude)[n]


def ltqruns(argument, *, exclude: abjad.Strings = None) -> list[list[abjad.LogicalTie]]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.ltqruns(staff)
        >>> for item in result:
        ...     item
        ...
        [LogicalTie(items=[Note("c'16")]), LogicalTie(items=[Note("c'16")]), LogicalTie(items=[Note("c'16")])]
        [LogicalTie(items=[Chord("<d' e'>4"), Chord("<d' e'>16")])]
        [LogicalTie(items=[Note("d'16")]), LogicalTie(items=[Note("d'16")]), LogicalTie(items=[Note("d'16")])]
        [LogicalTie(items=[Chord("<e' fs'>4"), Chord("<e' fs'>16")])]
        [LogicalTie(items=[Note("e'16")]), LogicalTie(items=[Note("e'16")]), LogicalTie(items=[Note("e'16")])]
        [LogicalTie(items=[Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])]

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
    result_1 = plts(argument, exclude=exclude)
    result_2 = abjad.select.group_by_pitch(result_1)
    result_3 = [list(_) for _ in result_2]
    result_4 = [abjad.select.group_by_contiguity(_) for _ in result_3]
    result_5 = abjad.select.flatten(result_4, depth=1)
    result_6 = [list(_) for _ in result_5]
    return result_6


def ltrun(argument, n: int, *, exclude: abjad.Strings = None) -> list[abjad.LogicalTie]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.ltrun(staff, -1)
        >>> result
        [LogicalTie(items=[Note("e'16")]), LogicalTie(items=[Note("e'16")]), LogicalTie(items=[Note("e'16")]), LogicalTie(items=[Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])]

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
    return ltruns(argument, exclude=exclude)[n]


def ltruns(argument, *, exclude: abjad.Strings = None) -> list[list[abjad.LogicalTie]]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.ltruns(staff)
        >>> for item in result:
        ...     item
        ...
        [LogicalTie(items=[Note("c'16")]), LogicalTie(items=[Note("c'16")]), LogicalTie(items=[Note("c'16")]), LogicalTie(items=[Chord("<d' e'>4"), Chord("<d' e'>16")])]
        [LogicalTie(items=[Note("d'16")]), LogicalTie(items=[Note("d'16")]), LogicalTie(items=[Note("d'16")]), LogicalTie(items=[Chord("<e' fs'>4"), Chord("<e' fs'>16")])]
        [LogicalTie(items=[Note("e'16")]), LogicalTie(items=[Note("e'16")]), LogicalTie(items=[Note("e'16")]), LogicalTie(items=[Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])]

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
    lts = abjad.select.logical_ties(argument, exclude=exclude, pitched=True)
    result = abjad.select.group_by_contiguity(lts)
    return [list(_) for _ in result]


def lts(
    argument, *, exclude: abjad.Strings = None, nontrivial: bool = None
) -> list[abjad.LogicalTie]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.lts(staff)
        >>> for item in result:
        ...     item
        ...
        LogicalTie(items=[Rest('r16')])
        LogicalTie(items=[Note("bf'16")])
        LogicalTie(items=[Chord("<a'' b''>16")])
        LogicalTie(items=[Note("c'16")])
        LogicalTie(items=[Chord("<d' e'>4"), Chord("<d' e'>16")])
        LogicalTie(items=[Rest('r16')])
        LogicalTie(items=[Note("bf'16")])
        LogicalTie(items=[Chord("<a'' b''>16")])
        LogicalTie(items=[Note("d'16")])
        LogicalTie(items=[Chord("<e' fs'>4"), Chord("<e' fs'>16")])
        LogicalTie(items=[Rest('r16')])
        LogicalTie(items=[Note("bf'16")])
        LogicalTie(items=[Chord("<a'' b''>16")])
        LogicalTie(items=[Note("e'16")])
        LogicalTie(items=[Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

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
    return abjad.select.logical_ties(argument, exclude=exclude, nontrivial=nontrivial)


def mgroups(
    argument,
    counts: typing.Sequence[int] = [1],
    *,
    exclude: abjad.Strings = None,
) -> list[list[abjad.Leaf]]:
    r"""
    Partitions measure-grouped leaves.

    ..  container:: example

        Partitions measure-grouped leaves into one part of length 2:

        >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r d''")
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
        >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

        >>> result = baca.select.mgroups(staff, [2])
        >>> for item in result:
        ...     item
        ...
        [Rest('r8'), Note("d'8"), Note("e'8"), Note("f'8")]

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
    leaves = abjad.select.leaves(argument, exclude=exclude)
    groups = abjad.select.group_by_measure(leaves)
    parts = abjad.select.partition_by_counts(groups, counts)
    result = [abjad.select.flatten(_) for _ in parts]
    return result


def mleaves(argument, count: int, *, exclude: abjad.Strings = None) -> list[abjad.Leaf]:
    r"""
    Selects all leaves in ``count`` measures.

    ..  container:: example

        Selects leaves in first three measures:

        >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r")
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
        >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

        >>> result = baca.select.mleaves(staff, 3)
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

        >>> result = baca.select.mleaves(staff, -3)
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
    leaves = abjad.select.leaves(argument, exclude=exclude)
    result = abjad.select.group_by_measure(leaves)
    if 0 < count:
        result_ = abjad.select.flatten(result[:count])
    elif count < 0:
        result_ = abjad.select.flatten(result[count:])
    else:
        raise Exception(count)
    return result_


def mmrest(
    argument, n: int, *, exclude: abjad.Strings = None
) -> abjad.MultimeasureRest:
    r"""
    Selects multimeasure rest ``n``.

    ..  container:: example

        Selects multimeasure rest -1:

        >>> staff = abjad.Staff("R1 R1 R1")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = baca.select.mmrest(staff, -1)
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
    items = mmrests(argument, exclude=exclude)
    mmrest = items[n]
    assert isinstance(mmrest, abjad.MultimeasureRest)
    return mmrest


def mmrests(argument, *, exclude: abjad.Strings = None) -> list[abjad.MultimeasureRest]:
    r"""
    Selects multimeasure rests.

    ..  container:: example

        Selects multimeasure rests:

        >>> staff = abjad.Staff("R1 R1 R1")
        >>> abjad.setting(staff).autoBeaming = False
        >>> lilypond_file = abjad.LilyPondFile([r'\include "abjad.ily"', staff])
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.mmrests(staff)
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
    prototype = abjad.MultimeasureRest
    items = abjad.select.leaves(argument, prototype, exclude=exclude)
    return items


def ntrun(argument, n: int, *, exclude: abjad.Strings = None) -> list[abjad.Leaf]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.ntrun(staff, -1)
        >>> result
        [Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")]

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
    return ntruns(argument, exclude=exclude)[n]


def ntruns(argument, *, exclude: abjad.Strings = None) -> list[list[abjad.Leaf]]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.ntruns(staff)
        >>> for item in result:
        ...     item
        ...
        [Note("c'16"), Note("c'16"), Note("c'16"), Chord("<d' e'>4"), Chord("<d' e'>16")]
        [Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16")]
        [Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")]

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
    runs = abjad.select.runs(argument, exclude=exclude)
    runs = abjad.select.nontrivial(runs)
    lists_ = [list(_) for _ in runs]
    return lists_


def omgroups(
    argument,
    counts: typing.Sequence[int] = [1],
    *,
    exclude: abjad.Strings = None,
) -> list[list[abjad.Leaf]]:
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

        >>> result = baca.select.omgroups(staff, [2])
        >>> for item in result:
        ...     item
        ...
        [Rest('r8'), Note("d'8"), Note("e'8"), Note("f'8")]
        [Note("g'8"), Note("a'8"), Note("b'8"), Rest('r8'), Note("d''8")]

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
    result_1 = abjad.select.leaves(argument, exclude=exclude)
    result_2 = abjad.select.group_by_measure(result_1)
    result_3 = abjad.select.partition_by_counts(result_2, counts, overhang=True)
    return [abjad.select.flatten(_) for _ in result_3]


def ompltgroups(
    argument,
    counts: typing.Sequence[int] = [1],
    *,
    exclude: abjad.Strings = None,
) -> list[list[abjad.LogicalTie]]:
    """
    Partitions measure-grouped plts (with overhang).
    """
    result_1 = plts(argument, exclude=exclude)
    result_2 = abjad.select.group_by_measure(result_1)
    result_3 = abjad.select.partition_by_counts(result_2, counts, overhang=True)
    result_4 = [abjad.select.flatten(_) for _ in result_3]
    return result_4


def phead(
    argument, n: int, *, exclude: abjad.Strings = None
) -> abjad.Note | abjad.Chord:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.phead(staff, -1)
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
    return pheads(argument, exclude=exclude)[n]


def pheads(
    argument, *, exclude: abjad.Strings = None, grace: bool = None
) -> list[abjad.Note | abjad.Chord]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.pheads(staff)
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
    result = plts(argument, exclude=exclude, grace=grace)
    return [_[0] for _ in result]


def pleaf(
    argument, n: int, *, exclude: abjad.Strings = None, grace: bool = None
) -> abjad.Note | abjad.Chord:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.pleaf(staff, -1)
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
    pleaf = pleaves(argument, exclude=exclude, grace=grace)[n]
    assert isinstance(pleaf, abjad.Note | abjad.Chord)
    return pleaf


def pleaves(
    argument, *, exclude: abjad.Strings = None, grace: bool = None
) -> list[abjad.Leaf]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.pleaves(staff)
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
    items = abjad.select.leaves(argument, exclude=exclude, grace=grace, pitched=True)
    return items


def plt(
    argument, n: int, *, exclude: abjad.Strings = None, grace: bool = None
) -> abjad.LogicalTie:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.plt(staff, -1)
        >>> result
        LogicalTie(items=[Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

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
    return plts(argument, exclude=exclude, grace=grace)[n]


def plts(
    argument, *, exclude: abjad.Strings = None, grace: bool = None
) -> list[abjad.LogicalTie]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.plts(staff)
        >>> for item in result:
        ...     item
        ...
        LogicalTie(items=[Note("bf'16")])
        LogicalTie(items=[Chord("<a'' b''>16")])
        LogicalTie(items=[Note("c'16")])
        LogicalTie(items=[Chord("<d' e'>4"), Chord("<d' e'>16")])
        LogicalTie(items=[Note("bf'16")])
        LogicalTie(items=[Chord("<a'' b''>16")])
        LogicalTie(items=[Note("d'16")])
        LogicalTie(items=[Chord("<e' fs'>4"), Chord("<e' fs'>16")])
        LogicalTie(items=[Note("bf'16")])
        LogicalTie(items=[Chord("<a'' b''>16")])
        LogicalTie(items=[Note("e'16")])
        LogicalTie(items=[Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

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
    return abjad.select.logical_ties(
        argument, exclude=exclude, grace=grace, pitched=True
    )


def ptail(
    argument, n: int, *, exclude: abjad.Strings = None
) -> abjad.Note | abjad.Chord:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.ptail(staff, -1)
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
    return ptails(argument, exclude=exclude)[n]


def ptail_in_each_tuplet(argument, n, pair=None):
    assert isinstance(n, int), repr(n)
    if pair is None:
        start, stop = None, None
    else:
        start, stop = pair
    selection = abjad.select.tuplets(argument)[start:stop]
    result = [ptail(_, n) for _ in selection]
    return result


def ptails(
    argument, *, exclude: abjad.Strings = None
) -> list[abjad.Note | abjad.Chord]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.ptails(staff)
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
    plts_ = plts(argument, exclude=exclude)
    leaves_ = [_[-1] for _ in plts_]
    return leaves_


def ptlt(argument, n: int, *, exclude: abjad.Strings = None) -> abjad.LogicalTie:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.ptlt(staff, -1)
        >>> result
        LogicalTie(items=[Note("e'16")])

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
    return ptlts(argument, exclude=exclude)[n]


def ptlts(argument, *, exclude: abjad.Strings = None) -> list[abjad.LogicalTie]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.ptlts(staff)
        >>> for item in result:
        ...     item
        ...
        LogicalTie(items=[Note("bf'16")])
        LogicalTie(items=[Chord("<a'' b''>16")])
        LogicalTie(items=[Note("c'16")])
        LogicalTie(items=[Note("bf'16")])
        LogicalTie(items=[Chord("<a'' b''>16")])
        LogicalTie(items=[Note("d'16")])
        LogicalTie(items=[Note("bf'16")])
        LogicalTie(items=[Chord("<a'' b''>16")])
        LogicalTie(items=[Note("e'16")])

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
    return abjad.select.logical_ties(
        argument, exclude=exclude, nontrivial=False, pitched=True
    )


def qrun(argument, n: int, *, exclude: abjad.Strings = None) -> list[abjad.Leaf]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.qrun(staff, -1)
        >>> result
        [Chord("<fs' gs'>4"), Chord("<fs' gs'>16")]

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
    return qruns(argument, exclude=exclude)[n]


def qruns(argument, *, exclude: abjad.Strings = None) -> list[list[abjad.Leaf]]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.qruns(staff)
        >>> for item in result:
        ...     item
        ...
        [Note("c'16"), Note("c'16"), Note("c'16")]
        [Chord("<d' e'>4"), Chord("<d' e'>16")]
        [Note("d'16"), Note("d'16"), Note("d'16")]
        [Chord("<e' fs'>4"), Chord("<e' fs'>16")]
        [Note("e'16"), Note("e'16"), Note("e'16")]
        [Chord("<fs' gs'>4"), Chord("<fs' gs'>16")]

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
    pleaves_ = pleaves(argument, exclude=exclude)
    lists_ = [list(_) for _ in abjad.select.group_by_pitch(pleaves_)]
    lists_ = [[list(_) for _ in abjad.select.group_by_contiguity(_)] for _ in lists_]
    lists_ = abjad.select.flatten(lists_, depth=1)
    return lists_


def rest(argument, n: int):
    return abjad.select.rest(argument, n)


def rleaf(argument, n: int = 0, *, exclude: abjad.Strings = None) -> abjad.Leaf:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.tuplet(staff, 1)
        >>> result = baca.select.rleaf(result, -1)
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
    return rleaves(argument, exclude=exclude)[n]


def rleak(argument, *, count: int = 1, grace: bool = None) -> list[abjad.Leaf]:
    r"""
    Leaks to the right.

    ..  container:: example

        Selects runs (each leaked to the right):

        >>> staff = abjad.Staff("c'8 r8 d'8 e'8 r8 f'8 g'8 a'8")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = abjad.select.runs(staff)
        >>> result = [baca.select.rleak(_) for _ in result]
        >>> for item in result:
        ...     item
        ...
        [Note("c'8"), Rest('r8')]
        [Note("d'8"), Note("e'8"), Rest('r8')]
        [Note("f'8"), Note("g'8"), Note("a'8")]

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

    """
    for _ in range(count):
        argument = abjad.select.with_next_leaf(argument, grace=grace)
    return argument


def rleak_runs(argument, start=0, stop=None):
    selection = abjad.select.runs(argument)
    if start != 0 or stop is not None:
        selection = selection[start:stop]
    runs = [rleaves(_) for _ in selection]
    return runs


def rleaves(
    argument, *, count: int = 1, exclude: abjad.Strings = None, grace: bool = None
) -> list[abjad.Leaf]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.tuplet(staff, 1)
        >>> result = baca.select.rleaves(result)
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
    leaves = abjad.select.leaves(argument, exclude=exclude, grace=grace)
    for _ in range(count):
        leaves = abjad.select.with_next_leaf(leaves, grace=grace)
    return leaves


def rmleaves(
    argument, count: int, *, exclude: abjad.Strings = None
) -> list[abjad.Leaf]:
    r"""
    Selects all leaves in ``count`` measures, leaked one leaf to the right.

    ..  container:: example

        Selects leaves in first two measures, leaked on leaf to the right:

        >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r")
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
        >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

        >>> result = baca.select.rmleaves(staff, 2)
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
    items = mleaves(argument, count, exclude=exclude)
    items_ = rleak(items)
    return items_


def rrun(argument, n: int, *, exclude: abjad.Strings = None) -> list[abjad.Leaf]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.rrun(staff, 1)
        >>> result
        [Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16"), Rest('r16')]

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
    return rruns(argument, exclude=exclude)[n]


def rruns(argument, *, exclude: abjad.Strings = None) -> list[list[abjad.Leaf]]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.rruns(staff)
        >>> for item in result:
        ...     item
        ...
        [Note("c'16"), Note("c'16"), Note("c'16"), Chord("<d' e'>4"), Chord("<d' e'>16"), Rest('r16')]
        [Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16"), Rest('r16')]
        [Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")]

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
    result = abjad.select.runs(argument, exclude=exclude)
    lists_ = [rleak(_) for _ in result]
    return lists_


def runs(argument, *, exclude=None, rleak=False):
    result = abjad.select.runs(argument, exclude=exclude)
    # result = _handle_pair(result, pair)
    if rleak is True:
        result = abjad.select.with_next_leaf(result)
    return result


def skip(argument, n: int, *, exclude: abjad.Strings = None) -> abjad.Skip:
    r"""
    Selects skip ``n``.

    ..  container:: example

        Selects skip -1:

        >>> staff = abjad.Staff("c'8 s e' f' g' s b' s")
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
        >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

        >>> result = baca.select.skip(staff, -1)
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
    skip = skips(argument, exclude=exclude)[n]
    assert isinstance(skip, abjad.Skip)
    return skip


def skips(argument, *, exclude: abjad.Strings = None) -> list[abjad.Component]:
    r"""
    Selects skips.

    ..  container:: example

        Selects skips:

        >>> staff = abjad.Staff("c'8 s e' f' g' s b' s")
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
        >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

        >>> result = baca.select.skips(staff)
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
    return abjad.select.components(argument, abjad.Skip, exclude=exclude)


def tleaf(
    argument, n: int = 0, *, exclude: abjad.Strings = None, grace: bool = None
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.tleaf(staff, 0)
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
    return tleaves(argument, exclude=exclude, grace=grace)[n]


def tleaves(
    argument,
    *,
    exclude: abjad.Strings = None,
    grace: bool = None,
    rleak: bool = False,
) -> list[abjad.Leaf]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.tleaves(staff)
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
    items = abjad.select.leaves(argument, exclude=exclude, grace=grace, trim=True)
    if rleak is True:
        items = abjad.select.with_next_leaf(items)
    return items


def tuplet(argument, n):
    return abjad.select.tuplet(argument, n)


def tuplets(argument, pair=None):
    result = abjad.select.tuplets(argument)
    result = _handle_pair(result, pair)
    return result


def wleaf(argument, n: int = 0, *, exclude: abjad.Strings = None) -> abjad.Leaf:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.tuplet(staff, 1)
        >>> result = baca.select.wleaf(result, 0)
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.tuplet(staff, 1)
        >>> result = baca.select.wleaf(result, -1)
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
    return wleaves(argument, exclude=exclude)[n]


def wleaves(argument, *, exclude: abjad.Strings = None) -> list[abjad.Leaf]:
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
        >>> lilypond_file = abjad.illustrators.selection(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.tuplet(staff, 1)
        >>> result = baca.select.wleaves(result)
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
    items = abjad.select.leaves(argument, exclude=exclude)
    items = abjad.select.with_previous_leaf(items)
    items = abjad.select.with_next_leaf(items)
    return items
