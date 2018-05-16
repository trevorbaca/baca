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
                \time 29/32
                s1 * 29/32
            }   % measure
        }
        \new Staff
        {
            {   % measure
                \time 29/32
                \scaleDurations #'(1 . 1) {
                    c'4..
                    c'64
                    \repeatTie
                    d'4..
                    d'64
                    \repeatTie
                }
            }   % measure
        }
    >>
}