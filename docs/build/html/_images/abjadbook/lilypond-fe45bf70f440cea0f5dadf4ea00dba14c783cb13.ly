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
                        -\accent                                                         %! IC
                        [
                        d'16
                        -\accent                                                         %! IC
                        ]
                        bf'4
                        -\accent                                                         %! IC
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override Script.color = #red                                    %! OC1
                        fs''16
                        -\accent                                                         %! IC
                        [
                        e''16
                        -\accent                                                         %! IC
                        ]
                        ef''4
                        -\accent                                                         %! IC
                        ~
                        ef''16
                        r16
                        af''16
                        -\accent                                                         %! IC
                        [
                        g''16
                        -\accent                                                         %! IC
                        ]
                        \revert Script.color                                             %! OC2
                    }
                    \times 4/5 {
                        a'16
                        -\accent                                                         %! IC
                        r4
                        \revert TupletBracket.staff-padding                              %! OC2
                    }
                }
            }
        >>
    >>
}