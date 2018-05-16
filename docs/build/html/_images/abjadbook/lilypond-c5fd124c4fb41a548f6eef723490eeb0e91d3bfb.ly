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
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        d'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 1
                        bf'16
                    }
                    \scaleDurations #'(1 . 1) {
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 2
                        fs''16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        e''16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        ef''16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        af''16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 1
                        g''16
                    }
                    \scaleDurations #'(1 . 1) {
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 2
                        a'16
                        r8
                        ]
                    }
                }
            }
        >>
    >>
}