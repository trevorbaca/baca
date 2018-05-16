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
                \time 11/8
                s1 * 11/8
            }   % measure
        }
        \new Staff
        \with
        {
            \override TupletBracket.staff-padding = #1.5
        }
        {
            {   % measure
                \time 11/8
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    c'8
                    [
                    d'8
                    ]
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 7/9 {
                    bf'8.
                    [
                    fs''8.
                    e''8.
                    ]
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 1/1 {
                    ef''8
                    [
                    af''8
                    ]
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 7/9 {
                    g''8.
                    [
                    a'8.
                    ]
                    r8.
                }
            }   % measure
        }
    >>
}