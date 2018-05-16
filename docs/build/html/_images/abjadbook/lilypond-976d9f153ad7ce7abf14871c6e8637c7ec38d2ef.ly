\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

#(set-global-staff-size 16)

\layout {
    \accidentalStyle dodecaphonic
    indent = #0
    line-width = #287.5
    ragged-right = ##t
}

\paper {
    markup-system-spacing.padding = 8
    system-system-spacing.padding = 10
    top-markup-spacing.padding = 4
}

\score {
    \new Score
    \with
    {
        \override BarLine.transparent = ##t
        \override BarNumber.stencil = ##f
        \override Beam.stencil = ##f
        \override Flag.stencil = ##f
        \override HorizontalBracket.staff-padding = #4
        \override SpacingSpanner.strict-grace-spacing = ##t
        \override SpacingSpanner.strict-note-spacing = ##t
        \override SpacingSpanner.uniform-stretching = ##t
        \override Stem.stencil = ##f
        \override TextScript.X-extent = ##f
        \override TextScript.staff-padding = #2
        \override TimeSignature.stencil = ##f
        proportionalNotationDuration = #(ly:make-moment 1 16)
    }
    <<
        \new Staff
        {
            \new Voice
            \with
            {
                \consists Horizontal_bracket_engraver
            }
            {
                \time 1/8
                ef'8
                \startGroup
                ^ \markup { 0 }
                f'8
                a8
                \stopGroup
                s8
                af8
                \startGroup
                ^ \markup { 1 }
                fs8
                g8
                bf8
                af8
                c8
                \stopGroup
                s8
                b,8
                \startGroup
                ^ \markup { 2 }
                cs8
                d8
                e8
                \stopGroup
                s8
                \bar "|."                                                                %! SCORE1
                \override Score.BarLine.transparent = ##f
            }
        }
    >>
}