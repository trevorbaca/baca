\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    {
        <c d bf e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
        - \markup { 1-80 }
    }
}