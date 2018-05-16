\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Score
    <<
        \new Staff
        {
            \new Voice
            {
                <c' d' ef' bqs'>1
            }
        }
    >>
}