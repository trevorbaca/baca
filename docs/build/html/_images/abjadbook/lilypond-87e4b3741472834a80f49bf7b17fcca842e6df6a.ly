\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\markup {
    \concat
        {
            permute(
            \bold
                J
            ", permutation=[1, 0, 3, 2])"
        }
    }