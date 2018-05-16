\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Score
    \with
    {
        proportionalNotationDuration = #(ly:make-moment 1 8)
    }
    <<
        \new Staff
        \with
        {
            \override BarLine.stencil = ##f
            \override Stem.transparent = ##t
            \override TextScript.font-size = #-1
            \override TextScript.staff-padding = #6
            \override TimeSignature.stencil = ##f
        }
        {
            \clef "bass"
            a,,4
            _ \markup { 1 }
            a,4
            _ \markup { 2 }
            e4
            ^ \markup { +2 }
            _ \markup { 3 }
            a4
            _ \markup { 4 }
            \clef "treble"
            cs'4
            ^ \markup { -14 }
            _ \markup { 5 }
            e'4
            ^ \markup { +2 }
            _ \markup { 6 }
            g'4
            ^ \markup { -31 }
            _ \markup { 7 }
            a'4
            _ \markup { 8 }
            b'4
            ^ \markup { +4 }
            _ \markup { 9 }
            cs''4
            ^ \markup { -14 }
            _ \markup { 10 }
            dqs''4
            ^ \markup { +1 }
            _ \markup { 11 }
            e''4
            ^ \markup { +2 }
            _ \markup { 12 }
            fqs''4
            ^ \markup { -9 }
            _ \markup { 13 }
            g''4
            ^ \markup { -31 }
            _ \markup { 14 }
            af''4
            ^ \markup { -12 }
            _ \markup { 15 }
            a''4
            _ \markup { 16 }
            bf''4
            ^ \markup { +5 }
            _ \markup { 17 }
            b''4
            ^ \markup { +4 }
            _ \markup { 18 }
            c'''4
            ^ \markup { -2 }
            _ \markup { 19 }
            cs'''4
            ^ \markup { -14 }
            _ \markup { 20 }
        }
    >>
}