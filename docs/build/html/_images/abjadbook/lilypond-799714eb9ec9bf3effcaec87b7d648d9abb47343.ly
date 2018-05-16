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
                g'8
                \startGroup
                \startGroup
                ^ \markup { 0 }
                cs'8
                ef'8
                e'8
                f'8
                b'8
                \stopGroup
                \stopGroup
                s8
                ef'8
                \startGroup
                \startGroup
                ^ \markup { 1 }
                f'8
                fs'8
                g'8
                \stopGroup
                \stopGroup
                s8
                a'8
                \startGroup
                \startGroup
                ^ \markup { 2 }
                bf'8
                c'8
                af'8
                \stopGroup
                \stopGroup
                s8
                g'8
                \startGroup
                \startGroup
                ^ \markup { 3 }
                ef'8
                \stopGroup
                s8
                f'8
                \startGroup
                ^ \markup { 4 }
                fs'8
                \stopGroup
                \stopGroup
                s8
                af'8
                \startGroup
                \startGroup
                ^ \markup { 5 }
                a'8
                bf'8
                c'8
                \stopGroup
                s8
                b'8
                \startGroup
                ^ \markup { 6 }
                g'8
                cs'8
                ef'8
                e'8
                f'8
                \stopGroup
                s8
                c'8
                \startGroup
                ^ \markup { 7 }
                af'8
                a'8
                bf'8
                \stopGroup
                \stopGroup
                s8
                f'8
                \startGroup
                \startGroup
                ^ \markup { 8 }
                b'8
                \stopGroup
                \stopGroup
                s8
                g'8
                \startGroup
                \startGroup
                ^ \markup { 9 }
                cs'8
                \stopGroup
                \stopGroup
                s8
                ef'8
                \startGroup
                \startGroup
                ^ \markup { 10 }
                e'8
                \stopGroup
                \stopGroup
                s8
                fs'8
                \stopGroup
                \startGroup
                \startGroup
                ^ \markup { 11 }
                s8
                g'8
                \startGroup
                ^ \markup { 12 }
                ef'8
                \stopGroup
                \stopGroup
                s8
                f'8
                \stopGroup
                \startGroup
                \startGroup
                ^ \markup { 13 }
                s8
                e'8
                \startGroup
                ^ \markup { 14 }
                f'8
                \stopGroup
                s8
                b'8
                \startGroup
                ^ \markup { 15 }
                g'8
                \stopGroup
                \stopGroup
                s8
                cs'8
                \startGroup
                \startGroup
                ^ \markup { 16 }
                ef'8
                \stopGroup
                \stopGroup
                s8
                f'8
                \startGroup
                \startGroup
                ^ \markup { 17 }
                fs'8
                g'8
                ef'8
                \stopGroup
                \stopGroup
                s8
                bf'8
                \startGroup
                \startGroup
                ^ \markup { 18 }
                c'8
                af'8
                a'8
                \stopGroup
                \stopGroup
                s8
                ef'8
                \startGroup
                \startGroup
                ^ \markup { 19 }
                f'8
                fs'8
                g'8
                \stopGroup
                s8
                a'8
                \stopGroup
                \stopGroup
                \startGroup
                ^ \markup { 20 }
                s8
                bf'8
                \startGroup
                \startGroup
                ^ \markup { 21 }
                c'8
                \stopGroup
                s8
                af'8
                \stopGroup
                \startGroup
                ^ \markup { 22 }
                s8
                ef'8
                \startGroup
                ^ \markup { 23 }
                e'8
                f'8
                \stopGroup
                \stopGroup
                s8
                b'8
                \startGroup
                \startGroup
                ^ \markup { 24 }
                g'8
                cs'8
                \stopGroup
                \stopGroup
                s8
                af'8
                \startGroup
                \startGroup
                ^ \markup { 25 }
                a'8
                bf'8
                c'8
                \stopGroup
                \stopGroup
                s8
                cs'8
                \startGroup
                \startGroup
                ^ \markup { 26 }
                ef'8
                e'8
                f'8
                b'8
                \once \override Accidental.color = #red
                \once \override Beam.color = #red
                \once \override Dots.color = #red
                \once \override NoteHead.color = #red
                \once \override Stem.color = #red
                g'8
                \stopGroup
                \stopGroup
                s8
                \once \override Accidental.color = #red
                \once \override Beam.color = #red
                \once \override Dots.color = #red
                \once \override NoteHead.color = #red
                \once \override Stem.color = #red
                g'8
                \startGroup
                \startGroup
                ^ \markup { 27 }
                ef'8
                f'8
                fs'8
                \stopGroup
                s8
                g'8
                \startGroup
                ^ \markup { 28 }
                cs'8
                ef'8
                e'8
                f'8
                b'8
                \stopGroup
                \stopGroup
                s8
                fs'8
                \startGroup
                \startGroup
                ^ \markup { 29 }
                g'8
                \stopGroup
                s8
                ef'8
                \startGroup
                ^ \markup { 30 }
                f'8
                \stopGroup
                s8
                c'8
                \startGroup
                ^ \markup { 31 }
                af'8
                a'8
                bf'8
                \stopGroup
                \stopGroup
                s8
                f'8
                \startGroup
                \startGroup
                ^ \markup { 32 }
                fs'8
                g'8
                ef'8
                \stopGroup
                \stopGroup
                s8
                bf'8
                \stopGroup
                \stopGroup
                \startGroup
                \startGroup
                ^ \markup { 33 }
                s8
                c'8
                \startGroup
                \startGroup
                ^ \markup { 34 }
                af'8
                \stopGroup
                \stopGroup
                s8
                a'8
                \stopGroup
                \startGroup
                \startGroup
                ^ \markup { 35 }
                s8
                b'8
                \startGroup
                ^ \markup { 36 }
                g'8
                \stopGroup
                \stopGroup
                s8
                cs'8
                \startGroup
                \startGroup
                ^ \markup { 37 }
                ef'8
                \stopGroup
                s8
                e'8
                \startGroup
                ^ \markup { 38 }
                f'8
                \stopGroup
                s8
                a'8
                \startGroup
                ^ \markup { 39 }
                bf'8
                c'8
                af'8
                \stopGroup
                \stopGroup
                s8
                f'8
                \startGroup
                \startGroup
                ^ \markup { 40 }
                b'8
                g'8
                cs'8
                ef'8
                e'8
                \stopGroup
                \stopGroup
                s8
                ef'8
                \startGroup
                \startGroup
                ^ \markup { 41 }
                f'8
                fs'8
                g'8
                \stopGroup
                \stopGroup
                s8
                e'8
                \startGroup
                \startGroup
                ^ \markup { 42 }
                f'8
                b'8
                g'8
                cs'8
                ef'8
                \stopGroup
                \stopGroup
                s8
                g'8
                \stopGroup
                \startGroup
                \startGroup
                ^ \markup { 43 }
                s8
                ef'8
                \startGroup
                ^ \markup { 44 }
                f'8
                \stopGroup
                \stopGroup
                s8
                fs'8
                \stopGroup
                \startGroup
                \startGroup
                ^ \markup { 45 }
                s8
                af'8
                \stopGroup
                \startGroup
                ^ \markup { 46 }
                s8
                a'8
                \startGroup
                ^ \markup { 47 }
                bf'8
                \stopGroup
                \stopGroup
                s8
                c'8
                \stopGroup
                \stopGroup
                \startGroup
                \startGroup
                ^ \markup { 48 }
                s8
                fs'8
                \startGroup
                \startGroup
                ^ \markup { 49 }
                g'8
                ef'8
                f'8
                \stopGroup
                \stopGroup
                s8
                c'8
                \startGroup
                \startGroup
                ^ \markup { 50 }
                af'8
                a'8
                bf'8
                \stopGroup
                \stopGroup
                s8
                ef'8
                \startGroup
                \startGroup
                ^ \markup { 51 }
                e'8
                f'8
                b'8
                g'8
                cs'8
                \stopGroup
                s8
                bf'8
                \startGroup
                ^ \markup { 52 }
                c'8
                af'8
                a'8
                \stopGroup
                \stopGroup
                s8
                cs'8
                \startGroup
                \startGroup
                ^ \markup { 53 }
                ef'8
                e'8
                \stopGroup
                s8
                f'8
                \startGroup
                ^ \markup { 54 }
                b'8
                g'8
                \stopGroup
                s8
                f'8
                \startGroup
                ^ \markup { 55 }
                fs'8
                g'8
                ef'8
                \stopGroup
                \stopGroup
                s8
                \bar "|."                                                                %! SCORE1
                \override Score.BarLine.transparent = ##f
            }
        }
    >>
}