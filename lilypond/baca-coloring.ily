%%% PERSISTENT INDICATOR MARKUP %%%

baca-explicit-indicator-markup = #(define-music-function string (string?)
    #{
    - \markup \with-color #(x11-color 'blue) { #string }
    #}
    )

baca-default-indicator-markup = #(define-music-function string (string?)
    #{
    - \markup \with-color #(x11-color 'DarkViolet) { #string }
    #}
    )

baca-redundant-indicator-markup = #(define-music-function string (string?)
    #{
    - \markup \with-color #(x11-color 'DeepPink1) { #string }
    #}
    )

baca-reapplied-indicator-markup = #(define-music-function string (string?)
    #{
    - \markup \with-color #(x11-color 'green4) { #string }
    #}
    )

% NOTE: this works:
%zebra = #(define-music-function (color) (color?)
%    #{
%    - \tweak color #color
%    - \markup { FOO }
%    #}
%    )

%%% COLOR MARKUP %%%

baca-dark-cyan-markup = #(define-music-function string (string?)
    #{
    - \markup \fontsize #3 \with-color #(x11-color 'DarkCyan) { #string }
    #}
    )

baca-forest-green-markup = #(define-music-function string (string?)
    #{
    - \markup \fontsize #3 \with-color #(x11-color 'ForestGreen) { #string }
    #}
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
