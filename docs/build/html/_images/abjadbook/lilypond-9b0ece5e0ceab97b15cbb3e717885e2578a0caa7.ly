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
                \time 2/8
                s1 * 1/4
            }   % measure
            {   % measure
                s1 * 1/4
            }   % measure
            {   % measure
                \time 4/8
                s1 * 1/2
            }   % measure
            {   % measure
                s1 * 1/2
            }   % measure
            {   % measure
                \time 2/4
                s1 * 1/2
            }   % measure
        }
        \new RhythmicStaff
        {
            {   % measure
                \time 2/8
                c'4
            }   % measure
            {   % measure
                c'4
            }   % measure
            {   % measure
                \time 4/8
                c'2
            }   % measure
            {   % measure
                c'2
            }   % measure
            {   % measure
                \time 2/4
                c'2
            }   % measure
        }
    >>
}