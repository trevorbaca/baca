\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Staff
    {
        \set Staff.instrumentName = \markup { Violin }
        \set Staff.shortInstrumentName = \markup { Vn. }
        \clef "percussion"
        c'8
        d'8
        e'8
        f'8
    }
}