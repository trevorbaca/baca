import abjad
import baca


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
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \time 8/16
                        \bar "" %! SEGMENT:EMPTY_START_BAR:1
                        s1 * 1/2
                            - \markup { %! STAGE_NUMBER_MARKUP:2
                                \fontsize %! STAGE_NUMBER_MARKUP:2
                                    #-3 %! STAGE_NUMBER_MARKUP:2
                                    \with-color %! STAGE_NUMBER_MARKUP:2
                                        #(x11-color 'DarkCyan) %! STAGE_NUMBER_MARKUP:2
                                        [1] %! STAGE_NUMBER_MARKUP:2
                                } %! STAGE_NUMBER_MARKUP:2
            <BLANKLINE>
                        %%% GlobalSkips [measure 2] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 2/4
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 1/2
                        s1 * 1/2
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \clef "treble" %! EXPLICIT_CLEF_COMMAND:3
                                \once \override Staff.Clef.color = #(x11-color 'blue) %! EXPLICIT_CLEF_COLOR:1
                                \override Staff.Clef.color = ##f %! EXPLICIT_CLEF_UNCOLOR:2
                                e'16 [
                                \override Staff.Clef.color = #(x11-color 'DarkCyan) %! EXPLICIT_CLEF_SHADOW:4
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
                                f'16 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                e'8 [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e'8
            <BLANKLINE>
                                f'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                e'4
            <BLANKLINE>
                                f'4
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                e'2
                                \bar "|"
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
        ...     spacing_specifier=baca.HorizontalSpacingSpecifier(),
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
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \time 8/16
                        \bar "" %! SEGMENT:EMPTY_START_BAR:1
                        \newSpacingSection
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 16) %! SEGMENT:SPACING_COMMAND:3
                        s1 * 1/2
                            - \markup {
                                \column
                                    {
                                        \line % STAGE_NUMBER_MARKUP:2
                                            { % STAGE_NUMBER_MARKUP:2
                                                \fontsize % STAGE_NUMBER_MARKUP:2
                                                    #-3 % STAGE_NUMBER_MARKUP:2
                                                    \with-color % STAGE_NUMBER_MARKUP:2
                                                        #(x11-color 'DarkCyan) % STAGE_NUMBER_MARKUP:2
                                                        [1] % STAGE_NUMBER_MARKUP:2
                                            } % STAGE_NUMBER_MARKUP:2
                                        \line % SEGMENT:SPACING_MARKUP:4
                                            { % SEGMENT:SPACING_MARKUP:4
                                                \with-color % SEGMENT:SPACING_MARKUP:4
                                                    #(x11-color 'DarkCyan) % SEGMENT:SPACING_MARKUP:4
                                                    \fontsize % SEGMENT:SPACING_MARKUP:4
                                                        #-3 % SEGMENT:SPACING_MARKUP:4
                                                        (1/16) % SEGMENT:SPACING_MARKUP:4
                                            } % SEGMENT:SPACING_MARKUP:4
                                    }
                                }
            <BLANKLINE>
                        %%% GlobalSkips [measure 2] %%%
                        \time 4/8
                        \newSpacingSection
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 8) %! SEGMENT:SPACING_COMMAND:1
                        s1 * 1/2
                            - \markup { %! SEGMENT:SPACING_MARKUP:2
                                \with-color %! SEGMENT:SPACING_MARKUP:2
                                    #(x11-color 'DarkCyan) %! SEGMENT:SPACING_MARKUP:2
                                    \fontsize %! SEGMENT:SPACING_MARKUP:2
                                        #-3 %! SEGMENT:SPACING_MARKUP:2
                                        (1/8) %! SEGMENT:SPACING_MARKUP:2
                                } %! SEGMENT:SPACING_MARKUP:2
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 2/4
                        \newSpacingSection
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 4) %! SEGMENT:SPACING_COMMAND:1
                        s1 * 1/2
                            - \markup { %! SEGMENT:SPACING_MARKUP:2
                                \with-color %! SEGMENT:SPACING_MARKUP:2
                                    #(x11-color 'DarkCyan) %! SEGMENT:SPACING_MARKUP:2
                                    \fontsize %! SEGMENT:SPACING_MARKUP:2
                                        #-3 %! SEGMENT:SPACING_MARKUP:2
                                        (1/4) %! SEGMENT:SPACING_MARKUP:2
                                } %! SEGMENT:SPACING_MARKUP:2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 1/2
                        \newSpacingSection
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 2) %! SEGMENT:SPACING_COMMAND:1
                        s1 * 1/2
                            - \markup { %! SEGMENT:SPACING_MARKUP:2
                                \with-color %! SEGMENT:SPACING_MARKUP:2
                                    #(x11-color 'DarkCyan) %! SEGMENT:SPACING_MARKUP:2
                                    \fontsize %! SEGMENT:SPACING_MARKUP:2
                                        #-3 %! SEGMENT:SPACING_MARKUP:2
                                        (1/2) %! SEGMENT:SPACING_MARKUP:2
                                } %! SEGMENT:SPACING_MARKUP:2
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \clef "treble" %! EXPLICIT_CLEF_COMMAND:3
                                \once \override Staff.Clef.color = #(x11-color 'blue) %! EXPLICIT_CLEF_COLOR:1
                                \override Staff.Clef.color = ##f %! EXPLICIT_CLEF_UNCOLOR:2
                                e'16 [
                                \override Staff.Clef.color = #(x11-color 'DarkCyan) %! EXPLICIT_CLEF_SHADOW:4
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
                                f'16 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                e'8 [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e'8
            <BLANKLINE>
                                f'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                e'4
            <BLANKLINE>
                                f'4
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                e'2
                                \bar "|"
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
        ...     spacing_specifier=baca.HorizontalSpacingSpecifier(
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
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \time 8/16
                        \bar "" %! SEGMENT:EMPTY_START_BAR:1
                        \newSpacingSection
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 16) %! SEGMENT:SPACING_COMMAND:3
                        s1 * 1/2
                            - \markup {
                                \column
                                    {
                                        \line % STAGE_NUMBER_MARKUP:2
                                            { % STAGE_NUMBER_MARKUP:2
                                                \fontsize % STAGE_NUMBER_MARKUP:2
                                                    #-3 % STAGE_NUMBER_MARKUP:2
                                                    \with-color % STAGE_NUMBER_MARKUP:2
                                                        #(x11-color 'DarkCyan) % STAGE_NUMBER_MARKUP:2
                                                        [1] % STAGE_NUMBER_MARKUP:2
                                            } % STAGE_NUMBER_MARKUP:2
                                        \line % SEGMENT:SPACING_MARKUP:4
                                            { % SEGMENT:SPACING_MARKUP:4
                                                \with-color % SEGMENT:SPACING_MARKUP:4
                                                    #(x11-color 'DarkCyan) % SEGMENT:SPACING_MARKUP:4
                                                    \fontsize % SEGMENT:SPACING_MARKUP:4
                                                        #-3 % SEGMENT:SPACING_MARKUP:4
                                                        (1/16) % SEGMENT:SPACING_MARKUP:4
                                            } % SEGMENT:SPACING_MARKUP:4
                                    }
                                }
            <BLANKLINE>
                        %%% GlobalSkips [measure 2] %%%
                        \time 4/8
                        \newSpacingSection
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 8) %! SEGMENT:SPACING_COMMAND:1
                        s1 * 1/2
                            - \markup { %! SEGMENT:SPACING_MARKUP:2
                                \with-color %! SEGMENT:SPACING_MARKUP:2
                                    #(x11-color 'DarkCyan) %! SEGMENT:SPACING_MARKUP:2
                                    \fontsize %! SEGMENT:SPACING_MARKUP:2
                                        #-3 %! SEGMENT:SPACING_MARKUP:2
                                        (1/8) %! SEGMENT:SPACING_MARKUP:2
                                } %! SEGMENT:SPACING_MARKUP:2
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 2/4
                        \newSpacingSection
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 4) %! SEGMENT:SPACING_COMMAND:1
                        s1 * 1/2
                            - \markup { %! SEGMENT:SPACING_MARKUP:2
                                \with-color %! SEGMENT:SPACING_MARKUP:2
                                    #(x11-color 'DarkCyan) %! SEGMENT:SPACING_MARKUP:2
                                    \fontsize %! SEGMENT:SPACING_MARKUP:2
                                        #-3 %! SEGMENT:SPACING_MARKUP:2
                                        (1/4) %! SEGMENT:SPACING_MARKUP:2
                                } %! SEGMENT:SPACING_MARKUP:2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 1/2
                        \newSpacingSection
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 2) %! SEGMENT:SPACING_COMMAND:1
                        s1 * 1/2
                            - \markup { %! SEGMENT:SPACING_MARKUP:2
                                \with-color %! SEGMENT:SPACING_MARKUP:2
                                    #(x11-color 'DarkCyan) %! SEGMENT:SPACING_MARKUP:2
                                    \fontsize %! SEGMENT:SPACING_MARKUP:2
                                        #-3 %! SEGMENT:SPACING_MARKUP:2
                                        (1/2) %! SEGMENT:SPACING_MARKUP:2
                                } %! SEGMENT:SPACING_MARKUP:2
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \clef "treble" %! EXPLICIT_CLEF_COMMAND:3
                                \once \override Staff.Clef.color = #(x11-color 'blue) %! EXPLICIT_CLEF_COLOR:1
                                \override Staff.Clef.color = ##f %! EXPLICIT_CLEF_UNCOLOR:2
                                e'16 [
                                \override Staff.Clef.color = #(x11-color 'DarkCyan) %! EXPLICIT_CLEF_SHADOW:4
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
                                f'16 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                e'8 [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e'8
            <BLANKLINE>
                                f'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                e'4
            <BLANKLINE>
                                f'4
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                e'2
                                \bar "|"
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
        ...     spacing_specifier=baca.HorizontalSpacingSpecifier(
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
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \time 8/16
                        \bar "" %! SEGMENT:EMPTY_START_BAR:1
                        \newSpacingSection
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 32) %! SEGMENT:SPACING_COMMAND:3
                        s1 * 1/2
                            - \markup {
                                \column
                                    {
                                        \line % STAGE_NUMBER_MARKUP:2
                                            { % STAGE_NUMBER_MARKUP:2
                                                \fontsize % STAGE_NUMBER_MARKUP:2
                                                    #-3 % STAGE_NUMBER_MARKUP:2
                                                    \with-color % STAGE_NUMBER_MARKUP:2
                                                        #(x11-color 'DarkCyan) % STAGE_NUMBER_MARKUP:2
                                                        [1] % STAGE_NUMBER_MARKUP:2
                                            } % STAGE_NUMBER_MARKUP:2
                                        \line % SEGMENT:SPACING_MARKUP:4
                                            { % SEGMENT:SPACING_MARKUP:4
                                                \with-color % SEGMENT:SPACING_MARKUP:4
                                                    #(x11-color 'DarkCyan) % SEGMENT:SPACING_MARKUP:4
                                                    \fontsize % SEGMENT:SPACING_MARKUP:4
                                                        #-3 % SEGMENT:SPACING_MARKUP:4
                                                        (1/32) % SEGMENT:SPACING_MARKUP:4
                                            } % SEGMENT:SPACING_MARKUP:4
                                    }
                                }
            <BLANKLINE>
                        %%% GlobalSkips [measure 2] %%%
                        \time 4/8
                        \newSpacingSection
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 16) %! SEGMENT:SPACING_COMMAND:1
                        s1 * 1/2
                            - \markup { %! SEGMENT:SPACING_MARKUP:2
                                \with-color %! SEGMENT:SPACING_MARKUP:2
                                    #(x11-color 'DarkCyan) %! SEGMENT:SPACING_MARKUP:2
                                    \fontsize %! SEGMENT:SPACING_MARKUP:2
                                        #-3 %! SEGMENT:SPACING_MARKUP:2
                                        (1/16) %! SEGMENT:SPACING_MARKUP:2
                                } %! SEGMENT:SPACING_MARKUP:2
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 2/4
                        \newSpacingSection
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 8) %! SEGMENT:SPACING_COMMAND:1
                        s1 * 1/2
                            - \markup { %! SEGMENT:SPACING_MARKUP:2
                                \with-color %! SEGMENT:SPACING_MARKUP:2
                                    #(x11-color 'DarkCyan) %! SEGMENT:SPACING_MARKUP:2
                                    \fontsize %! SEGMENT:SPACING_MARKUP:2
                                        #-3 %! SEGMENT:SPACING_MARKUP:2
                                        (1/8) %! SEGMENT:SPACING_MARKUP:2
                                } %! SEGMENT:SPACING_MARKUP:2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 1/2
                        \newSpacingSection
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 4) %! SEGMENT:SPACING_COMMAND:1
                        s1 * 1/2
                            - \markup { %! SEGMENT:SPACING_MARKUP:2
                                \with-color %! SEGMENT:SPACING_MARKUP:2
                                    #(x11-color 'DarkCyan) %! SEGMENT:SPACING_MARKUP:2
                                    \fontsize %! SEGMENT:SPACING_MARKUP:2
                                        #-3 %! SEGMENT:SPACING_MARKUP:2
                                        (1/4) %! SEGMENT:SPACING_MARKUP:2
                                } %! SEGMENT:SPACING_MARKUP:2
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \clef "treble" %! EXPLICIT_CLEF_COMMAND:3
                                \once \override Staff.Clef.color = #(x11-color 'blue) %! EXPLICIT_CLEF_COLOR:1
                                \override Staff.Clef.color = ##f %! EXPLICIT_CLEF_UNCOLOR:2
                                e'16 [
                                \override Staff.Clef.color = #(x11-color 'DarkCyan) %! EXPLICIT_CLEF_SHADOW:4
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
                                f'16 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                e'8 [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e'8
            <BLANKLINE>
                                f'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                e'4
            <BLANKLINE>
                                f'4
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                e'2
                                \bar "|"
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
        ...     spacing_specifier=baca.HorizontalSpacingSpecifier(
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
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \time 8/16
                        \bar "" %! SEGMENT:EMPTY_START_BAR:1
                        \newSpacingSection
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 32) %! SEGMENT:SPACING_COMMAND:3
                        s1 * 1/2
                            - \markup {
                                \column
                                    {
                                        \line % STAGE_NUMBER_MARKUP:2
                                            { % STAGE_NUMBER_MARKUP:2
                                                \fontsize % STAGE_NUMBER_MARKUP:2
                                                    #-3 % STAGE_NUMBER_MARKUP:2
                                                    \with-color % STAGE_NUMBER_MARKUP:2
                                                        #(x11-color 'DarkCyan) % STAGE_NUMBER_MARKUP:2
                                                        [1] % STAGE_NUMBER_MARKUP:2
                                            } % STAGE_NUMBER_MARKUP:2
                                        \line % SEGMENT:SPACING_MARKUP:4
                                            { % SEGMENT:SPACING_MARKUP:4
                                                \with-color % SEGMENT:SPACING_MARKUP:4
                                                    #(x11-color 'DarkCyan) % SEGMENT:SPACING_MARKUP:4
                                                    \fontsize % SEGMENT:SPACING_MARKUP:4
                                                        #-3 % SEGMENT:SPACING_MARKUP:4
                                                        (1/32) % SEGMENT:SPACING_MARKUP:4
                                            } % SEGMENT:SPACING_MARKUP:4
                                    }
                                }
            <BLANKLINE>
                        %%% GlobalSkips [measure 2] %%%
                        \time 4/8
                        \newSpacingSection
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 16) %! SEGMENT:SPACING_COMMAND:1
                        s1 * 1/2
                            - \markup { %! SEGMENT:SPACING_MARKUP:2
                                \with-color %! SEGMENT:SPACING_MARKUP:2
                                    #(x11-color 'DarkCyan) %! SEGMENT:SPACING_MARKUP:2
                                    \fontsize %! SEGMENT:SPACING_MARKUP:2
                                        #-3 %! SEGMENT:SPACING_MARKUP:2
                                        (1/16) %! SEGMENT:SPACING_MARKUP:2
                                } %! SEGMENT:SPACING_MARKUP:2
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 2/4
                        \newSpacingSection
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 16) %! SEGMENT:SPACING_COMMAND:1
                        s1 * 1/2
                            - \markup { %! SEGMENT:SPACING_MARKUP:2
                                \with-color %! SEGMENT:SPACING_MARKUP:2
                                    #(x11-color 'DarkCyan) %! SEGMENT:SPACING_MARKUP:2
                                    \fontsize %! SEGMENT:SPACING_MARKUP:2
                                        #-3 %! SEGMENT:SPACING_MARKUP:2
                                        (1/16) %! SEGMENT:SPACING_MARKUP:2
                                } %! SEGMENT:SPACING_MARKUP:2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 1/2
                        \newSpacingSection
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 16) %! SEGMENT:SPACING_COMMAND:1
                        s1 * 1/2
                            - \markup { %! SEGMENT:SPACING_MARKUP:2
                                \with-color %! SEGMENT:SPACING_MARKUP:2
                                    #(x11-color 'DarkCyan) %! SEGMENT:SPACING_MARKUP:2
                                    \fontsize %! SEGMENT:SPACING_MARKUP:2
                                        #-3 %! SEGMENT:SPACING_MARKUP:2
                                        (1/16) %! SEGMENT:SPACING_MARKUP:2
                                } %! SEGMENT:SPACING_MARKUP:2
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \clef "treble" %! EXPLICIT_CLEF_COMMAND:3
                                \once \override Staff.Clef.color = #(x11-color 'blue) %! EXPLICIT_CLEF_COLOR:1
                                \override Staff.Clef.color = ##f %! EXPLICIT_CLEF_UNCOLOR:2
                                e'16 [
                                \override Staff.Clef.color = #(x11-color 'DarkCyan) %! EXPLICIT_CLEF_SHADOW:4
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
                                f'16 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                e'8 [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e'8
            <BLANKLINE>
                                f'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                e'4
            <BLANKLINE>
                                f'4
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                e'2
                                \bar "|"
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
        ...     spacing_specifier=baca.HorizontalSpacingSpecifier(
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
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \time 4/8
                        \bar "" %! SEGMENT:EMPTY_START_BAR:1
                        \newSpacingSection
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 16) %! SEGMENT:SPACING_COMMAND:3
                        s1 * 1/2
                            - \markup {
                                \column
                                    {
                                        \line % STAGE_NUMBER_MARKUP:2
                                            { % STAGE_NUMBER_MARKUP:2
                                                \fontsize % STAGE_NUMBER_MARKUP:2
                                                    #-3 % STAGE_NUMBER_MARKUP:2
                                                    \with-color % STAGE_NUMBER_MARKUP:2
                                                        #(x11-color 'DarkCyan) % STAGE_NUMBER_MARKUP:2
                                                        [1] % STAGE_NUMBER_MARKUP:2
                                            } % STAGE_NUMBER_MARKUP:2
                                        \line % SEGMENT:SPACING_MARKUP:4
                                            { % SEGMENT:SPACING_MARKUP:4
                                                \with-color % SEGMENT:SPACING_MARKUP:4
                                                    #(x11-color 'DarkCyan) % SEGMENT:SPACING_MARKUP:4
                                                    \fontsize % SEGMENT:SPACING_MARKUP:4
                                                        #-3 % SEGMENT:SPACING_MARKUP:4
                                                        (1/16) % SEGMENT:SPACING_MARKUP:4
                                            } % SEGMENT:SPACING_MARKUP:4
                                    }
                                }
            <BLANKLINE>
                        %%% GlobalSkips [measure 2] %%%
                        \time 3/8
                        \newSpacingSection
                        \set Score.proportionalNotationDuration = #(ly:make-moment 1 16) %! SEGMENT:SPACING_COMMAND:1
                        s1 * 3/8
                            - \markup { %! SEGMENT:SPACING_MARKUP:2
                                \with-color %! SEGMENT:SPACING_MARKUP:2
                                    #(x11-color 'DarkCyan) %! SEGMENT:SPACING_MARKUP:2
                                    \fontsize %! SEGMENT:SPACING_MARKUP:2
                                        #-3 %! SEGMENT:SPACING_MARKUP:2
                                        (1/16) %! SEGMENT:SPACING_MARKUP:2
                                } %! SEGMENT:SPACING_MARKUP:2
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            \override TupletNumber.text = \markup {
                                \scale
                                    #'(0.75 . 0.75)
                                    \score
                                        {
                                            \new Score \with {
                                                \override SpacingSpanner.spacing-increment = #0.5
                                                proportionalNotationDuration = ##f
                                            } <<
                                                \new RhythmicStaff \with {
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
                                                } {
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
                                %%% MusicVoice [measure 1] %%%
                                \once \override Beam.grow-direction = #right
                                \clef "treble" %! EXPLICIT_CLEF_COMMAND:3
                                \once \override Staff.Clef.color = #(x11-color 'blue) %! EXPLICIT_CLEF_COLOR:1
                                \override Staff.Clef.color = ##f %! EXPLICIT_CLEF_UNCOLOR:2
                                e'16 * 63/32 [
                                \override Staff.Clef.color = #(x11-color 'DarkCyan) %! EXPLICIT_CLEF_SHADOW:4
            <BLANKLINE>
                                f'16 * 115/64
            <BLANKLINE>
                                e'16 * 91/64
            <BLANKLINE>
                                f'16 * 35/32
            <BLANKLINE>
                                e'16 * 29/32
            <BLANKLINE>
                                f'16 * 13/16 ]
                            }
                            \revert TupletNumber.text
                            \override TupletNumber.text = \markup {
                                \scale
                                    #'(0.75 . 0.75)
                                    \score
                                        {
                                            \new Score \with {
                                                \override SpacingSpanner.spacing-increment = #0.5
                                                proportionalNotationDuration = ##f
                                            } <<
                                                \new RhythmicStaff \with {
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
                                                } {
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
                                %%% MusicVoice [measure 2] %%%
                                \once \override Beam.grow-direction = #right
                                e'16 * 117/64 [
            <BLANKLINE>
                                f'16 * 99/64
            <BLANKLINE>
                                e'16 * 69/64
            <BLANKLINE>
                                f'16 * 13/16
            <BLANKLINE>
                                e'16 * 47/64 ]
                                \bar "|"
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
        '_fermata_measure_width',
        '_minimum_width',
        '_multiplier',
        '_overrides',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        fermata_measure_width=None,
        minimum_width=None,
        multiplier=None,
        overrides=None,
        ):
        if fermata_measure_width is not None:
            fermata_measure_width = abjad.Duration(fermata_measure_width)
        self._fermata_measure_width = fermata_measure_width
        if minimum_width is not None:
            minimum_width = abjad.Duration(minimum_width)
        self._minimum_width = minimum_width
        if multiplier is not None:
            multiplier = abjad.Multiplier(multiplier)
        self._multiplier = multiplier
        if overrides is not None:
            overrides = tuple(overrides)
        self._overrides = overrides

    ### SPECIAL METHODS ###

    def __call__(self, segment_maker=None, tag=None):
        r'''Calls command on `segment_maker`.

        Returns none.
        '''
        score = segment_maker._score
        context = score['GlobalSkips']
        skips = baca.select(context).skips()
        leaves = abjad.iterate(score).leaves(grace_notes=False)
        minimum_durations_by_measure = self._get_minimum_durations_by_measure(
            skips,
            leaves,
            )
        fermata_start_offsets = getattr(
            segment_maker,
            '_fermata_start_offsets',
            [],
            )
        if tag is not None:
            command_tag = f'{tag}_COMMAND'
            markup_tag = f'{tag}_MARKUP'
        else:
            command_tag = None
            markup_tag = None
        for measure_index, skip in enumerate(skips):
            measure_timespan = abjad.inspect(skip).get_timespan()
            if (self.fermata_measure_width is not None and
                measure_timespan.start_offset in fermata_start_offsets):
                duration = self.fermata_measure_width
            else:
                duration = minimum_durations_by_measure[measure_index]
                if self.minimum_width is not None:
                    if self.minimum_width < duration:
                        duration = self.minimum_width
                if self.multiplier is not None:
                    duration = duration / self.multiplier
            command = abjad.LilyPondCommand('newSpacingSection')
            abjad.attach(command, skip)
            moment = abjad.SchemeMoment(duration)
            string = r'\set Score.proportionalNotationDuration = #'
            string += str(moment)
            literal = abjad.LilyPondLiteral(string)
            abjad.attach(literal, skip, tag=command_tag)
            markup = abjad.Markup(f'({duration!s})').fontsize(-3)
            markup = markup.with_color(abjad.SchemeColor('DarkCyan'))
            abjad.attach(markup, skip, tag=markup_tag)

    ### PRIVATE METHODS ###

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

    ### PUBLIC PROPERTIES ###

    @property
    def fermata_measure_width(self):
        r'''Gets fermata measure width.

        Sets fermata measures to exactly this width when set; ignores minimum
        width and multiplier.

        Defaults to none.

        Set to duration or none.

        Returns duration or none.
        '''
        return self._fermata_measure_width

    @property
    def minimum_width(self):
        r'''Gets minimum width.

        Defaults to none and interprets none equal to ``1/8``.

        Set to duration or none.

        Returns duration or none.
        '''
        return self._minimum_width

    @property
    def multiplier(self):
        r'''Gets multiplier.

        Defaults to none.

        Set to multiplier or none.

        Returns multiplier or none.
        '''
        return self._multiplier

    @property
    def overrides(self):
        r'''Gets overrides.

        Defaults to none.

        Set to tuple or none.

        Returns tuple or none.
        '''
        return self._overrides
