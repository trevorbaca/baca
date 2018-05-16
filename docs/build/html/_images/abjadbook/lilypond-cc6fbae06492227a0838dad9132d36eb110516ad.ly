\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Staff
    {
        \clef "percussion"
        c'4
        e'4
        c'4
        e'4
    }
}