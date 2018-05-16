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
                \time 13/8
                s1 * 13/8
            }   % measure
        }
        \new Staff
        \with
        {
            \override TupletBracket.staff-padding = #4
        }
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/8 {
                        r8
                        r16
                        c'16
                        r16
                        d'16
                        r16
                        bf'16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 11/10 {
                        r16
                        fs''16
                        r16
                        e''16
                        r16
                        ef''16
                        r16
                        af''16
                        r16
                        g''16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/5 {
                        r16
                        a'16
                        r8.
                    }
                }
            }
        >>
    >>
}