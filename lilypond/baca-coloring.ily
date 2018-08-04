%%% COLOR: MARKUP %%%

#(define-markup-command (baca-explicit-indicator-markup layout props text) (markup?)
    "Blue markup for explicit status."
    (interpret-markup layout props
        #{
        \markup \with-color #(x11-color 'blue) { #text }
        #}
        )
    )

#(define-markup-command (baca-dark-cyan-markup layout props text) (markup?)
    "Dark cyan with font size 3."
    (interpret-markup layout props
        #{
        \markup \fontsize #3 \with-color #(x11-color 'DarkCyan) { #text }
        #}
        )
    )

#(define-markup-command (baca-default-indicator-markup layout props text) (markup?)
    "Dark violet for default indicators."
    (interpret-markup layout props
        #{
        \markup \with-color #(x11-color 'DarkViolet) { #text }
        #}
        )
    )

#(define-markup-command (baca-redundant-indicator-markup layout props text) (markup?)
    "DeepPink1 for redundant indicators."
    (interpret-markup layout props
        #{
        \markup \with-color #(x11-color 'DeepPink1) { #text }
        #}
        )
    )

#(define-markup-command (baca-forest-green-markup layout props text) (markup?)
    "Forest green with font size 3."
    (interpret-markup layout props
        #{
        \markup \fontsize #3 \with-color #(x11-color 'ForestGreen) { #text }
        #}
        )
    )

#(define-markup-command (baca-reapplied-indicator-markup layout props text) (markup?)
    "Green4 markup for reapplied indicators."
    (interpret-markup layout props
        #{
        \markup \with-color #(x11-color 'green4) { #text }
        #}
        )
    )

%%% COLOR: MUSIC %%%

baca_octave_warning = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \abjad_color_music red
    $music
    #}
    )

baca_out_of_range_warning = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \abjad_color_music red
    $music
    #}
    )

baca_repeat_pitch_class_warning = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \abjad_color_music red
    $music
    #}
    )

baca_unpitched_music_warning = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \abjad_color_music goldenrod
    $music
    #}
    )

baca_unregistered_pitch_warning = #(
    define-music-function (parser location music) (ly:music?)
    #{
    \abjad_color_music magenta
    $music
    #}
    )


%%% COLOR: TIME SIGNATURE %%%

baca_time_signature_color = #(define-music-function
    (parser location color music) (symbol? ly:music?)
    #{
    \once \override Score.TimeSignature.color = #(x11-color #'color)
    $music
    #}
    )
