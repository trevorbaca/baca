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
                \time 9/4
                s1 * 9/4
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \scaleDurations #'(1 . 1) {
                        c'16
                        [
                        d'16
                        bf'16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        fs'16
                        [
                        e'16
                        ef'16
                        af'16
                        g'16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        a'16
                    }
                    \scaleDurations #'(1 . 1) {
                        ef'16
                        [
                        f'16
                        cs'16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        a'16
                        [
                        g'16
                        fs'16
                        b'16
                        bf'16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        c'16
                    }
                    \scaleDurations #'(1 . 1) {
                        fs'16
                        [
                        af'16
                        e'16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        c'16
                        [
                        bf'16
                        a'16
                        d'16
                        cs'16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        ef'16
                    }
                    \scaleDurations #'(1 . 1) {
                        a'16
                        [
                        b'16
                        g'16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        ef'16
                        [
                        cs'16
                        c'16
                        f'16
                        e'16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        fs'16
                    }
                }
            }
        >>
    >>
}