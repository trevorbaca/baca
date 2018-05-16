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
            \override TupletBracket.direction = #up
            \override TupletBracket.staff-padding = #3
            autoBeaming = ##f
        }
        {
            {   % measure
                \time 7/4
                \tweak text #tuplet-number::calc-fraction-text
                \times 10/9 {
                    r16
                    c'16
                    c'16
                    c'16
                    <d' e'>4
                    ~
                    <d' e'>16
                }
                \times 8/9 {
                    r16
                    d'16
                    d'16
                    d'16
                    <e' fs'>4
                    ~
                    <e' fs'>16
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 10/9 {
                    r16
                    e'16
                    e'16
                    e'16
                    <fs' gs'>4
                    ~
                    <fs' gs'>16
                }
            }   % measure
        }
    >>
}