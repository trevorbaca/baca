\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "../../../../source/_stylesheets/string-trio-stylesheet.ily"

\layout {
    indent = #0
}

\score {
    \context Score = "Score"
    <<
        \context GlobalContext = "GlobalContext"
        <<
            \context GlobalSkips = "GlobalSkips"
            {
                
                % [GlobalSkips measure 1]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)         %! HSS1:SPACING
                \autoPageBreaksOff                                                       %! BMM1:BREAK
                \noBreak                                                                 %! BMM2:BREAK
                \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details  %! IC:BREAK
                #'((Y-offset . 0) (alignment-distances . (11)))                          %! IC:BREAK
                \time 3/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \bar ""                                                                  %! SM2:+SEGMENT:EMPTY_START_BAR
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                \pageBreak                                                               %! IC:BREAK
                s1 * 3/8
                
                % [GlobalSkips measure 2]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)         %! HSS1:SPACING
                \noBreak                                                                 %! BMM2:BREAK
                \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details  %! IC:BREAK
                #'((Y-offset . 15) (alignment-distances . (11)))                         %! IC:BREAK
                \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)      %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                \break                                                                   %! IC:BREAK
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
                    \set Staff.instrumentName = \markup { Flute }                        %! SM8:REDUNDANT_INSTRUMENT:IC
                    \set Staff.shortInstrumentName = \markup { Fl. }                     %! SM8:REDUNDANT_INSTRUMENT:IC
                %%% \once \override Staff.InstrumentName.color = #(x11-color 'DeepPink1) %! SM6:REDUNDANT_INSTRUMENT_COLOR:IC
                    c'4.
                %%% ^ \markup {                                                          %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                %%%     \with-color                                                      %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                %%%         #(x11-color 'DeepPink1)                                      %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                %%%         (“Flute”)                                                    %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                %%%     }                                                                %! SM11:REDUNDANT_INSTRUMENT_ALERT:IC
                %%% \override Staff.InstrumentName.color = #(x11-color 'DeepPink4)       %! SM6:REDRAWN_REDUNDANT_INSTRUMENT_COLOR:IC
                    \set Staff.instrumentName = \markup { Flute }                        %! SM8:REDRAWN_REDUNDANT_INSTRUMENT:SM34:IC
                    \set Staff.shortInstrumentName = \markup { Fl. }                     %! SM8:REDRAWN_REDUNDANT_INSTRUMENT:SM34:IC
                    
                    % [MusicVoice measure 2]                                             %! SM4
                    c'4.
                    
                }
            }
        >>
    >>
}