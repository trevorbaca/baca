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
                        -\downbow                                                        %! IC
                        [
                        d'16
                        -\upbow                                                          %! IC
                        ]
                        bf'4
                        -\downbow                                                        %! IC
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        -\upbow                                                          %! IC
                        [
                        e''16
                        -\downbow                                                        %! IC
                        ]
                        ef''4
                        -\upbow                                                          %! IC
                        ~
                        ef''16
                        r16
                        af''16
                        -\downbow                                                        %! IC
                        [
                        g''16
                        -\upbow                                                          %! IC
                        ]
                    }
                    \times 4/5 {
                        a'16
                        -\downbow                                                        %! IC
                        r4
                        \revert TupletBracket.staff-padding                              %! OC2
                    }
                }
            }
        >>
    >>
}