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
                \time 3/2
                s1 * 3/2
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \scaleDurations #'(1 . 1) {
                        \override Glissando.thickness = #'3                              %! OC1
                        \clef "treble"                                                   %! IC
                        ef'16
                        \glissando                                                       %! SC
                        [
                        \hide NoteHead                                                   %! SC
                        \override Accidental.stencil = ##f                               %! SC
                        \override NoteColumn.glissando-skip = ##t                        %! SC
                        \override NoteHead.no-ledgers = ##t                              %! SC
                        e'16
                        \glissando                                                       %! SC
                        f'16
                        \glissando                                                       %! SC
                        f'16
                        \glissando                                                       %! SC
                        f'16
                        \glissando                                                       %! SC
                        g'16
                        \glissando                                                       %! SC
                        g'16
                        \glissando                                                       %! SC
                        g'16
                        \glissando                                                       %! SC
                        a'16
                        \glissando                                                       %! SC
                        a'16
                        \glissando                                                       %! SC
                        a'16
                        \glissando                                                       %! SC
                        b'16
                        ]
                        \glissando                                                       %! SC
                    }
                    \scaleDurations #'(1 . 1) {
                        b'16
                        \glissando                                                       %! SC
                        [
                        c''16
                        \glissando                                                       %! SC
                        c''16
                        \glissando                                                       %! SC
                        c''16
                        \glissando                                                       %! SC
                        d''16
                        \glissando                                                       %! SC
                        d''16
                        \glissando                                                       %! SC
                        d''16
                        \glissando                                                       %! SC
                        e''16
                        \glissando                                                       %! SC
                        e''16
                        \glissando                                                       %! SC
                        e''16
                        \glissando                                                       %! SC
                        f''16
                        \glissando                                                       %! SC
                        \revert Accidental.stencil                                       %! SC
                        \revert NoteColumn.glissando-skip                                %! SC
                        \revert NoteHead.no-ledgers                                      %! SC
                        \undo \hide NoteHead                                             %! SC
                        fs''16
                        ]
                        \revert Glissando.thickness                                      %! OC2
                    }
                }
            }
        >>
    >>
}