\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "../../../../source/_stylesheets/two-voice-staff-stylesheet.ily"

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
            \context MusicStaff = "MusicStaff"
            <<
                \context MusicVoiceOne = "MusicVoiceOne"
                {
                    
                    % [MusicVoiceOne measure 1]                                          %! SM4
                    R1 * 1/2
                    
                    % [MusicVoiceOne measure 2]                                          %! SM4
                    R1 * 3/8
                    
                    % [MusicVoiceOne measure 3]                                          %! SM4
                    R1 * 1/2
                    
                    % [MusicVoiceOne measure 4]                                          %! SM4
                    R1 * 3/8
                    
                }
                \context MusicVoiceTwo = "MusicVoiceTwo"
                {
                    
                    % [MusicVoiceTwo measure 1]                                          %! SM4
                    R1 * 1/2
                    
                    % [MusicVoiceTwo measure 2]                                          %! SM4
                    R1 * 3/8
                    
                    % [MusicVoiceTwo measure 3]                                          %! SM4
                    R1 * 1/2
                    
                    % [MusicVoiceTwo measure 4]                                          %! SM4
                    R1 * 3/8
                    
                }
            >>
        >>
    >>
}