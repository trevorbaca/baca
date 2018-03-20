import abjad
import baca
import typing
from .BreakMeasureMap import BreakMeasureMap
from .SpacingSection import SpacingSection


class HorizontalSpacingSpecifier(abjad.AbjadObject):
    r'''Horizontal spacing specifier.

    >>> from abjad import rhythmmakertools as rhythmos

    ..  container:: example

        No spacing command:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.pitches('E4 F4'),
        ...     baca.RhythmCommand(
        ...         rhythm_maker=rhythmos.EvenRunRhythmMaker(),
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
                        \time 8/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 2/4                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 1/2                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
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
                                e'16
                                [
            <BLANKLINE>
                                f'16
            <BLANKLINE>
                                e'16
            <BLANKLINE>
                                f'16
            <BLANKLINE>
                                e'16
            <BLANKLINE>
                                f'16
            <BLANKLINE>
                                e'16
            <BLANKLINE>
                                f'16
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 2]                                             %! SM4
                                e'8
                                [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e'8
            <BLANKLINE>
                                f'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 3]                                             %! SM4
                                e'4
            <BLANKLINE>
                                f'4
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 4]                                             %! SM4
                                e'2
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Null spacing command:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.HorizontalSpacingSpecifier(),
        ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.pitches('E4 F4'),
        ...     baca.RhythmCommand(
        ...         rhythm_maker=rhythmos.EvenRunRhythmMaker(),
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
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)             %! HSS1:SPACING
                        \time 8/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 8)              %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 4)              %! HSS1:SPACING
                        \time 2/4                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 2)              %! HSS1:SPACING
                        \time 1/2                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
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
                                e'16
                                [
            <BLANKLINE>
                                f'16
            <BLANKLINE>
                                e'16
            <BLANKLINE>
                                f'16
            <BLANKLINE>
                                e'16
            <BLANKLINE>
                                f'16
            <BLANKLINE>
                                e'16
            <BLANKLINE>
                                f'16
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 2]                                             %! SM4
                                e'8
                                [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e'8
            <BLANKLINE>
                                f'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 3]                                             %! SM4
                                e'4
            <BLANKLINE>
                                f'4
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 4]                                             %! SM4
                                e'2
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Measurewise proportional spacing based on minimum duration per measure:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.HorizontalSpacingSpecifier(
        ...         multiplier=abjad.Multiplier(1),
        ...         ),
        ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.pitches('E4 F4'),
        ...     baca.RhythmCommand(
        ...         rhythm_maker=rhythmos.EvenRunRhythmMaker(),
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
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)             %! HSS1:SPACING
                        \time 8/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 8)              %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 4)              %! HSS1:SPACING
                        \time 2/4                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 2)              %! HSS1:SPACING
                        \time 1/2                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
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
                                e'16
                                [
            <BLANKLINE>
                                f'16
            <BLANKLINE>
                                e'16
            <BLANKLINE>
                                f'16
            <BLANKLINE>
                                e'16
            <BLANKLINE>
                                f'16
            <BLANKLINE>
                                e'16
            <BLANKLINE>
                                f'16
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 2]                                             %! SM4
                                e'8
                                [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e'8
            <BLANKLINE>
                                f'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 3]                                             %! SM4
                                e'4
            <BLANKLINE>
                                f'4
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 4]                                             %! SM4
                                e'2
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Measurewise proportional spacing based on twice the minimum duration
        per measure:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.HorizontalSpacingSpecifier(
        ...         multiplier=abjad.Multiplier(2),
        ...         ),
        ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.pitches('E4 F4'),
        ...     baca.RhythmCommand(
        ...         rhythm_maker=rhythmos.EvenRunRhythmMaker(),
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
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 32)             %! HSS1:SPACING
                        \time 8/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 8)              %! HSS1:SPACING
                        \time 2/4                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 4)              %! HSS1:SPACING
                        \time 1/2                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
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
                                e'16
                                [
            <BLANKLINE>
                                f'16
            <BLANKLINE>
                                e'16
            <BLANKLINE>
                                f'16
            <BLANKLINE>
                                e'16
            <BLANKLINE>
                                f'16
            <BLANKLINE>
                                e'16
            <BLANKLINE>
                                f'16
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 2]                                             %! SM4
                                e'8
                                [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e'8
            <BLANKLINE>
                                f'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 3]                                             %! SM4
                                e'4
            <BLANKLINE>
                                f'4
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 4]                                             %! SM4
                                e'2
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Measurewise proportional spacing based on twice the minimum duration
        per measure with minimum width equal to an eighth note:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.HorizontalSpacingSpecifier(
        ...         multiplier=abjad.Multiplier(2),
        ...         minimum_width=abjad.Duration(1, 8),
        ...         ),
        ...     time_signatures=[(8, 16), (4, 8), (2, 4), (1, 2)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.pitches('E4 F4'),
        ...     baca.RhythmCommand(
        ...         rhythm_maker=rhythmos.EvenRunRhythmMaker(),
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
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 32)             %! HSS1:SPACING
                        \time 8/16                                                                   %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)             %! HSS1:SPACING
                        \time 2/4                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)             %! HSS1:SPACING
                        \time 1/2                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
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
                                e'16
                                [
            <BLANKLINE>
                                f'16
            <BLANKLINE>
                                e'16
            <BLANKLINE>
                                f'16
            <BLANKLINE>
                                e'16
            <BLANKLINE>
                                f'16
            <BLANKLINE>
                                e'16
            <BLANKLINE>
                                f'16
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 2]                                             %! SM4
                                e'8
                                [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e'8
            <BLANKLINE>
                                f'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 3]                                             %! SM4
                                e'4
            <BLANKLINE>
                                f'4
                            }
                            {
            <BLANKLINE>
                                % [MusicVoice measure 4]                                             %! SM4
                                e'2
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Works with accelerando and ritardando figures:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     spacing=baca.HorizontalSpacingSpecifier(
        ...         minimum_width=abjad.Duration(1, 8),
        ...         ),
        ...     time_signatures=[(4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.pitches('E4 F4'),
        ...     baca.RhythmCommand(
        ...         rhythm_maker=rhythmos.AccelerandoRhythmMaker(
        ...             beam_specifier=rhythmos.BeamSpecifier(
        ...             use_feather_beams=True,
        ...                 ),
        ...             interpolation_specifiers=rhythmos.InterpolationSpecifier(
        ...                 start_duration=abjad.Duration(1, 8),
        ...                 stop_duration=abjad.Duration(1, 20),
        ...                 written_duration=abjad.Duration(1, 16),
        ...                 ),
        ...             tuplet_specifier=rhythmos.TupletSpecifier(
        ...                 use_note_duration_bracket=True,
        ...                 ),
        ...             ),
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
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)             %! HSS1:SPACING
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \newSpacingSection                                                           %! HSS1:SPACING
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 16)             %! HSS1:SPACING
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
                            \override TupletNumber.text = \markup {
                                \scale
                                    #'(0.75 . 0.75)
                                    \score
                                        {
                                            \new Score
                                            \with
                                            {
                                                \override SpacingSpanner.spacing-increment = #0.5
                                                proportionalNotationDuration = ##f
                                            }
                                            <<
                                                \new RhythmicStaff
                                                \with
                                                {
                                                    \remove Time_signature_engraver
                                                    \remove Staff_symbol_engraver
                                                    \override Stem.direction = #up
                                                    \override Stem.length = #5
                                                    \override TupletBracket.bracket-visibility = ##t
                                                    \override TupletBracket.direction = #up
                                                    \override TupletBracket.padding = #1.25
                                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                    tupletFullLength = ##t
                                                }
                                                {
                                                    c'2
                                                }
                                            >>
                                            \layout {
                                                indent = #0
                                                ragged-right = ##t
                                            }
                                        }
                                }
                            \times 1/1 {
            <BLANKLINE>
                                % [MusicVoice measure 1]                                             %! SM4
                                \once \override Beam.grow-direction = #right
                                e'16 * 63/32
                                [
            <BLANKLINE>
                                f'16 * 115/64
            <BLANKLINE>
                                e'16 * 91/64
            <BLANKLINE>
                                f'16 * 35/32
            <BLANKLINE>
                                e'16 * 29/32
            <BLANKLINE>
                                f'16 * 13/16
                                ]
                            }
                            \revert TupletNumber.text
                            \override TupletNumber.text = \markup {
                                \scale
                                    #'(0.75 . 0.75)
                                    \score
                                        {
                                            \new Score
                                            \with
                                            {
                                                \override SpacingSpanner.spacing-increment = #0.5
                                                proportionalNotationDuration = ##f
                                            }
                                            <<
                                                \new RhythmicStaff
                                                \with
                                                {
                                                    \remove Time_signature_engraver
                                                    \remove Staff_symbol_engraver
                                                    \override Stem.direction = #up
                                                    \override Stem.length = #5
                                                    \override TupletBracket.bracket-visibility = ##t
                                                    \override TupletBracket.direction = #up
                                                    \override TupletBracket.padding = #1.25
                                                    \override TupletBracket.shorten-pair = #'(-1 . -1.5)
                                                    \override TupletNumber.text = #tuplet-number::calc-fraction-text
                                                    tupletFullLength = ##t
                                                }
                                                {
                                                    c'4.
                                                }
                                            >>
                                            \layout {
                                                indent = #0
                                                ragged-right = ##t
                                            }
                                        }
                                }
                            \times 1/1 {
            <BLANKLINE>
                                % [MusicVoice measure 2]                                             %! SM4
                                \once \override Beam.grow-direction = #right
                                e'16 * 117/64
                                [
            <BLANKLINE>
                                f'16 * 99/64
            <BLANKLINE>
                                e'16 * 69/64
            <BLANKLINE>
                                f'16 * 13/16
            <BLANKLINE>
                                e'16 * 47/64
                                ]
            <BLANKLINE>
                            }
                            \revert TupletNumber.text
                        }
                    }
                >>
            >>

        Minimum duration in each measure is taken from the **nonmultiplied**
        duration of each note.

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(3) Specifiers'

    __slots__ = (
        '_breaks',
        '_fermata_measure_numbers',
        '_fermata_measure_width',
        '_fermata_score',
        '_fermata_start_offsets',
        '_first_measure_number',
        '_forbid_segment_maker_adjustments',
        '_measure_count',
        '_measures',
        '_minimum_width',
        '_multiplier',
        )

    _magic_lilypond_eol_adjustment = abjad.Multiplier(35, 24)

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        breaks=None,
        fermata_measure_width=None,
        fermata_score=None,
        first_measure_number=None,
        measure_count=None,
        measures=None,
        minimum_width=None,
        multiplier=None,
        ):
        if breaks is not None:
            prototype = BreakMeasureMap
            assert isinstance(breaks, prototype), repr(breaks)
        self._breaks = breaks
        self._fermata_measure_numbers = []
        if fermata_measure_width is not None:
            fermata_measure_width = abjad.Duration(fermata_measure_width)
        self._fermata_measure_width = fermata_measure_width
        if fermata_score is not None:
            assert isinstance(fermata_score, str), repr(fermata_score)
        self._fermata_score = fermata_score
        self._fermata_start_offsets = []
        if first_measure_number is not None:
            assert isinstance(first_measure_number, int)
            assert 1 <= first_measure_number
        self._first_measure_number = first_measure_number
        self._forbid_segment_maker_adjustments = None
        if measure_count is not None:
            assert isinstance(measure_count, int)
            assert 0 <= measure_count
        self._measure_count = measure_count
        if minimum_width is not None:
            minimum_width = abjad.Duration(minimum_width)
        self._minimum_width = minimum_width
        if multiplier is not None:
            multiplier = abjad.Multiplier(multiplier)
        self._multiplier = multiplier
        if measures is not None:
            prototype = abjad.OrderedDict
            assert isinstance(measures, prototype), repr(measures)
        self._measures = measures

    ### SPECIAL METHODS ###

    def __call__(self, segment_maker=None) -> None:
        r'''Calls command on `segment_maker`.
        '''
        score = segment_maker.score
        skips = baca.select(score['GlobalSkips']).skips()
        self._populate_fermata_measure_numbers()
        programmatic = True
        if self.measures and len(self.measures) == len(skips):
            programmatic = False
        if programmatic:
            leaves = abjad.iterate(score).leaves(grace_notes=False)
            method = self._get_minimum_durations_by_measure
            minimum_durations_by_measure = method(skips, leaves)
        string = '_fermata_start_offsets'
        self._fermata_start_offsets = getattr(segment_maker, string, [])
        first_measure_number = self.first_measure_number or 1
        for measure_index, skip in enumerate(skips):
            measure_number = first_measure_number + measure_index
            if (self.fermata_measure_width is not None and
                self._is_fermata_measure(measure_number, skip)):
                duration = self.fermata_measure_width
            elif self.measures and measure_number in self.measures:
                duration = self.measures[measure_number]
                duration = abjad.NonreducedFraction(duration)
            else:
                duration = minimum_durations_by_measure[measure_index]
                if self.minimum_width is not None:
                    if self.minimum_width < duration:
                        duration = self.minimum_width
                if self.multiplier is not None:
                    duration = duration / self.multiplier
            eol_adjusted = False
            if measure_number in self.eol_measure_numbers:
                duration_ = duration
                duration *= self._magic_lilypond_eol_adjustment
                eol_adjusted = True
            spacing_section = SpacingSection(duration)
            tag = abjad.Tag(abjad.tags.SPACING)
            abjad.attach(spacing_section, skip, tag=tag.prepend('HSS1'))
            if eol_adjusted:
                multiplier = self._magic_lilypond_eol_adjustment
                string = f'[[{duration_!s} * {multiplier!s}]]'
                markup = abjad.Markup(string)
            else:
                string = f'[{duration!s}]'
                markup = abjad.Markup(string)
            if programmatic:
                command = 'make-dark-cyan'
            else:
                command = 'make-forest-green'
            string = fr'^ \markup {{ \{command} "{string}" }}'
            literal = abjad.LilyPondLiteral(string, format_slot='after')
            tag = abjad.Tag(abjad.tags.SPACING_MARKUP).prepend('HSS2')
            abjad.attach(literal, skip, deactivate=True, tag=tag)

    ### PRIVATE METHODS ###

    def _coerce_measure_number(self, measure_number):
        if measure_number == 'end':
            return self.last_measure_number
        if measure_number == 0:
            raise Exception(f'zero-valued measure number not allowed.')
        if measure_number < 0:
            measure_number = self.last_measure_number - abs(measure_number) + 1
        if measure_number < self.first_measure_number:
            measure_number += self.first_measure_number - 1
        if self.last_measure_number < measure_number:
            raise Exception(f'measure number {measure_number} greater than'
                f' last measure number ({self.last_measure_number}).')
        return measure_number

    def _get_minimum_durations_by_measure(self, skips, leaves):
        measure_timespans = []
        durations_by_measure = []
        for skip in skips:
            measure_timespan = abjad.inspect(skip).get_timespan()
            measure_timespans.append(measure_timespan)
            durations_by_measure.append([])
        leaf_timespans = set()
        leaf_count = 0
        for leaf in leaves:
            leaf_timespan = abjad.inspect(leaf).get_timespan()
            leaf_duration = leaf_timespan.duration
            prototype = (abjad.Multiplier, abjad.NonreducedFraction)
            multiplier = abjad.inspect(leaf).get_indicator(prototype)
            if multiplier is not None:
                leaf_duration = leaf_duration / multiplier
            pair = (leaf_timespan, leaf_duration)
            leaf_timespans.add(pair)
            leaf_count += 1
        measure_index = 0
        measure_timespan = measure_timespans[measure_index]
        leaf_timespans = list(leaf_timespans)
        leaf_timespans.sort(key=lambda _: _[0].start_offset)
        start_offset = 0
        for pair in leaf_timespans:
            leaf_timespan, leaf_duration = pair
            assert start_offset <= leaf_timespan.start_offset
            start_offset = leaf_timespan.start_offset
            if leaf_timespan.starts_during_timespan(measure_timespan):
                durations_by_measure[measure_index].append(leaf_duration)
            else:
                measure_index += 1
                if len(measure_timespans) <= measure_index:
                    continue
                measure_timespan = measure_timespans[measure_index]
                assert leaf_timespan.starts_during_timespan(measure_timespan)
                durations_by_measure[measure_index].append(leaf_duration)
        minimum_durations_by_measure = [min(_) for _ in durations_by_measure]
        return minimum_durations_by_measure

    def _is_fermata_measure(self, measure_number, skip):
        if (self.fermata_measure_numbers and
            measure_number in self.fermata_measure_numbers):
            return True
        measure_timespan = abjad.inspect(skip).get_timespan()
        return measure_timespan.start_offset in self._fermata_start_offsets

    def _populate_fermata_measure_numbers(self):
        if not self.fermata_score:
            return
        path = abjad.Path(self.fermata_score)
        string = 'fermata_measure_numbers'
        dictionary = path.get_metadatum(string, abjad.OrderedDict())
        for path, fermata_measure_numbers in dictionary.items():
            self._fermata_measure_numbers.extend(fermata_measure_numbers)

    ### PUBLIC PROPERTIES ###

    @property
    def bol_measure_numbers(self) -> typing.List[int]:
        r'''Gets beginning-of-line measure numbers.

        ..  container:: example

            >>> breaks = baca.breaks(
            ...     baca.page([1, 15, (10, 20)], [9, 115, (10, 20)])
            ...     )
            >>> spacing = baca.scorewide_spacing(
            ...     (95, 18),
            ...     breaks=breaks,
            ...     fallback_duration=(1, 20),
            ...     )

            >>> spacing.bol_measure_numbers
            [95, 103]

        '''
        bol_measure_numbers = []
        if self.breaks and self.breaks.bol_measure_numbers:
            first_breaks_measure_number = self.breaks.bol_measure_numbers[0]
            for bol_measure_number in self.breaks.bol_measure_numbers:
                offset = bol_measure_number - first_breaks_measure_number
                bol_measure_number = self.first_measure_number + offset
                bol_measure_numbers.append(bol_measure_number)
        return bol_measure_numbers

    @property
    def breaks(self) -> typing.Optional[BreakMeasureMap]:
        r'''Gets break measure map.
        '''
        return self._breaks

    @property
    def eol_measure_numbers(self) -> typing.List[int]:
        r'''Gets end-of-line measure numbers.

        ..  container:: example

            >>> breaks = baca.breaks(
            ...     baca.page([1, 15, (10, 20)], [9, 115, (10, 20)])
            ...     )
            >>> spacing = baca.scorewide_spacing(
            ...     (95, 18),
            ...     breaks=breaks,
            ...     fallback_duration=(1, 20),
            ...     )

            >>> spacing.eol_measure_numbers
            [102, 112]

        '''
        eol_measure_numbers = []
        for bol_measure_number in self.bol_measure_numbers[1:]:
            eol_measure_number = bol_measure_number - 1
            eol_measure_numbers.append(eol_measure_number)
        if (self.last_measure_number and
            self.last_measure_number not in eol_measure_numbers):
            eol_measure_numbers.append(self.last_measure_number)
        return eol_measure_numbers

    @property
    def fermata_measure_numbers(self) -> typing.List[int]:
        r'''Gets fermata measure numbers.

        ..  container:: example

            >>> breaks = baca.breaks(
            ...     baca.page([1, 15, (10, 20)], [9, 115, (10, 20)])
            ...     )
            >>> spacing = baca.scorewide_spacing(
            ...     (95, 18),
            ...     breaks=breaks,
            ...     fallback_duration=(1, 20),
            ...     )

            >>> spacing.fermata_measure_numbers
            []

        '''
        return self._fermata_measure_numbers

    @property
    def fermata_measure_width(self) -> typing.Optional[
        abjad.NonreducedFraction
        ]:
        r'''Gets fermata measure width.

        Sets fermata measures to exactly this width when set; ignores minimum
        width and multiplier.
        '''
        return self._fermata_measure_width

    @property
    def fermata_score(self) -> typing.Optional[str]:
        r'''Gets name score package with fermata measures.
        '''
        return self._fermata_score

    @property
    def first_measure_number(self) -> int:
        r'''Gets first measure number.

        ..  container:: example

            >>> breaks = baca.breaks(
            ...     baca.page([1, 15, (10, 20)], [9, 115, (10, 20)])
            ...     )
            >>> spacing = baca.scorewide_spacing(
            ...     (95, 18),
            ...     breaks=breaks,
            ...     fallback_duration=(1, 20),
            ...     )

            >>> spacing.first_measure_number
            95

        '''
        return self._first_measure_number

    @property
    def last_measure_number(self) -> typing.Optional[int]:
        r'''Gets last measure number.

        ..  container:: example

            >>> breaks = baca.breaks(
            ...     baca.page([1, 15, (10, 20)], [9, 115, (10, 20)])
            ...     )
            >>> spacing = baca.scorewide_spacing(
            ...     (95, 18),
            ...     breaks=breaks,
            ...     fallback_duration=(1, 20),
            ...     )

            >>> spacing.last_measure_number
            112

        Returns none when first measure number is not defined.

        Returns none when measure count is not defined.
        '''
        if (self.first_measure_number is not None and
            self.measure_count is not None):
            return self.first_measure_number + self.measure_count - 1
        else:
            return None

    @property
    def measure_count(self) -> int:
        r'''Gets measure count.

        ..  container:: example

            >>> breaks = baca.breaks(
            ...     baca.page([1, 15, (10, 20)], [9, 115, (10, 20)])
            ...     )
            >>> spacing = baca.scorewide_spacing(
            ...     (95, 18),
            ...     breaks=breaks,
            ...     fallback_duration=(1, 20),
            ...     )

            >>> spacing.measure_count
            18

        '''
        return self._measure_count

    @property
    def measures(self) -> typing.Optional[abjad.OrderedDict]:
        r'''Gets measure overrides.
        '''
        return self._measures

    @property
    def minimum_width(self) -> typing.Optional[abjad.NonreducedFraction]:
        r'''Gets minimum width.

        Defaults to none and interprets none equal to ``1/8``.
        '''
        return self._minimum_width

    @property
    def multiplier(self) -> typing.Optional[abjad.Multiplier]:
        r'''Gets multiplier.
        '''
        return self._multiplier

    ### PUBLIC METHODS ###

    def override(
        self,
        measures: typing.Union[int, tuple, list],
        pair: typing.Union[typing.Tuple[int, int], str],
        ) -> None:
        r'''Overrides `measures` with spacing `pair`.

        ..  container:: example

            >>> breaks = baca.breaks(
            ...     baca.page([1, 15, (10, 20)]),
            ...     )
            >>> spacing = baca.scorewide_spacing(
            ...     (95, 5),
            ...     breaks=breaks,
            ...     fallback_duration=(1, 20),
            ...     )

            >>> abjad.f(spacing.measures)
            abjad.OrderedDict(
                [
                    (
                        95,
                        abjad.NonreducedFraction(1, 20),
                        ),
                    (
                        96,
                        abjad.NonreducedFraction(1, 20),
                        ),
                    (
                        97,
                        abjad.NonreducedFraction(1, 20),
                        ),
                    (
                        98,
                        abjad.NonreducedFraction(1, 20),
                        ),
                    (
                        99,
                        abjad.NonreducedFraction(1, 20),
                        ),
                    ]
                )

            Works with ``'all'``:

            >>> spacing.override('all', (1, 24))
            >>> abjad.f(spacing.measures)
            abjad.OrderedDict(
                [
                    (
                        95,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        96,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        97,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        98,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        99,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    ]
                )

            Works with measure number:

            >>> spacing.override('all', (1, 16))
            >>> spacing.override(95, (1, 24))
            >>> abjad.f(spacing.measures)
            abjad.OrderedDict(
                [
                    (
                        95,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        96,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        97,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        98,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        99,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    ]
                )

            Works with range of measure numbers:

            >>> spacing.override('all', (1, 16))
            >>> spacing.override((95, 97), (1, 24))
            >>> abjad.f(spacing.measures)
            abjad.OrderedDict(
                [
                    (
                        95,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        96,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        97,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        98,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        99,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    ]
                )

            Works with list of measure numbers:

            >>> spacing.override('all', (1, 16))
            >>> spacing.override([95, 97, 99], (1, 24))
            >>> abjad.f(spacing.measures)
            abjad.OrderedDict(
                [
                    (
                        95,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        96,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        97,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        98,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        99,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    ]
                )

            Works with negative indices:

            >>> spacing.override('all', (1, 16))
            >>> spacing.override([-3, -1], (1, 24))
            >>> abjad.f(spacing.measures)
            abjad.OrderedDict(
                [
                    (
                        95,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        96,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        97,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        98,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        99,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    ]
                )

            Works with ``'end'``:

            >>> spacing.override('all', (1, 16))
            >>> spacing.override('end', (1, 24))
            >>> abjad.f(spacing.measures)
            abjad.OrderedDict(
                [
                    (
                        95,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        96,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        97,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        98,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        99,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    ]
                )
                
            Works with ``'end'`` range:

            >>> spacing.override('all', (1, 16))
            >>> spacing.override((3, 'end'), (1, 24))
            >>> abjad.f(spacing.measures)
            abjad.OrderedDict(
                [
                    (
                        95,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        96,
                        abjad.NonreducedFraction(1, 16),
                        ),
                    (
                        97,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        98,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    (
                        99,
                        abjad.NonreducedFraction(1, 24),
                        ),
                    ]
                )

        '''
        if measures == 'all':
            measures = (1, 'end')
        duration = abjad.NonreducedFraction(pair)
        if isinstance(measures, (int, str)):
            number = self._coerce_measure_number(measures)
            self.measures[number] = duration
        elif isinstance(measures, tuple):
            start_measure, stop_measure = measures
            start_measure = self._coerce_measure_number(start_measure)
            stop_measure = self._coerce_measure_number(stop_measure)
            for number in range(start_measure, stop_measure + 1):
                self.measures[number] = duration
        elif isinstance(measures, list):
            for measure in measures:
                number = self._coerce_measure_number(measure)
                self.measures[number] = duration
        else:
            message = f'measures must be int, pair or list (not {measures!r})'
            raise TypeError(message)
