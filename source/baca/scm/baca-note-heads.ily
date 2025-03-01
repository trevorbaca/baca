\version "2.25.23"

% SHAPE NOTE-HEADS

baca-black-diamond-note-head = #(
    define-music-function (music) (ly:music?)
    #{
    \once \override NoteHead.style = #'harmonic-black
    $music
    #}
    )

baca-diamond-note-head = #(
    define-music-function (music) (ly:music?)
    #{
    \once \override NoteHead.style = #'harmonic
    $music
    #}
    )

baca-semicircle-note-head = #(
    define-music-function (music) (ly:music?)
    #{
    \once \set shapeNoteStyles = ##(re re re re re re re)
    $music
    #}
    )

baca-square-note-head = #(
    define-music-function (music) (ly:music?)
    #{
    \once \set shapeNoteStyles = ##(la la la la la la la)
    $music
    #}
    )

baca-triangle-note-head = #(
    define-music-function (music) (ly:music?)
    #{
    \once \set shapeNoteStyles = ##(do do do do do do do)
    $music
    #}
    )

% SLAP-TONGUE NOTE-HEAD

baca-slap-tongue-note-head = #(
    define-music-function (music) (ly:music?)
    #{
    \override NoteHead.stencil = #(
        lambda
        (grob)
        (grob-interpret-markup grob (markup #:musicglyph "scripts.sforzato"))
        )
    \override NoteHead.extra-offset = #'(0.1 . 0.0)
    $music
    \revert NoteHead.stencil
    \revert NoteHead.extra-offset
    #}
    )
