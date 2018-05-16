\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\markup {
    \line
        {
            \bold
                Q
            =
            \concat
                {
                    r
                    \sub
                        2
                    \concat
                        {
                            r
                            \sub
                                1
                            \bold
                                J
                        }
                }
        }
    }