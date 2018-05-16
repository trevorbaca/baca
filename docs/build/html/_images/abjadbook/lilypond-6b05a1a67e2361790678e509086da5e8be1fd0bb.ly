\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "../../../../source/_stylesheets/string-trio-stylesheet.ily"

\score {
    \context Score = "Score"
    <<
        \context GlobalContext = "GlobalContext"
        <<
            \context GlobalSkips = "GlobalSkips"
            {
                
                % [GlobalSkips measure 1]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)         %! HSS1:SPACING
                \time 4/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 1/2
                
                % [GlobalSkips measure 2]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)         %! HSS1:SPACING
                \time 3/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 3/8
                
                % [GlobalSkips measure 3]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)         %! HSS1:SPACING
                \time 4/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 1/2
                
                % [GlobalSkips measure 4]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)         %! HSS1:SPACING
                \time 3/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 3/8
                \override Score.BarLine.transparent = ##f                                %! SM5
                \bar "|"                                                                 %! SM5
                
            }
        >>
        \context MusicContext = "MusicContext"
        <<
            \context Staff = "MusicStaff"
            {
                \context Voice = "MusicVoice"
                {
                    {
                        
                        % [MusicVoice measure 1]                                         %! SM4
                        \override TextSpanner.staff-padding = #4.5                       %! OC1
                        e'8
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
                        \startTextSpan                                                   %! PWC1
                        
                        d''8
                        
                        f'8
                        
                        e''8
                        ]
                    }
                    {
                        
                        % [MusicVoice measure 2]                                         %! SM4
                        g'8
                        [
                        
                        f''8
                        
                        e'8
                        ]
                    }
                    {
                        
                        % [MusicVoice measure 3]                                         %! SM4
                        d''8
                        \stopTextSpan                                                    %! PWC1
                        [
                        - \tweak Y-extent ##f                                            %! PWC1
                        - \tweak bound-details.left.text \markup {
                            \concat
                                {
                                    \whiteout
                                        \upright
                                            ord.
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
                                            pont.
                                }
                            }                                                            %! PWC1
                        \startTextSpan                                                   %! PWC1
                        
                        f'8
                        
                        e''8
                        
                        g'8
                        ]
                    }
                    {
                        
                        % [MusicVoice measure 4]                                         %! SM4
                        f''8
                        [
                        
                        e'8
                        
                        d''8
                        ]
                        \stopTextSpan                                                    %! PWC1
                        \revert TextSpanner.staff-padding                                %! OC2
                        
                    }
                }
            }
        >>
    >>
}