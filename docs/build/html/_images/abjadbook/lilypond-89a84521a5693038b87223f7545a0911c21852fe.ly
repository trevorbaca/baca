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
                \time 27/16
                s1 * 27/16
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
                        s8.
                        [
                        s8.
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 1
                        bf'8.
                        -\accent                                                         %! IC
                    }
                    \scaleDurations #'(1 . 1) {
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 1
                        fs''8.
                        -\accent                                                         %! IC
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 1
                        e''8.
                        -\accent                                                         %! IC
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 1
                        ef''8.
                        -\accent                                                         %! IC
                        s8.
                        s8.
                    }
                    \scaleDurations #'(1 . 1) {
                        s8.
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
                        c'8.
                        [
                        d'8.
                        bf'8.
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        fs''8.
                        [
                        e''8.
                        ef''8.
                        af''8.
                        g''8.
                        ]
                    }
                    \scaleDurations #'(1 . 1) {
                        a'8.
                    }
                }
            }
        >>
    >>
}