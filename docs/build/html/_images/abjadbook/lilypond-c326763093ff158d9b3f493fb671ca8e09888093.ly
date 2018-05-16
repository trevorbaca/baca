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
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)         %! HSS1:SPACING
                \time 1/2                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 1/2
                
                % [GlobalSkips measure 2]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)         %! HSS1:SPACING
                \time 1/4                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 1/4
                \override Score.BarLine.transparent = ##f                                %! SM5
                \bar "|"                                                                 %! SM5
                
            }
        >>
        \context MusicContext = "MusicContext"
        <<
            \context Staff = "MusicStaff"
            \with
            {
                \override Beam.positions = #'(-5.5 . -5.5)
            }
            {
                \context Voice = "MusicVoice"
                {
                    {
                        \tweak text #tuplet-number::calc-fraction-text
                        \times 8/7 {
                            \scaleDurations #'(1 . 1) {
                                
                                % [MusicVoice measure 1]                                 %! SM4
                                \set stemLeftBeamCount = 0                               %! SM35
                                \set stemRightBeamCount = 2                              %! SM35
                                c'16
                                [                                                        %! SM35
                                
                                \set stemLeftBeamCount = 2                               %! SM35
                                \set stemRightBeamCount = 2                              %! SM35
                                d'16
                                
                                \set stemLeftBeamCount = 2                               %! SM35
                                \set stemRightBeamCount = 2                              %! SM35
                                bf'!16
                                
                                \set stemLeftBeamCount = 2                               %! SM35
                                \set stemRightBeamCount = 1                              %! SM35
                                fs''!16
                            }
                            \scaleDurations #'(1 . 1) {
                                
                                \set stemLeftBeamCount = 1                               %! SM35
                                \set stemRightBeamCount = 2                              %! SM35
                                e''16
                                
                                \set stemLeftBeamCount = 2                               %! SM35
                                \set stemRightBeamCount = 2                              %! SM35
                                ef''!16
                                
                                \set stemLeftBeamCount = 2                               %! SM35
                                \set stemRightBeamCount = 1                              %! SM35
                                b''16
                            }
                        }
                    }
                    {
                        \scaleDurations #'(1 . 1) {
                            
                            % [MusicVoice measure 2]                                     %! SM4
                            \set stemLeftBeamCount = 1                                   %! SM35
                            \set stemRightBeamCount = 2                                  %! SM35
                            g''16
                            
                            \set stemLeftBeamCount = 2                                   %! SM35
                            \set stemRightBeamCount = 2                                  %! SM35
                            cs''!16
                            
                            \set stemLeftBeamCount = 2                                   %! SM35
                            \set stemRightBeamCount = 2                                  %! SM35
                            a'16
                            
                            \set stemLeftBeamCount = 2                                   %! SM35
                            \set stemRightBeamCount = 0                                  %! SM35
                            af'!16
                            ]                                                            %! SM35
                            
                        }
                    }
                }
            }
        >>
    >>
}