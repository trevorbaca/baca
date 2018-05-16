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
                \time 3/4
                s1 * 3/4
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \times 4/5 {
                        r8
                        c'16
                        [
                        d'16
                        bf'16
                        ]
                    }
                    \times 2/3 {
                        c'16
                        [
                        d'16
                        bf'16
                        ]
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        c'16
                        [
                        d'16
                        bf'16
                        ]
                        r4
                    }
                }
            }
            \context Voice = "Voice 2"
            {
                \voiceTwo
                {
                    \override TupletBracket.stencil = ##f
                    \override TupletNumber.stencil = ##f
                    \times 4/5 {
                        s8
                        s16
                        s16
                        bf'16
                    }
                    \times 2/3 {
                        c'16
                        [
                        d'16
                        ]
                        s16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        s16
                        s16
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