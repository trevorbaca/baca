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
                        \set Staff.instrumentName = \markup { "Clarinet in B-flat" }     %! SM8:EXPLICIT_INSTRUMENT:IC
                        \set Staff.shortInstrumentName = \markup { "Cl. in B-flat" }     %! SM8:EXPLICIT_INSTRUMENT:IC
                        \once \override Staff.InstrumentName.color = #(x11-color 'blue)  %! SM6:EXPLICIT_INSTRUMENT_COLOR:IC
                        fs'!8
                        [
                        ^ \markup {                                                      %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            \with-color                                                  %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                #(x11-color 'blue)                                       %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                                (“clarinet”)                                             %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                            }                                                            %! SM11:EXPLICIT_INSTRUMENT_ALERT:IC
                        \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2) %! SM6:REDRAWN_EXPLICIT_INSTRUMENT_COLOR:IC
                        \set Staff.instrumentName = \markup { "Clarinet in B-flat" }     %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                        \set Staff.shortInstrumentName = \markup { "Cl. in B-flat" }     %! SM8:REDRAWN_EXPLICIT_INSTRUMENT:SM34:IC
                        
                        g'8
                        
                        fs'!8
                        
                        g'8
                        ]
                    }
                    {
                        
                        % [MusicVoice measure 2]                                         %! SM4
                        fs'!8
                        [
                        
                        g'8
                        
                        fs'!8
                        ]
                    }
                    {
                        
                        % [MusicVoice measure 3]                                         %! SM4
                        g'8
                        [
                        
                        fs'!8
                        
                        g'8
                        
                        fs'!8
                        ]
                    }
                    {
                        
                        % [MusicVoice measure 4]                                         %! SM4
                        g'8
                        [
                        
                        fs'!8
                        
                        g'8
                        ]
                        
                    }
                }
            }
        >>
    >>
}