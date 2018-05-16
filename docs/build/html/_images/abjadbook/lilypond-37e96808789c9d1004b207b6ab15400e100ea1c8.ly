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
                \time 15/16
                s1 * 15/16
            }   % measure
        }
        \new Staff
        \with
        {
            \override Beam.positions = #'(-5.5 . -5.5)
        }
        {
            {   % measure
                \time 15/16
                \tweak text #tuplet-number::calc-fraction-text
                \times 5/4 {
                    \set stemLeftBeamCount = 0
                    \set stemRightBeamCount = 2
                    c'16
                    [
                    \set stemLeftBeamCount = 2
                    \set stemRightBeamCount = 1
                    d'16
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 1
                    bf'8
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 7/6 {
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 2
                    fs''16
                    \set stemLeftBeamCount = 2
                    \set stemRightBeamCount = 1
                    e''16
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 1
                    ef''8
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 2
                    af''16
                    \set stemLeftBeamCount = 2
                    \set stemRightBeamCount = 1
                    g''16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/2 {
                    \set stemLeftBeamCount = 1
                    \set stemRightBeamCount = 0
                    a'8
                    ]
                }
            }   % measure
        }
    >>
}