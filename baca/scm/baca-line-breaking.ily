baca-broken-spanner-staff-padding = #(
    define-scheme-function (staff-padding-left staff-padding-right) (number? number?)
    (lambda (grob)
     (let* ((orig (ly:grob-original grob))
            (siblings (if (ly:grob? orig)
                       (ly:spanner-broken-into orig)
                       '())))
      (if (= (length siblings) 2)
       (begin
        (ly:grob-set-property! (car siblings) 'staff-padding staff-padding-left)
        (ly:grob-set-property! (car (cdr siblings)) 'staff-padding staff-padding-right)))
     ))
    )

%{

  EXAMPLE:

  \tweak after-line-breaking #(baca-broken-spanner-staff-padding 3 1.5)
  \times 8/10
  {
    a b c' d' e'
    \break
    f' g' a' b' c''
  }

%}
