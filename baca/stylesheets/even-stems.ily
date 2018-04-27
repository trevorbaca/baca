\version "2.19.56"

%% Grob should be a NoteColumn object
#(define (space-by-stems grob)
   (let* ((stem (ly:grob-object grob 'stem))
          (beam (ly:grob-object stem 'beam)))
     (if (eq? #t (ly:grob-property beam 'cross-staff))
         (let* ((stems (ly:grob-array->list (ly:grob-object beam 'stems)))
                 (note-columns (map (lambda (s) (ly:grob-parent s X)) stems))
                 ;; which NoteColumn am I?
                 (me-nc (memq grob note-columns))
                 (nth (- (length note-columns) (length me-nc)))
                 (orig-stem-pos (map (lambda (s nc) (ly:grob-relative-coordinate s nc X))
                                  stems note-columns)))
           (* -1 (list-ref orig-stem-pos nth)))
         0.0)))

spaceStemsEvenly =
#(define-music-function (mus) (ly:music?)
   #{
     \temporary \override NoteColumn.X-offset = #space-by-stems
     #mus
     \revert NoteColumn.X-offset
   #})

%%%%%%%%%%%%%%%%%% EXAMPLE %%%%%%%%%%%%%%%%%

tsd = { \change Staff = treble \stemDown }
bsu = { \change Staff = bass \stemUp }

treble = {
  \clef treble
  aes''32[ \bsu cis'! \tsd disis'''! \bsu deses'! \tsd d''' \bsu ees'!]
}

bass = {
  \clef bass
  s8.
}

\score {

  \new PianoStaff
  <<
    \new Staff = "treble" { \treble \spaceStemsEvenly \treble \treble }
    \new Staff = "bass" { \bass \bass \bass }
  >>

  \layout {
    \context {
      \Score
      proportionalNotationDuration = #(ly:make-moment 1/32)
      \override SpacingSpanner.uniform-stretching = ##t
      \override Score.SpacingSpanner.strict-note-spacing = ##t
    }
  }
}
