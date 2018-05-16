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
        \once \override Accidental.color = #red
        \once \override Beam.color = #red
        \once \override Dots.color = #red
        \once \override NoteHead.color = #red
        \once \override Stem.color = #red
        c'8
        ~
        \once \override Accidental.color = #red
        \once \override Beam.color = #red
        \once \override Dots.color = #red
        \once \override NoteHead.color = #red
        \once \override Stem.color = #red
        c'16
        \once \override Accidental.color = #red
        \once \override Beam.color = #red
        \once \override Dots.color = #red
        \once \override NoteHead.color = #red
        \once \override Stem.color = #red
        c'16
        r8
        \once \override Accidental.color = #blue
        \once \override Beam.color = #blue
        \once \override Dots.color = #blue
        \once \override NoteHead.color = #blue
        \once \override Stem.color = #blue
        c'16
        \once \override Accidental.color = #blue
        \once \override Beam.color = #blue
        \once \override Dots.color = #blue
        \once \override NoteHead.color = #blue
        \once \override Stem.color = #blue
        c'16
        \once \override Accidental.color = #red
        \once \override Beam.color = #red
        \once \override Dots.color = #red
        \once \override NoteHead.color = #red
        \once \override Stem.color = #red
        d'8
        ~
        \once \override Accidental.color = #red
        \once \override Beam.color = #red
        \once \override Dots.color = #red
        \once \override NoteHead.color = #red
        \once \override Stem.color = #red
        d'16
        \once \override Accidental.color = #red
        \once \override Beam.color = #red
        \once \override Dots.color = #red
        \once \override NoteHead.color = #red
        \once \override Stem.color = #red
        d'16
        r8
        \once \override Accidental.color = #blue
        \once \override Beam.color = #blue
        \once \override Dots.color = #blue
        \once \override NoteHead.color = #blue
        \once \override Stem.color = #blue
        d'16
        \once \override Accidental.color = #blue
        \once \override Beam.color = #blue
        \once \override Dots.color = #blue
        \once \override NoteHead.color = #blue
        \once \override Stem.color = #blue
        d'16
    }
}