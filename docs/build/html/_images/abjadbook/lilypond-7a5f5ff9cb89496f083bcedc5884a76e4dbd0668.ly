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
                    {
                        
                        % [MusicVoice measure 1]                                         %! SM4
                        \makeBlue                                                        %! SM24
                        c'8
                        [
                        ^ \markup {
                            \small
                                0
                            }
                        
                        \makeBlue                                                        %! SM24
                        c'8
                        ^ \markup {
                            \small
                                1
                            }
                        
                        \makeBlue                                                        %! SM24
                        c'8
                        ^ \markup {
                            \small
                                2
                            }
                        
                        \makeBlue                                                        %! SM24
                        c'8
                        ]
                        ^ \markup {
                            \small
                                3
                            }
                    }
                    {
                        
                        % [MusicVoice measure 2]                                         %! SM4
                        \makeBlue                                                        %! SM24
                        c'8
                        [
                        ^ \markup {
                            \small
                                4
                            }
                        
                        \makeBlue                                                        %! SM24
                        c'8
                        ^ \markup {
                            \small
                                5
                            }
                        
                        \makeBlue                                                        %! SM24
                        c'8
                        ]
                        ^ \markup {
                            \small
                                6
                            }
                    }
                    {
                        
                        % [MusicVoice measure 3]                                         %! SM4
                        \makeBlue                                                        %! SM24
                        c'8
                        [
                        ^ \markup {
                            \small
                                7
                            }
                        
                        \makeBlue                                                        %! SM24
                        c'8
                        ^ \markup {
                            \small
                                8
                            }
                        
                        \makeBlue                                                        %! SM24
                        c'8
                        ^ \markup {
                            \small
                                9
                            }
                        
                        \makeBlue                                                        %! SM24
                        c'8
                        ]
                        ^ \markup {
                            \small
                                10
                            }
                    }
                    {
                        
                        % [MusicVoice measure 4]                                         %! SM4
                        \makeBlue                                                        %! SM24
                        c'8
                        [
                        ^ \markup {
                            \small
                                11
                            }
                        
                        \makeBlue                                                        %! SM24
                        c'8
                        ^ \markup {
                            \small
                                12
                            }
                        
                        \makeBlue                                                        %! SM24
                        c'8
                        ]
                        ^ \markup {
                            \small
                                13
                            }
                        
                    }
                }
            }
        >>
    >>
}