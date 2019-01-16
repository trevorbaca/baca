%%% GLOBALS %%%

baca-lower-annotation-layer = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \tweak extra-offset #'(0 . 10)
    $music
    #}
    )

baca-upper-annotation-layer = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \tweak extra-offset #'(0 . 13)
    $music
    #}
    )

%%% BCP SPANNER %%%

bacaStartTextSpanBCP = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "BCP"
    )

bacaStopTextSpanBCP = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "BCP"
    )

#(define-markup-command
    (baca-bcp-left layout props n d)
    (number? number?)
    (interpret-markup layout props
    #{
    \markup \concat {
        \upright \fraction #(number->string n) #(number->string d)
        \hspace #0.5
        }
    #})
    )

baca-bcp-spanner-left-text = #(
    define-music-function
    (parser location n d music)
    (number? number? ly:music?)
    #{
    \tweak bound-details.left.text \markup \baca-bcp-left #n #d
    $music
    #}
    )

#(define-markup-command
    (baca-bcp-right layout props n d)
    (number? number?)
    (interpret-markup layout props
    #{
    \markup \upright \fraction #(number->string n) #(number->string d)
    #})
    )

baca-bcp-spanner-right-text = #(
    define-music-function
    (parser location n d music)
    (number? number? ly:music?)
    #{
    \tweak bound-details.right.text \markup \baca-bcp-right #n #d
    $music
    #}
    ) 

%%% BOW SPEED SPANNER %%%

bacaStartTextSpanBowSpeed = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "BowSpeed"
    )

bacaStopTextSpanBowSpeed = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "BowSpeed"
    )

%%% CLB SPANNER %%%

bacaStartTextSpanCLB = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "CLB"
    )

bacaStopTextSpanCLB = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "CLB"
    )

%%% CLOCK TIME SPANNER %%%

bacaStartTextSpanCT = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "CT"
    )

bacaStopTextSpanCT = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "CT"
    )

#(define-markup-command
    (baca-ct-left-markup layout props ct)
    (string?)
    (interpret-markup layout props
        #{
        \markup
        \with-color #(x11-color 'ForestGreen)
        \fontsize #-3
        \upright
        \concat { #ct \hspace #0.5 }
        #}
        )
    )

baca-ct-left-text-tweak = #(
    define-music-function
    (parser location left music)
    (string? ly:music?)
    #{
    \tweak bound-details.left.text \markup \baca-ct-left-markup #left
    $music
    #}
    )

#(define-markup-command
    (baca-ct-right-markup layout props ct)
    (string?)
    (interpret-markup layout props
        #{
        \markup 
        \with-color #(x11-color 'ForestGreen)
        \fontsize #-3
        \upright
        #ct
        #}
        )
    )

baca-ct-right-text-tweak = #(
    define-music-function
    (parser location right music)
    (string? ly:music?)
    #{
    \tweak bound-details.right.text \markup \baca-ct-right-markup #right
    $music
    #}
    ) 

baca-start-ct-left-only = #(
    define-music-function
    (parser location left music)
    (string? ly:music?)
    #{
    - \abjad-invisible-line
    - \baca-ct-left-text-tweak #left
    - \baca-upper-annotation-layer
    $music
    #}
    )

baca-start-ct-both = #(
    define-music-function
    (parser location left right music)
    (string? string? ly:music?)
    #{
    - \abjad-invisible-line
    - \baca-ct-left-text-tweak #left
    - \baca-ct-right-text-tweak #right
    - \baca-upper-annotation-layer
    $music
    #}
    )

%%% CIRCLE BOW SPANNER %%%

bacaStartTextSpanCircleBow = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "CircleBow"
    )

bacaStopTextSpanCircleBow = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "CircleBow"
    )

%%% DAMP SPANNER %%%

bacaStartTextSpanDamp = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "Damp"
    )

bacaStopTextSpanDamp = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "Damp"
    )

%%% HALF CLT SPANNER %%%

bacaStartTextSpanHalfCLT = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "HalfCLT"
    )

bacaStopTextSpanHalfCLT = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "HalfCLT"
    )

%%% LOCAL MEASURE INDEX SPANNER %%%

bacaStartTextSpanLMI = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "LMI"
    )

bacaStopTextSpanLMI = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "LMI"
    )

#(define-markup-command
    (baca-lmi-left-markup layout props lmi)
    (string?)
    (interpret-markup layout props
        #{
        \markup
        \with-color #(x11-color 'DarkCyan)
        \fontsize #-3
        \upright
        \concat { #lmi \hspace #0.5 }
        #}
        )
    )

baca-lmi-left-text-tweak = #(
    define-music-function
    (parser location left music)
    (string? ly:music?)
    #{
    \tweak bound-details.left.text \markup \baca-lmi-left-markup #left
    $music
    #}
    )

#(define-markup-command
    (baca-lmi-right-markup layout props lmi)
    (string?)
    (interpret-markup layout props
        #{
        \markup 
        \with-color #(x11-color 'DarkCyan)
        \fontsize #-3
        \upright
        #lmi
        #}
        )
    )

baca-lmi-right-text-tweak = #(
    define-music-function
    (parser location right music)
    (string? ly:music?)
    #{
    \tweak bound-details.right.text \markup \baca-lmi-right-markup #right
    $music
    #}
    ) 

baca-start-lmi-left-only = #(
    define-music-function
    (parser location left music)
    (string? ly:music?)
    #{
    - \abjad-invisible-line
    - \baca-lmi-left-text-tweak #left
    - \baca-lower-annotation-layer
    $music
    #}
    )

baca-start-lmi-both = #(
    define-music-function
    (parser location left right music)
    (string? string? ly:music?)
    #{
    - \abjad-invisible-line
    - \baca-lmi-left-text-tweak #left
    - \baca-lmi-right-text-tweak #right
    - \baca-lower-annotation-layer
    $music
    #}
    )

%%% LOCAL MEASURE NUMBER SPANNER %%%

bacaStartTextSpanLMN = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "LMN"
    )

bacaStopTextSpanLMN = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "LMN"
    )

#(define-markup-command
    (baca-lmn-left-markup layout props lmn)
    (string?)
    (interpret-markup layout props
        #{
        \markup
        \with-color #(x11-color 'DarkCyan)
        \fontsize #-3
        \upright
        \concat { #lmn \hspace #0.5 }
        #}
        )
    )

baca-lmn-left-text-tweak = #(
    define-music-function
    (parser location left music)
    (string? ly:music?)
    #{
    \tweak bound-details.left.text \markup \baca-lmn-left-markup #left
    $music
    #}
    )

#(define-markup-command
    (baca-lmn-right-markup layout props lmn)
    (string?)
    (interpret-markup layout props
        #{
        \markup 
        \with-color #(x11-color 'DarkCyan)
        \fontsize #-3
        \upright
        #lmn
        #}
        )
    )

baca-lmn-right-text-tweak = #(
    define-music-function
    (parser location right music)
    (string? ly:music?)
    #{
    \tweak bound-details.right.text \markup \baca-lmn-right-markup #right
    $music
    #}
    ) 

baca-start-lmn-left-only = #(
    define-music-function
    (parser location left music)
    (string? ly:music?)
    #{
    - \abjad-invisible-line
    - \baca-lmn-left-text-tweak #left
    - \baca-lower-annotation-layer
    $music
    #}
    )

baca-start-lmn-both = #(
    define-music-function
    (parser location left right music)
    (string? string? ly:music?)
    #{
    - \abjad-invisible-line
    - \baca-lmn-left-text-tweak #left
    - \baca-lmn-right-text-tweak #right
    - \baca-lower-annotation-layer
    $music
    #}
    )

%%% MATERIAL ANNOTATION SPANNER %%%

bacaStartTextSpanMA = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "MA"
    )

bacaStopTextSpanMA = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "MA"
    )

%%% MEASURE NUMBER SPANNER %%%

bacaStartTextSpanMN = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "MN"
    )

bacaStopTextSpanMN = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "MN"
    )

#(define-markup-command
    (baca-mn-left-markup layout props mn)
    (string?)
    (interpret-markup layout props
        #{
        \markup
        \with-color #(x11-color 'DarkOrchid)
        \fontsize #-3
        \upright
        \concat { #mn \hspace #0.5 }
        #}
        )
    )

baca-mn-left-text-tweak = #(
    define-music-function
    (parser location left music)
    (string? ly:music?)
    #{
    \tweak bound-details.left.text \markup \baca-mn-left-markup #left
    $music
    #}
    )

#(define-markup-command
    (baca-mn-right-markup layout props mn)
    (string?)
    (interpret-markup layout props
        #{
        \markup 
        \with-color #(x11-color 'DarkOrchid)
        \fontsize #-3
        \upright
        #mn
        #}
        )
    )

baca-mn-right-text-tweak = #(
    define-music-function
    (parser location right music)
    (string? ly:music?)
    #{
    \tweak bound-details.right.text \markup \baca-mn-right-markup #right
    $music
    #}
    ) 

baca-start-mn-left-only = #(
    define-music-function
    (parser location left music)
    (string? ly:music?)
    #{
    - \abjad-invisible-line
    - \baca-mn-left-text-tweak #left
    - \baca-lower-annotation-layer
    $music
    #}
    )

baca-start-mn-both = #(
    define-music-function
    (parser location left right music)
    (string? string? ly:music?)
    #{
    - \abjad-invisible-line
    - \baca-mn-left-text-tweak #left
    - \baca-mn-right-text-tweak #right
    - \baca-lower-annotation-layer
    $music
    #}
    )

%%% METRONOME MARK SPANNER %%%

bacaStartTextSpanMM = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "MM"
    )

bacaStopTextSpanMM = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "MM"
    )

baca-metronome-mark-spanner-layer = #(
    define-music-function
    (parser location music)
    (ly:music?)
    #{
    \tweak extra-offset #'(0 . 6)
    $music
    #}
    )

baca-metronome-mark-spanner-colored-left-markup = #(
    define-music-function
    (parser location markup color music)
    (markup? symbol? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \with-color #(x11-color color)
        #markup
        \hspace #0.5
        }
    $music
    #}
    )

baca-metronome-mark-spanner-colored-left-text = #(
    define-music-function
    (parser location log dots stem string color music)
    (number? number? number? string? symbol? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \with-color #(x11-color color)
        \abjad-metronome-mark-markup #log #dots #stem #string
        \hspace #0.5
        }
    $music
    #}
    )

baca-metronome-mark-spanner-left-markup = #(
    define-music-function
    (parser location markup music)
    (markup? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        #markup
        \hspace #0.5
        }
    $music
    #}
    )

baca-metronome-mark-spanner-left-text = #(
    define-music-function
    (parser location log dots stem string music)
    (number? number? number? string? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \abjad-metronome-mark-markup #log #dots #stem #string
        \hspace #0.5
        }
    $music
    #}
    )

baca-bracketed-metric-modulation = #(
    define-music-function
    (parser location
        mm-length mm-dots mm-stem mm-value
        lhs-length lhs-dots rhs-length rhs-dots
        modulation-scale music)
    (number? number? number? string?
        number? number? number? number?
        pair? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \abjad-bracketed-metric-modulation
            #mm-length #mm-dots #mm-stem #mm-value
            #lhs-length #lhs-dots #rhs-length #rhs-dots
            #modulation-scale
        \hspace #0.5
        }
    $music
    #}
    )

baca-colored-bracketed-metric-modulation = #(
    define-music-function
    (parser location
        mm-length mm-dots mm-stem mm-value
        lhs-length lhs-dots rhs-length rhs-dots
        modulation-scale color music)
    (number? number? number? string?
        number? number? number? number?
        pair? symbol? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \with-color #(x11-color color)
        \abjad-bracketed-metric-modulation
            #mm-length #mm-dots #mm-stem #mm-value
            #lhs-length #lhs-dots #rhs-length #rhs-dots
            #modulation-scale
        \hspace #0.5
        }
    $music
    #}
    )

baca-bracketed-metric-modulation-tuplet-lhs = #(
    define-music-function
    (parser location
        mm-length mm-dots mm-stem mm-value
        tuplet-length tuplet-dots tuplet-n tuplet-d
        note-length note-dots
        modulation-scale music)
    (number? number? number? string?
        number? number? number? number?
        number? number?
        pair? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \abjad-bracketed-metric-modulation-tuplet-lhs
            #mm-length #mm-dots #mm-stem #mm-value
            #tuplet-length #tuplet-dots #tuplet-n #tuplet-d
            #note-length #note-dots
            #modulation-scale
        \hspace #0.5
        }
    $music
    #}
    )

baca-colored-bracketed-metric-modulation-tuplet-lhs = #(
    define-music-function
    (parser location
        mm-length mm-dots mm-stem mm-value
        tuplet-length tuplet-dots tuplet-n tuplet-d
        note-length note-dots
        modulation-scale color music)
    (number? number? number? string?
        number? number? number? number?
        number? number?
        pair? symbol? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \abjad-bracketed-metric-modulation-tuplet-lhs
            #mm-length #mm-dots #mm-stem #mm-value
            #tuplet-length #tuplet-dots #tuplet-n #tuplet-d
            #note-length #note-dots
            #modulation-scale
        \hspace #0.5
        }
    $music
    #}
    )

baca-bracketed-metric-modulation-tuplet-rhs = #(
    define-music-function
    (parser location
        mm-length mm-dots mm-stem mm-value
        note-length note-dots
        tuplet-length tuplet-dots tuplet-n tuplet-d
        modulation-scale music)
    (number? number? number? string?
        number? number?
        number? number? number? number?
        pair? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \abjad-bracketed-metric-modulation-tuplet-rhs
            #mm-length #mm-dots #mm-stem #mm-value
            #note-length #note-dots
            #tuplet-length #tuplet-dots #tuplet-n #tuplet-d
            #modulation-scale
        \hspace #0.5
        }
    $music
    #}
    )

baca-colored-bracketed-metric-modulation-tuplet-rhs = #(
    define-music-function
    (parser location
        mm-length mm-dots mm-stem mm-value
        note-length note-dots
        tuplet-length tuplet-dots tuplet-n tuplet-d
        modulation-scale color music)
    (number? number? number? string?
        number? number?
        number? number? number? number?
        pair? symbol? ly:music?)
    #{
    \baca-metronome-mark-spanner-layer
    \tweak bound-details.left.text \markup \concat {
        \with-color #(x11-color color)
        \abjad-bracketed-metric-modulation-tuplet-rhs
            #mm-length #mm-dots #mm-stem #mm-value
            #note-length #note-dots
            #tuplet-length #tuplet-dots #tuplet-n #tuplet-d
            #modulation-scale
        \hspace #0.5
        }
    $music
    #}
    )

%%% PITCH ANNOTATION SPANNER %%%

bacaStartTextSpanPA = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "PA"
    )

bacaStopTextSpanPA = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "PA"
    )

%%% SCP SPANNER %%%

bacaStartTextSpanSCP = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "SCP"
    )

bacaStopTextSpanSCP = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "SCP"
    )

%%% SPACING MARKUP SPANNER %%%

bacaStartTextSpanSPM = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "SPM"
    )

bacaStopTextSpanSPM = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "SPM"
    )

#(define-markup-command
    (baca-spm-left-markup layout props spm)
    (string?)
    (interpret-markup layout props
        #{
        \markup
        \with-color #(x11-color 'ForestGreen)
        \fontsize #-3
        \upright
        \concat { #spm \hspace #0.5 }
        #}
        )
    )

baca-spm-left-text-tweak = #(
    define-music-function
    (parser location left music)
    (string? ly:music?)
    #{
    \tweak bound-details.left.text \markup \baca-spm-left-markup #left
    $music
    #}
    )

#(define-markup-command
    (baca-spm-right-markup layout props spm)
    (string?)
    (interpret-markup layout props
        #{
        \markup 
        \with-color #(x11-color 'ForestGreen)
        \fontsize #-3
        \upright
        #spm
        #}
        )
    )

baca-spm-right-text-tweak = #(
    define-music-function
    (parser location right music)
    (string? ly:music?)
    #{
    \tweak bound-details.right.text \markup \baca-spm-right-markup #right
    $music
    #}
    ) 

baca-start-spm-left-only = #(
    define-music-function
    (parser location left music)
    (string? ly:music?)
    #{
    - \abjad-invisible-line
    - \baca-spm-left-text-tweak #left
    - \baca-upper-annotation-layer
    $music
    #}
    )

baca-start-spm-both = #(
    define-music-function
    (parser location left right music)
    (string? string? ly:music?)
    #{
    - \abjad-invisible-line
    - \baca-spm-left-text-tweak #left
    - \baca-spm-right-text-tweak #right
    - \baca-upper-annotation-layer
    $music
    #}
    )

%%% SPAZZOLATO SPANNER %%%

bacaStartTextSpanSpazzolato = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "Spazzolato"
    )

bacaStopTextSpanSpazzolato = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "Spazzolato"
    )

%%% STAGE NUMBER SPANNER %%%

bacaStartTextSpanSNM = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "SNM"
    )

bacaStopTextSpanSNM = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "SNM"
    )

#(define-markup-command
    (baca-snm-left-markup layout props snm)
    (string?)
    (interpret-markup layout props
        #{
        \markup
        %%%\with-color #(x11-color 'red)
        \fontsize #-3
        \upright
        \concat { #snm \hspace #-0.25 }
        #}
        )
    )

#(define-markup-command
    (baca-snm-colored-left-markup layout props snm color)
    (string? color?)
    (interpret-markup layout props
        #{
        \markup
        \with-color #color
        \fontsize #-3
        \upright
        \concat { #snm \hspace #-0.25 }
        #}
        )
    )

baca-snm-left-text-tweak = #(
    define-music-function
    (parser location left music)
    (string? ly:music?)
    #{
    \tweak bound-details.left.text \markup \baca-snm-left-markup #left
    $music
    #}
    )

baca-snm-colored-left-text-tweak = #(
    define-music-function
    (parser location left color music)
    (string? color? ly:music?)
    #{
    \tweak bound-details.left.text \markup
        \baca-snm-colored-left-markup #left #color
    $music
    #}
    )

#(define-markup-command
    (baca-snm-right-markup layout props snm)
    (string?)
    (interpret-markup layout props
        #{
        \markup 
        \with-color #(x11-color 'red)
        \fontsize #-3
        \upright
        #snm
        #}
        )
    )

baca-snm-right-text-tweak = #(
    define-music-function
    (parser location right music)
    (string? ly:music?)
    #{
    \tweak bound-details.right.text \markup \baca-snm-right-markup #right
    $music
    #}
    ) 

baca-start-snm-left-only = #(
    define-music-function
    (parser location left music)
    (string? ly:music?)
    #{
    - \abjad-solid-line-with-hook
    - \baca-snm-left-text-tweak #left
    - \baca-upper-annotation-layer
    - \tweak bound-details.right.padding 1.25
    %%%- \tweak color #red
    $music
    #}
    )

baca-start-snm-colored-left-only = #(
    define-music-function
    (parser location left color music)
    (string? color? ly:music?)
    #{
    - \abjad-solid-line-with-hook
    %%%- \baca-snm-left-text-tweak #left
    - \baca-snm-colored-left-text-tweak #left #color
    - \baca-upper-annotation-layer
    - \tweak bound-details.right.padding 1.25
    - \tweak color #color
    $music
    #}
    )

baca-start-snm-both = #(
    define-music-function
    (parser location left right music)
    (string? string? ly:music?)
    #{
    - \abjad-solid-line-with-hook
    - \baca-snm-left-text-tweak #left
    - \baca-snm-right-text-tweak #right
    - \baca-upper-annotation-layer
    - \tweak bound-details.right.padding 0
    - \tweak bound-details.right.stencil-align-dir-y #center
    %%%- \tweak color #red
    $music
    #}
    )

%%% STRING NUMBER SPANNER %%%

bacaStartTextSpanStringNumber = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "StringNumber"
    )

bacaStopTextSpanStringNumber = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "StringNumber"
    )

%%% TEXT SPANNER %%%

baca-text-spanner-left-markup = #(
    define-music-function
    (parser location markup music)
    (markup? ly:music?)
    #{
    \tweak bound-details.left.text \markup \concat {
        \upright #markup \hspace #0.5
        }
    $music
    #}
    )

baca-text-spanner-left-text = #(
    define-music-function
    (parser location string music)
    (string? ly:music?)
    #{
    \tweak bound-details.left.text \markup \concat {
        \upright #string \hspace #0.5
        }
    $music
    #}
    )

baca-text-spanner-right-markup = #(
    define-music-function
    (parser location markup music)
    (markup? ly:music?)
    #{
    \tweak bound-details.right.text \markup \upright #markup
    $music
    #}
    )

baca-text-spanner-right-text = #(
    define-music-function
    (parser location string music)
    (string? ly:music?)
    #{
    \tweak bound-details.right.text \markup \upright #string
    $music
    #}
    )

%%% VIBRATO SPANNER %%%

bacaStartTextSpanVibrato = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "Vibrato"
    )

bacaStopTextSpanVibrato = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "Vibrato"
    )
