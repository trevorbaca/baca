% Aaron Hill, 2020-02-22

\version "2.19.82"

whenSharedBeam = #(lambda (grob)
   (define (beam-from-notehead nh)
     (let* ((nc (ly:grob-parent nh X))
            (stem (ly:grob-object nc 'stem)))
       (if (ly:grob? stem) (ly:grob-object stem 'beam) '())))
   (let* ((lb (beam-from-notehead (ly:spanner-bound grob LEFT)))
          (rb (beam-from-notehead (ly:spanner-bound grob RIGHT))))
     (and (ly:grob? lb) (ly:grob? rb) (eq? lb rb))))

\layout {
   \context {
     \Voice
     \override VoiceFollower.transparent = \whenSharedBeam
   }
}

\autochange {
   \showStaffSwitch
   c2 g'4 f8. f'16 b'8 a fis2.
}

% The principle is to check whether the NoteHeads being connected by the
% VoiceFollower have a shared Beam.
