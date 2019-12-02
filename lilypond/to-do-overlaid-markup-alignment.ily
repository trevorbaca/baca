% Michael Käppler (list)
% 2019-10-05

\version "2.19.80"

#(define-markup-command (aligned-overlay layout props xdir ydir args)
    (number? number? markup-list?)
    (let* ((stencils (interpret-markup-list layout props args))
           (align (lambda (stencil)
                    (ly:stencil-aligned-to
                               (ly:stencil-aligned-to stencil X xdir)
                               Y ydir)))
           (stencils-aligned-merged (apply ly:stencil-add (map align
stencils))))
      (ly:stencil-aligned-to (ly:stencil-aligned-to
stencils-aligned-merged X LEFT)
        Y DOWN)))

boxone = \markup \with-color #yellow \filled-box #'(0 . 10) #'(0 . 10) #0
boxtwo = \markup \with-color #green \filled-box #'(3 . 9) #'(5 . 11) #0
boxthree = \markup \with-color #red \filled-box #'(2 . 5) #'(3 . 6) #0

\markup \column {
   "Without alignment"
   \overlay { \boxone \boxtwo \boxthree }
   \line {
       \column {
         "Everything centered "
         \aligned-overlay #CENTER #CENTER { \boxone \boxtwo \boxthree }
       }
       \column {
         "Everything aligned to bottom-left "
         \aligned-overlay #LEFT #DOWN { \boxone \boxtwo \boxthree }
       }
       \column {
         "Different alignments "
         \aligned-overlay #CENTER #UP {
           \boxone
           \aligned-overlay #LEFT #CENTER { \boxtwo \boxthree }
         }
       }
       \column {
         "Values in-between"
         \aligned-overlay #-0.8 #-0.5 {
           \boxone
           \aligned-overlay #0.5 #-0.2 { \boxtwo \boxthree }
         }
       }
   }
}
