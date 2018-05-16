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
                \time 9/8
                s1 * 9/8
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \override TupletBracket.stencil = ##f
                    \override TupletNumber.stencil = ##f
                    \scaleDurations #'(1 . 1) {
                        \set stemLeftBeamCount = 0
                        \set stemRightBeamCount = 2
                        c'16
                        -\accent                                                         %! IC
                        [
                        s16
                        s16
                        s16
                        s16
                    }
                    \scaleDurations #'(1 . 1) {
                        s16
                        s16
                        s16
                        s16
                    }
                    \scaleDurations #'(1 . 1) {
                        s16
                        s16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        bf'16
                        -\accent                                                         %! IC
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        fs''16
                        -\accent                                                         %! IC
                        s16
                    }
                    \scaleDurations #'(1 . 1) {
                        s16
                        s16
                        s16
                        s16
                        ]
                    }
                    \revert TupletBracket.stencil
                    \revert TupletNumber.stencil
                }
            }
            \context Voice = "Voice 2"
            {
                \voiceTwo
                {
                    \scaleDurations #'(1 . 1) {
                        c'16
                        [
                        d'16
                        bf'16
                        fs''16
                        e''16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        ef''16
                        [
                        af''16
                        g''16
                        a'16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        c'16
                        [
                        d'16
                        bf'16
                        fs''16
                        e''16
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        ef''16
                        [
                        af''16
                        g''16
                        a'16
                        ]
                    }
                }
            }
        >>
    >>
}