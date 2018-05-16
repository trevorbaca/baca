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
                \time 3/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 3/8
                
                % [GlobalSkips measure 2]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)         %! HSS1:SPACING
                \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)      %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                s1 * 3/8
                
                % [GlobalSkips measure 3]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)         %! HSS1:SPACING
                \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)      %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                s1 * 3/8
                
                % [GlobalSkips measure 4]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)         %! HSS1:SPACING
                \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)      %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                s1 * 3/8
                
                % [GlobalSkips measure 5]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)         %! HSS1:SPACING
                \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)      %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
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
                        
                        % [MusicVoice measure 1]                                         %! SM4
                        \makeBlue                                                        %! SM24
                        c'8
                        [
                        
                        \makeBlue                                                        %! SM24
                        c'8
                        
                        \makeBlue                                                        %! SM24
                        c'8
                        ]
                    }
                    {
                        
                        % [MusicVoice measure 2]                                         %! SM4
                        \makeBlue                                                        %! SM24
                        c'8
                        [
                        
                        \makeBlue                                                        %! SM24
                        c'8
                        
                        \makeBlue                                                        %! SM24
                        c'8
                        ]
                    }
                    
                    % [MusicVoice measure 3]                                             %! SM4
                    \makeBlue                                                            %! SM24
                    c'4.
                    {
                        
                        % [MusicVoice measure 4]                                         %! SM4
                        \makeBlue                                                        %! SM24
                        c'8
                        [
                        
                        \makeBlue                                                        %! SM24
                        c'8
                        
                        \makeBlue                                                        %! SM24
                        c'8
                        ]
                    }
                    
                    % [MusicVoice measure 5]                                             %! SM4
                    \makeBlue                                                            %! SM24
                    c'4.
                    
                }
            }
        >>
    >>
}