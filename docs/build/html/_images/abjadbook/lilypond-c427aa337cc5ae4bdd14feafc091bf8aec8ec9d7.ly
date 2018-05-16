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
                \time 11/16
                s1 * 11/16
            }   % measure
        }
        \new Staff
        \with
        {
            \override DynamicLineSpanner.staff-padding = #4.5
        }
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \scaleDurations #'(1 . 1) {
                        c'16
                        \<                                                               %! HC1
                        \p                                                               %! HC1
                        [
                        d'16
                        bf'16
                        fs''16
                        \f                                                               %! HC1
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        e''16
                        [
                        ef''16
                        b''16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        g''16
                        \>                                                               %! HC1
                        \f                                                               %! HC1
                        [
                        cs''16
                        a'16
                        af'16
                        \p                                                               %! HC1
                        ]
                    }
                }
            }
        >>
    >>
}