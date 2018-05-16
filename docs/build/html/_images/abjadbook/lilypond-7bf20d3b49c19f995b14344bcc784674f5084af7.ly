\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\markup {
    \line
        {
            \concat
                {
                    \concat
                        {
                            permute(
                            \bold
                                X
                            ", row=[10, 0, 2, 6, 8, 7, 5, 3, 1, 9, 4, 11])"
                        }
                }
            Φ
            \bold
                J
        }
    }