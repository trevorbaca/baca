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
                \time 9/16
                s1 * 9/16
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \scaleDurations #'(1 . 1) {
                        c'16
                        [
                        d'16
                        bf16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        fs16
                        [
                        e'16
                        ef'16
                        af16
                        g16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        a16
                    }
                }
            }
        >>
    >>
}