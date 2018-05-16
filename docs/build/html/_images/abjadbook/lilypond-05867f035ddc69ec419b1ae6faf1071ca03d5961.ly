\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Staff
    {
        \time 5/4
        d'4
        ~
        d'16
        eqs'4
        ~
        eqs'16
        fs'4
        ~
        fs'16
        b'4
        ~
        b'16
    }
}