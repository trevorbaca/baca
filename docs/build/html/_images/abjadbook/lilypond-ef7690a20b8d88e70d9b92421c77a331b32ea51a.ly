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
        r8
        d'8
        e'8
        r8
        f'8
        g'8
        a'8
        b'8
        r8
        c''8
    }
}