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
                \time 6/32
                s1 * 3/16
            }   % measure
        }
        \new RhythmicStaff
        {
            {   % measure
                \time 6/32
                c'8.
            }   % measure
        }
    >>
}