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
        ~
        c'16
        d'16
        ~
        d'16
        d'16
        e'4
        ~
        e'16
        f'16
        ~
        f'16
        f'16
    }
}