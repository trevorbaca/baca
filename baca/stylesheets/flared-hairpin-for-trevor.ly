\version "2.19"

#(define ((elbowed-hairpin-modified-for-trevor coords x-op mirrored?) grob)
  ; note the extra x-op argument
  (define (pair-to-list pair)
    (list (car pair) (cdr pair)))
  (define (normalize-coords goods x y)
    (map
     (lambda (coord)
       ;x-op used here
       (cons (x-op x (car coord)) (* y (cdr coord))))
     goods))
  (define (my-c-p-s points thick decresc?)
    (make-connected-path-stencil
     points
     thick
     (if decresc? -1.0 1.0)
     1.0
     #f
     #f))
  ;; outer let to trigger suicide
  (let ((sten (ly:hairpin::print grob)))
    (if (grob::is-live? grob)
        (let* ((decresc? (eq? (ly:grob-property grob 'grow-direction) LEFT))
               (thick (ly:grob-property grob 'thickness 0.1))
               (thick (* thick (layout-line-thickness grob)))
               (xex (ly:stencil-extent sten X))
               (lenx (interval-length xex))
               (yex (ly:stencil-extent sten Y))
               (leny (interval-length yex))
               (xtrans (+ (car xex) (if decresc? lenx 0)))
               (ytrans (car yex))
               (uplist (map pair-to-list
                            (normalize-coords coords lenx (/ leny 2))))
               (downlist (map pair-to-list
                              (normalize-coords coords lenx (/ leny -2)))))
          (ly:stencil-translate
           (ly:stencil-add
            (my-c-p-s uplist thick decresc?)
            (if mirrored? (my-c-p-s downlist thick decresc?) empty-stencil))
           (cons xtrans ytrans)))
        '())))

#(define flared-hairpin-old
  (elbowed-hairpin-modified-for-trevor '((0.95 . 0.4) (1.0 . 1.0)) * #t))

#(define flared-hairpin-new
  (elbowed-hairpin-modified-for-trevor '((1.0 . 0.4) (0.5 . 1.0)) - #t))


\relative c' {
  \override Score.Hairpin.stencil = #flared-hairpin-old
  a\< b c d |
  e\f a a a |
  a\< b c d |
  a b c d |
  a b c d |
  a b c d |
  e\f a a a | \break
  \override Score.Hairpin.stencil = #flared-hairpin-new
  a\< b c d |
  e\f a a a |
  a\< b c d |
  a b c d |
  a b c d |
  a b c d |
  e\f a a a |
}