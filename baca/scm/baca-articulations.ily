\include "baca-markups.ily"

%%% BOWSTROKE ARTICULATIONS %%%

#(append! default-script-alist
   (list
    `(bacafulldownbow
       . (
           (stencil . ,ly:text-interface::print)
           (text . ,baca-full-downbow-markup)
           (avoid-slur . around)
           (direction . ,UP)
           (padding . 0.20)
           (script-priority . 150)
           (skyline-horizontal-padding . 0.20)
           (toward-stem-shift . 0.5)
           ))))

baca-full-downbow = #(make-articulation 'bacafulldownbow)

#(append! default-script-alist
   (list
    `(bacastoponstringfulldownbow
       . (
           (stencil . ,ly:text-interface::print)
           (text . ,baca-stop-on-string-full-downbow-markup)
           (avoid-slur . around)
           (direction . ,UP)
           (padding . 0.20)
           (script-priority . 150)
           (skyline-horizontal-padding . 0.20)
           (toward-stem-shift . 0.6)
           ))))

baca-stop-on-string-full-downbow = #(
    make-articulation 'bacastoponstringfulldownbow)

#(append! default-script-alist
   (list
    `(bacafullupbow
       . (
           (stencil . ,ly:text-interface::print)
           (text . ,baca-full-upbow-markup)
           (avoid-slur . around)
           (direction . ,UP)
           (padding . 0.20)
           (script-priority . 150)
           (skyline-horizontal-padding . 0.20)
           (toward-stem-shift . 0.5)
           ))))

baca-full-upbow = #(make-articulation 'bacafullupbow)

#(append! default-script-alist
   (list
    `(bacastoponstringfullupbow
       . (
           (stencil . ,ly:text-interface::print)
           (text . ,baca-stop-on-string-full-upbow-markup)
           (avoid-slur . around)
           (direction . ,UP)
           (padding . 0.20)
           (script-priority . 150)
           (skyline-horizontal-padding . 0.20)
           (toward-stem-shift . 0.6)
           ))))

baca-stop-on-string-full-upbow = #(
    make-articulation 'bacastoponstringfullupbow)

#(append! default-script-alist
   (list
    `(bacastoponstring
       . (
           (stencil . ,ly:text-interface::print)
           (text . ,baca-stop-on-string-markup)
           (avoid-slur . around)
           (padding . 0.20)
           (script-priority . 150)
           (side-relative-direction . ,DOWN)
           (skyline-horizontal-padding . 0.20)
           (toward-stem-shift . 0.4)
           ))))

baca-stop-on-string = #(make-articulation 'bacastoponstring)

%%% CIRCLE BOWING ARTICULATIONS %%%

#(append! default-script-alist
   (list
    `(bacacirclebowing
       . (
           (stencil . ,ly:text-interface::print)
           (text . ,baca-circle-bowing-markup)
           (avoid-slur . around)
           (direction . ,UP)
           (padding . 0.50)
           (script-priority . 125)
           (skyline-horizontal-padding . 0.20)
           (toward-stem-shift . -0.75)
           ))))

baca-circle-bowing = #(make-articulation 'bacacirclebowing)

%%% DAMP ARTICULATIONS %%%

#(append! default-script-alist
   (list
    `(bacadamp
       . (
           (stencil . ,ly:text-interface::print)
           (text . ,baca-damp-markup)
           (avoid-slur . around)
           (padding . 0.20)
           (script-priority . 125)
           (side-relative-direction . ,DOWN)
           (skyline-horizontal-padding . 0.20)
           ;;(toward-stem-shift . 0.5)
           ))))

baca-damp = #(make-articulation 'bacadamp)

%%% DIAMOND ARTICULATIONS %%%

#(append! default-script-alist
   (list
    `(bacadoublediamond
       . (
           (stencil . ,ly:text-interface::print)
           (text . ,baca-double-diamond-markup)
           (avoid-slur . around)
           (padding . 0.20)
           (script-priority . 125)
           (side-relative-direction . ,DOWN)
           (skyline-horizontal-padding . 0.20)
           ;;(toward-stem-shift . 0.5)
           ))))

baca-double-diamond = #(make-articulation 'bacadoublediamond)

%%% DOUBLE FLAGEOLET ARTICULATION %%%

#(append! default-script-alist
   (list
    `(bacadoubleflageolet
       . (
           (stencil . ,ly:text-interface::print)
           (text . ,baca-double-flageolet-markup)
           (avoid-slur . around)
           (padding . 0.20)
           (script-priority . 125)
           (side-relative-direction . ,DOWN)
           (skyline-horizontal-padding . 0.20)
           ;;(toward-stem-shift . 0.5)
           ))))

baca-double-flageolet = #(make-articulation 'bacadoubleflageolet)

%%% STACCATO ARTICULATIONS (MULTIPLE) %%%

baca-staccati =
#(define-music-function (parser location dots) (integer?)
   (let ((script (make-music 'ArticulationEvent
                             'articulation-type 'staccato)))
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

%%% LEAVE FILE-FINAL: %%%

\layout {
    \context {
        \Score
        scriptDefinitions = #default-script-alist
    }
}
