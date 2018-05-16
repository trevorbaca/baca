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
                        \override Beam.positions = #'(6 . 6)                             %! OC1
                        r8
                        c'16
                        [
                        d'16
                        bf'16
                        ]
                    }
                    \times 4/5 {
                        fs''16
                        [
                        e''16
                        ef''16
                        af''16
                        g''16
                        ]
                    }
                    \times 4/5 {
                        a'16
                        r4
                        \revert Beam.positions                                           %! OC2
                    }
                }
            }
        >>
    >>
}