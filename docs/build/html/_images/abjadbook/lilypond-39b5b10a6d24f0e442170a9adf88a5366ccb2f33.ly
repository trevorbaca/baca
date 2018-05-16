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
                        e'8
                        [
                        ^ \markup {
                            \small
                                E4
                            }
                        
                        d''8
                        ^ \markup {
                            \small
                                D5
                            }
                        
                        f'8
                        ^ \markup {
                            \small
                                F4
                            }
                        
                        e''8
                        ]
                        ^ \markup {
                            \small
                                E5
                            }
                    }
                    {
                        
                        % [MusicVoice measure 2]                                         %! SM4
                        g'8
                        [
                        ^ \markup {
                            \small
                                G4
                            }
                        
                        f''8
                        ^ \markup {
                            \small
                                F5
                            }
                        
                        e'8
                        ]
                        ^ \markup {
                            \small
                                E4
                            }
                    }
                    {
                        
                        % [MusicVoice measure 3]                                         %! SM4
                        d''8
                        [
                        ^ \markup {
                            \small
                                D5
                            }
                        
                        f'8
                        ^ \markup {
                            \small
                                F4
                            }
                        
                        e''8
                        ^ \markup {
                            \small
                                E5
                            }
                        
                        g'8
                        ]
                        ^ \markup {
                            \small
                                G4
                            }
                    }
                    {
                        
                        % [MusicVoice measure 4]                                         %! SM4
                        f''8
                        [
                        ^ \markup {
                            \small
                                F5
                            }
                        
                        e'8
                        ^ \markup {
                            \small
                                E4
                            }
                        
                        d''8
                        ]
                        ^ \markup {
                            \small
                                D5
                            }
                        
                    }
                }
            }
        >>
    >>
}