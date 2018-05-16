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
                \time 11/8
                s1 * 11/8
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TupletBracket.staff-padding = #5                       %! OC1
                        r8
                        c'16
                        [
                        ^ \markup {
                            \small
                                C4
                            }
                        d'16
                        ]
                        ^ \markup {
                            \small
                                D4
                            }
                        bf'4
                        ~
                        ^ \markup {
                            \small
                                Bb4
                            }
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        fs''16
                        [
                        ^ \markup {
                            \small
                                "F#5"
                            }
                        e''16
                        ]
                        ^ \markup {
                            \small
                                E5
                            }
                        ef''4
                        ~
                        ^ \markup {
                            \small
                                Eb5
                            }
                        ef''16
                        r16
                        af''16
                        [
                        ^ \markup {
                            \small
                                Ab5
                            }
                        g''16
                        ]
                        ^ \markup {
                            \small
                                G5
                            }
                    }
                    \times 4/5 {
                        a'16
                        ^ \markup {
                            \small
                                A4
                            }
                        r4
                        \revert TupletBracket.staff-padding                              %! OC2
                    }
                }
            }
        >>
    >>
}