% Harm and I on the LilyPond list (2019-03-11)
\version "2.19.83"
\language "english"

\new Staff {
  \override DynamicLineSpanner.after-line-breaking =
    #(lambda (grob)
       (let* ((staffs
                (filter
                  (lambda (e) (grob::has-interface e 'staff-symbol-interface))
                  (ly:grob-array->list
                    (ly:grob-object (ly:grob-parent grob Y) 'elements)))))

         (for-each
           (lambda (staff) (set! (ly:grob-object grob 'staff-symbol) staff))
           staffs)

         ;(format #t"\nstaff-padding: ~a\nY-offset: ~a\nstaff-symbol ~a\n"
         ;  (ly:grob-property grob 'staff-padding)
         ;  (ly:grob-property grob 'Y-offset)
         ;  (ly:grob-object grob 'staff-symbol))
           ))

    \override DynamicLineSpanner.staff-padding = 10
    c'1\p\< c'1 c'1
    \break

    c'1 \stopStaff \startStaff c'1 c'1
    \break

    c'1 c'1 c'1
    \break

    c'1 c'1 c'1\f
}

\paper {
    indent = 0
    ragged-right = ##t
}
