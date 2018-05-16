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
        ~
        c'16
        c'16
        r8
        c'16
        c'16
        d'8
        ~
        d'16
        d'16
        r8
        d'16
        d'16
    }
}