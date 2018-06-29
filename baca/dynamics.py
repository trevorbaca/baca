"""
Dynamics library.
"""
import abjad
import baca
import typing
from . import library
from . import typings
from .Command import Command
from .Command import Map
from .Command import Suite
from .DynamicBundle import DynamicBundle
from .IndicatorCommand import IndicatorCommand
from .OverrideCommand import OverrideCommand
from .PiecewiseIndicatorCommand import PiecewiseIndicatorCommand
from .SchemeManifest import SchemeManifest


# TODO: remove _local aliases

def parse_descriptor(
    descriptor: str
    ) -> typing.List[DynamicBundle]:
    r"""
    Parses ``descriptor``.

    ..  container:: example

        >>> for item in baca.parse_descriptor('f'):
        ...     item
        DynamicBundle(dynamic=Dynamic('f'))

        >>> for item in baca.parse_descriptor('"f"'):
        ...     item
        DynamicBundle(dynamic=Dynamic('f', command='\\baca_effort_f'))

        >>> for item in baca.parse_descriptor('niente'):
        ...     item
        DynamicBundle(dynamic=Dynamic('niente', command='\\!', direction=Down, name_is_textual=True))

        >>> for item in baca.parse_descriptor('<'):
        ...     item
        DynamicBundle(dynamic_trend=DynamicTrend(shape='<'))

        >>> for item in baca.parse_descriptor('o<|'):
        ...     item
        DynamicBundle(dynamic_trend=DynamicTrend(shape='o<|'))

        >>> for item in baca.parse_descriptor('--'):
        ...     item
        DynamicBundle(dynamic_trend=DynamicTrend(shape='--'))

        TODO: fix extra terminal forte:
        
        >>> for item in baca.parse_descriptor('< f'):
        ...     item
        DynamicBundle(dynamic_trend=DynamicTrend(shape='<'))
        DynamicBundle(dynamic=Dynamic('f'))
        DynamicBundle(dynamic=Dynamic('f'))

        >>> for item in baca.parse_descriptor('o< f'):
        ...     item
        DynamicBundle(dynamic_trend=DynamicTrend(shape='o<'))
        DynamicBundle(dynamic=Dynamic('f'))
        DynamicBundle(dynamic=Dynamic('f'))

        >>> for item in baca.parse_descriptor('niente o<| f'):
        ...     abjad.f(item)
        baca.DynamicBundle(
            dynamic=abjad.Dynamic('niente', command='\\!', direction=Down, name_is_textual=True, ),
            dynamic_trend=abjad.DynamicTrend(
                shape='o<|',
                ),
            )
        baca.DynamicBundle(
            dynamic=abjad.Dynamic('f'),
            )

        >>> for item in baca.parse_descriptor('f >'):
        ...     abjad.f(item)
        baca.DynamicBundle(
            dynamic=abjad.Dynamic('f'),
            dynamic_trend=abjad.DynamicTrend(
                shape='>',
                ),
            )

        >>> for item in baca.parse_descriptor('f >o'):
        ...     abjad.f(item)
        baca.DynamicBundle(
            dynamic=abjad.Dynamic('f'),
            dynamic_trend=abjad.DynamicTrend(
                shape='>o',
                tweaks=LilyPondTweakManager(('to_barline', True)),
                ),
            )

        >>> for item in baca.parse_descriptor('p mp mf f'):
        ...     item
        DynamicBundle(dynamic=Dynamic('p'))
        DynamicBundle(dynamic=Dynamic('mp'))
        DynamicBundle(dynamic=Dynamic('mf'))
        DynamicBundle(dynamic=Dynamic('f'))

        >>> for item in baca.parse_descriptor('p < f f > p'):
        ...     abjad.f(item)
        baca.DynamicBundle(
            dynamic=abjad.Dynamic('p'),
            dynamic_trend=abjad.DynamicTrend(
                shape='<',
                ),
            )
        baca.DynamicBundle(
            dynamic=abjad.Dynamic('f'),
            )
        baca.DynamicBundle(
            dynamic=abjad.Dynamic('f'),
            dynamic_trend=abjad.DynamicTrend(
                shape='>',
                ),
            )
        baca.DynamicBundle(
            dynamic=abjad.Dynamic('p'),
            )

    """
    assert isinstance(descriptor, str), repr(descriptor)
    indicators: typing.List[
        typing.Union[abjad.Dynamic, abjad.DynamicTrend]] = []
    bundles: typing.List[DynamicBundle] = []
    known_shapes = abjad.DynamicTrend('<').known_shapes
    for string in descriptor.split():
        if string in known_shapes:
            dynamic_trend = abjad.DynamicTrend(string)
            if dynamic_trend.shape == '>o':
                abjad.tweak(dynamic_trend).to_barline = True
            indicators.append(dynamic_trend)
        else:
            command = _local_dynamic(string)
            assert command.indicators
            dynamic = command.indicators[0]
            assert isinstance(dynamic, abjad.Dynamic)
            indicators.append(dynamic)
    if len(indicators) == 1:
        bundle = DynamicBundle.from_indicator(indicators[0])
        bundles.append(bundle)
        return bundles
    if isinstance(indicators[0], abjad.DynamicTrend):
        result = indicators.pop(0)
        assert isinstance(result, abjad.DynamicTrend)
        bundle = DynamicBundle(dynamic_trend=result)
        bundles.append(bundle)
    if len(indicators) == 1:
        bundle = DynamicBundle.from_indicator(indicators[0])
        bundles.append(bundle)
    for left, right in baca.sequence(indicators).nwise():
        if (isinstance(left, abjad.DynamicTrend) and
            isinstance(right, abjad.DynamicTrend)):
            raise Exception('consecutive dynamic trends')
        elif (isinstance(left, abjad.Dynamic) and
            isinstance(right, abjad.Dynamic)):
            bundle = DynamicBundle.from_indicator(left)
            bundles.append(bundle)
        elif (isinstance(left, abjad.Dynamic) and
            isinstance(right, abjad.DynamicTrend)):
            bundle = DynamicBundle(dynamic=left, dynamic_trend=right)
            bundles.append(bundle)
    if indicators and isinstance(indicators[-1], abjad.Dynamic):
        bundle = DynamicBundle.from_indicator(indicators[-1])
        bundles.append(bundle)
    return bundles

def ancora_dynamic(
    dynamic: str,
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> IndicatorCommand:
    r"""
    Attaches ancora dynamic.

    ..  container:: example

        Attaches ancora dynamic to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.ancora_dynamic('ff'),
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
                            \baca_ff_ancora                                                               %! IC
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

        Attaches ancora dynamic to pitched head 0 in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.ancora_dynamic(
        ...         'ff',
        ...         selector=baca.tuplets()[1:2].phead(0),
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
                            \baca_ff_ancora                                                               %! IC
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
    command = rf'\baca_{dynamic}_ancora'
    indicator = abjad.Dynamic(dynamic, command=command)
    return IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        )

def dynamic(
    dynamic: typing.Union[str, abjad.Dynamic],
    *tweaks: abjad.LilyPondTweakManager,
    selector: typings.Selector = 'baca.phead(0)',
    redundant: bool = None,
    ) -> IndicatorCommand:
    r"""
    Attaches dynamic.

    ..  container:: example

        Attaches dynamic to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('f'),
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
                            \f                                                                       %! IC
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

        Attaches dynamic to pitched head 0 in tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('f', selector=baca.tuplets()[1:2].phead(0)),
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
                            \f                                                                       %! IC
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

        Attaches effort dynamic to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.dynamic('"f"'),
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
                            \baca_effort_f                                                                %! IC
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

        Works with dynamic trends:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.dynamic('p'),
        ...     baca.dynamic('<'),
        ...     baca.dynamic('f', selector=baca.pleaf(-1)),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            \<                                                                       %! IC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
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
                            c''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            d''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Works with tweaks:        

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.dynamic('p', abjad.tweak('red').color),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            e'8
                            - \tweak color #red                                                      %! SM8:EXPLICIT_DYNAMIC:IC
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
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
                            c''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    scheme_manifest = SchemeManifest()
    known_shapes = abjad.DynamicTrend('<').known_shapes
    indicator: typing.Union[abjad.Dynamic, abjad.DynamicTrend]
    if isinstance(dynamic, str):
        if dynamic == 'niente':
            indicator = abjad.Dynamic('niente', command=r'\!')
        elif 'baca_' + dynamic in scheme_manifest.dynamics:
            name = scheme_manifest.dynamic_to_steady_state(dynamic)
            command = '\\baca_' + dynamic
            pieces = dynamic.split('_')
            if pieces[0] in ('sfz', 'sffz', 'sfffz'):
                sforzando = True
            else:
                sforzando = False
            name_is_textual = not(sforzando)
            indicator = abjad.Dynamic(
                name,
                command=command,
                name_is_textual=name_is_textual,
                sforzando=sforzando,
                )
        elif dynamic.startswith('"'):
            assert dynamic.endswith('"')
            dynamic = dynamic.strip('"')
            command = rf'\baca_effort_{dynamic}'
            indicator = abjad.Dynamic(f'{dynamic}', command=command)
        elif dynamic in known_shapes:
            indicator = abjad.DynamicTrend(dynamic)
        else:
            indicator = abjad.Dynamic(dynamic)
    else:
        prototype = (abjad.Dynamic, abjad.DynamicTrend)
        assert isinstance(dynamic, prototype), repr(dynamic)
        indicator = dynamic
    return IndicatorCommand(
        *tweaks,
        context='Voice',
        indicators=[indicator],
        redundant=redundant,
        selector=selector,
        )

_local_dynamic = dynamic

def hairpin(
    descriptor: typing.Union[str, typing.List[DynamicBundle]],
    *,
    left_broken: bool = None,
    right_broken: bool = None,
    selector: typings.Selector = 'baca.tleaves()',
    ) -> PiecewiseIndicatorCommand:
    r"""
    Attaches hairpin indicators.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.hairpin('p < f'),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \<                                                                       %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
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
                            c''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            d''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Effort dynamic al niente:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.hairpin('"ff" >o niente'),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \baca_effort_ff                                                               %! SM8:EXPLICIT_DYNAMIC:PIC
                            - \tweak to-barline ##t                                                  %! PIC
                            - \tweak circled-tip ##t                                                 %! PIC
                            \>                                                                       %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
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
                            c''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            d''8
                            \!                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Effort dynamic dal niente:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.hairpin('niente o< "ff"'),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \!                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            - \tweak circled-tip ##t                                                 %! PIC
                            \<                                                                       %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
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
                            c''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            d''8
                            \baca_effort_ff                                                               %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Effort dynamic constante:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.hairpin('"p" -- f'),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \baca_effort_p                                                                %! SM8:EXPLICIT_DYNAMIC:PIC
                            - \tweak stencil #constante-hairpin                                      %! PIC
                            \<                                                                       %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
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
                            c''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            d''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Effort dynamics crescendo subito, decrescendo subito:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.hairpin(
        ...         '"mp" <| "f"',
        ...         selector=baca.leaves()[:7],
        ...         ),
        ...     baca.hairpin(
        ...         '"mf" |> "p"',
        ...         selector=baca.leaves()[7:],
        ...         ),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \baca_effort_mp                                                               %! SM8:EXPLICIT_DYNAMIC:PIC
                            - \tweak stencil #abjad-flared-hairpin                                   %! PIC
                            \<                                                                       %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \baca_effort_f                                                                %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            d''8
                            \baca_effort_mf                                                               %! SM8:EXPLICIT_DYNAMIC:PIC
                            - \tweak stencil #abjad-flared-hairpin                                   %! PIC
                            \>                                                                       %! PIC
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            d''8
                            \baca_effort_p                                                                %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Works with lone dynamic:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.hairpin('f'),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
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
                            c''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Works with lone hairpin:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 C5 G4 F5'),
        ...     baca.suite(
        ...         baca.hairpin('<'),
        ...         baca.dynamic('f', selector=baca.pleaf(-1)),
        ...         ),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            e'8
                            \<                                                                       %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            c''8
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
                            c''8
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:IC
                            d''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:IC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    if isinstance(descriptor, str):
        bundles = parse_descriptor(descriptor)
    else:
        bundles = descriptor
    bookend: typing.Union[bool, int] = False
    if 1 < len(bundles) and bundles[-1].has_dynamic_only:
        bookend = -1
    right_open: typing.Optional[bool] = None
    if bundles[-1].both():
        right_open = True
    if isinstance(selector, str):
        selector = eval(selector)
    assert isinstance(selector, abjad.Expression)
    piece_selector = selector.group()
    return hairpins(
        dynamics=bundles,
        bookend=bookend,
        left_broken=left_broken,
        piece_selector=piece_selector,
        right_broken=right_broken,
        right_open=right_open,
        selector=baca.select().leaves(),
        )

# TODO: move baca.hairpin() into baca.hairpins()
def hairpins(
    dynamics: typing.Union[str, typing.List],
    bookend: typing.Union[bool, int] = False,
    last_hairpin: typing.Union[bool, str, abjad.DynamicTrend] = None,
    left_broken: bool = None,
    piece_selector: typings.Selector = 'baca.tleaves().group()',
    right_broken: bool = None,
    right_open: bool = None,
    selector: typings.Selector = 'baca.tleaves()'
    ) -> PiecewiseIndicatorCommand:
    r"""
    Attaches hairpin indicators for consecutive hairpins.

    ..  container:: example

        Partitions leaves:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpins(
        ...         'p f',
        ...         piece_selector=baca.leaves().partition_by_counts(
        ...             [3],
        ...             cyclic=True,
        ...             overhang=True,
        ...             ),
        ...         ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
            <BLANKLINE>
                            d''8
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        With hairpins:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpins(
        ...         'p < f >',
        ...         last_hairpin=False,
        ...         piece_selector=baca.leaves().partition_by_counts(
        ...             [3],
        ...             cyclic=True,
        ...             overhang=True,
        ...             ),
        ...         ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \<                                                                       %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \>                                                                       %! PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \<                                                                       %! PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \>                                                                       %! PIC
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
            <BLANKLINE>
                            d''8
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Bookends piece -1:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpins(
        ...         'p f',
        ...         bookend=-1,
        ...         piece_selector=baca.leaves().partition_by_counts(
        ...             [3],
        ...             cyclic=True,
        ...             overhang=True,
        ...             ),
        ...         ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            d''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        With hairpins:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpins(
        ...         'p < f >',
        ...         bookend=-1,
        ...         piece_selector=baca.leaves().partition_by_counts(
        ...             [3],
        ...             cyclic=True,
        ...             overhang=True,
        ...             ),
        ...         ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \<                                                                       %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \>                                                                       %! PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \<                                                                       %! PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \>                                                                       %! PIC
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            f''8
                            [
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \<                                                                       %! PIC
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            d''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Bookends each piece:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpins(
        ...         'p f',
        ...         bookend=True,
        ...         piece_selector=baca.leaves().partition_by_counts(
        ...             [3],
        ...             cyclic=True,
        ...             overhang=True,
        ...             ),
        ...         ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            f'8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'DeepPink1)        %! SM6:REDUNDANT_DYNAMIC_COLOR:PIC
                            e''8
                            \f                                                                       %! SM8:REDUNDANT_DYNAMIC:PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            f''8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'DeepPink1)        %! SM6:REDUNDANT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:REDUNDANT_DYNAMIC:PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            f'8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'DeepPink1)        %! SM6:REDUNDANT_DYNAMIC_COLOR:PIC
                            e''8
                            \f                                                                       %! SM8:REDUNDANT_DYNAMIC:PIC
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            f''8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            [
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'DeepPink1)        %! SM6:REDUNDANT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:REDUNDANT_DYNAMIC:PIC
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            d''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        With hairpins:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpins(
        ...         'p < f >',
        ...         bookend=True,
        ...         piece_selector=baca.leaves().partition_by_counts(
        ...             [3],
        ...             cyclic=True,
        ...             overhang=True,
        ...             ),
        ...         ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \<                                                                       %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            f'8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \>                                                                       %! PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            g'8
                            [
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            f''8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \<                                                                       %! PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            d''8
                            [
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            f'8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \>                                                                       %! PIC
            <BLANKLINE>
                            g'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            f''8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            [
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \<                                                                       %! PIC
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            d''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    ..  container:: example

        Groups leaves by measures:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpins(
        ...         'p f',
        ...         piece_selector=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            g'8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            d''8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
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
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            f''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        With hairpins:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpins(
        ...         'p < f >',
        ...         last_hairpin=False,
        ...         piece_selector=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \<                                                                       %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            g'8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \>                                                                       %! PIC
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            d''8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \<                                                                       %! PIC
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
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            f''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            d''8
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Bookends piece -1:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpins(
        ...         'p f',
        ...         bookend=-1,
        ...         piece_selector=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            g'8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            d''8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
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
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            f''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            d''8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        With hairpins:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpins(
        ...         'p < f >',
        ...         bookend=-1,
        ...         piece_selector=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \<                                                                       %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            g'8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \>                                                                       %! PIC
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            e'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            d''8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \<                                                                       %! PIC
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
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            f''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \>                                                                       %! PIC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            d''8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        Bookends each piece:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpins(
        ...         'p f',
        ...         bookend=True,
        ...         piece_selector=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'DeepPink1)        %! SM6:REDUNDANT_DYNAMIC_COLOR:PIC
                            g'8
                            \f                                                                       %! SM8:REDUNDANT_DYNAMIC:PIC
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'DeepPink1)        %! SM6:REDUNDANT_DYNAMIC_COLOR:PIC
                            d''8
                            \p                                                                       %! SM8:REDUNDANT_DYNAMIC:PIC
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            g'8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'DeepPink1)        %! SM6:REDUNDANT_DYNAMIC_COLOR:PIC
                            f''8
                            \f                                                                       %! SM8:REDUNDANT_DYNAMIC:PIC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            d''8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

        With hairpins:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.minimum_duration((1, 12)),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     'MusicVoice',
        ...     baca.dls_staff_padding(5),
        ...     baca.hairpins(
        ...         'p -- f >',
        ...         bookend=True,
        ...         piece_selector=baca.group_by_measures([1]),
        ...     ),
        ...     baca.make_even_divisions(),
        ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
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
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
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
                            \override DynamicLineSpanner.staff-padding = #'5                         %! OC1
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            - \tweak stencil #constante-hairpin                                      %! PIC
                            \<                                                                       %! PIC
                            [
            <BLANKLINE>
                            d''8
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            g'8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \>                                                                       %! PIC
                            [
            <BLANKLINE>
                            f''8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            e'8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            d''8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            - \tweak stencil #constante-hairpin                                      %! PIC
                            \<                                                                       %! PIC
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e''8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            g'8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            f''8
                            \f                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            \>                                                                       %! PIC
                            [
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            \once \override Voice.DynamicText.color = #(x11-color 'blue)             %! SM6:EXPLICIT_DYNAMIC_COLOR:PIC
                            d''8
                            \p                                                                       %! SM8:EXPLICIT_DYNAMIC:PIC
                            ]
                            \revert DynamicLineSpanner.staff-padding                                 %! OC2
            <BLANKLINE>
                        }
                    }
                >>
            >>

    """
    if isinstance(dynamics, str):
        bundles = parse_descriptor(dynamics)
    else:
        bundles = dynamics
    for item in bundles:
        assert isinstance(item, DynamicBundle), repr(dynamic)
    last_hairpin_: typing.Union[bool, abjad.DynamicTrend, None] = None
    if isinstance(last_hairpin, bool):
        last_hairpin_ = last_hairpin
    elif isinstance(last_hairpin, str):
        last_hairpin_ = abjad.DynamicTrend(last_hairpin)
    if left_broken is not None:
        left_broken = bool(left_broken)
    if left_broken is True:
        bundle = bundles[0]
        assert bundle.dynamic_trend and not bundle.dynamic
        dynamic_trend = abjad.new(bundle.dynamic_trend, left_broken=True)
        bundle = DynamicBundle(dynamic_trend=dynamic_trend)
        bundles[0] = bundle
    right_broken_: typing.Any = False
    if bool(right_broken) is True:
        right_broken_ = abjad.LilyPondLiteral(r'\!', format_slot='after')
    if right_open is not None:
        right_open = bool(right_open)
    return PiecewiseIndicatorCommand(
        bookend=bookend,
        bundles=bundles,
        last_piece_spanner=last_hairpin_,
        piece_selector=piece_selector,
        right_broken=right_broken_,
        right_open=right_open,
        selector=selector,
        )

def possibile_dynamic(
    dynamic: str,
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> IndicatorCommand:
    r"""
    Attaches possibile dynamic.

    ..  container:: example

        Attaches possibilie dynamic to pitched head 0:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.possibile_dynamic('ff'),
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
                            \baca_ff_poss                                                                 %! IC
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

        Attaches possibile dynamic to pitched head 0 of tuplet 1:

        >>> music_maker = baca.MusicMaker()
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
        ...     baca.possibile_dynamic(
        ...         'ff',
        ...         selector=baca.tuplets()[1:2].phead(0),
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
                            \baca_ff_poss                                                                 %! IC
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
    command = rf'\baca_{dynamic}_poss'
    indicator = abjad.Dynamic(dynamic, command=command)
    return IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        )

def subito_dynamic(
    dynamic: str,
    *,
    selector: typings.Selector = 'baca.phead(0)',
    ) -> IndicatorCommand:
    """
    Attaches subito dynamic.
    """
    command = rf'\baca_{dynamic}_sub'
    indicator = abjad.Dynamic(dynamic, command=command)
    return IndicatorCommand(
        indicators=[indicator],
        selector=selector,
        )
