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
                \time 13/16
                s1 * 13/16
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \scaleDurations #'(1 . 1) {
                        \override Staff.Stem.stemlet-length = 2
                        r8
                        [
                        c'16
                        d'16
                        \revert Staff.Stem.stemlet-length
                        bf'16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        \override Staff.Stem.stemlet-length = 2
                        fs''16
                        [
                        e''16
                        ef''16
                        af''16
                        \revert Staff.Stem.stemlet-length
                        g''16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        \override Staff.Stem.stemlet-length = 2
                        a'16
                        [
                        \revert Staff.Stem.stemlet-length
                        r8
                        ]
                    }
                }
            }
        >>
    >>
}