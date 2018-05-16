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
                \time 5/8
                s1 * 5/8
            }   % measure
        }
        \new RhythmicStaff
        {
            {   % measure
                \time 5/8
                c'4
                c'4
                c'8
            }   % measure
        }
    >>
}