import abjad
import baca
import typing
from abjadext import rmakers
from . import library
from . import typings
from .Command import Map
from .Command import Suite
from .GlobalFermataCommand import GlobalFermataCommand
from .HorizontalSpacingSpecifier import HorizontalSpacingSpecifier
from .ImbricationCommand import ImbricationCommand
from .IndicatorCommand import IndicatorCommand
from .InstrumentChangeCommand import InstrumentChangeCommand
from .LabelCommand import LabelCommand
from .LBSD import LBSD
from .Loop import Loop
from .MetronomeMarkCommand import MetronomeMarkCommand
from .PitchCommand import PitchCommand
from .Scope import Scope
from .SpannerCommand import SpannerCommand
from .StaffPositionInterpolationCommand import (
    StaffPositionInterpolationCommand,
    )

__documentation_section__ = '(1) Library'


def glissando(
    *,
    allow_repeats: bool = None,
    allow_ties: bool = None,
    right_broken: bool = None,
    selector: typings.Selector = 'baca.tleaves()',
    stems: bool = None,
    style: str = None,
    ) -> SpannerCommand:
    r"""
    Attaches glissando.

    ..  container:: example

        With segment-maker:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.glissando()
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
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
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
                            \glissando                                                               %! SC
            <BLANKLINE>
                            d''8
                            \glissando                                                               %! SC
            <BLANKLINE>
                            f'8
                            \glissando                                                               %! SC
            <BLANKLINE>
                            e''8
                            ]
                            \glissando                                                               %! SC
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
                            \glissando                                                               %! SC
            <BLANKLINE>
                            f''8
                            \glissando                                                               %! SC
            <BLANKLINE>
                            e'8
                            ]
                            \glissando                                                               %! SC
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
                            \glissando                                                               %! SC
            <BLANKLINE>
                            f'8
                            \glissando                                                               %! SC
            <BLANKLINE>
                            e''8
                            \glissando                                                               %! SC
            <BLANKLINE>
                            g'8
                            ]
                            \glissando                                                               %! SC
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
                            \glissando                                                               %! SC
            <BLANKLINE>
                            e'8
                            \glissando                                                               %! SC
            <BLANKLINE>
                            d''8
                            ]
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        First and last PLTs:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
        ...     baca.make_even_divisions(),
        ...     baca.glissando(selector=baca.plts()[:2]),
        ...     baca.glissando(selector=baca.plts()[-2:]),
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
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
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
                            \glissando                                                               %! SC
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
                            \glissando                                                               %! SC
            <BLANKLINE>
                            d''8
                            ]
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        With music-maker:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplets()[1:2].runs(),
        ...         baca.glissando(),
        ...         ),
        ...     baca.rests_around([2], [4]),
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
                            [
                            \glissando                                                               %! SC
                            e''16
                            ]
                            \glissando                                                               %! SC
                            ef''4
                            ~
                            ef''16
                            r16
                            af''16
                            [
                            \glissando                                                               %! SC
                            g''16
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    """
    glissando = abjad.Glissando(
        allow_repeats=allow_repeats,
        allow_ties=allow_ties,
        stems=stems,
        style=style,
        )
    return SpannerCommand(
        right_broken=right_broken,
        selector=selector,
        spanner=glissando,
        )

def global_fermata(
    description: str = None,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> GlobalFermataCommand:
    """
    Attaches global fermata.
    """
    return GlobalFermataCommand(
        description=description,
        selector=selector,
        )

def imbricate(
    voice_name: str,
    segment: typing.List,
    *specifiers: typing.Any,
    allow_unused_pitches: bool = None,
    by_pitch_class: bool = None,
    extend_beam: bool = None,
    hocket: bool = None,
    selector: typings.Selector = None,
    truncate_ties: bool = None
    ):
    r"""
    Imbricates ``segment`` in voice with ``voice_name``.

    ..  container:: example

        Imbricates segment:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.imbricate('Voice 2', [10, 20, 19]),
        ...     baca.rests_around([2], [4]),
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
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
                \context Voice = "Voice 2"
                {
                    \voiceTwo
                    {
                        \override TupletBracket.stencil = ##f
                        \override TupletNumber.stencil = ##f
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            s8
                            s16
                            s16
                            bf'4
                            ~
                            bf'16
                            s16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            s16
                            s16
                            s4
                            s16
                            s16
                            af''16
                            [
                            g''16
                            ]
                        }
                        \times 4/5 {
                            s16
                            s4
                        }
                        \revert TupletBracket.stencil
                        \revert TupletNumber.stencil
                    }
                }
            >>

    """
    return ImbricationCommand(
        voice_name,
        segment,
        *specifiers,
        allow_unused_pitches=allow_unused_pitches,
        by_pitch_class=by_pitch_class,
        extend_beam=extend_beam,
        hocket=hocket,
        selector=selector,
        truncate_ties=truncate_ties,
        )

def instrument(
    instrument: abjad.Instrument,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> InstrumentChangeCommand:
    """
    Makes instrument change command.
    """
    if not isinstance(instrument, abjad.Instrument):
        message = f'instrument must be instrument (not {instrument!r}).'
        raise Exception(message)
    return InstrumentChangeCommand(
        indicators=[instrument],
        selector=selector,
        )

def interpolate_staff_positions(
    start_pitch: typing.Union[str, abjad.NamedPitch],
    stop_pitch: typing.Union[str, abjad.NamedPitch],
    *,
    selector: typings.Selector = 'baca.plts()',
    ) -> StaffPositionInterpolationCommand:
    """
    Interpolates from staff position of ``start_pitch`` to staff
    position of ``stop_pitch``.
    """
    return StaffPositionInterpolationCommand(
        start_pitch=start_pitch,
        stop_pitch=stop_pitch,
        selector=selector,
        )

def label(
    expression: abjad.Expression,
    *,
    selector: typings.Selector = 'baca.leaves()',
    ) -> LabelCommand:
    r"""
    Labels ``selector`` output with label ``expression``.

    ..  container:: example

        Labels pitch names:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.label(abjad.label().with_pitches(locale='us')),
        ...     baca.rests_around([2], [4]),
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
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            ^ \markup { C4 }
                            [
                            d'16
                            ^ \markup { D4 }
                            ]
                            bf'4
                            ^ \markup { Bb4 }
                            ~
                            bf'16
                            r16
                        }
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 9/10 {
                            fs''16
                            ^ \markup { "F#5" }
                            [
                            e''16
                            ^ \markup { E5 }
                            ]
                            ef''4
                            ^ \markup { Eb5 }
                            ~
                            ef''16
                            r16
                            af''16
                            ^ \markup { Ab5 }
                            [
                            g''16
                            ^ \markup { G5 }
                            ]
                        }
                        \times 4/5 {
                            a'16
                            ^ \markup { A4 }
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Labels pitch names in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.label(
        ...         abjad.label().with_pitches(locale='us'),
        ...         selector=baca.tuplet(1),
        ...         ),
        ...     baca.rests_around([2], [4]),
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
                            ^ \markup { "F#5" }
                            [
                            e''16
                            ^ \markup { E5 }
                            ]
                            ef''4
                            ^ \markup { Eb5 }
                            ~
                            ef''16
                            r16
                            af''16
                            ^ \markup { Ab5 }
                            [
                            g''16
                            ^ \markup { G5 }
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    """
    return LabelCommand(expression=expression, selector=selector)

def laissez_vibrer(
    *,
    selector: typings.Selector  = 'baca.ptail(0)',
    ) -> IndicatorCommand:
    r"""
    Attaches laissez vibrer.

    ..  container:: example

        Attaches laissez vibrer to PLT tail 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.laissez_vibrer(),
        ...     baca.rests_around([2], [4]),
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
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            -\laissezVibrer                                                          %! IC
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
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches laissez vibrer to pitched tails in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.laissez_vibrer(selector=baca.ptails()),
        ...         ),
        ...     baca.rests_around([2], [4]),
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
                            -\laissezVibrer                                                          %! IC
                            [
                            e''16
                            -\laissezVibrer                                                          %! IC
                            ]
                            ef''4
                            ~
                            ef''16
                            -\laissezVibrer                                                          %! IC
                            r16
                            af''16
                            -\laissezVibrer                                                          %! IC
                            [
                            g''16
                            -\laissezVibrer                                                          %! IC
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation('laissezVibrer')],
        selector=selector,
        )

def long_fermata(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    r"""
    Attaches long fermata.

    ..  container:: example

        Attaches long fermata to first leaf:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.long_fermata(),
        ...     baca.rests_around([2], [4]),
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
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            -\longfermata                                                            %! IC
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
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches long fermata to first leaf in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.long_fermata(selector=baca.tuplets()[1:2].phead(0)),
        ...     baca.rests_around([2], [4]),
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
                            -\longfermata                                                            %! IC
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
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation('longfermata')],
        selector=selector,
        )

def loop(
    pitches: typing.Iterable,
    intervals: typing.Iterable,
    ) -> PitchCommand:
    """
    Loops ``pitches`` at ``intervals``.
    """
    loop = Loop(items=pitches, intervals=intervals)
    return library.pitches(loop)

def marcato(
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> IndicatorCommand:
    r"""
    Attaches marcato.

    ..  container:: example

        Attaches marcato to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.marcato(),
        ...     baca.rests_around([2], [4]),
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
                            \override TupletBracket.staff-padding = #5                               %! OC1
                            r8
                            c'16
                            -\marcato                                                                %! IC
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
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    ..  container:: example

        Attaches marcato to pitched heads in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.map(
        ...         baca.tuplet(1),
        ...         baca.marcato(selector=baca.pheads()),
        ...         ),
        ...     baca.rests_around([2], [4]),
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
                            -\marcato                                                                %! IC
                            [
                            e''16
                            -\marcato                                                                %! IC
                            ]
                            ef''4
                            -\marcato                                                                %! IC
                            ~
                            ef''16
                            r16
                            af''16
                            -\marcato                                                                %! IC
                            [
                            g''16
                            -\marcato                                                                %! IC
                            ]
                        }
                        \times 4/5 {
                            a'16
                            r4
                            \revert TupletBracket.staff-padding                                      %! OC2
                        }
                    }
                }
            >>

    """
    return IndicatorCommand(
        indicators=[abjad.Articulation('marcato')],
        selector=selector,
        )

def margin_markup(
    argument: str,
    *,
    alert: IndicatorCommand = None,
    context: str = 'Staff',
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> typing.Union[IndicatorCommand, Suite]:
    r"""
    Attaches margin markup.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.margin_markup('Fl.'),
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
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \baca_bar_line_visible                                                       %! SM5
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
                            \set Staff.instrumentName =                                              %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                            \markup { Fl. }                                                          %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                            \set Staff.shortInstrumentName =                                         %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                            \markup { Fl. }                                                          %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue)          %! SM6:EXPLICIT_MARGIN_MARKUP_COLOR:IC
                            e'2
                            ^ \markup {                                                              %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                \with-color                                                          %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                    #(x11-color 'blue)                                               %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                    [MarginMarkup]                                                   %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                                }                                                                    %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)        %! SM6:REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:IC
                            \set Staff.instrumentName =                                              %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                            \markup { Fl. }                                                          %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                            \set Staff.shortInstrumentName =                                         %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                            \markup { Fl. }                                                          %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            f'4.
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            e'2
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f'4.
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    if isinstance(argument, (str, abjad.Markup)):
        markup = abjad.Markup(argument)
        margin_markup = abjad.MarginMarkup(
            context=context,
            markup=markup,
            )
    elif isinstance(argument, abjad.MarginMarkup):
        margin_markup = abjad.new(
            argument,
            context=context,
            )
    else:
        raise TypeError(argument)
    assert isinstance(margin_markup, abjad.MarginMarkup)
    command = IndicatorCommand(
        indicators=[margin_markup],
        selector=selector,
        )
    if bool(alert):
        assert isinstance(alert, IndicatorCommand), repr(alert)
        return Suite(command, alert)
    else:
        return command

def metronome_mark(
    key: str,
    *,
    redundant: bool = None,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> typing.Optional[MetronomeMarkCommand]:
    """
    Attaches metronome mark matching ``key`` metronome mark manifest.
    """
    if redundant is True:
        return None
    return MetronomeMarkCommand(
        key=key,
        redundant=redundant,
        selector=selector,
        )

def minimum_duration(
    duration: typing.Union[tuple, abjad.Duration],
    ) -> HorizontalSpacingSpecifier:
    """
    Makes horizontal spacing specifier with ``duration`` minimum width.
    """
    return HorizontalSpacingSpecifier(
        minimum_duration=duration,
        )

def mleaves(count: int) -> abjad.Expression:
    """
    Selects all leaves in ``count`` measures.
    """
    assert isinstance(count, int), repr(count)
    selector = baca.select().leaves().group_by_measure()
    if 0 < count:
        selector = selector[:count].flatten()
    elif count < 0:
        selector = selector[-count:].flatten()
    else:
        raise Exception(count)
    return selector
