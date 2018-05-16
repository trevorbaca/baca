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
                    
                    % [MusicVoice measure 1]                                             %! SM4
                    \stopStaff                                                           %! SM8:EXPLICIT_STAFF_LINES:IC
                    \once \override Staff.StaffSymbol.line-count = 1                     %! SM8:EXPLICIT_STAFF_LINES:IC
                    \startStaff                                                          %! SM8:EXPLICIT_STAFF_LINES:IC
                    \clef "percussion"                                                   %! SM8:EXPLICIT_CLEF:IC
                    \once \override Staff.Clef.color = #(x11-color 'blue)                %! SM6:EXPLICIT_CLEF_COLOR:IC
                %@% \override Staff.Clef.color = ##f                                     %! SM7:EXPLICIT_CLEF_COLOR_CANCELLATION:IC
                    \set Staff.forceClef = ##t                                           %! SM8:EXPLICIT_CLEF:SM33:IC
                    \once \override Staff.StaffSymbol.color = #(x11-color 'blue)         %! SM6:EXPLICIT_STAFF_LINES_COLOR:IC
                    a4.
                    \override Staff.Clef.color = #(x11-color 'DeepSkyBlue2)              %! SM6:EXPLICIT_CLEF_REDRAW_COLOR:IC
                    
                    % [MusicVoice measure 2]                                             %! SM4
                    b4.
                    
                    % [MusicVoice measure 3]                                             %! SM4
                    c'4.
                    
                    % [MusicVoice measure 4]                                             %! SM4
                    d'4.
                    
                    % [MusicVoice measure 5]                                             %! SM4
                    e'4.
                    
                }
            }
        >>
    >>
}