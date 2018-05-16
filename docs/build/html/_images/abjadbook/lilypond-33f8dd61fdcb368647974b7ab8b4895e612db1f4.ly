\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\score {
    \new Staff
    {
        \time 5/4
        bf4
        ~
        bf16
        bqf4
        ~
        bqf16
        fs'4
        ~
        fs'16
        g'4
        ~
        g'16
    }
}