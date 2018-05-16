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
                \time 3/4
                s1 * 3/4
            }   % measure
        }
        \new Staff
        {
            {   % measure
                \time 3/4
                \scaleDurations #'(1 . 1) {
                    c'16
                    [
                    d'16
                    bf'8
                    ~
                    ]
                }
                \scaleDurations #'(1 . 1) {
                    bf'16
                    [
                    e''16
                    ~
                    e''8
                    g''16
                    ~
                    g''16
                    ~
                    ]
                }
                \scaleDurations #'(1 . 1) {
                    g''8
                }
            }   % measure
        }
    >>
}