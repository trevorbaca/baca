import abjad
import baca
import typing
from abjad import rhythmmakertools as rhythmos
from .GlobalFermataCommand import GlobalFermataCommand
from .HairpinCommand import HairpinCommand
from .HorizontalSpacingSpecifier import HorizontalSpacingSpecifier
from .ImbricationCommand import ImbricationCommand
from .IndicatorCommand import IndicatorCommand
from .InstrumentChangeCommand import InstrumentChangeCommand
from .LabelCommand import LabelCommand
from .LBSD import LBSD
from .Loop import Loop
from .MetronomeMarkCommand import MetronomeMarkCommand
from .OverrideCommand import OverrideCommand
from .PitchCommand import PitchCommand
from .RhythmCommand import RhythmCommand
from .Scope import Scope
from .SpannerCommand import SpannerCommand
from .StaffPositionInterpolationCommand import \
    StaffPositionInterpolationCommand
from .SuiteCommand import SuiteCommand
from .Typing import Number
from .Typing import NumberPair
from .Typing import Selector


class LibraryGM(abjad.AbjadObject):
    r'''Library G - M.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(1) Library'

    __slots__ = (
        )

    mask_type = typing.Union[abjad.SilenceMask, abjad.SustainMask]

    ### PUBLIC METHODS ###

    @staticmethod
    def glissando(
        selector: Selector = 'baca.tleaves()',
        allow_repeats: bool = None,
        right_broken: bool = None,
        stems: bool = None,
        style: str = None,
        ) -> SpannerCommand:
        r'''Attaches glissando to trimmed leaves.

        ..  container:: example

            With segment-maker:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_even_runs(),
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
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
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
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 1]                                             %! SM4
                                    e'8
                                    \glissando                                                           %! SC
                                    [
                <BLANKLINE>
                                    d''8
                                    \glissando                                                           %! SC
                <BLANKLINE>
                                    f'8
                                    \glissando                                                           %! SC
                <BLANKLINE>
                                    e''8
                                    ]
                                    \glissando                                                           %! SC
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 2]                                             %! SM4
                                    g'8
                                    \glissando                                                           %! SC
                                    [
                <BLANKLINE>
                                    f''8
                                    \glissando                                                           %! SC
                <BLANKLINE>
                                    e'8
                                    ]
                                    \glissando                                                           %! SC
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 3]                                             %! SM4
                                    d''8
                                    \glissando                                                           %! SC
                                    [
                <BLANKLINE>
                                    f'8
                                    \glissando                                                           %! SC
                <BLANKLINE>
                                    e''8
                                    \glissando                                                           %! SC
                <BLANKLINE>
                                    g'8
                                    ]
                                    \glissando                                                           %! SC
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 4]                                             %! SM4
                                    f''8
                                    \glissando                                                           %! SC
                                    [
                <BLANKLINE>
                                    e'8
                                    \glissando                                                           %! SC
                <BLANKLINE>
                                    d''8
                                    ]
                <BLANKLINE>
                                }
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
            ...     baca.make_even_runs(),
            ...     baca.glissando(baca.plts()[:2]),
            ...     baca.glissando(baca.plts()[-2:]),
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
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
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
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 1]                                             %! SM4
                                    e'8
                                    \glissando                                                           %! SC
                                    [
                <BLANKLINE>
                                    d''8
                <BLANKLINE>
                                    f'8
                <BLANKLINE>
                                    e''8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 2]                                             %! SM4
                                    g'8
                                    [
                <BLANKLINE>
                                    f''8
                <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 3]                                             %! SM4
                                    d''8
                                    [
                <BLANKLINE>
                                    f'8
                <BLANKLINE>
                                    e''8
                <BLANKLINE>
                                    g'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 4]                                             %! SM4
                                    f''8
                                    [
                <BLANKLINE>
                                    e'8
                                    \glissando                                                           %! SC
                <BLANKLINE>
                                    d''8
                                    ]
                <BLANKLINE>
                                }
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
            ...         baca.glissando(),
            ...         baca.tuplets()[1:2].runs(),
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
                                \glissando                                                               %! SC
                                [
                                e''16
                                ]
                                \glissando                                                               %! SC
                                ef''4
                                ~
                                ef''16
                                r16
                                af''16
                                \glissando                                                               %! SC
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

        '''
        glissando = abjad.Glissando(
            allow_repeats=allow_repeats,
            stems=stems,
            style=style,
            )
        return SpannerCommand(
            right_broken=right_broken,
            selector=selector,
            spanner=glissando,
            )

    @staticmethod
    def glissando_thickness(
        n: Number,
        selector: Selector = 'baca.tleaves()',
        ) -> OverrideCommand:
        r'''Attaches glissando to trimmed leaves.
        '''
        return OverrideCommand(
            attribute='thickness',
            value=str(n),
            grob='glissando',
            selector=selector,
            )

    @staticmethod
    def global_fermata(
        description: str = None,
        selector: Selector = 'baca.leaf(0)',
        ) -> GlobalFermataCommand:
        r'''Attaches global fermata to leaves.
        '''
        return GlobalFermataCommand(
            description=description,
            selector=selector,
            )

    @staticmethod
    def hairpin(
        string: str = None,
        selector: Selector = 'baca.tleaves()',
        left_broken: str = None,
        right_broken: str = None,
        ) -> HairpinCommand:
        r'''Makes hairpin from ``string`` and attaches hairpin trimmed leaves.

        ..  container:: example

            Attaches hairpin to trimmed leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.hairpin('p < f'),
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
                                \<                                                                       %! HC1
                                \p                                                                       %! HC1
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
                                \f                                                                       %! HC1
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches hairpin to trimmed leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(baca.hairpin('p < f'), baca.tuplet(1)),
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
                                \<                                                                       %! HC1
                                \p                                                                       %! HC1
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
                                \f                                                                       %! HC1
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

            Attaches hairpin to trimmed leaves in each tuplets:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(baca.hairpin('p < f'), baca.tuplets()),
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
                                \<                                                                       %! HC1
                                \p                                                                       %! HC1
                                [
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                \f                                                                       %! HC1
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                \<                                                                       %! HC1
                                \p                                                                       %! HC1
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
                                \f                                                                       %! HC1
                                ]
                            }
                            \times 4/5 {
                                a'16
                                \p                                                                       %! HC1
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        '''
        hairpin = abjad.Hairpin(string)
        if left_broken is not None:
            assert isinstance(left_broken, bool), repr(left_broken)
        if right_broken not in ('niente', None):
            assert isinstance(right_broken, bool), repr(right_broken)
        if left_broken and hairpin.start_dynamic is not None:
            raise Exception(f'no start dynamic with left broken: {string!r}.')
        if right_broken and hairpin.stop_dynamic is not None:
            raise Exception(f'no stop dynamic with right broken: {string!r}.')
        if left_broken is True:
            left_broken = hairpin.shape_string
        if right_broken is True:
            right_broken = hairpin.shape_string
        command = HairpinCommand(
            left_broken=left_broken,
            right_broken=right_broken,
            selector=selector,
            start=hairpin.start_dynamic,
            stop=hairpin.stop_dynamic,
            )
        return command

    @staticmethod
    def hairpin_shorten_pair(
        pair: NumberPair,
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        r'''Overrides hairpin shorten pair.
        '''
        return OverrideCommand(
            attribute='shorten_pair',
            value=pair,
            grob='hairpin',
            selector=selector,
            )

    @staticmethod
    def hairpin_stencil_false(
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r'''Overrides hairpin stencil.
        '''
        return OverrideCommand(
            attribute='stencil',
            value=False,
            grob='hairpin',
            selector=selector,
            )

    @staticmethod
    def hairpin_transparent(
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r'''Overrides hairpin transparent.
        '''
        return OverrideCommand(
            attribute='transparent',
            value=True,
            grob='hairpin',
            selector=selector,
            )

    # TODO: deprecate in favor of baca.sequence()
    @staticmethod
    def helianthate(
        sequence: typing.Sequence,
        n: int = 0,
        m: int = 0,
        ) -> typing.Sequence:
        '''Helianthates `sequence` by outer index of rotation `n` and inner
        index of rotation `m`.

        ..  container:: example

            Helianthates list of lists:

            >>> sequence = [[1, 2, 3], [4, 5], [6, 7, 8]]
            >>> sequence = baca.helianthate(sequence, n=-1, m=1)
            >>> for item in sequence:
            ...     item
            [1, 2, 3]
            [4, 5]
            [6, 7, 8]
            [5, 4]
            [8, 6, 7]
            [3, 1, 2]
            [7, 8, 6]
            [2, 3, 1]
            [4, 5]
            [1, 2, 3]
            [5, 4]
            [6, 7, 8]
            [4, 5]
            [8, 6, 7]
            [3, 1, 2]
            [7, 8, 6]
            [2, 3, 1]
            [5, 4]

        ..  container:: example

            Helianthates list of segments:

            >>> J = abjad.PitchClassSegment(items=[0, 2, 4])
            >>> K = abjad.PitchClassSegment(items=[5, 6])
            >>> L = abjad.PitchClassSegment(items=[7, 9, 11])
            >>> sequence = baca.helianthate([J, K, L], n=-1, m=1)
            >>> for item in sequence:
            ...     item
            ...
            PitchClassSegment([0, 2, 4])
            PitchClassSegment([5, 6])
            PitchClassSegment([7, 9, 11])
            PitchClassSegment([6, 5])
            PitchClassSegment([11, 7, 9])
            PitchClassSegment([4, 0, 2])
            PitchClassSegment([9, 11, 7])
            PitchClassSegment([2, 4, 0])
            PitchClassSegment([5, 6])
            PitchClassSegment([0, 2, 4])
            PitchClassSegment([6, 5])
            PitchClassSegment([7, 9, 11])
            PitchClassSegment([5, 6])
            PitchClassSegment([11, 7, 9])
            PitchClassSegment([4, 0, 2])
            PitchClassSegment([9, 11, 7])
            PitchClassSegment([2, 4, 0])
            PitchClassSegment([6, 5])

        ..  container:: example

            Helianthates trivially:

            >>> sequence = [[1, 2, 3], [4, 5], [6, 7, 8]]
            >>> baca.helianthate(sequence)
            [[1, 2, 3], [4, 5], [6, 7, 8]]

        Returns new object with type equal to that of ``sequence``.
        '''
        sequence_type = type(sequence)
        start = list(sequence[:])
        result = list(sequence[:])
        assert isinstance(n, int), repr(n)
        assert isinstance(m, int), repr(m)
        original_n = n
        original_m = m

        def _generalized_rotate(argument, n=0):
            if hasattr(argument, 'rotate'):
                return argument.rotate(n=n)
            argument_type = type(argument)
            argument = baca.Sequence(argument).rotate(n=n)
            return argument_type(argument)
        while True:
            inner = [_generalized_rotate(_, m) for _ in sequence]
            candidate = _generalized_rotate(inner, n)
            if candidate == start:
                break
            result.extend(candidate)
            n += original_n
            m += original_m
        result_ = sequence_type(result) # type: ignore
        return result_

    @staticmethod
    def imbricate(
        voice_name: str,
        segment: typing.List,
        *specifiers: typing.Any,
        allow_unused_pitches: bool = None,
        by_pitch_class: bool = None,
        extend_beam: bool = None,
        hocket: bool = None,
        selector: Selector = None,
        truncate_ties: bool = None
        ):
        r'''Imbricates `segment` in `voice_name`.

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

        '''
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

    @staticmethod
    def instrument(
        instrument: abjad.Instrument,
        selector: Selector = 'baca.leaf(0)',
        ) -> InstrumentChangeCommand:
        r'''Makes instrument change command.
        '''
        if not isinstance(instrument, abjad.Instrument):
            message = f'instrument must be instrument (not {instrument!r}).'
            raise Exception(message)
        return InstrumentChangeCommand(
            indicators=[instrument],
            selector=selector,
            )

    @staticmethod
    def interpolate_staff_positions(
        start_pitch: typing.Union[str, abjad.NamedPitch],
        stop_pitch: typing.Union[str, abjad.NamedPitch],
        selector: Selector = 'baca.plts()',
        ) -> StaffPositionInterpolationCommand:
        r'''Interpolates from staff position of ``start_pitch`` to staff
        position of ``stop_pitch``.
        '''
        return StaffPositionInterpolationCommand(
            start_pitch=start_pitch,
            stop_pitch=stop_pitch,
            selector=selector,
            )

    @staticmethod
    def invisible_line_segment() -> abjad.LineSegment:
        r'''Makes invisible line segment.

        ..  container:: example

            >>> abjad.f(baca.invisible_line_segment())
            abjad.LineSegment(
                dash_period=0,
                left_broken_text=False,
                left_hspace=0.25,
                left_stencil_align_direction_y=Center,
                right_broken_padding=0,
                right_broken_text=False,
                right_padding=1.5,
                right_stencil_align_direction_y=Center,
                )

        '''
        return abjad.LineSegment(
            dash_period=0,
            left_broken_text=False,
            left_hspace=0.25,
            left_stencil_align_direction_y=abjad.Center,
            right_broken_padding=0,
            right_broken_text=False,
            right_padding=1.5,
            right_stencil_align_direction_y=abjad.Center,
            )

    @staticmethod
    def label(
        expression: abjad.Expression,
        selector: Selector = 'baca.leaves()',
        ) -> LabelCommand:
        r'''Labels selections with label `expression`.

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
                                [
                                ^ \markup {
                                    \small
                                        C4
                                    }
                                d'16
                                ]
                                ^ \markup {
                                    \small
                                        D4
                                    }
                                bf'4
                                ~
                                ^ \markup {
                                    \small
                                        Bb4
                                    }
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                [
                                ^ \markup {
                                    \small
                                        "F#5"
                                    }
                                e''16
                                ]
                                ^ \markup {
                                    \small
                                        E5
                                    }
                                ef''4
                                ~
                                ^ \markup {
                                    \small
                                        Eb5
                                    }
                                ef''16
                                r16
                                af''16
                                [
                                ^ \markup {
                                    \small
                                        Ab5
                                    }
                                g''16
                                ]
                                ^ \markup {
                                    \small
                                        G5
                                    }
                            }
                            \times 4/5 {
                                a'16
                                ^ \markup {
                                    \small
                                        A4
                                    }
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
            ...         baca.tuplet(1),
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
                                ^ \markup {
                                    \small
                                        "F#5"
                                    }
                                e''16
                                ]
                                ^ \markup {
                                    \small
                                        E5
                                    }
                                ef''4
                                ~
                                ^ \markup {
                                    \small
                                        Eb5
                                    }
                                ef''16
                                r16
                                af''16
                                [
                                ^ \markup {
                                    \small
                                        Ab5
                                    }
                                g''16
                                ]
                                ^ \markup {
                                    \small
                                        G5
                                    }
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        '''
        return LabelCommand(expression=expression, selector=selector)

    @staticmethod
    def laissez_vibrer(
        selector: Selector  = 'baca.ptails()',
        ) -> IndicatorCommand:
        r'''Attaches laissez vibrer to PLT tails.

        ..  container:: example

            Attaches laissez vibrer to all PLT tails:

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
                                -\laissezVibrer                                                          %! IC
                                ]
                                bf'4
                                ~
                                bf'16
                                -\laissezVibrer                                                          %! IC
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
                                -\laissezVibrer                                                          %! IC
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
            ...     baca.laissez_vibrer(baca.tuplets()[1:2].ptails()),
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

        '''
        return IndicatorCommand(
            indicators=[abjad.Articulation('laissezVibrer')],
            selector=selector,
            )

    @staticmethod
    def lbsd(
        y_offset: int,
        alignment_distances: typing.Sequence,
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        r'''Makes line-break system details.
        '''
        alignment_distances = baca.sequence(alignment_distances).flatten()
        lbsd = LBSD(
            alignment_distances=alignment_distances,
            y_offset=y_offset,
            )
        return IndicatorCommand(
            indicators=[lbsd],
            selector=selector,
            )

    @staticmethod
    def literal(
        string: str,
        format_slot: str = 'before',
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        r'''Makes LilyPond literal.
        '''
        literal = abjad.LilyPondLiteral(string, format_slot=format_slot)
        return IndicatorCommand(
            indicators=[literal],
            selector=selector,
            )

    @staticmethod
    def long_fermata(
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        r'''Attaches long fermata to leaf.

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
            ...     baca.long_fermata(baca.tuplets()[1:2].phead(0)),
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

        '''
        return IndicatorCommand(
            indicators=[abjad.Articulation('longfermata')],
            selector=selector,
            )

    @staticmethod
    def loop(
        pitches: typing.Iterable,
        intervals: typing.Iterable,
        ) -> PitchCommand:
        r'''Loops `pitches` at `intervals`.
        '''
        from baca.tools.LibraryNS import LibraryNS
        loop = Loop(items=pitches, intervals=intervals)
        return LibraryNS.pitches(loop)

    @staticmethod
    def make_even_runs() -> RhythmCommand:
        r'''Makes even runs.
        '''
        return RhythmCommand(
            rhythm_maker=rhythmos.EvenRunRhythmMaker()
            )

    @staticmethod
    def make_fused_tuplet_monads(
        tuplet_ratio: typing.Tuple[int] = None,
        ) -> RhythmCommand:
        r'''Makes fused tuplet monads.
        '''
        tuplet_ratios = []
        if tuplet_ratio is None:
            tuplet_ratios.append((1,))
        else:
            tuplet_ratios.append(tuplet_ratio)
        return RhythmCommand(
            division_expression=abjad.sequence()
                .sum()
                .sequence(),
            rhythm_maker=rhythmos.TupletRhythmMaker(
                tie_specifier=rhythmos.TieSpecifier(
                    repeat_ties=True,
                    ),
                tuplet_ratios=tuplet_ratios,
                ),
            )

    @staticmethod
    def make_multimeasure_rests() -> RhythmCommand:
        r'''Makes multimeasure rests.
        '''
        mask = rhythmos.SilenceMask(
            pattern=abjad.index_all(),
            use_multimeasure_rests=True,
            )
        return RhythmCommand(
            rhythm_maker=rhythmos.NoteRhythmMaker(
                division_masks=[mask],
                ),
            )

    @staticmethod
    def make_notes(
        division_mask: mask_type = None,
        repeat_ties: bool = False,
        ) -> RhythmCommand:
        r'''Makes notes; rewrites meter.
        '''
        if division_mask is None:
            division_masks = None
        else:
            division_masks = [division_mask]
        if repeat_ties:
            tie_specifier = rhythmos.TieSpecifier(repeat_ties=True)
        else:
            tie_specifier = None
        return RhythmCommand(
            rewrite_meter=True,
            rhythm_maker=rhythmos.NoteRhythmMaker(
                division_masks=division_masks,
                tie_specifier=tie_specifier,
                )
            )

    @staticmethod
    def make_repeat_tied_notes(
        division_mask: mask_type = None,
        ) -> RhythmCommand:
        r'''Makes repeat-tied notes; rewrites meter.
        '''
        if division_mask is None:
            division_masks = None
        elif isinstance(division_mask, list):
            division_masks = division_mask[:]
        else:
            division_masks = [division_mask]
        return RhythmCommand(
            rewrite_meter=True,
            rhythm_maker=rhythmos.NoteRhythmMaker(
                division_masks=division_masks,
                tie_specifier=rhythmos.TieSpecifier(
                    tie_across_divisions=True,
                    repeat_ties=True,
                    ),
                ),
            )

    @staticmethod
    def make_repeated_duration_notes(
        durations: typing.Iterable,
        beam_specifier: rhythmos.BeamSpecifier = None,
        division_mask: abjad.Pattern = None,
        rewrite_meter: bool = True,
        ) -> RhythmCommand:
        r'''Makes repeated-duration notes.
        '''
        from baca.tools.LibraryNS import LibraryNS
        if division_mask is None:
            division_masks = None
        else:
            division_masks = [division_mask]
        if isinstance(durations, abjad.Duration):
            durations = [durations]
        elif isinstance(durations, tuple):
            assert len(durations) == 2
            durations = [abjad.Duration(durations)]
        tie_specifier = rhythmos.TieSpecifier(
            repeat_ties=True,
            )
        division_expression = LibraryNS.split_by_durations(durations=durations)
        return RhythmCommand(
            division_expression=division_expression,
            rewrite_meter=rewrite_meter,
            rhythm_maker=rhythmos.NoteRhythmMaker(
                beam_specifier=beam_specifier,
                division_masks=division_masks,
                tie_specifier=tie_specifier,
                ),
            )

    @staticmethod
    def make_rests() -> RhythmCommand:
        r'''Makes rests.
        '''
        return RhythmCommand(
            rhythm_maker=rhythmos.NoteRhythmMaker(
                division_masks=[abjad.silence([0], 1)],
                ),
            )
    
    @staticmethod
    def make_rhythm(selection: abjad.Selection) -> RhythmCommand:
        r'''Set rhythm to `selection`.
        '''
        assert isinstance(selection, abjad.Selection), repr(selection)
        assert all(isinstance(_,  abjad.Component) for _ in selection)
        return RhythmCommand(
            rhythm_maker=selection,
            )

    @staticmethod
    def make_single_attack(duration) -> RhythmCommand:
        r'''Makes single attacks with `duration`.
        '''
        duration = abjad.Duration(duration)
        numerator, denominator = duration.pair
        rhythm_maker = rhythmos.IncisedRhythmMaker(
            incise_specifier=rhythmos.InciseSpecifier(
                fill_with_notes=False,
                outer_divisions_only=True,
                prefix_talea=[numerator],
                prefix_counts=[1],
                talea_denominator=denominator,
                ),
            )
        return RhythmCommand(
            rhythm_maker=rhythm_maker,
            )

    @staticmethod
    def make_skips() -> RhythmCommand:
        r'''Makes skips.
        '''
        return RhythmCommand(
            rhythm_maker=rhythmos.SkipRhythmMaker()
            )

    @staticmethod
    def make_tied_notes() -> RhythmCommand:
        r'''Makes tied notes; rewrites meter.
        '''
        return RhythmCommand(
            rewrite_meter=True,
            rhythm_maker=rhythmos.NoteRhythmMaker(
                tie_specifier=rhythmos.TieSpecifier(
                    tie_across_divisions=True,
                    ),
                ),
            )

    @staticmethod
    def make_tied_repeated_durations(
        durations: typing.Iterable,
        ) -> RhythmCommand:
        r'''Makes tied repeated durations.
        '''
        command = LibraryGM.make_repeated_duration_notes(durations)
        return abjad.new(
            command,
            rewrite_meter=False,
            rhythm_maker__tie_specifier__tie_across_divisions=True,
            )

    @staticmethod
    def marcati(
        selector: Selector = 'baca.pheads()',
        ) -> IndicatorCommand:
        r'''Attaches marcati to pitched heads.

        ..  container:: example

            Attaches marcati to all pitched heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.marcati(),
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
                                -\marcato                                                                %! IC
                                ]
                                bf'4
                                -\marcato                                                                %! IC
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
                                -\marcato                                                                %! IC
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches marcati to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.marcati(baca.tuplets()[1:2].pheads()),
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

        '''
        return IndicatorCommand(
            indicators=[abjad.Articulation('marcato')],
            selector=selector,
            )

    @staticmethod
    def margin_markup(
        argument: str,
        alert: IndicatorCommand = None,
        context: str = 'Staff',
        selector: Selector = 'baca.leaf(0)',
        ) -> typing.Union[IndicatorCommand, SuiteCommand]:
        r'''Sets margin markup on each leaf in `selector` output.

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
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
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

        '''
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
            return SuiteCommand([command, alert])
        else:
            return command

    @staticmethod
    def metronome_mark(
        key: str,
        selector: Selector = 'baca.leaf(0)',
        ) -> MetronomeMarkCommand:
        r'''Attaches metronome mark with `key`.
        '''
        return MetronomeMarkCommand(
            key=key,
            selector=selector,
            )

    @staticmethod
    def minimum_duration(
        duration: typing.Union[tuple, abjad.Duration],
        ) -> HorizontalSpacingSpecifier:
        r'''Makes horizontal spacing specifier with `duration` minimum width.
        '''
        return HorizontalSpacingSpecifier(
            minimum_duration=duration,
            )

    @staticmethod
    def mmrest_text_color(
        color: str = 'red',
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r'''Overrides multimeasure rest text color.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.markup.boxed('still', selector=baca.leaf(1)),
            ...     baca.mmrest_text_color('red'),
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
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
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
                                \override MultiMeasureRestText.color = #red                              %! OC1
                                R1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                R1 * 3/8
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            \override                                                    %! IC
                                                #'(box-padding . 0.5)                                    %! IC
                                                \box                                                     %! IC
                                                    still                                                %! IC
                                    }                                                                    %! IC
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                R1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                R1 * 3/8
                                \revert MultiMeasureRestText.color                                       %! OC2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Raises exception when called on leaves other than multimeasure
            rests:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_notes(),
            ...     baca.markup.boxed('still', selector=baca.leaf(1)),
            ...     baca.mmrest_text_color('red'),
            ...     baca.pitches([2, 4]),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            Traceback (most recent call last):
                ...
            Exception: only MultimeasureRest (not Note) allowed.

        '''
        return OverrideCommand(
            attribute='color',
            value=color,
            grob='multi_measure_rest_text',
            selector=selector,
            whitelist=(abjad.MultimeasureRest,),
            )

    @staticmethod
    def mmrest_text_extra_offset(
        pair: NumberPair,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r'''Overrides multimeasure rest text extra offset.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.markup.boxed('still', selector=baca.leaf(1)),
            ...     baca.mmrest_text_extra_offset((0, 2)),
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
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
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
                                \override MultiMeasureRestText.extra-offset = #'(0 . 2)                  %! OC1
                                R1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                R1 * 3/8
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            \override                                                    %! IC
                                                #'(box-padding . 0.5)                                    %! IC
                                                \box                                                     %! IC
                                                    still                                                %! IC
                                    }                                                                    %! IC
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                R1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                R1 * 3/8
                                \revert MultiMeasureRestText.extra-offset                                %! OC2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        '''
        return OverrideCommand(
            attribute='extra_offset',
            value=pair,
            grob='multi_measure_rest_text',
            selector=selector,
            whitelist=(abjad.MultimeasureRest,),
            )

    @staticmethod
    def mmrest_text_padding(
        n: Number,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r'''Overrides multimeasure rest text padding.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.markup.boxed('still', selector=baca.leaf(1)),
            ...     baca.mmrest_text_padding(2),
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
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
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
                                \override MultiMeasureRestText.padding = #2                              %! OC1
                                R1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                R1 * 3/8
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            \override                                                    %! IC
                                                #'(box-padding . 0.5)                                    %! IC
                                                \box                                                     %! IC
                                                    still                                                %! IC
                                    }                                                                    %! IC
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                R1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                R1 * 3/8
                                \revert MultiMeasureRestText.padding                                     %! OC2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        '''
        return OverrideCommand(
            attribute='padding',
            value=n,
            grob='multi_measure_rest_text',
            selector=selector,
            whitelist=(abjad.MultimeasureRest,),
            )

    @staticmethod
    def mmrest_text_parent_center(
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r'''Overrides multimeasure rest text parent alignment X to center.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.markup.boxed('still', selector=baca.leaf(1)),
            ...     baca.mmrest_text_parent_center(),
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
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
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
                                \override MultiMeasureRestText.parent-alignment-X = #0                   %! OC1
                                R1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                R1 * 3/8
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            \override                                                    %! IC
                                                #'(box-padding . 0.5)                                    %! IC
                                                \box                                                     %! IC
                                                    still                                                %! IC
                                    }                                                                    %! IC
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                R1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                R1 * 3/8
                                \revert MultiMeasureRestText.parent-alignment-X                          %! OC2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        '''
        return OverrideCommand(
            attribute='parent_alignment_X',
            value=0,
            grob='multi_measure_rest_text',
            selector=selector,
            whitelist=(abjad.MultimeasureRest,),
            )

    @staticmethod
    def mmrest_text_staff_padding(
        n: Number,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r'''Overrides multimeasure rest text staff padding.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.markup.boxed('still', selector=baca.leaf(1)),
            ...     baca.mmrest_text_staff_padding(2),
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
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/2
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
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
                                \override MultiMeasureRestText.staff-padding = #2                        %! OC1
                                R1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                R1 * 3/8
                                ^ \markup {                                                              %! IC
                                    \whiteout                                                            %! IC
                                        \upright                                                         %! IC
                                            \override                                                    %! IC
                                                #'(box-padding . 0.5)                                    %! IC
                                                \box                                                     %! IC
                                                    still                                                %! IC
                                    }                                                                    %! IC
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                R1 * 1/2
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                R1 * 3/8
                                \revert MultiMeasureRestText.staff-padding                               %! OC2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        '''
        return OverrideCommand(
            attribute='staff_padding',
            value=n,
            grob='multi_measure_rest_text',
            selector=selector,
            whitelist=(abjad.MultimeasureRest,),
            )
