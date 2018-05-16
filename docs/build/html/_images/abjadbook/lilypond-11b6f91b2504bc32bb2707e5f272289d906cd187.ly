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
                    <fs' g'>1
                }
            }
            \new Staff
            {
                \new Voice
                {
                    <bf bqf>1
                }
            }
        >>
    >>
}