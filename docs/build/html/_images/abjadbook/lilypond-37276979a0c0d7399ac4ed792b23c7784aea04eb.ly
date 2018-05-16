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
                    \set Staff.instrumentName =                                          %! SM8:REAPPLIED_MARGIN_MARKUP:SM37:-PARTS
                    \markup { I+II }                                                     %! SM8:REAPPLIED_MARGIN_MARKUP:SM37:-PARTS
                    \set Staff.shortInstrumentName =                                     %! SM8:REAPPLIED_MARGIN_MARKUP:SM37:-PARTS
                    \markup { I+II }                                                     %! SM8:REAPPLIED_MARGIN_MARKUP:SM37:-PARTS
                    \once \override Staff.InstrumentName.color = #(x11-color 'green4)    %! SM6:REAPPLIED_MARGIN_MARKUP_COLOR:SM37:-PARTS
                    c'4.
                    ^ \markup {                                                          %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37:-PARTS
                        \with-color                                                      %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37:-PARTS
                            #(x11-color 'green4)                                         %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37:-PARTS
                            [“I+II”]                                                     %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37:-PARTS
                        }                                                                %! SM11:REAPPLIED_MARGIN_MARKUP_ALERT:SM37:-PARTS
                    \override Staff.InstrumentName.color = #(x11-color 'OliveDrab)       %! SM6:REDRAWN_REAPPLIED_MARGIN_MARKUP_COLOR:SM37:-PARTS
                    \set Staff.instrumentName =                                          %! SM8:REDRAWN_REAPPLIED_MARGIN_MARKUP:SM34:SM37:-PARTS
                    \markup { I+II }                                                     %! SM8:REDRAWN_REAPPLIED_MARGIN_MARKUP:SM34:SM37:-PARTS
                    \set Staff.shortInstrumentName =                                     %! SM8:REDRAWN_REAPPLIED_MARGIN_MARKUP:SM34:SM37:-PARTS
                    \markup { I+II }                                                     %! SM8:REDRAWN_REAPPLIED_MARGIN_MARKUP:SM34:SM37:-PARTS
                    
                    % [MusicVoice measure 2]                                             %! SM4
                    c'4.
                    
                }
            }
        >>
    >>
}