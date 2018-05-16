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
                \time 21/16
                s1 * 21/16
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/6 {
                        r16
                        c'16
                        [
                        d'16
                        bf'16
                        ]
                        r8
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/8 {
                        r16
                        fs''16
                        [
                        e''16
                        ef''16
                        af''16
                        g''16
                        ]
                        r8
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 5/4 {
                        r16
                        a'16
                        r8
                    }
                }
            }
        >>
    >>
}