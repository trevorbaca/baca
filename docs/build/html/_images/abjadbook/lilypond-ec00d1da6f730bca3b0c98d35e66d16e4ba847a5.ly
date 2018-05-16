\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Score
    <<
        \new StaffGroup
        <<
            \new Staff
            {
                {   % measure
                    \time 4/8
                    r8
                    d'8
                    <bf bqf>4
                }   % measure
                {   % measure
                    \time 3/8
                    r8
                    r8
                    r8
                }   % measure
            }
            \new Staff
            {
                {   % measure
                    \time 4/8
                    g'4
                    fs'8
                    r8
                }   % measure
                {   % measure
                    \time 3/8
                    r8
                    r8
                    r8
                }   % measure
            }
        >>
    >>
}