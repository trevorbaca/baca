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
                \time 45/32
                s1 * 45/32
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
                        [
                        s32
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 1
                        d'8
                        s32
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 1
                        bf'8
                        s32
                    }
                    \scaleDurations #'(1 . 1) {
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 1
                        fs''8
                        s32
                        s8
                        s32
                        s8
                        s32
                        s8
                        s32
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 1
                        g''8
                        s32
                    }
                    \scaleDurations #'(1 . 1) {
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 1
                        a'8
                        s32
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
                        c'8
                        ~
                        [
                        c'32
                        d'8
                        ~
                        d'32
                        bf'8
                        ~
                        bf'32
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        fs''8
                        ~
                        [
                        fs''32
                        e''8
                        ~
                        e''32
                        ef''8
                        ~
                        ef''32
                        af''8
                        ~
                        af''32
                        g''8
                        ~
                        g''32
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        a'8
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