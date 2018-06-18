import abjad
import baca
import typing
from abjadext import rmakers
from . import library
from .AccidentalAdjustmentCommand import AccidentalAdjustmentCommand
from .AnchorSpecifier import AnchorSpecifier
from .BowContactPointCommand import BowContactPointCommand
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
from .MapCommand import MapCommand
from .MicrotoneDeviationCommand import MicrotoneDeviationCommand
from .OctaveDisplacementCommand import OctaveDisplacementCommand
from .OverrideCommand import OverrideCommand
from .PiecewiseCommand import PiecewiseCommand
from .RegisterToOctaveCommand import RegisterToOctaveCommand
from .SpannerCommand import SpannerCommand
from .SuiteCommand import SuiteCommand
from .Typing import Number
from .Typing import NumberPair
from .Typing import Selector


class LibraryAF(abjad.AbjadObject):
    """
    Library A - F.

    >>> from abjadext import rmakers

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(1) Library'

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    @staticmethod
    def accent(
        *,
        selector: Selector = 'baca.phead(0)',
        ) -> IndicatorCommand:
        r"""
        Attaches accent.

        ..  container:: example

            Attaches accent to pitched head 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.accent(),
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

            Attaches accent to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.tuplet(1),
            ...         baca.accent(selector=baca.pheads()),
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

        """
        return IndicatorCommand(
            indicators=[abjad.Articulation('>')],
            selector=selector,
            )

    @staticmethod
    def accidental_stencil_false(
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        """
        Overrides accidental stencil.
        """
        return OverrideCommand(
            attribute='stencil',
            grob='accidental',
            selector=selector,
            value=False,
            )

    @staticmethod
    def accidental_transparent(
        *,
        selector: Selector = 'baca.leaves()',
        ):
        """
        Overrides accidental transparency on.
        """
        return OverrideCommand(
            attribute='transparent',
            value=True,
            grob='accidental',
            selector=selector,
            )

    @staticmethod
    def accidental_x_extent_false(
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        """
        Overrides accidental x-extent.
        """
        return OverrideCommand(
            attribute='X_extent',
            grob='accidental',
            selector=selector,
            value=False,
            )

    @staticmethod
    def allow_octaves(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> IndicatorCommand:
        """
        Attaches ALLOW_OCTAVE tag.
        """
        return IndicatorCommand(
            indicators=[abjad.tags.ALLOW_OCTAVE],
            selector=selector,
            )

    @staticmethod
    def alternate_bow_strokes(
        *,
        downbow_first: bool = True,
        selector: Selector = 'baca.pheads()',
        ) -> IndicatorCommand:
        r"""
        Attaches alternate bow strokes.

        :param downbow_first: is true when first stroke is down-bow.

        ..  container:: example

            Attaches alternate bow strokes to pitched heads (down-bow first):

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

            Attaches alternate bow strokes to pitched heads (up-bow first):

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
            ...         baca.tuplet(1),
            ...         baca.alternate_bow_strokes(),
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

        """
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
        """
        Anchors music in this figure (filtered by ``local_selector``) to
        start offset of ``remote_voice_name`` (filtered by
        ``remote_selector``).

        :param remote_voice_name: name of voice to which this music anchors.

        :param remote_seelctor: selector applied to remote voice.

        :param local_selector: selector applied to this music.
        """
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
        """
        Anchors music in this figure (filtered by ``local_selector``) to
        stop offset of ``remote_voice_name`` (filtered by ``remote_selector``).

        :param remote_voice_name: name of voice to which this music anchors.

        :param remote_selector: selector applied to remote voice.

        :param local_selector: selector applied to this music.
        """
        return AnchorSpecifier(
            local_selector=local_selector,
            remote_selector=remote_selector,
            remote_voice_name=remote_voice_name,
            use_remote_stop_offset=True,
            )

    @staticmethod
    def anchor_to_figure(figure_name: str) -> AnchorSpecifier:
        """
        Anchors music in this figure to start of ``figure_name``.

        :param figure_name: figure name.
        """
        return AnchorSpecifier(
            figure_name=figure_name,
            )

    @staticmethod
    def ancora_dynamic(
        dynamic: str,
        *,
        selector: Selector = 'baca.phead(0)',
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

        """
        command = rf'\{dynamic}_ancora'
        indicator = abjad.Dynamic(dynamic, command=command)
        return IndicatorCommand(
            indicators=[indicator],
            selector=selector,
            )

    @staticmethod
    def apply(
        selector: Selector,
        *commands: typing.Iterable[Command],
        ) -> typing.List[Command]:
        r"""
        Applies ``selector`` to each command in ``commands``.

        ..  container:: example

            Applies leaf selector to commands:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.apply(
            ...         baca.leaves()[4:-3],
            ...         baca.marcato(),
            ...         baca.slur(),
            ...         baca.staccato(),
            ...         ),
            ...     baca.make_even_divisions(),
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
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                -\marcato                                                                %! IC
                                -\staccato                                                               %! IC
                                [
                                (                                                                        %! SC
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                -\marcato                                                                %! IC
                                -\staccato                                                               %! IC
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                -\marcato                                                                %! IC
                                -\staccato                                                               %! IC
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                -\marcato                                                                %! IC
                                -\staccato                                                               %! IC
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                -\marcato                                                                %! IC
                                -\staccato                                                               %! IC
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                -\marcato                                                                %! IC
                                -\staccato                                                               %! IC
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                -\marcato                                                                %! IC
                                -\staccato                                                               %! IC
                                ]
                                )                                                                        %! SC
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ]
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Applies measure selector to commands:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.apply(
            ...         baca.group_by_measures()[1:-1],
            ...         baca.marcato(),
            ...         baca.slur(),
            ...         baca.staccato(),
            ...         ),
            ...     baca.make_even_divisions(),
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
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                -\marcato                                                                %! IC
                                -\staccato                                                               %! IC
                                [
                                (                                                                        %! SC
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                -\marcato                                                                %! IC
                                -\staccato                                                               %! IC
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                -\marcato                                                                %! IC
                                -\staccato                                                               %! IC
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                -\marcato                                                                %! IC
                                -\staccato                                                               %! IC
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                -\marcato                                                                %! IC
                                -\staccato                                                               %! IC
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                -\marcato                                                                %! IC
                                -\staccato                                                               %! IC
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                -\marcato                                                                %! IC
                                -\staccato                                                               %! IC
                                ]
                                )                                                                        %! SC
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                [
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                <BLANKLINE>
                                \baca_unpitched_music_warning                                            %! SM24
                                c'8
                                ]
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Raises exception on nonselector input:

            >>> baca.apply(99, baca.staccato())
            Traceback (most recent call last):
                ...
            Exception:
              Selector must be str or expression.
              Not 99.

        """
        if not isinstance(selector, (str, abjad.Expression)):
            message = '\n  Selector must be str or expression.'
            message += f'\n  Not {selector!r}.'
            raise Exception(message)
        commands_: typing.List[Command] = []
        for command in commands:
            assert isinstance(command, Command), repr(command)
            command_ = abjad.new(command, selector=selector)
            commands_.append(command_)
        return commands_

    @staticmethod
    def arpeggio(
        *,
        selector: Selector = 'baca.chead(0)',
        ) -> IndicatorCommand:
        r"""
        Attaches arpeggio.

        ..  container:: example

            Attaches arpeggio to chord head 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.arpeggio(),
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
                                ~
                                [
                                <ef'' e'' fs'''>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                <g' af''>8
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

            Attaches arpeggio to last two chord heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.arpeggio(selector=baca.cheads()[-2:]),
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
        *,
        selector: Selector = 'baca.phead(0)',
        ) -> IndicatorCommand:
        """
        Attaches ``articulation``.
        """
        articulation_ = abjad.Articulation(articulation)
        return IndicatorCommand(
            indicators=[articulation_],
            selector=selector,
            )

    @staticmethod
    def articulations(
        articulations: typing.List,
        *,
        selector: Selector = 'baca.pheads()',
        ) -> IndicatorCommand:
        """
        Attaches ``articulations``.
        """
        return IndicatorCommand(
            indicators=articulations,
            selector=selector,
            )

    @staticmethod
    def bar_extent(
        pair: NumberPair,
        *,
        selector: Selector = 'baca.leaf(0)',
        after: bool = False,
        ) -> OverrideCommand:
        r"""
        Overrides bar line bar extent.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.bar_extent((-4, 4), selector=baca.group_by_measure()[1]),
            ...     baca.bar_extent((-4, 4), selector=baca.leaf(-1), after=True),
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
                                e'8
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
                                \override Staff.BarLine.bar-extent = #'(-4 . 4)                          %! OC1
                                g'8
                                [
                <BLANKLINE>
                                f''8
                <BLANKLINE>
                                e'8
                                ]
                                \revert Staff.BarLine.bar-extent                                         %! OC2
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
                <BLANKLINE>
                                d''8
                                ]
                                \once \override Staff.BarLine.bar-extent = #'(-4 . 4)                    %! OC1
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return OverrideCommand(
            after=after,
            attribute='bar_extent',
            context='Staff',
            grob='bar_line',
            selector=selector,
            value=pair,
            )

    @staticmethod
    def bar_extent_persistent(
        pair: NumberPair = None,
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        r"""
        Makes persistent bar-extent override.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.bar_extent_persistent((0, 0)),
            ...     baca.make_even_divisions(),
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
                <BLANKLINE>
                                % [MusicVoice measure 1]                                                 %! SM4
                                \override Staff.BarLine.bar-extent = #'(0 . 0)                           %! SM8:EXPLICIT_PERSISTENT_OVERRIDE:IC
                                \stopStaff                                                               %! SM8:EXPLICIT_STAFF_LINES:IC
                                \once \override Staff.StaffSymbol.line-count = 1                         %! SM8:EXPLICIT_STAFF_LINES:IC
                                \startStaff                                                              %! SM8:EXPLICIT_STAFF_LINES:IC
                                \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! SM6:EXPLICIT_STAFF_LINES_COLOR:IC
                                b'8
                                [
                <BLANKLINE>
                                b'8
                <BLANKLINE>
                                b'8
                <BLANKLINE>
                                b'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                b'8
                                [
                <BLANKLINE>
                                b'8
                <BLANKLINE>
                                b'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                b'8
                                [
                <BLANKLINE>
                                b'8
                <BLANKLINE>
                                b'8
                <BLANKLINE>
                                b'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
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
                    >>
                >>

        """
        override = abjad.PersistentOverride(
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
    def bar_extent_zero(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> SuiteCommand:
        """
        Makes bar-extent zero suite.
        """
        return library.suite(
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
            selector=selector,
            )

    @staticmethod
    def bar_line_transparent(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r"""
        Overrides bar line transparency.

        ..  container:: example

            Makes all bar lines transparent:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=rmakers.TaleaRhythmMaker(
            ...             talea=rmakers.Talea(
            ...                 counts=[1, 1, 1, -1],
            ...                 denominator=8,
            ...                 ),
            ...             ),
            ...         ),
            ...     baca.bar_line_transparent(),
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
                                \override Score.BarLine.transparent = ##t                                %! OC1
                                e'8
                                [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8
                                ]
                <BLANKLINE>
                                r8
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                e''8
                                [
                <BLANKLINE>
                                g'8
                <BLANKLINE>
                                f''8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                r8
                <BLANKLINE>
                                e'8
                                [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                r8
                <BLANKLINE>
                                e''8
                                [
                <BLANKLINE>
                                g'8
                                ]
                                \revert Score.BarLine.transparent                                        %! OC2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Makes bar line before measure 1 transparent:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.pitches('E4 D5 F4 E5 G4 F5'),
            ...     baca.RhythmCommand(
            ...         rhythm_maker=rmakers.TaleaRhythmMaker(
            ...             talea=rmakers.Talea(
            ...                 counts=[1, 1, 1, -1],
            ...                 denominator=8,
            ...                 ),
            ...             ),
            ...         ),
            ...     baca.bar_line_transparent(selector=baca.group_by_measure()[1]),
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
                                e'8
                                [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8
                                ]
                <BLANKLINE>
                                r8
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                \override Score.BarLine.transparent = ##t                                %! OC1
                                e''8
                                [
                <BLANKLINE>
                                g'8
                <BLANKLINE>
                                f''8
                                ]
                                \revert Score.BarLine.transparent                                        %! OC2
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                r8
                <BLANKLINE>
                                e'8
                                [
                <BLANKLINE>
                                d''8
                <BLANKLINE>
                                f'8
                                ]
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                r8
                <BLANKLINE>
                                e''8
                                [
                <BLANKLINE>
                                g'8
                                ]
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return OverrideCommand(
            attribute='transparent',
            value=True,
            context='Score',
            grob='bar_line',
            selector=selector,
            )

    @staticmethod
    def bass_to_octave(
        n: int,
        *,
        selector: Selector = 'baca.plts()',
        ) -> RegisterToOctaveCommand:
        r"""
        Octave-transposes music.

        ..  container:: example

            Octave-transposes music such that the lowest note in the entire
            selection appears in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.bass_to_octave(3),
            ...     baca.color(selector=baca.plts().group()),
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
            ...     baca.map(
            ...         baca.plts(),
            ...         baca.bass_to_octave(3),
            ...         ),
            ...     baca.color(selector=baca.plts()),
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
            ...     baca.map(
            ...         baca.plts()[-2:],
            ...         baca.bass_to_octave(3),
            ...         ),
            ...     baca.color(selector=baca.plts()[-2:]),
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
            anchor=abjad.Down,
            octave_number=n,
            selector=selector,
            )

    @staticmethod
    def bcps(
        *tweaks: abjad.LilyPondTweakManager,
        bcps: typing.Iterable[typing.Tuple[int, int]] = None,
        helper: typing.Callable = None,
        selector: Selector = 'baca.leaves()',
        ) -> BowContactPointCommand:
        """
        Makes bow contact points.
        """
        return BowContactPointCommand(
            *tweaks,
            bcps=bcps,
            helper=helper,
            selector=selector,
            )

    @staticmethod
    def beam(
        *tweaks: abjad.LilyPondTweakManager,
        selector: Selector = 'baca.tleaves()',
        ) -> SpannerCommand:
        r"""
        Attaches beam.

        ..  container:: example

            Beams everything:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.beam(),
            ...     baca.make_even_divisions(),
            ...     baca.pitch('C4'),
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
                                c'8
                                [                                                                        %! SC
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                c'8
                <BLANKLINE>
                                c'8
                <BLANKLINE>
                                c'8
                                ]                                                                        %! SC
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return SpannerCommand(
            *tweaks,
            detach_first=True,
            selector=selector,
            spanner=abjad.Beam(),
            )

    @staticmethod
    def beam_divisions(
        *,
        stemlets: Number = None,
        ) -> rmakers.BeamSpecifier:
        r"""
        Beams divisions.

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

        """
        return rmakers.BeamSpecifier(
            beam_each_division=True,
            beam_rests=bool(stemlets),
            stemlet_length=stemlets,
            )

    @staticmethod
    def beam_everything(
        *,
        hide_nibs: bool = False,
        stemlets: Number = None,
        ) -> rmakers.BeamSpecifier:
        r"""
        Beams everything.

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

        """
        return rmakers.BeamSpecifier(
            beam_divisions_together=True,
            beam_each_division=True,
            beam_rests=True,
            hide_nibs=hide_nibs,
            stemlet_length=stemlets,
            )

    @staticmethod
    def beam_positions(
        n: Number,
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r"""
        Overrides beam positions.

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
            ...     baca.beam_positions(6, selector=baca.tuplet(1)),
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

        """
        return OverrideCommand(
            attribute='positions',
            value=(n, n),
            grob='beam',
            selector=selector,
            )

    @staticmethod
    def beam_runs(*, hide_nibs: bool = False) -> rmakers.BeamSpecifier:
        r"""
        Beams PLT runs.

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

        """
        return rmakers.BeamSpecifier(
            beam_divisions_together=True,
            beam_each_division=True,
            beam_rests=False,
            hide_nibs=hide_nibs,
            )

    @staticmethod
    def beam_stencil_false(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        """
        Overrides beam stencil.
        """
        return OverrideCommand(
            attribute='stencil',
            grob='beam',
            selector=selector,
            value=False,
            )

    @staticmethod
    def beam_transparent(
        *,
        selector: Selector = 'baca.leaves()',
        ):
        """
        Overrides beam transparency.
        """
        return OverrideCommand(
            attribute='transparent',
            value=True,
            grob='beam',
            selector=selector,
            )

    @staticmethod
    def breaks(
        *page_specifiers: typing.Any,
        local_measure_numbers: bool = None,
        partial_score: typing.Optional[int] = None,
        ) -> BreakMeasureMap:
        r"""
        Makes breaks.

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

        Set ``partial_score`` when rendering only the first measures of a
        score; leave ``partial_score`` set to none when rendering a complete
        score.

        ..  container:: example

            Raises exception on misnumbered pages:

            >>> breaks = baca.breaks(
            ...     baca.page(
            ...         [1, 20, [15, 20, 20]], 
            ...         [13, 140, [15, 20, 20]], 
            ...         number=1,
            ...         ),
            ...     baca.page(
            ...         [23, 20, [15, 20, 20]],
            ...         number=9,
            ...         ),
            ...     )
            Traceback (most recent call last):
                ... 
            Exception: page number (9) is not 2.

        ..  container:: example

            Raises exception on too few measures:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.StringTrioScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8), (4, 8)],
            ...     breaks=baca.breaks(
            ...         baca.page([99, 0, (10, 20,)]),
            ...         baca.page([109, 0, (10, 20,)]),
            ...         ),
            ...     )

            >>> maker(
            ...     'ViolinMusicVoice',
            ...     baca.make_even_divisions(),
            ...     baca.pitch('E4'),
            ...     )
            >>> lilypond_file = maker.run(environment='docs')
            Traceback (most recent call last):
                ...
            Exception: score ends at measure 103 (not 109).

        """
        commands = abjad.OrderedDict()
        if not page_specifiers:
            return BreakMeasureMap(
                commands=commands,
                partial_score=partial_score,
                )
        first_system = page_specifiers[0].systems[0]
        if hasattr(first_system, 'measure'):
            first_measure_number = first_system.measure
        else:
            first_measure_number = first_system[0]
        bol_measure_numbers = []
        for i, page_specifier in enumerate(page_specifiers):
            page_number = i + 1
            if page_specifier.number is not None:
                if page_specifier.number != page_number:
                    message = f'page number ({page_specifier.number})'
                    message += f' is not {page_number}.'
                    raise Exception(message)
            for j, system in enumerate(page_specifier.systems):
                if hasattr(system, 'measure'):
                    measure_number = system.measure
                else:
                    measure_number = system[0]
                bol_measure_numbers.append(measure_number)
                skip_index = measure_number - first_measure_number
                if hasattr(system, 'y_offset'):
                    y_offset = system.y_offset
                else:
                    y_offset = system[1]
                if hasattr(system, 'distances'):
                    alignment_distances = system.distances
                else:
                    alignment_distances = system[2]
                selector = f'baca.skip({skip_index})'
                if j == 0:
                    break_ = abjad.LilyPondLiteral(r'\pageBreak')
                else:
                    break_ = abjad.LilyPondLiteral(r'\break')
                command = IndicatorCommand(
                    indicators=[break_],
                    selector=selector,
                    )
                lbsd = library.lbsd(
                    y_offset,
                    alignment_distances,
                    selector=selector,
                    )
                commands[measure_number] = [command, lbsd]
        breaks = BreakMeasureMap(
            commands=commands,
            local_measure_numbers=local_measure_numbers,
            partial_score=partial_score,
            )
        breaks._bol_measure_numbers.extend(bol_measure_numbers)
        return breaks

    @staticmethod
    def breathe(
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        """
        Attaches LilyPond breathe command to before-slot.
        """
        breathe = abjad.LilyPondLiteral(r'\breathe', format_slot='before')
        return IndicatorCommand(
            indicators=[breathe],
            selector=selector,
            )

    # TODO: integrate <>
    @staticmethod
    def breathe_after() -> IndicatorCommand:
        """
        Attaches LilyPond breathe command to before-slot of
        leaf-just-after-last.
        """
        breathe = abjad.LilyPondLiteral(r'\breathe', format_slot='before')
        return LibraryAF.breathe(
            selector='baca.rleaves()[-1:]',
            )

    @staticmethod
    def center_to_octave(
        n: int,
        *,
        selector: Selector = 'baca.plts()',
        ) -> RegisterToOctaveCommand:
        r"""
        Octave-transposes music.

        ..  container:: example

            Octave-transposes music such that the centroid of all PLTs appears
            in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.center_to_octave(3),
            ...     baca.color(selector=baca.plts().group()),
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
            ...     baca.map(
            ...         baca.plts(),
            ...         baca.center_to_octave(3),
            ...         ),
            ...     baca.color(selector=baca.plts()),
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
            ...     baca.map(
            ...         baca.plts()[-2:],
            ...         baca.center_to_octave(3),
            ...         ),
            ...     baca.color(selector=baca.plts()[-2:]),
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
        *,
        selector: Selector = 'baca.leaf(0)',
        redundant: bool = None,
        ) -> IndicatorCommand:
        r"""
        Attaches clef.

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

        """
        indicator = abjad.Clef(clef)
        return IndicatorCommand(
            indicators=[indicator],
            redundant=redundant,
            selector=selector,
            )

    @staticmethod
    def clef_extra_offset(
        pair: NumberPair,
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        """
        Overrides clef extra offset.
        """
        return OverrideCommand(
            attribute='extra_offset',
            context='Staff',
            grob='clef',
            selector=selector,
            value=pair,
            )

    @staticmethod
    def clef_shift(
        clef: typing.Union[str, abjad.Clef],
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> SuiteCommand:
        """
        Shifts clef to left by width of clef.
        """
        if isinstance(clef, str):
            clef = abjad.Clef(clef)
        if isinstance(clef, (int, float)):
            extra_offset_x = clef
        else:
            assert isinstance(clef, abjad.Clef)
            width = clef._to_width[clef.name]
            extra_offset_x = -width
        command = library.suite(
            LibraryAF.clef_x_extent_false(),
            LibraryAF.clef_extra_offset((extra_offset_x, 0)),
            )
        library.tag(
            abjad.tags.SHIFTED_CLEF,
            command,
            tag_measure_number=True,
            )
        return command

    @staticmethod
    def clef_x_extent_false(
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        """
        Overrides clef x-extent.
        """
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
        *,
        selector: Selector = 'baca.plts()',
        start_pitch: typing.Union[int, str, abjad.NamedPitch] = None,
        ) -> ClusterCommand:
        """
        Makes clusters with ``widths`` and ``start_pitch``.
        """
        return ClusterCommand(
            selector=selector,
            start_pitch=start_pitch,
            widths=widths,
            )

    @staticmethod
    def coat(pitch: typing.Union[int, str, abjad.Pitch]) -> Coat:
        r"""
        Coats ``pitch``.

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

        """
        return Coat(pitch)

    @staticmethod
    def color(*, selector: Selector = 'baca.leaves()') -> ColorCommand:
        r"""
        Colors leaves.

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

        """
        return ColorCommand(selector=selector)

    @staticmethod
    def color_fingerings(
        numbers: typing.List[Number],
        *,
        selector: Selector = 'baca.pheads()',
        ) -> ColorFingeringCommand:
        """
        Adds color fingerings.
        """
        return ColorFingeringCommand(numbers=numbers, selector=selector)

    @staticmethod
    def compound_quarter_divisions() -> DivisionSequenceExpression:
        """
        Makes compound quarter divisions.
        """
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
        *,
        selector: Selector = 'baca.leaves()',
        ) -> ContainerCommand:
        r"""
        Makes container with ``identifier`` and extends container with
        ``selector`` output.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.container('ViolinI', selector=baca.leaves()[:2]),
            ...     baca.container('ViolinII', selector=baca.leaves()[2:]),
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

        """
        if identifier is not None:
            if not isinstance(identifier, str):
                message = f'identifier must be string (not {identifier!r}).'
                raise Exception(message)
        return ContainerCommand(
            identifier=identifier,
            selector=selector,
            )

    @staticmethod
    def cross_staff(
        *,
        selector: Selector = 'baca.phead(0)',
        ) -> IndicatorCommand:
        r"""
        Attaches cross-staff command.

        ..  container:: example

            Attaches cross-staff command to pitched head 0:

            >>> score_template = baca.StringTrioScoreTemplate()
            >>> accumulator = baca.MusicAccumulator(score_template=score_template)
            >>> accumulator(
            ...     accumulator.music_maker(
            ...         'ViolinMusicVoice',
            ...         [[9, 11, 12, 14, 16]],
            ...         baca.flags(),
            ...         baca.stem_up(),
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
            ...         baca.stem_up(),
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
            ...     spacing=baca.minimum_duration((1, 12)),
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
                                            ef''!8
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
                                            d'8
                <BLANKLINE>
                                            e'8
                <BLANKLINE>
                                            f'8
                <BLANKLINE>
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
            >>> accumulator = baca.MusicAccumulator(score_template=score_template)
            >>> accumulator(
            ...     accumulator.music_maker(
            ...         'ViolinMusicVoice',
            ...         [[9, 11, 12, 14, 16]],
            ...         baca.flags(),
            ...         baca.stem_up(),
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
            ...         baca.stem_up(),
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
            ...     spacing=baca.minimum_duration((1, 12)),
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
                                            ef''!8
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

        """
        return IndicatorCommand(
            indicators=[abjad.LilyPondLiteral(r'\crossStaff')],
            selector=selector,
            )

    @staticmethod
    def deviation(
        deviations: typing.List[Number],
        *,
        selector: Selector = 'baca.plts()',
        ) -> MicrotoneDeviationCommand:
        """
        Sets microtone ``deviations``.
        """
        return MicrotoneDeviationCommand(
            deviations=deviations,
            selector=selector,
            )

    @staticmethod
    def diatonic_clusters(
        widths: typing.List[int],
        *,
        selector: Selector = 'baca.plts()',
        ) -> DiatonicClusterCommand:
        """
        Makes diatonic clusters with ``widths``.
        """
        return DiatonicClusterCommand(
            selector=selector,
            widths=widths,
            )

    @staticmethod
    def displacement(
        displacements: typing.List[int],
        *,
        selector: Selector = 'baca.plts()',
        ) -> OctaveDisplacementCommand:
        r"""
        Octave-displaces ``selector`` output.

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
            ...     baca.displacement(
            ...         [0, 0, -1, -1, 1, 1],
            ...         selector=baca.plts()[-6:],
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

        """
        return OctaveDisplacementCommand(
            displacements=displacements,
            selector=selector,
            )

    @staticmethod
    def dls_padding(
        n: Number,
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        """
        Overrides dynamic line spanner padding.
        """
        return OverrideCommand(
            attribute='padding',
            value=str(n),
            grob='dynamic_line_spanner',
            selector=selector,
            )

    @staticmethod
    def dls_staff_padding(
        n: Number,
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r"""
        Overrides dynamic line spanner staff padding

        ..  container:: example

            Overrides dynamic line spanner staff padding on all leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dls_staff_padding(4),
            ...     baca.map(
            ...         baca.tuplets(),
            ...         baca.hairpin('p < f'),
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
                                \override DynamicLineSpanner.staff-padding = #'4                         %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                r8
                                c'16
                                \p                                                                       %! HC1
                                \<                                                                       %! HC1
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
                                \p                                                                       %! HC1
                                \<                                                                       %! HC1
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
            ...     baca.dls_staff_padding(4, selector=baca.tuplet(1)),
            ...     baca.map(
            ...         baca.tuplets(),
            ...         baca.hairpin('p < f'),
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
                                \p                                                                       %! HC1
                                \<                                                                       %! HC1
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
                                \p                                                                       %! HC1
                                \<                                                                       %! HC1
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

        """
        return OverrideCommand(
            attribute='staff_padding',
            value=str(n),
            grob='dynamic_line_spanner',
            selector=selector,
            )

    @staticmethod
    def dls_up(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r"""
        Overrides dynamic line spanner direction.

        ..  container:: example

            Up-overrides dynamic line spanner direction on all leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.dls_up(),
            ...     baca.map(
            ...         baca.tuplets(),
            ...         baca.hairpin('p < f'),
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
                                \override DynamicLineSpanner.direction = #up                             %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                r8
                                c'16
                                \p                                                                       %! HC1
                                \<                                                                       %! HC1
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
                                \p                                                                       %! HC1
                                \<                                                                       %! HC1
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
            ...     baca.dls_up(selector=baca.tuplet(1)),
            ...     baca.map(
            ...         baca.tuplets(),
            ...         baca.hairpin('p < f'),
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
                                \p                                                                       %! HC1
                                \<                                                                       %! HC1
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
                                \p                                                                       %! HC1
                                \<                                                                       %! HC1
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

        """
        return OverrideCommand(
            attribute='direction',
            value=abjad.Up,
            grob='dynamic_line_spanner',
            selector=selector,
            )

    @staticmethod
    def dots_stencil_false(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        """
        Overrides dots stencil.
        """
        return OverrideCommand(
            attribute='stencil',
            grob='dots',
            selector=selector,
            value=False,
            )

    @staticmethod
    def dots_transparent(
        *,
        selector: Selector = 'baca.leaves()',
        ):
        """
        Overrides dots transparency.
        """
        return OverrideCommand(
            attribute='transparent',
            value=True,
            grob='dots',
            selector=selector,
            )

    @staticmethod
    def double_staccato(
        *,
        selector: Selector = 'baca.phead(0)',
        ) -> IndicatorCommand:
        r"""
        Attaches double-staccato.

        ..  container:: example

            Attaches double-staccato to pitched head 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.double_staccato(),
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
                                -\baca_staccati #2                                                              %! IC
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

            Attaches double-staccato to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.tuplet(1),
            ...         baca.double_staccato(selector=baca.pheads()),
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
                                -\baca_staccati #2                                                              %! IC
                                [
                                e''16
                                -\baca_staccati #2                                                              %! IC
                                ]
                                ef''4
                                -\baca_staccati #2                                                              %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\baca_staccati #2                                                              %! IC
                                [
                                g''16
                                -\baca_staccati #2                                                              %! IC
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
            indicators=[abjad.Articulation('baca_staccati #2')],
            selector=selector,
            )

    @staticmethod
    def down_arpeggio(
        *,
        selector: Selector = 'baca.chead(0)',
        ) -> IndicatorCommand:
        r"""
        Attaches down-arpeggio.

        ..  container:: example

            Attaches down-arpeggio to chord head 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.down_arpeggio(),
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
                                <ef'' e'' fs'''>8
                                ~
                                [
                                <ef'' e'' fs'''>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                <g' af''>8
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

            Attaches down-arpeggio to last two chord heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.down_arpeggio(selector=baca.cheads()[-2:]),
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
    def down_bow(
        *,
        selector: Selector = 'baca.phead(0)',
        ) -> IndicatorCommand:
        r"""
        Attaches down-bow.

        ..  container:: example

            Attaches down-bow to pitched head 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.down_bow(),
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

            Attaches down-bow to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.tuplet(1),
            ...         baca.down_bow(selector=baca.pheads()),
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

        """
        return IndicatorCommand(
            indicators=[abjad.Articulation('downbow')],
            selector=selector,
            )

    @staticmethod
    def espressivo(
        *,
        selector: Selector = 'baca.phead(0)',
        ) -> IndicatorCommand:
        r"""
        Attaches espressivo.

        ..  container:: example

            Attaches espressivo to pitched head 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.espressivo(),
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
                                -\espressivo                                                             %! IC
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

            Attaches espressivo to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.tuplet(1),
            ...         baca.espressivo(selector=baca.pheads()),
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
                                -\espressivo                                                             %! IC
                                [
                                e''16
                                -\espressivo                                                             %! IC
                                ]
                                ef''4
                                -\espressivo                                                             %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\espressivo                                                             %! IC
                                [
                                g''16
                                -\espressivo                                                             %! IC
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
            indicators=[abjad.Articulation('espressivo')],
            selector=selector,
            )

    @staticmethod
    def fermata(
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        r"""
        Attaches fermata.

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
            ...     baca.fermata(selector=baca.tuplets()[1:2].phead(0)),
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

        """
        return IndicatorCommand(
            indicators=[abjad.Articulation('fermata')],
            selector=selector,
            )

    @staticmethod
    def finger_pressure_transition(
        *,
        selector: Selector = 'baca.tleaves()',
        right_broken: bool = None,
        ) -> SuiteCommand:
        r"""
        Makes finger pressure transition glissando.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.finger_pressure_transition(selector=baca.notes()[:2]),
            ...     baca.finger_pressure_transition(selector=baca.notes()[2:]),
            ...     baca.make_notes(),
            ...     baca.note_head_style_harmonic(selector=baca.note(0)),
            ...     baca.note_head_style_harmonic(selector=baca.note(2)),
            ...     baca.pitch('C5'),
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
                                \override Glissando.arrow-length = #'2                                   %! OC1
                                \override Glissando.arrow-width = #'0.5                                  %! OC1
                                \override Glissando.bound-details.right.arrow = ##t                      %! OC1
                                \override Glissando.thickness = #'3                                      %! OC1
                                \once \override NoteHead.style = #'harmonic                              %! OC1
                                c''2
                                \glissando                                                               %! SC
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c''4.
                                \revert Glissando.arrow-length                                           %! OC2
                                \revert Glissando.arrow-width                                            %! OC2
                                \revert Glissando.bound-details.right.arrow                              %! OC2
                                \revert Glissando.thickness                                              %! OC2
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                \override Glissando.arrow-length = #'2                                   %! OC1
                                \override Glissando.arrow-width = #'0.5                                  %! OC1
                                \override Glissando.bound-details.right.arrow = ##t                      %! OC1
                                \override Glissando.thickness = #'3                                      %! OC1
                                \once \override NoteHead.style = #'harmonic                              %! OC1
                                c''2
                                \glissando                                                               %! SC
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                c''4.
                                \revert Glissando.arrow-length                                           %! OC2
                                \revert Glissando.arrow-width                                            %! OC2
                                \revert Glissando.bound-details.right.arrow                              %! OC2
                                \revert Glissando.thickness                                              %! OC2
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return library.suite(
            SpannerCommand(
                right_broken=right_broken,
                selector=selector,
                spanner=abjad.Glissando(allow_repeats=True),
                ),
            OverrideCommand(
                attribute='arrow_length',
                value='2',
                grob='glissando',
                selector=selector,
                ),
            OverrideCommand(
                attribute='arrow_width',
                value='0.5',
                grob='glissando',
                selector=selector,
                ),
            OverrideCommand(
                attribute='bound_details__right__arrow',
                value=True,
                grob='glissando',
                selector=selector,
                ),
            OverrideCommand(
                attribute='thickness',
                value='3',
                grob='glissando',
                selector=selector,
                ),
            )

    @staticmethod
    def flag_stencil_false(
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        """
        Overrides flag stencil.
        """
        return OverrideCommand(
            attribute='stencil',
            grob='flag',
            selector=selector,
            value=False,
            )

    @staticmethod
    def flag_transparent(
        *,
        selector: Selector = 'baca.leaves()',
        ):
        """
        Overrides flag transparency.
        """
        return OverrideCommand(
            attribute='transparent',
            value=True,
            grob='flag',
            selector=selector,
            )

    @staticmethod
    def flageolet(
        *,
        selector: Selector = 'baca.phead(0)',
        ) -> IndicatorCommand:
        r"""
        Attaches flageolet.

        ..  container:: example

            Attaches flageolet to pitched head 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.flageolet(),
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

            Attaches flageolet to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.tuplet(1),
            ...         baca.flageolet(selector=baca.pheads()),
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

        """
        return IndicatorCommand(
            indicators=[abjad.Articulation('flageolet')],
            selector=selector,
            )

    @staticmethod
    def flags() -> rmakers.BeamSpecifier:
        r"""
        Flags music.

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

        """
        return rmakers.BeamSpecifier(
            beam_divisions_together=False,
            beam_each_division=False,
            )

    @staticmethod
    def force_accidental(
        *,
        selector: Selector = 'baca.pleaf(0)',
        ) -> AccidentalAdjustmentCommand:
        r"""
        Forces accidental.

        ..  container:: example

            Inverts edition-specific tags:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.not_parts(baca.force_accidental(selector=baca.pleaves()[:2])),
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

        """
        return AccidentalAdjustmentCommand(
            forced=True,
            selector=selector,
            )

    @staticmethod
    def fuse_compound_quarter_divisions(
        counts: typing.List[int],
        ) -> DivisionSequenceExpression:
        r"""
        Fuses compound quarter divisions.

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

        """
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
