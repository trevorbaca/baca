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
                \time 5/8
                s1 * 5/8
            }   % measure
        }
        \new Staff
        {
            {   % measure
                \time 5/8
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/4 {
                    c'16
                    [
                    d'16
                    bf'8
                    ]
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 5/6 {
                    fs''16
                    [
                    e''16
                    ef''8
                    af''16
                    g''16
                    ]
                }
                \scaleDurations #'(1 . 1) {
                    a'8
                }
            }   % measure
        }
    >>
}