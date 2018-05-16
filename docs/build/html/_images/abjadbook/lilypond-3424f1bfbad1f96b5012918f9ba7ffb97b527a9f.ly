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
                \time 1/16
                s1 * 1/16
            }   % measure
        }
        \new Staff
        {
            {   % measure
                \time 1/16
                \scaleDurations #'(1 . 1) {
                    a'16
                }
            }   % measure
        }
    >>
}