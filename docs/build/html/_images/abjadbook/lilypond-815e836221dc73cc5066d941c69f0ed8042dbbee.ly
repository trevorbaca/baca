\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Staff
    \with
    {
        autoBeaming = ##f
    }
    {
        \times 2/3 {
            c'8
            d'8
            e'8
        }
        f'8
        r8
        r8
        f'8
        \times 2/3 {
            e'8
            d'8
            c'8
        }
    }
}