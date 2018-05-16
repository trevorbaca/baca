\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "../../../../source/_stylesheets/string-trio-stylesheet.ily"

\score {
    \context Score = "Score"
    \with
    {
        \override SpacingSpanner.strict-grace-spacing = ##f
        \override SpacingSpanner.strict-note-spacing = ##f
    }
    <<
        \context GlobalContext = "GlobalContext"
        <<
            \context GlobalSkips = "GlobalSkips"
            {
                
                % [GlobalSkips measure 1]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)         %! HSS1:SPACING
                \time 3/16                                                               %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 3/16
                
                % [GlobalSkips measure 2]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)         %! HSS1:SPACING
                \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)      %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                s1 * 3/16
                
                % [GlobalSkips measure 3]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)         %! HSS1:SPACING
                \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)      %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                s1 * 3/16
                
                % [GlobalSkips measure 4]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)         %! HSS1:SPACING
                \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)      %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                s1 * 3/16
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
                            \makeMagenta                                                 %! SM25
                            e'8.
                        }
                    }
                    {
                        \scaleDurations #'(1 . 1) {
                            
                            % [MusicVoice measure 2]                                     %! SM4
                            \acciaccatura {
                                
                                \makeMagenta                                             %! SM25
                                fs'16
                                [                                                        %! ACC1
                                
                                \makeMagenta                                             %! SM25
                                d'16
                                
                                \makeMagenta                                             %! SM25
                                ef'16
                                
                                \makeMagenta                                             %! SM25
                                f'16
                                
                                \makeMagenta                                             %! SM25
                                a'16
                                
                                \makeMagenta                                             %! SM25
                                af'16
                                ]                                                        %! ACC1
                                
                            }
                            \makeMagenta                                                 %! SM25
                            c'8.
                        }
                    }
                    {
                        \scaleDurations #'(1 . 1) {
                            
                            % [MusicVoice measure 3]                                     %! SM4
                            \makeMagenta                                                 %! SM25
                            b'8.
                        }
                    }
                    {
                        \scaleDurations #'(1 . 1) {
                            
                            % [MusicVoice measure 4]                                     %! SM4
                            \acciaccatura {
                                
                                \makeMagenta                                             %! SM25
                                bf'16
                                [                                                        %! ACC1
                                
                                \makeMagenta                                             %! SM25
                                g'16
                                
                                \makeMagenta                                             %! SM25
                                a'16
                                
                                \makeMagenta                                             %! SM25
                                af'16
                                
                                \makeMagenta                                             %! SM25
                                c'16
                                ]                                                        %! ACC1
                                
                            }
                            \makeMagenta                                                 %! SM25
                            f'8.
                            
                        }
                    }
                }
            }
        >>
    >>
}