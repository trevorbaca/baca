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
                \time 9/32
                s1 * 9/32
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \scaleDurations #'(1 . 1) {
                        c'32
                        [
                        d'32
                        bf'32
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        fs''32
                        [
                        e''32
                        ef''32
                        af''32
                        g''32
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        a'32
                    }
                }
            }
        >>
    >>
}