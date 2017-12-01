import abjad
import baca
from .Command import Command


class RegisterInterpolationCommand(Command):
    r"""Register interpolation command.

    ..  container:: example

        With music-maker:

        >>> music_maker = baca.MusicMaker()

        >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     collections,
        ...     baca.register(0, 24),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            fs'16 [
                            e'16
                            ef'16
                            f'16
                            a'16
                            bf'16
                            c''16
                            b'16
                            af'16
                            g''16
                            cs''16
                            d''16 ]
                        }
                        {
                            fs''16 [
                            e''16
                            ef''16
                            f''16
                            a''16
                            bf''16
                            c'''16
                            b''16
                            af''16
                            g'''16
                            cs'''16
                            d'''16 ]
                        }
                    }
                }
            >>

    ..  container:: example

        With chords:

        >>> music_maker = baca.MusicMaker()

        >>> collections = [
        ...     [6, 4], [3, 5], [9, 10], [0, 11], [8, 7], [1, 2],
        ...     ]
        >>> collections = [set(_) for _ in collections]
        >>> contribution = music_maker(
        ...     'Voice 1',
        ...     collections,
        ...     baca.register(0, 24),
        ...     )
        >>> lilypond_file = music_maker.show(contribution)
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff])
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            <e' fs'>16
                        }
                        {
                            <f' ef''>16
                        }
                        {
                            <a' bf'>16
                        }
                        {
                            <c'' b''>16
                        }
                        {
                            <g'' af''>16
                        }
                        {
                            <cs''' d'''>16
                        }
                    }
                }
            >>

    ..  container:: example

        Holds register constant:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.pitches(pitches),
        ...     baca.make_even_runs(),
        ...     baca.register(12, 12),
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
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 5] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 6] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 7] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 8] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \clef "treble" %! EXPLICIT_CLEF_COMMAND:2
                                \once \override Staff.Clef.color = #(x11-color 'blue) %! EXPLICIT_CLEF_COLOR:1
                                fs''8 [
                                \override Staff.Clef.color = #(x11-color 'DarkCyan) %! EXPLICIT_CLEF_SHADOW:3
            <BLANKLINE>
                                e''8
            <BLANKLINE>
                                ef''8
            <BLANKLINE>
                                f''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                a''8 [
            <BLANKLINE>
                                bf''8
            <BLANKLINE>
                                c''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                b''8 [
            <BLANKLINE>
                                af''8
            <BLANKLINE>
                                g''8
            <BLANKLINE>
                                cs''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                d''8 [
            <BLANKLINE>
                                fs''8
            <BLANKLINE>
                                e''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 5] %%%
                                ef''8 [
            <BLANKLINE>
                                f''8
            <BLANKLINE>
                                a''8
            <BLANKLINE>
                                bf''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 6] %%%
                                c''8 [
            <BLANKLINE>
                                b''8
            <BLANKLINE>
                                af''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 7] %%%
                                g''8 [
            <BLANKLINE>
                                cs''8
            <BLANKLINE>
                                d''8
            <BLANKLINE>
                                fs''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 8] %%%
                                e''8 [
            <BLANKLINE>
                                ef''8
            <BLANKLINE>
                                f''8 ]
                                \bar "|"
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Octave-transposes to a target interpolated from 12 down to 0:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.pitches(pitches),
        ...     baca.make_even_runs(),
        ...     baca.register(12, 0),
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
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 5] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 6] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 7] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 8] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \clef "treble" %! EXPLICIT_CLEF_COMMAND:2
                                \once \override Staff.Clef.color = #(x11-color 'blue) %! EXPLICIT_CLEF_COLOR:1
                                fs''8 [
                                \override Staff.Clef.color = #(x11-color 'DarkCyan) %! EXPLICIT_CLEF_SHADOW:3
            <BLANKLINE>
                                e''8
            <BLANKLINE>
                                ef''8
            <BLANKLINE>
                                f''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                a''8 [
            <BLANKLINE>
                                bf'8
            <BLANKLINE>
                                c''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                b'8 [
            <BLANKLINE>
                                af'8
            <BLANKLINE>
                                g''8
            <BLANKLINE>
                                cs''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                d''8 [
            <BLANKLINE>
                                fs'8
            <BLANKLINE>
                                e''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 5] %%%
                                ef''8 [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                a'8
            <BLANKLINE>
                                bf'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 6] %%%
                                c''8 [
            <BLANKLINE>
                                b'8
            <BLANKLINE>
                                af'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 7] %%%
                                g'8 [
            <BLANKLINE>
                                cs''8
            <BLANKLINE>
                                d'8
            <BLANKLINE>
                                fs'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 8] %%%
                                e'8 [
            <BLANKLINE>
                                ef'8
            <BLANKLINE>
                                f'8 ]
                                \bar "|"
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Octave-transposes to a target interpolated from 0 up to 12:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.pitches(pitches),
        ...     baca.make_even_runs(),
        ...     baca.register(0, 12),
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
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 5] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 6] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 7] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 8] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \clef "treble" %! EXPLICIT_CLEF_COMMAND:2
                                \once \override Staff.Clef.color = #(x11-color 'blue) %! EXPLICIT_CLEF_COLOR:1
                                fs'8 [
                                \override Staff.Clef.color = #(x11-color 'DarkCyan) %! EXPLICIT_CLEF_SHADOW:3
            <BLANKLINE>
                                e'8
            <BLANKLINE>
                                ef'8
            <BLANKLINE>
                                f'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                a'8 [
            <BLANKLINE>
                                bf'8
            <BLANKLINE>
                                c''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                b'8 [
            <BLANKLINE>
                                af'8
            <BLANKLINE>
                                g'8
            <BLANKLINE>
                                cs''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                d''8 [
            <BLANKLINE>
                                fs'8
            <BLANKLINE>
                                e''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 5] %%%
                                ef''8 [
            <BLANKLINE>
                                f''8
            <BLANKLINE>
                                a'8
            <BLANKLINE>
                                bf'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 6] %%%
                                c''8 [
            <BLANKLINE>
                                b'8
            <BLANKLINE>
                                af'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 7] %%%
                                g''8 [
            <BLANKLINE>
                                cs''8
            <BLANKLINE>
                                d''8
            <BLANKLINE>
                                fs''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 8] %%%
                                e''8 [
            <BLANKLINE>
                                ef''8
            <BLANKLINE>
                                f''8 ]
                                \bar "|"
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Octave-transposes to a target interpolated from 12 down to -12:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.pitches(pitches),
        ...     baca.make_even_runs(),
        ...     baca.register(12, -12),
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
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 5] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 6] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 7] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 8] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \clef "treble" %! EXPLICIT_CLEF_COMMAND:2
                                \once \override Staff.Clef.color = #(x11-color 'blue) %! EXPLICIT_CLEF_COLOR:1
                                fs''8 [
                                \override Staff.Clef.color = #(x11-color 'DarkCyan) %! EXPLICIT_CLEF_SHADOW:3
            <BLANKLINE>
                                e''8
            <BLANKLINE>
                                ef''8
            <BLANKLINE>
                                f''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                a'8 [
            <BLANKLINE>
                                bf'8
            <BLANKLINE>
                                c''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                b'8 [
            <BLANKLINE>
                                af'8
            <BLANKLINE>
                                g'8
            <BLANKLINE>
                                cs''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                d'8 [
            <BLANKLINE>
                                fs'8
            <BLANKLINE>
                                e'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 5] %%%
                                ef'8 [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                a'8
            <BLANKLINE>
                                bf8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 6] %%%
                                c'8 [
            <BLANKLINE>
                                b8
            <BLANKLINE>
                                af8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 7] %%%
                                g8 [
            <BLANKLINE>
                                cs'8
            <BLANKLINE>
                                d'8
            <BLANKLINE>
                                fs8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 8] %%%
                                e8 [
            <BLANKLINE>
                                ef8
            <BLANKLINE>
                                f8 ]
                                \bar "|"
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    ..  container:: example

        Octave-transposes to a target interpolated from -12 up to 12:

            >>> time_signatures = 4 * [(4, 8), (3, 8)]
            >>> maker = baca.SegmentMaker(
            ...     score_template=baca.SingleStaffScoreTemplate(),
            ...     time_signatures=time_signatures,
            ...     )

        >>> pitches = [6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]
        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.pitches(pitches),
        ...     baca.make_even_runs(),
        ...     baca.register(-12, 12),
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
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 5] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 6] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 7] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 8] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \clef "treble" %! EXPLICIT_CLEF_COMMAND:2
                                \once \override Staff.Clef.color = #(x11-color 'blue) %! EXPLICIT_CLEF_COLOR:1
                                fs8 [
                                \override Staff.Clef.color = #(x11-color 'DarkCyan) %! EXPLICIT_CLEF_SHADOW:3
            <BLANKLINE>
                                e8
            <BLANKLINE>
                                ef8
            <BLANKLINE>
                                f8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                a8 [
            <BLANKLINE>
                                bf8
            <BLANKLINE>
                                c'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 3] %%%
                                b8 [
            <BLANKLINE>
                                af8
            <BLANKLINE>
                                g'8
            <BLANKLINE>
                                cs'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 4] %%%
                                d'8 [
            <BLANKLINE>
                                fs'8
            <BLANKLINE>
                                e'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 5] %%%
                                ef'8 [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                a'8
            <BLANKLINE>
                                bf'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 6] %%%
                                c''8 [
            <BLANKLINE>
                                b'8
            <BLANKLINE>
                                af'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 7] %%%
                                g'8 [
            <BLANKLINE>
                                cs''8
            <BLANKLINE>
                                d''8
            <BLANKLINE>
                                fs''8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 8] %%%
                                e''8 [
            <BLANKLINE>
                                ef''8
            <BLANKLINE>
                                f''8 ]
                                \bar "|"
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start_pitch',
        '_stop_pitch',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        selector='baca.plts()',
        start_pitch=None,
        stop_pitch=None,
        ):
        Command.__init__(self, selector=selector)
        start_pitch = abjad.NumberedPitch(start_pitch)
        self._start_pitch = start_pitch
        stop_pitch = abjad.NumberedPitch(stop_pitch)
        self._stop_pitch = stop_pitch

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.start_pitch is None or self.stop_pitch is None:
            return
        if self.selector:
            argument = self.selector(argument)
        plts = baca.select(argument).plts()
        length = len(plts)
        for i, plt in enumerate(plts):
            registration = self._get_registration(i, length)
            for pleaf in plt:
                if isinstance(pleaf, abjad.Note):
                    written_pitches = registration([pleaf.written_pitch])
                    pleaf.written_pitch = written_pitches[0]
                elif isinstance(pleaf, abjad.Chord):
                    written_pitches = registration(pleaf.written_pitches)
                    pleaf.written_pitches = written_pitches
                else:
                    raise TypeError(pleaf)
                abjad.detach('not yet registered', pleaf)

    ### PRIVATE METHODS ###

    def _get_registration(self, i, length):
        start_pitch = self.start_pitch.number
        stop_pitch = self.stop_pitch.number
        compass = stop_pitch - start_pitch
        fraction = abjad.Fraction(i, length)
        addendum = fraction * compass
        current_pitch = start_pitch + addendum
        current_pitch = int(current_pitch)
        return baca.Registration([('[A0, C8]', current_pitch)])

    ### PUBLIC PROPERTIES ###

    @property
    def selector(self):
        r"""Gets selector.

        ..  container:: example

            Selects tuplet 0:

            >>> music_maker = baca.MusicMaker()

            >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.color(baca.tuplet(0)),
            ...     baca.register(0, 24, baca.tuplet(0)),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                fs'16 [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                e'16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                ef''16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                f''16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a'16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                bf'16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                c''16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                b''16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                af''16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                g''16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                cs'''16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                d'''16 ]
                            }
                            {
                                fs'16 [
                                e'16
                                ef'16
                                f'16
                                a'16
                                bf'16
                                c'16
                                b'16
                                af'16
                                g'16
                                cs'16
                                d'16 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Selects tuplet -1:

            >>> music_maker = baca.MusicMaker()

            >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.color(baca.tuplet(-1)),
            ...     baca.register(0, 24, baca.tuplet(-1)),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                fs'16 [
                                e'16
                                ef'16
                                f'16
                                a'16
                                bf'16
                                c'16
                                b'16
                                af'16
                                g'16
                                cs'16
                                d'16 ]
                            }
                            {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                fs'16 [
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                e'16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                ef''16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                f''16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                a'16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                bf'16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                c''16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                b''16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                af''16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                g''16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                cs'''16
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                d'''16 ]
                            }
                        }
                    }
                >>

        ..  container:: example

            Maps to tuplets:

            >>> music_maker = baca.MusicMaker()

            >>> collections = 2 * [[6, 4, 3, 5, 9, 10, 0, 11, 8, 7, 1, 2]]
            >>> contribution = music_maker(
            ...     'Voice 1',
            ...     collections,
            ...     baca.color(baca.tuplets()),
            ...     baca.map(baca.register(0, 24), baca.tuplets()),
            ...     )
            >>> lilypond_file = music_maker.show(contribution)
            >>> abjad.show(lilypond_file) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff])
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                fs'16 [
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                e'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                ef''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                f''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                a'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                bf'16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                c''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                b''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                af''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                g''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                cs'''16
                                \once \override Accidental.color = #red
                                \once \override Beam.color = #red
                                \once \override Dots.color = #red
                                \once \override NoteHead.color = #red
                                \once \override Stem.color = #red
                                d'''16 ]
                            }
                            {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                fs'16 [
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                e'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                ef''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                f''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                a'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                bf'16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                c''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                b''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                af''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                g''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                cs'''16
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                d'''16 ]
                            }
                        }
                    }
                >>

        Set to selector or none.
        """
        return self._selector

    @property
    def start_pitch(self):
        r'''Gets start pitch.

        Set to pitch.

        Returns pitch.
        '''
        return self._start_pitch

    @property
    def stop_pitch(self):
        r'''Gets stop pitch.

        Set to pitch.

        Returns pitch.
        '''
        return self._stop_pitch
