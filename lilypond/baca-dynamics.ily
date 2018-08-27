%%% ANCORA DYNAMICS %%%

#(define-markup-command
    (baca-ancora-dynamic layout props dynamic)
    (string?)
    (interpret-markup layout props
    #{
    \markup
    \line {
        \dynamic #dynamic
        \hspace #0.25
        \normal-text ancora
        }
    #}))

baca-ppp-ancora = #(
    make-dynamic-script
    (markup #:baca-ancora-dynamic "ppp")
    )

baca-pp-ancora = #(
    make-dynamic-script
    (markup #:baca-ancora-dynamic "pp")
    )

baca-p-ancora = #(
    make-dynamic-script
    (markup #:baca-ancora-dynamic "p")
    )

baca-mp-ancora = #(
    make-dynamic-script
    (markup #:baca-ancora-dynamic "mp")
    )

baca-mm-ancora = #(
    make-dynamic-script
    (markup #:baca-ancora-dynamic "mm")
    )

baca-f-ancora = #(
    make-dynamic-script
    (markup #:baca-ancora-dynamic "f")
    )

baca-ff-ancora = #(
    make-dynamic-script
    (markup #:baca-ancora-dynamic "ff")
    )

baca-fff-ancora = #(
    make-dynamic-script
    (markup #:baca-ancora-dynamic "fff")
    )

%%% EFFORT DYNAMICS %%%

#(define-markup-command
    (baca-effort-dynamic layout props left dynamic right)
    (number? string? number?)
    (interpret-markup layout props
    #{
    \markup
    \whiteout
    \line {
        \general-align #Y #-2 \normal-text \larger "“"
        \hspace #left
        \dynamic #dynamic
        \hspace #right
        \general-align #Y #-2 \normal-text \larger "”"
        }
    #}))

baca-effort-ppp = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.1 "ppp" -0.25)
    )

baca-effort-pp = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.1 "pp" -0.25)
    )

baca-effort-p = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.1 "p" -0.25)
    )

baca-effort-mp = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.1 "mp" -0.25)
    )

baca-effort-mf = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.1 "mf" -0.2)
    )

baca-effort-f = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.4 "mf" -0.2)
    )

baca-effort-ff = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.4 "mf" -0.2)
    )

baca-effort-fff = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.4 "mf" -0.2)
    )

baca-effort-sfz = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.3 "mf" -0.2)
    )

baca-effort-sffz = #(
    make-dynamic-script
    (markup #:baca-effort-dynamic -0.3 "mf" -0.2)
    )

%%% FP DYNAMICS %%%

baca-ffp = #(make-dynamic-script "ffp")
baca-fffp = #(make-dynamic-script "fffp")

%%% POSS. DYNAMICS %%%

#(define-markup-command
    (baca-poss-dynamic layout props dynamic)
    (string?)
    (interpret-markup layout props
    #{
    \markup
    \line {
        \dynamic #dynamic
        \hspace #0.25
        \normal-text poss.
        }
    #}))

baca-ppp-poss = #(
    make-dynamic-script
    (markup #:baca-poss-dynamic "ppp")
    )

baca-pp-poss = #(
    make-dynamic-script
    (markup #:baca-poss-dynamic "pp")
    )

baca-p-poss = #(
    make-dynamic-script
    (markup #:baca-poss-dynamic "p")
    )

baca-f-poss = #(
    make-dynamic-script
    (markup #:baca-poss-dynamic "f")
    )

baca-ff-poss = #(
    make-dynamic-script
    (markup #:baca-poss-dynamic "ff")
    )

baca-fff-poss = #(
    make-dynamic-script
    (markup #:baca-poss-dynamic "fff")
    )

%%% SEMPRE DYNAMICS %%%

#(define-markup-command
    (baca-sempre-dynamic layout props dynamic)
    (string?)
    (interpret-markup layout props
    #{
    \markup
    \line {
        \dynamic #dynamic
        \hspace #0.25
        \normal-text sempre
        }
    #}))

baca-ppp-sempre = #(
    make-dynamic-script
    (markup #:baca-sempre-dynamic "ppp")
    )

baca-pp-sempre = #(
    make-dynamic-script
    (markup #:baca-sempre-dynamic "pp")
    )

baca-p-sempre = #(
    make-dynamic-script
    (markup #:baca-sempre-dynamic "p")
    )

baca-mp-sempre = #(
    make-dynamic-script
    (markup #:baca-sempre-dynamic "mp")
    )

baca-mf-sempre = #(
    make-dynamic-script
    (markup #:baca-sempre-dynamic "mf")
    )

baca-f-sempre = #(
    make-dynamic-script
    (markup #:baca-sempre-dynamic "f")
    )

baca-ff-sempre = #(
    make-dynamic-script
    (markup #:baca-sempre-dynamic "ff")
    )

baca-fff-sempre = #(
    make-dynamic-script
    (markup #:baca-sempre-dynamic "fff")
    )

%%% SCRATCH DYNAMICS %%%

#(define-markup-command
    (baca-scratch-dynamic layout props dynamic)
    (string?)
    (interpret-markup layout props
    #{
    \markup
    \line {
        \dynamic #dynamic
        \hspace #0.25
        \normal-text scratch
        }
    #}))

baca-ppp-scratch = #(
    make-dynamic-script
    (markup #:baca-scratch-dynamic "ppp")
    )

baca-pp-scratch = #(
    make-dynamic-script
    (markup #:baca-scratch-dynamic "pp")
    )

baca-p-scratch = #(
    make-dynamic-script
    (markup #:baca-scratch-dynamic "p")
    )

baca-mp-scratch = #(
    make-dynamic-script
    (markup #:baca-scratch-dynamic "mp")
    )

baca-mf-scratch = #(
    make-dynamic-script
    (markup #:baca-scratch-dynamic "mf")
    )

baca-f-scratch = #(
    make-dynamic-script
    (markup #:baca-scratch-dynamic "f")
    )

baca-ff-scratch = #(
    make-dynamic-script
    (markup #:baca-scratch-dynamic "ff")
    )

baca-fff-scratch = #(
    make-dynamic-script
    (markup #:baca-scratch-dynamic "fff")
    )

%%% SFORZANDO DYNAMICS %%%

baca-sff = #(make-dynamic-script "sff")
baca-sffp = #(make-dynamic-script "sffp")
baca-sffpp = #(make-dynamic-script "sffpp")
baca-sfpp = #(make-dynamic-script "sfpp")
baca-sffz = #(make-dynamic-script "sffz")
baca-sfffz = #(make-dynamic-script "sfffz")

baca-sfz-f = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "sfz"
            #:hspace -0.25
            #:normal-text "/"
            #:hspace -0.5
            #:dynamic "f"
            )
        )
    )

baca-sfz-p = #(
    make-dynamic-script
    (markup
        #:line (
            #:dynamic "sfz"
            #:hspace 0
            #:normal-text "/"
            #:hspace 0 
            #:dynamic "p"
            )
        )
    )

%%% SUBITO DYNAMICS %%%

baca-ppp-sub = 
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "ppp"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca-pp-sub = 
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "pp"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca-p-sub = 
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "p"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca-mp-sub = 
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "mp"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca-mf-sub =
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "mf"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca-f-sub =
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "f"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca-ff-sub =
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "ff"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

baca-fff-sub =
    #(make-dynamic-script
    (markup
        #:line (
            #:dynamic "fff"
            #:hspace 0.25
            #:normal-text "sub."
            )
        )
    )

%%% TEXT-ONLY DYNAMICS %%%

    %%% NOTE: Use ...
    %%%
    %%%       DynamicText.X-extent = #'(0 . 0)
    %%%
    %%% ... instead of ...
    %%%
    %%%       DynamicText.X-extent = ##f
    %%%
    %%% ... to avoid warnings in LilyPond log.

baca-appena-udibile = 
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
    #(make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:normal-text "appena udibile"
            )
        )
    )

baca-niente = #(
    make-dynamic-script
    (markup
        #:whiteout
        #:normal-text
        #:italic "niente"
        )
    )

%%% TEXTUAL DYNAMICS %%%

    %%% NOTE: Use ...
    %%%
    %%%       DynamicText.X-extent = #'(0 . 0)
    %%%
    %%% ... instead of ...
    %%%
    %%%       DynamicText.X-extent = ##f
    %%%
    %%% ... to avoid warnings in LilyPond log.

baca-p-sub-but-accents-continue-sffz = 
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
    #(make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:general-align Y -0.75 #:dynamic "p"
            #:normal-text "sub. (but accents continue"
            #:dynamic "sffz"
            #:hspace -0.5
            #:normal-text ")"
            )
        )
    )

baca-f-but-accents-sffz =
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
    #(make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:general-align Y -0.75 #:dynamic "f"
            #:hspace 0.25
            #:normal-text "(but accents"
            #:hspace 0.25
            #:dynamic "sffz"
            #:hspace -0.5
            #:normal-text ")"
            )
        )
    )

baca-f-sub-but-accents-continue-sffz =
    \tweak DynamicText.self-alignment-X #LEFT
    \tweak DynamicText.X-extent #'(0 . 0)
    #(make-dynamic-script
    (markup
        #:whiteout
        #:line (
            #:general-align Y -0.75 #:dynamic "f"
            #:hspace 0.25
            #:normal-text "sub. (but accents continue"
            #:dynamic "sffz"
            #:hspace -0.5
            #:normal-text ")"
            )
        )
    )
