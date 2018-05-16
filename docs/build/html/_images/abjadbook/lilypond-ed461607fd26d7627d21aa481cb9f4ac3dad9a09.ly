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
                \time 15/8
                s1 * 15/8
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \scaleDurations #'(1 . 1) {
                        r8
                        <c' d' ef'>4
                    }
                    \scaleDurations #'(1 . 1) {
                        <c' d' ef'>4
                    }
                    \scaleDurations #'(1 . 1) {
                        <c d ef>4
                    }
                    \scaleDurations #'(1 . 1) {
                        <c d ef>4
                    }
                    \scaleDurations #'(1 . 1) {
                        <c'' d'' ef''>4
                    }
                    \scaleDurations #'(1 . 1) {
                        <c'' d'' ef''>4
                        r4
                    }
                }
            }
        >>
    >>
}