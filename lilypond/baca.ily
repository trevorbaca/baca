\include "/Users/trevorbaca/abjad/docs/source/_stylesheets/abjad.ily"
\include "/Users/trevorbaca/abjad/docs/source/_stylesheets/flared-hairpin.ily"
#(ly:set-option 'relative-includes #t)
\include "baca-coloring.ily"
\include "baca-dynamics.ily"
\include "flared-hairpin-for-trevor.ily"
\include "text-spanner-id.ily"

%%% BOWSTROKES: MARKUP & ARTICULATIONS %%%

baca_full_downbow_markup = \markup {
    \combine
        \musicglyph #"scripts.downbow"
        \path #0.15 
        #'(
            (moveto 0.7375 0.05)
            (rlineto 1 0)
            (closepath)
            )
    }

baca_full_upbow_markup = \markup {
    \combine
        \musicglyph #"scripts.upbow"
        \path #0.15 
        #'(
            (moveto 0.62 2.005)
            (rlineto 1 0)
            (closepath)
            )
    }

baca_stop_on_string_markup = \markup {
    \path #0.15 
    #'(
        (moveto 0 0)
        (rlineto 1 0)
        (closepath)
        (rmoveto 1 0.3)
        (rlineto 0 -0.6)
        (closepath)
        )
    }

baca_stop_on_string_full_downbow_markup = \markup {
    \combine
        \musicglyph #"scripts.downbow"
        \path #0.15 
        #'(
            (moveto 0.7375 0.05)
            (rlineto 1 0)
            (closepath)
            (rmoveto 1 0.3)
            (rlineto 0 -0.6)
            (closepath)
            )
    }

baca_stop_on_string_full_upbow_markup = \markup {
    \combine
        \musicglyph #"scripts.upbow"
        \path #0.15 
        #'(
            (moveto 0.62 2.005)
            (rlineto 1 0)
            (closepath)
            (rmoveto 1 0.3)
            (rlineto 0 -0.6)
            (closepath)
            )
    }

#(append! default-script-alist
   (list
    `("bacafulldownbow"
       . (
           (stencil . ,ly:text-interface::print)
           (text . ,baca_full_downbow_markup)
           (avoid-slur . around)
           (direction . ,UP)
           (padding . 0.20)
           (script-priority . 150)
           (skyline-horizontal-padding . 0.20)
           (toward-stem-shift . 0.5)
           ))))

baca_full_downbow = #(make-articulation "bacafulldownbow")

#(append! default-script-alist
   (list
    `("bacastoponstringfulldownbow"
       . (
           (stencil . ,ly:text-interface::print)
           (text . ,baca_stop_on_string_full_downbow_markup)
           (avoid-slur . around)
           (direction . ,UP)
           (padding . 0.20)
           (script-priority . 150)
           (skyline-horizontal-padding . 0.20)
           (toward-stem-shift . 0.6)
           ))))

baca_stop_on_string_full_downbow = #(
    make-articulation "bacastoponstringfulldownbow")

#(append! default-script-alist
   (list
    `("bacafullupbow"
       . (
           (stencil . ,ly:text-interface::print)
           (text . ,baca_full_upbow_markup)
           (avoid-slur . around)
           (direction . ,UP)
           (padding . 0.20)
           (script-priority . 150)
           (skyline-horizontal-padding . 0.20)
           (toward-stem-shift . 0.5)
           ))))

baca_full_upbow = #(make-articulation "bacafullupbow")

#(append! default-script-alist
   (list
    `("bacastoponstringfullupbow"
       . (
           (stencil . ,ly:text-interface::print)
           (text . ,baca_stop_on_string_full_upbow_markup)
           (avoid-slur . around)
           (direction . ,UP)
           (padding . 0.20)
           (script-priority . 150)
           (skyline-horizontal-padding . 0.20)
           (toward-stem-shift . 0.6)
           ))))

baca_stop_on_string_full_upbow = #(
    make-articulation "bacastoponstringfullupbow")

#(append! default-script-alist
   (list
    `("bacastoponstring"
       . (
           (stencil . ,ly:text-interface::print)
           (text . ,baca_stop_on_string_markup)
           (avoid-slur . around)
           (direction . ,UP)
           (padding . 0.20)
           (script-priority . 150)
           (skyline-horizontal-padding . 0.20)
           (toward-stem-shift . 0.4)
           ))))

baca_stop_on_string = #(make-articulation "bacastoponstring")

\layout {
    \context {
        \Score
        scriptDefinitions = #default-script-alist
    }
}

%%% ARTICULATIONS: MULTIPLE STACCATI %%%

baca_staccati =
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

%%% BAR LINES %%%

baca_bar_line_visible = #(define-music-function
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

baca_lbsd = #(define-music-function
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

%%% DAMP %%%

baca_damp_markup = \markup {
    \scale #'(0.75 . 0.75)
    \combine
    \bold \override #'(font-name . "Times") "O"
    \path #0.15
    #'(
        (moveto -.4 .7)
        (rlineto 2.4 0)
        (closepath)
        (moveto .8 -.5)
        (rlineto 0 2.4)
        )
    }

#(append! default-script-alist
   (list
    `("bacadamp"
       . (
           (stencil . ,ly:text-interface::print)
           (text . ,baca_damp_markup)
           (avoid-slur . around)
           (direction . ,UP)
           (padding . 0.20)
           (script-priority . 125)
           (skyline-horizontal-padding . 0.20)
           ;;(toward-stem-shift . 0.5)
           ))))

baca_damp = #(make-articulation "bacadamp")

%%% DIAMOND MARKUP %%%

baca_black_diamond_markup = \markup
{
    \scale #'(0.75 . 0.75)
    \musicglyph #"noteheads.s2harmonic"
}

baca_diamond_markup = \markup
{
    \scale #'(0.75 . 0.75)
    \musicglyph #"noteheads.s0harmonic"
}

baca_double_black_diamond_markup = \markup
{
    \override #'(baseline-skip . 1.75)
    \scale #'(0.75 . 0.75)
    \column
    {
        \musicglyph #"noteheads.s2harmonic"
        \musicglyph #"noteheads.s2harmonic"
    }
}

baca_double_diamond_markup = \markup
{
    \override #'(baseline-skip . 1.75)
    \scale #'(0.75 . 0.75)
    \column
    {
        \musicglyph #"noteheads.s0harmonic"
        \musicglyph #"noteheads.s0harmonic"
    }
}

baca_triple_black_diamond_markup = \markup
{
    \override #'(baseline-skip . 1.75)
    \scale #'(0.75 . 0.75)
    \column
    {
        \musicglyph #"noteheads.s2harmonic"
        \musicglyph #"noteheads.s2harmonic"
        \musicglyph #"noteheads.s2harmonic"
    }
}

baca_triple_diamond_markup = \markup
{
    \override #'(baseline-skip . 1.75)
    \scale #'(0.75 . 0.75)
    \column
    {
        \musicglyph #"noteheads.s0harmonic"
        \musicglyph #"noteheads.s0harmonic"
        \musicglyph #"noteheads.s0harmonic"
    }
}

%%% FERMATA MARKUP %%%

baca_fermata_markup = \markup { \musicglyph #"scripts.ufermata" }

baca_long_fermata_markup = \markup { \musicglyph #"scripts.ulongfermata" }

baca_short_fermata_markup = \markup { \musicglyph #"scripts.ushortfermata" }

baca_very_long_fermata_markup = \markup {
    \musicglyph #"scripts.uverylongfermata"
    }

%%% NOTE-HEADS: SHAPED %%%

baca_black_diamond_note_head = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \once \override NoteHead.style = #'harmonic-black
    $music
    #}
    )

baca_diamond_note_head = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \once \override NoteHead.style = #'harmonic
    $music
    #}
    )

baca_semicircle_note_head = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \once \set shapeNoteStyles = ##(re re re re re re re)
    $music
    #}
    )

baca_square_note_head = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \once \set shapeNoteStyles = ##(la la la la la la la)
    $music
    #}
    )

baca_triangle_note_head = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \once \set shapeNoteStyles = ##(do do do do do do do)
    $music
    #}
    )

%%% NOTE-HEAD: SLAP-TONGUE %%%

baca_slap_tongue_note_head =
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

baca_metronome_mark_spanner_colored_left_text = #(
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

baca_metronome_mark_spanner_left_text = #(
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

baca_bcp_spanner_left_text = #(
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

baca_bcp_spanner_right_text = #(
    define-music-function
    (parser location n d music) (number? number? ly:music?)
    #{
    \tweak bound-details.right.text \markup \baca-bcp-right #n #d
    $music
    #})

baca_text_spanner_left_markup = #(
    define-music-function (parser location markup music) (markup? ly:music?)
    #{
    \tweak bound-details.left.text \markup \concat {
        \upright #markup \hspace #0.5
        }
    $music
    #})

baca_text_spanner_left_text = #(
    define-music-function (parser location string music) (string? ly:music?)
    #{
    \tweak bound-details.left.text \markup \concat {
        \upright #string \hspace #0.5
        }
    $music
    #})

baca_text_spanner_right_markup = #(
    define-music-function (parser location markup music) (markup? ly:music?)
    #{
    \tweak bound-details.right.text \markup \upright #markup
    $music
    #})

baca_text_spanner_right_text = #(
    define-music-function (parser location string music) (string? ly:music?)
    #{
    \tweak bound-details.right.text \markup \upright #string
    $music
    #})

%%% SPACING COMMANDS %%%

baca_new_spacing_section = #(define-music-function
    (parser location n d music) (number? number? ly:music?)
    #{
    \set Score.proportionalNotationDuration = #(ly:make-moment n d)
    \newSpacingSection
    $music
    #}
    )
