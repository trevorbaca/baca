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
                \time 5/16
                s1 * 5/16
            }   % measure
        }
        \new Staff
        {
            {   % measure
                \time 5/16
                \scaleDurations #'(1 . 1) {
                    c'16
                    [
                    d'16
                    bf'8
                    af'16
                    ]
                }
            }   % measure
        }
    >>
}