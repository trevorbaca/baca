\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Staff
    {
        c'4.
        ^ \markup {
            \small
                3/8
            }
        d'8
        ~
        ^ \markup {
            \small
                1/2
            }
        d'4.
        e'16
        [
        ^ \markup {
            \small
                1/16
            }
        ef'16
        ]
        ^ \markup {
            \small
                1/16
            }
    }
}