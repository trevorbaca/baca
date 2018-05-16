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
                            A
                            \bold
                                X
                        }
                    \concat
                        {
                            T
                            \sub
                                3
                            \bold
                                X
                        }
                }
            Φ
            \bold
                J
        }
    }