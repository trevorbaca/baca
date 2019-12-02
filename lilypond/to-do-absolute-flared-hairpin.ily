% Aaron Hill (list)
% 2019-11-17
% Note: must not include baca.ily (for elbowed-hairpin definition)

\version "2.19.83"

abs-hairpin = #(define-scheme-function (elx ely) (number? number?)
   (lambda (grob)
     (let* ((sten (ly:hairpin::print grob))
            (xex (ly:stencil-extent sten X))
            (yex (ly:stencil-extent sten Y))
            (width (interval-length xex))
            (height (/ (interval-length yex) 2))
            (x (- 1 (/ elx width)))
            (y (- 1 (/ ely height))))
       (elbowed-hairpin `((0 . 0) (,x . ,y) (1 . 1)) #t))))

{
   \override Hairpin.height = 2
   \override Hairpin.stencil = \abs-hairpin 1.5 1
   c''4^\> \repeat unfold 2 { c'' } c''\!
   c''4^\< \repeat unfold 4 { c'' } c''\!
   c''4^\> \repeat unfold 6 { c'' } c''\!
   c''4^\< \repeat unfold 8 { c'' } c''\!
}
