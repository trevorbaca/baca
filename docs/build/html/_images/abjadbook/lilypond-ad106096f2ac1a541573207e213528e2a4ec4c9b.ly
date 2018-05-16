\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\header {
    tagline = \markup {
        \null
        }
}

\score {
    \new Score
    \with
    {
        proportionalNotationDuration = #(ly:make-moment 1 8)
    }
    <<
        \new Staff
        \with
        {
            \consists Horizontal_bracket_engraver
            \override Clef.stencil = ##f
            \override HorizontalBracket.bracket-flare = #'(0 . 0)
            \override HorizontalBracket.direction = #up
            \override HorizontalBracket.extra-offset = #'(-4 . 0)
            \override HorizontalBracket.staff-padding = #2.5
            \override Rest.transparent = ##t
            \override TextScript.extra-offset = #'(-4 . 0)
            \override TextScript.staff-padding = #4.5
        }
        {
            {   % measure
                \time 3/8
                r1 * 3/8
                \startGroup
                ^ \markup {
                    \circle
                        \smaller
                            0
                    }
            }   % measure
            {   % measure
                \time 3/16
                r1 * 3/16
            }   % measure
            {   % measure
                \time 3/16
                r1 * 3/16
                \stopGroup
            }   % measure
            {   % measure
                \time 5/8
                r1 * 5/8
                \startGroup
                ^ \markup {
                    \circle
                        \smaller
                            1
                    }
            }   % measure
            {   % measure
                \time 5/16
                r1 * 5/16
            }   % measure
            {   % measure
                \time 5/16
                r1 * 5/16
            }   % measure
            {   % measure
                \time 5/16
                r1 * 5/16
                \stopGroup
            }   % measure
        }
    >>
}