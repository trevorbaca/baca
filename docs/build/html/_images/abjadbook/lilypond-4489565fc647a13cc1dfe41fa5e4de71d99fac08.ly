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
        c'4
        \times 2/3 {
            d'8
            r8
            e'8
        }
        r16
        f'16
        g'8
        a'4
    }
}