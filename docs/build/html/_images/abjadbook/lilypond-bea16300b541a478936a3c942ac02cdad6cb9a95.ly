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
                        d'16
                        bf'16
                        (                                                                %! SC
                        fs''16
                        ]
                        )                                                                %! SC
                    }
                    \scaleDurations #'(1 . 1) {
                        e''16
                        [
                        ef''16
                        (                                                                %! SC
                        b''16
                        ]
                        )                                                                %! SC
                    }
                    \scaleDurations #'(1 . 1) {
                        g''16
                        [
                        cs''16
                        a'16
                        (                                                                %! SC
                        af'16
                        ]
                        )                                                                %! SC
                    }
                }
            }
        >>
    >>
}