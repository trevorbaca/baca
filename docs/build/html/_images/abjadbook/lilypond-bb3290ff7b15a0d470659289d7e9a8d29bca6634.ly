\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\markup {
    \concat
        {
            flatten(
            \line
                {
                    \concat
                        {
                            T
                            \sub
                                3
                            \bold
                                X
                        }
                    /@
                    \bold
                        J
                }
            ", depth=-1)"
        }
    }