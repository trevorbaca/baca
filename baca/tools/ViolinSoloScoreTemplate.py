import abjad
import baca
from .ScoreTemplate import ScoreTemplate


class ViolinSoloScoreTemplate(ScoreTemplate):
    r'''Violin solo score template.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.ViolinSoloScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score" <<
                \tag violin                                                                          %! ST4
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
            <BLANKLINE>
                        % GlobalSkips [measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
            <BLANKLINE>
                        % GlobalSkips [measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
            <BLANKLINE>
                        % GlobalSkips [measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                        \stopTextSpan                                                                %! SM29
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \tag violin                                                                      %! ST4
                    \context ViolinMusicStaff = "ViolinMusicStaff" {
                        \context ViolinMusicVoice = "ViolinMusicVoice" {
            <BLANKLINE>
                            % ViolinMusicVoice [measure 1]                                           %! SM4
                            \set ViolinMusicStaff.instrumentName = \markup {                         %! DEFAULT_INSTRUMENT:SM8
                                \hcenter-in                                                          %! DEFAULT_INSTRUMENT:SM8
                                    #16                                                              %! DEFAULT_INSTRUMENT:SM8
                                    Violin                                                           %! DEFAULT_INSTRUMENT:SM8
                                }                                                                    %! DEFAULT_INSTRUMENT:SM8
                            \set ViolinMusicStaff.shortInstrumentName = \markup {                    %! DEFAULT_INSTRUMENT:SM8
                                \hcenter-in                                                          %! DEFAULT_INSTRUMENT:SM8
                                    #10                                                              %! DEFAULT_INSTRUMENT:SM8
                                    Vn.                                                              %! DEFAULT_INSTRUMENT:SM8
                                }                                                                    %! DEFAULT_INSTRUMENT:SM8
                            \set ViolinMusicStaff.forceClef = ##t                                    %! DEFAULT_CLEF:SM8
                            \clef "treble"                                                           %! DEFAULT_CLEF:SM8
                            \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! DEFAULT_INSTRUMENT_COLOR:SM6
                            \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet)   %! DEFAULT_CLEF_COLOR:SM6
                        %@% \override ViolinMusicStaff.Clef.color = ##f                              %! DEFAULT_CLEF_COLOR_CANCELLATION:SM7
                            R1 * 1/2
                            ^ \markup {
                                \column
                                    {
                                    %@% \line                                                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%     {                                                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%         \vcenter                                             %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%             (Violin                                          %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%         \vcenter                                             %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%             \hcenter-in                                      %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                 #16                                          %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                 Violin                                       %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%         \concat                                              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%             {                                                %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                 \vcenter                                     %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                     \hcenter-in                              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                         #10                                  %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                         Vn.                                  %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                 \vcenter                                     %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                     )                                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%             }                                                %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%     }                                                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        \line                                                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                            {                                                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                \with-color                                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                    #(x11-color 'DarkViolet)                         %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                    {                                                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        \vcenter                                     %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            (Violin                                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        \vcenter                                     %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \hcenter-in                              %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                #16                                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                Violin                               %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        \concat                                      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            {                                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                \vcenter                             %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    \hcenter-in                      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        #10                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        Vn.                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                \vcenter                             %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    )                                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            }                                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                    }                                                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                            }                                                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                    }
                                }
                            \set ViolinMusicStaff.instrumentName = \markup {                         %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \hcenter-in                                                          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    #16                                                              %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    Violin                                                           %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                }                                                                    %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                            \set ViolinMusicStaff.shortInstrumentName = \markup {                    %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \hcenter-in                                                          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    #10                                                              %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    Vn.                                                              %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                }                                                                    %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                            \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet)   %! REDRAWN_DEFAULT_INSTRUMENT_COLOR:SM6
                            \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)             %! DEFAULT_CLEF_REDRAW_COLOR:SM6
            <BLANKLINE>
                            % ViolinMusicVoice [measure 2]                                           %! SM4
                            R1 * 3/8
            <BLANKLINE>
                            % ViolinMusicVoice [measure 3]                                           %! SM4
                            R1 * 1/2
            <BLANKLINE>
                            % ViolinMusicVoice [measure 4]                                           %! SM4
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
        r'''Calls violin solo score template.

        Returns score.
        '''
        # GLOBAL CONTEXT
        global_context = self._make_global_context()
        instrument_tags = (
            'violin',
            )
        tag_string = '.'.join(instrument_tags)
        self._attach_tag(tag_string, global_context)

        # VIOLIN
        violin_music_voice = abjad.Voice(
            [],
            context_name='ViolinMusicVoice',
            name='ViolinMusicVoice',
            )
        violin_music_staff = abjad.Staff(
            [violin_music_voice],
            context_name='ViolinMusicStaff',
            name='ViolinMusicStaff',
            )
        violin = abjad.Violin(
            markup=baca.markup.instrument('Violin'),
            short_markup=baca.markup.short_instrument('Vn.'),
            )
        abjad.annotate(
            violin_music_staff,
            'default_instrument',
            violin,
            )
        abjad.annotate(
            violin_music_staff,
            'default_clef',
            abjad.Clef('treble'),
            )
        self._attach_tag('violin', violin_music_staff)

        # MUSIC ONTEXT
        music_context = abjad.Context(
            [violin_music_staff],
            context_name='MusicContext',
            is_simultaneous=True,
            name='MusicContext',
            )

        # SCORE
        score = abjad.Score(
            [global_context, music_context],
            name='Score',
            )
        return score
