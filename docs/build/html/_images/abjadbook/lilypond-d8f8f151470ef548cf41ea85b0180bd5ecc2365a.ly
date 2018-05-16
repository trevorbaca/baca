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
                \time 7/4
                s1 * 7/4
            }   % measure
        }
        \new Staff
        \with
        {
            \override Beam.positions = #'(-6 . -6)
            \override Stem.direction = #down
        }
        {
            {   % measure
                \time 7/4
                \tweak edge-height #'(0.7 . 0)
                \times 2/3 {
                    c'8
                }
                \tweak edge-height #'(0.7 . 0)
                \times 2/3 {
                    d'8
                    [
                    bf'8
                    ]
                }
                \times 2/3 {
                    fs''8
                    [
                    e''8
                    ef''8
                    ]
                }
                \tweak edge-height #'(0.7 . 0)
                \times 2/3 {
                    af''8
                    [
                    g''8
                    a'8
                    c'8
                    ]
                }
                \tweak edge-height #'(0.7 . 0)
                \times 2/3 {
                    d'8
                    [
                    bf'8
                    fs''8
                    e''8
                    ef''8
                    ]
                }
                \times 2/3 {
                    af''8
                    [
                    g''8
                    a'8
                    c'8
                    d'8
                    bf'8
                    ]
                }
            }   % measure
        }
    >>
}