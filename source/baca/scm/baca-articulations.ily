\version "2.25.26"
\include "baca-markups.ily"


#(define my-script-alist
  (cons*
  `(bacafulldownbow
    . (
      (stencil . ,ly:text-interface::print)
      (text . ,baca-full-downbow-markup)
      (avoid-slur . around)
      (direction . ,UP)
      (padding . 0.20)
      (script-priority . 150)
      (side-axis . ,Y)
      (skyline-horizontal-padding . 0.20)
      (toward-stem-shift . 0.5)
      ))
  `(bacastoponstringfulldownbow
    . (
      (stencil . ,ly:text-interface::print)
      (text . ,baca-stop-on-string-full-downbow-markup)
      (avoid-slur . around)
      (direction . ,UP)
      (padding . 0.20)
      (script-priority . 150)
      (side-axis . ,Y)
      (skyline-horizontal-padding . 0.20)
      (toward-stem-shift . 0.6)
      ))
  `(bacafullupbow
    . (
      (stencil . ,ly:text-interface::print)
      (text . ,baca-full-upbow-markup)
      (avoid-slur . around)
      (direction . ,UP)
      (padding . 0.20)
      (script-priority . 150)
      (side-axis . ,Y)
      (skyline-horizontal-padding . 0.20)
      (toward-stem-shift . 0.5)
      ))
  `(bacastoponstringfullupbow
    . (
      (stencil . ,ly:text-interface::print)
      (text . ,baca-stop-on-string-full-upbow-markup)
      (avoid-slur . around)
      (direction . ,UP)
      (padding . 0.20)
      (script-priority . 150)
      (side-axis . ,Y)
      (skyline-horizontal-padding . 0.20)
      (toward-stem-shift . 0.6)
      ))
  `(bacastoponstring
    . (
      (stencil . ,ly:text-interface::print)
      (text . ,baca-stop-on-string-markup)
      (avoid-slur . around)
      (padding . 0.20)
      (script-priority . 150)
      (side-axis . ,Y)
      (side-relative-direction . ,DOWN)
      (skyline-horizontal-padding . 0.20)
      (toward-stem-shift . 0.4)
      ))
  `(bacacirclebowing
    . (
      (stencil . ,ly:text-interface::print)
      (text . ,baca-circle-bowing-markup)
      (avoid-slur . around)
      (direction . ,UP)
      (padding . 0.50)
      (script-priority . 125)
      (side-axis . ,Y)
      (skyline-horizontal-padding . 0.20)
      (toward-stem-shift . -0.75)
      ))
  `(bacadamp
    . (
      (stencil . ,ly:text-interface::print)
      (text . ,baca-damp-markup)
      (avoid-slur . around)
      (padding . 0.20)
      (script-priority . 125)
      (side-axis . ,Y)
      (side-relative-direction . ,DOWN)
      (skyline-horizontal-padding . 0.20)
      ;;(toward-stem-shift . 0.5)
      ))
  `(bacadoublediamond
    . (
      (stencil . ,ly:text-interface::print)
      (text . ,baca-double-diamond-markup)
      (avoid-slur . around)
      (padding . 0.20)
      (script-priority . 125)
      (side-axis . ,Y)
      (side-relative-direction . ,DOWN)
      (skyline-horizontal-padding . 0.20)
      ;;(toward-stem-shift . 0.5)
      ))
  `(bacadoubleflageolet
    . (
      (stencil . ,ly:text-interface::print)
      (text . ,baca-double-flageolet-markup)
      (avoid-slur . around)
      (padding . 0.20)
      (script-priority . 125)
      (side-axis . ,Y)
      (side-relative-direction . ,DOWN)
      (skyline-horizontal-padding . 0.20)
      ;;(toward-stem-shift . 0.5)
      ))
  default-script-alist))

baca-full-downbow = #(make-articulation 'bacafulldownbow)
baca-stop-on-string-full-downbow = #(make-articulation 'bacastoponstringfulldownbow)
baca-full-upbow = #(make-articulation 'bacafullupbow)
baca-stop-on-string-full-upbow = #(make-articulation 'bacastoponstringfullupbow)
baca-stop-on-string = #(make-articulation 'bacastoponstring)
baca-circle-bowing = #(make-articulation 'bacacirclebowing)
baca-damp = #(make-articulation 'bacadamp)
baca-double-diamond = #(make-articulation 'bacadoublediamond)
baca-double-flageolet = #(make-articulation 'bacadoubleflageolet)

% STACCATO ARTICULATIONS (MULTIPLE)

baca-staccati = #(define-music-function (dots) (integer?)
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

% LEAVE FILE-FINAL

\layout
{
  \context
  {
    \Score
    scriptDefinitions = #my-script-alist
  }
}
