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
                \time 11/8
                s1 * 11/8
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = #5                       %! OC1
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        [
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5 {
                        a'16
                        r4
                        \revert TupletBracket.staff-padding                              %! OC2
                    }
                }
            }
            \context Voice = "Voice 2"
            {
                \voiceTwo
                {
                    \override TupletBracket.stencil = ##f
                    \override TupletNumber.stencil = ##f
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        s8
                        s16
                        s16
                        bf'4
                        ~
                        bf'16
                        s16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        s16
                        s16
                        s4
                        s16
                        s16
                        af''16
                        [
                        g''16
                        ]
                    }
                    \times 4/5 {
                        s16
                        s4
                    }
                    \revert TupletBracket.stencil
                    \revert TupletNumber.stencil
                }
            }
        >>
    >>
}