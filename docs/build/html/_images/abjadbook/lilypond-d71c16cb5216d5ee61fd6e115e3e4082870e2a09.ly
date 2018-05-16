\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "default.ily"

#(set-global-staff-size 18)

\layout {
    indent = #0
    ragged-right = ##t
}

\paper {
    system-system-spacing = #'((basic-distance . 0) (minimum-distance . 0) (padding . 12) (stretchability . 0))
    top-margin = #24
}

\score {
    \new Score
    \with
    {
        \override BarLine.stencil = ##f
        \override BarNumber.transparent = ##t
        \override SpanBar.stencil = ##f
        \override TextScript.staff-padding = #10
        \override TimeSignature.stencil = ##f
        proportionalNotationDuration = #(ly:make-moment 1 30)
    }
    <<
        \new PianoStaff
        <<
            \context Staff = "Treble Staff"
            {
                \clef "treble"
                <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
                <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                <b c' d' bf' ef'' af'' a'' cs''' f''' g''' fs''''>4
                <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                <c' d' bf' b' ef'' a'' cs''' af''' f'''' fs'''' g''''>4
                <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                <b cs' e' d'' fs'' g'' af'' bf'' f''' a'''>4
                <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                <c' ef' f' b' cs'' e'' fs''' af''' a''''>4
                <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                <b c' f' g' ef'' fs'' af'' cs''' e''' a'''>4
                <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                <b d' g' bf' e'' f'' fs'' af'' a'' ef''' cs''''>4
                <e' af' b' f'' g'' ef''' fs''' a''' cs''''>4
            }
            \context Staff = "Bass Staff"
            {
                \clef "bass"
                <c d bf>4
                <c d bf>4
                <c d bf>4
                e4
                e4
                e4
                e4
                <c ef>4
                <c ef>4
                <d g bf>4
                <d g bf>4
                <d bf>4
                <d bf>4
                c4
                c4
                <c d bf>4
            }
        >>
    >>
}