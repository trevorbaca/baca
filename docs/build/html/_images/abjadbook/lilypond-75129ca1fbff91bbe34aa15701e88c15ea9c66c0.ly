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
                \time 3/8
                s1 * 3/8
            }   % measure
            {   % measure
                \time 5/8
                s1 * 5/8
            }   % measure
        }
        \new RhythmicStaff
        {
            {   % measure
                \time 7/8
                c'4
                c'4
                c'4
                c'8
            }   % measure
            {   % measure
                \time 3/8
                c'4
                c'8
            }   % measure
            {   % measure
                \time 5/8
                c'4
                c'4
                c'8
            }   % measure
        }
    >>
}