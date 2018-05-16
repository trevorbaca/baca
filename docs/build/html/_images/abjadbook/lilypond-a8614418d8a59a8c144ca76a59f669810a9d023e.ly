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
        \with
        {
            \override Beam.positions = #'(-6 . -6)
            \override Stem.direction = #down
        }
        {
            {   % measure
                \time 3/2
                \scaleDurations #'(1 . 1) {
                    c'4
                }
                \scaleDurations #'(1 . 1) {
                    d'8
                    [
                    bf'8
                    ]
                }
                \times 4/6 {
                    fs''8
                    [
                    e''8
                    ef''8
                    ]
                }
                \scaleDurations #'(1 . 1) {
                    af''16
                    [
                    g''16
                    a'16
                    c'16
                    ]
                }
                \times 4/5 {
                    d'16
                    [
                    bf'16
                    fs''16
                    e''16
                    ef''16
                    ]
                }
                \times 4/6 {
                    af''16
                    [
                    g''16
                    a'16
                    c'16
                    d'16
                    bf'16
                    ]
                }
            }   % measure
        }
    >>
}