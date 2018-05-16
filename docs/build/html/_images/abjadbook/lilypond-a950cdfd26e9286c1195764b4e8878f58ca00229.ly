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
                \time 5/4
                s1 * 5/4
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \scaleDurations #'(1 . 1) {
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        <c d bf>8
                        ~
                        [
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        <c d bf>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        f'8
                        ~
                        [
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        f'32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        <ef' e' fs''>8
                        ~
                        [
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        <ef' e' fs''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        <g af'>8
                        ~
                        [
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        <g af'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        a8
                        ~
                        [
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        a32
                        ]
                        r16.
                    }
                }
            }
        >>
    >>
}