%%% BCP SPANNER %%%

bacaStartTextSpanBCP = #(
    make-music 'TextSpanEvent 'span-direction START 'spanner-id "BCP"
    )

bacaStopTextSpanBCP = #(
    make-music 'TextSpanEvent 'span-direction STOP 'spanner-id "BCP"
    )

#(define-markup-command
    (baca-bcp-left layout props n d) (number? number?)
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

%%% METRONOME MARK SPANNER %%%

baca-metronome-mark-spanner-colored-left-text = #(
    define-music-function
    (parser location log dots stem string color music)
    (number? number? number? string? symbol? ly:music?)
    #{
    \tweak bound-details.left.text \markup \concat {
        \with-color #(x11-color color)
        \abjad-metronome-mark-markup #log #dots #stem #string
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
    \tweak bound-details.left.text \markup \concat {
        \abjad-metronome-mark-markup #log #dots #stem #string
        \hspace #0.5
        }
    $music
    #}
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
