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
                \time 39/32
                s1 * 39/32
            }   % measure
        }
        \new Staff
        {
            {   % measure
                \time 39/32
                \scaleDurations #'(1 . 1) {
                    c'8
                    [
                    d'8
                    bf'8
                    ~
                    bf'32
                    ]
                }
                \scaleDurations #'(1 . 1) {
                    fs''8
                    [
                    e''8
                    ef''8
                    ~
                    ef''32
                    af''8
                    g''8
                    ]
                }
                \scaleDurations #'(1 . 1) {
                    a'8
                    ~
                    [
                    a'32
                    ]
                }
            }   % measure
        }
    >>
}