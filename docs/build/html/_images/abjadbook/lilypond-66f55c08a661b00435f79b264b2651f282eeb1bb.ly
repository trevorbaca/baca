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
                \time 13/16
                s1 * 13/16
            }   % measure
        }
        \new Staff
        {
            {   % measure
                \time 13/16
                \scaleDurations #'(1 . 1) {
                    c'16
                    [
                    d'16
                    bf'8
                    af'16
                    ]
                }
                \scaleDurations #'(1 . 1) {
                    fs''16
                    [
                    e''8
                    ef''16
                    af''16
                    g''8
                    ]
                }
                \scaleDurations #'(1 . 1) {
                    a'16
                }
            }   % measure
        }
    >>
}