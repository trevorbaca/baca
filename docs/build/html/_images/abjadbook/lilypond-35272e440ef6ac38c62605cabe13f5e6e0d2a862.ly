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
                \time 5/4
                s1 * 5/4
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \scaleDurations #'(1 . 1) {
                        \arpeggioArrowDown                                               %! IC
                        <c' d' bf'>8
                        \arpeggio                                                        %! IC
                        ~
                        [
                        <c' d' bf'>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        f''8
                        ~
                        [
                        f''32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        <ef'' e'' fs'''>8
                        ~
                        [
                        <ef'' e'' fs'''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        <g' af''>8
                        ~
                        [
                        <g' af''>32
                        ]
                        r16.
                    }
                    \scaleDurations #'(1 . 1) {
                        a'8
                        ~
                        [
                        a'32
                        ]
                        r16.
                    }
                }
            }
        >>
    >>
}