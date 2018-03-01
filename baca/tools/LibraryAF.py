import abjad
import baca
import typing
from abjad import rhythmmakertools as rhythmos
from .AccidentalAdjustmentCommand import AccidentalAdjustmentCommand
from .AnchorSpecifier import AnchorSpecifier
from .BreakMeasureMap import BreakMeasureMap
from .ClusterCommand import ClusterCommand
from .Coat import Coat
from .ColorCommand import ColorCommand
from .ColorFingeringCommand import ColorFingeringCommand
from .Command import Command
from .ContainerCommand import ContainerCommand
from .DiatonicClusterCommand import DiatonicClusterCommand
from .DivisionSequenceExpression import DivisionSequenceExpression
from .IndicatorCommand import IndicatorCommand
from .MicrotoneDeviationCommand import MicrotoneDeviationCommand
from .OctaveDisplacementCommand import OctaveDisplacementCommand
from .OverrideCommand import OverrideCommand
from .PersistentOverride import PersistentOverride
from .RegisterToOctaveCommand import RegisterToOctaveCommand
from .SuiteCommand import SuiteCommand
from .Typing import Number
from .Typing import NumberPair
from .Typing import Selector


class LibraryAF(abjad.AbjadObject):
    r'''Library A - F.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(1) Library'

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    @staticmethod
    def accents(
        selector: Selector = 'baca.pheads()',
        ) -> IndicatorCommand:
        r'''Attaches accents to pitched heads.

        ..  container:: example

            Attaches accents to all pitched heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.accents(),
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
                                -\accent                                                                 %! IC
                                [
                                d'16
                                -\accent                                                                 %! IC
                                ]
                                bf'4
                                -\accent                                                                 %! IC
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                -\accent                                                                 %! IC
                                [
                                e''16
                                -\accent                                                                 %! IC
                                ]
                                ef''4
                                -\accent                                                                 %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\accent                                                                 %! IC
                                [
                                g''16
                                -\accent                                                                 %! IC
                                ]
                            }
                            \times 4/5 {
                                a'16
                                -\accent                                                                 %! IC
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches accents to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(baca.accents(), baca.tuplet(1)),
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
                                -\accent                                                                 %! IC
                                [
                                e''16
                                -\accent                                                                 %! IC
                                ]
                                ef''4
                                -\accent                                                                 %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\accent                                                                 %! IC
                                [
                                g''16
                                -\accent                                                                 %! IC
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
            indicators=[abjad.Articulation('>')],
            selector=selector,
            )

    @staticmethod
    def alternate_bow_strokes(
        downbow_first: bool = True,
        selector: Selector = 'baca.pheads()',
        ) -> IndicatorCommand:
        r'''Attaches alternate bow strokes.

        :param downbow_first: is true when first stroke is down-bow.

        ..  container:: example

            Attaches alternate bow strokes to all pitched heads (down-bow
            first):

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.alternate_bow_strokes(downbow_first=True),
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
                                -\downbow                                                                %! IC
                                [
                                d'16
                                -\upbow                                                                  %! IC
                                ]
                                bf'4
                                -\downbow                                                                %! IC
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                -\upbow                                                                  %! IC
                                [
                                e''16
                                -\downbow                                                                %! IC
                                ]
                                ef''4
                                -\upbow                                                                  %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\downbow                                                                %! IC
                                [
                                g''16
                                -\upbow                                                                  %! IC
                                ]
                            }
                            \times 4/5 {
                                a'16
                                -\downbow                                                                %! IC
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches alternate bow strokes to all pitched heads (up-bow first):

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.alternate_bow_strokes(downbow_first=False),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(6),
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
                                \override TupletBracket.staff-padding = #6                               %! OC1
                                r8
                                c'16
                                -\upbow                                                                  %! IC
                                [
                                d'16
                                -\downbow                                                                %! IC
                                ]
                                bf'4
                                -\upbow                                                                  %! IC
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                -\downbow                                                                %! IC
                                [
                                e''16
                                -\upbow                                                                  %! IC
                                ]
                                ef''4
                                -\downbow                                                                %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\upbow                                                                  %! IC
                                [
                                g''16
                                -\downbow                                                                %! IC
                                ]
                            }
                            \times 4/5 {
                                a'16
                                -\upbow                                                                  %! IC
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches alternate bow strokes to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.alternate_bow_strokes(),
            ...         baca.tuplet(1),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(6),
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
                                \override TupletBracket.staff-padding = #6                               %! OC1
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
                                -\downbow                                                                %! IC
                                [
                                e''16
                                -\upbow                                                                  %! IC
                                ]
                                ef''4
                                -\downbow                                                                %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\upbow                                                                  %! IC
                                [
                                g''16
                                -\downbow                                                                %! IC
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
        if downbow_first:
            strings = ['downbow', 'upbow']
        else:
            strings = ['upbow', 'downbow']
        indicators = [abjad.Articulation(_) for _ in strings]
        return IndicatorCommand(
            indicators=indicators,
            selector=selector,
            )

    @staticmethod
    def anchor(
        remote_voice_name: str,
        remote_selector: Selector = None,
        local_selector: Selector = None,
        ) -> AnchorSpecifier:
        r'''Anchors music in this figure (filtered by ``local_selector``) to
        start offset of ``remote_voice_name`` (filtered by
        ``remote_selector``).

        :param remote_voice_name: name of voice to which this music anchors.

        :param remote_seelctor: selector applied to remote voice.

        :param local_selector: selector applied to this music.
        '''
        return AnchorSpecifier(
            local_selector=local_selector,
            remote_selector=remote_selector,
            remote_voice_name=remote_voice_name,
            )

    @staticmethod
    def anchor_after(
        remote_voice_name: str,
        remote_selector: Selector = None,
        local_selector: Selector = None,
        ) -> AnchorSpecifier:
        r'''Anchors music in this figure (filtered by ``local_selector``) to
        stop offset of ``remote_voice_name`` (filtered by ``remote_selector``).

        :param remote_voice_name: name of voice to which this music anchors.

        :param remote_selector: selector applied to remote voice.

        :param local_selector: selector applied to this music.
        '''
        return AnchorSpecifier(
            local_selector=local_selector,
            remote_selector=remote_selector,
            remote_voice_name=remote_voice_name,
            use_remote_stop_offset=True,
            )

    @staticmethod
    def anchor_to_figure(figure_name: str) -> AnchorSpecifier:
        r'''Anchors music in this figure to start of ``figure_name``.

        :param figure_name: figure name.
        '''
        return AnchorSpecifier(
            figure_name=figure_name,
            )

    @staticmethod
    def ancora_dynamic(
        dynamic: str,
        selector: Selector = 'baca.phead(0)',
        ) -> IndicatorCommand:
        r'''Attaches ancora dynamic pitched head 0.

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
                                \ff_ancora                                                               %! IC
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
            ...         baca.tuplets()[1:2].phead(0),
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
                                \ff_ancora                                                               %! IC
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
        command = rf'\{dynamic}_ancora'
        indicator = abjad.Dynamic(dynamic, command=command)
        return IndicatorCommand(
            indicators=[indicator],
            selector=selector,
            )

    @staticmethod
    def arpeggios(
        selector: Selector = 'baca.cheads()',
        ) -> IndicatorCommand:
        r"""Attaches arpeggios.

        ..  container:: example

            Attaches arpeggios to all chord heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.arpeggios(),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
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
                            \scaleDurations #'(1 . 1) {
                                <c' d' bf'>8
                                -\arpeggio                                                               %! IC
                                ~
                                [
                                <c' d' bf'>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                f''8
                                ~
                                [
                                f''32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                <ef'' e'' fs'''>8
                                -\arpeggio                                                               %! IC
                                ~
                                [
                                <ef'' e'' fs'''>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                <g' af''>8
                                -\arpeggio                                                               %! IC
                                ~
                                [
                                <g' af''>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                a'8
                                ~
                                [
                                a'32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches arpeggios to last two chord heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.arpeggios(baca.cheads()[-2:]),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
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
                            \scaleDurations #'(1 . 1) {
                                <c' d' bf'>8
                                ~
                                [
                                <c' d' bf'>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                f''8
                                ~
                                [
                                f''32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                <ef'' e'' fs'''>8
                                -\arpeggio                                                               %! IC
                                ~
                                [
                                <ef'' e'' fs'''>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                <g' af''>8
                                -\arpeggio                                                               %! IC
                                ~
                                [
                                <g' af''>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                a'8
                                ~
                                [
                                a'32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        """
        return IndicatorCommand(
            indicators=[abjad.Articulation('arpeggio')],
            selector=selector,
            )

    @staticmethod
    def articulation(
        articulation: str,
        selector: Selector = 'baca.phead(0)',
        ) -> IndicatorCommand:
        r'''Attaches articulation to ``selector`` output.
        '''
        articulation_ = abjad.Articulation(articulation)
        return IndicatorCommand(
            indicators=[articulation_],
            selector=selector,
            )

    @staticmethod
    def articulations(
        articulations: typing.List,
        selector: Selector = 'baca.pheads()',
        ) -> IndicatorCommand:
        r'''Attaches articulations.
        '''
        return IndicatorCommand(
            indicators=articulations,
            selector=selector,
            )

    @staticmethod
    def bar_extent(
        pair: NumberPair,
        selector: Selector = 'baca.leaf(0)',
        after: bool = False,
        ) -> OverrideCommand:
        r'''Overrides bar line bar extent.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 12)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.bar_extent((-4, 4), baca.group_by_measure()[1]),
            ...     baca.bar_extent((-4, 4), baca.leaf(-1), after=True),
            ...     baca.make_even_runs(),
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
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 1]                                             %! SM4
                                    e'8
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
                                    \override Staff.BarLine.bar-extent = #'(-4 . 4)                      %! OC1
                                    g'8
                                    [
                <BLANKLINE>
                                    f''8
                <BLANKLINE>
                                    e'8
                                    ]
                                    \revert Staff.BarLine.bar-extent                                     %! OC2
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
                <BLANKLINE>
                                    d''8
                                    ]
                                    \once \override Staff.BarLine.bar-extent = #'(-4 . 4)                %! OC1
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        '''
        return OverrideCommand(
            after=after,
            attribute='bar_extent',
            context='Staff',
            grob='bar_line',
            selector=selector,
            value=pair,
            )

    @staticmethod
    def bar_extent_zero(
        selector: Selector = 'baca.leaves()',
        ) -> SuiteCommand:
        r'''Makes bar-extent zero suite.
        '''
        return SuiteCommand(
            [
                LibraryAF.bar_extent(
                    (0, 0),
                    after=True,
                    selector='baca.leaves()',
                    ),
                LibraryAF.bar_extent(
                    (0, 0),
                    after=True,
                    selector='baca.leaf(-1)',
                    ),
                ],
            selector=selector,
            )

    @staticmethod
    def bar_extent_persistent(
        pair: NumberPair = None,
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        r'''Makes persistent bar-extent override.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_width((1, 12)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.bar_extent_persistent((0, 0)),
            ...     baca.make_even_runs(),
            ...     baca.staff_lines(1),
            ...     baca.staff_position(0),
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
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 1]                                             %! SM4
                                    \override Staff.BarLine.bar-extent = #'(0 . 0)                       %! SM8:EXPLICIT_PERSISTENT_OVERRIDE:IC
                                    \stopStaff                                                           %! SM8:EXPLICIT_STAFF_LINES:IC
                                    \once \override Staff.StaffSymbol.line-count = 1                     %! SM8:EXPLICIT_STAFF_LINES:IC
                                    \startStaff                                                          %! SM8:EXPLICIT_STAFF_LINES:IC
                                    \once \override Staff.StaffSymbol.color = #(x11-color 'blue)         %! SM6:EXPLICIT_STAFF_LINES_COLOR:IC
                                    b'8
                                    [
                <BLANKLINE>
                                    b'8
                <BLANKLINE>
                                    b'8
                <BLANKLINE>
                                    b'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 2]                                             %! SM4
                                    b'8
                                    [
                <BLANKLINE>
                                    b'8
                <BLANKLINE>
                                    b'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 3]                                             %! SM4
                                    b'8
                                    [
                <BLANKLINE>
                                    b'8
                <BLANKLINE>
                                    b'8
                <BLANKLINE>
                                    b'8
                                    ]
                                }
                                {
                <BLANKLINE>
                                    % [MusicVoice measure 4]                                             %! SM4
                                    b'8
                                    [
                <BLANKLINE>
                                    b'8
                <BLANKLINE>
                                    b'8
                                    ]
                <BLANKLINE>
                                }
                            }
                        }
                    >>
                >>

        '''
        override = PersistentOverride(
            after=True,
            attribute='bar_extent',
            context='Staff',
            grob='bar_line',
            value=pair,
            )
        return IndicatorCommand(
            indicators=[override],
            selector=selector,
            )

    @staticmethod
    def bass_to_octave(
        n: int,
        selector: Selector = 'baca.plts()',
        ) -> RegisterToOctaveCommand:
        r"""Octave-transposes music.

        ..  container:: example

            Octave-transposes music such that the lowest note in the entire
            selection appears in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.bass_to_octave(3),
            ...     baca.color(baca.plts().group()),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
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
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <c d bf>8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <c d bf>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                f'8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                f'32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <ef' e' fs''>8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <ef' e' fs''>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <g af'>8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <g af'>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Octave-transposes music such that the lowest pitch in each pitched
            logical tie appears in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.map(baca.bass_to_octave(3), baca.plts()),
            ...     baca.color(baca.plts()),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
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
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <c d bf>8
                                ~
                                [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <c d bf>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                f8
                                ~
                                [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                f32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef e fs'>8
                                ~
                                [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef e fs'>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                <g af'>8
                                ~
                                [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                <g af'>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a8
                                ~
                                [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Octave-transposes music such that the lowest pitch in each of the
            last two pitched logical ties appears in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.map(baca.bass_to_octave(3), baca.plts()[-2:]),
            ...     baca.color(baca.plts()[-2:]),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
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
                            \scaleDurations #'(1 . 1) {
                                <c' d' bf'>8
                                ~
                                [
                                <c' d' bf'>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                f''8
                                ~
                                [
                                f''32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                <ef'' e'' fs'''>8
                                ~
                                [
                                <ef'' e'' fs'''>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <g af'>8
                                ~
                                [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <g af'>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                a8
                                ~
                                [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                a32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        """
        return RegisterToOctaveCommand(
            anchor=abjad.Bottom,
            octave_number=n,
            selector=selector,
            )

    @staticmethod
    def beam_divisions(
        stemlets: Number = None,
        ) -> rhythmos.BeamSpecifier:
        r'''Beams divisions.

        ..  container:: example

            Beams divisions:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.beam_divisions(),
            ...     baca.rests_around([2], [2]),
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
                            \scaleDurations #'(1 . 1) {
                                r8
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                a'16
                                r8
                            }
                        }
                    }
                >>

        ..  container:: example

            Beams divisions with stemlets:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.beam_divisions(stemlets=2),
            ...     baca.rests_around([2], [2]),
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
                            \scaleDurations #'(1 . 1) {
                                \override Staff.Stem.stemlet-length = 2
                                r8
                                [
                                c'16
                                d'16
                                \revert Staff.Stem.stemlet-length
                                bf'16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                \override Staff.Stem.stemlet-length = 2
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                \revert Staff.Stem.stemlet-length
                                g''16
                                ]
                            }
                            \scaleDurations #'(1 . 1) {
                                \override Staff.Stem.stemlet-length = 2
                                a'16
                                [
                                \revert Staff.Stem.stemlet-length
                                r8
                                ]
                            }
                        }
                    }
                >>

        '''
        return rhythmos.BeamSpecifier(
            beam_each_division=True,
            beam_rests=bool(stemlets),
            stemlet_length=stemlets,
            )

    @staticmethod
    def beam_everything(
        hide_nibs: bool = False,
        stemlets: Number = None,
        ) -> rhythmos.BeamSpecifier:
        r'''Beams everything.

        ..  container:: example

            Beams everything:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.beam_everything(),
            ...     baca.rests_around([2], [2]),
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
                            \scaleDurations #'(1 . 1) {
                                r8
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                c'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                bf'16
                            }
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                fs''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                e''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                ef''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                af''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                g''16
                            }
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                a'16
                                r8
                                ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Beams everything with stemlets:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.beam_everything(stemlets=2),
            ...     baca.rests_around([2], [2]),
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
                            \scaleDurations #'(1 . 1) {
                                \override Staff.Stem.stemlet-length = 2
                                r8
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                c'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                bf'16
                            }
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                fs''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                e''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                ef''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                af''16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                g''16
                            }
                            \scaleDurations #'(1 . 1) {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                a'16
                                \revert Staff.Stem.stemlet-length
                                r8
                                ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Beams everything without nibs:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.beam_everything(hide_nibs=True),
            ...     baca.rests_around([2], [2]),
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
                            \scaleDurations #'(1 . 1) {
                                r8
                                [
                                c'16
                                d'16
                                bf'16
                            }
                            \scaleDurations #'(1 . 1) {
                                fs''16
                                e''16
                                ef''16
                                af''16
                                g''16
                            }
                            \scaleDurations #'(1 . 1) {
                                a'16
                                r8
                                ]
                            }
                        }
                    }
                >>

        '''
        return rhythmos.BeamSpecifier(
            beam_divisions_together=True,
            beam_each_division=True,
            beam_rests=True,
            hide_nibs=hide_nibs,
            stemlet_length=stemlets,
            )

    @staticmethod
    def beam_positions(
        n: Number,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r'''Overrides beam positions.

        ..  container:: example

            Overrides beam positions on all leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.beam_positions(6),
            ...     baca.rests_around([2], [4]),
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
                            \times 4/5 {
                                \override Beam.positions = #'(6 . 6)                                     %! OC1
                                r8
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \times 4/5 {
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert Beam.positions                                                   %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides beam positions on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.beam_positions(6, baca.tuplet(1)),
            ...     baca.rests_around([2], [4]),
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
                            \times 4/5 {
                                r8
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \times 4/5 {
                                \override Beam.positions = #'(6 . 6)                                     %! OC1
                                fs''16
                                [
                                e''16
                                ef''16
                                af''16
                                g''16
                                ]
                                \revert Beam.positions                                                   %! OC2
                            }
                            \times 4/5 {
                                a'16
                                r4
                            }
                        }
                    }
                >>

        '''
        return OverrideCommand(
            attribute='positions',
            value=(n, n),
            grob='beam',
            selector=selector,
            )

    @staticmethod
    def beam_runs(hide_nibs: bool = False) -> rhythmos.BeamSpecifier:
        r'''Beams PLT runs.

        ..  container:: example

            Beams PLT runs:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.beam_runs(),
            ...     baca.rests_around([2], [2]),
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
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                c'16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                d'16
                                ]
                                bf'4
                                ~
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                bf'16
                                [
                                ]
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                fs''16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                e''16
                                ]
                                ef''4
                                ~
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                ef''16
                                [
                                ]
                                r16
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 2
                                af''16
                                [
                                \set stemLeftBeamCount = 2
                                \set stemRightBeamCount = 1
                                g''16
                            }
                            \times 2/3 {
                                \set stemLeftBeamCount = 1
                                \set stemRightBeamCount = 2
                                a'16
                                ]
                                r8
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Beams PLT runs without nibs:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.beam_runs(hide_nibs=True),
            ...     baca.rests_around([2], [2]),
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
                            }
                            \times 2/3 {
                                a'16
                                ]
                                r8
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        '''
        return rhythmos.BeamSpecifier(
            beam_divisions_together=True,
            beam_each_division=True,
            beam_rests=False,
            hide_nibs=hide_nibs,
            )

    @staticmethod
    def breaks(*pages: typing.Any) -> BreakMeasureMap:
        r'''Makes breaks.

        ..  container:: example

            >>> breaks = baca.breaks(
            ...     baca.page(
            ...         [1, 20, [15, 20, 20]], 
            ...         [13, 140, [15, 20, 20]], 
            ...         ),
            ...     baca.page(
            ...         [23, 20, [15, 20, 20]],
            ...         ),
            ...     )

        '''
        from baca.tools.LibraryGM import LibraryGM
        from baca.tools.LibraryNS import LibraryNS
        commands: typing.List = []
        if not pages:
            return BreakMeasureMap(commands=commands)
        first_measure_number = pages[0].items[0][0]
        bol_measure_numbers = []
        for page in pages:
            for i, item in enumerate(page.items):
                measure_number = item[0]
                bol_measure_numbers.append(measure_number)
                skip_index = measure_number - first_measure_number
                y_offset = item[1]
                alignment_distances = item[2]
                selector = f'baca.skip({skip_index})'
                if i == 0:
                    break_ = abjad.LilyPondLiteral(r'\pageBreak')
                else:
                    break_ = abjad.LilyPondLiteral(r'\break')
                command = IndicatorCommand(
                    indicators=[break_],
                    selector=selector,
                    )
                commands.append(command)
                lbsd = LibraryGM.lbsd(y_offset, alignment_distances, selector)
                commands.append(lbsd)
        breaks = BreakMeasureMap(commands=commands)
        breaks._bol_measure_numbers.extend(bol_measure_numbers)
        return breaks

    @staticmethod
    def build(command: Command) -> Command:
        r'''Tags ``command`` with ``-SEGMENT``.
        '''
        from baca.tools.LibraryTZ import LibraryTZ
        return LibraryTZ.tag(
            '-SEGMENT',
            command,
            )

    @staticmethod
    def center_to_octave(
        n: int,
        selector: Selector = 'baca.plts()',
        ) -> RegisterToOctaveCommand:
        r"""Octave-transposes music.

        ..  container:: example

            Octave-transposes music such that the centroid of all PLTs appears
            in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.center_to_octave(3),
            ...     baca.color(baca.plts().group()),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
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
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <c, d, bf,>8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <c, d, bf,>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                f8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                f32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <ef e fs'>8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <ef e fs'>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <g, af>8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <g, af>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a,8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a,32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Octave-transposes music such that the centroid of each pitched
            logical tie appears in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.map(baca.center_to_octave(3), baca.plts()),
            ...     baca.color(baca.plts()),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
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
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <c d bf>8
                                ~
                                [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <c d bf>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                f8
                                ~
                                [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                f32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef e fs'>8
                                ~
                                [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef e fs'>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                <g, af>8
                                ~
                                [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                <g, af>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a8
                                ~
                                [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Octave-transposes music such that the centroid of each of the last
            two pitched logical ties appears in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.map(baca.center_to_octave(3), baca.plts()[-2:]),
            ...     baca.color(baca.plts()[-2:]),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
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
                            \scaleDurations #'(1 . 1) {
                                <c' d' bf'>8
                                ~
                                [
                                <c' d' bf'>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                f''8
                                ~
                                [
                                f''32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                <ef'' e'' fs'''>8
                                ~
                                [
                                <ef'' e'' fs'''>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <g, af>8
                                ~
                                [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <g, af>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                a8
                                ~
                                [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                a32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        """
        return RegisterToOctaveCommand(
            anchor=abjad.Center,
            octave_number=n,
            selector=selector,
            )

    @staticmethod
    def clef(
        clef: str = 'treble',
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        r'''Attaches clef to leaf 0.

        ..  container:: example

            Attaches clef to leaf 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.clef('alto'),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(7),
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
                                \override TupletBracket.staff-padding = #7                               %! OC1
                                \clef "alto"                                                             %! IC
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
                >>

        ..  container:: example

            Attaches clef to leaf 0 in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.clef(
            ...         clef='alto',
            ...         selector=baca.tuplets()[1:2].leaf(0),
            ...         ),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(7),
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
                                \override TupletBracket.staff-padding = #7                               %! OC1
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
                                \clef "alto"                                                             %! IC
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

        '''
        indicator = abjad.Clef(clef)
        return IndicatorCommand(
            indicators=[indicator],
            selector=selector,
            )

    @staticmethod
    def clef_extra_offset(
        pair: NumberPair,
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        r'''Overrides clef extra offset.
        '''
        return OverrideCommand(
            attribute='extra_offset',
            context='Staff',
            grob='clef',
            selector=selector,
            value=pair,
            )

    @staticmethod
    def clef_x_extent_false(
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        r'''Overrides clef x-extent.
        '''
        return OverrideCommand(
            attribute='X_extent',
            context='Staff',
            grob='clef',
            selector=selector,
            value=False,
            )

    @staticmethod
    def clusters(
        widths: typing.List[int],
        selector: Selector = 'baca.plts()',
        start_pitch: typing.Union[int, str, abjad.NamedPitch] = None,
        ) -> ClusterCommand:
        r'''Makes clusters.
        '''
        return ClusterCommand(
            selector=selector,
            start_pitch=start_pitch,
            widths=widths,
            )

    @staticmethod
    def coat(pitch: typing.Union[int, str, abjad.Pitch]) -> Coat:
        r'''Coats `pitch`.

        ..  container:: example

            Coats pitches:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     3 * [[0, 2, 10]],
            ...     baca.imbricate(
            ...         'Voice 2',
            ...         [baca.coat(0), baca.coat(2), 10, 0, 2],
            ...         ),
            ...     baca.rests_around([2], [4]),
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
                            \times 4/5 {
                                r8
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \times 2/3 {
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/7 {
                                c'16
                                [
                                d'16
                                bf'16
                                ]
                                r4
                            }
                        }
                    }
                    \context Voice = "Voice 2"
                    {
                        \voiceTwo
                        {
                            \override TupletBracket.stencil = ##f
                            \override TupletNumber.stencil = ##f
                            \times 4/5 {
                                s8
                                s16
                                s16
                                bf'16
                            }
                            \times 2/3 {
                                c'16
                                [
                                d'16
                                ]
                                s16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 6/7 {
                                s16
                                s16
                                s16
                                s4
                            }
                            \revert TupletBracket.stencil
                            \revert TupletNumber.stencil
                        }
                    }
                >>

        '''
        return Coat(pitch)

    @staticmethod
    def color(selector: Selector = 'baca.leaves()') -> ColorCommand:
        r'''Colors leaves.

        ..  container:: example

            Colors all leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.color(),
            ...     baca.flags(),
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
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                r8
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                d'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                bf'4
                                ~
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                bf'16
                                \once \override Dots.color = #blue
                                \once \override Rest.color = #blue
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                fs''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                ef''4
                                ~
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                ef''16
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                r16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                af''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                g''16
                            }
                            \times 4/5 {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                a'16
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Colors leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.color(selector=baca.tuplets()[1:2].leaves()),
            ...     baca.flags(),
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
                                d'16
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                fs''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                ef''4
                                ~
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                ef''16
                                \once \override Dots.color = #red
                                \once \override Rest.color = #red
                                r16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                af''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                g''16
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
        return ColorCommand(selector=selector)

    @staticmethod
    def color_fingerings(
        numbers: typing.List[Number],
        selector: Selector = 'baca.pheads()',
        ) -> ColorFingeringCommand:
        r'''Color fingerings.
        '''
        return ColorFingeringCommand(numbers=numbers, selector=selector)

    @staticmethod
    def compound_quarter_divisions() -> DivisionSequenceExpression:
        r'''Makes compound quarter divisions.
        '''
        expression = DivisionSequenceExpression()
        expression = expression.split_by_durations(
            compound_meter_multiplier=abjad.Multiplier((3, 2)),
            durations=[abjad.Duration(1, 4)],
            )
        expression = expression.flatten(depth=-1)
        return expression

    @staticmethod
    def container(
        identifier: str = None,
        selector: Selector = 'baca.leaves()',
        ) -> ContainerCommand:
        r'''Inserts `selector` output in container.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.container('ViolinI', baca.leaves()[:2]),
            ...     baca.container('ViolinII', baca.leaves()[2:]),
            ...     baca.make_notes(repeat_ties=True),
            ...     baca.pitches('E4 F4'),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')

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
                            {   %*% ViolinI
            <BLANKLINE>
                                % [MusicVoice measure 1]                                             %! SM4
                                e'2
            <BLANKLINE>
                                % [MusicVoice measure 2]                                             %! SM4
                                f'4.
                            }   %*% ViolinI
                            {   %*% ViolinII
            <BLANKLINE>
                                % [MusicVoice measure 3]                                             %! SM4
                                e'2
            <BLANKLINE>
                                % [MusicVoice measure 4]                                             %! SM4
                                f'4.
            <BLANKLINE>
                            }   %*% ViolinII
                        }
                    }
                >>
            >>

        '''
        if identifier is not None:
            if not isinstance(identifier, str):
                message = f'identifier must be string (not {identifier!r}).'
                raise Exception(message)
        return ContainerCommand(
            identifier=identifier,
            selector=selector,
            )

    @staticmethod
    def cross_note_heads(
        selector: Selector = 'baca.tleaves()',
        ) -> OverrideCommand:
        r'''Overrides note-head style on pitched leaves.

        ..  container:: example

            Overrides note-head style on all pitched leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.cross_note_heads(),
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
                                \override NoteHead.style = #'cross                                       %! OC1
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
                                \revert NoteHead.style                                                   %! OC2
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides note-head style on pitched leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.cross_note_heads(baca.tuplet(1)),
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
                                \override NoteHead.style = #'cross                                       %! OC1
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
                                \revert NoteHead.style                                                   %! OC2
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
        return OverrideCommand(
            attribute='style',
            value='cross',
            grob='note_head',
            selector=selector,
            )

    @staticmethod
    def cross_staff(
        selector: Selector = 'baca.pheads()',
        ) -> IndicatorCommand:
        r'''Attaches cross-staff command to leaves.

        ..  container:: example

            Attaches cross-staff command to all leaves:

            >>> score_template = baca.StringTrioScoreTemplate()
            >>> accumulator = baca.MusicAccumulator(score_template)
            >>> accumulator(
            ...     accumulator.music_maker(
            ...         'ViolinMusicVoice',
            ...         [[9, 11, 12, 14, 16]],
            ...         baca.flags(),
            ...         baca.stems_up(),
            ...         denominator=8,
            ...         figure_name='vn.1',
            ...         talea_denominator=8,
            ...         ),
            ...     )
            >>> accumulator(
            ...     accumulator.music_maker(
            ...         'ViolaMusicVoice',
            ...         [[0, 2, 4, 5, 7]],
            ...         baca.anchor('ViolinMusicVoice'),
            ...         baca.cross_staff(),
            ...         baca.flags(),
            ...         baca.stems_up(),
            ...         figure_name='va.1',
            ...         talea_denominator=8,
            ...         ),
            ...     )
            >>> accumulator(
            ...     accumulator.music_maker(
            ...         'ViolinMusicVoice',
            ...         [[15]],
            ...         baca.flags(),
            ...         figure_name='vn.2',
            ...         talea_denominator=8,
            ...         ),
            ...     )

            >>> maker = baca.SegmentMaker(
            ...     ignore_repeat_pitch_classes=True,
            ...     ignore_unregistered_pitches=True,
            ...     score_template=accumulator.score_template,
            ...     spacing=baca.minimum_width((1, 12)),
            ...     time_signatures=accumulator.time_signatures,
            ...     )
            >>> accumulator.populate_segment_maker(maker)
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
                            \time 5/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 5/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \time 2/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context StringSectionStaffGroup = "String Section Staff Group"
                        <<
                            \tag Violin                                                                  %! ST4
                            \context ViolinMusicStaff = "ViolinMusicStaff"
                            {
                                \context ViolinMusicVoice = "ViolinMusicVoice"
                                {
                                    {
                                        \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                            % [ViolinMusicVoice measure 1]                               %! SM4
                                            \override Stem.direction = #up                               %! OC1
                                            \set ViolinMusicStaff.instrumentName = \markup {             %! SM8:DEFAULT_INSTRUMENT:ST1
                                                \hcenter-in                                              %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    #10                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    Violin                                               %! SM8:DEFAULT_INSTRUMENT:ST1
                                                }                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                            \set ViolinMusicStaff.shortInstrumentName = \markup {        %! SM8:DEFAULT_INSTRUMENT:ST1
                                                \hcenter-in                                              %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    #10                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    Vn.                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                                }                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                            \clef "treble"                                               %! SM8:DEFAULT_CLEF:ST3
                                            \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                            \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                                        %@% \override ViolinMusicStaff.Clef.color = ##f                  %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                            \set ViolinMusicStaff.forceClef = ##t                        %! SM8:DEFAULT_CLEF:SM33:ST3
                                            a'8
                                            ^ \markup {                                                  %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                \with-color                                              %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                    #(x11-color 'DarkViolet)                             %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                    (Violin)                                             %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                }                                                        %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                            \set ViolinMusicStaff.instrumentName = \markup {             %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                \hcenter-in                                              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    #10                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    Violin                                               %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                }                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            \set ViolinMusicStaff.shortInstrumentName = \markup {        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                \hcenter-in                                              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    #10                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    Vn.                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                }                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            \override ViolinMusicStaff.Clef.color = #(x11-color 'violet) %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
                <BLANKLINE>
                                            b'8
                <BLANKLINE>
                                            c''8
                <BLANKLINE>
                                            d''8
                <BLANKLINE>
                                            e''8
                                            \revert Stem.direction                                       %! OC2
                                        }
                                    }
                                    {
                                        \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                            % [ViolinMusicVoice measure 2]                               %! SM4
                                            ef''8
                <BLANKLINE>
                                        }
                                    }
                                }
                            }
                            \tag Viola                                                                   %! ST4
                            \context ViolaMusicStaff = "ViolaMusicStaff"
                            {
                                \context ViolaMusicVoice = "ViolaMusicVoice"
                                {
                                    {
                                        \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                            % [ViolaMusicVoice measure 1]                                %! SM4
                                            \override Stem.direction = #up                               %! OC1
                                            \set ViolaMusicStaff.instrumentName = \markup {              %! SM8:DEFAULT_INSTRUMENT:ST1
                                                \hcenter-in                                              %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    #10                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    Viola                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                                }                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                            \set ViolaMusicStaff.shortInstrumentName = \markup {         %! SM8:DEFAULT_INSTRUMENT:ST1
                                                \hcenter-in                                              %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    #10                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    Va.                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                                }                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                            \clef "alto"                                                 %! SM8:DEFAULT_CLEF:ST3
                                            \crossStaff                                                  %! IC
                                            \once \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                            \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                                        %@% \override ViolaMusicStaff.Clef.color = ##f                   %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                            \set ViolaMusicStaff.forceClef = ##t                         %! SM8:DEFAULT_CLEF:SM33:ST3
                                            c'8
                                            ^ \markup {                                                  %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                \with-color                                              %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                    #(x11-color 'DarkViolet)                             %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                    (Viola)                                              %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                }                                                        %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                            \set ViolaMusicStaff.instrumentName = \markup {              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                \hcenter-in                                              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    #10                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    Viola                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                }                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            \set ViolaMusicStaff.shortInstrumentName = \markup {         %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                \hcenter-in                                              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    #10                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    Va.                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                }                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)  %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
                <BLANKLINE>
                                            \crossStaff                                                  %! IC
                                            d'8
                <BLANKLINE>
                                            \crossStaff                                                  %! IC
                                            e'8
                <BLANKLINE>
                                            \crossStaff                                                  %! IC
                                            f'8
                <BLANKLINE>
                                            \crossStaff                                                  %! IC
                                            g'8
                                            \revert Stem.direction                                       %! OC2
                                        }
                                    }
                <BLANKLINE>
                                    % [ViolaMusicVoice measure 2]                                        %! SM4
                                    R1 * 1/8
                <BLANKLINE>
                                }
                            }
                            \tag Cello                                                                   %! ST4
                            \context CelloMusicStaff = "CelloMusicStaff"
                            {
                                \context CelloMusicVoice = "CelloMusicVoice"
                                {
                <BLANKLINE>
                                    % [CelloMusicVoice measure 1]                                        %! SM4
                                    \set CelloMusicStaff.instrumentName = \markup {                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                        \hcenter-in                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                            #10                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                            Cello                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                        }                                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \set CelloMusicStaff.shortInstrumentName = \markup {                 %! SM8:DEFAULT_INSTRUMENT:ST1
                                        \hcenter-in                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                            #10                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                            Vc.                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                        }                                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \clef "bass"                                                         %! SM8:DEFAULT_CLEF:ST3
                                    \once \override CelloMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                    \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                                %@% \override CelloMusicStaff.Clef.color = ##f                           %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                    \set CelloMusicStaff.forceClef = ##t                                 %! SM8:DEFAULT_CLEF:SM33:ST3
                                    R1 * 5/8
                                    ^ \markup {                                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        \with-color                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            #(x11-color 'DarkViolet)                                     %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            (Cello)                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        }                                                                %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \override CelloMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                    \set CelloMusicStaff.instrumentName = \markup {                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        \hcenter-in                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            #10                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            Cello                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        }                                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \set CelloMusicStaff.shortInstrumentName = \markup {                 %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        \hcenter-in                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            #10                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            Vc.                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        }                                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \override CelloMusicStaff.Clef.color = #(x11-color 'violet)          %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
                <BLANKLINE>
                                    % [CelloMusicVoice measure 2]                                        %! SM4
                                    R1 * 1/8
                <BLANKLINE>
                                }
                            }
                        >>
                    >>
                >>

        ..  container:: example

            Attaches cross-staff command to last two pitched leaves:

            >>> score_template = baca.StringTrioScoreTemplate()
            >>> accumulator = baca.MusicAccumulator(score_template)
            >>> accumulator(
            ...     accumulator.music_maker(
            ...         'ViolinMusicVoice',
            ...         [[9, 11, 12, 14, 16]],
            ...         baca.flags(),
            ...         baca.stems_up(),
            ...         denominator=8,
            ...         figure_name='vn.1',
            ...         talea_denominator=8,
            ...         ),
            ...     )
            >>> accumulator(
            ...     accumulator.music_maker(
            ...         'ViolaMusicVoice',
            ...         [[0, 2, 4, 5, 7]],
            ...         baca.anchor('ViolinMusicVoice'),
            ...         baca.cross_staff(selector=baca.pleaves()[-2:]),
            ...         baca.flags(),
            ...         baca.stems_up(),
            ...         figure_name='va.1',
            ...         talea_denominator=8,
            ...         ),
            ...     )
            >>> accumulator(
            ...     accumulator.music_maker(
            ...         'ViolinMusicVoice',
            ...         [[15]],
            ...         baca.flags(),
            ...         figure_name='vn.2',
            ...         talea_denominator=8,
            ...         ),
            ...     )

            >>> maker = baca.SegmentMaker(
            ...     ignore_repeat_pitch_classes=True,
            ...     ignore_unregistered_pitches=True,
            ...     score_template=accumulator.score_template,
            ...     spacing=baca.minimum_width((1, 12)),
            ...     time_signatures=accumulator.time_signatures,
            ...     )
            >>> accumulator.populate_segment_maker(maker)
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
                            \time 5/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 5/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \time 2/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 1/8
                            \override Score.BarLine.transparent = ##f                                    %! SM5
                            \bar "|"                                                                     %! SM5
                <BLANKLINE>
                        }
                    >>
                    \context MusicContext = "MusicContext"
                    <<
                        \context StringSectionStaffGroup = "String Section Staff Group"
                        <<
                            \tag Violin                                                                  %! ST4
                            \context ViolinMusicStaff = "ViolinMusicStaff"
                            {
                                \context ViolinMusicVoice = "ViolinMusicVoice"
                                {
                                    {
                                        \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                            % [ViolinMusicVoice measure 1]                               %! SM4
                                            \override Stem.direction = #up                               %! OC1
                                            \set ViolinMusicStaff.instrumentName = \markup {             %! SM8:DEFAULT_INSTRUMENT:ST1
                                                \hcenter-in                                              %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    #10                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    Violin                                               %! SM8:DEFAULT_INSTRUMENT:ST1
                                                }                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                            \set ViolinMusicStaff.shortInstrumentName = \markup {        %! SM8:DEFAULT_INSTRUMENT:ST1
                                                \hcenter-in                                              %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    #10                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    Vn.                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                                }                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                            \clef "treble"                                               %! SM8:DEFAULT_CLEF:ST3
                                            \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                            \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                                        %@% \override ViolinMusicStaff.Clef.color = ##f                  %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                            \set ViolinMusicStaff.forceClef = ##t                        %! SM8:DEFAULT_CLEF:SM33:ST3
                                            a'8
                                            ^ \markup {                                                  %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                \with-color                                              %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                    #(x11-color 'DarkViolet)                             %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                    (Violin)                                             %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                }                                                        %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                            \set ViolinMusicStaff.instrumentName = \markup {             %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                \hcenter-in                                              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    #10                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    Violin                                               %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                }                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            \set ViolinMusicStaff.shortInstrumentName = \markup {        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                \hcenter-in                                              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    #10                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    Vn.                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                }                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            \override ViolinMusicStaff.Clef.color = #(x11-color 'violet) %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
                <BLANKLINE>
                                            b'8
                <BLANKLINE>
                                            c''8
                <BLANKLINE>
                                            d''8
                <BLANKLINE>
                                            e''8
                                            \revert Stem.direction                                       %! OC2
                                        }
                                    }
                                    {
                                        \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                            % [ViolinMusicVoice measure 2]                               %! SM4
                                            ef''8
                <BLANKLINE>
                                        }
                                    }
                                }
                            }
                            \tag Viola                                                                   %! ST4
                            \context ViolaMusicStaff = "ViolaMusicStaff"
                            {
                                \context ViolaMusicVoice = "ViolaMusicVoice"
                                {
                                    {
                                        \scaleDurations #'(1 . 1) {
                <BLANKLINE>
                                            % [ViolaMusicVoice measure 1]                                %! SM4
                                            \override Stem.direction = #up                               %! OC1
                                            \set ViolaMusicStaff.instrumentName = \markup {              %! SM8:DEFAULT_INSTRUMENT:ST1
                                                \hcenter-in                                              %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    #10                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    Viola                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                                }                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                            \set ViolaMusicStaff.shortInstrumentName = \markup {         %! SM8:DEFAULT_INSTRUMENT:ST1
                                                \hcenter-in                                              %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    #10                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                                    Va.                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                                }                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                            \clef "alto"                                                 %! SM8:DEFAULT_CLEF:ST3
                                            \once \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                            \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                                        %@% \override ViolaMusicStaff.Clef.color = ##f                   %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                            \set ViolaMusicStaff.forceClef = ##t                         %! SM8:DEFAULT_CLEF:SM33:ST3
                                            c'8
                                            ^ \markup {                                                  %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                \with-color                                              %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                    #(x11-color 'DarkViolet)                             %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                    (Viola)                                              %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                                }                                                        %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                            \set ViolaMusicStaff.instrumentName = \markup {              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                \hcenter-in                                              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    #10                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    Viola                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                }                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            \set ViolaMusicStaff.shortInstrumentName = \markup {         %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                \hcenter-in                                              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    #10                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                    Va.                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                                }                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)  %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
                <BLANKLINE>
                                            d'8
                <BLANKLINE>
                                            e'8
                <BLANKLINE>
                                            \crossStaff                                                  %! IC
                                            f'8
                <BLANKLINE>
                                            \crossStaff                                                  %! IC
                                            g'8
                                            \revert Stem.direction                                       %! OC2
                                        }
                                    }
                <BLANKLINE>
                                    % [ViolaMusicVoice measure 2]                                        %! SM4
                                    R1 * 1/8
                <BLANKLINE>
                                }
                            }
                            \tag Cello                                                                   %! ST4
                            \context CelloMusicStaff = "CelloMusicStaff"
                            {
                                \context CelloMusicVoice = "CelloMusicVoice"
                                {
                <BLANKLINE>
                                    % [CelloMusicVoice measure 1]                                        %! SM4
                                    \set CelloMusicStaff.instrumentName = \markup {                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                        \hcenter-in                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                            #10                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                            Cello                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                        }                                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \set CelloMusicStaff.shortInstrumentName = \markup {                 %! SM8:DEFAULT_INSTRUMENT:ST1
                                        \hcenter-in                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                            #10                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                            Vc.                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                        }                                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \clef "bass"                                                         %! SM8:DEFAULT_CLEF:ST3
                                    \once \override CelloMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                    \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                                %@% \override CelloMusicStaff.Clef.color = ##f                           %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                    \set CelloMusicStaff.forceClef = ##t                                 %! SM8:DEFAULT_CLEF:SM33:ST3
                                    R1 * 5/8
                                    ^ \markup {                                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        \with-color                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            #(x11-color 'DarkViolet)                                     %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            (Cello)                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        }                                                                %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \override CelloMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                    \set CelloMusicStaff.instrumentName = \markup {                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        \hcenter-in                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            #10                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            Cello                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        }                                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \set CelloMusicStaff.shortInstrumentName = \markup {                 %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        \hcenter-in                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            #10                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            Vc.                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        }                                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \override CelloMusicStaff.Clef.color = #(x11-color 'violet)          %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
                <BLANKLINE>
                                    % [CelloMusicVoice measure 2]                                        %! SM4
                                    R1 * 1/8
                <BLANKLINE>
                                }
                            }
                        >>
                    >>
                >>

        '''
        return IndicatorCommand(
            indicators=[abjad.LilyPondLiteral(r'\crossStaff')],
            selector=selector,
            )

    @staticmethod
    def dashed_arrow() -> abjad.ArrowLineSegment:
        r'''Makes dashed arrow line segment.
        '''
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

    @staticmethod
    def deviation(
        deviations: typing.List[Number],
        selector: Selector = 'baca.plts()',
        ) -> MicrotoneDeviationCommand:
        r''''Makes microtone deviation.
        '''
        return MicrotoneDeviationCommand(
            deviations=deviations,
            selector=selector,
            )

    @staticmethod
    def diatonic_clusters(
        widths: typing.List[int],
        selector: Selector = 'baca.plts()',
        ) -> DiatonicClusterCommand:
        r'''Makes diatonic clusters.
        '''
        return DiatonicClusterCommand(
            selector=selector,
            widths=widths,
            )

    @staticmethod
    def displacement(
        displacements: typing.List[int],
        selector: Selector = 'baca.plts()',
        ) -> OctaveDisplacementCommand:
        r'''Octave-displaces PLTs.

        ..  container:: example

            Octave-displaces PLTs:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     3 * [[0, 2, 3]],
            ...     baca.displacement([0, 0, -1, -1, 1, 1]),
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
                                ef4
                                ~
                                ef16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                c16
                                [
                                d''16
                                ]
                                ef''4
                                ~
                                ef''16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 11/12 {
                                c'16
                                [
                                d'16
                                ]
                                ef4
                                ~
                                ef16
                                r16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Octave-displaces chords:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     6 * [{0, 2, 3}],
            ...     baca.displacement([0, 0, -1, -1, 1, 1]),
            ...     baca.rests_around([2], [4]),
            ...     counts=[4],
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
                            \scaleDurations #'(1 . 1) {
                                r8
                                <c' d' ef'>4
                            }
                            \scaleDurations #'(1 . 1) {
                                <c' d' ef'>4
                            }
                            \scaleDurations #'(1 . 1) {
                                <c d ef>4
                            }
                            \scaleDurations #'(1 . 1) {
                                <c d ef>4
                            }
                            \scaleDurations #'(1 . 1) {
                                <c'' d'' ef''>4
                            }
                            \scaleDurations #'(1 . 1) {
                                <c'' d'' ef''>4
                                r4
                            }
                        }
                    }
                >>

        ..  container:: example

            Octave-displaces last six pitched logical ties:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     3 * [[0, 2, 3]],
            ...     baca.displacement([0, 0, -1, -1, 1, 1], baca.plts()[-6:]),
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
                                ef'4
                                ~
                                ef'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                c'16
                                [
                                d'16
                                ]
                                ef4
                                ~
                                ef16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 11/12 {
                                c16
                                [
                                d''16
                                ]
                                ef''4
                                ~
                                ef''16
                                r16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        '''
        return OctaveDisplacementCommand(
            displacements=displacements,
            selector=selector,
            )

    @staticmethod
    def dls_sp(
        n: Number,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r'''Overrides dynamic line spanner staff padding.
        '''
        from baca.tools.LibraryAF import LibraryAF
        return LibraryAF.dynamic_line_spanner_staff_padding(
            n,
            selector=selector,
            )

    @staticmethod
    def double_tonguing(
        selector: Selector = 'baca.pheads()',
        ) -> IndicatorCommand:
        r'''Attaches double-staccati to pitched heads.

        ..  container:: example

            Attaches double-staccati to all pitched heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.double_tonguing(),
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
                                -\tongue #2                                                              %! IC
                                [
                                d'16
                                -\tongue #2                                                              %! IC
                                ]
                                bf'4
                                -\tongue #2                                                              %! IC
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                -\tongue #2                                                              %! IC
                                [
                                e''16
                                -\tongue #2                                                              %! IC
                                ]
                                ef''4
                                -\tongue #2                                                              %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\tongue #2                                                              %! IC
                                [
                                g''16
                                -\tongue #2                                                              %! IC
                                ]
                            }
                            \times 4/5 {
                                a'16
                                -\tongue #2                                                              %! IC
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches double-staccati to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.double_tonguing(
            ...         baca.tuplets()[1:2].pheads(),
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
                                -\tongue #2                                                              %! IC
                                [
                                e''16
                                -\tongue #2                                                              %! IC
                                ]
                                ef''4
                                -\tongue #2                                                              %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\tongue #2                                                              %! IC
                                [
                                g''16
                                -\tongue #2                                                              %! IC
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
            indicators=[abjad.Articulation('tongue #2')],
            selector=selector,
            )

    @staticmethod
    def down_arpeggios(
        selector: Selector = 'baca.cheads()',
        ) -> IndicatorCommand:
        r"""Attaches down-arpeggios to chord heads.

        ..  container:: example

            Attaches down-arpeggios to all chord heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.down_arpeggios(),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
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
                            \scaleDurations #'(1 . 1) {
                                \arpeggioArrowDown                                                       %! IC
                                <c' d' bf'>8
                                \arpeggio                                                                %! IC
                                ~
                                [
                                <c' d' bf'>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                f''8
                                ~
                                [
                                f''32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \arpeggioArrowDown                                                       %! IC
                                <ef'' e'' fs'''>8
                                \arpeggio                                                                %! IC
                                ~
                                [
                                <ef'' e'' fs'''>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \arpeggioArrowDown                                                       %! IC
                                <g' af''>8
                                \arpeggio                                                                %! IC
                                ~
                                [
                                <g' af''>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                a'8
                                ~
                                [
                                a'32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches down-arpeggios to last two chord heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.down_arpeggios(baca.cheads()[-2:]),
            ...     counts=[5, -3],
            ...     talea_denominator=32,
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
                            \scaleDurations #'(1 . 1) {
                                <c' d' bf'>8
                                ~
                                [
                                <c' d' bf'>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                f''8
                                ~
                                [
                                f''32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \arpeggioArrowDown                                                       %! IC
                                <ef'' e'' fs'''>8
                                \arpeggio                                                                %! IC
                                ~
                                [
                                <ef'' e'' fs'''>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \arpeggioArrowDown                                                       %! IC
                                <g' af''>8
                                \arpeggio                                                                %! IC
                                ~
                                [
                                <g' af''>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                a'8
                                ~
                                [
                                a'32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        """
        return IndicatorCommand(
            indicators=[abjad.Arpeggio(direction=abjad.Down)],
            selector=selector,
            )

    @staticmethod
    def down_bows(
        selector: Selector = 'baca.pheads()',
        ) -> IndicatorCommand:
        r'''Attaches down-bows to pitched heads.

        ..  container:: example

            Attaches down-bows to all pitched heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.down_bows(),
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
                                -\downbow                                                                %! IC
                                [
                                d'16
                                -\downbow                                                                %! IC
                                ]
                                bf'4
                                -\downbow                                                                %! IC
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                -\downbow                                                                %! IC
                                [
                                e''16
                                -\downbow                                                                %! IC
                                ]
                                ef''4
                                -\downbow                                                                %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\downbow                                                                %! IC
                                [
                                g''16
                                -\downbow                                                                %! IC
                                ]
                            }
                            \times 4/5 {
                                a'16
                                -\downbow                                                                %! IC
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches down-bows to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.down_bows(
            ...         baca.tuplets()[1:2].pheads(),
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
                                -\downbow                                                                %! IC
                                [
                                e''16
                                -\downbow                                                                %! IC
                                ]
                                ef''4
                                -\downbow                                                                %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\downbow                                                                %! IC
                                [
                                g''16
                                -\downbow                                                                %! IC
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
            indicators=[abjad.Articulation('downbow')],
            selector=selector,
            )

    @staticmethod
    def dynamic(
        dynamic: str,
        selector: Selector = 'baca.phead(0)',
        ) -> IndicatorCommand:
        r'''Attaches dynamic to pitched head 0.

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
            ...     baca.dynamic('f', baca.tuplets()[1:2].phead(0)),
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

        '''
        if dynamic in baca.tools.scheme.dynamics:
            steady_state = baca.tools.scheme.dynamic_to_steady_state(dynamic)
            command = '\\' + dynamic
            first = dynamic.split('_')[0]
            if first in ('sfz', 'sffz', 'sfffz'):
                sforzando = True
            else:
                sforzando = False
            indicator = abjad.Dynamic(
                steady_state,
                command=command,
                sforzando=sforzando,
                )
        else:
            indicator = abjad.Dynamic(dynamic)
        return IndicatorCommand(
            context='Voice',
            indicators=[indicator],
            selector=selector,
            )

    @staticmethod
    def dynamic_line_spanner_padding(
        n: Number,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r'''Overrides dynamic line spanner padding on leaves.
        '''
        return OverrideCommand(
            attribute='padding',
            value=str(n),
            grob='dynamic_line_spanner',
            selector=selector,
            )

    @staticmethod
    def dynamic_line_spanner_staff_padding(
        n: Number,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r'''Overrides dynamic line spanner staff padding on leaves.

        ..  container:: example

            Overrides dynamic line spanner staff padding on all leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic_line_spanner_staff_padding(4),
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
                                \override DynamicLineSpanner.staff-padding = #'4                         %! OC1
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
                                \revert DynamicLineSpanner.staff-padding                                 %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides dynamic line spanner staff padding on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic_line_spanner_staff_padding(4, baca.tuplet(1)),
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
                                \override DynamicLineSpanner.staff-padding = #'4                         %! OC1
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
                                \revert DynamicLineSpanner.staff-padding                                 %! OC2
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
        return OverrideCommand(
            attribute='staff_padding',
            value=str(n),
            grob='dynamic_line_spanner',
            selector=selector,
            )

    @staticmethod
    def dynamic_line_spanner_up(
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r'''Up-overrides dynamic line spanner direction.

        ..  container:: example

            Up-overrides dynamic line spanner direction on all leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic_line_spanner_up(),
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
                                \override DynamicLineSpanner.direction = #up                             %! OC1
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
                                \revert DynamicLineSpanner.direction                                     %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Up-overrides dynamic line spanner direction on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic_line_spanner_up(baca.tuplet(1)),
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
                                \override DynamicLineSpanner.direction = #up                             %! OC1
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
                                \revert DynamicLineSpanner.direction                                     %! OC2
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
        return OverrideCommand(
            attribute='direction',
            value=abjad.Up,
            grob='dynamic_line_spanner',
            selector=selector,
            )

    @staticmethod
    def dynamic_text_extra_offset(
        pair: NumberPair,
        selector: Selector = 'baca.pleaf(0)',
        ) -> OverrideCommand:
        r'''Overrides dynamic text extra offset.

        ..  container:: example

            Overrides dynamic text extra offset on pitched leaf 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic('p'),
            ...     baca.dynamic('f', baca.tuplets()[1:2].pleaf(0)),
            ...     baca.dynamic_text_extra_offset((-3, 0)),
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
                                \once \override DynamicText.extra-offset = #'(-3 . 0)                    %! OC1
                                c'16
                                \p                                                                       %! IC
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

            Overrides dynamic text extra offset on leaf 0 in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic('p'),
            ...     baca.dynamic('f', baca.tuplets()[1:2].leaf(0)),
            ...     baca.dynamic_text_extra_offset(
            ...         (-3, 0),
            ...         baca.tuplets()[1:2].leaf(0),
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
                                \p                                                                       %! IC
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
                                \once \override DynamicText.extra-offset = #'(-3 . 0)                    %! OC1
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

        '''
        return OverrideCommand(
            attribute='extra_offset',
            value=pair,
            grob='dynamic_text',
            selector=selector,
            )

    @staticmethod
    def dynamic_text_x_extent_zero(
        selector: Selector = 'baca.pleaf(0)',
        ) -> OverrideCommand:
        r'''Overrides dynamic text X-extent.
        '''
        return OverrideCommand(
            attribute='X_extent',
            value=(0, 0),
            grob='dynamic_text',
            selector=selector,
            )

    @staticmethod
    def dynamic_text_x_offset(
        n: Number,
        selector: Selector = 'baca.pleaf(0)',
        ) -> OverrideCommand:
        r'''Overrides dynamic text X-extent.
        '''
        return OverrideCommand(
            attribute='X_offset',
            value=n,
            grob='dynamic_text',
            selector=selector,
            )

    @staticmethod
    def dynamics(string: str) -> typing.List[abjad.Dynamic]:
        r'''Makes dynamics from `string`.

        ..  container::

            >>> baca.dynamics('ff p f pp')
            [Dynamic('ff'), Dynamic('p'), Dynamic('f'), Dynamic('pp')]

        '''
        return [abjad.Dynamic(_) for _ in string.split()]

    @staticmethod
    def dynamics_down(
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        r'''Attaches dynamic-down command to leaf 0.

        ..  container:: example

            Attaches dynamic-down command to leaf 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic('p'),
            ...     baca.dynamic('f', baca.tuplets()[1:2].phead(0)),
            ...     baca.dynamics_down(),
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
                                \dynamicDown                                                             %! IC
                                r8
                                c'16
                                \p                                                                       %! IC
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

            Attaches dynamic-down command to leaf 0 in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic('p'),
            ...     baca.dynamic('f', baca.tuplets()[1:2].phead(0)),
            ...     baca.dynamics_down(baca.tuplets()[1:2].leaf(0)),
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
                                \p                                                                       %! IC
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
                                \dynamicDown                                                             %! IC
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

        '''
        return IndicatorCommand(
            indicators=[abjad.LilyPondLiteral(r'\dynamicDown')],
            selector=selector,
            )

    @staticmethod
    def dynamics_up(
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        r'''Attaches dynamic-up command to leaf 0.

        ..  container:: example

            Attaches dynamic-up command to leaf 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic('p'),
            ...     baca.dynamic('f', baca.tuplets()[1:2].phead(0)),
            ...     baca.dynamics_up(),
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
                                \dynamicUp                                                               %! IC
                                r8
                                c'16
                                \p                                                                       %! IC
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

            Attaches dynamic-up command to leaf 0 in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dynamic('p'),
            ...     baca.dynamic('f', baca.tuplets()[1:2].phead(0)),
            ...     baca.dynamics_up(baca.tuplets()[1:2].leaf(0)),
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
                                \p                                                                       %! IC
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
                                \dynamicUp                                                               %! IC
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

        '''
        return IndicatorCommand(
            indicators=[abjad.LilyPondLiteral(r'\dynamicUp')],
            selector=selector,
            )

    @staticmethod
    def effort_dynamic(
        dynamic: str,
        selector: Selector = 'baca.phead(0)',
        ) -> IndicatorCommand:
        r'''Attaches effort dynamic to pitched head 0.

        ..  container:: example

            Attaches effort dynamic to pitched head 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.effort_dynamic('f'),
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
                                \effort_f                                                                %! IC
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

            Attaches effort dynamic to pitched head 0 in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.effort_dynamic(
            ...         'f',
            ...         baca.tuplets()[1:2].phead(0),
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
                                \effort_f                                                                %! IC
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
        command = rf'\effort_{dynamic}'
        indicator = abjad.Dynamic(f'{dynamic}', command=command)
        return IndicatorCommand(
            indicators=[indicator],
            selector=selector,
            )

    @staticmethod
    def fermata(
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        r'''Attaches fermata to leaf.

        ..  container:: example

            Attaches fermata to first leaf:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.fermata(),
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
                                -\fermata                                                                %! IC
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

            Attaches fermata to first leaf in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.fermata(baca.tuplets()[1:2].phead(0)),
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
                                -\fermata                                                                %! IC
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
            indicators=[abjad.Articulation('fermata')],
            selector=selector,
            )

    @staticmethod
    def flageolets(
        selector: Selector = 'baca.pheads()',
        ) -> IndicatorCommand:
        r'''Attaches flageolets to pitched heads.

        ..  container:: example

            Attaches flageolets to all pitched heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.flageolets(),
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
                                -\flageolet                                                              %! IC
                                [
                                d'16
                                -\flageolet                                                              %! IC
                                ]
                                bf'4
                                -\flageolet                                                              %! IC
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                -\flageolet                                                              %! IC
                                [
                                e''16
                                -\flageolet                                                              %! IC
                                ]
                                ef''4
                                -\flageolet                                                              %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\flageolet                                                              %! IC
                                [
                                g''16
                                -\flageolet                                                              %! IC
                                ]
                            }
                            \times 4/5 {
                                a'16
                                -\flageolet                                                              %! IC
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches flageolets to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.flageolets(baca.tuplets()[1:2].pheads()),
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
                                -\flageolet                                                              %! IC
                                [
                                e''16
                                -\flageolet                                                              %! IC
                                ]
                                ef''4
                                -\flageolet                                                              %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\flageolet                                                              %! IC
                                [
                                g''16
                                -\flageolet                                                              %! IC
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
            indicators=[abjad.Articulation('flageolet')],
            selector=selector,
            )

    @staticmethod
    def flags() -> rhythmos.BeamSpecifier:
        r'''Flags music.

        ..  container:: example

            Flags music:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.flags(),
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
                                d'16
                                bf'4
                                ~
                                bf'16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                e''16
                                ef''4
                                ~
                                ef''16
                                r16
                                af''16
                                g''16
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
        return rhythmos.BeamSpecifier(
            beam_divisions_together=False,
            beam_each_division=False,
            )

    @staticmethod
    def force_accidentals(
        selector: Selector = 'baca.pleaf(0)',
        ) -> AccidentalAdjustmentCommand:
        r'''Forces accidentals.

        ..  container:: example

            Inverts edition-specific tags:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     baca.scope('MusicVoice', 1),
            ...     baca.not_parts(baca.force_accidentals(baca.pleaves()[:2])),
            ...     baca.make_notes(repeat_ties=True),
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
                                e'2                                                                      %! AJC:+PARTS
                            %@% e'!2                                                                     %! AJC:-PARTS
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                f'4.                                                                     %! AJC:+PARTS
                            %@% f'!4.                                                                    %! AJC:-PARTS
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
        return AccidentalAdjustmentCommand(
            forced=True,
            selector=selector,
            )

    @staticmethod
    def fuse_compound_quarter_divisions(
        counts: typing.List[int],
        ) -> DivisionSequenceExpression:
        r'''Fuses compound quarter divisions.

        ..  container:: example

            >>> expression = baca.fuse_compound_quarter_divisions([1])

            >>> for item in expression([(2, 8), (2, 8), (2, 8)]):
            ...     item
            ...
            Division((1, 4))
            Division((1, 4))
            Division((1, 4))

            >>> for item in expression([(3, 8), (3, 8), (3, 8)]):
            ...     item
            ...
            Division((1, 4))
            Division((1, 8))
            Division((1, 4))
            Division((1, 8))
            Division((1, 4))
            Division((1, 8))

        ..  container:: example

            >>> expression = baca.fuse_compound_quarter_divisions([2])

            >>> for item in expression([(2, 8), (2, 8), (2, 8)]):
            ...     item
            ...
            Division((2, 4))
            Division((1, 4))

            >>> for item in expression([(3, 8), (3, 8), (3, 8)]):
            ...     item
            ...
            Division((3, 8))
            Division((3, 8))
            Division((3, 8))

        '''
        if not all(isinstance(_, int) for _ in counts):
            raise Exception(counts)
        expression = DivisionSequenceExpression()
        expression = expression.division_sequence()
        expression = expression.split_by_durations(
            compound_meter_multiplier=abjad.Multiplier((3, 2)),
            durations=[abjad.Duration(1, 4)],
            )
        expression = expression.flatten(depth=-1)
        expression = expression.partition_by_counts(
            counts=counts,
            cyclic=True,
            overhang=True,
            )
        expression = expression.map(baca.sequence().sum())
        expression = expression.flatten(depth=-1)
        return expression
