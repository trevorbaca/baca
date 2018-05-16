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
                \time 7/8
                s1 * 7/8
            }   % measure
            {   % measure
                s1 * 7/8
            }   % measure
            {   % measure
                \time 7/16
                s1 * 7/16
            }   % measure
        }
        \new RhythmicStaff
        {
            {   % measure
                \time 7/8
                c'2..
            }   % measure
            {   % measure
                c'2..
            }   % measure
            {   % measure
                \time 7/16
                c'4..
            }   % measure
        }
    >>
}