\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Staff
    {
        {   % measure
            \time 2/8
            <c' bf'>8
            <g' a'>8
        }   % measure
        {   % measure
            af'8
            r8
        }   % measure
        {   % measure
            r8
            gf'8
        }   % measure
    }
}