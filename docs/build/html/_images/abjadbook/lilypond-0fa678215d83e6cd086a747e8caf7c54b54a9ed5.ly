\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\markup {
    \concat
        {
            flatten(
            \bold
                J
            ", depth=-1)"
        }
    }