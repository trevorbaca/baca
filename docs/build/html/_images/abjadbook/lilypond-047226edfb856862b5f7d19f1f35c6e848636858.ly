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
                \time 4/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 1/2
                
                % [GlobalSkips measure 2]                                                %! SM4
                \time 3/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 3/8
                
                % [GlobalSkips measure 3]                                                %! SM4
                \time 4/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 1/2
                
                % [GlobalSkips measure 4]                                                %! SM4
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
                    \override Beam.positions = #'(6 . 6)                                 %! OC1
                    \override Stem.direction = #up                                       %! OC1
                    e'8
                    [
                    
                    d''8
                    
                    f'8
                    ]
                    
                    \override Rest.direction = #up                                       %! OC1
                    r8
                    
                    % [MusicVoice measure 2]                                             %! SM4
                    e''8
                    [
                    
                    g'8
                    
                    f''8
                    ]
                    
                    % [MusicVoice measure 3]                                             %! SM4
                    r8
                    
                    e'8
                    [
                    
                    d''8
                    
                    f'8
                    ]
                    
                    % [MusicVoice measure 4]                                             %! SM4
                    r8
                    \revert Rest.direction                                               %! OC2
                    
                    e''8
                    [
                    
                    g'8
                    ]
                    \revert Beam.positions                                               %! OC2
                    \revert Stem.direction                                               %! OC2
                    
                }
            }
        >>
    >>
}