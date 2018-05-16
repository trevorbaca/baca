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
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 4/3 {
                        c'16
                        [
                        d'16
                        bf'16
                        ]
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/5 {
                        fs''16
                        [
                        e''16
                        ef''16
                        af''16
                        g''16
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