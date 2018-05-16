\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "../../../../source/_stylesheets/string-trio-stylesheet.ily"

\score {
    \context Score = "Score"
    \with
    {
        autoBeaming = ##f
    }
    <<
        \context GlobalContext = "GlobalContext"
        <<
            \context GlobalSkips = "GlobalSkips"
            {
                
                % [GlobalSkips measure 1]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)         %! HSS1:SPACING
                \time 1/16                                                               %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 1/16
                
                % [GlobalSkips measure 2]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)         %! HSS1:SPACING
                \time 7/16                                                               %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 7/16
                
                % [GlobalSkips measure 3]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)         %! HSS1:SPACING
                \time 1/16                                                               %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 1/16
                
                % [GlobalSkips measure 4]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)         %! HSS1:SPACING
                \time 3/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 3/8
                \override Score.BarLine.transparent = ##f                                %! SM5
                \bar "|"                                                                 %! SM5
                
            }
        >>
        \context MusicContext = "MusicContext"
        <<
            \context Staff = "MusicStaff"
            {
                \context Voice = "MusicVoice"
                {
                    {
                        \scaleDurations #'(1 . 1) {
                            
                            % [MusicVoice measure 1]                                     %! SM4
                            \set Staff.instrumentName = \markup { Violin }               %! SM8:EXPLICIT_INSTRUMENT:IC
                            \set Staff.shortInstrumentName = \markup { Vn. }             %! SM8:EXPLICIT_INSTRUMENT:IC
                            \once \override Staff.InstrumentName.color = #(x11-color 'blue) %! SM6:EXPLICIT_INSTRUMENT_COLOR:IC
                            e'16
                            ^ \markup {                                                  %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                \with-color                                              %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    #(x11-color 'blue)                                   %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                    (Violin)                                             %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                }                                                        %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! SM6:REDRAWN_EXPLICIT_INSTRUMENT_COLOR:IC
                            \set Staff.instrumentName = \markup { Violin }               %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                            \set Staff.shortInstrumentName = \markup { Vn. }             %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                        }
                    }
                    {
                        \scaleDurations #'(1 . 1) {
                            
                            % [MusicVoice measure 2]                                     %! SM4
                            \makeRed                                                     %! SM13
                            c16
                            - \tweak color #red                                          %! SM13
                            ^ \markup { * }                                              %! SM13
                            
                            d'16
                            
                            ef'!16
                            
                            f'16
                            
                            af'!16
                            
                            a'16
                            
                            c'16
                        }
                    }
                    {
                        \scaleDurations #'(1 . 1) {
                            
                            % [MusicVoice measure 3]                                     %! SM4
                            b'16
                        }
                    }
                    {
                        \scaleDurations #'(1 . 1) {
                            
                            % [MusicVoice measure 4]                                     %! SM4
                            bf'!16
                            
                            g'16
                            
                            a'16
                            
                            bf'!16
                            
                            c'16
                            
                            f'16
                            
                        }
                    }
                }
            }
        >>
    >>
}