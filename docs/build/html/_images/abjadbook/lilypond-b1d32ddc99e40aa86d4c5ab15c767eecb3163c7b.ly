\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Score
    <<
        \new Staff
        {
            c'8
            d'8
            e'8
            f'8
        }
        \new Staff
        {
            c'4
            d'4
        }
        \new Staff
        {
            \times 2/3 {
                c'8
                d'8
                e'8
            }
            \times 2/3 {
                c'8
                d'8
                e'8
            }
        }
    >>
}