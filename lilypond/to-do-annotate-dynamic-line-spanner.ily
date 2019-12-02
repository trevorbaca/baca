% Aaron Hill (LilyPond list)
% 2019-03-25

\include "english.ly"
\version "2.19.83"

\paper
{
    indent = 0
    line-width = 5\in
    ragged-right = ##f
}
\layout
{
    \omit Staff.TimeSignature
}

test = {
  %% Overlay reference lines.
   \override Hairpin.stencil =
     #(grob-transformer 'stencil (lambda (grob orig)
       (let* ((p (ly:grob-object grob 'axis-group-parent-Y))
              (y (ly:grob-property p 'minimum-space)))
         (grob-interpret-markup grob #{
           \markup \with-dimensions-from \stencil $orig \overlay {
             \with-color #(rgb-color 0.4 0.7 1.0)
             \path #0.2 #'((moveto -8 0) (lineto 8 0))
             \with-color #(rgb-color 1.0 0.4 0.7)
             \path #0.2 #`((moveto 0 0) (lineto 0 ,y)
               (moveto -2 ,y) (lineto 2 ,y)
               (moveto -1 ,(- y 1.5)) (lineto 0 ,y)
               (lineto 1 ,(- y 1.5)))
             \stencil $orig } #}))))
   | g4\p\< g'2.\!
   | g4\p g4\< g'2\!
   | g4\p g'4\< g'2\!
   | g'2.\< g4\!\f
   | g'2\< g4\! g4\f
   | g'2\< g'4\! g4\f \break
}

{
   \test
   \override DynamicLineSpanner.staff-padding = 8
   \test
   \override DynamicLineSpanner.minimum-space = 8
   \override DynamicLineSpanner.padding = 0
   \override DynamicLineSpanner.staff-padding = 8
   \test
}
