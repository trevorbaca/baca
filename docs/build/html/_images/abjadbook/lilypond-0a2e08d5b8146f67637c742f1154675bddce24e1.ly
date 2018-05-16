\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "../../../../source/_stylesheets/string-trio-stylesheet.ily"

\score {
    \context Score = "Score"
    <<
        \context GlobalContext = "GlobalContext"
        <<
            \context GlobalSkips = "GlobalSkips"
            {
                
                % [GlobalSkips measure 1]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)         %! HSS1:SPACING
                \time 5/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 5/8
                
                % [GlobalSkips measure 2]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)         %! HSS1:SPACING
                \time 2/16                                                               %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 1/8
                \override Score.BarLine.transparent = ##f                                %! SM5
                \bar "|"                                                                 %! SM5
                
            }
        >>
        \context MusicContext = "MusicContext"
        <<
            \context StringSectionStaffGroup = "String Section Staff Group"
            <<
                \tag Violin                                                              %! ST4
                \context ViolinMusicStaff = "ViolinMusicStaff"
                {
                    \context ViolinMusicVoice = "ViolinMusicVoice"
                    {
                        {
                            \scaleDurations #'(1 . 1) {
                                
                                % [ViolinMusicVoice measure 1]                           %! SM4
                                \override Stem.direction = #up                           %! OC1
                                \set ViolinMusicStaff.instrumentName = \markup {         %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \hcenter-in                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                        #10                                              %! SM8:DEFAULT_INSTRUMENT:ST1
                                        Violin                                           %! SM8:DEFAULT_INSTRUMENT:ST1
                                    }                                                    %! SM8:DEFAULT_INSTRUMENT:ST1
                                \set ViolinMusicStaff.shortInstrumentName = \markup {    %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \hcenter-in                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                        #10                                              %! SM8:DEFAULT_INSTRUMENT:ST1
                                        Vn.                                              %! SM8:DEFAULT_INSTRUMENT:ST1
                                    }                                                    %! SM8:DEFAULT_INSTRUMENT:ST1
                                \clef "treble"                                           %! SM8:DEFAULT_CLEF:ST3
                                \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                            %@% \override ViolinMusicStaff.Clef.color = ##f              %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                \set ViolinMusicStaff.forceClef = ##t                    %! SM8:DEFAULT_CLEF:SM33:ST3
                                a'8
                                ^ \markup {                                              %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \with-color                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        #(x11-color 'DarkViolet)                         %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        (Violin)                                         %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    }                                                    %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                \set ViolinMusicStaff.instrumentName = \markup {         %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \hcenter-in                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        #10                                              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        Violin                                           %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    }                                                    %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                \set ViolinMusicStaff.shortInstrumentName = \markup {    %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \hcenter-in                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        #10                                              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        Vn.                                              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    }                                                    %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                \override ViolinMusicStaff.Clef.color = #(x11-color 'violet) %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
                                
                                b'8
                                
                                c''8
                                
                                d''8
                                
                                e''8
                                \revert Stem.direction                                   %! OC2
                            }
                        }
                        {
                            \scaleDurations #'(1 . 1) {
                                
                                % [ViolinMusicVoice measure 2]                           %! SM4
                                ef''!8
                                
                            }
                        }
                    }
                }
                \tag Viola                                                               %! ST4
                \context ViolaMusicStaff = "ViolaMusicStaff"
                {
                    \context ViolaMusicVoice = "ViolaMusicVoice"
                    {
                        {
                            \scaleDurations #'(1 . 1) {
                                
                                % [ViolaMusicVoice measure 1]                            %! SM4
                                \override Stem.direction = #up                           %! OC1
                                \set ViolaMusicStaff.instrumentName = \markup {          %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \hcenter-in                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                        #10                                              %! SM8:DEFAULT_INSTRUMENT:ST1
                                        Viola                                            %! SM8:DEFAULT_INSTRUMENT:ST1
                                    }                                                    %! SM8:DEFAULT_INSTRUMENT:ST1
                                \set ViolaMusicStaff.shortInstrumentName = \markup {     %! SM8:DEFAULT_INSTRUMENT:ST1
                                    \hcenter-in                                          %! SM8:DEFAULT_INSTRUMENT:ST1
                                        #10                                              %! SM8:DEFAULT_INSTRUMENT:ST1
                                        Va.                                              %! SM8:DEFAULT_INSTRUMENT:ST1
                                    }                                                    %! SM8:DEFAULT_INSTRUMENT:ST1
                                \clef "alto"                                             %! SM8:DEFAULT_CLEF:ST3
                                \crossStaff                                              %! IC
                                \once \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                                \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                            %@% \override ViolaMusicStaff.Clef.color = ##f               %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                                \set ViolaMusicStaff.forceClef = ##t                     %! SM8:DEFAULT_CLEF:SM33:ST3
                                c'8
                                ^ \markup {                                              %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    \with-color                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        #(x11-color 'DarkViolet)                         %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                        (Viola)                                          %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                    }                                                    %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                                \set ViolaMusicStaff.instrumentName = \markup {          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \hcenter-in                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        #10                                              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        Viola                                            %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    }                                                    %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                \set ViolaMusicStaff.shortInstrumentName = \markup {     %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    \hcenter-in                                          %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        #10                                              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                        Va.                                              %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                    }                                                    %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                \override ViolaMusicStaff.Clef.color = #(x11-color 'violet) %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
                                
                                d'8
                                
                                e'8
                                
                                f'8
                                
                                g'8
                                \revert Stem.direction                                   %! OC2
                            }
                        }
                        
                        % [ViolaMusicVoice measure 2]                                    %! SM4
                        R1 * 1/8
                        
                    }
                }
                \tag Cello                                                               %! ST4
                \context CelloMusicStaff = "CelloMusicStaff"
                {
                    \context CelloMusicVoice = "CelloMusicVoice"
                    {
                        
                        % [CelloMusicVoice measure 1]                                    %! SM4
                        \set CelloMusicStaff.instrumentName = \markup {                  %! SM8:DEFAULT_INSTRUMENT:ST1
                            \hcenter-in                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                #10                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                Cello                                                    %! SM8:DEFAULT_INSTRUMENT:ST1
                            }                                                            %! SM8:DEFAULT_INSTRUMENT:ST1
                        \set CelloMusicStaff.shortInstrumentName = \markup {             %! SM8:DEFAULT_INSTRUMENT:ST1
                            \hcenter-in                                                  %! SM8:DEFAULT_INSTRUMENT:ST1
                                #10                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                                Vc.                                                      %! SM8:DEFAULT_INSTRUMENT:ST1
                            }                                                            %! SM8:DEFAULT_INSTRUMENT:ST1
                        \clef "bass"                                                     %! SM8:DEFAULT_CLEF:ST3
                        \once \override CelloMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_INSTRUMENT_COLOR:ST1
                        \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_CLEF_COLOR:ST3
                    %@% \override CelloMusicStaff.Clef.color = ##f                       %! SM7:DEFAULT_CLEF_COLOR_CANCELLATION:ST3
                        \set CelloMusicStaff.forceClef = ##t                             %! SM8:DEFAULT_CLEF:SM33:ST3
                        R1 * 5/8
                        ^ \markup {                                                      %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                            \with-color                                                  %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                #(x11-color 'DarkViolet)                                 %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                                (Cello)                                                  %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                            }                                                            %! SM11:DEFAULT_INSTRUMENT_ALERT:ST1
                        \override CelloMusicStaff.InstrumentName.color = #(x11-color 'violet) %! SM6:REDRAWN_DEFAULT_INSTRUMENT_COLOR:ST1
                        \set CelloMusicStaff.instrumentName = \markup {                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                            \hcenter-in                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                #10                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                Cello                                                    %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                            }                                                            %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                        \set CelloMusicStaff.shortInstrumentName = \markup {             %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                            \hcenter-in                                                  %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                #10                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                                Vc.                                                      %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                            }                                                            %! SM8:REDRAWN_DEFAULT_INSTRUMENT:SM34:ST1
                        \override CelloMusicStaff.Clef.color = #(x11-color 'violet)      %! SM6:DEFAULT_CLEF_REDRAW_COLOR:ST3
                        
                        % [CelloMusicVoice measure 2]                                    %! SM4
                        R1 * 1/8
                        
                    }
                }
            >>
        >>
    >>
}