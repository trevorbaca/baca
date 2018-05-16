\version "2.19.0"
\language "english"

\include "default.ily"
\include "rhythm-maker-docs.ily"

\score {
    \new Score
    \with
    {
        \override SpacingSpanner.strict-grace-spacing = ##f
        \override SpacingSpanner.strict-note-spacing = ##f
    }
    <<
        \new GlobalContext
        {
            {   % measure
                \time 3/2
                s1 * 3/2
            }   % measure
        }
        \new Staff
        {
            {   % measure
                \time 3/2
                \scaleDurations #'(1 . 1) {
                    c'4
                }
                \scaleDurations #'(1 . 1) {
                    \acciaccatura {
                        d'16
                    }
                    bf'4
                }
                \scaleDurations #'(1 . 1) {
                    \acciaccatura {
                        fs''16
                        [                                                                %! ACC1
                        e''16
                        ]                                                                %! ACC1
                    }
                    ef''4
                }
                \scaleDurations #'(1 . 1) {
                    \acciaccatura {
                        af''16
                        [                                                                %! ACC1
                        g''16
                        a'16
                        ]                                                                %! ACC1
                    }
                    c'4
                }
                \scaleDurations #'(1 . 1) {
                    \acciaccatura {
                        d'16
                        [                                                                %! ACC1
                        bf'16
                        fs''16
                        e''16
                        ]                                                                %! ACC1
                    }
                    ef''4
                }
                \scaleDurations #'(1 . 1) {
                    \acciaccatura {
                        af''16
                        [                                                                %! ACC1
                        g''16
                        a'16
                        c'16
                        d'16
                        ]                                                                %! ACC1
                    }
                    bf'4
                }
            }   % measure
        }
    >>
}