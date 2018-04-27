% LilyPond list: Stefano Troncaro & Kieren MacMillan
\version "2.19.53"

\layout {
  \context {
    \Score
    \remove Mark_engraver
    \remove Staff_collecting_engraver
    \override RehearsalMark.self-alignment-X = #LEFT
    \override TextSpanner.to-barline = ##t
  }
  \context {
    \Dynamics
    \consists Mark_engraver
    \consists Staff_collecting_engraver
    \override RehearsalMark.padding = #2
    \override TextSpanner.padding = #2
  }
}

\score { <<
  \new Dynamics {
    \override TextSpanner.bound-details.left.text = \markup {
        \teeny { "align with" } }
    s1 \startTextSpan |
    s4 \stopTextSpan \mark "This" s2. |
  }
  \new Staff {
    \relative c' {
      c4 d e f |
      g a'' b, c |
    }
  }
>> }
