import abjad
import baca
from .ScoreTemplate import ScoreTemplate


class StringTrioScoreTemplate(ScoreTemplate):
    r'''String trio score template.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score" <<
                \tag violin.viola.cello                                                              %! ST4
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
                    \context StringSectionStaffGroup = "String Section Staff Group" <<
                        \tag violin                                                                  %! ST4
                        \context ViolinMusicStaff = "ViolinMusicStaff" {
                            \context ViolinMusicVoice = "ViolinMusicVoice" {
            <BLANKLINE>
                                % ViolinMusicVoice [measure 1]                                       %! SM4
                                \set ViolinMusicStaff.instrumentName = \markup {                     %! DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! DEFAULT_INSTRUMENT:SM8
                                        Violin                                                       %! DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! DEFAULT_INSTRUMENT:SM8
                                \set ViolinMusicStaff.shortInstrumentName = \markup {                %! DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! DEFAULT_INSTRUMENT:SM8
                                        Vn.                                                          %! DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! DEFAULT_INSTRUMENT:SM8
                                \set ViolinMusicStaff.forceClef = ##t                                %! DEFAULT_CLEF:SM8
                                \clef "treble"                                                       %! DEFAULT_CLEF:SM8
                                \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! DEFAULT_INSTRUMENT_COLOR:SM6
                                \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:SM6
                            %@% \override ViolinMusicStaff.Clef.color = ##f                          %! DEFAULT_CLEF_COLOR_CANCELLATION:SM7
                                R1 * 1/2
                                ^ \markup {
                                    \column
                                        {
                                        %@% \line                                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%     {                                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%         \vcenter                                         %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             (Violin                                      %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%         \vcenter                                         %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             \hcenter-in                                  %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 #10                                      %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 Violin                                   %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%         \concat                                          %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             {                                            %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 \vcenter                                 %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                     \hcenter-in                          %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                         #10                              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                         Vn.                              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 \vcenter                                 %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                     )                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             }                                            %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%     }                                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            \line                                                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                {                                                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                    \with-color                                      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        #(x11-color 'DarkViolet)                     %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        {                                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \vcenter                                 %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                (Violin                              %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \vcenter                                 %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                \hcenter-in                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    #10                              %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    Violin                           %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \concat                                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                {                                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    \vcenter                         %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        \hcenter-in                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                            #10                      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                            Vn.                      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    \vcenter                         %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        )                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                }                                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        }                                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                }                                                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                        }
                                    }
                                \set ViolinMusicStaff.instrumentName = \markup {                     %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Violin                                                       %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \set ViolinMusicStaff.shortInstrumentName = \markup {                %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Vn.                                                          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %! REDRAWN_DEFAULT_INSTRUMENT_COLOR:SM6
                                \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)         %! DEFAULT_CLEF_REDRAW_COLOR:SM6
            <BLANKLINE>
                                % ViolinMusicVoice [measure 2]                                       %! SM4
                                R1 * 3/8
            <BLANKLINE>
                                % ViolinMusicVoice [measure 3]                                       %! SM4
                                R1 * 1/2
            <BLANKLINE>
                                % ViolinMusicVoice [measure 4]                                       %! SM4
                                R1 * 3/8
            <BLANKLINE>
                            }
                        }
                        \tag viola                                                                   %! ST4
                        \context ViolaMusicStaff = "ViolaMusicStaff" {
                            \context ViolaMusicVoice = "ViolaMusicVoice" {
            <BLANKLINE>
                                % ViolaMusicVoice [measure 1]                                        %! SM4
                                \set ViolaMusicStaff.instrumentName = \markup {                      %! DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! DEFAULT_INSTRUMENT:SM8
                                        Viola                                                        %! DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! DEFAULT_INSTRUMENT:SM8
                                \set ViolaMusicStaff.shortInstrumentName = \markup {                 %! DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! DEFAULT_INSTRUMENT:SM8
                                        Va.                                                          %! DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! DEFAULT_INSTRUMENT:SM8
                                \set ViolaMusicStaff.forceClef = ##t                                 %! DEFAULT_CLEF:SM8
                                \clef "alto"                                                         %! DEFAULT_CLEF:SM8
                                \once \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! DEFAULT_INSTRUMENT_COLOR:SM6
                                \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:SM6
                            %@% \override ViolaMusicStaff.Clef.color = ##f                           %! DEFAULT_CLEF_COLOR_CANCELLATION:SM7
                                R1 * 1/2
                                ^ \markup {
                                    \column
                                        {
                                        %@% \line                                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%     {                                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%         \vcenter                                         %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             (Viola                                       %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%         \vcenter                                         %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             \hcenter-in                                  %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 #10                                      %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 Viola                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%         \concat                                          %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             {                                            %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 \vcenter                                 %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                     \hcenter-in                          %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                         #10                              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                         Va.                              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 \vcenter                                 %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                     )                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             }                                            %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%     }                                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            \line                                                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                {                                                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                    \with-color                                      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        #(x11-color 'DarkViolet)                     %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        {                                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \vcenter                                 %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                (Viola                               %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \vcenter                                 %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                \hcenter-in                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    #10                              %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    Viola                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \concat                                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                {                                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    \vcenter                         %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        \hcenter-in                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                            #10                      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                            Va.                      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    \vcenter                         %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        )                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                }                                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        }                                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                }                                                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                        }
                                    }
                                \set ViolaMusicStaff.instrumentName = \markup {                      %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Viola                                                        %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \set ViolaMusicStaff.shortInstrumentName = \markup {                 %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Va.                                                          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'violet) %! REDRAWN_DEFAULT_INSTRUMENT_COLOR:SM6
                                \override ViolaMusicStaff.Clef.color = #(x11-color 'violet)          %! DEFAULT_CLEF_REDRAW_COLOR:SM6
            <BLANKLINE>
                                % ViolaMusicVoice [measure 2]                                        %! SM4
                                R1 * 3/8
            <BLANKLINE>
                                % ViolaMusicVoice [measure 3]                                        %! SM4
                                R1 * 1/2
            <BLANKLINE>
                                % ViolaMusicVoice [measure 4]                                        %! SM4
                                R1 * 3/8
            <BLANKLINE>
                            }
                        }
                        \tag cello                                                                   %! ST4
                        \context CelloMusicStaff = "CelloMusicStaff" {
                            \context CelloMusicVoice = "CelloMusicVoice" {
            <BLANKLINE>
                                % CelloMusicVoice [measure 1]                                        %! SM4
                                \set CelloMusicStaff.instrumentName = \markup {                      %! DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! DEFAULT_INSTRUMENT:SM8
                                        Cello                                                        %! DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! DEFAULT_INSTRUMENT:SM8
                                \set CelloMusicStaff.shortInstrumentName = \markup {                 %! DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! DEFAULT_INSTRUMENT:SM8
                                        Vc.                                                          %! DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! DEFAULT_INSTRUMENT:SM8
                                \set CelloMusicStaff.forceClef = ##t                                 %! DEFAULT_CLEF:SM8
                                \clef "bass"                                                         %! DEFAULT_CLEF:SM8
                                \once \override CelloMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! DEFAULT_INSTRUMENT_COLOR:SM6
                                \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:SM6
                            %@% \override CelloMusicStaff.Clef.color = ##f                           %! DEFAULT_CLEF_COLOR_CANCELLATION:SM7
                                R1 * 1/2
                                ^ \markup {
                                    \column
                                        {
                                        %@% \line                                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%     {                                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%         \vcenter                                         %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             (Cello                                       %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%         \vcenter                                         %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             \hcenter-in                                  %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 #10                                      %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 Cello                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%         \concat                                          %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             {                                            %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 \vcenter                                 %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                     \hcenter-in                          %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                         #10                              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                         Vc.                              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 \vcenter                                 %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                     )                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             }                                            %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%     }                                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            \line                                                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                {                                                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                    \with-color                                      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        #(x11-color 'DarkViolet)                     %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        {                                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \vcenter                                 %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                (Cello                               %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \vcenter                                 %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                \hcenter-in                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    #10                              %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    Cello                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \concat                                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                {                                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    \vcenter                         %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        \hcenter-in                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                            #10                      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                            Vc.                      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    \vcenter                         %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        )                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                }                                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        }                                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                }                                                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                        }
                                    }
                                \set CelloMusicStaff.instrumentName = \markup {                      %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Cello                                                        %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \set CelloMusicStaff.shortInstrumentName = \markup {                 %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                                      %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #10                                                          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Vc.                                                          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                                %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \override CelloMusicStaff.InstrumentName.color = #(x11-color 'violet) %! REDRAWN_DEFAULT_INSTRUMENT_COLOR:SM6
                                \override CelloMusicStaff.Clef.color = #(x11-color 'violet)          %! DEFAULT_CLEF_REDRAW_COLOR:SM6
            <BLANKLINE>
                                % CelloMusicVoice [measure 2]                                        %! SM4
                                R1 * 3/8
            <BLANKLINE>
                                % CelloMusicVoice [measure 3]                                        %! SM4
                                R1 * 1/2
            <BLANKLINE>
                                % CelloMusicVoice [measure 4]                                        %! SM4
                                R1 * 3/8
            <BLANKLINE>
                            }
                        }
                    >>
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls string trio score template.

        Returns score.
        '''
        global_context = self._make_global_context()
        instrument_tags = (
            'violin',
            'viola',
            'cello',
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
            markup=baca.markup.instrument('Violin', hcenter_in=10),
            short_markup=baca.markup.short_instrument(
                'Vn.',
                hcenter_in=10,
                ),
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

        # VIOLA
        viola_music_voice = abjad.Voice(
            [],
            context_name='ViolaMusicVoice',
            name='ViolaMusicVoice',
            )
        viola_music_staff = abjad.Staff(
            [viola_music_voice],
            context_name='ViolaMusicStaff',
            name='ViolaMusicStaff',
            )
        abjad.annotate(
            viola_music_staff,
            'default_instrument',
            abjad.Viola(
                markup=baca.markup.instrument('Viola', hcenter_in=10),
                short_markup=baca.markup.short_instrument(
                    'Va.',
                    hcenter_in=10,
                    ),
                ),
            )
        abjad.annotate(
            viola_music_staff,
            'default_clef',
            abjad.Clef('alto'),
            )
        self._attach_tag('viola', viola_music_staff)

        # CELLO
        cello_music_voice = abjad.Voice(
            [],
            context_name='CelloMusicVoice',
            name='CelloMusicVoice',
            )
        cello_music_staff = abjad.Staff(
            [cello_music_voice],
            context_name='CelloMusicStaff',
            name='CelloMusicStaff',
            )
        abjad.annotate(
            cello_music_staff,
            'default_instrument',
            abjad.Cello(
                markup=baca.markup.instrument('Cello', hcenter_in=10),
                short_markup=baca.markup.short_instrument(
                    'Vc.',
                    hcenter_in=10,
                    ),
                ),
            )
        abjad.annotate(
            cello_music_staff,
            'default_clef',
            abjad.Clef('bass'),
            )
        self._attach_tag('cello', cello_music_staff)

        # SCORE
        string_section_staff_group = abjad.StaffGroup(
            [
                violin_music_staff,
                viola_music_staff,
                cello_music_staff,
                ],
            context_name='StringSectionStaffGroup',
            name='String Section Staff Group',
            )
        music_context = abjad.Context(
            [
                string_section_staff_group,
                ],
            context_name='MusicContext',
            is_simultaneous=True,
            name='MusicContext',
            )
        score = abjad.Score(
            [
                global_context,
                music_context,
                ],
            name='Score',
            )
        return score
