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
                \time 3/8
                s1 * 3/8
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \scaleDurations #'(1 . 1) {
                        <e' fs'>16
                    }
                    \scaleDurations #'(1 . 1) {
                        <f' ef''>16
                    }
                    \scaleDurations #'(1 . 1) {
                        <a' bf'>16
                    }
                    \scaleDurations #'(1 . 1) {
                        <c'' b''>16
                    }
                    \scaleDurations #'(1 . 1) {
                        <g'' af''>16
                    }
                    \scaleDurations #'(1 . 1) {
                        <cs''' d'''>16
                    }
                }
            }
        >>
    >>
}