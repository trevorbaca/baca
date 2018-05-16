\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\markup {
    \line
        {
            "(1, 2, 3)"
            +
            \bold
                K
        }
    }