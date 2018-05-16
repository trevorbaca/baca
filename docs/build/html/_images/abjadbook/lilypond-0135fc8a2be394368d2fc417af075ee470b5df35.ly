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
                \time 5/2
                s1 * 5/2
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \scaleDurations #'(1 . 1) {
                        r16
                        r16
                        fs''8
                        r8
                        r8
                        r16
                        r16
                        e''8
                        r8
                        r8
                        r16
                        r16
                        ef''8
                        r8
                        r8
                        r16
                        r16
                        af''8
                        r8
                        r8
                        r16
                        r16
                        g''8
                        r8
                        r8
                    }
                }
            }
        >>
    >>
}