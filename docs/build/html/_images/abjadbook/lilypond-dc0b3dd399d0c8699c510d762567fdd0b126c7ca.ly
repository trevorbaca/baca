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
                
                % [GlobalSkips measure 5]                                                %! SM4
                \time 4/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 1/2
                
                % [GlobalSkips measure 6]                                                %! SM4
                \time 3/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 3/8
                
                % [GlobalSkips measure 7]                                                %! SM4
                \time 4/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 1/2
                
                % [GlobalSkips measure 8]                                                %! SM4
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
                        fs''!8
                        [
                        
                        e''8
                        
                        ef''!8
                        
                        f''8
                        ]
                    }
                    {
                        
                        % [MusicVoice measure 2]                                         %! SM4
                        a''8
                        [
                        
                        bf''!8
                        
                        c''8
                        ]
                    }
                    {
                        
                        % [MusicVoice measure 3]                                         %! SM4
                        b''8
                        [
                        
                        af''!8
                        
                        g''8
                        
                        cs''!8
                        ]
                    }
                    {
                        
                        % [MusicVoice measure 4]                                         %! SM4
                        d''8
                        [
                        
                        fs''!8
                        
                        e''8
                        ]
                    }
                    {
                        
                        % [MusicVoice measure 5]                                         %! SM4
                        ef''!8
                        [
                        
                        f''8
                        
                        a''8
                        
                        bf''!8
                        ]
                    }
                    {
                        
                        % [MusicVoice measure 6]                                         %! SM4
                        c''8
                        [
                        
                        b''8
                        
                        af''!8
                        ]
                    }
                    {
                        
                        % [MusicVoice measure 7]                                         %! SM4
                        g''8
                        [
                        
                        cs''!8
                        
                        d''8
                        
                        fs''!8
                        ]
                    }
                    {
                        
                        % [MusicVoice measure 8]                                         %! SM4
                        e''8
                        [
                        
                        ef''!8
                        
                        f''8
                        ]
                        
                    }
                }
            }
        >>
    >>
}