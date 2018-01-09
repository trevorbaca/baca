import abjad
import baca


class LayoutMeasureMap(abjad.AbjadObject):
    r'''Layout measure map.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8), (4, 8)],
        ...     layout_measure_map=baca.LayoutMeasureMap([
        ...         baca.line_break(baca.skip(0)),
        ...         baca.lbsd(100, [30, 30], baca.skip(1)),
        ...         baca.line_break(baca.skip(1)),
        ...         ]),
        ...     )

        >>> maker(
        ...     baca.scope('ViolinMusicVoice', 1),
        ...     baca.make_even_runs(),
        ...     baca.pitches('E4', repeats=True),
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
                        \autoPageBreaksOff                                                           %! SEGMENT_LAYOUT:LMM1
                        \noBreak                                                                     %! SEGMENT_LAYOUT:LMM2
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
                        ^ \markup {                                                                  %! STAGE_NUMBER_MARKUP:SM3
                            \fontsize                                                                %! STAGE_NUMBER_MARKUP:SM3
                                #-3                                                                  %! STAGE_NUMBER_MARKUP:SM3
                                \with-color                                                          %! STAGE_NUMBER_MARKUP:SM3
                                    #(x11-color 'DarkCyan)                                           %! STAGE_NUMBER_MARKUP:SM3
                                    [1]                                                              %! STAGE_NUMBER_MARKUP:SM3
                            }                                                                        %! STAGE_NUMBER_MARKUP:SM3
                        \break                                                                       %! SEGMENT_LAYOUT:LMM3
            <BLANKLINE>
                        % GlobalSkips [measure 2]                                                    %! SM4
                        \noBreak                                                                     %! SEGMENT_LAYOUT:LMM2
                        \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! SEGMENT_LAYOUT:LMM3
                        #'((Y-offset . 100) (alignment-distances . (30 30)))                         %! SEGMENT_LAYOUT:LMM3
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                        \break                                                                       %! SEGMENT_LAYOUT:LMM3
            <BLANKLINE>
                        % GlobalSkips [measure 3]                                                    %! SM4
                        \noBreak                                                                     %! SEGMENT_LAYOUT:LMM2
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
            <BLANKLINE>
                        % GlobalSkips [measure 4]                                                    %! SM4
                        \noBreak                                                                     %! SEGMENT_LAYOUT:LMM2
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
            <BLANKLINE>
                        % GlobalSkips [measure 5]                                                    %! SM4
                        \noBreak                                                                     %! SEGMENT_LAYOUT:LMM2
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
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
                                {
            <BLANKLINE>
                                    % ViolinMusicVoice [measure 1]                                   %! SM4
                                    \set ViolinMusicStaff.instrumentName = \markup {                 %! DEFAULT_INSTRUMENT:SM8
                                        \hcenter-in                                                  %! DEFAULT_INSTRUMENT:SM8
                                            #10                                                      %! DEFAULT_INSTRUMENT:SM8
                                            Violin                                                   %! DEFAULT_INSTRUMENT:SM8
                                        }                                                            %! DEFAULT_INSTRUMENT:SM8
                                    \set ViolinMusicStaff.shortInstrumentName = \markup {            %! DEFAULT_INSTRUMENT:SM8
                                        \hcenter-in                                                  %! DEFAULT_INSTRUMENT:SM8
                                            #10                                                      %! DEFAULT_INSTRUMENT:SM8
                                            Vn.                                                      %! DEFAULT_INSTRUMENT:SM8
                                        }                                                            %! DEFAULT_INSTRUMENT:SM8
                                    \set ViolinMusicStaff.forceClef = ##t                            %! DEFAULT_CLEF:SM8
                                    \clef "treble"                                                   %! DEFAULT_CLEF:SM8
                                    \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! DEFAULT_INSTRUMENT_COLOR:SM6
                                    \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:SM6
                                %F% \override ViolinMusicStaff.Clef.color = ##f                      %! DEFAULT_CLEF_COLOR_CANCELLATION:SM7
                                    e'8
                                    [
                                    ^ \markup {
                                        \column
                                            {
                                            %F% \line                                                %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            %F%     {                                                %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            %F%         \vcenter                                     %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            %F%             (Violin                                  %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            %F%         \vcenter                                     %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            %F%             \hcenter-in                              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            %F%                 #10                                  %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            %F%                 Violin                               %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            %F%         \concat                                      %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            %F%             {                                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            %F%                 \vcenter                             %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            %F%                     \hcenter-in                      %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            %F%                         #10                          %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            %F%                         Vn.                          %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            %F%                 \vcenter                             %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            %F%                     )                                %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            %F%             }                                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            %F%     }                                                %! DEFAULT_INSTRUMENT_ALERT:SM10
                                                \line                                                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                    {                                                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        \with-color                                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            #(x11-color 'DarkViolet)                 %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            {                                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                \vcenter                             %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    (Violin                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                \vcenter                             %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    \hcenter-in                      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        #10                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        Violin                       %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                \concat                              %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    {                                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        \vcenter                     %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                            \hcenter-in              %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                                #10                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                                Vn.                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        \vcenter                     %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                            )                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    }                                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            }                                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                    }                                                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                            }
                                        }
                                    \set ViolinMusicStaff.instrumentName = \markup {                 %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        \hcenter-in                                                  %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                            #10                                                      %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                            Violin                                                   %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        }                                                            %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \set ViolinMusicStaff.shortInstrumentName = \markup {            %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        \hcenter-in                                                  %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                            #10                                                      %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                            Vn.                                                      %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        }                                                            %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %! REDRAWN_DEFAULT_INSTRUMENT_COLOR:SM6
                                    \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)     %! DEFAULT_CLEF_REDRAW_COLOR:SM6
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
            <BLANKLINE>
                                    % ViolinMusicVoice [measure 2]                                   %! SM4
                                    e'8
                                    [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
            <BLANKLINE>
                                    % ViolinMusicVoice [measure 3]                                   %! SM4
                                    e'8
                                    [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
            <BLANKLINE>
                                    % ViolinMusicVoice [measure 4]                                   %! SM4
                                    e'8
                                    [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
            <BLANKLINE>
                                    % ViolinMusicVoice [measure 5]                                   %! SM4
                                    e'8
                                    [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
            <BLANKLINE>
                                }
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
                            %F% \override ViolaMusicStaff.Clef.color = ##f                           %! DEFAULT_CLEF_COLOR_CANCELLATION:SM7
                                R1 * 1/2
                                ^ \markup {
                                    \column
                                        {
                                        %F% \line                                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%     {                                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%         \vcenter                                         %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%             (Viola                                       %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%         \vcenter                                         %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%             \hcenter-in                                  %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%                 #10                                      %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%                 Viola                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%         \concat                                          %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%             {                                            %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%                 \vcenter                                 %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%                     \hcenter-in                          %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%                         #10                              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%                         Va.                              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%                 \vcenter                                 %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%                     )                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%             }                                            %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%     }                                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
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
                                % ViolaMusicVoice [measure 5]                                        %! SM4
                                R1 * 1/2
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
                            %F% \override CelloMusicStaff.Clef.color = ##f                           %! DEFAULT_CLEF_COLOR_CANCELLATION:SM7
                                R1 * 1/2
                                ^ \markup {
                                    \column
                                        {
                                        %F% \line                                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%     {                                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%         \vcenter                                         %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%             (Cello                                       %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%         \vcenter                                         %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%             \hcenter-in                                  %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%                 #10                                      %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%                 Cello                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%         \concat                                          %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%             {                                            %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%                 \vcenter                                 %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%                     \hcenter-in                          %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%                         #10                              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%                         Vc.                              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%                 \vcenter                                 %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%                     )                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%             }                                            %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %F%     }                                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
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
                                % CelloMusicVoice [measure 5]                                        %! SM4
                                R1 * 1/2
            <BLANKLINE>
                            }
                        }
                    >>
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_build',
        '_commands',
        '_tag',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, commands=None, build=None):
        self._build = build
        tag = baca.Tags.build(baca.Tags.LAYOUT, build=build)
        self._tag = tag
        if commands is not None:
            commands_ = []
            for command in commands:
                command_ = abjad.new(command, site='LMM3', tag=self.tag)
                commands_.append(command_)
            commands = commands_
            commands = tuple(commands)
        self._commands = commands

    ### SPECIAL METHODS ###

    def __call__(self, context=None):
        r'''Calls map on `context`.

        Returns none.
        '''
        if context is None:
            return
        skips = baca.select(context).skips()
        literal = abjad.LilyPondLiteral(r'\autoPageBreaksOff', 'before')
        abjad.attach(literal, skips[0], site='LMM1', tag=self.tag)
        for skip in skips:
            if not abjad.inspect(skip).has_indicator(baca.LBSD):
                literal = abjad.LilyPondLiteral(r'\noBreak', 'before')
                abjad.attach(literal, skip, site='LMM2', tag=self.tag)
        for command in self.commands:
            command(context)

    ### PUBLIC PROPERTIES ###

    @property
    def build(self):
        r'''Gets build.
        '''
        return self._build

    @property
    def commands(self):
        r'''Gets commands.

        ..  container:: example

            >>> layout = baca.LayoutMeasureMap([
            ...     baca.line_break(baca.skip(0)),
            ...     baca.page_break(baca.skip(1)),
            ...     ])

            >>> for command in layout.commands:
            ...     abjad.f(command)
            ...
            baca.IndicatorCommand(
                indicators=abjad.CyclicTuple(
                    [
                        abjad.LilyPondLiteral('\\break', format_slot='after', ),
                        ]
                    ),
                selector=baca.skip(0),
                site='LMM3',
                tag='SEGMENT_LAYOUT',
                )
            baca.IndicatorCommand(
                indicators=abjad.CyclicTuple(
                    [
                        abjad.LilyPondLiteral('\\pageBreak', format_slot='after', ),
                        ]
                    ),
                selector=baca.skip(1),
                site='LMM3',
                tag='SEGMENT_LAYOUT',
                )

        Returns commands.
        '''
        return self._commands

    @property
    def tag(self):
        r'''Gets tag.
        '''
        return self._tag
