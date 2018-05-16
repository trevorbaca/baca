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
                \time 19/16
                s1 * 19/16
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