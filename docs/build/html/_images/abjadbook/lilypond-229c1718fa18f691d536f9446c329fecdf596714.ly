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
        }
        \new RhythmicStaff
        {
            {   % measure
                \time 3/4
                c'8
                c'4
                c'16
                c'4
                c'16
            }   % measure
        }
    >>
}