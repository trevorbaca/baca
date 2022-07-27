import dataclasses
import typing
from inspect import currentframe as _frame

import abjad

from . import command as _command
from . import commands as _commands
from . import select as _select
from . import tags as _tags
from . import tweaks as _tweaks
from . import typings as _typings
from .enums import enums as _enums


def _do_color_fingering_command(argument, numbers, *, direction=abjad.UP, tweaks=None):
    pheads = _select.pheads(argument)
    total = len(pheads)
    numbers = abjad.CyclicTuple(numbers)
    for i, phead in enumerate(pheads):
        number = numbers[i]
        if number != 0:
            fingering = abjad.ColorFingering(number)
            fingering = _tweaks.bundle_tweaks(fingering, tweaks, i=i, total=total)
            abjad.attach(fingering, phead, direction=direction)


def _prepare_alternate_bow_strokes(*tweaks, downbow_first, full):
    indicators: list[abjad.Articulation | abjad.Bundle]
    if downbow_first:
        if full:
            strings = ["baca-full-downbow", "baca-full-upbow"]
        else:
            strings = ["downbow", "upbow"]
    else:
        if full:
            strings = ["baca-full-upbow", "baca-full-downbow"]
        else:
            strings = ["upbow", "downbow"]
    indicators = [abjad.Articulation(_) for _ in strings]
    indicators = [_tweaks.bundle_tweaks(_, tweaks) for _ in indicators]
    return indicators


@dataclasses.dataclass(frozen=True, order=True, slots=True, unsafe_hash=True)
class ColorFingeringCommand(_command.Command):
    r"""
    Color fingering command.

    ..  container:: example

        With section-accumulator:

        >>> score = baca.docs.make_empty_score(1)
        >>> accumulator = baca.CommandAccumulator(
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ... )
        >>> baca.interpret.set_up_score(
        ...     score,
        ...     accumulator,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     docs=True,
        ... )

        >>> music = baca.make_notes(accumulator.get(), repeat_ties=True)
        >>> score["Music"].extend(music)
        >>> accumulator(
        ...     "Music",
        ...     baca.pitch("E4"),
        ...     baca.ColorFingeringCommand(numbers=[0, 1, 2, 1]),
        ... )

        >>> _, _ = baca.interpret.section(
        ...     score,
        ...     accumulator.manifests(),
        ...     accumulator.time_signatures,
        ...     commands=accumulator.commands,
        ...     move_global_context=True,
        ...     remove_tags=baca.tags.documentation_removal_tags(),
        ... )
        >>> lilypond_file = baca.lilypond.file(
        ...     score,
        ...     includes=["baca.ily"],
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            {
                \context Staff = "Staff"
                <<
                    \context Voice = "Skips"
                    {
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                        \time 4/8
                        s1 * 4/8
                        \time 3/8
                        s1 * 3/8
                    }
                    \context Voice = "Music"
                    {
                        e'2
                        e'4.
                        ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 1 }
                        e'2
                        ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 2 }
                        e'4.
                        ^ \markup { \override #'(circle-padding . 0.25) \circle \finger 1 }
                    }
                >>
            }

    """

    direction: abjad.Vertical | None = abjad.UP
    numbers: typing.Sequence[int] = ()
    tweaks: tuple[_typings.IndexedTweak, ...] = ()

    def __post_init__(self):
        _command.Command.__post_init__(self)
        assert abjad.math.all_are_nonnegative_integers(self.numbers)
        _tweaks.validate_indexed_tweaks(self.tweaks)

    def _call(self, *, argument=None, runtime=None) -> bool:
        if argument is None:
            return False
        if not self.numbers:
            return False
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return False
        _do_color_fingering_command(
            argument, self.numbers, direction=self.direction, tweaks=self.tweaks
        )
        return False


def accent(
    selector: typing.Callable = lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation(">")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def accent_function(
    argument,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    tag = abjad.Tag("baca.accent()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("accent")
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def alternate_bow_strokes(
    *tweaks: abjad.Tweak,
    downbow_first: bool = True,
    full: bool = False,
    selector: typing.Callable = lambda _: _select.pheads(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    indicators = _prepare_alternate_bow_strokes(
        *tweaks, downbow_first=downbow_first, full=full
    )
    return _commands.IndicatorCommand(
        indicators=indicators,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def alternate_bow_strokes_function(
    argument,
    *tweaks: abjad.Tweak,
    downbow_first: bool = True,
    full: bool = False,
    tags: list[abjad.Tag] = None,
) -> None:
    pass
    tag = abjad.Tag("baca.alternate_bow_strokes()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    indicators = _prepare_alternate_bow_strokes(
        *tweaks, downbow_first=downbow_first, full=full
    )
    indicators = abjad.CyclicTuple(indicators)
    leaves = abjad.select.leaves(argument)
    for i, leaf in enumerate(leaves):
        indicator = indicators[i]
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def arpeggio(
    selector: typing.Callable = lambda _: _select.chead(_, 0, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    r"""
    Attaches arpeggio.

    ..  container:: example

        Attaches arpeggio to chord head 0:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.arpeggio(),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 5/4
                        <c' d' bf'>8
                        - \arpeggio
                        [
                        ~
                        <c' d' bf'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        f''8
                        [
                        ~
                        f''32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <ef'' e'' fs'''>8
                        [
                        ~
                        <ef'' e'' fs'''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <g' af''>8
                        [
                        ~
                        <g' af''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'8
                        [
                        ~
                        a'32
                        ]
                        r16.
                    }
                }
            >>

    """
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("arpeggio")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def articulation(
    articulation: str,
    selector: typing.Callable = lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    articulation_ = abjad.Articulation(articulation)
    return _commands.IndicatorCommand(
        indicators=[articulation_],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def articulations(
    articulations: list,
    selector: typing.Callable = lambda _: _select.pheads(_, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=articulations,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def breathe(
    selector: typing.Callable = lambda _: _select.pleaf(_, -1, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
) -> _commands.IndicatorCommand:
    indicator: abjad.LilyPondLiteral | abjad.Bundle
    # TODO: change to abjad.Articulation("breathe", site="after")?
    indicator = abjad.LilyPondLiteral(r"\breathe", site="after")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return _commands.IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def breathe_function(
    leaf,
    *tweaks: abjad.Tweak,
    tags: list[abjad.Tag] = None,
) -> None:
    indicator: abjad.LilyPondLiteral | abjad.Bundle
    # TODO: change to abjad.Articulation("breathe", site="after")?
    indicator = abjad.LilyPondLiteral(r"\breathe", site="after")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    tag = abjad.Tag("baca.breathe()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    abjad.attach(
        indicator,
        leaf,
        tag=tag,
    )


def color_fingerings(
    numbers: list[int],
    *tweaks: _typings.IndexedTweak,
    selector: typing.Callable = lambda _: _select.pheads(_, exclude=_enums.HIDDEN),
) -> ColorFingeringCommand:
    return ColorFingeringCommand(numbers=numbers, selector=selector, tweaks=tweaks)


def color_fingerings_function(
    argument,
    numbers: list[int],
    *tweaks: _typings.IndexedTweak,
) -> None:
    _do_color_fingering_command(argument, numbers, tweaks=tweaks)


def damp(
    *tweaks: abjad.Tweak,
    selector: typing.Callable = lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    indicator: abjad.Articulation | abjad.Bundle
    indicator = abjad.Articulation("baca-damp")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return _commands.IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def double_flageolet(
    selector: typing.Callable = lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("baca-double-flageolet")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def double_staccato(
    selector: typing.Callable = lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    r"""
    Attaches double-staccato.

    ..  container:: example

        Attaches double-staccato to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.double_staccato(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["baca.ily"]
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        - \baca-staccati #2
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("baca-staccati #2")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def double_staccato_function(
    argument,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    tag = abjad.Tag("baca.double_staccato()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("baca-staccati #2")
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def down_arpeggio(
    selector: typing.Callable = lambda _: _select.chead(_, 0, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    r"""
    Attaches down-arpeggio.

    ..  container:: example

        Attaches down-arpeggio to chord head 0:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.down_arpeggio(),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \arpeggioArrowDown
                        \time 5/4
                        <c' d' bf'>8
                        \arpeggio
                        [
                        ~
                        <c' d' bf'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        f''8
                        [
                        ~
                        f''32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <ef'' e'' fs'''>8
                        [
                        ~
                        <ef'' e'' fs'''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <g' af''>8
                        [
                        ~
                        <g' af''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'8
                        [
                        ~
                        a'32
                        ]
                        r16.
                    }
                }
            >>

    """
    return _commands.IndicatorCommand(
        indicators=[abjad.Arpeggio(direction=abjad.DOWN)],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def down_bow(
    selector: typing.Callable = lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
    full: bool = False,
) -> _commands.IndicatorCommand:
    r"""
    Attaches down-bow.

    ..  container:: example

        Attaches down-bow to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.down_bow(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["baca.ily"]
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        - \downbow
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Attaches full down-bow to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.down_bow(full=True),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["baca.ily"]
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        - \baca-full-downbow
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    indicator: abjad.Articulation | abjad.Bundle
    if full:
        indicator = abjad.Articulation("baca-full-downbow")
    else:
        indicator = abjad.Articulation("downbow")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return _commands.IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def down_bow_function(
    leaf: abjad.Leaf,
    *tweaks: abjad.Tweak,
    full: bool = False,
    tags: list[abjad.Tag] = None,
) -> None:
    assert isinstance(leaf, abjad.Leaf), repr(leaf)
    indicator: abjad.Articulation | abjad.Bundle
    if full:
        indicator = abjad.Articulation("baca-full-downbow")
    else:
        indicator = abjad.Articulation("downbow")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    tag = abjad.Tag("baca.down_bow()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    abjad.attach(
        indicator,
        leaf,
        tag=tag,
    )


def espressivo(
    selector: typing.Callable = lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
) -> _commands.IndicatorCommand:
    r"""
    Attaches espressivo.

    ..  container:: example

        Attaches espressivo to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.espressivo(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        - \espressivo
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    indicator: abjad.Articulation | abjad.Bundle
    indicator = abjad.Articulation("espressivo")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return _commands.IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def espressivo_function(
    leaf,
    *tweaks: abjad.Tweak,
    tags: list[abjad.Tag] = None,
) -> None:
    indicator: abjad.Articulation | abjad.Bundle
    indicator = abjad.Articulation("espressivo")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    tag = abjad.Tag("baca.espressivo()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    abjad.attach(
        indicator,
        leaf,
        tag=tag,
    )


def fermata(
    selector: typing.Callable = lambda _: abjad.select.leaf(_, 0),
) -> _commands.IndicatorCommand:
    r"""
    Attaches fermata.

    ..  container:: example

        Attaches fermata to first leaf:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.fermata(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        - \fermata
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("fermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def flageolet(
    selector: typing.Callable = lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    r"""
    Attaches flageolet.

    ..  container:: example

        Attaches flageolet to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.flageolet(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        - \flageolet
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("flageolet")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def laissez_vibrer(
    selector: typing.Callable = lambda _: _select.ptail(_, 0, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    r"""
    Attaches laissez vibrer.

    ..  container:: example

        Attaches laissez vibrer to PLT tail 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.laissez_vibrer(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        \laissezVibrer
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return _commands.IndicatorCommand(
        indicators=[abjad.LaissezVibrer()],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def laissez_vibrer_function(
    argument,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    tag = abjad.Tag("baca.laissez_vibrer()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.LaissezVibrer()
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def long_fermata(
    selector: typing.Callable = lambda _: abjad.select.leaf(_, 0),
) -> _commands.IndicatorCommand:
    r"""
    Attaches long fermata.

    ..  container:: example

        Attaches long fermata to first leaf:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.long_fermata(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        - \longfermata
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("longfermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def marcato(
    selector: typing.Callable = lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    r"""
    Attaches marcato.

    ..  container:: example

        Attaches marcato to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.marcato(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        - \marcato
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("marcato")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def marcato_function(
    argument,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    tag = abjad.Tag("baca.marcato()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("marcato")
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def short_fermata(
    selector: typing.Callable = lambda _: abjad.select.leaf(_, 0),
) -> _commands.IndicatorCommand:
    r"""
    Attaches short fermata.

    ..  container:: example

        Attaches short fermata to first leaf:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.short_fermata(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        - \shortfermata
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("shortfermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def snap_pizzicato(
    selector: typing.Callable = lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("snappizzicato")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def staccatissimo(
    selector: typing.Callable = lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    r"""
    Attaches staccatissimo.

    ..  container:: example

        Attaches staccatissimo to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.staccatissimo(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        - \staccatissimo
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("staccatissimo")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def staccatissimo_function(
    argument,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    tag = abjad.Tag("baca.staccatissimo()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("staccatissimo")
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def staccato(
    selector: typing.Callable = lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("staccato")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def staccato_function(
    argument,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    tag = abjad.Tag("baca.staccato()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("staccato")
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def stem_tremolo(
    selector: typing.Callable = lambda _: _select.pleaf(_, 0, exclude=_enums.HIDDEN),
    *,
    tremolo_flags: int = 32,
) -> _commands.IndicatorCommand:
    r"""
    Attaches stem tremolo.

    ..  container:: example

        Attaches stem tremolo to pitched leaf 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.stem_tremolo(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        :32
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return _commands.IndicatorCommand(
        indicators=[abjad.StemTremolo(tremolo_flags=tremolo_flags)],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def stem_tremolo_function(
    argument,
    *,
    tremolo_flags: int = 32,
    tags: list[abjad.Tag] = None,
) -> None:
    indicator = abjad.StemTremolo(tremolo_flags=tremolo_flags)
    tag = abjad.Tag("baca.stem_tremolo()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    for leaf in abjad.select.leaves(argument):
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def stop_on_string(
    selector: typing.Callable = lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
    *,
    map=None,
) -> _commands.IndicatorCommand:
    r"""
    Attaches stop-on-string.

    ..  container:: example

        Attaches stop-on-string to pitched head -1:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.stop_on_string(
        ...         selector=lambda _: baca.select.pleaf(_, -1),
        ...     ),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(
        ...     selection, includes=["baca.ily"]
        ... )
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        - \baca-stop-on-string
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    articulation = abjad.Articulation("baca-stop-on-string")
    return _commands.IndicatorCommand(
        indicators=[articulation],
        map=map,
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def tenuto(
    selector: typing.Callable = lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    r"""
    Attaches tenuto.

    ..  container:: example

        Attaches tenuto to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tenuto(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        - \tenuto
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("tenuto")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def tenuto_function(
    argument,
    *,
    tags: list[abjad.Tag] = None,
) -> None:
    tag = abjad.Tag("baca.tenuto()")
    for tag_ in tags or []:
        tag = tag.append(tag_)
    for leaf in abjad.iterate.leaves(argument):
        indicator = abjad.Articulation("tenuto")
        abjad.attach(
            indicator,
            leaf,
            tag=tag,
        )


def triple_staccato(
    selector: typing.Callable = lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("baca-staccati #3")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def up_arpeggio(
    selector: typing.Callable = lambda _: _select.chead(_, 0, exclude=_enums.HIDDEN),
) -> _commands.IndicatorCommand:
    r"""
    Attaches up-arpeggio.

    ..  container:: example

        Attaches up-arpeggios to chord head 0:

        >>> stack = baca.stack(
        ...     baca.figure([5, -3], 32),
        ...     rmakers.beam(),
        ...     baca.up_arpeggio(),
        ... )
        >>> selection = stack([{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \arpeggioArrowUp
                        \time 5/4
                        <c' d' bf'>8
                        \arpeggio
                        [
                        ~
                        <c' d' bf'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        f''8
                        [
                        ~
                        f''32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <ef'' e'' fs'''>8
                        [
                        ~
                        <ef'' e'' fs'''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <g' af''>8
                        [
                        ~
                        <g' af''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'8
                        [
                        ~
                        a'32
                        ]
                        r16.
                    }
                }
            >>

    """
    return _commands.IndicatorCommand(
        indicators=[abjad.Arpeggio(direction=abjad.UP)],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def up_bow(
    selector: typing.Callable = lambda _: _select.phead(_, 0, exclude=_enums.HIDDEN),
    *tweaks: abjad.Tweak,
    full: bool = False,
) -> _commands.IndicatorCommand:
    r"""
    Attaches up-bow.

    ..  container:: example

        Attaches up-bow to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ...     baca.up_bow(),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        - \upbow
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    indicator: abjad.Articulation | abjad.Bundle
    if full:
        indicator = abjad.Articulation("baca-full-upbow")
    else:
        indicator = abjad.Articulation("upbow")
    indicator = _tweaks.bundle_tweaks(indicator, tweaks)
    return _commands.IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )


def very_long_fermata(
    selector: typing.Callable = lambda _: abjad.select.leaf(_, 0),
) -> _commands.IndicatorCommand:
    r"""
    Attaches very long fermata.

    ..  container:: example

        Attaches very long fermata to first leaf:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.very_long_fermata(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        >>> lilypond_file = abjad.illustrators.selection(selection)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> score = lilypond_file["Score"]
            >>> string = abjad.lilypond(score)
            >>> print(string)
            \context Score = "Score"
            <<
                \context Staff = "Staff"
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        - \verylongfermata
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    return _commands.IndicatorCommand(
        indicators=[abjad.Articulation("verylongfermata")],
        selector=selector,
        tags=[_tags.function_name(_frame())],
    )
