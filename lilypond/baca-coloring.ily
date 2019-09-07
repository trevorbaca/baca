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

baca-time-signature-transparent = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \once \override Score.TimeSignature.transparent = ##t
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
    \once \override MultiMeasureRest.transparent = ##t
    \once \override NoteHead.no-ledgers = ##t
    \once \override NoteHead.transparent = ##t
    \once \override RepeatTie.transparent = ##t
    \once \override Stem.transparent = ##t
    \once \override StemTremolo.transparent = ##t
    $music
    #}
    )

%%% PERSISTENT INDICATOR MARKUP %%%

baca-explicit-indicator-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \markup
    \with-color #(x11-color 'blue)
    #string
    #}
    )

baca-default-indicator-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \markup
    \with-color #(x11-color 'DarkViolet)
    #string
    #}
    )

baca-redundant-indicator-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \markup
    \with-color #(x11-color 'DeepPink1)
    #string
    #}
    )

baca-reapplied-indicator-markup = #(
    define-music-function
    string
    (string?)
    #{
    - \markup
    \with-color #(x11-color 'green4)
    #string
    #}
    )

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
