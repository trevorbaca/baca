\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

\layout {
    \accidentalStyle forget
    indent = #0
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
        \override Stem.stencil = ##f
        \override TimeSignature.stencil = ##f
        proportionalNotationDuration = #(ly:make-moment 1 12)
    }
    <<
        \new Staff
        {
            \new Voice
            {
                c'8
                b'8
                d'8
                e'8
                f'8
                g'8
                e'8
                b'8
                a'8
                c'8
                \bar "|." %! SCORE1
                \override Score.BarLine.transparent = ##f
            }
        }
    >>
}