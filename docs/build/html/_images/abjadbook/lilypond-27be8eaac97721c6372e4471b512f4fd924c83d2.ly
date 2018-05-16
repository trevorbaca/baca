\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Staff
    {
        \clef "treble"
        b'4
        d''4
        b'4
        d''4
    }
}