\version "2.25.16"

% SYMBOL

baca-circle-bowing-markup =
    \markup
    \translate #'(0.6 . 0)
    \scale #'(0.35 . 0.35)
    \concat {
        \draw-circle #2 #0.4 ##f
        \hspace #-4.5
        \raise #0.75
        \with-color #white
        \scale #'(0.35 . 0.35)
        \draw-circle #1 #1 ##t
        \hspace #-1.5
        \raise #-0.75
        \scale #'(0.75 . 0.75)
        \triangle ##t
        \hspace #-1
        \raise #1.35
        \with-color #white
        \rotate #45
        \filled-box #'(-0.35 . 0.35) #'(-0.35 . 0.35) #0
    }

% MARKUPS

baca-circle-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.25
    }

baca-circle-ext-tight-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 "(ext. tight)"
    }

baca-circle-fast-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 (fast)
    }

baca-circle-granulation-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 (granulation)
    }

baca-circle-mod-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 "(mod.)"
    }

baca-circle-mod-width-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 "(mod. width)"
    }

baca-circle-poco-tight-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 "(poco. tight)"
    }

baca-circle-scratch-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 (scratch)
    }

baca-circle-slow-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 (slow)
    }

baca-circle-tight-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 (tight)
    }

baca-circle-tight-poss-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 "(tight poss.)"
    }

baca-circle-tight-poss-grind-at-talon-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6
    "(tight poss.: grind at talon)"
    }

baca-circle-very-tight-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 "(very tight)"
    }

baca-circle-very-wide-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 "(very wide)"
    }

baca-circle-wide-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 (wide)
    }

baca-circle-wide-poss-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 "(wide poss.)"
    }
