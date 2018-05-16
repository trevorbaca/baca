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
        \once \override Accidental.color = #red
        \once \override Beam.color = #red
        \once \override Dots.color = #red
        \once \override NoteHead.color = #red
        \once \override Stem.color = #red
        d'8
        ~
        d'16
        e'16
        ~
        e'8
        f'4
        \once \override Accidental.color = #blue
        \once \override Beam.color = #blue
        \once \override Dots.color = #blue
        \once \override NoteHead.color = #blue
        \once \override Stem.color = #blue
        g'8
    }
}