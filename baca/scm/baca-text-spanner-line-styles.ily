baca-dashed-line-with-arrow = #(
    define-music-function (parser location music) (ly:music?)
    #{
    - \abjad-dashed-line-with-arrow
    - \tweak Y-extent ##f
    $music
    #}
    )

baca-dashed-line-with-hook = #(
    define-music-function (parser location music) (ly:music?)
    #{
    - \abjad-dashed-line-with-hook
    - \tweak Y-extent ##f
    $music
    #}
    )

baca-dashed-line-with-up-hook = #(
    define-music-function (parser location music) (ly:music?)
    #{
    - \abjad-dashed-line-with-up-hook
    - \tweak Y-extent ##f
    $music
    #}
    )

baca-solid-line-with-arrow = #(
    define-music-function (parser location music) (ly:music?)
    #{
    - \abjad-solid-line-with-arrow
    - \tweak Y-extent ##f
    $music
    #}
    )

baca-solid-line-with-hook = #(
    define-music-function (parser location music) (ly:music?)
    #{
    - \abjad-solid-line-with-hook
    - \tweak Y-extent ##f
    $music
    #}
    )

baca-solid-line-with-up-hook = #(
    define-music-function (parser location music) (ly:music?)
    #{
    - \abjad-solid-line-with-up-hook
    - \tweak Y-extent ##f
    $music
    #}
    )

baca-invisible-line = #(
    define-music-function (parser location music) (ly:music?)
    #{
    - \abjad-invisible-line
    - \tweak Y-extent ##f
    $music
    #}
    )
