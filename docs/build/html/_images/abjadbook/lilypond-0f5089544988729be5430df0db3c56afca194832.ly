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
        \times 2/3 {
            \once \override Accidental.color = #red
            \once \override Beam.color = #red
            \once \override Dots.color = #red
            \once \override NoteHead.color = #red
            \once \override Stem.color = #red
            <c' e' g'>8
            ~
            <c' e' g'>8
            d'8
        }
        e'8
        r8
        r8
        <g d' fs'>8
        \times 2/3 {
            e'8
            \once \override Accidental.color = #blue
            \once \override Beam.color = #blue
            \once \override Dots.color = #blue
            \once \override NoteHead.color = #blue
            \once \override Stem.color = #blue
            <c' d'>8
            ~
            <c' d'>8
        }
    }
}