% Andrew Bernard (list)
% 2019-04-10


#(define make-outline-counter
  (lambda ()
    (let ((lst (list 0))
      (indent-level 0))
      (define counter
    (lambda (method)
      (define (inc)
        (list-set! lst indent-level (+ (list-ref lst indent-level) 1))
        (output-list-item-number))

      (define (indent)
        (set! lst (append lst (list 1)))
        (display lst) (newline)
        (set! indent-level (+ indent-level 1))
        (output-list-item-number))

      (define (unindent)
        (if (> indent-level 0)
        (begin
          (set! indent-level (- indent-level 1))
          (set! lst (drop-right lst 1))
          (inc)
          (output-list-item-number)
          )))
     
      (define (reset)
        (set! lst (drop-right lst (- (length lst) 1)))
        (list-set! lst 0 1)
        (set! indent-level 0)
        (output-list-item-number))

      (define (output-list-item-number)
          (let loop ((l lst) (str ""))
        (if (null? l)
            str
            (begin
              (loop (cdr l)
                (string-append str (format #f "~a." (car l)))
                )))))

      (cond ((eq? method 'inc) inc)
        ((eq? method 'indent) indent)
        ((eq? method 'unindent) unindent)
        ((eq? method 'reset) reset))
      ))
      counter)))
     
% create counter
#(define a (make-outline-counter))

\markup { #((a 'inc)) }
{ c''4 }
\markup { #((a 'inc)) }
{ c''4 }
\markup { #((a 'inc)) }
{ c''4 }
\markup { #((a 'indent)) }
{ c''4 }
\markup { #((a 'inc)) }
{ c''4 }
\markup { #((a 'unindent)) }
{ c''4 }
\markup { #((a 'inc)) }
{ c''4 }
\markup { #((a 'indent)) }
{ c''4 }
\markup { #((a 'reset)) }
{ c''4 }
