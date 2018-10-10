%%% SYMBOL %%%

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

%%% MARKUPS %%%

baca-circles-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.25
    }

baca-ext-tight-circles-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 "(ext. tight)"
    }

baca-fast-circles-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 (fast)
    }

baca-mod-width-circles-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 "(mod. width)"
    }

baca-poco-tight-circles-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 "(poco. tight)"
    }

baca-scratch-circles-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 (scratch)
    }

baca-slow-circles-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 (slow)
    }

baca-tight-circles-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 (tight)
    }

baca-very-tight-circles-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 "(very tight)"
    }

baca-very-wide-circles-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 "(very wide)"
    }

baca-wide-circles-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 (wide)
    }

baca-wide-poss-circles-markup = \markup \concat {
    \baca-circle-bowing-markup \hspace #1.75 \raise #-0.6 "(wide poss.)"
    }
