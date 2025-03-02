\version "2.25.24"
\include "baca-markups.ily"

% ORDINARY

baca-bow-on-wooden-mute-markup = \markup "bow on wooden mute"

baca-bow-on-tailpiece-markup = \markup "bow on tailpiece"

baca-estr-sul-pont-markup = \markup "estr. sul pont."

baca-leggieriss-markup = \markup leggieriss.

baca-leggierissimo-markup = \markup leggierissimo

baca-molto-flautando-markup = \markup "molto flautando"

baca-non-flautando-markup = \markup "non flautando"

baca-ordinario-markup = \markup ordinario

baca-pizz-markup = \markup \upright pizz.

baca-pochiss-scratch-markup = \markup \whiteout "pochiss. scratch"

baca-poco-vib-markup = \markup "poco vib."

baca-pos-ord-markup = \markup "pos. ord."

baca-scratch-molto-markup = \markup "scratch molto"

baca-scratch-poss-markup = \markup "scratch poss."

baca-spazzolato-markup = \markup spazzolato

baca-string-i-markup = \markup I

baca-string-ii-markup = \markup II

baca-string-iii-markup = \markup III

baca-string-iv-markup = \markup IV

baca-strings-iii-plus-iv-markup = \markup III+IV

baca-subito-ordinario-markup = \markup "subito ordinario"

baca-tasto-markup = \markup tasto

baca-tasto-plus-half-scratch-markup = \markup \whiteout "tasto + 1/2 scratch"

baca-tasto-plus-pochiss-scratch-markup = \markup \whiteout "tasto + pochiss. scratch"

baca-tasto-plus-scratch-moltiss-markup = \markup \whiteout "tasto + scratch moltiss."

baca-tasto-plus-xfb-markup = \markup \whiteout "tasto + XFB"

baca-vib-poco-markup = \markup "vib. poco"

% BOXED

baca-boxed-arco-markup = \baca-boxed-markup \markup \whiteout arco

baca-boxed-arco-ordinario-markup = \baca-boxed-markup \markup \whiteout "arco ordinario"

baca-boxed-bow-directly-on-bridge-noise-only-markup =
    \baca-boxed-markup
    \markup
    \whiteout
    \column {
        "bow directly on bridge;"
        "noise only: no pitch"
    }

baca-boxed-col-legno-battuto-markup =
    \baca-boxed-markup \markup \whiteout "col legno battuto"

baca-boxed-half-clt-markup = \baca-boxed-markup "1/2 clt"

baca-boxed-ob-markup = \baca-boxed-markup \markup \whiteout OB

baca-boxed-spazz-markup = \baca-boxed-markup \markup \whiteout spazz.

baca-boxed-spazzolato-markup = \baca-boxed-markup \markup \whiteout spazzolato

baca-boxed-xfb-markup = \baca-boxed-markup \markup \whiteout XFB

baca-boxed-xp-markup = \baca-boxed-markup \markup \whiteout XP

% PARENTHESIZED

baca-parenthesized-half-harm-markup =
    \markup
    \upright
    \line {
        (
        \hspace #-0.5
        "half-harm."
        \hspace #-0.5
        )
        \hspace #0.5
    }

baca-parenthesized-pizz-markup =
    \markup
    \upright
    \line {
        (
        \hspace #-0.5
        "pizz."
        \hspace #-0.5
        )
        \hspace #0.5
    }

baca-parenthesized-string-i-markup =
    \markup
    \upright
    \line {
        (
        \hspace #-0.5
        I
        \hspace #-0.5
        )
        \hspace #0.5
    }

baca-parenthesized-string-ii-markup =
    \markup
    \upright
    \line {
        (
        \hspace #-0.5
        II
        \hspace #-0.5
        )
        \hspace #0.5
    }

baca-parenthesized-string-iii-markup =
    \markup
    \upright
    \line {
        (
        \hspace #-0.5
        III
        \hspace #-0.5
        )
        \hspace #0.5
    }

baca-parenthesized-string-iv-markup =
    \markup
    \upright
    \line {
        (
        \hspace #-0.5
        IV
        \hspace #-0.5
        )
        \hspace #0.5
    }
