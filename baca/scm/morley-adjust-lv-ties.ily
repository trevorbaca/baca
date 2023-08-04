% Author: Thomas Morley
% Date: 2019-05-14

morley-adjust-lv-ties =
#(define-music-function (x-start amount)
   ((list? (circular-list #f)) number?)
   "
 Extends @code{LaissezVibrerTie}s by @var{amount}.
 Example:

  @verbatim
    {
     \\morley-adjust-lv-ties #2
     <fis' cis'' a''>2\\laissezVibrer
    }
  @end verbatim
 
 If @var{x-start} is specified, the start of a single @code{LaissezVibrerTie}
 may be tweaked. The numeric value of this element of @var{x-start} determines
 the amount of the offset.
 @code{LaissezVibrerTie}s which should not be tweaked are to be specified with
 @code{#f}
 Example:

  @verbatim
    {
     \\morley-adjust-lv-ties #'(#f 1 #f) #2
     <fis' cis'' a''>2\\laissezVibrer
    }
  @end verbatim
"
   #{
     \once
     \override LaissezVibrerTieColumn.before-line-breaking =
     #(lambda (grob)
        (let* ((ties (ly:grob-array->list (ly:grob-object grob 'ties)))
               (c-ps
                (map
                 (lambda (tie) (ly:grob-property tie 'control-points))
                 ties))
               (directions
                (map
                 (lambda (tie) (ly:grob-property tie 'direction))
                 ties))
               (first-cps
                (map
                 (lambda (c-p) (first c-p))
                 c-ps))
               (second-cps
                (map
                 (lambda (c-p) (second c-p))
                 c-ps))
               (third-cps
                (map
                 (lambda (c-p) (third c-p))
                 c-ps))
               (fourth-cps
                (map
                 (lambda (c-p) (fourth c-p))
                 c-ps))
               (new-first-cps
                (for-each
                 (lambda (first-cp x)
                   (if (number? x)
                       (set-car! first-cp (+ (car first-cp) x))))
                 first-cps x-start))
               ;; TODO:
               ;; Several hardcoded values following here.
               ;; Find better dependencies!!
               (new-second-cps
                (for-each
                 (lambda (second-cp x dir)
                   (let ((val (if (number? x) x 0.4)))
                     (set-car!
                      second-cp
                      (+ (car second-cp) (* val 1.2)))
                     (set-cdr!
                      second-cp
                      (+ (cdr second-cp) (min (* dir (/ amount 10)) 0.3)))))
                 second-cps x-start directions))
               (new-third-cps
                (for-each
                 (lambda (third-cp x dir)
                   (let ((val (if (number? x) 0.2 0.4)))
                     (set-car!
                      third-cp
                      (+ (car third-cp) (- amount val)))
                     (set-cdr!
                      third-cp
                      (+ (cdr third-cp) (min (* dir (/ amount 10)) 0.3)))))
                 third-cps x-start directions))
               (new-fourth-cps
                (for-each
                 (lambda (fourth-cp)
                   (set-car! fourth-cp (+ (car fourth-cp) amount)))
                 fourth-cps)))

          (for-each
           (lambda (tie first-cp second-cp third-cp fourth-cp)
             (ly:grob-set-property! tie 'control-points
               (list first-cp second-cp third-cp fourth-cp)))
           ties first-cps second-cps third-cps fourth-cps)))
   #})



%{

  EXAMPLE:

  {
    <fs' cs'' a''>2
    \laissezVibrer

    \morley-adjust-lv-ties #2
    <fs' cs'' a''>2
    \laissezVibrer

    \morley-adjust-lv-ties #'(#f 1 #f) #2
    <fs' cs'' a''>2
    \laissezVibrer

    <fs' cs'' a''>2
    \laissezVibrer

    \morley-adjust-lv-ties #'(#f #f #f) #2
    <fs' cs'' a''>2
    \laissezVibrer

    \morley-adjust-lv-ties #6
    <fs' cs'' a''>2
    \laissezVibrer

    \morley-adjust-lv-ties #'(#f 1.35 #f) #6
    <fs' cs'' a''>2
    \laissezVibrer

    \morley-adjust-lv-ties #'(#f 1.35 0.1) #6
    <fs' cs'' a''>2
    \laissezVibrer

  }

%}
