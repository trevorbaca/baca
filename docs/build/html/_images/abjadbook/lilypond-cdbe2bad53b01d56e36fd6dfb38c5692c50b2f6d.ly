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
        \once \override Accidental.color = #red
        \once \override Beam.color = #red
        \once \override Dots.color = #red
        \once \override NoteHead.color = #red
        \once \override Stem.color = #red
        d'8
        \once \override Dots.color = #red
        \once \override Rest.color = #red
        r8
        \times 2/3 {
            \once \override Accidental.color = #blue
            \once \override Beam.color = #blue
            \once \override Dots.color = #blue
            \once \override NoteHead.color = #blue
            \once \override Stem.color = #blue
            e'8
            \once \override Dots.color = #blue
            \once \override Rest.color = #blue
            r8
            \once \override Accidental.color = #blue
            \once \override Beam.color = #blue
            \once \override Dots.color = #blue
            \once \override NoteHead.color = #blue
            \once \override Stem.color = #blue
            f'8
        }
        \once \override Accidental.color = #cyan
        \once \override Beam.color = #cyan
        \once \override Dots.color = #cyan
        \once \override NoteHead.color = #cyan
        \once \override Stem.color = #cyan
        g'8
        \once \override Accidental.color = #cyan
        \once \override Beam.color = #cyan
        \once \override Dots.color = #cyan
        \once \override NoteHead.color = #cyan
        \once \override Stem.color = #cyan
        a'8
        \once \override Dots.color = #cyan
        \once \override Rest.color = #cyan
        r8
    }
}