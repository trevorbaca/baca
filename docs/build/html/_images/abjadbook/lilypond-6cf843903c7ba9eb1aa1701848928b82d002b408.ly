\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Staff
    {
        \set Staff.instrumentName = \markup { Violin }
        \set Staff.shortInstrumentName = \markup { Vn. }
        c'8
        r8
        <d fs>8
        r8
    }
}