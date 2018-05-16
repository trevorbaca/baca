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
                        \startTrillSpan                                                  %! SC
                        d'16
                        ]
                        \stopTrillSpan                                                   %! SC
                        \startTrillSpan                                                  %! SC
                        bf'4
                        ~
                        \stopTrillSpan                                                   %! SC
                        \startTrillSpan                                                  %! SC
                        bf'16
                        r16
                        \stopTrillSpan                                                   %! SC
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        [
                        \startTrillSpan                                                  %! SC
                        e''16
                        ]
                        \stopTrillSpan                                                   %! SC
                        \startTrillSpan                                                  %! SC
                        ef''4
                        ~
                        \stopTrillSpan                                                   %! SC
                        \startTrillSpan                                                  %! SC
                        ef''16
                        r16
                        \stopTrillSpan                                                   %! SC
                        af''16
                        [
                        \startTrillSpan                                                  %! SC
                        g''16
                        ]
                        \stopTrillSpan                                                   %! SC
                        \startTrillSpan                                                  %! SC
                    }
                    \times 4/5 {
                        a'16
                        \stopTrillSpan                                                   %! SC
                        \startTrillSpan                                                  %! SC
                        r4
                        \stopTrillSpan                                                   %! SC
                        \revert TupletBracket.staff-padding                              %! OC2
                    }
                }
            }
        >>
    >>
}