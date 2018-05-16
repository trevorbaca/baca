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
                \time 4/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 1/2
                
                % [GlobalSkips measure 2]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)         %! HSS1:SPACING
                \time 3/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 3/8
                
                % [GlobalSkips measure 3]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)         %! HSS1:SPACING
                \time 4/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 1/2
                
                % [GlobalSkips measure 4]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)         %! HSS1:SPACING
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
                    
                    % [MusicVoice measure 1]                                             %! SM4
                    \override Glissando.arrow-length = #'2                               %! OC1
                    \override Glissando.arrow-width = #'0.5                              %! OC1
                    \override Glissando.bound-details.right.arrow = ##t                  %! OC1
                    \override Glissando.thickness = #'3                                  %! OC1
                    \once \override NoteHead.style = #'harmonic                          %! OC1
                    c''2
                    \glissando                                                           %! SC
                    
                    % [MusicVoice measure 2]                                             %! SM4
                    c''4.
                    \revert Glissando.arrow-length                                       %! OC2
                    \revert Glissando.arrow-width                                        %! OC2
                    \revert Glissando.bound-details.right.arrow                          %! OC2
                    \revert Glissando.thickness                                          %! OC2
                    
                    % [MusicVoice measure 3]                                             %! SM4
                    \override Glissando.arrow-length = #'2                               %! OC1
                    \override Glissando.arrow-width = #'0.5                              %! OC1
                    \override Glissando.bound-details.right.arrow = ##t                  %! OC1
                    \override Glissando.thickness = #'3                                  %! OC1
                    \once \override NoteHead.style = #'harmonic                          %! OC1
                    c''2
                    \glissando                                                           %! SC
                    
                    % [MusicVoice measure 4]                                             %! SM4
                    c''4.
                    \revert Glissando.arrow-length                                       %! OC2
                    \revert Glissando.arrow-width                                        %! OC2
                    \revert Glissando.bound-details.right.arrow                          %! OC2
                    \revert Glissando.thickness                                          %! OC2
                    
                }
            }
        >>
    >>
}