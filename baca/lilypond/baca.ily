\include "/Users/trevorbaca/abjad/docs/source/_stylesheets/flared-hairpin.ily"
#(ly:set-option 'relative-includes #t)
\include "flared-hairpin-for-trevor.ily"
\include "text-spanner-id.ily"

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

%%% COLOR: MARKUP %%%

#(define-markup-command (baca-dark-cyan-markup layout props text) (markup?)
    "Dark cyan with font size 3."
    (interpret-markup layout props
        #{\markup \fontsize #3 \with-color #(x11-color 'DarkCyan) { #text }
            #}
        )
    )

#(define-markup-command (baca-forest-green-markup layout props text) (markup?)
    "Forest green with font size 3."
    (interpret-markup layout props
        #{\markup \fontsize #3 \with-color #(x11-color 'ForestGreen) { #text }
            #}
        )
    )

%%% COLOR: MUSIC %%%

baca_goldenrod_music = {
    \once \override Accidental.color = #(x11-color 'goldenrod)
    \once \override Beam.color = #(x11-color 'goldenrod)
    \once \override Dots.color = #(x11-color 'goldenrod)
    \once \override Flag.color = #(x11-color 'goldenrod)
    \once \override NoteHead.color = #(x11-color 'goldenrod)
    \once \override Stem.color = #(x11-color 'goldenrod)
    }

baca_magenta_music = {
    \once \override Accidental.color = #magenta
    \once \override Beam.color = #magenta
    \once \override Dots.color = #magenta
    \once \override Flag.color = #magenta
    \once \override NoteHead.color = #magenta
    \once \override Stem.color = #magenta
    }

baca_red_music = {
    \once \override Accidental.color = #red
    \once \override Beam.color = #red
    \once \override Dots.color = #red
    \once \override Flag.color = #red
    \once \override NoteHead.color = #red
    \once \override Stem.color = #red
    }

baca_octave_warning = \baca_red_music

baca_out_of_range_warning = \baca_red_music

baca_repeat_pitch_class_warning = \baca_red_music

baca_unpitched_music_warning = \baca_goldenrod_music

baca_unregistered_pitch_warning = \baca_magenta_music

%%% DAMP %%%

baca_karim_damp = \markup{
    \center-column {
  {\override #'(thickness . 1.8)
    \combine \draw-line #'(-1.5 . 0)
    \combine \draw-line #'(0 . -1.5)
    \combine \draw-line #'(0 . 1.5)
    \combine \draw-line #'(1.5 . 0)
    \draw-circle #0.8 #0.2 ##f
    }}}

% use scale instead of fontsize
baca_pierre_damp = \markup {
    \combine \bold "O"
    \path #0.2 
    #'((moveto -.4 .8)(lineto 2.2 .8)
        (closepath)
        (moveto .9 -.5)(lineto .9 2.1))
    }

%%% DYNAMICS: ANCORA %%%

baca_ppp_ancora = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "ppp"
            #:hspace 0.25
            #:normal-text "ancora"
            )
        )
    )

baca_pp_ancora = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "pp"
            #:hspace 0.25
            #:normal-text "ancora."
            )
        )
    )

baca_p_ancora = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "p"
            #:hspace 0.25
            #:normal-text "ancora"
            )
        )
    )

baca_mp_ancora = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "mp"
            #:hspace 0.25
            #:normal-text "ancora"
            )
        )
    )

baca_mf_ancora = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "mf"
            #:hspace 0.25
            #:normal-text "ancora"
            )
        )
    )

baca_f_ancora = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "f"
            #:hspace 0.25
            #:normal-text "ancora"
            )
        )
    )

baca_ff_ancora = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "ff"
            #:hspace 0.25
            #:normal-text "ancora"
            )
        )
    )

baca_fff_ancora = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "fff"
            #:hspace 0.25
            #:normal-text "ancora"
            )
        )
    )

%%% DYNAMICS: EFFORT %%%

baca_effort_ppp = #(
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

baca_effort_pp = #(
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

baca_effort_p = #(
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

baca_effort_mp = #(
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

baca_effort_mf = #(
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

baca_effort_f = #(
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

baca_effort_ff = #(
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

baca_effort_fff = #(
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

baca_effort_sfz = #(
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

baca_effort_sffz = #(
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

%%% DYNAMICS: FP %%%

baca_ffp = #(make-dynamic-script "ffp")
baca_fffp = #(make-dynamic-script "fffp")

%%% DYNAMICS: POSSIBILE %%%

baca_ppp_poss = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "ppp"
            #:hspace 0.25
            #:normal-text "poss."
            )
        )
    )

baca_pp_poss = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "pp"
            #:hspace 0.25
            #:normal-text "poss."
            )
        )
    )

baca_p_poss = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "p"
            #:hspace 0.25
            #:normal-text "poss."
            )
        )
    )

baca_f_poss = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "f"
            #:hspace 0.25
            #:normal-text "poss."
            )
        )
    )

baca_ff_poss = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "ff"
            #:hspace 0.25
            #:normal-text "poss."
            )
        )
    )

baca_fff_poss = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "fff"
            #:hspace 0.25 
            #:normal-text "poss."
            )
        )
    )

%%% DYNAMICS: SFORZANDO %%%

baca_sff = #(make-dynamic-script "sff")
baca_sffp = #(make-dynamic-script "sffp")
baca_sffpp = #(make-dynamic-script "sffpp")
baca_sfpp = #(make-dynamic-script "sfpp")
baca_sffz = #(make-dynamic-script "sffz")
baca_sfffz = #(make-dynamic-script "sfffz")

baca_sfz_f = #(
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

baca_sfz_p = #(
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

%%% DYNAMICS: SUBITO %%%

baca_ppp_sub = 
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "ppp"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca_pp_sub = 
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "pp"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca_p_sub = 
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "p"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca_mp_sub = 
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "mp"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca_mf_sub =
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "mf"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca_f_sub =
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "f"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca_ff_sub =
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "ff"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca_fff_sub =
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "fff"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

%%% DYNAMICS: TEXT ONLY %%%

    %%% NOTE: Use ...
    %%%
    %%%       DynamicText.X-extent = #'(0 . 0)
    %%%
    %%% ... instead of ...
    %%%
    %%%       DynamicText.X-extent = ##f
    %%%
    %%% ... to avoid warnings in LilyPond log.

baca_appena_udibile = 
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
    #(make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:normal-text "appena udibile"
            )
        )
    )

baca_niente = #(
    make-dynamic-script
    (markup
        #:whiteout
        #:normal-text
        #:italic "niente"
        )
    )

%%% DYNAMICS: WITH TEXT %%%

    %%% NOTE: Use ...
    %%%
    %%%       DynamicText.X-extent = #'(0 . 0)
    %%%
    %%% ... instead of ...
    %%%
    %%%       DynamicText.X-extent = ##f
    %%%
    %%% ... to avoid warnings in LilyPond log.

baca_p_sub_but_accents_continue_sffz = 
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
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

baca_f_but_accents_sffz =
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
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

baca_f_sub_but_accents_continue_sffz =
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
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

%%% MARKUP: DIAMONDS %%%

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
