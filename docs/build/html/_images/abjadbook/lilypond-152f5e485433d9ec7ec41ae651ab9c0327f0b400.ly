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
                \time 11/16
                s1 * 11/16
            }   % measure
        }
        \new Staff
        \with
        {
            \override Stem.direction = #down
        }
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \scaleDurations #'(1 . 1) {
                        c'16
                        [
                        (                                                                %! SC
                        d'16
                        )                                                                %! SC
                        bf'16
                        fs''16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        e''16
                        [
                        (                                                                %! SC
                        ef''16
                        )                                                                %! SC
                        b''16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        g''16
                        [
                        (                                                                %! SC
                        cs''16
                        )                                                                %! SC
                        a'16
                        af'16
                        ]
                    }
                }
            }
        >>
    >>
}