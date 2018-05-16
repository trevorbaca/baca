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
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \scaleDurations #'(1 . 1) {
                        c'16
                        [
                        d'16
                        bf'16
                        fs''16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        e''16
                        [
                        ef''16
                        b''16
                        f''16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        g''16
                        [
                        cs''16
                        a'16
                        af'16
                        ]
                    }
                }
            }
        >>
    >>
}