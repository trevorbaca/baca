\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Score
    <<
        \new PianoStaff
        <<
            \new Staff
            {
                \new Voice
                {
                    <c' a' bf' d''>1
                }
            }
            \new Staff
            {
                \new Voice
                {
                    s1
                }
            }
        >>
    >>
}