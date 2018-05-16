\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\markup {
    \concat
        {
            split(
            \bold
                J
            ", <3, 15, 3>+)"
        }
    }