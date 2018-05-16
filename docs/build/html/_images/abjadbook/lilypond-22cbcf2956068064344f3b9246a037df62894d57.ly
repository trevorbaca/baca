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
                \time 3/4
                s1 * 3/4
            }   % measure
            {   % measure
                \time 6/8
                s1 * 3/4
            }   % measure
        }
        \new RhythmicStaff
        {
            {   % measure
                \time 3/4
                c'4
                c'4
                c'4
            }   % measure
            {   % measure
                \time 6/8
                c'4
                c'4
                c'4
            }   % measure
        }
    >>
}