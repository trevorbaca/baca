\version "2.19.0"
\language "english"

\include "default.ily"
\include "rhythm-maker-docs.ily"

\score {
    \new Score
    <<
        \new GlobalContext
        {
            {   % measure
                \time 3/2
                s1 * 3/2
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \scaleDurations #'(1 . 1) {
                        fs'16
                        [
                        e'16
                        ef'16
                        f'16
                        a'16
                        bf'16
                        c'16
                        b'16
                        af'16
                        g'16
                        cs'16
                        d'16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        fs'16
                        [
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        e'16
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        ef''16
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        f''16
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        a'16
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        bf'16
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        c''16
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        b''16
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        af''16
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        g''16
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        cs'''16
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        d'''16
                        ]
                    }
                }
            }
        >>
    >>
}