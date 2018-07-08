"""
Function library.
"""
import abjad
import typing
from . import indicatorlib
from . import markuplib
from . import typings
from .IndicatorCommand import IndicatorCommand
from .PitchCommand import PitchCommand
from .Sequence import Sequence


def apply_tweaks(argument, tweaks):
    """
    Applies ``tweaks`` to ``argument``.
    """
    if not tweaks:
        return
    manager = abjad.tweak(argument)
    for manager_ in tweaks:
        tuples = manager_._get_attribute_tuples()
        for attribute, value in tuples:
            setattr(manager, attribute, value)

def lbsd(
    y_offset: int,
    alignment_distances: typing.Sequence,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    """
    Makes line-break system details.
    """
    alignment_distances = Sequence(alignment_distances).flatten()
    lbsd = indicatorlib.LBSD(
        alignment_distances=alignment_distances,
        y_offset=y_offset,
        )
    return IndicatorCommand(
        indicators=[lbsd],
        selector=selector,
        )

def literal(
    string: str,
    *,
    format_slot: str = 'before',
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    """
    Attaches LilyPond literal.
    """
    literal = abjad.LilyPondLiteral(string, format_slot=format_slot)
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        )

def markup(
    argument: typing.Union[str, abjad.Markup],
    *tweaks: abjad.LilyPondTweakManager,
    direction: abjad.VerticalAlignment = abjad.Up,
    selector: typings.Selector = 'baca.pleaf(0)',
    literal: bool = False,
    ) -> IndicatorCommand:
    r"""
    Makes markup and inserts into indicator command.

    ..  container:: example

        Attaches markup to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.markup('più mosso'),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.outside-staff-priority = #1000                   %! OC1
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            ^ \markup { "più mosso" }                                                %! IC
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
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
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.outside-staff-priority                             %! OC2
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches markup to pitched head 0 in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.markup(
        ...         'più mosso',
        ...         selector=baca.tuplets()[1:2].phead(0),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.outside-staff-priority = #1000                   %! OC1
                            \override TupletBracket.staff-padding = #5                               %! OC1
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
                        \times 9/10 {
                            fs''16
                            ^ \markup { "più mosso" }                                                %! IC
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
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.outside-staff-priority                             %! OC2
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches markup to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.markup(
        ...         '*',
        ...         selector=baca.tuplets()[1:2].pheads(),
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.outside-staff-priority = #1000                   %! OC1
                            \override TupletBracket.staff-padding = #5                               %! OC1
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
                        \times 9/10 {
                            fs''16
                            ^ \markup { * }                                                          %! IC
                            [
                            e''16
                            ^ \markup { * }                                                          %! IC
                            ]
                            ef''4
                            ^ \markup { * }                                                          %! IC
                            ~
                            ef''16
                            r16
                            af''16
                            ^ \markup { * }                                                          %! IC
                            [
                            g''16
                            ^ \markup { * }                                                          %! IC
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.outside-staff-priority                             %! OC2
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Set the ``literal=True`` to pass predefined markup commands:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.markup(
        ...         r'\baca_triple_diamond_markup',
        ...         literal=True,
        ...         ),
        ...     baca.rests_around([2], [4]),
        ...     baca.tuplet_bracket_outside_staff_priority(1000),
        ...     baca.tuplet_bracket_staff_padding(5),
        ...     counts=[1, 1, 5, -1],
        ...     time_treatments=[-1],
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff
            <<
                \context Voice = "Voice 1"
                {
                    \voiceOne
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            \override TupletBracket.outside-staff-priority = #1000                   %! OC1
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            ^ \markup { \baca_triple_diamond_markup }                                %! IC
                            [
                            d'16
                            ]
                            bf'4
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
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
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.outside-staff-priority                             %! OC2
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Raises exception on nonstring, nonmarkup ``argument``:

        >>> baca.markup(['Allegro', 'ma non troppo'])
        Traceback (most recent call last):
            ...
        Exception: MarkupLibary.__call__():
            Value of 'argument' must be str or markup.
            Not ['Allegro', 'ma non troppo'].

    """
    if direction not in (abjad.Down, abjad.Up):
        message = f'direction must be up or down (not {direction!r}).'
        raise Exception(message)
    if isinstance(argument, str):
        if literal:
            markup = abjad.Markup.from_literal(
                argument,
                direction=direction,
                )
        else:
            markup = abjad.Markup(argument, direction=direction)
    elif isinstance(argument, abjad.Markup):
        markup = abjad.new(argument, direction=direction)
    else:
        message = 'MarkupLibary.__call__():\n'
        message += "  Value of 'argument' must be str or markup.\n"
        message += f'  Not {argument!r}.'
        raise Exception(message)
    prototype = (str, abjad.Expression)
    if selector is not None and not isinstance(selector, prototype):
        message = f'selector must be string or expression'
        message += f' (not {selector!r}).'
        raise Exception(message)
    selector = selector or 'baca.phead(0)'
    return IndicatorCommand(
        *tweaks,
        indicators=[markup],
        selector=selector,
        )

def pitches(
    pitches: typing.Iterable,
    *,
    allow_octaves: bool = None,
    allow_repeats: bool = None,
    do_not_transpose: bool = None,
    exact: bool = None,
    ignore_incomplete: bool = None,
    persist: str = None,
    selector: typings.Selector = 'baca.pleaves()',
    ) -> PitchCommand:
    """
    Makes pitch command.
    """
    if do_not_transpose not in (None, True, False):
        raise Exception('do_not_transpose must be boolean'
            f' (not {do_not_transpose!r}).')
    if bool(exact):
        cyclic = False
    else:
        cyclic = True
    if ignore_incomplete not in (None, True, False):
        raise Exception('ignore_incomplete must be boolean'
            f' (not {ignore_incomplete!r}).')
    if ignore_incomplete is True and not persist:
        raise Exception(f'ignore_incomplete is ignored'
            ' when persist is not set.')
    if persist is not None and not isinstance(persist, str):
        raise Exception(f'persist name must be string (not {persist!r}).')
    return PitchCommand(
        allow_octaves=allow_octaves,
        allow_repeats=allow_repeats,
        cyclic=cyclic,
        do_not_transpose=do_not_transpose,
        ignore_incomplete=ignore_incomplete,
        persist=persist,
        pitches=pitches,
        selector=selector,
        )
