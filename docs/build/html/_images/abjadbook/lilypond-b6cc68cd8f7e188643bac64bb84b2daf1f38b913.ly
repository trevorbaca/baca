\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new StaffGroup
    <<
        \new Staff
        {
            c'4
            <d' fs' a'>4
            b2
        }
        \new Staff
        {
            c4.
            r8
            g2
        }
    >>
}