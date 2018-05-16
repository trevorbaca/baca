\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Staff
    {
        c'4
        \startTrillSpan
        \startTrillSpan
        d'4
        e'4
        f'4
        \stopTrillSpan
        \stopTrillSpan
    }
}