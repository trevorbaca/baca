\version "2.19.0"
\language "english"

\include "default.ily"
\include "rhythm-maker-docs.ily"

\score {
    \new Score
    <<
        \new GlobalContext
        {
            {   % measure
                \time 11/8
                s1 * 11/8
            }   % measure
        }
        \new Staff
        <<
            \context Voice = "Voice 1"
            {
                \voiceOne
                {
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TextScript.staff-padding = #6                          %! OC1
                        \override TupletBracket.staff-padding = #5                       %! OC1
                        r8
                        c'16
                        [
                        d'16
                        ]
                        bf'4
                        ~
                        bf'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 9/10 {
                        \override TextSpanner.staff-padding = #6                         %! OC1
                        fs''16
                        [
                        - \tweak Y-extent ##f                                            %! PWC1
                        - \tweak bound-details.left.text \markup {
                            \concat
                                {
                                    \whiteout
                                        \upright
                                            pont.
                                    \hspace
                                        #0.5
                                }
                            }                                                            %! PWC1
                        - \tweak arrow-width 0.25                                        %! PWC1
                        - \tweak dash-fraction 0.25                                      %! PWC1
                        - \tweak dash-period 1.5                                         %! PWC1
                        - \tweak bound-details.left-broken.text ##f                      %! PWC1
                        - \tweak bound-details.left.stencil-align-dir-y #center          %! PWC1
                        - \tweak bound-details.right.arrow ##t                           %! PWC1
                        - \tweak bound-details.right-broken.arrow ##f                    %! PWC1
                        - \tweak bound-details.right-broken.padding 0                    %! PWC1
                        - \tweak bound-details.right-broken.text ##f                     %! PWC1
                        - \tweak bound-details.right.padding 0.5                         %! PWC1
                        - \tweak bound-details.right.stencil-align-dir-y #center         %! PWC1
                        - \tweak bound-details.right.text \markup {
                            \concat
                                {
                                    \hspace
                                        #0.0
                                    \whiteout
                                        \upright
                                            ord.
                                }
                            }                                                            %! PWC1
                        \startTextSpan                                                   %! PWC1
                        e''16
                        ]
                        ef''4
                        ~
                        ef''16
                        r16
                        af''16
                        [
                        g''16
                        ]
                        \stopTextSpan                                                    %! PWC1
                        \revert TextSpanner.staff-padding                                %! OC2
                    }
                    \times 4/5 {
                        a'16
                        r4
                        \revert TextScript.staff-padding                                 %! OC2
                        \revert TupletBracket.staff-padding                              %! OC2
                    }
                }
            }
        >>
    >>
}