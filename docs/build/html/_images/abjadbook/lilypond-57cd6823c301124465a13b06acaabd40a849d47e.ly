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
                    \scaleDurations #'(1 . 1) {
                        c'8
                        \fermata                                                         %! IC
                        ~
                        [
                        c'32
                        d'8
                        bf'8
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        fs''8
                        \fermata                                                         %! IC
                        ~
                        [
                        fs''32
                        e''8
                        ef''8
                        af''8
                        \fermata                                                         %! IC
                        ~
                        af''32
                        g''8
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        a'8
                        \fermata                                                         %! IC
                        ~
                        [
                        a'32
                        ]
                    }
                }
            }
        >>
    >>
}