\include "text-spanner-id.ily"


%%%%%%%%%%%%%%%%%%%%%%%%%%%%% EXAMPLE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\layout {
  \context {
    \Voice
    \remove #"Text_spanner_engraver"
    \consists \alternateTextSpannerEngraver
  }
}

\relative c' {
  \override TextSpanner.style = ##f
  \override TextSpanner.thickness = 10
  %\override TextSpanner.to-barline = ##t
  %\override TextSpanner.outside-staff-priority = ##f
  \override TextSpanner.outside-staff-padding = 1.5
  a4
  -\tweak color #red
  \startTextSpan
  b
  -\tweak color #green
  \startTextSpanOne
  c
  -\tweak color #blue
  \startTextSpanTwo
  d
  \startTextSpanThree

  a4\stopTextSpan
  b
  \stopTextSpanOne
  -\tweak color #red
  \startTextSpan
  c
  \stopTextSpanTwo
  -\tweak color #green
  \startTextSpanOne
  d
  \stopTextSpanThree
  -\tweak color #blue
  \startTextSpanTwo

  a4
  \startTextSpanThree
  b c d
  \break

  a4 b c d

  a1\stopTextSpan\stopTextSpanOne\stopTextSpanTwo\stopTextSpanThree
}
