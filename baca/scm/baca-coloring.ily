%%% COLORED MUSIC %%%

baca-mock-coloring = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \abjad-color-music #'firebrick
    $music
    #}
    )

baca-not-yet-pitched-coloring = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \abjad-color-music #'goldenrod
    $music
    #}
    )

baca-not-yet-registered-pitch-coloring = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \abjad-color-music #'magenta
    $music
    #}
    )

baca-octave-coloring = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \abjad-color-music #'red
    $music
    #}
    )

baca-out-of-range-coloring = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \abjad-color-music #'red
    $music
    #}
    )

baca-repeat-pitch-class-coloring = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \abjad-color-music #'red
    $music
    #}
    )

%%% COLORED TIME SIGNATURES %%%

baca-time-signature-color = #(
    define-music-function
    (parser location color music)
    (symbol? ly:music?)
    #{
    \once \override Score.TimeSignature.color = #(x11-color color)
    $music
    #}
    )

baca-time-signature-transparent = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \once \override Score.TimeSignature.transparent = ##t
    $music
    #}
    )

%%% INSTRUMENT COLORING %%%

baca-explicit-instrument-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \markup
    \with-color #(x11-color 'blue)
    #string
    #}
    )

baca-reapplied-instrument-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \markup
    \with-color #(x11-color 'green4)
    #string
    #}
    )

baca-redundant-instrument-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \markup
    \with-color #(x11-color 'DeepPink1)
    #string
    #}
    )

%%% SHORT INSTRUMENT NAME COLORING %%%

baca-explicit-short-instrument-name-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \markup
    \with-color #(x11-color 'blue)
    #string
    #}
    )

baca-reapplied-short-instrument-name-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \markup
    \with-color #(x11-color 'green4)
    #string
    #}
    )

baca-redundant-short-instrument-name-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \markup
    \with-color #(x11-color 'DeepPink1)
    #string
    #}
    )

%%% NOTES

% Note that this works:
%zebra = #(
%    define-music-function
%    (color)
%    (color?)
%    #{
%    - \tweak color #color
%    - \markup
%    FOO
%    #}
%    )
