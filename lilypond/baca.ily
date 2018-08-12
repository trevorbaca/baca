\include "/Users/trevorbaca/abjad/docs/source/_stylesheets/abjad.ily"
#(ly:set-option 'relative-includes #t)
\include "baca-articulations.ily"
\include "baca-coloring.ily"
\include "baca-dynamics.ily"
\include "baca-markups.ily"

%%% BAR LINES %%%

baca-bar-line-visible = #(define-music-function
    (parser location music) (ly:music?)
    #{
    \once \override Score.BarLine.transparent = ##f
    $music
    #}
    )

%%% BAR NUMBERS: OVAL %%%

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

baca-lbsd = #(define-music-function
    (parser location y-offset distances)
    (number? list?)
    #{
    \overrideProperty
    Score.NonMusicalPaperColumn.
    line-break-system-details.Y-offset
    #y-offset
    \overrideProperty
    Score.NonMusicalPaperColumn.
    line-break-system-details.alignment-distances
    #distances
    #}
    )

%%% NOTE-HEADS: SHAPED %%%

baca-black-diamond-note-head = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \once \override NoteHead.style = #'harmonic-black
    $music
    #}
    )

baca-diamond-note-head = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \once \override NoteHead.style = #'harmonic
    $music
    #}
    )

baca-semicircle-note-head = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \once \set shapeNoteStyles = ##(re re re re re re re)
    $music
    #}
    )

baca-square-note-head = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \once \set shapeNoteStyles = ##(la la la la la la la)
    $music
    #}
    )

baca-triangle-note-head = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \once \set shapeNoteStyles = ##(do do do do do do do)
    $music
    #}
    )

%%% NOTE-HEAD: SLAP-TONGUE %%%

baca-slap-tongue-note-head =
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

%%% TEXT SPANNERS: COMMANDS %%%

bacaStartTextSpanBCP =
#(make-music 'TextSpanEvent 'span-direction START 'spanner-id "BCP")

bacaStopTextSpanBCP =
#(make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "BCP")

%%% METRONOME MARK SPANNERS %%%

baca-metronome-mark-spanner-colored-left-text = #(
    define-music-function
    (parser location log dots stem string color music)
    (number? number? number? string? symbol? ly:music?)
    #{
    \tweak bound-details.left.text \markup \concat {
        \with-color #(x11-color color)
        \abjad-metronome-mark-markup #log #dots #stem #string
        \hspace #0.5
        }
    $music
    #})

baca-metronome-mark-spanner-left-text = #(
    define-music-function
    (parser location log dots stem string music)
    (number? number? number? string? ly:music?)
    #{
    \tweak bound-details.left.text \markup \concat {
        \abjad-metronome-mark-markup #log #dots #stem #string
        \hspace #0.5
        }
    $music
    #})

%%% TEXT SPANNERS: EMBEDDED MARKUP %%%

#(define-markup-command
    (baca-bcp-left layout props n d) (number? number?)
    (interpret-markup layout props
    #{
    \markup \concat {
        \upright \fraction #(number->string n) #(number->string d)
        \hspace #0.5
        }
    #})
    )

baca-bcp-spanner-left-text = #(
    define-music-function
    (parser location n d music) (number? number? ly:music?)
    #{
    \tweak bound-details.left.text \markup \baca-bcp-left #n #d
    $music
    #})

#(define-markup-command
    (baca-bcp-right layout props n d) (number? number?)
    (interpret-markup layout props
    #{
    \markup \upright \fraction #(number->string n) #(number->string d)
    #})
    )

baca-bcp-spanner-right-text = #(
    define-music-function
    (parser location n d music) (number? number? ly:music?)
    #{
    \tweak bound-details.right.text \markup \baca-bcp-right #n #d
    $music
    #})

baca-text-spanner-left-markup = #(
    define-music-function (parser location markup music) (markup? ly:music?)
    #{
    \tweak bound-details.left.text \markup \concat {
        \upright #markup \hspace #0.5
        }
    $music
    #})

baca-text-spanner-left-text = #(
    define-music-function (parser location string music) (string? ly:music?)
    #{
    \tweak bound-details.left.text \markup \concat {
        \upright #string \hspace #0.5
        }
    $music
    #})

baca-text-spanner-right-markup = #(
    define-music-function (parser location markup music) (markup? ly:music?)
    #{
    \tweak bound-details.right.text \markup \upright #markup
    $music
    #})

baca-text-spanner-right-text = #(
    define-music-function (parser location string music) (string? ly:music?)
    #{
    \tweak bound-details.right.text \markup \upright #string
    $music
    #})

%%% SPACING COMMANDS %%%

baca-new-spacing-section = #(define-music-function
    (parser location n d music) (number? number? ly:music?)
    #{
    \set Score.proportionalNotationDuration = #(ly:make-moment n d)
    \newSpacingSection
    $music
    #}
    )
