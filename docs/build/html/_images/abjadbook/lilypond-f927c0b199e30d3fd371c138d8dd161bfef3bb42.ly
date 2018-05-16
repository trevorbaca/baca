\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Staff
    {
        \newSpacingSection
        \set Score.proportionalNotationDuration = #(ly:make-moment 2 24)
        c'4
        d'4
        e'4
        f'4
    }
}