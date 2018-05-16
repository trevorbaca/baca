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
                \time 2/4
                s1 * 1/2
            }   % measure
            {   % measure
                \time 3/4
                s1 * 3/4
            }   % measure
        }
        \new RhythmicStaff
        {
            {   % measure
                \time 2/4
                c'4
                c'4
            }   % measure
            {   % measure
                \time 3/4
                c'4
                c'4
                c'4
            }   % measure
        }
    >>
}