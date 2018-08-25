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

%%% COLORED MARKUP %%%

baca-clock-time-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \tweak extra-offset #'(0 . 14)
    - \tweak font-size #2
    - \markup
    \with-dimensions-from \null
    \with-color #(x11-color 'DarkCyan)
    { #string }
    #}
    )

baca-local-measure-index-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \tweak extra-offset #'(0 . 6)
    - \tweak font-size #2
    - \markup
    \with-dimensions-from \null
    \with-color #(x11-color 'DarkCyan)
    { #string }
    #}
    )

baca-local-measure-number-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \tweak extra-offset #'(0 . 6)
    - \tweak font-size #2
    - \markup
    \with-dimensions-from \null
    \with-color #(x11-color 'DarkCyan)
    { #string }
    #}
    )

baca-measure-number-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \tweak extra-offset #'(0 . 10)
    - \tweak font-size #2
    - \markup
    \with-dimensions-from \null
    \with-color #(x11-color 'DarkCyan)
    { #string }
    #}
    )

baca-spacing-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \tweak extra-offset #'(0 . 14)
    - \tweak font-size #2
    - \markup
    \with-dimensions-from \null
    \with-color #(x11-color 'ForestGreen)
    { #string }
    #}
    )

baca-stage-number-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \tweak extra-offset #'(0 . 14)
    - \tweak font-size #2
    - \markup
    \with-dimensions-from \null
    \with-color #(x11-color 'DarkCyan)
    { #string }
    #}
    )

%%% COLORED MUSIC %%%

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

%%% COLORED TIME SIGNATURES %%%

baca-time-signature-color = #(
    define-music-function
    (parser location color music)
    (symbol? ly:music?)
    #{
    \once \override Score.TimeSignature.color = #(x11-color #'color)
    $music
    #}
    )

baca-invisible-music = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \once \override Accidental.transparent = ##t
    \once \override Dots.transparent = ##t
    \once \override NoteHead.no-ledgers = ##t
    \once \override NoteHead.transparent = ##t
    $music
    #}
    )

% NOTE: this works:
%zebra = #(define-music-function (color) (color?)
%    #{
%    - \tweak color #color
%    - \markup { FOO }
%    #}
%    )

