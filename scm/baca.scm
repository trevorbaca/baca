#(define (funky-time-signature-engraver ctx)
  (let ((time-signature '())
        (last-fraction #f))
    `((process-music
       . ,(lambda (trans)
            (let ((frac (ly:context-property ctx 'timeSignatureFraction)))
              (if (and (null? time-signature)
                       (not (equal? last-fraction frac))
                       (pair? frac))
                  (begin
                    (set! time-signature
                          (ly:engraver-make-grob trans 'TimeSignature '()))
                    (set! (ly:grob-property time-signature 'fraction) frac)

                    (and (not last-fraction)
                         (set! (ly:grob-property time-signature
'break-visibility)
                               (ly:context-property ctx
'implicitTimeSignatureVisibility)))

                    (set! last-fraction frac))))))

      (stop-translation-timestep
       . ,(lambda (trans)
            (set! time-signature '()))))))
