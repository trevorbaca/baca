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
                \time 15/16
                s1 * 15/16
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \scaleDurations #'(1 . 1) {
                        d''4
                        ~
                        d''16
                        d''4
                        ~
                        d''16
                        d''4
                        ~
                        d''16
                    }
                }
            }
        >>
    >>
}