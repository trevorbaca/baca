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
                \time 3/2
                s1 * 3/2
            }   % measure
        }
        \new Staff
        {
            {   % measure
                \time 3/2
                \scaleDurations #'(1 . 1) {
                    \override Staff.Stem.stemlet-length = 1.5
                    c'8.
                    [
                    r16
                    d'8
                    \revert Staff.Stem.stemlet-length
                    bf'8
                    ]
                }
                \scaleDurations #'(1 . 1) {
                    \override Staff.Stem.stemlet-length = 1.5
                    fs''8.
                    [
                    r16
                    e''8
                    ef''8
                    af''8.
                    r16
                    \revert Staff.Stem.stemlet-length
                    g''8
                    ]
                }
                \scaleDurations #'(1 . 1) {
                    \override Staff.Stem.stemlet-length = 1.5
                    \revert Staff.Stem.stemlet-length
                    a'8
                }
            }   % measure
        }
    >>
}