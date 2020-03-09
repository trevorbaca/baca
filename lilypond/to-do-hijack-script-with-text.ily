% From Harm on 2019-12-08
\include "english.ly"
\version "2.19.83"


{
    a'
      -\tweak font-name #"TeXGyreSchola"
      -\tweak stencil #ly:text-interface::print
      -\tweak text "foo"
      -!
    c''
      -\tweak font-name "TeXGyreSchola"
      -\tweak stencil #ly:text-interface::print
      -\tweak text "bar"
      -!
}
