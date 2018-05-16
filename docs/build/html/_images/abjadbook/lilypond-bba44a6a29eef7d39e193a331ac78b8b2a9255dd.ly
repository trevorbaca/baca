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
                    \set Staff.instrumentName =                                          %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                    \markup { Fl. }                                                      %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                    \set Staff.shortInstrumentName =                                     %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                    \markup { Fl. }                                                      %! SM8:EXPLICIT_MARGIN_MARKUP:IC
                    \once \override Staff.InstrumentName.color = #(x11-color 'blue)      %! SM6:EXPLICIT_MARGIN_MARKUP_COLOR:IC
                    e'2
                    ^ \markup {                                                          %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                        \with-color                                                      %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                            #(x11-color 'blue)                                           %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                            [MarginMarkup]                                               %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                        }                                                                %! SM11:EXPLICIT_MARGIN_MARKUP_ALERT:IC
                    \override Staff.InstrumentName.color = #(x11-color 'DeepSkyBlue2)    %! SM6:REDRAWN_EXPLICIT_MARGIN_MARKUP_COLOR:IC
                    \set Staff.instrumentName =                                          %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                    \markup { Fl. }                                                      %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                    \set Staff.shortInstrumentName =                                     %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                    \markup { Fl. }                                                      %! SM8:REDRAWN_EXPLICIT_MARGIN_MARKUP:SM34:IC
                    
                    % [MusicVoice measure 2]                                             %! SM4
                    f'4.
                    
                    % [MusicVoice measure 3]                                             %! SM4
                    e'2
                    
                    % [MusicVoice measure 4]                                             %! SM4
                    f'4.
                    
                }
            }
        >>
    >>
}