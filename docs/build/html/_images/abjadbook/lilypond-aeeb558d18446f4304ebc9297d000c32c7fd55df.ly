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
                \time 15/16
                s1 * 15/16
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \scaleDurations #'(1 . 1) {
                        fs''8
                        r16
                        e''8
                        r16
                        ef''8
                        r16
                        af''8
                        r16
                        g''8
                        r16
                    }
                }
            }
        >>
    >>
}