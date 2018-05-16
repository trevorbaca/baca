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
                <fs' g' bf' bqf'>1
            }
        }
    >>
}