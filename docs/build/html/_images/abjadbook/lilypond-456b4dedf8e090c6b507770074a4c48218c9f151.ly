\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\markup {
    \line
        {
            \bold
                X
            /@
            \concat
                {
                    P
                    \sub
                        [3]
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
        }
    }