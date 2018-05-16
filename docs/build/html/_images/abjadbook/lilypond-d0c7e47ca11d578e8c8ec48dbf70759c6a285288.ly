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
                \time 15/8
                s1 * 15/8
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
                \time 15/8
                \times 4/6 {
                    c'16
                    [
                    d'16
                    bf'8
                    fs''16
                    e''16
                    ]
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 6/7 {
                    ef''8
                    [
                    af''16
                    g''16
                    a'8
                    c'16
                    ]
                }
                \times 4/7 {
                    d'16
                    [
                    bf'8
                    fs''16
                    e''16
                    ef''8
                    ]
                }
                \scaleDurations #'(1 . 1) {
                    af''16
                    [
                    g''16
                    a'8
                    c'16
                    d'16
                    ]
                }
                \times 4/7 {
                    bf'8
                    [
                    fs''16
                    e''16
                    ef''8
                    af''16
                    ]
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 6/7 {
                    g''16
                    [
                    a'8
                    c'16
                    d'16
                    bf'8
                    ]
                }
            }   % measure
        }
    >>
}