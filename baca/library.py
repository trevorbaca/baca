"""
Function library.
"""
import abjad
import typing
from . import typings
from .Command import Command
from .Command import Map
from .Command import Suite
from .DivisionSequenceExpression import DivisionSequenceExpression
from .IndicatorCommand import IndicatorCommand
from .LBSD import LBSD
from .Markup import Markup
from .MeasureWrapper import MeasureWrapper
from .PiecewiseSpannerCommand import PiecewiseSpannerCommand
from .PitchCommand import PitchCommand
from .Scope import Scope
from .Sequence import Sequence
from .TimelineScope import TimelineScope


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

def dashed_arrow() -> abjad.ArrowLineSegment:
    """
    Makes dashed arrow line segment.
    """
    return abjad.ArrowLineSegment(
        dash_fraction=0.25,
        dash_period=1.5,
        left_broken_text=False,
        left_hspace=0.5,
        right_broken_arrow=False,
        right_broken_padding=0,
        right_broken_text=False,
        right_padding=0.5,
        )

def dashed_hook() -> abjad.LineSegment:
    """
    Makes dashed hook line segment.
    """
    return abjad.LineSegment(
        dash_fraction=0.25,
        dash_period=1.5,
        left_broken_text=False,
        left_hspace=0.5,
        left_stencil_align_direction_y=0,
        right_broken_arrow=False,
        right_broken_padding=0,
        right_broken_text=False,
        # right padding to avoid last leaf in spanner
        right_padding=1.25,
        right_text=abjad.Markup.draw_line(0, -1),
        )

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
    lbsd = LBSD(
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

def map(
    selector: typing.Union[abjad.Expression, str],
    *commands: typing.Union[Command, Map, Suite],
    ) -> Map:
    """
    Maps ``selector`` to each command in ``commands``.
    """
    if not isinstance(selector, (abjad.Expression, str)):
        message = '\n  Map selector must be expression or string.'
        message += f'\n  Not {format(selector)}.'
        raise Exception(message)
    if not commands:
        raise Exception('map commands must not be empty.')
    commands_ = []
    for item in commands:
        if isinstance(item, (list, tuple)):
            commands_.extend(item)
        else:
            commands_.append(item)
    for command in commands_:
        if not isinstance(command, (Command, Map, Suite)):
            message = '\n  Must be command, map, suite.'
            message += f'\n  Not {type(command).__name__}: {command!r}.'
            raise Exception(message)
    return Map(selector, *commands_)

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

def measures(
    measures: typing.Union[int, typing.List[int], typing.Tuple[int, int]],
    *commands: Command,
    ) -> typing.List[MeasureWrapper]:
    r"""
    Wraps each command in ``commands`` with ``measures``.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 16)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.measures(
        ...         (1, 2),
        ...         baca.make_even_divisions(),
        ...         ),
        ...     baca.measures(
        ...         (3, 4),
        ...         baca.make_repeat_tied_notes(),
        ...         ),
        ...     baca.pitches('E4 F4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #16                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            e'8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            e'8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            f'2
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f'4.
                            \repeatTie
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    wrappers = []
    for command in commands:
        wrapper = MeasureWrapper(
            command=command,
            measures=measures,
            )
        wrappers.append(wrapper)
    return wrappers

def not_parts(command: Command) -> typing.Union[Command, Map, Suite]:
    """
    Tags ``command`` with ``-PARTS``.

    Returns ``command``.
    """
    return tag('-PARTS', command)

def not_score(command: Command) -> typing.Union[Command, Map, Suite]:
    """
    Tags ``command`` with ``-SCORE``.

    Returns ``command``.
    """
    return tag('-SCORE', command)

def not_segment(command: Command) -> typing.Union[Command, Map, Suite]:
    """
    Tags ``command`` with ``-SEGMENT``.

    Returns ``command``.
    """
    return tag('-SEGMENT', command)

def only_parts(command: Command) -> typing.Union[Command, Map, Suite]:
    """
    Tags ``command`` with ``+PARTS``.

    Returns ``command``.
    """
    return tag('+PARTS', command)

def only_score(command: Command) -> typing.Union[Command, Map, Suite]:
    """
    Tags ``command`` with ``+SCORE``.

    Returns ``command``.
    """
    return tag('+SCORE', command)

def only_segment(command: Command) -> typing.Union[Command, Map, Suite]:
    """
    Tags ``command`` with ``+SEGMENT``.

    Returns ``command``.
    """
    return tag('+SEGMENT', command)

def pick(pattern, *commands) -> typing.List[typings.Pair]:
    """
    Maps ``pattern`` to each command in ``commands``.
    """
    pairs = []
    for command in commands:
        pair = (command, pattern)
        pairs.append(pair)
    return pairs

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

def scope(
    voice_name: str,
    stages: typing.Union[int, typing.Tuple[int, int]] = (1, -1),
    ) -> Scope:
    r"""
    Scopes ``voice_name`` for ``stages``.

    ..  container:: example

        >>> baca.scope('HornVoiceI', 1)
        Scope(stages=(1, 1), voice_name='HornVoiceI')

        >>> baca.scope('HornVoiceI', (1, 8))
        Scope(stages=(1, 8), voice_name='HornVoiceI')

        >>> baca.scope('HornVoiceI', (4, -1))
        Scope(stages=(4, -1), voice_name='HornVoiceI')

        >>> baca.scope('HornVoiceI')
        Scope(stages=(1, -1), voice_name='HornVoiceI')

    ..  container:: example

        Negative stage numbers are allowed:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8)],
        ...     )
        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_repeated_duration_notes([(1, 8)]),
        ...     )
        >>> maker(
        ...     ('MusicVoice', (-4, -3)),
        ...     baca.pitch('D4'),
        ...     )
        >>> maker(
        ...     ('MusicVoice', (-2, -1)),
        ...     baca.pitch('E4'),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        s1 * 3/8
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            d'8
            <BLANKLINE>
                            d'8
            <BLANKLINE>
                            d'8
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            d'8
            <BLANKLINE>
                            d'8
            <BLANKLINE>
                            d'8
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            e'8
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            e'8
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Raises exception when stages are other than nonzero integers:

        >>> baca.scope('MusicVoice', 0)
        Traceback (most recent call last):
            ...
        Exception: stages must be nonzero integer or pair of nonzero integers (not 0).

        >>> baca.scope('MusicVoice', 'text')
        Traceback (most recent call last):
            ...
        Exception: stages must be nonzero integer or pair of nonzero integers (not 'text').

    """
    message = 'stages must be nonzero integer or pair of nonzero integers'
    message += f' (not {stages!r}).'
    if isinstance(stages, int):
        start, stop = stages, stages
    elif isinstance(stages, tuple):
        assert len(stages) == 2, repr(stages)
        start, stop = stages
    else:
        raise Exception(message)
    if (not isinstance(start, int) or
        not isinstance(stop, int) or 
        start == 0  or
        stop == 0):
        raise Exception(message)
    stages = (start, stop)
    return Scope(
        stages=stages,
        voice_name=voice_name,
        )

def split_by_durations(
    durations: typing.Iterable,
    remainder: abjad.HorizontalAlignment = abjad.Right,
    ) -> DivisionSequenceExpression:
    r"""
    Splits divisions by ``durations``.

    ..  container:: example

        >>> expression = baca.split_by_durations([(3, 8)])

        >>> for item in expression([(2, 8), (2, 8)]):
        ...     item
        ...
        Division((3, 8))
        Division((1, 8))

        >>> for item in expression([(2, 8), (2, 8), (2, 8)]):
        ...     item
        ...
        Division((3, 8))
        Division((3, 8))

        >>> for item in expression([(2, 8), (2, 8), (2, 8), (2, 8)]):
        ...     item
        ...
        Division((3, 8))
        Division((3, 8))
        Division((2, 8))

    """
    expression = DivisionSequenceExpression()
    expression = expression.division_sequence()
    expression = expression.flatten(depth=-1)
    expression = expression.sum()
    expression = expression.division_sequence()
    expression = expression.split_by_durations(
        cyclic=True,
        durations=durations,
        remainder=remainder,
        )
    expression = expression.flatten(depth=-1)
    return expression

def suite(
    *commands: Command,
    ) -> Suite:
    """
    Makes suite.

    ..  container:: example

        Raises exception on noncommand:

        >>> baca.suite(['Allegro'])
        Traceback (most recent call last):
            ...
        Exception:
            Must contain only commands, maps, suites.
            Not list: ['Allegro'].

    """
    for command in commands:
        if not isinstance(command, (Command, Map, Suite)):
            message = '\n  Must contain only commands, maps, suites.'
            message += f'\n  Not {type(command).__name__}: {command!r}.'
            raise Exception(message)
    return Suite(*commands)

def tag(
    tags: typing.Union[str, typing.List[str]],
    command: typing.Union[Command, Map, Suite, abjad.Markup],
    *,
    deactivate: bool = None,
    tag_measure_number: bool = None,
    ) -> typing.Union[Command, Map, Suite]:
    """
    Appends each tag in ``tags`` to ``command``.

    Sorts ``command`` tags.

    Returns ``command`` for in-place definition file application.
    """
    if isinstance(tags, str):
        tags = [tags]
    if not isinstance(tags, list):
        message = f'tags must be string or list of strings'
        message += f' (not {tags!r}).'
        raise Exception(message)
    if isinstance(command, abjad.Markup):
        command = markup(command)
    assert Command._validate_tags(tags), repr(tags)
    if isinstance(command, (Map, Suite)):
        for command_ in command.commands:
            tag(
                tags,
                command_,
                deactivate=deactivate,
                tag_measure_number=tag_measure_number,
                )
    else:
        assert command._tags is not None
        tags.sort()
        tags_ = [abjad.Tag(_) for _ in tags]
        command._tags.extend(tags_)
        command._deactivate = deactivate
        command.tag_measure_number = tag_measure_number
    return command

def timeline(scopes) -> TimelineScope:
    """
    Makes timeline scope.
    """
    scopes = [scope(*_) for _ in scopes]
    return TimelineScope(scopes=scopes)
