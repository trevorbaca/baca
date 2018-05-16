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
                \time 9/8
                s1 * 9/8
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \override TupletBracket.stencil = ##f
                    \override TupletNumber.stencil = ##f
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/5 {
                        s16
                        [
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        d'16
                        -\accent                                                         %! IC
                        s16
                        s16
                        s16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/5 {
                        s16
                        s16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        g''16
                        -\accent                                                         %! IC
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        a'16
                        -\accent                                                         %! IC
                        s16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/5 {
                        s16
                        s16
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        fs''16
                        -\accent                                                         %! IC
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        e''16
                        -\accent                                                         %! IC
                        s16
                        ]
                    }
                    \revert TupletBracket.stencil
                    \revert TupletNumber.stencil
                }
            }
            \context Voice = "Voice 2"
            {
                \voiceTwo
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/5 {
                        \set stemLeftBeamCount = 0
                        \set stemRightBeamCount = 2
                        c'16
                        -\staccato                                                       %! IC
                        [
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        d'16
                        -\staccato                                                       %! IC
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        bf'16
                        -\staccato                                                       %! IC
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        fs''16
                        -\staccato                                                       %! IC
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 1
                        e''16
                        -\staccato                                                       %! IC
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/5 {
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 2
                        ef''16
                        -\staccato                                                       %! IC
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        af''16
                        -\staccato                                                       %! IC
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        g''16
                        -\staccato                                                       %! IC
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        a'16
                        -\staccato                                                       %! IC
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 1
                        c'16
                        -\staccato                                                       %! IC
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/5 {
                        \set stemLeftBeamCount = 1
                        \set stemRightBeamCount = 2
                        d'16
                        -\staccato                                                       %! IC
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        bf'16
                        -\staccato                                                       %! IC
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        fs''16
                        -\staccato                                                       %! IC
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 2
                        e''16
                        -\staccato                                                       %! IC
                        \set stemLeftBeamCount = 2
                        \set stemRightBeamCount = 0
                        ef''16
                        -\staccato                                                       %! IC
                        ]
                    }
                }
            }
        >>
    >>
}