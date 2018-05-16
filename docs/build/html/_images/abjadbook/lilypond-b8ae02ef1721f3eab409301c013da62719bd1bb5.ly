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
                \time 7/4
                s1 * 7/4
            }   % measure
        }
        \new Staff
        {
            {   % measure
                \time 7/4
                \scaleDurations #'(1 . 1) {
                    r4
                }
                \scaleDurations #'(1 . 1) {
                    \acciaccatura {
                        c'16
                    }
                    r4
                }
                \scaleDurations #'(1 . 1) {
                    \acciaccatura {
                        d'16
                        [                                                                %! ACC1
                        bf'16
                        ]                                                                %! ACC1
                    }
                    r4
                }
                \scaleDurations #'(1 . 1) {
                    \acciaccatura {
                        fs''16
                        [                                                                %! ACC1
                        e''16
                        ef''16
                        ]                                                                %! ACC1
                    }
                    r4
                }
                \scaleDurations #'(1 . 1) {
                    \acciaccatura {
                        af''16
                        [                                                                %! ACC1
                        g''16
                        a'16
                        c'16
                        ]                                                                %! ACC1
                    }
                    r4
                }
                \scaleDurations #'(1 . 1) {
                    \acciaccatura {
                        d'16
                        [                                                                %! ACC1
                        bf'16
                        fs''16
                        e''16
                        ef''16
                        ]                                                                %! ACC1
                    }
                    r4
                }
                \scaleDurations #'(1 . 1) {
                    \acciaccatura {
                        af''16
                        [                                                                %! ACC1
                        g''16
                        a'16
                        c'16
                        d'16
                        bf'16
                        ]                                                                %! ACC1
                    }
                    r4
                }
            }   % measure
        }
    >>
}