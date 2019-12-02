% Aaron Hill (list)
% 2019-11-17

\version "2.19.83"

#(define-markup-command (note-names layout props note-name accidental)
    (markup? markup?)
    "Provide note name for clarity."
    (interpret-markup layout props
      #{
        \markup {
          \override #'(font-name . "Latin Modern Sans Demi Cond")
          \concat
          {
            \fontsize #-1 \vcenter #note-name \hspace #.2
            \fontsize #-4 #accidental
          }
        }
      #}))


#(define-markup-command (note-names-multiple layout props args)
   (markup-list?)
   "Provide multiple note names for clarity."
   (define (paired lst) (if (null? lst) '()
       (cons (cons (first lst) (second lst))
             (paired (cddr lst)))))
   (interpret-markup layout props
     #{ \markup \concat { \vcenter [
           \override #'(word-space . 1)
           \line { $@(map (lambda (x) #{
           \markup \note-names $(car x) $(cdr x)
         #}) (paired args)) } \vcenter ] } #} ))


{
   <c' e' gis'>
     ^\markup \note-names-multiple { "C" \natural "E" \natural "G" \sharp }
}
