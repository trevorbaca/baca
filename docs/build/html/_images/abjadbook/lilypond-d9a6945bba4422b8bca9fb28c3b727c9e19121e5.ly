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
        \once \override Accidental.color = #green
        \once \override Beam.color = #green
        \once \override Dots.color = #green
        \once \override NoteHead.color = #green
        \once \override Stem.color = #green
        c'8
        ~
        \once \override Accidental.color = #green
        \once \override Beam.color = #green
        \once \override Dots.color = #green
        \once \override NoteHead.color = #green
        \once \override Stem.color = #green
        c'16
        \once \override Accidental.color = #green
        \once \override Beam.color = #green
        \once \override Dots.color = #green
        \once \override NoteHead.color = #green
        \once \override Stem.color = #green
        c'16
        r8
        \once \override Accidental.color = #green
        \once \override Beam.color = #green
        \once \override Dots.color = #green
        \once \override NoteHead.color = #green
        \once \override Stem.color = #green
        c'16
        \once \override Accidental.color = #green
        \once \override Beam.color = #green
        \once \override Dots.color = #green
        \once \override NoteHead.color = #green
        \once \override Stem.color = #green
        c'16
        \once \override Accidental.color = #green
        \once \override Beam.color = #green
        \once \override Dots.color = #green
        \once \override NoteHead.color = #green
        \once \override Stem.color = #green
        d'8
        ~
        \once \override Accidental.color = #green
        \once \override Beam.color = #green
        \once \override Dots.color = #green
        \once \override NoteHead.color = #green
        \once \override Stem.color = #green
        d'16
        \once \override Accidental.color = #green
        \once \override Beam.color = #green
        \once \override Dots.color = #green
        \once \override NoteHead.color = #green
        \once \override Stem.color = #green
        d'16
        r8
        \once \override Accidental.color = #green
        \once \override Beam.color = #green
        \once \override Dots.color = #green
        \once \override NoteHead.color = #green
        \once \override Stem.color = #green
        d'16
        \once \override Accidental.color = #green
        \once \override Beam.color = #green
        \once \override Dots.color = #green
        \once \override NoteHead.color = #green
        \once \override Stem.color = #green
        d'16
    }
}