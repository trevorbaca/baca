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
                        \pitchedTrill                                                    %! SC
                        c'16
                        [
                        \startTrillSpan d'                                               %! SC
                        \pitchedTrill                                                    %! SC
                        d'16
                        ]
                        \stopTrillSpan                                                   %! SC
                        \startTrillSpan e'                                               %! SC
                        \pitchedTrill                                                    %! SC
                        bf'4
                        ~
                        \stopTrillSpan                                                   %! SC
                        \startTrillSpan c''                                              %! SC
                        bf'16
                        r16
                        \stopTrillSpan                                                   %! SC
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \pitchedTrill                                                    %! SC
                        fs''16
                        [
                        \startTrillSpan gs''                                             %! SC
                        \pitchedTrill                                                    %! SC
                        e''16
                        ]
                        \stopTrillSpan                                                   %! SC
                        \startTrillSpan fs''                                             %! SC
                        \pitchedTrill                                                    %! SC
                        ef''4
                        ~
                        \stopTrillSpan                                                   %! SC
                        \startTrillSpan f''                                              %! SC
                        ef''16
                        r16
                        \stopTrillSpan                                                   %! SC
                        \pitchedTrill                                                    %! SC
                        af''16
                        [
                        \startTrillSpan bf''                                             %! SC
                        \pitchedTrill                                                    %! SC
                        g''16
                        ]
                        \stopTrillSpan                                                   %! SC
                        \startTrillSpan a''                                              %! SC
                    }
                    \times 4/5 {
                        \pitchedTrill                                                    %! SC
                        a'16
                        \stopTrillSpan                                                   %! SC
                        \startTrillSpan b'                                               %! SC
                        r4
                        \stopTrillSpan                                                   %! SC
                        \revert TupletBracket.staff-padding                              %! OC2
                    }
                }
            }
        >>
    >>
}