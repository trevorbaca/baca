"""
Select.
"""

import functools
import typing

import abjad

from . import sequence as _sequence
from . import typings as _typings


def chead(argument, n: int, *, exclude: _typings.Exclude | None = None) -> abjad.Chord:
    r"""
    Selects chord head ``n`` in ``argument``.

    Selects chord head -1:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.chead(staff, -1)
        >>> result
        Chord("<fs' gs'>4")

        >>> abjad.label.color_leaves(result, "#green")
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    return cheads(argument, exclude=exclude)[n]


def cheads(argument, *, exclude: _typings.Exclude | None = None) -> list[abjad.Chord]:
    r"""
    Selects chord heads in ``argument``.

    Selects chord heads:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    items = []
    prototype = abjad.Chord
    for item in abjad.select.leaves(argument, prototype, exclude=exclude, head=True):
        assert isinstance(item, prototype)
        items.append(item)
    return items


def clparts(
    argument,
    counts: typing.Sequence[int],
    *,
    exclude: _typings.Exclude | None = None,
) -> list[list[abjad.Leaf]]:
    r"""
    Selects leaves cyclically partitioned by ``counts`` (with overhang).

    Selects leaves cyclically partitioned 2, 3, 4:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
                    {
                        \abjad-color-music #'red
                        \time 7/4
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    leaves = abjad.select.leaves(argument, exclude=exclude)
    lists = abjad.select.partition_by_counts(
        leaves, counts=counts, cyclic=True, overhang=True
    )
    return lists


# TODO: maybe remove in favor of cyclic=True keyword to baca.select.mgroups()?
def cmgroups(
    argument, counts: list[int] = [1], *, exclude: _typings.Exclude | None = None
) -> list[list[abjad.Leaf]]:
    r"""
    Partitions measure-grouped leaves (cyclically).

    Partitions measure-grouped leaves into pairs:

    ..  container:: example

        >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r d''")
        >>> score = abjad.Score([staff])
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \time 2/8
                r8
                \abjad-color-music #'red
                d'8
                \abjad-color-music #'red
                e'8
                \abjad-color-music #'red
                f'8
                \abjad-color-music #'blue
                \time 3/8
                g'8
                \abjad-color-music #'blue
                a'8
                \abjad-color-music #'blue
                b'8
                \abjad-color-music #'blue
                \time 1/8
                r8
                d''8
            }

    """
    leaves = abjad.select.leaves(argument, exclude=exclude)
    result = abjad.select.group_by_measure(leaves)
    result = abjad.select.partition_by_counts(result, counts, cyclic=True)
    items = [abjad.select.flatten(_) for _ in result]
    return items


def duration(argument, string, *, preprolated: bool = False) -> list:
    result = []
    operator, duration = parse_duration_inequality_string(string)
    for item in argument:
        item_duration = abjad.get.duration(item, preprolated=preprolated)
        if (
            (operator == "==" and item_duration == duration)
            or (operator == "<=" and item_duration <= duration)
            or (operator == "<" and item_duration < duration)
            or (operator == ">=" and item_duration >= duration)
            or (operator == ">" and item_duration > duration)
        ):
            result.append(item)
    return result


def enchain(argument, counts: typing.Sequence[int]) -> list[list]:
    r"""
    Enchains items in argument.

    Enchains leaves in alternating groups of 5:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> for i, leaves in enumerate(result):
        ...     if i % 2 == 0:
        ...         color, direction = "#red", abjad.UP
        ...     else:
        ...         color, direction = "#blue", abjad.DOWN
        ...     string = rf'\markup {{ \bold \with-color {color} * }}'
        ...     for leaf in leaves:
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    lists = abjad.select.partition_by_counts(
        argument, counts=counts, cyclic=True, enchain=True, overhang=True
    )
    return lists


def grace(
    argument, n: int = 0, *, exclude: _typings.Exclude | None = None
) -> abjad.Leaf:
    r"""
    Selects grace ``n``.

    Selects grace -1:

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
        >>> abjad.attach(container, staff[1])
        >>> container = abjad.AfterGraceContainer("af'16 gf'16")
        >>> abjad.attach(container, staff[1])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = baca.select.grace(staff, -1)
        >>> result
        Note("gf'16")

        >>> abjad.label.color_leaves(result, "#green")
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


def graces(argument, *, exclude: _typings.Exclude | None = None) -> list[abjad.Leaf]:
    r"""
    Selects graces.

    Selects graces:

    ..  container:: example

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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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


def group_consecutive(components) -> list[list]:
    assert all(isinstance(_, abjad.Component) for _ in components), repr(components)
    groups = [components[:1]]
    previous_stop_offset = abjad.get.timespan(groups[-1][-1]).stop_offset
    for component in components[1:]:
        component_timespan = abjad.get.timespan(component)
        if component_timespan.start_offset == previous_stop_offset:
            groups[-1].append(component)
        else:
            groups.append([component])
        previous_stop_offset = component_timespan.stop_offset
    return groups


def has_grace_container(argument):
    result = []
    for item in argument:
        if (
            abjad.get.after_grace_container(item) is not None
            or abjad.get.before_grace_container(item) is not None
        ):
            result.append(item)
    return result


# TODO: change name to baca.select.nongrace_leaf()
def hleaf(
    argument, n: int = 0, *, exclude: _typings.Exclude | None = None
) -> abjad.Leaf:
    r"""
    Selects haupt leaf ``n``.

    Selects haupt leaf 1:

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> container = abjad.BeforeGraceContainer("cf''16 bf'16")
        >>> abjad.attach(container, staff[1])
        >>> container = abjad.AfterGraceContainer("af'16 gf'16")
        >>> abjad.attach(container, staff[1])
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = baca.select.hleaf(staff, 1)
        >>> result
        Note("d'8")

        >>> abjad.label.color_leaves(result, "#green")
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


# TODO: change name to baca.select.nongrace_leaves()
def hleaves(argument, *, exclude: _typings.Exclude | None = None) -> list[abjad.Leaf]:
    r"""
    Selects haupt leaves.

    Selects haupt leaves:

    ..  container:: example

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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
    argument,
    n: int = 0,
    *,
    count: int = 1,
    exclude: _typings.Exclude | None = None,
) -> abjad.Leaf:
    r"""
    Selects leaf ``n`` from leaves leaked to the left.

    Selects leaf 0 from leaves (leaked to the left) in tuplet 1:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.tuplet(staff, 1)
        >>> result = baca.select.lleaf(result, 0)
        >>> result
        Chord("<d' e'>16")

        >>> abjad.label.color_leaves(result, "#green")
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    return lleaves(argument, count=count, exclude=exclude)[n]


def lleak(argument, count: int = 1) -> list[abjad.Leaf]:
    r"""
    Leaks to the left.

    Selects runs (each leaked to the left):

    ..  container:: example

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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
    argument, *, count: int = 1, exclude: _typings.Exclude | None = None
) -> list[abjad.Leaf]:
    r"""
    Selects leaves, leaked to the left.

    Selects leaves (leaked to the left) in tuplet 1:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    leaves = abjad.select.leaves(argument, exclude=exclude)
    for _ in range(count):
        leaves = abjad.select.with_previous_leaf(leaves)
    return leaves


def lparts(
    argument,
    counts: typing.Sequence[int],
    *,
    exclude: _typings.Exclude | None = None,
    # TODO: change default to abjad.EXACT
    overhang: bool | abjad.enums.Comparison = False,
) -> list[list[abjad.Leaf]]:
    r"""
    Selects leaves partitioned by ``counts``.

    Selects leaves partitioned 2, 3, 4:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
                    {
                        \abjad-color-music #'red
                        \time 7/4
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    leaves = abjad.select.leaves(argument, exclude=exclude)
    lists = abjad.select.partition_by_counts(leaves, counts, overhang=overhang)
    return lists


def lt(
    argument, n: int, *, exclude: _typings.Exclude | None = None
) -> abjad.LogicalTie:
    r"""
    Selects logical tie ``n``.

    Selects logical tie -1:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.lt(staff, -1)
        >>> result
        LogicalTie(items=[Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

        >>> abjad.label.color_leaves(result, "#green")
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    return lts(argument, exclude=exclude)[n]


def ltleaf(
    argument, n: int = 0, *, exclude: _typings.Exclude | None = None
) -> abjad.Leaf:
    r"""
    Selects left-trimmed leaf ``n``.

    Selects left-trimmed leaf 0:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 r4 r16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.ltleaf(staff, 0)
        >>> result
        Note("bf'16")

        >>> abjad.label.color_leaves(result, "#green")
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
                    {
                        r16
                        bf'16
                        <a'' b''>16
                        e'16
                        r4
                        r16
                    }
                }
            }

    """
    return ltleaves(argument, exclude=exclude)[n]


def ltleaves(argument, *, exclude: _typings.Exclude | None = None) -> list[abjad.Leaf]:
    r"""
    Selects left-trimmed leaves.

    Selects left-trimmed leaves:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 r4 r16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    items = abjad.select.leaves(argument, exclude=exclude, trim=abjad.LEFT)
    return items


def ltqrun(
    argument, n: int, *, exclude: _typings.Exclude | None = None
) -> list[abjad.LogicalTie]:
    r"""
    Selects logical tie equipitch run ``n``.

    Selects logical tie equipitch run -1:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.ltqrun(staff, -1)
        >>> result
        [LogicalTie(items=[Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])]

        >>> abjad.label.color_leaves(result, "#green")
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    return ltqruns(argument, exclude=exclude)[n]


def ltqruns(
    argument, *, exclude: _typings.Exclude | None = None
) -> list[list[abjad.LogicalTie]]:
    r"""
    Selects logical tie equipitch runs.

    Selects logical tie equipitch runs:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    result_1 = plts(argument, exclude=exclude)
    result_2 = abjad.select.group_by_pitch(result_1)
    result_3 = [list(_) for _ in result_2]
    result_4 = [abjad.select.group_by_contiguity(_) for _ in result_3]
    result_5 = abjad.select.flatten(result_4, depth=1)
    result_6 = [list(_) for _ in result_5]
    return result_6


def ltrun(
    argument, n: int, *, exclude: _typings.Exclude | None = None
) -> list[abjad.LogicalTie]:
    r"""
    Selects logical tie run ``n``.

    Selects logical tie run -1:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.ltrun(staff, -1)
        >>> result
        [LogicalTie(items=[Note("e'16")]), LogicalTie(items=[Note("e'16")]), LogicalTie(items=[Note("e'16")]), LogicalTie(items=[Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])]

        >>> abjad.label.color_leaves(result, "#green")
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    return ltruns(argument, exclude=exclude)[n]


def ltruns(
    argument, *, exclude: _typings.Exclude | None = None
) -> list[list[abjad.LogicalTie]]:
    r"""
    Selects logical tie runs.

    Selects logical tie runs:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    lts = abjad.select.logical_ties(argument, exclude=exclude, pitched=True)
    result = abjad.select.group_by_contiguity(lts)
    return [list(_) for _ in result]


def lts(
    argument,
    *,
    exclude: _typings.Exclude | None = None,
    nontrivial: bool | None = None,
) -> list[abjad.LogicalTie]:
    r"""
    Selects logical ties.

    Selects logical ties:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
                    {
                        \abjad-color-music #'red
                        \time 7/4
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    return abjad.select.logical_ties(argument, exclude=exclude, nontrivial=nontrivial)


def mgroups(
    argument,
    counts: typing.Sequence[int] = [1],
    *,
    exclude: _typings.Exclude | None = None,
) -> list[list[abjad.Leaf]]:
    r"""
    Partitions measure-grouped leaves.

    Partitions measure-grouped leaves into one part of length 2:

    ..  container:: example

        >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r d''")
        >>> score = abjad.Score([staff])
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
        >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

        >>> result = baca.select.mgroups(staff, [2])
        >>> for item in result:
        ...     item
        ...
        [Rest('r8'), Note("d'8"), Note("e'8"), Note("f'8")]

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \time 2/8
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


def mleaves(
    argument, count: int, *, exclude: _typings.Exclude | None = None
) -> list[abjad.Leaf]:
    r"""
    Selects all leaves in ``count`` measures.

    Selects leaves in first three measures:

    ..  container:: example

        >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r")
        >>> score = abjad.Score([staff])
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \time 2/8
                r8
                \abjad-color-music #'blue
                d'8
                \abjad-color-music #'red
                e'8
                \abjad-color-music #'blue
                f'8
                \abjad-color-music #'red
                \time 3/8
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
        >>> score = abjad.Score([staff])
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \abjad-color-music #'red
                \time 3/8
                g'8
                \abjad-color-music #'blue
                a'8
                \abjad-color-music #'red
                b'8
                \abjad-color-music #'blue
                \time 1/8
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
    argument, n: int, *, exclude: _typings.Exclude | None = None
) -> abjad.MultimeasureRest:
    r"""
    Selects multimeasure rest ``n``.

    Selects multimeasure rest -1:

    ..  container:: example

        >>> staff = abjad.Staff("R1 R1 R1")
        >>> abjad.setting(staff).autoBeaming = False

        >>> result = baca.select.mmrest(staff, -1)
        >>> result
        MultimeasureRest('R1')

        >>> abjad.label.color_leaves(result, "#green")
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


def mmrests(
    argument, *, exclude: _typings.Exclude | None = None
) -> list[abjad.MultimeasureRest]:
    r"""
    Selects multimeasure rests.

    Selects multimeasure rests:

    ..  container:: example

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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
    leaves = abjad.select.leaves(argument, prototype, exclude=exclude)
    mmrests = []
    for leaf in leaves:
        assert isinstance(leaf, prototype)
        mmrests.append(leaf)
    return mmrests


def ntrun(
    argument, n: int, *, exclude: _typings.Exclude | None = None
) -> list[abjad.Leaf]:
    r"""
    Selects nontrivial run ``n``.

    Selects nontrivial run -1:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.ntrun(staff, -1)
        >>> result
        [Note("e'16"), Note("e'16"), Note("e'16"), Chord("<fs' gs'>4"), Chord("<fs' gs'>16")]

        >>> abjad.label.color_leaves(result, "#green")
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    return ntruns(argument, exclude=exclude)[n]


def ntruns(
    argument, *, exclude: _typings.Exclude | None = None
) -> list[list[abjad.Leaf]]:
    r"""
    Selects nontrivial runs.

    Selects nontrivial runs:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
    exclude: _typings.Exclude | None = None,
) -> list[list[abjad.Leaf]]:
    r"""
    Partitions measure-grouped leaves (with overhang).

    Partitions measure-grouped leaves into one part of length 2 followed by an
    overhang part of remaining measures:

    ..  container:: example

        >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r d''")
        >>> score = abjad.Score([staff])
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \time 2/8
                r8
                \abjad-color-music #'red
                d'8
                \abjad-color-music #'red
                e'8
                \abjad-color-music #'red
                f'8
                \abjad-color-music #'blue
                \time 3/8
                g'8
                \abjad-color-music #'blue
                a'8
                \abjad-color-music #'blue
                b'8
                \abjad-color-music #'blue
                \time 1/8
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
    exclude: _typings.Exclude | None = None,
) -> list[list[abjad.LogicalTie]]:
    """
    Partitions measure-grouped plts (with overhang).
    """
    result_1 = plts(argument, exclude=exclude)
    result_2 = abjad.select.group_by_measure(result_1)
    result_3 = abjad.select.partition_by_counts(result_2, counts, overhang=True)
    result_4 = [abjad.select.flatten(_) for _ in result_3]
    return result_4


def parse_duration_inequality_string(string) -> tuple[str, abjad.Duration]:
    """
    Parses duration inequality ``string``.

        >>> baca.select.parse_duration_inequality_string("3/16")
        ('==', Duration(3, 16))

        >>> baca.select.parse_duration_inequality_string("<=3/16")
        ('<=', Duration(3, 16))

        >>> baca.select.parse_duration_inequality_string("<3/16")
        ('<', Duration(3, 16))

    """
    for operator in ("<=", "<", ">=", ">"):
        if string.startswith(operator):
            fraction_string = string.removeprefix(operator)
            duration = abjad.Duration(fraction_string)
            break
    else:
        operator = "=="
        duration = abjad.Duration(string)
    return operator, duration


def partition_in_halves(argument) -> list[list]:
    durations = [abjad.get.duration(_) for _ in argument]
    maximum_denominator = max([_.denominator for _ in durations])
    pairs = [
        abjad.duration.pair_with_denominator(_, maximum_denominator) for _ in durations
    ]
    numerators = [_[0] for _ in pairs]
    lists = _sequence.partition_in_halves(numerators)
    counts = [len(_) for _ in lists]
    lists = abjad.select.partition_by_counts(argument, counts)
    return lists


def phead(
    argument, n: int, *, exclude: _typings.Exclude | None = None
) -> abjad.Note | abjad.Chord:
    r"""
    Selects pitched head ``n``.

    Selects pitched head -1:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.phead(staff, -1)
        >>> result
        Chord("<fs' gs'>4")

        >>> abjad.label.color_leaves(result, "#green")
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    return pheads(argument, exclude=exclude)[n]


# TODO: remove grace=None keyword
def pheads(
    argument, *, exclude: _typings.Exclude | None = None, grace: bool | None = None
) -> list[abjad.Note | abjad.Chord]:
    r"""
    Selects pitched heads.

    Selects pitched heads:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    result = plts(argument, exclude=exclude, grace=grace)
    return [_[0] for _ in result]


# TODO: remove grace=None keyword
def pleaf(
    argument,
    n: int,
    *,
    exclude: _typings.Exclude | None = None,
    grace: bool | None = None,
) -> abjad.Note | abjad.Chord:
    r"""
    Selects pitched leaf ``n``.

    Selects pitched leaf -1:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.pleaf(staff, -1)
        >>> result
        Chord("<fs' gs'>16")

        >>> abjad.label.color_leaves(result, "#green")
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    pleaf = pleaves(argument, exclude=exclude, grace=grace)[n]
    assert isinstance(pleaf, abjad.Note | abjad.Chord)
    return pleaf


# TODO: remove grace=None keyword
def pleaves(
    argument, *, exclude: _typings.Exclude | None = None, grace: bool | None = None
) -> list[abjad.Leaf]:
    r"""
    Selects pitched leaves.

    Selects pitched leaves:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    items = abjad.select.leaves(argument, exclude=exclude, grace=grace, pitched=True)
    return items


# TODO: remove grace=None keyword
def plt(
    argument,
    n: int,
    *,
    exclude: _typings.Exclude | None = None,
    grace: bool | None = None,
) -> abjad.LogicalTie:
    r"""
    Selects pitched logical tie ``n``.

    Selects pitched logical tie -1:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.plt(staff, -1)
        >>> result
        LogicalTie(items=[Chord("<fs' gs'>4"), Chord("<fs' gs'>16")])

        >>> abjad.label.color_leaves(result, "#green")
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    return plts(argument, exclude=exclude, grace=grace)[n]


# TODO: remove grace=None keyword
def plts(
    argument, *, exclude: _typings.Exclude | None = None, grace: bool | None = None
) -> list[abjad.LogicalTie]:
    r"""
    Selects pitched logical ties.

    Selects pitched logical ties:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    return abjad.select.logical_ties(
        argument, exclude=exclude, grace=grace, pitched=True
    )


def ptail(
    argument, n: int, *, exclude: _typings.Exclude | None = None
) -> abjad.Note | abjad.Chord:
    r"""
    Selects pitched tail ``n``.

    Selects pitched tail -1:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.ptail(staff, -1)
        >>> result
        Chord("<fs' gs'>16")

        >>> abjad.label.color_leaves(result, "#green")
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    return ptails(argument, exclude=exclude)[n]


def ptails(
    argument, *, exclude: _typings.Exclude | None = None
) -> list[abjad.Note | abjad.Chord]:
    r"""
    Selects pitched tails.

    Selects pitched tails:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    plts_ = plts(argument, exclude=exclude)
    leaves_ = [_[-1] for _ in plts_]
    return leaves_


def ptlt(
    argument, n: int, *, exclude: _typings.Exclude | None = None
) -> abjad.LogicalTie:
    r"""
    Selects pitched trivial logical tie ``n``.

    Selects pitched trivial logical tie -1:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.ptlt(staff, -1)
        >>> result
        LogicalTie(items=[Note("e'16")])

        >>> abjad.label.color_leaves(result, "#green")
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    return ptlts(argument, exclude=exclude)[n]


def ptlts(
    argument, *, exclude: _typings.Exclude | None = None
) -> list[abjad.LogicalTie]:
    r"""
    Selects pitched trivial logical ties.

    Selects pitched trivial logical ties:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    return abjad.select.logical_ties(
        argument, exclude=exclude, nontrivial=False, pitched=True
    )


def qrun(
    argument, n: int, *, exclude: _typings.Exclude | None = None
) -> list[abjad.Leaf]:
    r"""
    Selects equipitch run ``n``.

    Selects equipitch run -1:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.qrun(staff, -1)
        >>> result
        [Chord("<fs' gs'>4"), Chord("<fs' gs'>16")]

        >>> abjad.label.color_leaves(result, "#green")
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    return qruns(argument, exclude=exclude)[n]


def qruns(
    argument, *, exclude: _typings.Exclude | None = None
) -> list[list[abjad.Leaf]]:
    r"""
    Selects equipitch runs.

    Selects equipitch runs:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    pleaves_ = pleaves(argument, exclude=exclude)
    lists_ = [list(_) for _ in abjad.select.group_by_pitch(pleaves_)]
    lists_ = [[list(_) for _ in abjad.select.group_by_contiguity(_)] for _ in lists_]
    lists_ = abjad.select.flatten(lists_, depth=1)
    return lists_


def rest(argument, n: int):
    return abjad.select.rest(argument, n)


def rleaf(
    argument, n: int = 0, *, exclude: _typings.Exclude | None = None
) -> abjad.Leaf:
    r"""
    Selects leaf ``n`` from leaves leaked to the right.

    Selects leaf -1 from leaves (leaked to the right) in tuplet 1:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.tuplet(staff, 1)
        >>> result = baca.select.rleaf(result, -1)
        >>> result
        Rest('r16')

        >>> abjad.label.color_leaves(result, "#green")
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    return rleaves(argument, exclude=exclude)[n]


# TODO: remove grace=None keyword
def rleak(argument, *, count: int = 1, grace: bool | None = None) -> list[abjad.Leaf]:
    r"""
    Leaks to the right.

    Selects runs (each leaked to the right):

    ..  container:: example

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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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


def rleak_next_nonobgc_leaf(argument):
    result = rleak(argument)
    if abjad.get.parentage(result[-1]).get(abjad.OnBeatGraceContainer):
        result = rleak(argument, grace=False)
    return result


def rleak_final_item_next_nonobgc_leaf(argument):
    result = list(argument)
    result[-1] = rleak_next_nonobgc_leaf(argument[-1])
    return result


# TODO: remove grace=None keyword
def rleaves(
    argument,
    *,
    count: int = 1,
    exclude: _typings.Exclude | None = None,
    grace: bool | None = None,
) -> list[abjad.Leaf]:
    r"""
    Selects leaves, leaked to the right.

    Selects leaves (leaked to the right) in tuplet 1:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    leaves = abjad.select.leaves(argument, exclude=exclude, grace=grace)
    for _ in range(count):
        leaves = abjad.select.with_next_leaf(leaves, grace=grace)
    return leaves


def rmleaves(
    argument, count: int, *, exclude: _typings.Exclude | None = None
) -> list[abjad.Leaf]:
    r"""
    Selects all leaves in ``count`` measures, leaked one leaf to the right.

    Selects leaves in first two measures, leaked on leaf to the right:

    ..  container:: example

        >>> staff = abjad.Staff("r8 d' e' f' g' a' b' r")
        >>> score = abjad.Score([staff], name="Score")
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \time 2/8
                r8
                \abjad-color-music #'blue
                d'8
                \abjad-color-music #'red
                e'8
                \abjad-color-music #'blue
                f'8
                \abjad-color-music #'red
                \time 3/8
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


def rrun(
    argument, n: int, *, exclude: _typings.Exclude | None = None
) -> list[abjad.Leaf]:
    r"""
    Selects run ``n`` (leaked to the right).

    Selects run 1 (leaked to the right):

    ..  container:: example

        >>> tuplets = [
        ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.rrun(staff, 1)
        >>> result
        [Note("d'16"), Note("d'16"), Note("d'16"), Chord("<e' fs'>4"), Chord("<e' fs'>16"), Rest('r16')]

        >>> abjad.label.color_leaves(result, "#green")
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    return rruns(argument, exclude=exclude)[n]


def rruns(
    argument, *, exclude: _typings.Exclude | None = None
) -> list[list[abjad.Leaf]]:
    r"""
    Selects runs (leaked to the right).

    Selects runs (leaked to the right):

    ..  container:: example

        >>> tuplets = [
        ...     "r16 c'16 c'16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 d'16 d'16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 e'16 e'16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    result = abjad.select.runs(argument, exclude=exclude)
    lists_ = [rleak(_) for _ in result]
    return lists_


def runs(argument, *, exclude=None, rleak=False):
    result = abjad.select.runs(argument, exclude=exclude)
    if rleak is True:
        result = abjad.select.with_next_leaf(result)
    return result


def skip(argument, n: int, *, exclude: _typings.Exclude | None = None) -> abjad.Skip:
    r"""
    Selects skip ``n``.

    Selects skip -1:

    ..  container:: example

        >>> staff = abjad.Staff("c'8 s e' f' g' s b' s")
        >>> score = abjad.Score([staff], name="Score")
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.attach(abjad.TimeSignature((2, 8)), staff[0])
        >>> abjad.attach(abjad.TimeSignature((3, 8)), staff[4])
        >>> abjad.attach(abjad.TimeSignature((1, 8)), staff[7])

        >>> result = baca.select.skip(staff, -1)
        >>> result
        Skip('s8')

        >>> abjad.label.color_leaves(result, "#green")
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


def skips(argument, *, exclude: _typings.Exclude | None = None) -> list[abjad.Skip]:
    r"""
    Selects skips.

    Selects skips:

    ..  container:: example

        >>> staff = abjad.Staff("c'8 s e' f' g' s b' s")
        >>> score = abjad.Score([staff], name="Score")
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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


def sort_by_timeline(leaves):
    assert all(isinstance(_, abjad.Leaf) for _ in leaves), repr(leaves)

    def compare(leaf_1, leaf_2):
        start_offset_1 = abjad.get.timespan(leaf_1).start_offset
        start_offset_2 = abjad.get.timespan(leaf_2).start_offset
        if start_offset_1 < start_offset_2:
            return -1
        if start_offset_2 < start_offset_1:
            return 1
        index_1 = abjad.get.parentage(leaf_1).score_index()
        index_2 = abjad.get.parentage(leaf_2).score_index()
        if index_1 < index_2:
            return -1
        if index_2 < index_1:
            return 1
        return 0

    leaves = list(leaves)
    leaves.sort(key=functools.cmp_to_key(compare))
    return leaves


# TODO: remove grace=None keyword
def tleaf(
    argument,
    n: int = 0,
    *,
    exclude: _typings.Exclude | None = None,
    grace: bool | None = None,
) -> abjad.Leaf:
    r"""
    Selects trimmed leaf ``n``.

    Selects trimmed leaf 0:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = baca.select.tleaf(staff, 0)
        >>> result
        Note("bf'16")

        >>> abjad.label.color_leaves(result, "#green")
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    return tleaves(argument, exclude=exclude, grace=grace)[n]


# TODO: remove grace=None keyword
def tleaves(
    argument,
    *,
    exclude: _typings.Exclude | None = None,
    grace: bool | None = None,
) -> list[abjad.Leaf]:
    r"""
    Selects trimmed leaves.

    Selects trimmed leaves:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    items = abjad.select.leaves(argument, exclude=exclude, grace=grace, trim=True)
    return items


def tupletted(argument) -> list:
    r"""
    Selects tupletted items in ``argument``.

        >>> voice = abjad.Voice(r"c'4 d' \times 2/3 { e' f' g' }")

        >>> leaves = abjad.select.leaves(voice)
        >>> baca.select.tupletted(leaves)
        [Note("e'4"), Note("f'4"), Note("g'4")]

        >>> baca.select.tupletted(voice)
        []

    """
    result = []
    for item in argument:
        parentage = abjad.get.parentage(item).components()[1:]
        if any(isinstance(_, abjad.Tuplet) for _ in parentage):
            result.append(item)
    return result


def tupletted_first_leaf(argument) -> list:
    result = []
    for item in argument:
        first_leaf = abjad.select.leaf(item, 0)
        parentage = abjad.get.parentage(first_leaf).components()[1:]
        if any(isinstance(_, abjad.Tuplet) for _ in parentage):
            result.append(item)
    return result


def untupletted(argument) -> list:
    r"""
    Selects tupletted items in ``argument``.

        >>> voice = abjad.Voice(r"c'4 d' \times 2/3 { e' f' g' }")

        >>> leaves = abjad.select.leaves(voice)
        >>> baca.select.untupletted(leaves)
        [Note("c'4"), Note("d'4")]

        >>> baca.select.untupletted(voice)
        [Note("c'4"), Note("d'4"), Tuplet('3:2', "e'4 f'4 g'4")]

    """
    result = []
    for item in argument:
        parentage = abjad.get.parentage(item).components()[1:]
        if not any(isinstance(_, abjad.Tuplet) for _ in parentage):
            result.append(item)
    return result


def untupletted_first_leaf(argument) -> list:
    result = []
    for item in argument:
        first_leaf = abjad.select.leaf(item, 0)
        parentage = abjad.get.parentage(first_leaf).components()[1:]
        if not any(isinstance(_, abjad.Tuplet) for _ in parentage):
            result.append(item)
    return result


def wleaf(
    argument, n: int = 0, *, exclude: _typings.Exclude | None = None
) -> abjad.Leaf:
    r"""
    Selects leaf ``n`` from leaves leaked wide.

    Selects leaf 0 from leaves (leaked to both the left and right) in tuplet 1:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.tuplet(staff, 1)
        >>> result = baca.select.wleaf(result, 0)
        >>> result
        Chord("<d' e'>16")

        >>> abjad.label.color_leaves(result, "#green")
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    ..  container:: example

        Selects leaf -1 from leaves (leaked to both the left and right) in tuplet 1:

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
        >>> staff = lilypond_file["Staff"]
        >>> abjad.setting(staff).autoBeaming = False
        >>> abjad.override(staff).TupletBracket.direction = abjad.UP
        >>> abjad.override(staff).TupletBracket.staff_padding = 3
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        >>> result = abjad.select.tuplet(staff, 1)
        >>> result = baca.select.wleaf(result, -1)
        >>> result
        Rest('r16')

        >>> abjad.label.color_leaves(result, "#green")
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    return wleaves(argument, exclude=exclude)[n]


def wleaves(argument, *, exclude: _typings.Exclude | None = None) -> list[abjad.Leaf]:
    r"""
    Selects leaves, leaked "wide" (to both the left and right).

    Selects leaves (leaked wide) in tuplet 1:

    ..  container:: example

        >>> tuplets = [
        ...     "r16 bf'16 <a'' b''>16 c'16 <d' e'>4 ~ <d' e'>16",
        ...     "r16 bf'16 <a'' b''>16 d'16 <e' fs'>4 ~ <e' fs'>16",
        ...     "r16 bf'16 <a'' b''>16 e'16 <fs' gs'>4 ~ <fs' gs'>16",
        ... ]
        >>> tuplets = zip(["9:10", "9:8", "9:10"], tuplets, strict=True)
        >>> tuplets = [abjad.Tuplet(*_) for _ in tuplets]
        >>> rmakers.tweak_tuplet_number_text_calc_fraction_text(tuplets)
        >>> lilypond_file = abjad.illustrators.components(tuplets)
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

        >>> abjad.label.color_leaves(result, ["#red", "#blue"])
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
                \context Voice = "Voice"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 9/10
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
                    \tuplet 9/8
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
                    \tuplet 9/10
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
            }

    """
    items = abjad.select.leaves(argument, exclude=exclude)
    items = abjad.select.with_previous_leaf(items)
    items = abjad.select.with_next_leaf(items)
    return items
