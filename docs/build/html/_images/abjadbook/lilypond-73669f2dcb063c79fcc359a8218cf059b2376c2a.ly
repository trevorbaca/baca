\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Staff
    \with
    {
        \override SustainPedalLineSpanner.staff-padding = #6
        autoBeaming = ##f
    }
    {
        \once \override Accidental.color = #red
        \once \override Beam.color = #red
        \once \override Dots.color = #red
        \once \override NoteHead.color = #red
        \once \override Stem.color = #red
        \set Staff.pedalSustainStyle = #'mixed
        c'8
        \sustainOn
        \once \override Dots.color = #red
        \once \override Rest.color = #red
        r8
        \sustainOff
        \once \override Accidental.color = #blue
        \once \override Beam.color = #blue
        \once \override Dots.color = #blue
        \once \override NoteHead.color = #blue
        \once \override Stem.color = #blue
        \set Staff.pedalSustainStyle = #'mixed
        d'8
        ~
        \sustainOn
        \once \override Accidental.color = #blue
        \once \override Beam.color = #blue
        \once \override Dots.color = #blue
        \once \override NoteHead.color = #blue
        \once \override Stem.color = #blue
        d'8
        \once \override Accidental.color = #red
        \once \override Beam.color = #red
        \once \override Dots.color = #red
        \once \override NoteHead.color = #red
        \once \override Stem.color = #red
        \set Staff.pedalSustainStyle = #'mixed
        e'8
        ~
        \sustainOff
        \sustainOn
        \once \override Accidental.color = #red
        \once \override Beam.color = #red
        \once \override Dots.color = #red
        \once \override NoteHead.color = #red
        \once \override Stem.color = #red
        e'8
        \once \override Dots.color = #red
        \once \override Rest.color = #red
        r8
        \sustainOff
        \once \override Accidental.color = #blue
        \once \override Beam.color = #blue
        \once \override Dots.color = #blue
        \once \override NoteHead.color = #blue
        \once \override Stem.color = #blue
        \set Staff.pedalSustainStyle = #'mixed
        f'8
        \sustainOn
        \sustainOff
    }
}