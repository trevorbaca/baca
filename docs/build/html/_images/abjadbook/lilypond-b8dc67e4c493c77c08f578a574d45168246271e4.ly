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
                \time 11/8
                s1 * 11/8
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = #5                       %! OC1
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        fs16
                        [
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        e'16
                        ]
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        ef'4
                        ~
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        ef'16
                        \once \override Dots.color = #green
                        \once \override Rest.color = #green
                        r16
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        af16
                        [
                        \once \override Accidental.color = #green
                        \once \override Beam.color = #green
                        \once \override Dots.color = #green
                        \once \override NoteHead.color = #green
                        \once \override Stem.color = #green
                        g16
                        ]
                    }
                    \times 4/5 {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding                              %! OC2
                    }
                }
            }
        >>
    >>
}