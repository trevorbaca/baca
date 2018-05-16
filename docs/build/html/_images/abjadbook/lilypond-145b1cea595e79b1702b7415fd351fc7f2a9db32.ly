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
                    \set Staff.instrumentName =                                          %! SM8:DEFAULT_MARGIN_MARKUP:ST2:-PARTS
                    \markup { I+II }                                                     %! SM8:DEFAULT_MARGIN_MARKUP:ST2:-PARTS
                    \set Staff.shortInstrumentName =                                     %! SM8:DEFAULT_MARGIN_MARKUP:ST2:-PARTS
                    \markup { I+II }                                                     %! SM8:DEFAULT_MARGIN_MARKUP:ST2:-PARTS
                %%% \once \override Staff.InstrumentName.color = #(x11-color 'DarkViolet) %! SM6:DEFAULT_MARGIN_MARKUP_COLOR:ST2:-PARTS
                    c'4.
                %%% ^ \markup {                                                          %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:ST2:-PARTS
                %%%     \with-color                                                      %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:ST2:-PARTS
                %%%         #(x11-color 'DarkViolet)                                     %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:ST2:-PARTS
                %%%         [“I+II”]                                                     %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:ST2:-PARTS
                %%%     }                                                                %! SM11:DEFAULT_MARGIN_MARKUP_ALERT:ST2:-PARTS
                %%% \override Staff.InstrumentName.color = #(x11-color 'violet)          %! SM6:REDRAWN_DEFAULT_MARGIN_MARKUP_COLOR:ST2:-PARTS
                    \set Staff.instrumentName =                                          %! SM8:REDRAWN_DEFAULT_MARGIN_MARKUP:SM34:ST2:-PARTS
                    \markup { I+II }                                                     %! SM8:REDRAWN_DEFAULT_MARGIN_MARKUP:SM34:ST2:-PARTS
                    \set Staff.shortInstrumentName =                                     %! SM8:REDRAWN_DEFAULT_MARGIN_MARKUP:SM34:ST2:-PARTS
                    \markup { I+II }                                                     %! SM8:REDRAWN_DEFAULT_MARGIN_MARKUP:SM34:ST2:-PARTS
                    
                    % [MusicVoice measure 2]                                             %! SM4
                    c'4.
                    
                }
            }
        >>
    >>
}