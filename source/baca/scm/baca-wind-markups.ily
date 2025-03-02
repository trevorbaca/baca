\version "2.25.24"
\include "baca-markups.ily"

% ORDINARY

baca-airtone-markup = \markup \upright airtone

baca-cov-markup = \markup \upright cov.

baca-covered-markup = \markup \upright covered

baca-fluttertongue-markup = \markup \upright fluttertongue

% BOXED

baca-boxed-airtone-markup = \baca-boxed-markup \markup
    \whiteout
    airtone

baca-boxed-doubletrill-markup = \baca-boxed-markup \markup
    \whiteout
    doubletrill

baca-boxed-jet-whistle-markup = \baca-boxed-markup \markup
    \whiteout
    "jet whistle"

baca-boxed-keynoise-markup = \baca-boxed-markup \markup
    \whiteout
    keynoise

baca-boxed-overblow-markup = \baca-boxed-markup \markup
    \whiteout
    overblow

baca-boxed-put-reed-back-in-markup = \baca-boxed-markup \markup
    \whiteout
    "put reed back in"

baca-boxed-put-staple-back-in-markup = \baca-boxed-markup \markup
    \whiteout
    "put staple back in"

baca-boxed-remove-staple-markup = \baca-boxed-markup \markup
    \whiteout
    "remove staple"

baca-boxed-to-bass-clarinet-markup = \baca-boxed-markup \markup
    \whiteout
    "to bass clarinet"

baca-boxed-to-bass-flute-markup = \baca-boxed-markup \markup
    \whiteout
    "to bass flute"

% PARENTHESIZED

baca-parenthesized-air-markup =
    \markup
    \upright
    \line {
        (
        \hspace #-0.5
        air
        \hspace #-0.5
        )
        \hspace #0.5
    }

baca-parenthesized-cov-markup =
    \markup
    \upright
    \line {
        (
        \hspace #-0.5
        cov.
        \hspace #-0.5
        )
        \hspace #0.5
    }

baca-parenthesized-flutt-markup =
    \markup
    \upright
    \line {
        (
        \hspace #-0.5
        flutt. 
        \hspace #-0.5
        )
        \hspace #0.5
    }
