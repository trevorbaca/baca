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
        \time 2/8
        c'8
        s8
        e'8
        f'8
        \time 3/8
        g'8
        s8
        b'8
        % green
        \time 1/8
        s8
    }
}