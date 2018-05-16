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
                \time 3/8
                s1 * 3/8
            }   % measure
        }
        \new Staff
        {
            {   % measure
                \time 3/8
                \scaleDurations #'(1 . 1) {
                    fs''16
                    [
                    e''16
                    ef''8
                    af''16
                    g''16
                    ]
                }
            }   % measure
        }
    >>
}