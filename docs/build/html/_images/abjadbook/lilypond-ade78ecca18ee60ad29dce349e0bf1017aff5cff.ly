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
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \scaleDurations #'(1 . 1) {
                        r8
                        [
                        c'16
                        d'16
                        bf'16
                    }
                    \scaleDurations #'(1 . 1) {
                        fs''16
                        e''16
                        ef''16
                        af''16
                        g''16
                    }
                    \scaleDurations #'(1 . 1) {
                        a'16
                        r8
                        ]
                    }
                }
            }
        >>
    >>
}