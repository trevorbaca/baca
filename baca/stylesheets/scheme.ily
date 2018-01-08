%%% BAČA SCHEME DEFINITIONS %%%

%%% OVAL BAR NUMBERS %%%

#(define-markup-command (oval layout props arg)
 (markup?)
 #:properties ((thickness 1)
               (font-size 0)
               (oval-padding 0.5))
 (let ((th (* (ly:output-def-lookup layout 'line-thickness)
              thickness))
       (pad (* (magstep font-size) oval-padding))
       (m (interpret-markup layout props (markup #:hcenter-in 4.0 arg))))
   (oval-stencil m th pad (* pad 8.0))))

#(define (format-oval-barnumbers barnum measure-pos alt-number context)
 (make-oval-markup
  (robust-bar-number-function barnum measure-pos alt-number context)))

%%% SLAP TONGUE %%%

slap =
#(define-music-function (parser location music) (ly:music?)
#{
  \override NoteHead #'stencil = #(lambda (grob)
    (grob-interpret-markup grob
      (markup #:musicglyph "scripts.sforzato")))
  \override NoteHead #'extra-offset = #'(0.1 . 0.0)
  $music
  \revert NoteHead #'stencil
  \revert NoteHead #'extra-offset
#})

%%% TONGUE COMMAND FOR DOUBLE- AND TRIPLE-TONGUING WITH STACCATI %%%

tongue =
#(define-music-function (parser location dots) (integer?)
   (let ((script (make-music 'ArticulationEvent
                             'articulation-type "staccato")))
     (set! (ly:music-property script 'tweaks)
           (acons 'stencil
                  (lambda (grob)
                    (let ((stil (ly:script-interface::print grob)))
                      (let loop ((count (1- dots)) (new-stil stil))
                        (if (> count 0)
                            (loop (1- count)
                                  (ly:stencil-combine-at-edge new-stil X RIGHT stil 0.2))
                            (ly:stencil-aligned-to new-stil X CENTER)))))
                  (ly:music-property script 'tweaks)))
     script))

%%% DYNAMICS %%%

sff = #(make-dynamic-script "sff")
sffp = #(make-dynamic-script "sffp")
sffpp = #(make-dynamic-script "sffpp")
sfpp = #(make-dynamic-script "sfpp")

sffz = #(make-dynamic-script "sffz")
sfffz = #(make-dynamic-script "sfffz")

ffp = #(make-dynamic-script "ffp")
fffp = #(make-dynamic-script "fffp")
mf_sub = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "mf"
            #:hspace -0.25
            #:normal-text #:italic "sub."
            )
        )
    )

%%% SHAPE NOTE HEADS %%%

blackDiamondNoteHead = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \once \override NoteHead.style = #'harmonic-black
    $music
    #}
    )

diamondNoteHead = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \once \override NoteHead.style = #'harmonic
    $music
    #}
    )

semicircleNoteHead = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \once \set shapeNoteStyles = ##(re re re re re re re)
    $music
    #}
    )

squareNoteHead = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \once \set shapeNoteStyles = ##(la la la la la la la)
    $music
    #}
    )

triangleNoteHead = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \once \set shapeNoteStyles = ##(do do do do do do do)
    $music
    #}
    )
