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
                \time 19/16
                s1 * 19/16
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
                        s8
                        s16
                        d'16
                        s16
                        s16
                        s16
                    }
                    \scaleDurations #'(1 . 1) {
                        s16
                        s16
                        g''16
                        [
                        a'16
                        ]
                        s16
                    }
                    \scaleDurations #'(1 . 1) {
                        s16
                        s16
                        fs''16
                        [
                        e''16
                        ]
                        s16
                        s8
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
                        r8
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        c'16
                        [
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        d'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        bf'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        fs''16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 1
                        e''16
                    }
                    \scaleDurations #'(1 . 1) {
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 2
                        ef''16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        af''16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        g''16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        a'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 1
                        c'16
                    }
                    \scaleDurations #'(1 . 1) {
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 2
                        d'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        bf'16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        fs''16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        e''16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        ef''16
                        ]
                        r8
                    }
                }
            }
        >>
    >>
}