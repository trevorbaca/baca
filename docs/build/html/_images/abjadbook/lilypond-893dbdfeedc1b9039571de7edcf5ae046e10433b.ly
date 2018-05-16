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
                \time 15/16
                s1 * 15/16
            }   % measure
        }
        \new Staff
        \with
        {
            \override TupletBracket.staff-padding = #1.5
        }
        {
            {   % measure
                \time 15/16
                \tweak text #tuplet-number::calc-fraction-text
                \times 5/4 {
                    \override Staff.Stem.stemlet-length = 0.75
                    r16
                    [
                    d'16
                    \revert Staff.Stem.stemlet-length
                    bf'8
                    ]
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 7/6 {
                    \override Staff.Stem.stemlet-length = 0.75
                    fs''16
                    [
                    e''16
                    ef''8
                    af''16
                    \revert Staff.Stem.stemlet-length
                    r16
                    ]
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 3/2 {
                    \override Staff.Stem.stemlet-length = 0.75
                    \revert Staff.Stem.stemlet-length
                    a'8
                }
            }   % measure
        }
    >>
}