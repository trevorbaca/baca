"""
Indicator commands.
"""
import inspect
import typing

import abjad

from . import commandclasses, const, indicators, scoping
from . import selection as _selection
from . import tags as _tags


def _site(frame):
    prefix = "baca"
    return scoping.site(frame, prefix)


### FACTORY FUNCTIONS ###


def accent(
    selector=lambda _: _selection.Selection(_).phead(0, exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
    r"""
    Attaches accent.

    ..  container:: example

        Attaches accent to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.accent(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        - \accent
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
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Articulation(">")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def alternate_bow_strokes(
    selector=lambda _: _selection.Selection(_).pheads(exclude=const.HIDDEN),
    *tweaks: abjad.TweakInterface,
    downbow_first: bool = True,
    full: bool = None,
) -> commandclasses.IndicatorCommand:
    r"""
    Attaches alternate bow strokes.

    ..  container:: example

        Attaches alternate bow strokes to pitched heads (down-bow first):

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.alternate_bow_strokes(downbow_first=True),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
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
                        - \upbow
                        ]
                        bf'4
                        - \downbow
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        - \upbow
                        [
                        e''16
                        - \downbow
                        ]
                        ef''4
                        - \upbow
                        ~
                        ef''16
                        r16
                        af''16
                        - \downbow
                        [
                        g''16
                        - \upbow
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        - \downbow
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Attaches alternate bow strokes to pitched heads (up-bow first):

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.alternate_bow_strokes(downbow_first=False),
        ...     baca.tuplet_bracket_staff_padding(6),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 6
                        \time 11/8
                        r8
                        c'16
                        - \upbow
                        [
                        d'16
                        - \downbow
                        ]
                        bf'4
                        - \upbow
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        - \downbow
                        [
                        e''16
                        - \upbow
                        ]
                        ef''4
                        - \downbow
                        ~
                        ef''16
                        r16
                        af''16
                        - \upbow
                        [
                        g''16
                        - \downbow
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        - \upbow
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    ..  container:: example

        Attaches alternate full bow strokes to pitched heads:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.alternate_bow_strokes(full=True),
        ...     baca.tuplet_bracket_staff_padding(6),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(
            ...     selection, includes=["baca.ily"]
            ... )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 6
                        \time 11/8
                        r8
                        c'16
                        - \baca-full-downbow
                        [
                        d'16
                        - \baca-full-upbow
                        ]
                        bf'4
                        - \baca-full-downbow
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        fs''16
                        - \baca-full-upbow
                        [
                        e''16
                        - \baca-full-downbow
                        ]
                        ef''4
                        - \baca-full-upbow
                        ~
                        ef''16
                        r16
                        af''16
                        - \baca-full-downbow
                        [
                        g''16
                        - \baca-full-upbow
                        ]
                    }
                    \times 4/5
                    {
                        a'16
                        - \baca-full-downbow
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
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
    return commandclasses.IndicatorCommand(
        indicators=indicators,
        selector=selector,
        tags=[_site(inspect.currentframe())],
        tweaks=tweaks,
    )


def arpeggio(
    selector=lambda _: _selection.Selection(_).chead(0, exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
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

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \time 5/4
                        <c' d' bf'>8
                        - \arpeggio
                        ~
                        [
                        <c' d' bf'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        f''8
                        ~
                        [
                        f''32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <ef'' e'' fs'''>8
                        ~
                        [
                        <ef'' e'' fs'''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <g' af''>8
                        ~
                        [
                        <g' af''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'8
                        ~
                        [
                        a'32
                        ]
                        r16.
                    }
                }
            >>

    """
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Articulation("arpeggio")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def articulation(
    articulation: str,
    selector=lambda _: _selection.Selection(_).phead(0, exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
    """
    Attaches articulation.
    """
    articulation_ = abjad.Articulation(articulation)
    return commandclasses.IndicatorCommand(
        indicators=[articulation_],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def articulations(
    articulations: typing.List,
    selector=lambda _: _selection.Selection(_).pheads(exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
    """
    Attaches articulations.
    """
    return commandclasses.IndicatorCommand(
        indicators=articulations,
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def bar_line(
    abbreviation: str = "|",
    selector=lambda _: _selection.Selection(_).leaf(0),
    *,
    format_slot: str = "after",
) -> commandclasses.IndicatorCommand:
    """
    Attaches bar line.
    """
    indicator = abjad.BarLine(abbreviation, format_slot=format_slot)
    return commandclasses.IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def breathe(
    selector=lambda _: _selection.Selection(_).pleaf(-1, exclude=const.HIDDEN),
    *tweaks: abjad.TweakInterface,
) -> commandclasses.IndicatorCommand:
    """
    Attaches breathe command.
    """
    # TODO: change to abjad.Articulation("breathe", format_slot="after")?
    breathe = abjad.LilyPondLiteral(r"\breathe", format_slot="after")
    return commandclasses.IndicatorCommand(
        indicators=[breathe],
        selector=selector,
        tags=[_site(inspect.currentframe())],
        tweaks=tweaks,
    )


def clef(
    clef: str = "treble",
    selector=lambda _: _selection.Selection(_).leaf(0),
    *,
    redundant: bool = None,
) -> commandclasses.IndicatorCommand:
    r"""
    Attaches clef.

    ..  container:: example

        Attaches clef to leaf 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.clef('alto'),
        ...     baca.tuplet_bracket_staff_padding(7),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 7
                        \time 11/8
                        \clef "alto"
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
                        r4
                        \revert TupletBracket.staff-padding
                    }
                }
            >>

    """
    indicator = abjad.Clef(clef)
    return commandclasses.IndicatorCommand(
        indicators=[indicator],
        redundant=redundant,
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def damp(
    selector=lambda _: _selection.Selection(_).phead(0, exclude=const.HIDDEN),
    *tweaks: abjad.TweakInterface,
) -> commandclasses.IndicatorCommand:
    """
    Attaches damp.
    """
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Articulation("baca-damp")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
        tweaks=tweaks,
    )


def double_flageolet(
    selector=lambda _: _selection.Selection(_).phead(0, exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
    """
    Attaches double flageolet.
    """
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Articulation("baca-double-flageolet")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def double_staccato(
    selector=lambda _: _selection.Selection(_).phead(0, exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
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

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(
            ...     selection, includes=["baca.ily"]
            ... )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
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
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Articulation("baca-staccati #2")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def down_arpeggio(
    selector=lambda _: _selection.Selection(_).chead(0, exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
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

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \arpeggioArrowDown
                        \time 5/4
                        <c' d' bf'>8
                        \arpeggio
                        ~
                        [
                        <c' d' bf'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        f''8
                        ~
                        [
                        f''32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <ef'' e'' fs'''>8
                        ~
                        [
                        <ef'' e'' fs'''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <g' af''>8
                        ~
                        [
                        <g' af''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'8
                        ~
                        [
                        a'32
                        ]
                        r16.
                    }
                }
            >>

    """
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Arpeggio(direction=abjad.Down)],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def down_bow(
    selector=lambda _: _selection.Selection(_).phead(0, exclude=const.HIDDEN),
    *tweaks: abjad.TweakInterface,
    full: bool = None,
) -> commandclasses.IndicatorCommand:
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

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(
            ...     selection, includes=["baca.ily"]
            ... )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
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

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(
            ...     selection, includes=["baca.ily"]
            ... )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
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
    if full:
        articulation = abjad.Articulation("baca-full-downbow")
    else:
        articulation = abjad.Articulation("downbow")
    return commandclasses.IndicatorCommand(
        indicators=[articulation],
        selector=selector,
        tags=[_site(inspect.currentframe())],
        tweaks=tweaks,
    )


def espressivo(
    selector=lambda _: _selection.Selection(_).phead(0, exclude=const.HIDDEN),
    *tweaks: abjad.TweakInterface,
) -> commandclasses.IndicatorCommand:
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

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
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
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Articulation("espressivo")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
        tweaks=tweaks,
    )


def fermata(
    selector=lambda _: _selection.Selection(_).leaf(0),
) -> commandclasses.IndicatorCommand:
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

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
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
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Articulation("fermata")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def flageolet(
    selector=lambda _: _selection.Selection(_).phead(0, exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
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

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
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
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Articulation("flageolet")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def hide_black_note_heads(
    selector=lambda _: _selection.Selection(_).leaves(exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
    r"""
    Attaches note-head stencil false to black note-heads.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.hide_black_note_heads(),
        ...     baca.make_notes()
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \baca-not-yet-pitched-coloring
                            b'2
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            \baca-not-yet-pitched-coloring
                            \once \override NoteHead.transparent = ##t
                            b'4.
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            \baca-not-yet-pitched-coloring
                            b'2
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            \baca-not-yet-pitched-coloring
                            \once \override NoteHead.transparent = ##t
                            b'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 5]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 5]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

    """
    string = r"\once \override NoteHead.transparent = ##t"
    literal = abjad.LilyPondLiteral(string)
    return commandclasses.IndicatorCommand(
        indicators=[literal],
        predicate=lambda _: _.written_duration < abjad.Duration(1, 2),
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def laissez_vibrer(
    selector=lambda _: _selection.Selection(_).ptail(0, exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
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

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
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
    return commandclasses.IndicatorCommand(
        indicators=[abjad.LaissezVibrer()],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def literal(
    string: typing.Union[str, typing.List[str]],
    selector=lambda _: _selection.Selection(_).leaf(0),
    *,
    format_slot: str = "before",
) -> commandclasses.IndicatorCommand:
    """
    Attaches LilyPond literal.
    """
    literal = abjad.LilyPondLiteral(string, format_slot=format_slot)
    return commandclasses.IndicatorCommand(
        indicators=[literal],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def long_fermata(
    selector=lambda _: _selection.Selection(_).leaf(0),
) -> commandclasses.IndicatorCommand:
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

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
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
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Articulation("longfermata")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def marcato(
    selector=lambda _: _selection.Selection(_).phead(0, exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
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

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
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
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Articulation("marcato")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def margin_markup(
    argument: str,
    selector=lambda _: _selection.Selection(_).leaf(0),
    *,
    alert: commandclasses.IndicatorCommand = None,
    context: str = "Staff",
) -> typing.Union[commandclasses.IndicatorCommand, scoping.Suite]:
    r"""
    Attaches margin markup.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.margin_markup('Fl.'),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \time 4/8
                        \baca-time-signature-color #'blue
                        s1 * 1/2
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \set Staff.shortInstrumentName =
                            \markup { Fl. }
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)
                            e'2
                            ^ \baca-explicit-indicator-markup "[MarginMarkup]"
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes(repeat_ties=True)"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)
                            \set Staff.shortInstrumentName =
                            \markup { Fl. }
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            f'4.
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            e'2
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            f'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 5]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    \baca-not-yet-pitched-coloring
                                    b'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 5]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

    """
    if isinstance(argument, (str, abjad.Markup)):
        markup = abjad.Markup(argument)
        margin_markup = abjad.MarginMarkup(context=context, markup=markup)
    elif isinstance(argument, abjad.MarginMarkup):
        margin_markup = abjad.new(argument, context=context)
    else:
        raise TypeError(argument)
    assert isinstance(margin_markup, abjad.MarginMarkup)
    command = commandclasses.IndicatorCommand(
        indicators=[margin_markup],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )
    if bool(alert):
        assert isinstance(alert, commandclasses.IndicatorCommand), repr(alert)
        return scoping.suite(command, alert)
    else:
        return command


def mark(
    argument: str,
    selector=lambda _: _selection.Selection(_).leaf(0),
    *tweaks: abjad.TweakInterface,
) -> commandclasses.IndicatorCommand:
    """
    Attaches mark.
    """
    assert isinstance(argument, (abjad.Markup, str)), repr(argument)
    rehearsal_mark = abjad.RehearsalMark(markup=argument)
    return commandclasses.IndicatorCommand(
        indicators=[rehearsal_mark],
        selector=selector,
        tags=[_site(inspect.currentframe())],
        tweaks=tweaks,
    )


def parenthesize(
    selector=lambda _: _selection.Selection(_).phead(0, exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
    r"""
    Attaches LilyPond ``\parenthesize`` command.

    ..  container:: example

        Attaches parenthesize command to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.parenthesize(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        \parenthesize
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
    return commandclasses.IndicatorCommand(
        indicators=[abjad.LilyPondLiteral(r"\parenthesize")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def quadruple_staccato(
    selector=lambda _: _selection.Selection(_).phead(0, exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
    """
    Attaches quadruple-staccato.
    """
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Articulation("baca-staccati #4")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def rehearsal_mark(
    argument: typing.Union[int, str],
    selector=lambda _: _selection.Selection(_).leaf(0),
    *tweaks: abjad.TweakInterface,
    font_size: int = 10,
) -> commandclasses.IndicatorCommand:
    """
    Attaches rehearsal mark.
    """
    assert isinstance(argument, str), repr(argument)
    assert isinstance(font_size, (int, float)), repr(font_size)
    string = rf'\baca-rehearsal-mark-markup "{argument}" #{font_size}'
    markup = abjad.Markup(string, direction=abjad.Center, literal=True)
    return commandclasses.IndicatorCommand(
        indicators=[markup],
        selector=selector,
        tags=[_site(inspect.currentframe())],
        tweaks=tweaks,
    )


def repeat_tie(
    selector: abjad.Expression, *, allow_rest: bool = None
) -> commandclasses.IndicatorCommand:
    r"""
    Attaches repeat-tie.

    ..  container:: example

        Attaches repeat-tie to pitched head 1:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.chunk(
        ...         baca.pitch(
        ...             0,
        ...             selector=baca.selectors.plt(1),
        ...         ),
        ...         baca.repeat_tie(
        ...             baca.selectors.phead(1),
        ...         ),
        ...     ),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        [
                        c'16
                        \repeatTie
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
    if allow_rest is not None:
        allow_rest = bool(allow_rest)
    return commandclasses.IndicatorCommand(
        do_not_test=allow_rest,
        indicators=[abjad.RepeatTie()],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def short_fermata(
    selector=lambda _: _selection.Selection(_).leaf(0),
) -> commandclasses.IndicatorCommand:
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

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
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
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Articulation("shortfermata")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def snap_pizzicato(
    selector=lambda _: _selection.Selection(_).phead(0, exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
    """
    Attaches snap pizzicato.
    """
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Articulation("snappizzicato")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def staccatissimo(
    selector=lambda _: _selection.Selection(_).phead(0, exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
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

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
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
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Articulation("staccatissimo")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def staccato(
    selector=lambda _: _selection.Selection(_).phead(0, exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
    r"""
    Attaches staccato.

    ..  container:: example

        Attaches staccato to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.staccato(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        - \staccato
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
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Articulation("staccato")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def staff_lines(
    n: int, selector=lambda _: _selection.Selection(_).leaf(0)
) -> scoping.Suite:
    r"""
    Makes staff line command.

    ..  container:: example

        Single-line staff with percussion clef:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.clef('percussion'),
        ...     baca.make_notes(),
        ...     baca.staff_lines(1),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 6]
                        \baca-new-spacing-section #1 #4
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \override Staff.BarLine.bar-extent = #'(0 . 0)
                            \stopStaff
                            \once \override Staff.StaffSymbol.line-count = 1
                            \startStaff
                            \clef "percussion"
                            \once \override Staff.Clef.color = #(x11-color 'blue)
                            %@% \override Staff.Clef.color = ##f
                            \set Staff.forceClef = ##t
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)
                            a4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            b4.
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            c'4.
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            d'4.
            <BLANKLINE>
                            % [Music_Voice measure 5]
                            e'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 6]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    \baca-not-yet-pitched-coloring
                                    c'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 6]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>


        Single-line staff with bass clef:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.clef('bass'),
        ...     baca.make_notes(),
        ...     baca.staff_lines(1),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 6]
                        \baca-new-spacing-section #1 #4
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \override Staff.BarLine.bar-extent = #'(0 . 0)
                            \stopStaff
                            \once \override Staff.StaffSymbol.line-count = 1
                            \startStaff
                            \clef "bass"
                            \once \override Staff.Clef.color = #(x11-color 'blue)
                            %@% \override Staff.Clef.color = ##f
                            \set Staff.forceClef = ##t
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)
                            b,4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            c4.
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            d4.
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            e4.
            <BLANKLINE>
                            % [Music_Voice measure 5]
                            f4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 6]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    \baca-not-yet-pitched-coloring
                                    d1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 6]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

    ..  container:: example

        Two-line staff with percussion clef:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.clef('percussion'),
        ...     baca.make_notes(),
        ...     baca.staff_lines(2),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 6]
                        \baca-new-spacing-section #1 #4
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \override Staff.BarLine.bar-extent = #'(-0.5 . 0.5)
                            \stopStaff
                            \once \override Staff.StaffSymbol.line-count = 2
                            \startStaff
                            \clef "percussion"
                            \once \override Staff.Clef.color = #(x11-color 'blue)
                            %@% \override Staff.Clef.color = ##f
                            \set Staff.forceClef = ##t
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)
                            a4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            b4.
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            c'4.
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            d'4.
            <BLANKLINE>
                            % [Music_Voice measure 5]
                            e'4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 6]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    \baca-not-yet-pitched-coloring
                                    c'1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 6]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

        Two-line staff with bass clef; clef set before staff positions:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.clef('bass'),
        ...     baca.make_notes(),
        ...     baca.staff_lines(2),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 6]
                        \baca-new-spacing-section #1 #4
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \override Staff.BarLine.bar-extent = #'(-0.5 . 0.5)
                            \stopStaff
                            \once \override Staff.StaffSymbol.line-count = 2
                            \startStaff
                            \clef "bass"
                            \once \override Staff.Clef.color = #(x11-color 'blue)
                            %@% \override Staff.Clef.color = ##f
                            \set Staff.forceClef = ##t
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)
                            b,4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            c4.
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            d4.
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            e4.
            <BLANKLINE>
                            % [Music_Voice measure 5]
                            f4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 6]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    \baca-not-yet-pitched-coloring
                                    d1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 6]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

        Two-line staff with bass clef; staff positions set before clef:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.SpacingSpecifier(fallback_duration=(1, 12)),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'Music_Voice',
        ...     baca.make_notes(),
        ...     baca.staff_lines(2),
        ...     baca.staff_positions([-2, -1, 0, 1, 2]),
        ...     baca.clef('bass'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            <BLANKLINE>
            \context Score = "Score"
            <<
            <BLANKLINE>
                \context GlobalContext = "Global_Context"
                <<
            <BLANKLINE>
                    \context GlobalSkips = "Global_Skips"
                    {
            <BLANKLINE>
                        % [Global_Skips measure 1]
                        \baca-new-spacing-section #1 #12
                        \time 3/8
                        \baca-time-signature-color #'blue
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 2]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 3]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 4]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 5]
                        \baca-new-spacing-section #1 #12
                        s1 * 3/8
            <BLANKLINE>
                        % [Global_Skips measure 6]
                        \baca-new-spacing-section #1 #4
                        \time 1/4
                        \baca-time-signature-transparent
                        s1 * 1/4
                        \once \override Score.BarLine.transparent = ##t
                        \once \override Score.SpanBar.transparent = ##t
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
                \context MusicContext = "Music_Context"
                <<
            <BLANKLINE>
                    \context Staff = "Music_Staff"
                    {
            <BLANKLINE>
                        \context Voice = "Music_Voice"
                        {
            <BLANKLINE>
                            % [Music_Voice measure 1]
                            \override Staff.BarLine.bar-extent = #'(-0.5 . 0.5)
                            \stopStaff
                            \once \override Staff.StaffSymbol.line-count = 2
                            \startStaff
                            \clef "bass"
                            \once \override Staff.StaffSymbol.color = #(x11-color 'blue)
                            \once \override Staff.Clef.color = #(x11-color 'blue)
                            %@% \override Staff.Clef.color = ##f
                            \set Staff.forceClef = ##t
                            g'4.
                            - \abjad-dashed-line-with-hook
                            - \baca-text-spanner-left-text "make_notes()"
                            - \tweak bound-details.right.padding 2.75
                            - \tweak color #darkcyan
                            - \tweak staff-padding 8
                            \bacaStartTextSpanRhythmAnnotation
                            \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)
            <BLANKLINE>
                            % [Music_Voice measure 2]
                            a'4.
            <BLANKLINE>
                            % [Music_Voice measure 3]
                            b'4.
            <BLANKLINE>
                            % [Music_Voice measure 4]
                            c''4.
            <BLANKLINE>
                            % [Music_Voice measure 5]
                            d''4.
                            <> \bacaStopTextSpanRhythmAnnotation
            <BLANKLINE>
                            <<
            <BLANKLINE>
                                \context Voice = "Music_Voice"
                                {
            <BLANKLINE>
                                    % [Music_Voice measure 6]
                                    \abjad-invisible-music-coloring
                                    %@% \abjad-invisible-music
                                    \baca-not-yet-pitched-coloring
                                    d1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                                \context Voice = "Rest_Voice"
                                {
            <BLANKLINE>
                                    % [Rest_Voice measure 6]
                                    \once \override Score.TimeSignature.X-extent = ##f
                                    \once \override MultiMeasureRest.transparent = ##t
                                    \stopStaff
                                    \once \override Staff.StaffSymbol.transparent = ##t
                                    \startStaff
                                    R1 * 1/4
                                    %@% ^ \baca-duration-multiplier-markup #"1" #"4"
            <BLANKLINE>
                                }
            <BLANKLINE>
                            >>
            <BLANKLINE>
                        }
            <BLANKLINE>
                    }
            <BLANKLINE>
                >>
            <BLANKLINE>
            >>

    """
    command_1 = commandclasses.IndicatorCommand(
        indicators=[indicators.BarExtent(n)],
        selector=selector,
        tags=[_tags.NOT_PARTS],
    )
    command_2 = commandclasses.IndicatorCommand(
        indicators=[indicators.StaffLines(n)],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )
    return scoping.suite(command_1, command_2)


def start_markup(
    argument: typing.Union[str, typing.List[str]],
    selector=lambda _: _selection.Selection(_).leaf(0),
    *,
    context: str = "Staff",
    hcenter_in: abjad.Number = None,
    literal: bool = None,
) -> commandclasses.IndicatorCommand:
    """
    Attaches start markup.
    """
    if literal is True or (isinstance(argument, str) and argument.startswith("\\")):
        assert isinstance(argument, str), repr(argument)
        assert argument.startswith("\\"), repr(argument)
        start_markup = abjad.StartMarkup(markup=argument)
    elif isinstance(argument, str):
        width = hcenter_in or 16
        string = rf'\markup \hcenter-in #{width} "{argument}"'
        start_markup = abjad.StartMarkup(markup=string)
    elif isinstance(argument, list) and len(argument) == 2:
        width = hcenter_in or 16
        line_1 = rf'\hcenter-in #{width} "{argument[0]}"'
        line_2 = rf'\hcenter-in #{width} "{argument[1]}"'
        string = rf"\markup \column {{ {line_1} {line_2} }}"
        start_markup = abjad.StartMarkup(markup=string)
    elif isinstance(argument, list) and len(argument) == 3:
        width = hcenter_in or 16
        line_1 = rf'\hcenter-in #{width} "{argument[0]}"'
        line_2 = rf'\hcenter-in #{width} "{argument[1]}"'
        line_3 = rf'\hcenter-in #{width} "{argument[2]}"'
        string = rf"\markup \column {{ {line_1} {line_2} {line_3} }}"
        start_markup = abjad.StartMarkup(markup=string)
    elif isinstance(argument, abjad.Markup):
        markup = abjad.Markup(argument)
        start_markup = abjad.StartMarkup(markup=markup)
    elif isinstance(argument, abjad.StartMarkup):
        start_markup = argument
    else:
        raise TypeError(argument)
    assert isinstance(start_markup, abjad.StartMarkup)
    start_markup = abjad.new(start_markup, context=context)
    command = commandclasses.IndicatorCommand(
        indicators=[start_markup],
        selector=selector,
        tags=[_site(inspect.currentframe()), _tags.NOT_PARTS],
    )
    return command


def stem_tremolo(
    selector=lambda _: _selection.Selection(_).pleaf(0, exclude=const.HIDDEN),
    *,
    tremolo_flags: int = 32,
) -> commandclasses.IndicatorCommand:
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

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
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
    return commandclasses.IndicatorCommand(
        indicators=[abjad.StemTremolo(tremolo_flags=tremolo_flags)],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def stop_on_string(
    selector=lambda _: _selection.Selection(_).phead(0, exclude=const.HIDDEN),
    *,
    map: abjad.Expression = None,
) -> commandclasses.IndicatorCommand:
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
        ...         selector=baca.selectors.pleaf(-1),
        ...     ),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(
            ...     selection, includes=["baca.ily"]
            ... )
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
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
    return commandclasses.IndicatorCommand(
        indicators=[articulation],
        map=map,
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def stop_trill(
    selector=lambda _: _selection.Selection(_).leaf(0),
) -> commandclasses.IndicatorCommand:
    r"""
    Attaches stop trill to closing-slot.

    The closing format slot is important because LilyPond fails to compile
    when ``\stopTrillSpan`` appears after ``\set instrumentName`` commands
    (and probably other ``\set`` commands). Setting format slot to closing
    here positions ``\stopTrillSpan`` after the leaf in question (which is
    required) and also draws ``\stopTrillSpan`` closer to the leaf in
    question, prior to ``\set instrumetName`` and other commands positioned
    in the after slot.

    Eventually it will probably be necessary to model ``\stopTrillSpan``
    with a dedicated format slot.
    """
    return literal(r"\stopTrillSpan", format_slot="closing", selector=selector)


def stopped(
    selector=lambda _: _selection.Selection(_).phead(0, exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
    r"""
    Attaches stopped +-sign.

    ..  container:: example

        Attaches stopped +-sign to pitched head 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.stopped(),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        c'16
                        - \stopped
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
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Articulation("stopped")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def tie(selector: abjad.Expression) -> commandclasses.IndicatorCommand:
    r"""
    Attaches tie.

    ..  container:: example

        Attaches tie to pitched tail 0:

        >>> stack = baca.stack(
        ...     baca.figure(
        ...         [1, 1, 5, -1],
        ...         16,
        ...         affix=baca.rests_around([2], [4]),
        ...         restart_talea=True,
        ...         treatments=[-1],
        ...     ),
        ...     rmakers.beam(),
        ...     baca.chunk(
        ...         baca.pitch(
        ...             2,
        ...             selector=baca.selectors.plt(0),
        ...         ),
        ...         baca.tie(baca.selectors.ptail(0)),
        ...     ),
        ...     baca.tuplet_bracket_staff_padding(2),
        ... )
        >>> selection = stack([[0, 2, 10], [18, 16, 15, 20, 19], [9]])

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10
                    {
                        \override TupletBracket.staff-padding = 2
                        \time 11/8
                        r8
                        d'16
                        [
                        ~
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
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Tie()],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def tenuto(
    selector=lambda _: _selection.Selection(_).phead(0, exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
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

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
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
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Articulation("tenuto")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def triple_staccato(
    selector=lambda _: _selection.Selection(_).phead(0, exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
    """
    Attaches triple-staccato.
    """
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Articulation("baca-staccati #3")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def up_arpeggio(
    selector=lambda _: _selection.Selection(_).chead(0, exclude=const.HIDDEN),
) -> commandclasses.IndicatorCommand:
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

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
                {
                    \scaleDurations #'(1 . 1)
                    {
                        \arpeggioArrowUp
                        \time 5/4
                        <c' d' bf'>8
                        \arpeggio
                        ~
                        [
                        <c' d' bf'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        f''8
                        ~
                        [
                        f''32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <ef'' e'' fs'''>8
                        ~
                        [
                        <ef'' e'' fs'''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        <g' af''>8
                        ~
                        [
                        <g' af''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1)
                    {
                        a'8
                        ~
                        [
                        a'32
                        ]
                        r16.
                    }
                }
            >>

    """
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Arpeggio(direction=abjad.Up)],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )


def up_bow(
    selector=lambda _: _selection.Selection(_).phead(0, exclude=const.HIDDEN),
    *tweaks: abjad.TweakInterface,
    full: bool = None,
) -> commandclasses.IndicatorCommand:
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

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
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
    if full:
        articulation = abjad.Articulation("baca-full-upbow")
    else:
        articulation = abjad.Articulation("upbow")
    return commandclasses.IndicatorCommand(
        indicators=[articulation],
        selector=selector,
        tags=[_site(inspect.currentframe())],
        tweaks=tweaks,
    )


def very_long_fermata(
    selector=lambda _: _selection.Selection(_).leaf(0),
) -> commandclasses.IndicatorCommand:
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

        ..  book::
            :lilypond/no-stylesheet:

            >>> lilypond_file = abjad.illustrators.selection(selection)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> string = abjad.lilypond(lilypond_file[abjad.Score])
            >>> print(string)
            \new Score
            <<
                \new Staff
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
    return commandclasses.IndicatorCommand(
        indicators=[abjad.Articulation("verylongfermata")],
        selector=selector,
        tags=[_site(inspect.currentframe())],
    )
