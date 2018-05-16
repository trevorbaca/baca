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
                \time 3/4
                s1 * 3/4
            }   % measure
        }
        \new Staff
        {
            {   % measure
                \time 3/4
                \scaleDurations #'(1 . 1) {
                    c'8
                }
                \scaleDurations #'(1 . 1) {
                    \acciaccatura {
                        d'8
                    }
                    bf'8
                }
                \scaleDurations #'(1 . 1) {
                    \acciaccatura {
                        fs''8
                        [                                                                %! ACC1
                        e''8
                        ]                                                                %! ACC1
                    }
                    ef''8
                }
                \scaleDurations #'(1 . 1) {
                    \acciaccatura {
                        af''8
                        [                                                                %! ACC1
                        g''8
                        a'8
                        ]                                                                %! ACC1
                    }
                    c'8
                }
                \scaleDurations #'(1 . 1) {
                    \acciaccatura {
                        d'8
                        [                                                                %! ACC1
                        bf'8
                        fs''8
                        e''8
                        ]                                                                %! ACC1
                    }
                    ef''8
                }
                \scaleDurations #'(1 . 1) {
                    \acciaccatura {
                        af''8
                        [                                                                %! ACC1
                        g''8
                        a'8
                        c'8
                        d'8
                        ]                                                                %! ACC1
                    }
                    bf'8
                }
            }   % measure
        }
    >>
}