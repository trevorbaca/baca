\version "2.19.0"
\language "english"

\include "default.ily"
\include "rhythm-maker-docs.ily"

\score {
    \new Score
    <<
        \new GlobalContext
        {
            {   % measure
                \time 7/4
                s1 * 7/4
            }   % measure
        }
        \new Staff
        \with
        {
            \override TextScript.staff-padding = #6
            \override TupletBracket.direction = #up
            \override TupletBracket.staff-padding = #3
            autoBeaming = ##f
        }
        {
            {   % measure
                \time 7/4
                \tweak text #tuplet-number::calc-fraction-text
                \times 10/9 {
                    r16
                    ^ \markup {
                        \bold
                            \with-color
                                #red
                                *
                        }
                    bf'16
                    ^ \markup {
                        \bold
                            \with-color
                                #red
                                *
                        }
                    <a'' b''>16
                    ^ \markup {
                        \bold
                            \with-color
                                #red
                                *
                        }
                    c'16
                    ^ \markup {
                        \bold
                            \with-color
                                #red
                                *
                        }
                    <d' e'>4
                    ~
                    ^ \markup {
                        \bold
                            \with-color
                                #red
                                *
                        }
                    _ \markup {
                        \bold
                            \with-color
                                #blue
                                *
                        }
                    <d' e'>16
                    _ \markup {
                        \bold
                            \with-color
                                #blue
                                *
                        }
                }
                \times 8/9 {
                    r16
                    _ \markup {
                        \bold
                            \with-color
                                #blue
                                *
                        }
                    bf'16
                    _ \markup {
                        \bold
                            \with-color
                                #blue
                                *
                        }
                    <a'' b''>16
                    ^ \markup {
                        \bold
                            \with-color
                                #red
                                *
                        }
                    _ \markup {
                        \bold
                            \with-color
                                #blue
                                *
                        }
                    d'16
                    ^ \markup {
                        \bold
                            \with-color
                                #red
                                *
                        }
                    <e' fs'>4
                    ~
                    ^ \markup {
                        \bold
                            \with-color
                                #red
                                *
                        }
                    <e' fs'>16
                    ^ \markup {
                        \bold
                            \with-color
                                #red
                                *
                        }
                }
                \tweak text #tuplet-number::calc-fraction-text
                \times 10/9 {
                    r16
                    ^ \markup {
                        \bold
                            \with-color
                                #red
                                *
                        }
                    _ \markup {
                        \bold
                            \with-color
                                #blue
                                *
                        }
                    bf'16
                    _ \markup {
                        \bold
                            \with-color
                                #blue
                                *
                        }
                    <a'' b''>16
                    _ \markup {
                        \bold
                            \with-color
                                #blue
                                *
                        }
                    e'16
                    _ \markup {
                        \bold
                            \with-color
                                #blue
                                *
                        }
                    <fs' gs'>4
                    ~
                    ^ \markup {
                        \bold
                            \with-color
                                #red
                                *
                        }
                    _ \markup {
                        \bold
                            \with-color
                                #blue
                                *
                        }
                    <fs' gs'>16
                    ^ \markup {
                        \bold
                            \with-color
                                #red
                                *
                        }
                }
            }   % measure
        }
    >>
}