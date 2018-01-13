import abjad
import baca
from .ScoreTemplate import ScoreTemplate


class SingleStaffScoreTemplate(ScoreTemplate):
    r'''Single-staff score template.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
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
                                %@%                 m0                                               %! MEASURE_INDEX_MARKUP:SM31
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
                    %@%             m1                                                               %! MEASURE_INDEX_MARKUP:SM31
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
                    %@%             m2                                                               %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                        \stopTextSpan                                                                %! SM29
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             m3                                                               %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
            <BLANKLINE>
                            % MusicVoice [measure 1]                                                 %! SM4
                            R1 * 1/2
            <BLANKLINE>
                            % MusicVoice [measure 2]                                                 %! SM4
                            R1 * 3/8
            <BLANKLINE>
                            % MusicVoice [measure 3]                                                 %! SM4
                            R1 * 1/2
            <BLANKLINE>
                            % MusicVoice [measure 4]                                                 %! SM4
                            R1 * 3/8
            <BLANKLINE>
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls score template.

        Returns score.
        '''

        # GLOBAL CONTEXT
        global_context = self._make_global_context()

        # MUSIC VOICE, MUSIC STAFF
        music_voice = abjad.Voice(name='MusicVoice')
        music_staff = abjad.Staff(
            [music_voice],
            name='MusicStaff',
            )

#        abjad.annotate(
#            music_staff,
#            'default_clef',
#            abjad.Clef('treble'),
#            )

        # MUSIC CONTEXT
        music_context = abjad.Context(
            [music_staff],
            context_name='MusicContext',
            is_simultaneous=True,
            name='MusicContext',
            )

        # SCORE
        score = abjad.Score(
            [global_context, music_context],
            name='Score',
            )

        self._attach_calltime_defaults(score)

        return score
