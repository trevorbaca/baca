% 2018-07-24: example appears to do nothing;
%             test when writing final LilyPond object position docs.
\version "2.19.56"

#(define (at-line-beginning? grob)
   (let ((col (ly:item-get-column grob)))
     (and (eq? #t (ly:grob-property col 'non-musical))
          (= 1 (ly:item-break-dir col)))))

{
  \override Score.RehearsalMark.self-alignment-X =
  #(lambda (grob)
     (let ((beginning? (at-line-beginning? grob)))
       (if beginning? -1 0)))
  \mark \default
  R1
  \mark \default
  R1
  \break
  \mark \default
  R1
}
