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
        c'8
        d'8
        r8
        \times 2/3 {
            e'8
            r8
            f'8
        }
        g'8
        a'8
        r8
        r8
        <c' e' g'>8
        ~
        <c' e' g'>4
    }
}