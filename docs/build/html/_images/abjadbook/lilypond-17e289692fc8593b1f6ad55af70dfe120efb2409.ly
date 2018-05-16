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
        {   % measure
            \time 2/8
            \tempo 4=60
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
        }   % measure
        {   % measure
            \once \override Accidental.color = #red
            \once \override Beam.color = #red
            \once \override Dots.color = #red
            \once \override NoteHead.color = #red
            \once \override Stem.color = #red
            e'8
            \once \override Accidental.color = #blue
            \once \override Beam.color = #blue
            \once \override Dots.color = #blue
            \once \override NoteHead.color = #blue
            \once \override Stem.color = #blue
            f'8
        }   % measure
        {   % measure
            \once \override Accidental.color = #blue
            \once \override Beam.color = #blue
            \once \override Dots.color = #blue
            \once \override NoteHead.color = #blue
            \once \override Stem.color = #blue
            g'8
            \once \override Accidental.color = #blue
            \once \override Beam.color = #blue
            \once \override Dots.color = #blue
            \once \override NoteHead.color = #blue
            \once \override Stem.color = #blue
            a'8
        }   % measure
        {   % measure
            b'8
            c''8
        }   % measure
    }
}