\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Staff
    {
        c'4
        \startTrillSpan
        d'4
        e'4
        \stopTrillSpan
        \startTrillSpan
        f'4
        \stopTrillSpan
    }
}