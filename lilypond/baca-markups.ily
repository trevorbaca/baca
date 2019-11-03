%%% ACCIDENTAL MARKUP %%%

baca-sharp-markup = \markup
    \line {
        \scale #'(0.65 . 0.65)
        \sharp
    }

%%% BOWSPEED MARKUP %%%

baca-left-broken-xfb-markup =
    \markup
    \upright
    \line {
        (
        \hspace #-0.5
        XFB
        \hspace #-0.5
        )
        \hspace #0.75
    }

%%% BOWSTROKE MARKUP %%%

baca-full-downbow-markup =
    \markup
    \combine
    \musicglyph #"scripts.downbow"
    \path #0.15
    #'(
        (moveto 0.7375 0.05)
        (rlineto 1 0)
        (closepath)
        )

baca-full-upbow-markup =
    \markup
    \combine
    \musicglyph #"scripts.upbow"
    \path #0.15
    #'(
        (moveto 0.62 2.005)
        (rlineto 1 0)
        (closepath)
        )

baca-stop-on-string-markup =
    \markup
    \path #0.15
    #'(
        (moveto 0 0)
        (rlineto 1 0)
        (closepath)
        (rmoveto 1 0.3)
        (rlineto 0 -0.6)
        (closepath)
        )

baca-stop-on-string-full-downbow-markup =
    \markup
    \combine
    \musicglyph #"scripts.downbow"
    \path #0.15
    #'(
        (moveto 0.7375 0.05)
        (rlineto 1 0)
        (closepath)
        (rmoveto 1 0.3)
        (rlineto 0 -0.6)
        (closepath)
        )

baca-stop-on-string-full-upbow-markup =
    \markup
    \combine
    \musicglyph #"scripts.upbow"
    \path #0.15
    #'(
        (moveto 0.62 2.005)
        (rlineto 1 0)
        (closepath)
        (rmoveto 1 0.3)
        (rlineto 0 -0.6)
        (closepath)
        )

%%% CIRCLE BOWING MARKUP %%%

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

baca-left-broken-circle-bowing-markup =
    \markup
    \upright
    \line {
        (
        \hspace #-0.5
        \raise #0.5
        \baca-circle-bowing-markup
        \hspace #0.65
        )
        \hspace #0.5
    }

%%% DAMP MARKUP (intentionally out of alphabetical order) %%%

baca-damp-markup =
    \markup
    \scale #'(0.75 . 0.75)
    \combine
    \bold
    \override #'(font-name . "Times") "O"
    \path #0.15
    #'(
        (moveto -.4 .7)
        (rlineto 2.4 0)
        (closepath)
        (moveto .8 -.5)
        (rlineto 0 2.4)
        )

baca-damp-half-clt-markup =
    \markup
    \raise #0.25
    \line {
        \baca-damp-markup
        "½ clt"
    }

baca-left-broken-damp-markup =
    \markup
    \upright
    \line {
        (
        \hspace #-0.85
        \baca-damp-markup
        \hspace #-0.85
        )
        \hspace #0.5
    }

%%% CLB MARKUP %%%

baca-damp-clb-one-markup =
    \markup
    \upright
    \line {
        \baca-damp-markup
        col legno battuto
        (I)
    }

baca-damp-clb-two-markup =
    \markup
    \upright
    \line {
        \baca-damp-markup
        col legno battuto
        (II)
    }

baca-damp-clb-three-markup =
    \markup
    \upright
    \line {
        \baca-damp-markup
        col legno battuto
        (III)
    }

baca-damp-clb-four-markup =
    \markup
    \upright
    \line {
        \baca-damp-markup
        col legno battuto
        (IV)
    }

baca-left-broken-clb-markup =
    \markup
    \upright
    \line {
        (
        \hspace #-0.5
        clb
        \hspace #-0.5
        )
        \hspace #0.75
    }

%%% CLT MARKUP

baca-left-broken-half-clt-markup =
    \markup
    \upright
    \line {
        (
        \hspace #-0.5
        "½ clt"
        \hspace #-0.5
        )
        \hspace #0.5
    }

%%% COVERED MARKUP %%%

baca-cov-markup =
    \markup
    \upright
    \line {
        %%%\hspace #-0.5
        cov.
        %%%%\hspace #-0.5
    }

baca-covered-markup =
    \markup
    \upright
    \line {
        %%%\hspace #-0.5
        covered
        %%%%\hspace #-0.5
    }

baca-left-broken-covered-markup =
    \markup
    \upright
    \line {
        (
        \hspace #-0.85
        cov.
        \hspace #-0.85
        )
        \hspace #0.5
    }

%%% DIAMOND MARKUP %%%

baca-black-diamond-markup =
    \markup
    \musicglyph #"noteheads.s2harmonic"

baca-diamond-markup =
    \markup
    \musicglyph #"noteheads.s0harmonic"

baca-diamond-parenthesized-double-diamond-markup =
    \markup
    \concat {
        \general-align #Y #2.5
        \scale #'(0.75 . 0.75)
        \musicglyph #"noteheads.s0harmonic"
        \hspace #0.45
        \general-align #Y #1
        \scale #'(1 . 1.5)
        "("
        \hspace #-0.1
        \general-align #Y #1.25
        \override #'(baseline-skip . 1.75)
        \scale #'(0.75 . 0.75)
        \column
        {
            \musicglyph #"noteheads.s0harmonic"
            \musicglyph #"noteheads.s0harmonic"
        }
        \hspace #-0.15
        \general-align #Y #1
        \scale #'(1 . 1.5)
        ")"
    }

baca-double-black-diamond-markup =
    \markup
    \override #'(baseline-skip . 1.75)
    \scale #'(0.75 . 0.75)
    \column
    {
        \musicglyph #"noteheads.s2harmonic"
        \musicglyph #"noteheads.s2harmonic"
    }

baca-double-diamond-markup =
    \markup
    \override #'(baseline-skip . 1.75)
    \scale #'(0.75 . 0.75)
    \column
    {
        \musicglyph #"noteheads.s0harmonic"
        \musicglyph #"noteheads.s0harmonic"
    }

baca-double-diamond-parenthesized-top-markup =
    \markup
    \concat {
        \general-align #Y #1.25
        \override #'(baseline-skip . 1.75)
        \scale #'(0.75 . 0.75)
        \center-column
        {
            \concat {
                \general-align #Y #0.75
                "("
                \general-align #Y #1
                \musicglyph #"noteheads.s0harmonic"
                \general-align #Y #0.75
                ")"
                }
            \musicglyph #"noteheads.s0harmonic"
        }
    }

baca-triple-black-diamond-markup =
    \markup
    \override #'(baseline-skip . 1.75)
    \scale #'(0.75 . 0.75)
    \column
    {
        \musicglyph #"noteheads.s2harmonic"
        \musicglyph #"noteheads.s2harmonic"
        \musicglyph #"noteheads.s2harmonic"
    }

baca-triple-diamond-markup =
    \markup
    \override #'(baseline-skip . 1.75)
    \scale #'(0.75 . 0.75)
    \column
    {
        \musicglyph #"noteheads.s0harmonic"
        \musicglyph #"noteheads.s0harmonic"
        \musicglyph #"noteheads.s0harmonic"
    }

baca-triple-diamond-parenthesized-top-markup =
    \markup
    \concat {
        \general-align #Y #1.25
        \override #'(baseline-skip . 1.75)
        \scale #'(0.75 . 0.75)
        \center-column
        {
            \concat {
                \general-align #Y #0.75
                "("
                \general-align #Y #1
                \musicglyph #"noteheads.s0harmonic"
                \general-align #Y #0.75
                ")"
                }
            \musicglyph #"noteheads.s0harmonic"
            \musicglyph #"noteheads.s0harmonic"
        }
    }

%%% DURATION MULTIPLIER MARKUP %%%

baca-duration-multiplier-markup = #(
    define-music-function
    (n d)
    (string? string?)
    #{
    - \tweak color #(x11-color 'sienna)
    - \tweak extra-offset #'(0 . 3)
    - \markup
    \with-dimensions-from \null
    \fraction #n #d
    #}
    )

%%% FERMATA MARKUP %%%

baca-fermata-markup =
    \markup
    \with-dimensions-from \null
    \musicglyph #"scripts.ufermata"

baca-long-fermata-markup = \markup
    \with-dimensions-from \null
    \musicglyph #"scripts.ulongfermata"

baca-short-fermata-markup =
    \markup
    \with-dimensions-from \null
    \musicglyph #"scripts.ushortfermata"

baca-very-long-fermata-markup =
    \markup
    \with-dimensions-from \null
    \musicglyph #"scripts.uverylongfermata"

%%% NULL MARKUP %%%

baca-null-markup = \markup \null

%%% REHEARSAL MARKS %%%

% IMPORTANT: markup attach direction must be neutral or down (- or _);
%            markup attach direction of up (^) negatively impacts global
%            skips context vertical spacing
baca-rehearsal-mark-markup = #(
    define-music-function
    (string font-size)
    (string? number?)
    #{
    - \tweak font-size #font-size
    - \markup
    \with-dimensions-from \null
    \halign #-1
    \override #'(box-padding . 0.5)
    \box
    { \combine \halign #0 #string \halign #0 \transparent "O" }
    #}
    )

%%% SCP MARKUP %%%

baca-left-broken-t-markup =
    \markup
    \upright
    \line {
        (
        \hspace #-0.5
        T
        \hspace #-0.5
        )
        \hspace #0.75
    }

%%% SPAZZOLATO MARKUP %%%

baca-spazzolato-markup =
    \markup
    \upright
    spazzolato

baca-left-broken-spazz-markup =
    \markup
    \upright
    \line {
        (
        \hspace #-0.5
        spazz. 
        \hspace #-0.5
        )
        \hspace #0.75
    }

%%% VIBRATO MARKUP %%%

baca-non-vib-markup =
    \markup
    \upright
    "non vib."

baca-sub-non-vib-markup =
    \markup
    \upright
    "sub. non vib."
