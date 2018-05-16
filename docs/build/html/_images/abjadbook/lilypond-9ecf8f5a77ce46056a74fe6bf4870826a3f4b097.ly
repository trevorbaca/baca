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
                        \set Staff.pedalSustainStyle = #'bracket                         %! SC
                        r8
                        \sustainOn                                                       %! SC
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                        \sustainOff                                                      %! SC
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override Staff.SustainPedalLineSpanner.staff-padding = #4       %! OC1
                        \set Staff.pedalSustainStyle = #'bracket                         %! SC
                        fs''16
                        [
                        \sustainOn                                                       %! SC
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
                        \sustainOff                                                      %! SC
                        \revert Staff.SustainPedalLineSpanner.staff-padding              %! OC2
                    }
                    \times 4/5 {
                        \set Staff.pedalSustainStyle = #'bracket                         %! SC
                        a'16
                        \sustainOn                                                       %! SC
                        r4
                        \sustainOff                                                      %! SC
                        \revert TupletBracket.staff-padding                              %! OC2
                    }
                }
            }
        >>
    >>
}