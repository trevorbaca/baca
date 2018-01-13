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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
            \new Staff <<
                \context Voice = "Voice 1" {
                    \voiceOne
                    {
                        {
                            fs'16
                            [
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
                            d''16
                            ]
                        }
                        {
                            fs''16
                            [
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
                            d'''16
                            ]
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        % GlobalSkips [measure 1]                                                    %! SM4
                        \once \override TextSpanner.Y-extent = ##f                                   %! SM29
                        \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29
                        \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29
                        \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29
                        \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29
                        \once \override TextSpanner.dash-period = 0                                  %! SM29
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                        \startTextSpan                                                               %! SM29
                        ^ \markup {
                            \column
                                {
                                %@% \line                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %@%     {                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %@%         \fontsize                                                %! MEASURE_INDEX_MARKUP:SM31
                                %@%             #3                                                   %! MEASURE_INDEX_MARKUP:SM31
                                %@%             \with-color                                          %! MEASURE_INDEX_MARKUP:SM31
                                %@%                 #(x11-color 'DarkCyan)                           %! MEASURE_INDEX_MARKUP:SM31
                                %@%                 [00]                                             %! MEASURE_INDEX_MARKUP:SM31
                                %@%     }                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %@% \line                                                            %! STAGE_NUMBER_MARKUP:SM3
                                %@%     {                                                            %! STAGE_NUMBER_MARKUP:SM3
                                %@%         \fontsize                                                %! STAGE_NUMBER_MARKUP:SM3
                                %@%             #3                                                   %! STAGE_NUMBER_MARKUP:SM3
                                %@%             \with-color                                          %! STAGE_NUMBER_MARKUP:SM3
                                %@%                 #(x11-color 'DarkCyan)                           %! STAGE_NUMBER_MARKUP:SM3
                                %@%                 [1]                                              %! STAGE_NUMBER_MARKUP:SM3
                                %@%     }                                                            %! STAGE_NUMBER_MARKUP:SM3
                                }
                            }
            <BLANKLINE>
                        % GlobalSkips [measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [01]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [02]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [03]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 5]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [04]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 6]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [05]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 7]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [06]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 8]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                        \stopTextSpan                                                                %! SM29
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [07]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                % MusicVoice [measure 1]                                             %! SM4
                                fs''8
                                [
            <BLANKLINE>
                                e''8
            <BLANKLINE>
                                ef''8
            <BLANKLINE>
                                f''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 2]                                             %! SM4
                                a''8
                                [
            <BLANKLINE>
                                bf''8
            <BLANKLINE>
                                c''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 3]                                             %! SM4
                                b''8
                                [
            <BLANKLINE>
                                af''8
            <BLANKLINE>
                                g''8
            <BLANKLINE>
                                cs''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 4]                                             %! SM4
                                d''8
                                [
            <BLANKLINE>
                                fs''8
            <BLANKLINE>
                                e''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 5]                                             %! SM4
                                ef''8
                                [
            <BLANKLINE>
                                f''8
            <BLANKLINE>
                                a''8
            <BLANKLINE>
                                bf''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 6]                                             %! SM4
                                c''8
                                [
            <BLANKLINE>
                                b''8
            <BLANKLINE>
                                af''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 7]                                             %! SM4
                                g''8
                                [
            <BLANKLINE>
                                cs''8
            <BLANKLINE>
                                d''8
            <BLANKLINE>
                                fs''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 8]                                             %! SM4
                                e''8
                                [
            <BLANKLINE>
                                ef''8
            <BLANKLINE>
                                f''8
                                ]
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        % GlobalSkips [measure 1]                                                    %! SM4
                        \once \override TextSpanner.Y-extent = ##f                                   %! SM29
                        \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29
                        \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29
                        \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29
                        \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29
                        \once \override TextSpanner.dash-period = 0                                  %! SM29
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                        \startTextSpan                                                               %! SM29
                        ^ \markup {
                            \column
                                {
                                %@% \line                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %@%     {                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %@%         \fontsize                                                %! MEASURE_INDEX_MARKUP:SM31
                                %@%             #3                                                   %! MEASURE_INDEX_MARKUP:SM31
                                %@%             \with-color                                          %! MEASURE_INDEX_MARKUP:SM31
                                %@%                 #(x11-color 'DarkCyan)                           %! MEASURE_INDEX_MARKUP:SM31
                                %@%                 [00]                                             %! MEASURE_INDEX_MARKUP:SM31
                                %@%     }                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %@% \line                                                            %! STAGE_NUMBER_MARKUP:SM3
                                %@%     {                                                            %! STAGE_NUMBER_MARKUP:SM3
                                %@%         \fontsize                                                %! STAGE_NUMBER_MARKUP:SM3
                                %@%             #3                                                   %! STAGE_NUMBER_MARKUP:SM3
                                %@%             \with-color                                          %! STAGE_NUMBER_MARKUP:SM3
                                %@%                 #(x11-color 'DarkCyan)                           %! STAGE_NUMBER_MARKUP:SM3
                                %@%                 [1]                                              %! STAGE_NUMBER_MARKUP:SM3
                                %@%     }                                                            %! STAGE_NUMBER_MARKUP:SM3
                                }
                            }
            <BLANKLINE>
                        % GlobalSkips [measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [01]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [02]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [03]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 5]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [04]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 6]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [05]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 7]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [06]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 8]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                        \stopTextSpan                                                                %! SM29
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [07]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                % MusicVoice [measure 1]                                             %! SM4
                                fs''8
                                [
            <BLANKLINE>
                                e''8
            <BLANKLINE>
                                ef''8
            <BLANKLINE>
                                f''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 2]                                             %! SM4
                                a''8
                                [
            <BLANKLINE>
                                bf'8
            <BLANKLINE>
                                c''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 3]                                             %! SM4
                                b'8
                                [
            <BLANKLINE>
                                af'8
            <BLANKLINE>
                                g''8
            <BLANKLINE>
                                cs''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 4]                                             %! SM4
                                d''8
                                [
            <BLANKLINE>
                                fs'8
            <BLANKLINE>
                                e''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 5]                                             %! SM4
                                ef''8
                                [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                a'8
            <BLANKLINE>
                                bf'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 6]                                             %! SM4
                                c''8
                                [
            <BLANKLINE>
                                b'8
            <BLANKLINE>
                                af'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 7]                                             %! SM4
                                g'8
                                [
            <BLANKLINE>
                                cs''8
            <BLANKLINE>
                                d'8
            <BLANKLINE>
                                fs'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 8]                                             %! SM4
                                e'8
                                [
            <BLANKLINE>
                                ef'8
            <BLANKLINE>
                                f'8
                                ]
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        % GlobalSkips [measure 1]                                                    %! SM4
                        \once \override TextSpanner.Y-extent = ##f                                   %! SM29
                        \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29
                        \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29
                        \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29
                        \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29
                        \once \override TextSpanner.dash-period = 0                                  %! SM29
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                        \startTextSpan                                                               %! SM29
                        ^ \markup {
                            \column
                                {
                                %@% \line                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %@%     {                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %@%         \fontsize                                                %! MEASURE_INDEX_MARKUP:SM31
                                %@%             #3                                                   %! MEASURE_INDEX_MARKUP:SM31
                                %@%             \with-color                                          %! MEASURE_INDEX_MARKUP:SM31
                                %@%                 #(x11-color 'DarkCyan)                           %! MEASURE_INDEX_MARKUP:SM31
                                %@%                 [00]                                             %! MEASURE_INDEX_MARKUP:SM31
                                %@%     }                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %@% \line                                                            %! STAGE_NUMBER_MARKUP:SM3
                                %@%     {                                                            %! STAGE_NUMBER_MARKUP:SM3
                                %@%         \fontsize                                                %! STAGE_NUMBER_MARKUP:SM3
                                %@%             #3                                                   %! STAGE_NUMBER_MARKUP:SM3
                                %@%             \with-color                                          %! STAGE_NUMBER_MARKUP:SM3
                                %@%                 #(x11-color 'DarkCyan)                           %! STAGE_NUMBER_MARKUP:SM3
                                %@%                 [1]                                              %! STAGE_NUMBER_MARKUP:SM3
                                %@%     }                                                            %! STAGE_NUMBER_MARKUP:SM3
                                }
                            }
            <BLANKLINE>
                        % GlobalSkips [measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [01]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [02]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [03]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 5]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [04]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 6]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [05]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 7]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [06]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 8]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                        \stopTextSpan                                                                %! SM29
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [07]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                % MusicVoice [measure 1]                                             %! SM4
                                fs'8
                                [
            <BLANKLINE>
                                e'8
            <BLANKLINE>
                                ef'8
            <BLANKLINE>
                                f'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 2]                                             %! SM4
                                a'8
                                [
            <BLANKLINE>
                                bf'8
            <BLANKLINE>
                                c''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 3]                                             %! SM4
                                b'8
                                [
            <BLANKLINE>
                                af'8
            <BLANKLINE>
                                g'8
            <BLANKLINE>
                                cs''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 4]                                             %! SM4
                                d''8
                                [
            <BLANKLINE>
                                fs'8
            <BLANKLINE>
                                e''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 5]                                             %! SM4
                                ef''8
                                [
            <BLANKLINE>
                                f''8
            <BLANKLINE>
                                a'8
            <BLANKLINE>
                                bf'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 6]                                             %! SM4
                                c''8
                                [
            <BLANKLINE>
                                b'8
            <BLANKLINE>
                                af'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 7]                                             %! SM4
                                g''8
                                [
            <BLANKLINE>
                                cs''8
            <BLANKLINE>
                                d''8
            <BLANKLINE>
                                fs''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 8]                                             %! SM4
                                e''8
                                [
            <BLANKLINE>
                                ef''8
            <BLANKLINE>
                                f''8
                                ]
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        % GlobalSkips [measure 1]                                                    %! SM4
                        \once \override TextSpanner.Y-extent = ##f                                   %! SM29
                        \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29
                        \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29
                        \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29
                        \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29
                        \once \override TextSpanner.dash-period = 0                                  %! SM29
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                        \startTextSpan                                                               %! SM29
                        ^ \markup {
                            \column
                                {
                                %@% \line                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %@%     {                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %@%         \fontsize                                                %! MEASURE_INDEX_MARKUP:SM31
                                %@%             #3                                                   %! MEASURE_INDEX_MARKUP:SM31
                                %@%             \with-color                                          %! MEASURE_INDEX_MARKUP:SM31
                                %@%                 #(x11-color 'DarkCyan)                           %! MEASURE_INDEX_MARKUP:SM31
                                %@%                 [00]                                             %! MEASURE_INDEX_MARKUP:SM31
                                %@%     }                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %@% \line                                                            %! STAGE_NUMBER_MARKUP:SM3
                                %@%     {                                                            %! STAGE_NUMBER_MARKUP:SM3
                                %@%         \fontsize                                                %! STAGE_NUMBER_MARKUP:SM3
                                %@%             #3                                                   %! STAGE_NUMBER_MARKUP:SM3
                                %@%             \with-color                                          %! STAGE_NUMBER_MARKUP:SM3
                                %@%                 #(x11-color 'DarkCyan)                           %! STAGE_NUMBER_MARKUP:SM3
                                %@%                 [1]                                              %! STAGE_NUMBER_MARKUP:SM3
                                %@%     }                                                            %! STAGE_NUMBER_MARKUP:SM3
                                }
                            }
            <BLANKLINE>
                        % GlobalSkips [measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [01]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [02]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [03]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 5]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [04]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 6]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [05]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 7]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [06]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 8]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                        \stopTextSpan                                                                %! SM29
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [07]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                % MusicVoice [measure 1]                                             %! SM4
                                fs''8
                                [
            <BLANKLINE>
                                e''8
            <BLANKLINE>
                                ef''8
            <BLANKLINE>
                                f''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 2]                                             %! SM4
                                a'8
                                [
            <BLANKLINE>
                                bf'8
            <BLANKLINE>
                                c''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 3]                                             %! SM4
                                b'8
                                [
            <BLANKLINE>
                                af'8
            <BLANKLINE>
                                g'8
            <BLANKLINE>
                                cs''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 4]                                             %! SM4
                                d'8
                                [
            <BLANKLINE>
                                fs'8
            <BLANKLINE>
                                e'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 5]                                             %! SM4
                                ef'8
                                [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                a'8
            <BLANKLINE>
                                bf8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 6]                                             %! SM4
                                c'8
                                [
            <BLANKLINE>
                                b8
            <BLANKLINE>
                                af8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 7]                                             %! SM4
                                g8
                                [
            <BLANKLINE>
                                cs'8
            <BLANKLINE>
                                d'8
            <BLANKLINE>
                                fs8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 8]                                             %! SM4
                                e8
                                [
            <BLANKLINE>
                                ef8
            <BLANKLINE>
                                f8
                                ]
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
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        % GlobalSkips [measure 1]                                                    %! SM4
                        \once \override TextSpanner.Y-extent = ##f                                   %! SM29
                        \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29
                        \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29
                        \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29
                        \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29
                        \once \override TextSpanner.dash-period = 0                                  %! SM29
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                        \startTextSpan                                                               %! SM29
                        ^ \markup {
                            \column
                                {
                                %@% \line                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %@%     {                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %@%         \fontsize                                                %! MEASURE_INDEX_MARKUP:SM31
                                %@%             #3                                                   %! MEASURE_INDEX_MARKUP:SM31
                                %@%             \with-color                                          %! MEASURE_INDEX_MARKUP:SM31
                                %@%                 #(x11-color 'DarkCyan)                           %! MEASURE_INDEX_MARKUP:SM31
                                %@%                 [00]                                             %! MEASURE_INDEX_MARKUP:SM31
                                %@%     }                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %@% \line                                                            %! STAGE_NUMBER_MARKUP:SM3
                                %@%     {                                                            %! STAGE_NUMBER_MARKUP:SM3
                                %@%         \fontsize                                                %! STAGE_NUMBER_MARKUP:SM3
                                %@%             #3                                                   %! STAGE_NUMBER_MARKUP:SM3
                                %@%             \with-color                                          %! STAGE_NUMBER_MARKUP:SM3
                                %@%                 #(x11-color 'DarkCyan)                           %! STAGE_NUMBER_MARKUP:SM3
                                %@%                 [1]                                              %! STAGE_NUMBER_MARKUP:SM3
                                %@%     }                                                            %! STAGE_NUMBER_MARKUP:SM3
                                }
                            }
            <BLANKLINE>
                        % GlobalSkips [measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [01]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [02]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [03]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 5]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [04]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 6]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [05]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 7]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [06]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 8]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                        \stopTextSpan                                                                %! SM29
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             [07]                                                             %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                % MusicVoice [measure 1]                                             %! SM4
                                fs8
                                [
            <BLANKLINE>
                                e8
            <BLANKLINE>
                                ef8
            <BLANKLINE>
                                f8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 2]                                             %! SM4
                                a8
                                [
            <BLANKLINE>
                                bf8
            <BLANKLINE>
                                c'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 3]                                             %! SM4
                                b8
                                [
            <BLANKLINE>
                                af8
            <BLANKLINE>
                                g'8
            <BLANKLINE>
                                cs'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 4]                                             %! SM4
                                d'8
                                [
            <BLANKLINE>
                                fs'8
            <BLANKLINE>
                                e'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 5]                                             %! SM4
                                ef'8
                                [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                a'8
            <BLANKLINE>
                                bf'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 6]                                             %! SM4
                                c''8
                                [
            <BLANKLINE>
                                b'8
            <BLANKLINE>
                                af'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 7]                                             %! SM4
                                g'8
                                [
            <BLANKLINE>
                                cs''8
            <BLANKLINE>
                                d''8
            <BLANKLINE>
                                fs''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 8]                                             %! SM4
                                e''8
                                [
            <BLANKLINE>
                                ef''8
            <BLANKLINE>
                                f''8
                                ]
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
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
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
                                fs'16
                                [
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
                                d'''16
                                ]
                            }
                            {
                                fs'16
                                [
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
                                d'16
                                ]
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
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
                \new Staff <<
                    \context Voice = "Voice 1" {
                        \voiceOne
                        {
                            {
                                fs'16
                                [
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
                                d'16
                                ]
                            }
                            {
                                \once \override Accidental.color = #green
                                \once \override Beam.color = #green
                                \once \override Dots.color = #green
                                \once \override NoteHead.color = #green
                                \once \override Stem.color = #green
                                fs'16
                                [
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
                                d'''16
                                ]
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
            >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(lilypond_file[abjad.Staff], strict=89)
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
                                fs'16
                                [
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
                                d'''16
                                ]
                            }
                            {
                                \once \override Accidental.color = #blue
                                \once \override Beam.color = #blue
                                \once \override Dots.color = #blue
                                \once \override NoteHead.color = #blue
                                \once \override Stem.color = #blue
                                fs'16
                                [
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
                                d'''16
                                ]
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
