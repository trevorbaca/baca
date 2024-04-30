% Author: David Nalesnik
% Date: 2015-04-17
% https://lists.gnu.org/archive/html/lilypond-user/2015-04/msg00513.html
% https://github.com/openlilylib/snippets/blob/master/notation-snippets/...
% shaping-bezier-curves/shape-tie-column/README.md

shapeRepeatTieColumn =
#(define-music-function (parser location all-offsets) (list?)
   #{
     \override RepeatTieColumn.before-line-breaking =
     #(lambda (grob)
        (let ((ties (ly:grob-array->list (ly:grob-object grob 'ties))))
          (for-each
           (lambda (tie offsets-for-tie)
             (if (number-pair-list? offsets-for-tie)
                 (set! (ly:grob-property tie 'control-points)
                       (map
                        (lambda (x y) (coord-translate x y))
                        (ly:semi-tie::calc-control-points tie) offsets-for-tie))))
           ties all-offsets)))
   #})

%{

  \new Staff \with {
    \shapeRepeatTieColumn #'(
                              ((-2 . 0) (-1 . 0) (-0.5 . 0) (0 . 0))
                              ((-2 . 0) (-1 . 0) (-0.5 . 0) (0 . 0))
                              )                
    \override RepeatTie.X-extent = ##f
  } {
    <c' g'>1
    <c' g'>1 \repeatTie
    <c' g'>1 \repeatTie
    <c' g'>1 \repeatTie
  }

%}
