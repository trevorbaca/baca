\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\markup {
    \concat
        {
            join(
            \concat
                {
                    split(
                    \bold
                        J
                    ", <10>)"
                }
            )
        }
    }