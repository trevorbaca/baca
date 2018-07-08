import abjad
import collections
import typing
from . import indicatorlib
from . import library
from . import markuplib
from . import typings
from abjadext import rmakers
from .AnchorSpecifier import AnchorSpecifier
from .ClusterCommand import ClusterCommand
from .Command import Command
from .Command import Map
from .Command import Suite
from .ContainerCommand import ContainerCommand
from .IndicatorCommand import IndicatorCommand
from .NestingCommand import NestingCommand
from .PartAssignmentCommand import PartAssignmentCommand
from .PitchCommand import PitchCommand
from .RestAffixSpecifier import RestAffixSpecifier
from .Scope import Scope
from .Selection import Selection
from .Selection import _select
from .Sequence import Sequence
from .StaffPositionCommand import StaffPositionCommand
from .TieCorrectionCommand import TieCorrectionCommand


__documentation_section__ = '(1) Library'

def natural_clusters(
    widths: typing.Iterable[int],
    *,
    selector: typings.Selector = 'baca.plts()',
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

def one_voice(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    """
    Makes LilyPond ``\oneVoice`` command.
    """
    literal = abjad.LilyPondLiteral(r'\oneVoice')
    return IndicatorCommand(
        indicators=[literal],
        selector=selector,
        )

def parts(
    part_assignment: abjad.PartAssignment,
    *,
    selector: typings.Selector = 'baca.leaves()',
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
                                \clef "treble"                                                   %! SM8:DEFAULT_CLEF:ST3
                                \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                            %@% \override ViolinMusicStaff.Clef.color = ##f                      %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                \set ViolinMusicStaff.forceClef = ##t                            %! SM8:DEFAULT_CLEF:SM33:ST3
                                e'2
                                ^ \markup {                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \with-color                                                  %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        #(x11-color 'DarkViolet)                                 %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        (Violin)                                                 %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    }                                                            %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
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
                            \clef "alto"                                                         %! SM8:DEFAULT_CLEF:ST3
                            \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                        %@% \override ViolaMusicStaff.Clef.color = ##f                           %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                            \set ViolaMusicStaff.forceClef = ##t                                 %! SM8:DEFAULT_CLEF:SM33:ST3
                            R1 * 1/2
                            ^ \markup {                                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                \with-color                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    #(x11-color 'DarkViolet)                                     %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    (Viola)                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                }                                                                %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
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
                            \clef "bass"                                                         %! SM8:DEFAULT_CLEF:ST3
                            \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                        %@% \override CelloMusicStaff.Clef.color = ##f                           %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                            \set CelloMusicStaff.forceClef = ##t                                 %! SM8:DEFAULT_CLEF:SM33:ST3
                            R1 * 1/2
                            ^ \markup {                                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                \with-color                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    #(x11-color 'DarkViolet)                                     %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    (Cello)                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                }                                                                %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
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

def pitch(
    pitch,
    *,
    selector: typings.Selector = 'baca.pleaves()',
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

def rehearsal_mark(
    argument: typing.Union[int, str],
    *tweaks: abjad.LilyPondTweakManager,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    """
    Attaches rehearsal mark.
    """
    if isinstance(argument, str):
        mark = abjad.RehearsalMark.from_string(argument)
    else:
        assert isinstance(argument, int)
        mark = abjad.RehearsalMark(number=argument)
    return IndicatorCommand(
        *tweaks,
        indicators=[mark],
        selector=selector,
        )

def repeat_tie_from(
    *,
    selector: typings.Selector = 'baca.pleaf(-1)',
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
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
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

def repeat_tie_to(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
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
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
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

def resume() -> AnchorSpecifier:
    """
    Resumes music at next offset across all voices in score.
    """
    return AnchorSpecifier()

def resume_after(remote_voice_name) -> AnchorSpecifier:
    """
    Resumes music after remote selection.
    """
    return AnchorSpecifier(
        remote_selector='baca.leaf(-1)',
        remote_voice_name=remote_voice_name,
        use_remote_stop_offset=True,
        )

# TODO: move to baca.Selection
def rmleaves(count: int) -> abjad.Expression:
    """
    Selects all leaves in ``count`` measures, leaked one leaf to the right.
    """
    assert isinstance(count, int), repr(count)
    selector = _select().leaves().group_by_measure()
    selector = selector[:count].flatten().rleak()
    return selector

def short_fermata(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
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

def staccatissimo(
    *,
    selector: typings.Selector = 'baca.phead(0)',
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
        ...         baca.tuplet(1),
        ...         baca.staccatissimo(selector=baca.pheads()),
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

def staccato(
    *,
    selector: typings.Selector = 'baca.phead(0)',
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
        ...         baca.tuplet(1),
        ...         baca.staccato(selector=baca.pheads()),
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

def staff_lines(
    n: int,
    *,
    selector: typings.Selector = 'baca.leaf(0)',
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
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
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
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
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
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
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
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
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
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
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
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
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
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
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
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
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
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
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
            <BLANKLINE>
                        % [GlobalSkips measure 5]                                                    %! SM4
                        \baca_new_spacing_section #1 #12                                             %! HSS1:SPACING
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
        indicators=[indicatorlib.StaffLines(line_count=n)],
        selector=selector,
        )

def staff_position(
    number: int,
    *,
    selector: typings.Selector = 'baca.plts()',
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

def staff_positions(
    numbers,
    *,
    allow_repeats: bool = None,
    exact: bool = None,
    selector: typings.Selector = 'baca.plts()',
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

def start_markup(
    argument: str,
    *,
    context: str = 'Staff',
    hcenter_in: typings.Number = None,
    selector: typings.Selector = 'baca.leaf(0)',
    ) -> IndicatorCommand:
    """
    Attaches start markup.
    """
    if isinstance(argument, (list, str)):
        markup = markuplib.instrument(argument, hcenter_in=hcenter_in)
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

def stem_tremolo(
    *,
    selector: typings.Selector = 'baca.pleaf(0)',
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
        ...         baca.tuplet(1),
        ...         baca.stem_tremolo(selector=baca.pleaves()),
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

def stop_trill(
    *,
    selector: typings.Selector = 'baca.leaf(0)',
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
    return library.literal(
        r'\stopTrillSpan',
        format_slot='closing',
        selector=selector,
        )

def stopped(
    *,
    selector: typings.Selector = 'baca.phead(0)',
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
