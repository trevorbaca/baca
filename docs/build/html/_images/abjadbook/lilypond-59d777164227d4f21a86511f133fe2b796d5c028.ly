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
                \time 9/8
                s1 * 9/8
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \times 2/3 {
                        c'16
                        [
                        d'16
                        bf'16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        fs''8.
                        [
                        e''8.
                        ef''8.
                        af''8.
                        g''8.
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        a'16
                    }
                }
            }
        >>
    >>
}