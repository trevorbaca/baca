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
                \time 11/8
                s1 * 11/8
            }   % measure
        }
        \new Staff
        {
            {   % measure
                \time 11/8
                \scaleDurations #'(1 . 1) {
                    c'8
                }
                \scaleDurations #'(1 . 1) {
                    d'8
                    [
                    bf'8
                    ]
                }
                \scaleDurations #'(1 . 1) {
                    fs''8
                    [
                    \acciaccatura {
                        e''16
                    }
                    ef''8
                    ]
                }
                \scaleDurations #'(1 . 1) {
                    af''8
                    [
                    \acciaccatura {
                        g''16
                        [                                                                %! ACC1
                        a'16
                        ]                                                                %! ACC1
                    }
                    c'8
                    ]
                }
                \scaleDurations #'(1 . 1) {
                    d'8
                    [
                    \acciaccatura {
                        bf'16
                        [                                                                %! ACC1
                        fs''16
                        e''16
                        ]                                                                %! ACC1
                    }
                    ef''8
                    ]
                }
                \scaleDurations #'(1 . 1) {
                    af''8
                    [
                    \acciaccatura {
                        g''16
                        [                                                                %! ACC1
                        a'16
                        c'16
                        d'16
                        ]                                                                %! ACC1
                    }
                    bf'8
                    ]
                }
            }   % measure
        }
    >>
}