% Urs Liska and David Nalesnik on LilyPond list (2019-03-14)
% Could possibly be modified to control repeat bar BarLine.X-extent 
% at line breaks
\include "/Users/trevorbaca/baca/lilypond/baca.ily"
\include "english.ly"
\version "2.19.83"


#(define color-system-start-bar
   (lambda (grob)
     (let*
      ((staff-elements
        (ly:grob-array->list
         (ly:grob-object (ly:grob-system grob) 'all-elements)))
       (ssb
        (filter
         (lambda (e)
           (eq? 'SystemStartBar (assq-ref (ly:grob-property e 'meta) 'name)))
         staff-elements)))
      (ly:grob-set-property! (car ssb) 'color red))))

annotateSystemStartBar =
#(define-music-function (comment)(string?)
  ; the string? argument is discarded and only used for the input file
   #{
     \once \override NoteHead.after-line-breaking = #color-system-start-bar
   #})

\score {
  \new PianoStaff <<
    \new Staff {
      c'1
      \break
      \annotateSystemStartBar "This is a comment that is now documented in the input"
      c'
    }
    \new Staff { c'1 c' }
  >>
}
