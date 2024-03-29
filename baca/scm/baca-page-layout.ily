%%% BAR LINES %%%

baca-bar-line-visible = #(
    define-music-function (music) (ly:music?)
    #{
    \once \override Score.BarLine.transparent = ##f
    $music
    #}
    )

%%% BAR NUMBERS %%%

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

#(define (baca-oval-bar-numbers barnum measure-pos alt-number context)
 (make-oval-markup
  (robust-bar-number-function barnum measure-pos alt-number context)))

%%% BREAKS %%%

baca-lbsd = #(
    define-music-function (y-offset distances) (number? list?)
    #{
    \overrideProperty
    Score.NonMusicalPaperColumn.line-break-system-details.Y-offset #y-offset
    \overrideProperty
    Score.NonMusicalPaperColumn.line-break-system-details.alignment-distances #distances
    #}
    )

%%% FERMATA MEASURES %%%

baca-fermata-measure = #(
    define-music-function (music) (ly:music?)
    #{
    \once \override Score.MultiMeasureRest.transparent = ##t
    \once \override Score.TimeSignature.stencil = ##f
    $music
    #}
    )

%%% SPACING SECTIONS %%%

baca-new-spacing-section = #(
    define-music-function (n d music) (number? number? ly:music?)
    #{
    \set Score.proportionalNotationDuration = #(ly:make-moment n d)
    \newSpacingSection
    $music
    #}
    )
