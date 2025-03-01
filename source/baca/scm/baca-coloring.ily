\version "2.25.23"

% BAR LINE COLORING

baca-thick-red-bar-line = #(
    define-music-function (music) (ly:music?)
    #{
    \once \override Score.BarLine.color = #red
    \once \override Score.BarLine.hair-thickness = 3
    \once \override Score.SpanBar.color = #red
    $music
    #}
    )

% INSTRUMENT COLORING

baca-explicit-instrument-markup = #(
    define-music-function string (string?)
    #{
    - \markup
    \with-color #(x11-color 'blue)
    #string
    #}
    )

baca-reapplied-instrument-markup = #(
    define-music-function string (string?)
    #{
    - \markup
    \with-color #(x11-color 'green4)
    #string
    #}
    )

baca-redundant-instrument-markup = #(
    define-music-function string (string?)
    #{
    - \markup
    \with-color #(x11-color 'DeepPink1)
    #string
    #}
    )

% MUSIC COLORING

baca-mock-coloring = #(
    define-music-function (music) (ly:music?)
    #{
    \abjad-color-music #'firebrick
    $music
    #}
    )

baca-not-yet-pitched-coloring = #(
    define-music-function (music) (ly:music?)
    #{
    \abjad-color-music #'goldenrod
    $music
    #}
    )

baca-not-yet-registered-pitch-coloring = #(
    define-music-function (music) (ly:music?)
    #{
    \abjad-color-music #'magenta
    $music
    #}
    )

baca-octave-coloring = #(
    define-music-function (music) (ly:music?)
    #{
    \abjad-color-music #'red
    $music
    #}
    )

baca-out-of-range-coloring = #(
    define-music-function (music) (ly:music?)
    #{
    \abjad-color-music #'red
    $music
    #}
    )

baca-repeat-pitch-class-coloring = #(
    define-music-function (music) (ly:music?)
    #{
    \abjad-color-music #'red
    $music
    #}
    )

% SHORT INSTRUMENT NAME COLORING

baca-explicit-short-instrument-name-markup = #(
    define-music-function string (string?)
    #{
    - \markup
    \with-color #(x11-color 'blue)
    #string
    #}
    )

baca-reapplied-short-instrument-name-markup = #(
    define-music-function string (string?)
    #{
    - \markup
    \with-color #(x11-color 'green4)
    #string
    #}
    )

baca-redundant-short-instrument-name-markup = #(
    define-music-function string (string?)
    #{
    - \markup
    \with-color #(x11-color 'DeepPink1)
    #string
    #}
    )

% TIME SIGNATURE COLORING

baca-time-signature-color = #(
    define-music-function (color music) (color? ly:music?)
    #{
    \once \override Score.TimeSignature.color = #color
    $music
    #}
    )

baca-time-signature-transparent = #(
    define-music-function (music) (ly:music?)
    #{
    \once \override Score.TimeSignature.transparent = ##t
    $music
    #}
    )

% NOTES

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
