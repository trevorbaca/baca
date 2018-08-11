%%% PERSISTENT INDICATOR MARKUP %%%

baca-explicit-indicator-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \markup \with-color #(x11-color 'blue) { #string }
    #}
    )

baca-default-indicator-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \markup \with-color #(x11-color 'DarkViolet) { #string }
    #}
    )

baca-redundant-indicator-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \markup \with-color #(x11-color 'DeepPink1) { #string }
    #}
    )

baca-reapplied-indicator-markup = #(
    define-music-function
    string
    (string?)
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

baca-dark-cyan-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \markup \fontsize #3 \with-color #(x11-color 'DarkCyan) { #string }
    #}
    )

baca-forest-green-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \markup \fontsize #3 \with-color #(x11-color 'ForestGreen) { #string }
    #}
    )

%%% COLOR: MUSIC %%%

baca-octave-warning = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \abjad-color-music #'red
    $music
    #}
    )

baca-out-of-range-warning = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \abjad-color-music #'red
    $music
    #}
    )

baca-repeat-pitch-class-warning = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \abjad-color-music #'red
    $music
    #}
    )

baca-unpitched-music-warning = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \abjad-color-music #'goldenrod
    $music
    #}
    )

baca-unregistered-pitch-warning = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \abjad-color-music #'magenta
    $music
    #}
    )

%%% COLOR: TIME SIGNATURE %%%

baca-time-signature-color = #(
    define-music-function
    (parser location color music)
    (symbol? ly:music?)
    #{
    \once \override Score.TimeSignature.color = #(x11-color #'color)
    $music
    #}
    )
