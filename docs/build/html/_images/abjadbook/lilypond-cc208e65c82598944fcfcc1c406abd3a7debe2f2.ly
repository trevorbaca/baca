\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\markup {
    \concat
        {
            partition(
            \bold
                J
            ", [2, 3, 5]!)"
        }
    }