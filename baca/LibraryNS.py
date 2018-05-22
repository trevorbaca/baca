import abjad
import baca
import collections
import typing
from abjad import rhythmos
from .AnchorSpecifier import AnchorSpecifier
from .BreakMeasureMap import BreakMeasureMap
from .ClusterCommand import ClusterCommand
from .Command import Command
from .ContainerCommand import ContainerCommand
from .DivisionMaker import DivisionMaker
from .DivisionSequenceExpression import DivisionSequenceExpression
from .HorizontalSpacingSpecifier import HorizontalSpacingSpecifier
from .IndicatorCommand import IndicatorCommand
from .MapCommand import MapCommand
from .MarkupLibrary import MarkupLibrary
from .NestingCommand import NestingCommand
from .OverrideCommand import OverrideCommand
from .PageSpecifier import PageSpecifier
from .PartAssignmentCommand import PartAssignmentCommand
from .PiecewiseCommand import PiecewiseCommand
from .PitchCommand import PitchCommand
from .RegisterCommand import RegisterCommand
from .RegisterInterpolationCommand import RegisterInterpolationCommand
from .RegisterToOctaveCommand import RegisterToOctaveCommand
from .Registration import Registration
from .RestAffixSpecifier import RestAffixSpecifier
from .RhythmCommand import RhythmCommand
from .Scope import Scope
from .SettingCommand import SettingCommand
from .SpannerCommand import SpannerCommand
from .StaffLines import StaffLines
from .StaffPositionCommand import StaffPositionCommand
from .SuiteCommand import SuiteCommand
from .SystemSpecifier import SystemSpecifier
from .TieCorrectionCommand import TieCorrectionCommand
from .Typing import Number
from .Typing import NumberPair
from .Typing import Selector
rhythm_maker_typing = typing.Union[
    rhythmos.RhythmMaker,
    abjad.Selection,
    typing.Iterable[
        typing.Tuple[
            typing.Union[
                rhythmos.RhythmMaker,
                abjad.Selection,
                ],
            abjad.Pattern,
            ],
        ],
    ]


class LibraryNS(abjad.AbjadObject):
    """
    Library N - S.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(1) Library'

    __slots__ = (
        )

    ### PUBLIC METHODS ###

    @staticmethod
    def natural_clusters(
        widths: typing.Iterable[int],
        *,
        selector: Selector = 'baca.plts()',
        start_pitch: typing.Union[int, str, abjad.NamedPitch] = None,
        ) -> ClusterCommand:
        """
        Makes natural clusters with ``widths`` and ``start_pitch``.
        """
        return ClusterCommand(
            hide_flat_markup=True,
            selector=selector,
            start_pitch=start_pitch,
            widths=widths,
            )

    @staticmethod
    def nest(
        time_treatments: typing.Iterable = None,
        ) -> NestingCommand:
        r"""
        Nests music.

        ..  container:: example

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.nest('+4/16'),
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
                            \times 13/11 {
                                \tweak text #tuplet-number::calc-fraction-text
                                \times 9/10 {
                                    \override TupletBracket.staff-padding = #5                           %! OC1
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
                                    \revert TupletBracket.staff-padding                                  %! OC2
                                }
                            }
                        }
                    }
                >>

        """
        if not isinstance(time_treatments, list):
            time_treatments = [time_treatments]
        return NestingCommand(
            lmr_specifier=None,
            time_treatments=time_treatments,
            )

    @staticmethod
    def no_ledgers(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        """
        Overrides note-head no-ledgers.
        """
        return OverrideCommand(
            attribute='no_ledgers',
            value=True,
            grob='note_head',
            selector=selector,
            )

    @staticmethod
    def not_parts(command: Command) -> Command:
        """
        Tags ``command`` with ``-PARTS``.

        Returns ``command``.
        """
        from .LibraryTZ import LibraryTZ
        return LibraryTZ.tag(
            '-PARTS',
            command,
            )

    @staticmethod
    def not_score(command: Command) -> Command:
        """
        Tags ``command`` with ``-SCORE``.

        Returns ``command``.
        """
        from .LibraryTZ import LibraryTZ
        return LibraryTZ.tag(
            '-SCORE',
            command,
            )

    @staticmethod
    def not_segment(command: Command) -> Command:
        """
        Tags ``command`` with ``-SEGMENT``.

        Returns ``command``.
        """
        from .LibraryTZ import LibraryTZ
        return LibraryTZ.tag(
            '-SEGMENT',
            command,
            )

    @staticmethod
    def note_column_shift(
        n: Number,
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        """
        Overrides note column force hshift.
        """
        return OverrideCommand(
            attribute='force_hshift',
            value=n,
            grob='note_column',
            selector=selector,
            )

    @staticmethod
    def note_head_color(
        color: str,
        *,
        selector: Selector = 'baca.pleaves()',
        ) -> OverrideCommand:
        """
        Overrides note-head color.
        """
        return OverrideCommand(
            attribute='color',
            grob='note_head',
            selector=selector,
            value=color,
            )

    @staticmethod
    def note_head_stencil_false(
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        """
        Overrides note-head stencil.
        """
        return OverrideCommand(
            attribute='stencil',
            grob='note_head',
            selector=selector,
            value=False,
            )

    @staticmethod
    def note_head_style_cross(
        *,
        selector: Selector = 'baca.tleaves()',
        ) -> OverrideCommand:
        r"""
        Overrides note-head style.

        ..  container:: example

            Overrides note-head style on all pitched leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.note_head_style_cross(),
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
            ...     baca.note_head_style_cross(selector=baca.tuplet(1)),
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

        """
        return OverrideCommand(
            attribute='style',
            value='cross',
            grob='note_head',
            selector=selector,
            )

    @staticmethod
    def note_head_style_harmonic(
        *,
        selector: Selector = 'baca.tleaves()',
        ) -> OverrideCommand:
        r"""
        Overrides note-head style for ``selector`` output.

        ..  container:: example

            Overrides note-head style on all PLTs:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.note_head_style_harmonic(),
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
                                \override NoteHead.style = #'harmonic                                    %! OC1
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

            Overrides note-head style on PLTs in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.note_head_style_harmonic(selector=baca.tuplet(1)),
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
                                \override NoteHead.style = #'harmonic                                    %! OC1
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

        """
        return OverrideCommand(
            attribute='style',
            value='harmonic',
            grob='note_head',
            selector=selector,
            )

    @staticmethod
    def note_head_transparent(
        *,
        selector: Selector = 'baca.leaves()',
        ):
        """
        Overrides note-head transparency.
        """
        return OverrideCommand(
            attribute='transparent',
            value=True,
            grob='note_head',
            selector=selector,
            )

    @staticmethod
    def one_voice(
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        """
        Makes LilyPond ``\oneVoice`` command.
        """
        literal = abjad.LilyPondLiteral(r'\oneVoice')
        return IndicatorCommand(
            indicators=[literal],
            selector=selector,
            )

    @staticmethod
    def only_parts(command: Command) -> Command:
        """
        Tags ``command`` with ``+PARTS``.

        Returns ``command``.
        """
        from .LibraryTZ import LibraryTZ
        return LibraryTZ.tag(
            '+PARTS',
            command,
            )

    @staticmethod
    def only_score(command: Command) -> Command:
        """
        Tags ``command`` with ``+SCORE``.

        Returns ``command``.
        """
        from .LibraryTZ import LibraryTZ
        return LibraryTZ.tag(
            '+SCORE',
            command,
            )

    @staticmethod
    def only_segment(command: Command) -> Command:
        """
        Tags ``command`` with ``+SEGMENT``.

        Returns ``command``.
        """
        from .LibraryTZ import LibraryTZ
        return LibraryTZ.tag(
            '+SEGMENT',
            command,
            )

    @staticmethod
    def ottava(
        *,
        selector: Selector = 'baca.tleaves()',
        ) -> SpannerCommand:
        r"""
        Attaches ottava spanner.

        ..  container:: example

            Attaches ottava spanner to trimmed leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.ottava(),
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
                                \ottava #1                                                               %! SC
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
                                \ottava #0                                                               %! SC
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return SpannerCommand(
            selector=selector,
            spanner=abjad.OctavationSpanner(start=1, stop=0),
            )

    @staticmethod
    def ottava_bassa(
        *,
        selector: Selector = 'baca.tleaves()',
        ) -> SpannerCommand:
        r"""
        Attaches ottava bassa spanner.

        ..  container:: example

            Attaches ottava bassa spanner to trimmed leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.ottava_bassa(),
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
                                \ottava #-1                                                              %! SC
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
                                \ottava #0                                                               %! SC
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return SpannerCommand(
            selector=selector,
            spanner=abjad.OctavationSpanner(start=-1, stop=0),
            )

    @staticmethod
    def ottava_bracket_staff_padding(
        n: Number,
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        """
        Overrides ottava bracket staff padding.
        """
        return OverrideCommand(
            attribute='staff_padding',
            context='Staff',
            value=n,
            grob='ottava_bracket',
            selector=selector,
            )

    @staticmethod
    def page(
        *systems: typing.Any,
        number: int = None
        ) -> PageSpecifier:
        r"""
        Makes page specifier.

        ..  container:: example
            
            Raises exception when systems overlap at Y-offset:

            >>> baca.page(
            ...     [1, 60, (20, 20,)],
            ...     [4, 60, (20, 20,)],
            ...     )
            Traceback (most recent call last):
                ...
            Exception: systems overlap at Y-offset 60.

        """
        if systems is None:
            systems_ = None
        else:
            systems_ = []
            prototype = (list, SystemSpecifier)
            for system in systems:
                assert isinstance(system, prototype), repr(system)
                systems_.append(system)
        return PageSpecifier(number=number, systems=systems_)

    @staticmethod
    def parts(
        part_assignment: abjad.PartAssignment,
        *,
        selector: Selector = 'baca.leaves()',
        ) -> PartAssignmentCommand:
        r"""
        Inserts ``selector`` output in container and sets part assignment.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.StringTrioScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'ViolinMusicVoice',
            ...     baca.make_notes(),
            ...     baca.parts(abjad.PartAssignment('Violin')),
            ...     baca.pitch('E4'),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

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
                    \context StringSectionStaffGroup = "String Section Staff Group"
                    <<
                        \tag Violin                                                                  %! ST4
                        \context ViolinMusicStaff = "ViolinMusicStaff"
                        {
                            \context ViolinMusicVoice = "ViolinMusicVoice"
                            {
                                {   %*% PartAssignment('Violin')
            <BLANKLINE>
                                    % [ViolinMusicVoice measure 1]                                   %! SM4
                                    \set ViolinMusicStaff.instrumentName = \markup {                 %! SM8:DEFAULT_INSTRUMENT:ST1
                                        \hcenter-in                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                            #10                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                            Violin                                                   %! SM8:DEFAULT_INSTRUMENT:ST1
                                        }                                                            %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \set ViolinMusicStaff.shortInstrumentName = \markup {            %! SM8:DEFAULT_INSTRUMENT:ST1
                                        \hcenter-in                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                            #10                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                            Vn.                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                        }                                                            %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \clef "treble"                                                   %! SM8:DEFAULT_CLEF:ST3
                                    \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                    \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                                %@% \override ViolinMusicStaff.Clef.color = ##f                      %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                    \set ViolinMusicStaff.forceClef = ##t                            %! SM8:DEFAULT_CLEF:SM33:ST3
                                    e'2
                                    ^ \markup {                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        \with-color                                                  %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            #(x11-color 'DarkViolet)                                 %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                            (Violin)                                                 %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        }                                                            %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                    \set ViolinMusicStaff.instrumentName = \markup {                 %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        \hcenter-in                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            #10                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            Violin                                                   %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        }                                                            %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \set ViolinMusicStaff.shortInstrumentName = \markup {            %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        \hcenter-in                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            #10                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                            Vn.                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        }                                                            %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)     %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
            <BLANKLINE>
                                    % [ViolinMusicVoice measure 2]                                   %! SM4
                                    e'4.
            <BLANKLINE>
                                    % [ViolinMusicVoice measure 3]                                   %! SM4
                                    e'2
            <BLANKLINE>
                                    % [ViolinMusicVoice measure 4]                                   %! SM4
                                    e'4.
            <BLANKLINE>
                                }   %*% PartAssignment('Violin')
                            }
                        }
                        \tag Viola                                                                   %! ST4
                        \context ViolaMusicStaff = "ViolaMusicStaff"
                        {
                            \context ViolaMusicVoice = "ViolaMusicVoice"
                            {
            <BLANKLINE>
                                % [ViolaMusicVoice measure 1]                                        %! SM4
                                \set ViolaMusicStaff.instrumentName = \markup {                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \hcenter-in                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                        #10                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                        Viola                                                        %! SM8:DEFAULT_INSTRUMENT:ST1
                                    }                                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                \set ViolaMusicStaff.shortInstrumentName = \markup {                 %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \hcenter-in                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                        #10                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                        Va.                                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                    }                                                                %! SM8:DEFAULT_INSTRUMENT:ST1
                                \clef "alto"                                                         %! SM8:DEFAULT_CLEF:ST3
                                \once \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                            %@% \override ViolaMusicStaff.Clef.color = ##f                           %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                \set ViolaMusicStaff.forceClef = ##t                                 %! SM8:DEFAULT_CLEF:SM33:ST3
                                R1 * 1/2
                                ^ \markup {                                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \with-color                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        #(x11-color 'DarkViolet)                                     %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        (Viola)                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    }                                                                %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                \set ViolaMusicStaff.instrumentName = \markup {                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \hcenter-in                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        #10                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        Viola                                                        %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    }                                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                \set ViolaMusicStaff.shortInstrumentName = \markup {                 %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \hcenter-in                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        #10                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        Va.                                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    }                                                                %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)          %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
            <BLANKLINE>
                                % [ViolaMusicVoice measure 2]                                        %! SM4
                                R1 * 3/8
            <BLANKLINE>
                                % [ViolaMusicVoice measure 3]                                        %! SM4
                                R1 * 1/2
            <BLANKLINE>
                                % [ViolaMusicVoice measure 4]                                        %! SM4
                                R1 * 3/8
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
                                R1 * 1/2
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
                                R1 * 3/8
            <BLANKLINE>
                                % [CelloMusicVoice measure 3]                                        %! SM4
                                R1 * 1/2
            <BLANKLINE>
                                % [CelloMusicVoice measure 4]                                        %! SM4
                                R1 * 3/8
            <BLANKLINE>
                            }
                        }
                    >>
                >>
            >>

        ..  container:: example

            Raises exception when voice does not allow part assignment:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.StringTrioScoreTemplate(),
            ...     test_container_identifiers=True,
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> part_assignment = abjad.PartAssignment('Flute')

            >>> maker(
            ...     'ViolinMusicVoice',
            ...     baca.make_notes(),
            ...     baca.parts(part_assignment),
            ...     baca.pitches('E4 F4'),
            ...     )

            >>> lilypond_file = maker.run(environment='docs')
            Traceback (most recent call last):
                ...
            Exception: ViolinMusicVoice does not allow Flute part assignment:
              abjad.PartAssignment('Flute')

        """
        if not isinstance(part_assignment, abjad.PartAssignment):
            message = 'part_assignment must be part assignment'
            message += f' (not {part_assignment!r}).'
            raise Exception(message)
        return PartAssignmentCommand(
            part_assignment=part_assignment,
            )

    @staticmethod
    def piecewise(
        spanner: abjad.Spanner,
        indicators: typing.Iterable,
        selector: Selector,
        *,
        bookend: bool = False,
        spanner_selector: typing.Union[MapCommand, Selector] = 'baca.leaves()',
        tweaks: typing.List[typing.Tuple] = None,
        ):
        """
        Makes piecewise command from ``spanner``, ``indicators`` and
        indicator ``selector``.
        """
        return PiecewiseCommand(
            bookend=bookend,
            indicators=indicators,
            selector=selector,
            spanner=spanner,
            spanner_selector=spanner_selector,
            tweaks=tweaks,
            )

    @staticmethod
    def pitch(
        pitch,
        *,
        selector: Selector = 'baca.pleaves()',
        do_not_transpose: bool = None,
        persist: str = None,
        ) -> PitchCommand:
        """
        Makes pitch command.
        """
        if isinstance(pitch, (list, tuple)) and len(pitch) == 1:
            raise Exception(f'one-note chord {pitch!r}?')
        if do_not_transpose not in (None, True, False):
            raise Exception('do_not_transpose must be boolean'
                f' (not {do_not_transpose!r}).')
        if persist is not None and not isinstance(persist, str):
            raise Exception(f'persist name must be string (not {persist!r}).')
        return PitchCommand(
            allow_repeats=True,
            cyclic=True,
            do_not_transpose=do_not_transpose,
            persist=persist,
            pitches=[pitch],
            selector=selector,
            )

    @staticmethod
    def pitches(
        pitches: typing.Iterable,
        *,
        allow_repeats: bool = None,
        do_not_transpose: bool = None,
        exact: bool = None,
        ignore_incomplete: bool = None,
        persist: str = None,
        selector: Selector = 'baca.pleaves()',
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
            allow_repeats=allow_repeats,
            cyclic=cyclic,
            do_not_transpose=do_not_transpose,
            ignore_incomplete=ignore_incomplete,
            persist=persist,
            pitches=pitches,
            selector=selector,
            )

    @staticmethod
    def possibile_dynamic(
        dynamic: str,
        *,
        selector: Selector = 'baca.phead(0)',
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
                                \ff_poss                                                                 %! IC
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
                                \ff_poss                                                                 %! IC
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
        command = rf'\{dynamic}_poss'
        indicator = abjad.Dynamic(dynamic, command=command)
        return IndicatorCommand(
            indicators=[indicator],
            selector=selector,
            )

    @staticmethod
    def previous_metadata(path: str) -> typing.Optional[abjad.OrderedDict]:
        """
        Gets previous segment metadata before ``path``.
        """
        # reproduces abjad.Path.get_previous_path()
        # because Travis isn't configured for scores-directory calculations
        definition_py = abjad.Path(path)
        segment = abjad.Path(definition_py).parent
        assert segment.is_segment(), repr(segment)
        segments = segment.parent
        assert segments.is_segments(), repr(segments)
        paths = segments.list_paths()
        paths = [_ for _ in paths if not _.name.startswith('.')]
        assert all(_.is_dir() for _ in paths), repr(paths)
        index = paths.index(segment)
        if index == 0:
            return None
        previous_index = index - 1
        previous_segment = paths[previous_index]
        previous_metadata = previous_segment.get_metadata()
        return previous_metadata

    @staticmethod
    def register(
        start: int,
        stop: int = None,
        *,
        selector: Selector = 'baca.plts()',
        ) -> typing.Union[RegisterCommand, RegisterInterpolationCommand]:
        r"""
        Octave-transposes ``selector`` output.

        ..  container:: example

            Octave-transposes all PLTs to the octave rooted at -6:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.register(-6),
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
                                bf4
                                ~
                                bf16
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs16
                                [
                                e'16
                                ]
                                ef'4
                                ~
                                ef'16
                                r16
                                af16
                                [
                                g16
                                ]
                            }
                            \times 4/5 {
                                a16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

            Octave-transposes PLTs in tuplet 1 to the octave rooted at -6:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.color(selector=baca.tuplet(1)),
            ...     baca.register(-6, selector=baca.tuplet(1)),
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
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                fs16
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                e'16
                                ]
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                ef'4
                                ~
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                ef'16
                                \once \override Dots.color = #green
                                \once \override Rest.color = #green
                                r16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                af16
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                g16
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

            Octave-transposes all PLTs to an octave interpolated from -6 to 18:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.register(-6, 18),
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
                                fs'16
                                [
                                e'16
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
                                a''16
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

            Octave-transposes PLTs in tuplet 1 to an octave interpolated from
            -6 to 18:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.color(selector=baca.tuplet(1)),
            ...     baca.register(-6, 18, selector=baca.tuplet(1)),
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
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                fs16
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                e'16
                                ]
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                ef'4
                                ~
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                ef'16
                                \once \override Dots.color = #green
                                \once \override Rest.color = #green
                                r16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                af'16
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
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
        if stop is None:
            return RegisterCommand(
                registration=Registration([('[A0, C8]', start)]),
                selector=selector,
                )
        return RegisterInterpolationCommand(
            selector=selector,
            start_pitch=start,
            stop_pitch=stop,
            )

    @staticmethod
    def rehearsal_mark(
        argument: typing.Union[int, str],
        *,
        selector: Selector = 'baca.leaf(0)',
        tweaks: typing.List[typing.Tuple] = None,
        ) -> IndicatorCommand:
        """
        Attaches rehearsal mark.
        """
        if isinstance(argument, str):
            mark = abjad.RehearsalMark.from_string(argument)
        else:
            assert isinstance(argument, int)
            mark = abjad.RehearsalMark(number=argument)
        if tweaks is not None:
            assert isinstance(tweaks, list), tweaks
            for tweak in tweaks:
                assert isinstance(tweak, tuple), repr(tweak)
                assert len(tweak) == 2, repr(tweak)
                assert isinstance(tweak[0], str), repr(tweak)
        return IndicatorCommand(
            indicators=[mark],
            selector=selector,
            tweaks=tweaks,
            )

    @staticmethod
    def rehearsal_mark_extra_offset(
        pair: NumberPair,
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        """
        Overrides rehearsal mark extra offset.
        """
        return OverrideCommand(
            attribute='extra_offset',
            value=pair,
            context='GlobalContext',
            grob='rehearsal_mark',
            selector=selector,
            )

    @staticmethod
    def rehearsal_mark_y_offset(
        n: Number,
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        """
        Overrides rehearsal mark Y offset.
        """
        return OverrideCommand(
            attribute='Y_offset',
            value=n,
            context='GlobalContext',
            grob='rehearsal_mark',
            selector=selector,
            )

    # TODO: remove
    @staticmethod
    def reiterated_dynamic(
        dynamic: str,
        *,
        selector: Selector = 'baca.pheads()',
        ) -> IndicatorCommand:
        r"""
        Attaches `dynamic` to pitched heads.

        ..  container:: example

            Attaches dynamic to pitched heads:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.reiterated_dynamic('f'),
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
                                \f                                                                       %! IC
                                ]
                                bf'4
                                \f                                                                       %! IC
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
                                \f                                                                       %! IC
                                ]
                                ef''4
                                \f                                                                       %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                \f                                                                       %! IC
                                [
                                g''16
                                \f                                                                       %! IC
                                ]
                            }
                            \times 4/5 {
                                a'16
                                \f                                                                       %! IC
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches dynamic to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.reiterated_dynamic(
            ...         'f',
            ...         selector=baca.tuplets()[1:2].pheads(),
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
                                \f                                                                       %! IC
                                [
                                e''16
                                \f                                                                       %! IC
                                ]
                                ef''4
                                \f                                                                       %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                \f                                                                       %! IC
                                [
                                g''16
                                \f                                                                       %! IC
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
            indicators=[abjad.Dynamic(dynamic)],
            selector=selector,
            )

    @staticmethod
    def repeat_tie(
        *,
        selector: Selector = 'baca.qrun(0)',
        ) -> SpannerCommand:
        r"""
        Attaches repeat tie.

        ..  container:: example

            Attaches repeat tie to each equipitch run:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 0, 10], [10, 16, 16, 18, 20], [9]],
            ...     baca.map(baca.repeat_tie(), baca.qruns()),
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
                                c'16
                                \repeatTie                                                               %! SC
                                ]
                                bf'4
                                bf'16
                                \repeatTie                                                               %! SC
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                bf'16
                                [
                                e''16
                                ]
                                e''4
                                \repeatTie                                                               %! SC
                                e''16
                                \repeatTie                                                               %! SC
                                r16
                                fs''16
                                [
                                af''16
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
        return SpannerCommand(
            selector=selector,
            spanner=abjad.Tie(repeat=True),
            )

    @staticmethod
    def repeat_tie_down(
        *,
        selector: Selector = 'baca.tleaves()',
        ) -> OverrideCommand:
        r"""
        Overrides repeat tie direction.

        ..  container:: example

            Overrides repeat tie direction on pitched leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[11, 11, 12], [11, 11, 11], [11]],
            ...     baca.map(baca.repeat_tie(), baca.qruns()),
            ...     baca.repeat_tie_down(),
            ...     baca.rests_around([2], [4]),
            ...     baca.stem_up(),
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
                                \override RepeatTie.direction = #down                                    %! OC1
                                \override Stem.direction = #up                                           %! OC1
                                b'16
                                [
                                b'16
                                \repeatTie                                                               %! SC
                                ]
                                c''4
                                c''16
                                \repeatTie                                                               %! SC
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                b'16
                                [
                                b'16
                                \repeatTie                                                               %! SC
                                ]
                                b'4
                                \repeatTie                                                               %! SC
                                b'16
                                \repeatTie                                                               %! SC
                                r16
                            }
                            \times 4/5 {
                                b'16
                                \revert RepeatTie.direction                                              %! OC2
                                \revert Stem.direction                                                   %! OC2
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides repeat tie direction on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[11, 11, 12], [11, 11, 11], [11]],
            ...     baca.map(baca.repeat_tie(), baca.qruns()),
            ...     baca.map(baca.repeat_tie_down(), baca.tuplet(1)),
            ...     baca.rests_around([2], [4]),
            ...     baca.stem_up(),
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
                                \override Stem.direction = #up                                           %! OC1
                                b'16
                                [
                                b'16
                                \repeatTie                                                               %! SC
                                ]
                                c''4
                                c''16
                                \repeatTie                                                               %! SC
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                \override RepeatTie.direction = #down                                    %! OC1
                                b'16
                                [
                                b'16
                                \repeatTie                                                               %! SC
                                ]
                                b'4
                                \repeatTie                                                               %! SC
                                b'16
                                \repeatTie                                                               %! SC
                                \revert RepeatTie.direction                                              %! OC2
                                r16
                            }
                            \times 4/5 {
                                b'16
                                \revert Stem.direction                                                   %! OC2
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return OverrideCommand(
            attribute='direction',
            value=abjad.Down,
            grob='repeat_tie',
            selector=selector,
            )

    @staticmethod
    def repeat_tie_from(
        *,
        selector: Selector = 'baca.pleaf(-1)',
        ) -> TieCorrectionCommand:
        r"""
        Repeat-ties from leaf.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_notes(),
            ...     baca.repeat_tie_from(selector=baca.leaf(1)),
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
                                c'2
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                c'2
                                \repeatTie                                                               %! TCC
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return TieCorrectionCommand(
            repeat=True,
            selector=selector,
            )

    @staticmethod
    def repeat_tie_repeat_pitches() -> MapCommand:
        """
        Repeat-ties repeat pitches.
        """
        return baca.map(
            SpannerCommand(
                selector='baca.qrun(0)',
                spanner=abjad.Tie(repeat=True),
                ),
            baca.select().ltqruns().nontrivial(),
            )

    @staticmethod
    def repeat_tie_stencil_false(
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        """
        Overrides repeat tie stencil.
        """
        return OverrideCommand(
            attribute='stencil',
            grob='repeat_tie',
            selector=selector,
            value=False,
            )

    @staticmethod
    def repeat_tie_to(
        *,
        selector: Selector = 'baca.pleaf(0)',
        ) -> TieCorrectionCommand:
        r"""
        Repeat-ties to leaf.

        ..  container:: example

            >>> maker = baca.SegmentMaker(
            ...     ignore_unpitched_notes=True,
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_notes(),
            ...     baca.repeat_tie_to(selector=baca.leaf(2)),
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
                                c'2
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                c'2
                                \repeatTie                                                               %! TCC
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return TieCorrectionCommand(
            direction=abjad.Left,
            repeat=True,
            selector=selector,
            )

    @staticmethod
    def repeat_tie_transparent(
        *,
        selector: Selector = 'baca.leaves()',
        ):
        """
        Overrides repeat tie transparency.
        """
        return OverrideCommand(
            attribute='transparent',
            value=True,
            grob='repeat_tie',
            selector=selector,
            )

    @staticmethod
    def repeat_tie_up(
        *,
        selector: Selector = 'baca.tleaves()',
        ) -> OverrideCommand:
        r"""
        Overrides repeat tie direction.

        ..  container:: example

            Overrides repeat tie direction on all leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[11, 11, 12], [11, 11, 11], [11]],
            ...     baca.map(baca.repeat_tie(), baca.qruns()),
            ...     baca.repeat_tie_up(),
            ...     baca.rests_around([2], [4]),
            ...     baca.stem_down(),
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
                                \override RepeatTie.direction = #up                                      %! OC1
                                \override Stem.direction = #down                                         %! OC1
                                b'16
                                [
                                b'16
                                \repeatTie                                                               %! SC
                                ]
                                c''4
                                c''16
                                \repeatTie                                                               %! SC
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                b'16
                                [
                                b'16
                                \repeatTie                                                               %! SC
                                ]
                                b'4
                                \repeatTie                                                               %! SC
                                b'16
                                \repeatTie                                                               %! SC
                                r16
                            }
                            \times 4/5 {
                                b'16
                                \revert RepeatTie.direction                                              %! OC2
                                \revert Stem.direction                                                   %! OC2
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides repeat tie direction on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[11, 11, 12], [11, 11, 11], [11]],
            ...     baca.map(baca.repeat_tie(), baca.qruns()),
            ...     baca.map(baca.repeat_tie_up(), baca.tuplet(1)),
            ...     baca.rests_around([2], [4]),
            ...     baca.stem_down(),
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
                                \override Stem.direction = #down                                         %! OC1
                                b'16
                                [
                                b'16
                                \repeatTie                                                               %! SC
                                ]
                                c''4
                                c''16
                                \repeatTie                                                               %! SC
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 7/8 {
                                \override RepeatTie.direction = #up                                      %! OC1
                                b'16
                                [
                                b'16
                                \repeatTie                                                               %! SC
                                ]
                                b'4
                                \repeatTie                                                               %! SC
                                b'16
                                \repeatTie                                                               %! SC
                                \revert RepeatTie.direction                                              %! OC2
                                r16
                            }
                            \times 4/5 {
                                b'16
                                \revert Stem.direction                                                   %! OC2
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
            grob='repeat_tie',
            selector=selector,
            )

    @staticmethod
    def rest_down(
        *,
        selector: Selector = 'baca.rests()',
        ) -> OverrideCommand:
        r"""
        Overrides rest direction.

        ..  container:: example

            Down-overrides direction of rests:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rest_down(),
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
                                \override Rest.direction = #down                                         %! OC1
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
                                \revert Rest.direction                                                   %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Down-overrides direction of rests in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(baca.rest_down(), baca.tuplet(1)),
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
                                \once \override Rest.direction = #down                                   %! OC1
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
        return OverrideCommand(
            attribute='direction',
            value=abjad.Down,
            grob='rest',
            selector=selector,
            )

    @staticmethod
    def rest_extra_offset(
        pair: NumberPair,
        *,
        selector: Selector = 'baca.rest(0)',
        ) -> OverrideCommand:
        """
        Overrides rest extra offset.
        """
        if not isinstance(pair, tuple):
            raise Exception(
                f'rest extra offset must be pair (not {pair!r}).'
                )
        if len(pair) != 2:
            raise Exception(
                f'rest extra offset must be pair (not {pair!r}).'
                )
        return OverrideCommand(
            attribute='extra_offset',
            value=pair,
            grob='rest',
            selector=selector,
            )

    @staticmethod
    def rest_position(
        n: Number,
        *,
        selector: Selector = 'baca.rests()',
        ) -> OverrideCommand:
        r"""
        Overrides rest position.

        ..  container:: example

            Overrides rest position:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rest_position(-6),
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
                                \override Rest.staff-position = #-6                                      %! OC1
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
                                \revert Rest.staff-position                                              %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides rest position in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(baca.rest_position(-6), baca.tuplet(1)),
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
                                \once \override Rest.staff-position = #-6                                %! OC1
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
        return OverrideCommand(
            attribute='staff_position',
            value=n,
            grob='rest',
            selector=selector,
            )

    @staticmethod
    def rest_transparent(
        *,
        selector: Selector = 'baca.rests()',
        ) -> OverrideCommand:
        r"""
        Overrides rest transparency.

        ..  container:: example

            Makes rests transparent:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.rest_transparent(),
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
                                \override Rest.transparent = ##t                                         %! OC1
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
                                \revert Rest.transparent                                                 %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Makes rests in tuplet 1 transparent:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(baca.rest_transparent(), baca.tuplet(1)),
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
                                \once \override Rest.transparent = ##t                                   %! OC1
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
        return OverrideCommand(
            attribute='transparent',
            value=True,
            grob='rest',
            selector=selector,
            )

    @staticmethod
    def rest_up(
        *,
        selector: Selector = 'baca.rests()',
        ) -> OverrideCommand:
        r"""
        Overrides rest direction.

        ..  container:: example

            Up-overrides rest direction:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rest_up(),
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
                                \override Rest.direction = #up                                           %! OC1
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
                                \revert Rest.direction                                                   %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Up-overrides direction of rests in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(baca.rest_up(), baca.tuplet(1)),
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
                                \once \override Rest.direction = #up                                     %! OC1
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
        return OverrideCommand(
            attribute='direction',
            value=abjad.Up,
            grob='rest',
            selector=selector,
            )

    @staticmethod
    def rests_after(counts: typing.Iterable[int]) -> RestAffixSpecifier:
        r"""
        Makes rests after music.

        ..  container:: example

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_after([2]),
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
                            \times 7/8 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                            \times 2/3 {
                                a'16
                                r8
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return RestAffixSpecifier(
            suffix=counts,
            )

    @staticmethod
    def rests_around(
        prefix: typing.List[int],
        suffix: typing.List[int],
        ) -> RestAffixSpecifier:
        r"""
        Makes rests around music.

        ..  container:: example

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
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
                                ]
                            }
                            \times 2/3 {
                                a'16
                                r8
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return RestAffixSpecifier(
            prefix=prefix,
            suffix=suffix,
            )

    @staticmethod
    def rests_before(counts: typing.List[int]) -> RestAffixSpecifier:
        r"""
        Makes rests before music.

        ..  container:: example

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_before([2]),
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
                            \scaleDurations #'(1 . 1) {
                                a'16
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return RestAffixSpecifier(
            prefix=counts,
            )

    @staticmethod
    def resume() -> AnchorSpecifier:
        """
        Resumes music at next offset across all voices in score.
        """
        return AnchorSpecifier()

    @staticmethod
    def resume_after(remote_voice_name) -> AnchorSpecifier:
        """
        Resumes music after remote selection.
        """
        return AnchorSpecifier(
            remote_selector='baca.leaf(-1)',
            remote_voice_name=remote_voice_name,
            use_remote_stop_offset=True,
            )

    @staticmethod
    def rhythm(
        rhythm_maker: rhythm_maker_typing,
        *,
        division_maker: DivisionMaker = None,
        division_expression: abjad.Expression = None,
        left_broken: bool = None,
        multimeasure_rests: bool = None,
        persist: str = None,
        reference_meters: typing.Iterable[abjad.Meter] = None,
        rewrite_meter: bool = None,
        rewrite_rest_filled: bool = None,
        rhythm_overwrites: typing.List[tuple] = None,
        right_broken: bool = None,
        split_at_measure_boundaries: bool = None,
        stages: typing.Tuple[int, int] = None,
        tie_first: bool = None,
        tie_last: bool = None,
        ) -> RhythmCommand:
        """
        Makes rhythm command.
        """
        return RhythmCommand(
            division_maker=division_maker,
            division_expression=division_expression,
            left_broken=left_broken,
            multimeasure_rests=multimeasure_rests,
            persist=persist,
            reference_meters=reference_meters,
            rewrite_meter=rewrite_meter,
            rewrite_rest_filled=rewrite_rest_filled,
            rhythm_overwrites=rhythm_overwrites,
            rhythm_maker=rhythm_maker,
            right_broken=right_broken,
            split_at_measure_boundaries=split_at_measure_boundaries,
            stages=stages,
            tie_first=tie_first,
            tie_last=tie_last,
            )

    @staticmethod
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
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
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

    @staticmethod
    def scorewide_spacing(
        path: typing.Union[abjad.Path, typing.Tuple[int, int, list]],
        fallback_duration: typing.Tuple[int, int],
        breaks: BreakMeasureMap = None,
        fermata_measure_duration: typing.Tuple[int, int] = (1, 4),
        ) -> HorizontalSpacingSpecifier:
        r"""
        Makes scorewide spacing.

        :param path: path from which first measure number, measure count,
            and fermata measure numbers metadata will be read;
            triple may be passed directly for tests.

        :param fallback_duration: spacing for measures without override.

        :param breaks: break measure map giving beginning-of-line and
            end-of-line measure numbers.

        :param fermata_measure_duration: spacing for measures found in fermata
            measure numbers path metadata.

        ..  container:: example

            >>> breaks = baca.breaks(
            ...     baca.page([1, 15, (10, 20)], [9, 115, (10, 20)])
            ...     )
            >>> spacing = baca.scorewide_spacing(
            ...     (95, 18, [105, 107]),
            ...     breaks=breaks,
            ...     fallback_duration=(1, 20),
            ...     )

            >>> spacing.bol_measure_numbers
            [95, 103]

            >>> spacing.eol_measure_numbers
            [102, 112]

            >>> spacing.fermata_measure_numbers
            [105, 107]

            >>> spacing.first_measure_number
            95

            >>> spacing.last_measure_number
            112

            >>> spacing.measure_count
            18

            >>> len(spacing.measures)
            18

        """
        if isinstance(path, tuple):
            assert len(path) == 3, repr(path)
            first_measure_number, measure_count, fermata_measure_numbers = path
        else:
            path = abjad.Path(path)
            first_measure_number, measure_count, fermata_measure_numbers = \
                path.get_measure_profile_metadata()
            first_measure_number = first_measure_number or 1
        fallback_fraction = abjad.NonreducedFraction(fallback_duration)
        measures = abjad.OrderedDict()
        last_measure_number = first_measure_number + measure_count - 1
        for n in range(first_measure_number, last_measure_number + 1):
            measures[n] = fallback_fraction
        specifier = HorizontalSpacingSpecifier(
            breaks=breaks,
            fermata_measure_duration=fermata_measure_duration,
            fermata_measure_numbers=fermata_measure_numbers,
            first_measure_number=first_measure_number,
            measure_count=measure_count,
            measures=measures,
            )
        specifier._forbid_segment_maker_adjustments = True
        return specifier

    @staticmethod
    def script_color(
        color: str = 'red',
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r"""
        Overrides script color.

        ..  container:: example

            Overrides script color on all leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.accent(selector=baca.pheads()),
            ...     baca.rests_around([2], [4]),
            ...     baca.script_color('red'),
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
                                \override Script.color = #red                                            %! OC1
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
                                \revert Script.color                                                     %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides script color on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.accent(selector=baca.pheads()),
            ...     baca.rests_around([2], [4]),
            ...     baca.map(baca.script_color('red'), baca.tuplet(1)),
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
                                \override Script.color = #red                                            %! OC1
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
                                \revert Script.color                                                     %! OC2
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

        """
        return OverrideCommand(
            attribute='color',
            value=color,
            grob='script',
            selector=selector,
            )

    @staticmethod
    def script_down(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r"""
        Overrides script direction.

        ..  container:: example

            Down-overrides script direction on all leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.accent(selector=baca.pheads()),
            ...     baca.rests_around([2], [4]),
            ...     baca.script_down(),
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
                                \override Script.direction = #down                                       %! OC1
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
                                \revert Script.direction                                                 %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Down-overrides script direction all leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.accent(selector=baca.pheads()),
            ...     baca.rests_around([2], [4]),
            ...     baca.map(baca.script_down(), baca.tuplet(1)),
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
                                \override Script.direction = #down                                       %! OC1
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
                                \revert Script.direction                                                 %! OC2
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

        """
        return OverrideCommand(
            attribute='direction',
            value=abjad.Down,
            grob='script',
            selector=selector,
            )

    @staticmethod
    def script_extra_offset(
        pair: NumberPair,
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        r"""
        Overrides script extra offset.

        ..  container:: example

            Overrides script extra offset on leaf 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.accent(selector=baca.pheads()),
            ...     baca.rests_around([2], [4]),
            ...     baca.script_extra_offset((-1.5, 0), selector=baca.leaf(1)),
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
                                \once \override Script.extra-offset = #'(-1.5 . 0)                       %! OC1
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

            Overrides script extra offset on leaf 0 in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.accent(selector=baca.pheads()),
            ...     baca.rests_around([2], [4]),
            ...     baca.map(
            ...         baca.script_extra_offset((-1.5, 0), selector=baca.leaf(0)),
            ...         baca.tuplet(1),
            ...         ),
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
                                \once \override Script.extra-offset = #'(-1.5 . 0)                       %! OC1
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

        """
        return OverrideCommand(
            attribute='extra_offset',
            value=pair,
            grob='script',
            selector=selector,
            )

    @staticmethod
    def script_padding(
        number: Number,
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        """
        Overrides script padding.
        """
        return OverrideCommand(
            attribute='padding',
            value=number,
            grob='script',
            selector=selector,
            )

    @staticmethod
    def script_staff_padding(
        n: Number,
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        """
        Overrides script staff padding.
        """
        return OverrideCommand(
            attribute='staff_padding',
            value=n,
            grob='script',
            selector=selector,
            )

    @staticmethod
    def script_up(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r"""
        Overrides script direction.

        ..  container:: example

            Up-overrides script direction on all leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.accent(selector=baca.pheads()),
            ...     baca.rests_around([2], [4]),
            ...     baca.script_up(),
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
                                \override Script.direction = #up                                         %! OC1
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
                                \revert Script.direction                                                 %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Up-overrides script direction on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.accent(selector=baca.pheads()),
            ...     baca.rests_around([2], [4]),
            ...     baca.map(baca.script_up(), baca.tuplet(1)),
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
                                \override Script.direction = #up                                         %! OC1
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
                                \revert Script.direction                                                 %! OC2
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

        """
        return OverrideCommand(
            attribute='direction',
            value=abjad.Up,
            grob='script',
            selector=selector,
            )

    @staticmethod
    def shift_clef(
        clef: typing.Union[str, abjad.Clef],
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> SuiteCommand:
        """
        Shifts clef to left by width of clef.
        """
        from .LibraryAF import LibraryAF
        from .LibraryTZ import LibraryTZ
        if isinstance(clef, str):
            clef = abjad.Clef(clef)
        if isinstance(clef, (int, float)):
            extra_offset_x = clef
        else:
            assert isinstance(clef, abjad.Clef)
            width = clef._to_width[clef.name]
            extra_offset_x = -width
        command = LibraryNS.suite(
            LibraryAF.clef_x_extent_false(),
            LibraryAF.clef_extra_offset((extra_offset_x, 0)),
            )
        LibraryTZ.tag(
            abjad.tags.SHIFTED_CLEF,
            command,
            tag_measure_number=True,
            )
        return command

    @staticmethod
    def shift_dynamic(
        dynamic: typing.Union[str, abjad.Dynamic],
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> SuiteCommand:
        """
        Shifts dynamic to left by width of dynamic.
        """
        from .LibraryAF import LibraryAF
        dynamic = abjad.Dynamic(dynamic)
        width = dynamic._to_width[dynamic.name]
        extra_offset_x = -width
        return LibraryNS.suite(
            LibraryAF.dynamic_text_extra_offset((extra_offset_x, 0)),
            LibraryAF.dynamic_text_x_extent_zero(),
            )

    @staticmethod
    def shift_hairpin_start(
        dynamic: typing.Union[str, abjad.Dynamic],
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> SuiteCommand:
        """
        Shifts hairpin start dynamic to left by width of dynamic.
        """
        from .LibraryAF import LibraryAF
        from .LibraryGM import LibraryGM
        dynamic = abjad.Dynamic(dynamic)
        width = dynamic._to_width[dynamic.name]
        extra_offset_x = -width
        hairpin_shorten_left = width - 1.25
        return LibraryNS.suite(
            LibraryAF.dynamic_text_extra_offset((extra_offset_x, 0)),
            LibraryAF.dynamic_text_x_extent_zero(),
            LibraryGM.hairpin_shorten_pair((hairpin_shorten_left, 0)),
            )

    @staticmethod
    def short_fermata(
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        r"""
        Attaches short fermata.

        ..  container:: example

            Attaches short fermata to first leaf:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.short_fermata(),
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
                                -\shortfermata                                                           %! IC
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

            Attaches short fermata to first leaf in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.short_fermata(
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
                                -\shortfermata                                                           %! IC
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
            indicators=[abjad.Articulation('shortfermata')],
            selector=selector,
            )

    @staticmethod
    def skips_after(counts: typing.List[int]) -> RestAffixSpecifier:
        r"""
        Makes skips after music.

        ..  container:: example

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.skips_after([2]),
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
                            \times 7/8 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
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
                            \times 2/3 {
                                a'16
                                s8
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return RestAffixSpecifier(
            skips_instead_of_rests=True,
            suffix=counts,
            )

    @staticmethod
    def skips_around(
        prefix: typing.List[int],
        suffix: typing.List[int],
        ) -> RestAffixSpecifier:
        r"""
        Makes skips around music.

        ..  container:: example

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.skips_around([2], [2]),
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
                                s8
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
                            \times 2/3 {
                                a'16
                                s8
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return RestAffixSpecifier(
            prefix=prefix,
            skips_instead_of_rests=True,
            suffix=suffix,
            )

    @staticmethod
    def skips_before(
        counts: typing.List[int],
        ) -> RestAffixSpecifier:
        r"""
        Makes skips before music.

        ..  container:: example

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.skips_before([2]),
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
                                s8
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
                            \scaleDurations #'(1 . 1) {
                                a'16
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return RestAffixSpecifier(
            prefix=counts,
            skips_instead_of_rests=True,
            )

    @staticmethod
    def slur(
        *,
        selector: Selector = 'baca.tleaves()',
        ) -> SpannerCommand:
        r"""
        Attaches slur.

        ..  container:: example

            Attaches slur to trimmed leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.slur(),
            ...     baca.slur_down(),
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
                                \override Slur.direction = #down                                         %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                r8
                                c'16
                                [
                                (                                                                        %! SC
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
                                )                                                                        %! SC
                                r4
                                \revert Slur.direction                                                   %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Attaches slur to trimmed leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(baca.slur(), baca.tuplet(1)),
            ...     baca.slur_down(),
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
                                \override Slur.direction = #down                                         %! OC1
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
                                (                                                                        %! SC
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
                                )                                                                        %! SC
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert Slur.direction                                                   %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return SpannerCommand(
            selector=selector,
            spanner=abjad.Slur(),
            )

    @staticmethod
    def slur_down(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r"""
        Overrides slur direction.

        ..  container:: example

            Overrides slur direction on leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.slur(),
            ...         baca.tuplets().map(baca.tleaves()).nontrivial(),
            ...         ),
            ...     baca.slur_down(),
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
                                \override Slur.direction = #down                                         %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                r8
                                c'16
                                [
                                (                                                                        %! SC
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                )                                                                        %! SC
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                [
                                (                                                                        %! SC
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
                                )                                                                        %! SC
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert Slur.direction                                                   %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides slur direction leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.slur(),
            ...         baca.tuplets().map(baca.tleaves()).nontrivial(),
            ...         ),
            ...     baca.map(baca.slur_down(), baca.tuplet(1)),
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
                                (                                                                        %! SC
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                )                                                                        %! SC
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override Slur.direction = #down                                         %! OC1
                                fs''16
                                [
                                (                                                                        %! SC
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
                                )                                                                        %! SC
                                \revert Slur.direction                                                   %! OC2
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
        return OverrideCommand(
            attribute='direction',
            value=abjad.Down,
            grob='slur',
            selector=selector,
            )

    @staticmethod
    def slur_up(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r"""
        Overrides slur direction.

        ..  container:: example

            Up-overrides slur direction on leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.slur(),
            ...         baca.tuplets().map(baca.tleaves()).nontrivial(),
            ...         ),
            ...     baca.slur_up(),
            ...     baca.stem_down(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     baca.tuplet_bracket_down(),
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
                                \override Slur.direction = #up                                           %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                \override TupletBracket.direction = #down                                %! OC1
                                r8
                                \override Stem.direction = #down                                         %! OC1
                                c'16
                                [
                                (                                                                        %! SC
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                )                                                                        %! SC
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                fs''16
                                [
                                (                                                                        %! SC
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
                                )                                                                        %! SC
                            }
                            \times 4/5 {
                                a'16
                                \revert Stem.direction                                                   %! OC2
                                r4
                                \revert Slur.direction                                                   %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                                \revert TupletBracket.direction                                          %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Up-overrides slur direction for leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.slur(),
            ...         baca.tuplets().map(baca.tleaves()).nontrivial(),
            ...         ),
            ...     baca.map(baca.slur_up(), baca.tuplet(1)),
            ...     baca.stem_down(),
            ...     baca.rests_around([2], [4]),
            ...     baca.tuplet_bracket_staff_padding(5),
            ...     baca.tuplet_bracket_down(),
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
                                \override TupletBracket.direction = #down                                %! OC1
                                r8
                                \override Stem.direction = #down                                         %! OC1
                                c'16
                                [
                                (                                                                        %! SC
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                )                                                                        %! SC
                                r16
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override Slur.direction = #up                                           %! OC1
                                fs''16
                                [
                                (                                                                        %! SC
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
                                )                                                                        %! SC
                                \revert Slur.direction                                                   %! OC2
                            }
                            \times 4/5 {
                                a'16
                                \revert Stem.direction                                                   %! OC2
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                                \revert TupletBracket.direction                                          %! OC2
                            }
                        }
                    }
                >>

        """
        return OverrideCommand(
            attribute='direction',
            value=abjad.Up,
            grob='slur',
            selector=selector,
            )

    @staticmethod
    def soprano_to_octave(
        n: int,
        *,
        selector: Selector = 'baca.plts()',
        ) -> RegisterToOctaveCommand:
        r"""
        Octave-transposes music.

        ..  container:: example

            Octave-transposes music such that the highest note in the
            collection of all PLTs appears in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.color(selector=baca.plts().group()),
            ...     baca.soprano_to_octave(3),
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
                                <c,, d,, bf,,>8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <c,, d,, bf,,>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                f,8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                f,32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <ef, e, fs>8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <ef, e, fs>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <g,, af,>8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                <g,, af,>32
                                ]
                                r16.
                            }
                            \scaleDurations #'(1 . 1) {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a,,8
                                ~
                                [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a,,32
                                ]
                                r16.
                            }
                        }
                    }
                >>

        ..  container:: example

            Octave-transposes music that such that the highest note in each
            pitched logical tie appears in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.map(baca.soprano_to_octave(3), baca.plts()),
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
                                <ef, e, fs>8
                                ~
                                [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                <ef, e, fs>32
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

            Octave-transposes music that such that the highest note in each
            of the last two PLTs appears in octave 3:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [{0, 2, 10}, [17], {15, 16, 30}, {7, 20}, [9]],
            ...     baca.map(baca.soprano_to_octave(3), baca.plts()[-2:]),
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
            anchor=abjad.Up,
            octave_number=n,
            selector=selector,
            )

    @staticmethod
    def span_bar_color(
        color: str,
        *,
        after: bool = None,
        context: str = 'Score',
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        """
        Overrides span bar color.
        """
        return OverrideCommand(
            after=after,
            attribute='color',
            value=color,
            context=context,
            grob='span_bar',
            selector=selector,
            )

    @staticmethod
    def span_bar_extra_offset(
        pair: NumberPair,
        *,
        after: bool = None,
        context: str = 'Score',
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        """
        Overrides span bar extra offset.
        """
        return OverrideCommand(
            after=after,
            attribute='extra_offset',
            value=pair,
            context=context,
            grob='span_bar',
            selector=selector,
            )

    @staticmethod
    def span_bar_transparent(
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        r"""
        Overrides span bar transparency.

        ..  container:: example

            Makes span bar before leaf 0 transparent:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.span_bar_transparent(),
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
                                \once \override Score.SpanBar.transparent = ##t                          %! OC1
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
                >>

        """
        return OverrideCommand(
            attribute='transparent',
            value=True,
            context='Score',
            grob='span_bar',
            selector=selector,
            )

    @staticmethod
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

    @staticmethod
    def staccatissimo(
        *,
        selector: Selector = 'baca.phead(0)',
        ) -> IndicatorCommand:
        r"""
        Attaches staccatissimo.

        ..  container:: example

            Attaches staccatissimo to pitched head 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.staccatissimo(),
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
                                -\staccatissimo                                                          %! IC
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

            Attaches staccatissimo to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.staccatissimo(selector=baca.pheads()),
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
                                -\staccatissimo                                                          %! IC
                                [
                                e''16
                                -\staccatissimo                                                          %! IC
                                ]
                                ef''4
                                -\staccatissimo                                                          %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\staccatissimo                                                          %! IC
                                [
                                g''16
                                -\staccatissimo                                                          %! IC
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
            indicators=[abjad.Articulation('staccatissimo')],
            selector=selector,
            )

    @staticmethod
    def staccato(
        *,
        selector: Selector = 'baca.phead(0)',
        ) -> IndicatorCommand:
        r"""
        Attaches staccato.

        ..  container:: example

            Attaches staccato to pitched head 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.staccato(),
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
                                -\staccato                                                               %! IC
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

            Attaches staccato to pitched heads in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(
            ...         baca.staccato(selector=baca.pheads()),
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
                                -\staccato                                                               %! IC
                                [
                                e''16
                                -\staccato                                                               %! IC
                                ]
                                ef''4
                                -\staccato                                                               %! IC
                                ~
                                ef''16
                                r16
                                af''16
                                -\staccato                                                               %! IC
                                [
                                g''16
                                -\staccato                                                               %! IC
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
            indicators=[abjad.Articulation('staccato')],
            selector=selector,
            )

    @staticmethod
    def staff_lines(
        n: int,
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        r"""
        Makes staff line command.

        ..  container:: example

            Single-line staff with percussion clef:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.clef('percussion'),
            ...     baca.make_notes(),
            ...     baca.staff_lines(1),
            ...     baca.staff_positions([-2, -1, 0, 1, 2]),
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
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 5]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
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
                                \stopStaff                                                               %! SM8:EXPLICIT_STAFF_LINES:IC
                                \once \override Staff.StaffSymbol.line-count = 1                         %! SM8:EXPLICIT_STAFF_LINES:IC
                                \startStaff                                                              %! SM8:EXPLICIT_STAFF_LINES:IC
                                \clef "percussion"                                                       %! SM8:EXPLICIT_CLEF:IC
                                \once \override Staff.Clef.color = #(x11-color 'blue)                    %! SM6:EXPLICIT_CLEF_COLOR:IC
                            %@% \override Staff.Clef.color = ##f                                         %! SM7:EXPLICIT_CLEF_COLOR_CANCELLATION:IC
                                \set Staff.forceClef = ##t                                               %! SM8:EXPLICIT_CLEF:SM33:IC
                                \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! SM6:EXPLICIT_STAFF_LINES_COLOR:IC
                                a4.
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! SM6:EXPLICIT_CLEF_REDRAW_COLOR:IC
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                b4.
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                d'4.
                <BLANKLINE>
                                % [MusicVoice measure 5]                                                 %! SM4
                                e'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>


            Single-line staff with bass clef:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.clef('bass'),
            ...     baca.make_notes(),
            ...     baca.staff_lines(1),
            ...     baca.staff_positions([-2, -1, 0, 1, 2]),
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
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 5]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
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
                                \stopStaff                                                               %! SM8:EXPLICIT_STAFF_LINES:IC
                                \once \override Staff.StaffSymbol.line-count = 1                         %! SM8:EXPLICIT_STAFF_LINES:IC
                                \startStaff                                                              %! SM8:EXPLICIT_STAFF_LINES:IC
                                \clef "bass"                                                             %! SM8:EXPLICIT_CLEF:IC
                                \once \override Staff.Clef.color = #(x11-color 'blue)                    %! SM6:EXPLICIT_CLEF_COLOR:IC
                            %@% \override Staff.Clef.color = ##f                                         %! SM7:EXPLICIT_CLEF_COLOR_CANCELLATION:IC
                                \set Staff.forceClef = ##t                                               %! SM8:EXPLICIT_CLEF:SM33:IC
                                \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! SM6:EXPLICIT_STAFF_LINES_COLOR:IC
                                b,4.
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! SM6:EXPLICIT_CLEF_REDRAW_COLOR:IC
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c4.
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                d4.
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                e4.
                <BLANKLINE>
                                % [MusicVoice measure 5]                                                 %! SM4
                                f4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            Two-line staff with percussion clef:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.clef('percussion'),
            ...     baca.make_notes(),
            ...     baca.staff_lines(2),
            ...     baca.staff_positions([-2, -1, 0, 1, 2]),
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
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 5]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
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
                                \stopStaff                                                               %! SM8:EXPLICIT_STAFF_LINES:IC
                                \once \override Staff.StaffSymbol.line-count = 2                         %! SM8:EXPLICIT_STAFF_LINES:IC
                                \startStaff                                                              %! SM8:EXPLICIT_STAFF_LINES:IC
                                \clef "percussion"                                                       %! SM8:EXPLICIT_CLEF:IC
                                \once \override Staff.Clef.color = #(x11-color 'blue)                    %! SM6:EXPLICIT_CLEF_COLOR:IC
                            %@% \override Staff.Clef.color = ##f                                         %! SM7:EXPLICIT_CLEF_COLOR_CANCELLATION:IC
                                \set Staff.forceClef = ##t                                               %! SM8:EXPLICIT_CLEF:SM33:IC
                                \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! SM6:EXPLICIT_STAFF_LINES_COLOR:IC
                                a4.
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! SM6:EXPLICIT_CLEF_REDRAW_COLOR:IC
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                b4.
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                c'4.
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                d'4.
                <BLANKLINE>
                                % [MusicVoice measure 5]                                                 %! SM4
                                e'4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

            Two-line staff with bass clef:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.clef('bass'),
            ...     baca.make_notes(),
            ...     baca.staff_lines(2),
            ...     baca.staff_positions([-2, -1, 0, 1, 2]),
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
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 5]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
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
                                \stopStaff                                                               %! SM8:EXPLICIT_STAFF_LINES:IC
                                \once \override Staff.StaffSymbol.line-count = 2                         %! SM8:EXPLICIT_STAFF_LINES:IC
                                \startStaff                                                              %! SM8:EXPLICIT_STAFF_LINES:IC
                                \clef "bass"                                                             %! SM8:EXPLICIT_CLEF:IC
                                \once \override Staff.Clef.color = #(x11-color 'blue)                    %! SM6:EXPLICIT_CLEF_COLOR:IC
                            %@% \override Staff.Clef.color = ##f                                         %! SM7:EXPLICIT_CLEF_COLOR_CANCELLATION:IC
                                \set Staff.forceClef = ##t                                               %! SM8:EXPLICIT_CLEF:SM33:IC
                                \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! SM6:EXPLICIT_STAFF_LINES_COLOR:IC
                                b,4.
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! SM6:EXPLICIT_CLEF_REDRAW_COLOR:IC
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                c4.
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                d4.
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                e4.
                <BLANKLINE>
                                % [MusicVoice measure 5]                                                 %! SM4
                                f4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        ..  container:: example

            ..  note:: It is currently necessary to make sure that clef
                commands precede staff position commands. Otherwise output like
                the following can result:

            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     spacing=baca.minimum_duration((1, 12)),
            ...     time_signatures=[(3, 8), (3, 8), (3, 8), (3, 8), (3, 8)],
            ...     )

            >>> maker(
            ...     'MusicVoice',
            ...     baca.make_notes(),
            ...     baca.staff_lines(2),
            ...     baca.suite(
            ...         baca.staff_positions([-2, -1, 0, 1, 2]),
            ...         baca.clef('bass'),
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
                            \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                            \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 2]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 3]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 4]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                            s1 * 3/8
                <BLANKLINE>
                            % [GlobalSkips measure 5]                                                    %! SM4
                            \newSpacingSection                                                           %! HSS1:SPACING
                            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! HSS1:SPACING
                            \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)          %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
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
                                \stopStaff                                                               %! SM8:EXPLICIT_STAFF_LINES:IC
                                \once \override Staff.StaffSymbol.line-count = 2                         %! SM8:EXPLICIT_STAFF_LINES:IC
                                \startStaff                                                              %! SM8:EXPLICIT_STAFF_LINES:IC
                                \clef "bass"                                                             %! SM8:EXPLICIT_CLEF:IC
                                \once \override Staff.StaffSymbol.color = #(x11-color 'blue)             %! SM6:EXPLICIT_STAFF_LINES_COLOR:IC
                                \once \override Staff.Clef.color = #(x11-color 'blue)                    %! SM6:EXPLICIT_CLEF_COLOR:IC
                            %@% \override Staff.Clef.color = ##f                                         %! SM7:EXPLICIT_CLEF_COLOR_CANCELLATION:IC
                                \set Staff.forceClef = ##t                                               %! SM8:EXPLICIT_CLEF:SM33:IC
                                g'4.
                                \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)                  %! SM6:EXPLICIT_CLEF_REDRAW_COLOR:IC
                <BLANKLINE>
                                % [MusicVoice measure 2]                                                 %! SM4
                                a'4.
                <BLANKLINE>
                                % [MusicVoice measure 3]                                                 %! SM4
                                b'4.
                <BLANKLINE>
                                % [MusicVoice measure 4]                                                 %! SM4
                                c''4.
                <BLANKLINE>
                                % [MusicVoice measure 5]                                                 %! SM4
                                d''4.
                <BLANKLINE>
                            }
                        }
                    >>
                >>

        """
        return IndicatorCommand(
            indicators=[StaffLines(line_count=n)],
            selector=selector,
            )

    @staticmethod
    def staff_position(
        number: int,
        *,
        selector: Selector = 'baca.plts()',
        ) -> StaffPositionCommand:
        """
        Makes staff position command; allows repeats.
        """
        assert isinstance(number, int), repr(number)
        return StaffPositionCommand(
            allow_repeats=True,
            numbers=[number],
            selector=selector,
            ) 

    @staticmethod
    def staff_positions(
        numbers,
        *,
        allow_repeats: bool = None,
        exact: bool = None,
        selector: Selector = 'baca.plts()',
        ) -> StaffPositionCommand:
        """
        Makes staff position command; does not allow repeats.
        """
        if allow_repeats is None and len(numbers) == 1:
            allow_repeats = True
        return StaffPositionCommand(
            allow_repeats=allow_repeats,
            exact=exact,
            numbers=numbers,
            selector=selector,
            ) 

    @staticmethod
    def start_markup(
        argument: str,
        *,
        context: str = 'Staff',
        hcenter_in: Number = None,
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        """
        Attaches start markup.
        """
        if isinstance(argument, (list, str)):
            markup = MarkupLibrary.instrument(argument, hcenter_in=hcenter_in)
            start_markup = abjad.StartMarkup(
                context=context,
                markup=markup,
                )
        elif isinstance(argument, abjad.Markup):
            markup = abjad.Markup(argument)
            start_markup = abjad.StartMarkup(
                context=context,
                markup=markup,
                )
        elif isinstance(argument, abjad.StartMarkup):
            start_markup = abjad.new(
                argument,
                context=context,
                )
        else:
            raise TypeError(argument)
        assert isinstance(start_markup, abjad.StartMarkup)
        command = IndicatorCommand(
            indicators=[start_markup],
            selector=selector,
            tags=[abjad.Tag('STMK'), abjad.Tag('-PARTS')],
            )
        return command

    @staticmethod
    def stem_color(
        color: str = 'red',
        *,
        context: str = None,
        selector: Selector = 'baca.tleaves()',
        ) -> OverrideCommand:
        r"""
        Overrides stem color.

        ..  container:: example

            Overrides stem color on pitched leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.stem_color(color='red'),
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
                                \override Stem.color = #red                                              %! OC1
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
                                \revert Stem.color                                                       %! OC2
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides stem color on pitched leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.map(baca.stem_color('red'), baca.tuplet(1)),
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
                                \override Stem.color = #red                                              %! OC1
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
                                \revert Stem.color                                                       %! OC2
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
        return OverrideCommand(
            attribute='color',
            value=color,
            context=context,
            grob='stem',
            selector=selector,
            )

    @staticmethod
    def stem_down(
        *,
        selector: Selector = 'baca.tleaves()',
        ) -> OverrideCommand:
        r"""
        Overrides stem direction.

        ..  container:: example

            Down-overrides stem direction pitched leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.stem_down(),
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
                                \override Stem.direction = #down                                         %! OC1
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
                                \revert Stem.direction                                                   %! OC2
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Down-overrides stem direction for leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(baca.stem_down(), baca.tuplet(1)),
            ...     baca.stem_up(),
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
                                \override Stem.direction = #up                                           %! OC1
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
                                \override Stem.direction = #down                                         %! OC1
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
                                \revert Stem.direction                                                   %! OC2
                            }
                            \times 4/5 {
                                a'16
                                \revert Stem.direction                                                   %! OC2
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return OverrideCommand(
            attribute='direction',
            value=abjad.Down,
            grob='stem',
            selector=selector,
            )

    @staticmethod
    def stem_stencil_false(
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> OverrideCommand:
        """
        Overrides stem stencil.
        """
        return OverrideCommand(
            attribute='stencil',
            grob='stem',
            selector=selector,
            value=False,
            )

    @staticmethod
    def stem_transparent(
        *,
        selector: Selector = 'baca.leaves()',
        ):
        """
        Overrides stem transparency.
        """
        return OverrideCommand(
            attribute='transparent',
            value=True,
            grob='stem',
            selector=selector,
            )

    @staticmethod
    def stem_tremolo(
        *,
        selector: Selector = 'baca.pleaf(0)',
        tremolo_flags:int = 32,
        ) -> IndicatorCommand:
        r"""
        Attaches stem tremolo.

        ..  container:: example

            Attaches stem tremolo to pitched leaf 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.stem_tremolo(),
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
                                :32                                                                      %! IC
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

            Attaches stem tremolo to pitched leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(
            ...         baca.stem_tremolo(selector=baca.pleaves()),
            ...         baca.tuplet(1),
            ...         ),
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
                                :32                                                                      %! IC
                                [
                                e''16
                                :32                                                                      %! IC
                                ]
                                ef''4
                                :32                                                                      %! IC
                                ~
                                ef''16
                                :32                                                                      %! IC
                                r16
                                af''16
                                :32                                                                      %! IC
                                [
                                g''16
                                :32                                                                      %! IC
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
            indicators=[abjad.StemTremolo(tremolo_flags=tremolo_flags)],
            selector=selector,
            )

    @staticmethod
    def stem_up(
        *,
        selector: Selector = 'baca.tleaves()',
        ) -> OverrideCommand:
        r"""
        Overrides stem direction.

        ..  container:: example

            Up-overrides stem direction on pitched leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 2',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.stem_up(),
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
                    \context Voice = "Voice 2"
                    {
                        \voiceTwo
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                r8
                                \override Stem.direction = #up                                           %! OC1
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
                                \revert Stem.direction                                                   %! OC2
                                r4
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Up-overrides stem direction on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 2',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [10]],
            ...     baca.rests_around([2], [4]),
            ...     baca.stem_down(),
            ...     baca.map(baca.stem_up(), baca.tuplet(1)),
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
                    \context Voice = "Voice 2"
                    {
                        \voiceTwo
                        {
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                r8
                                \override Stem.direction = #down                                         %! OC1
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
                                \override Stem.direction = #up                                           %! OC1
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
                                \revert Stem.direction                                                   %! OC2
                            }
                            \times 4/5 {
                                bf'16
                                \revert Stem.direction                                                   %! OC2
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
            grob='stem',
            selector=selector,
            )

    @staticmethod
    def stop_trill(
        *,
        selector: Selector = 'baca.leaf(0)',
        ) -> IndicatorCommand:
        """
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
        from .LibraryGM import LibraryGM
        return LibraryGM.literal(
            r'\stopTrillSpan',
            format_slot='closing',
            selector=selector,
            )

    @staticmethod
    def stopped(
        *,
        selector: Selector = 'baca.phead(0)',
        ) -> IndicatorCommand:
        r"""
        Attaches stopped +-sign.

        ..  container:: example

            Attaches stopped +-sign to pitched head 0:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.stopped(),
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
                                -\stopped                                                                %! IC
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

        """
        return IndicatorCommand(
            indicators=[abjad.Articulation('stopped')],
            selector=selector,
            )

    @staticmethod
    def strict_note_spacing_off(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r"""
        Overrides spacing spanner strict note spacing.

        ..  container:: example

            Turns strict note spacing off on leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.strict_note_spacing_off(),
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
                                \override Score.SpacingSpanner.strict-note-spacing = ##f                 %! OC1
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
                                \revert Score.SpacingSpanner.strict-note-spacing                         %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return OverrideCommand(
            attribute='strict_note_spacing',
            value=False,
            context='Score',
            grob='spacing_spanner',
            selector=selector,
            )

    @staticmethod
    def strict_quarter_divisions() -> DivisionSequenceExpression:
        """
        Makes strict quarter divisions.

        ..  container:: example

            >>> expression = baca.strict_quarter_divisions()
            >>> for item in expression([(2, 4), (2, 4)]):
            ...     item
            ...
            Division((1, 4))
            Division((1, 4))
            Division((1, 4))
            Division((1, 4))

        """
        expression = DivisionSequenceExpression()
        expression = expression.division_sequence()
        expression = expression.split_by_durations(
            durations=[abjad.Duration(1, 4)]
            )
        expression = expression.sequence()
        expression = expression.flatten(depth=-1)
        return expression

    @staticmethod
    def subito_dynamic(
        dynamic: str,
        *,
        selector: Selector = 'baca.phead(0)',
        ) -> IndicatorCommand:
        """
        Attaches subito dynamic.
        """
        command = rf'\{dynamic}_sub'
        indicator = abjad.Dynamic(dynamic, command=command)
        return IndicatorCommand(
            indicators=[indicator],
            selector=selector,
            )

    @staticmethod
    def suite(
        *commands: typing.Sequence[Command],
        selector: Selector = None,
        ) -> SuiteCommand:
        """
        Makes suite.

        ..  container:: example

            Raises exception on noncommand:

            >>> baca.suite(['Allegro'])
            Traceback (most recent call last):
                ...
            Exception:
              Commands must contain only commands.
              Not list: ['Allegro'].

        """
        for command in commands:
            if not isinstance(command, Command):
                message = '\n  Commands must contain only commands.'
                message += f'\n  Not {type(command).__name__}: {command!r}.'
                raise Exception(message)
        if not isinstance(selector, (str, abjad.Expression, type(None))):
            message = f'\n  Must be selector, string or none:'
            message += f'\n  Not {selector!r}.'
            raise Exception(message)
        return SuiteCommand(*commands, selector=selector)

    @staticmethod
    def sustain_pedal(
        *,
        selector: Selector = 'baca.leaves()',
        ) -> SpannerCommand:
        r"""
        Attaches sustain pedal.

        ..  container:: example

            Pedals leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.sustain_pedal(),
            ...     baca.sustain_pedal_staff_padding(4),
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
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                r8
                                \sustainOn                                                               %! SC
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
                                \sustainOff                                                              %! SC
                                \revert Staff.SustainPedalLineSpanner.staff-padding                      %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Pedals leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(baca.sustain_pedal(), baca.tuplet(1)),
            ...     baca.sustain_pedal_staff_padding(4),
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
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! OC1
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
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                fs''16
                                [
                                \sustainOn                                                               %! SC
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
                                \sustainOff                                                              %! SC
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert Staff.SustainPedalLineSpanner.staff-padding                      %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Pedals leaves in tuplet 1 (leaked to the left):

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(
            ...         baca.sustain_pedal(selector=baca.lleaves()),
            ...         baca.tuplet(1),
            ...         ),
            ...     baca.sustain_pedal_staff_padding(4),
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
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                r8
                                c'16
                                [
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                r16
                                \sustainOn                                                               %! SC
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
                                \sustainOff                                                              %! SC
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \revert Staff.SustainPedalLineSpanner.staff-padding                      %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Pedals leaves in tuplet 1 (leaked to the right):

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(
            ...         baca.sustain_pedal(selector=baca.rleaves()),
            ...         baca.tuplet(1),
            ...         ),
            ...     baca.sustain_pedal_staff_padding(4),
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
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! OC1
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
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                fs''16
                                [
                                \sustainOn                                                               %! SC
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
                                \sustainOff                                                              %! SC
                                r4
                                \revert Staff.SustainPedalLineSpanner.staff-padding                      %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Pedals leaves in tuplet 1 (leaked wide):

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(
            ...         baca.sustain_pedal(selector=baca.wleaves()),
            ...         baca.tuplet(1),
            ...         ),
            ...     baca.sustain_pedal_staff_padding(4),
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
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                r8
                                c'16
                                [
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                r16
                                \sustainOn                                                               %! SC
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
                                \sustainOff                                                              %! SC
                                r4
                                \revert Staff.SustainPedalLineSpanner.staff-padding                      %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Pedals leaves in tuplets:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(baca.sustain_pedal(), baca.tuplets()),
            ...     baca.sustain_pedal_staff_padding(4),
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
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                r8
                                \sustainOn                                                               %! SC
                                c'16
                                [
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                                \sustainOff                                                              %! SC
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                fs''16
                                [
                                \sustainOn                                                               %! SC
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
                                \sustainOff                                                              %! SC
                            }
                            \times 4/5 {
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                a'16
                                \sustainOn                                                               %! SC
                                r4
                                \sustainOff                                                              %! SC
                                \revert Staff.SustainPedalLineSpanner.staff-padding                      %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Pedals leaves in tuplets (leaked to the left):

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(
            ...         baca.sustain_pedal(selector=baca.lleaves()),
            ...         baca.tuplets(),
            ...         ),
            ...     baca.sustain_pedal_staff_padding(4),
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
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                r8
                                \sustainOn                                                               %! SC
                                c'16
                                [
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                r16
                                \sustainOff                                                              %! SC
                                \sustainOn                                                               %! SC
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
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                g''16
                                ]
                                \sustainOff                                                              %! SC
                                \sustainOn                                                               %! SC
                            }
                            \times 4/5 {
                                a'16
                                r4
                                \sustainOff                                                              %! SC
                                \revert Staff.SustainPedalLineSpanner.staff-padding                      %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Pedals leaves in tuplets (leaked to the right):

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(
            ...         baca.sustain_pedal(selector=baca.rleaves()),
            ...         baca.tuplets(),
            ...         ),
            ...     baca.sustain_pedal_staff_padding(4),
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
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                r8
                                \sustainOn                                                               %! SC
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
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                fs''16
                                \sustainOff                                                              %! SC
                                [
                                \sustainOn                                                               %! SC
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
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                a'16
                                \sustainOff                                                              %! SC
                                \sustainOn                                                               %! SC
                                r4
                                \sustainOff                                                              %! SC
                                \revert Staff.SustainPedalLineSpanner.staff-padding                      %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return SpannerCommand(
            selector=selector,
            spanner=abjad.PianoPedalSpanner(style='bracket'),
            )

    @staticmethod
    def sustain_pedal_staff_padding(
        n: Number,
        *,
        context: str = 'Staff',
        selector: Selector = 'baca.leaves()',
        ) -> OverrideCommand:
        r"""
        Overrides sustain pedal staff padding.

        ..  container:: example

            Overrides sustain pedal staff padding on leaves:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(
            ...         baca.sustain_pedal(selector=baca.rleaves()),
            ...         baca.tuplets(),
            ...         ),
            ...     baca.sustain_pedal_staff_padding(4),
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
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! OC1
                                \override TupletBracket.staff-padding = #5                               %! OC1
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                r8
                                \sustainOn                                                               %! SC
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
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                fs''16
                                \sustainOff                                                              %! SC
                                [
                                \sustainOn                                                               %! SC
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
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                a'16
                                \sustainOff                                                              %! SC
                                \sustainOn                                                               %! SC
                                r4
                                \sustainOff                                                              %! SC
                                \revert Staff.SustainPedalLineSpanner.staff-padding                      %! OC2
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        ..  container:: example

            Overrides sustain pedal staff padding on leaves in tuplet 1:

            >>> music_maker = baca.MusicMaker()
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     [[0, 2, 10], [18, 16, 15, 20, 19], [9]],
            ...     baca.rests_around([2], [4]),
            ...     baca.map(baca.sustain_pedal(), baca.tuplets()),
            ...     baca.map(
            ...         baca.sustain_pedal_staff_padding(4),
            ...         baca.tuplet(1),
            ...         ),
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
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                r8
                                \sustainOn                                                               %! SC
                                c'16
                                [
                                d'16
                                ]
                                bf'4
                                ~
                                bf'16
                                r16
                                \sustainOff                                                              %! SC
                            }
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 9/10 {
                                \override Staff.SustainPedalLineSpanner.staff-padding = #4               %! OC1
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                fs''16
                                [
                                \sustainOn                                                               %! SC
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
                                \sustainOff                                                              %! SC
                                \revert Staff.SustainPedalLineSpanner.staff-padding                      %! OC2
                            }
                            \times 4/5 {
                                \set Staff.pedalSustainStyle = #'bracket                                 %! SC
                                a'16
                                \sustainOn                                                               %! SC
                                r4
                                \sustainOff                                                              %! SC
                                \revert TupletBracket.staff-padding                                      %! OC2
                            }
                        }
                    }
                >>

        """
        return OverrideCommand(
            attribute='staff_padding',
            value=n,
            context=context,
            grob='sustain_pedal_line_spanner',
            selector=selector,
            )

    @staticmethod
    def swell(
        peak: str,
        counts: typing.List[int],
        *,
        selector: Selector = 'baca.leaves()',
        spanner_selector: typing.Union[MapCommand, Selector] = 'baca.leaves()',
        ) -> PiecewiseCommand:
        """
        Makes two-stage niente swell.
        """
        from .LibraryAF import LibraryAF
        from .LibraryGM import LibraryGM
        assert isinstance(peak, str), repr(peak)
        assert isinstance(counts, list), repr(counts)
        assert all(isinstance(_, int) for _ in counts), repr(counts)
        if isinstance(selector, str):
            selector = eval(selector)
        assert isinstance(selector, abjad.Expression), repr(selector)
        selector = selector.enchain(counts)
        return LibraryAF.enchained_hairpin(
            *LibraryGM.make_dynamics(f'niente {peak} niente'),
            bookend=True,
            selector=selector,
            spanner_selector=spanner_selector,
            )

    @staticmethod
    def system(
        *distances: typing.Any,
        measure: int = None,
        y_offset: Number = None
        ) -> SystemSpecifier:
        """
        Makes system specifier.
        """
        distances_ = baca.sequence(distances).flatten()
        return SystemSpecifier(
            distances=distances_,
            measure=measure,
            y_offset=y_offset,
            )
