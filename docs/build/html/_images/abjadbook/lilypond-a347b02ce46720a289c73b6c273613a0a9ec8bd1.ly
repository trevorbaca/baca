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
                \time 5/4
                s1 * 5/4
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
                        \override Stem.direction = #down                                 %! OC1
                        b'16
                        ~                                                                %! SC
                        [
                        b'16
                        ]
                        c''4
                        ~                                                                %! SC
                        c''16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 7/8 {
                        \override Tie.direction = #up                                    %! OC1
                        b'16
                        ~                                                                %! SC
                        [
                        b'16
                        ~                                                                %! SC
                        ]
                        b'4
                        ~                                                                %! SC
                        b'16
                        \revert Tie.direction                                            %! OC2
                        r16
                    }
                    \times 4/5 {
                        b'16
                        \revert Stem.direction                                           %! OC2
                        r4
                        \revert TupletBracket.staff-padding                              %! OC2
                    }
                }
            }
        >>
    >>
}