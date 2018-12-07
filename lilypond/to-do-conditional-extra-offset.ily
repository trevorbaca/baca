% Peter Crighton on the LilyPond user list:

\once \override Glissando.Y-offset =
    #(lambda (grob) (and
        (if (= 0 (ly:grob-property grob 'glissando-index)) '0.25)
      (if (= 1 (ly:grob-property grob 'glissando-index)) '-0.25)))
<g c>2\glissando <a d>
