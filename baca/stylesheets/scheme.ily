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

%%% DYNAMICS (ANCORA) %%%

ppp_poss = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "ppp"
            #:hspace 0.25
            #:normal-text "ancora"
            )
        )
    )

pp_ancora = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "pp"
            #:hspace 0.25
            #:normal-text "ancora."
            )
        )
    )

p_ancora = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "p"
            #:hspace 0.25
            #:normal-text "ancora"
            )
        )
    )

mp_ancora = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "mp"
            #:hspace 0.25
            #:normal-text "ancora"
            )
        )
    )

mf_ancora = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "mf"
            #:hspace 0.25
            #:normal-text "ancora"
            )
        )
    )

f_ancora = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "f"
            #:hspace 0.25
            #:normal-text "ancora"
            )
        )
    )

ff_ancora = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "ff"
            #:hspace 0.25
            #:normal-text "ancora"
            )
        )
    )

fff_ancora = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "fff"
            #:hspace 0.25
            #:normal-text "ancora"
            )
        )
    )

%%% DYNAMICS (PHRASAL) %%%

p_sub_but_accents_continue_sffz = 
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent ##f
    #(make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:general-align Y -0.75 #:dynamic "p"
            #:normal-text "sub. (but accents continue"
            #:dynamic "sffz"
            #:hspace -0.5
            #:normal-text ")"
            )
        )
    )

f_but_accents_sffz =
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent ##f
    #(make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:general-align Y -0.75 #:dynamic "f"
            #:hspace 0.25
            #:normal-text "(but accents"
            #:hspace 0.25
            #:dynamic "sffz"
            #:hspace -0.5
            #:normal-text ")"
            )
        )
    )

f_sub_but_accents_continue_sffz =
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent ##f
    #(make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:general-align Y -0.75 #:dynamic "f"
            #:hspace 0.25
            #:normal-text "sub. (but accents continue"
            #:dynamic "sffz"
            #:hspace -0.5
            #:normal-text ")"
            )
        )
    )

%%% DYNAMICS (EFFORT) %%%

effort_ppp = #(
    make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:general-align Y -2 #:normal-text #:larger "“"
            #:hspace -0.1
            #:dynamic "ppp"
            #:hspace -0.25
            #:general-align Y -2 #:normal-text #:larger "”"
            )
        )
    )

effort_pp = #(
    make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:general-align Y -2 #:normal-text #:larger "“"
            #:hspace -0.1
            #:dynamic "pp"
            #:hspace -0.25
            #:general-align Y -2 #:normal-text #:larger "”"
            )
        )
    )

effort_p = #(
    make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:general-align Y -2 #:normal-text #:larger "“"
            #:hspace -0.1
            #:dynamic "p"
            #:hspace -0.25
            #:general-align Y -2 #:normal-text #:larger "”"
            )
        )
    )

effort_mp = #(
    make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:general-align Y -2 #:normal-text #:larger "“"
            #:hspace -0.1
            #:dynamic "mp"
            #:hspace -0.25
            #:general-align Y -2 #:normal-text #:larger "”"
            )
        )
    )

effort_mf = #(
    make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:general-align Y -2 #:normal-text #:larger "“"
            #:hspace -0.1
            #:dynamic "mf"
            #:hspace -0.2
            #:general-align Y -2 #:normal-text #:larger "”"
            )
        )
    )

effort_f = #(
    make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:general-align Y -2 #:normal-text #:larger "“"
            #:hspace -0.4
            #:dynamic "f"
            #:hspace -0.2
            #:general-align Y -2 #:normal-text #:larger "”"
            )
        )
    )

effort_ff = #(
    make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:general-align Y -2 #:normal-text #:larger "“"
            #:hspace -0.4
            #:dynamic "ff"
            #:hspace -0.2
            #:general-align Y -2 #:normal-text #:larger "”"
            )
        )
    )

effort_fff = #(
    make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:general-align Y -2 #:normal-text #:larger "“"
            #:hspace -0.4
            #:dynamic "fff"
            #:hspace -0.2
            #:general-align Y -2 #:normal-text #:larger "”"
            )
        )
    )

effort_sfz = #(
    make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:general-align Y -2 #:normal-text #:larger "“"
            #:hspace -0.3
            #:dynamic "sfz"
            #:hspace -0.2
            #:general-align Y -2 #:normal-text #:larger "”"
            )
        )
    )

effort_sffz = #(
    make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:general-align Y -2 #:normal-text #:larger "“"
            #:hspace -0.3
            #:dynamic "sffz"
            #:hspace -0.2
            #:general-align Y -2 #:normal-text #:larger "”"
            )
        )
    )

%%% DYNAMICS (FP) %%%

ffp = #(make-dynamic-script "ffp")
fffp = #(make-dynamic-script "fffp")

%%% DYNAMICS (POSSIBILE) %%%

ppp_poss = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "ppp"
            #:hspace 0.25
            #:normal-text "poss."
            )
        )
    )

pp_poss = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "pp"
            #:hspace 0.25
            #:normal-text "poss."
            )
        )
    )

p_poss = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "p"
            #:hspace 0.25
            #:normal-text "poss."
            )
        )
    )

f_poss = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "f"
            #:hspace 0.25
            #:normal-text "poss."
            )
        )
    )

ff_poss = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "ff"
            #:hspace 0.25
            #:normal-text "poss."
            )
        )
    )

fff_poss = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "fff"
            #:hspace 0.25 
            #:normal-text "poss."
            )
        )
    )

%%% DYNAMICS (SFORZANDO) %%%

sff = #(make-dynamic-script "sff")
sffp = #(make-dynamic-script "sffp")
sffpp = #(make-dynamic-script "sffpp")
sfpp = #(make-dynamic-script "sfpp")
sffz = #(make-dynamic-script "sffz")
sfffz = #(make-dynamic-script "sfffz")

sfz_f = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "sfz"
            #:hspace -0.25
            #:normal-text "/"
            #:hspace -0.5
            #:dynamic "f"
            )
        )
    )

sfz_p = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "sfz"
            #:hspace 0
            #:normal-text "/"
            #:hspace 0 
            #:dynamic "p"
            )
        )
    )

%%% DYNAMICS (SUBITO) %%%

ppp_sub = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "ppp"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

pp_sub = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "pp"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

p_sub = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "p"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

mp_sub = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "mp"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

mf_sub = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "mf"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

f_sub = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "f"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

ff_sub = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "ff"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

fff_sub = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "fff"
            #:hspace 0.25
            #:normal-text "sub."
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
