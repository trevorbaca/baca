%%% STRING MARKUPS %%%

baca-arco-markup = \markup
    \whiteout
    \override #'(box-padding . 0.5)
    \box
    arco

baca-bow-directly-on-bridge-noise-only-markup = \markup
    \whiteout
    \override #'(box-padding . 0.5)
    \box
    \column {
        "bow directly on bridge;"
        "noise only: no pitch"
    }

baca-col-legno-battuto-markup = \markup
    \whiteout
    \override #'(box-padding . 0.5)
    \box
    "col legno battuto"

baca-half-clt-markup = \baca-boxed-markup "1/2 clt"

baca-leggieriss-markup = \markup
    leggieriss.

baca-ob-markup = \markup
    \whiteout
    \override #'(box-padding . 0.5)
    \box
    "OB"

baca-pizz-markup = \markup
    \upright
    pizz.

baca-pochiss-scratch-markup = \markup
    \whiteout
    "pochiss. scratch"

baca-poco-vib-markup = \markup "poco vib."

baca-pos-ord-markup = \markup "pos. ord."

baca-spazz-markup = \markup
    \whiteout
    \override #'(box-padding . 0.5)
    \box
    spazz.

baca-spazzolato-boxed-markup = \markup
    \whiteout
    \override #'(box-padding . 0.5)
    \box
    spazzolato

baca-string-i-markup = \markup
    I

baca-string-ii-markup = \markup
    II

baca-string-iii-markup = \markup
    III

baca-string-iv-markup = \markup
    IV

baca-tasto-markup = \markup
    tasto

baca-tasto-plus-half-scratch-markup = \markup
    \whiteout
    "tasto + 1/2 scratch"

baca-tasto-plus-pochiss-scratch-markup = \markup
    \whiteout
    "tasto + pochiss. scratch"

baca-tasto-plus-scratch-moltiss-markup = \markup
    \whiteout
    "tasto + scratch moltiss."

baca-tasto-plus-xfb-markup = \markup
    \whiteout
    "tasto + XFB"

baca-vib-poco-markup = \markup "vib. poco"

baca-xfb-markup = \markup
    \whiteout
    \override #'(box-padding . 0.5)
    \box
    XFB

baca-xp-markup = \baca-boxed-markup XP
