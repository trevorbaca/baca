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
                        e'8
                        [
                        - \tweak staff-padding #4
                        - \tweak Y-extent ##f
                        - \tweak bound-details.left.text \markup {
                            \concat
                                {
                                    \whiteout
                                        \upright
                                            "1/2 clt"
                                    \hspace
                                        #0.5
                                }
                            }
                        - \tweak dash-fraction 0.25
                        - \tweak dash-period 1.5
                        - \tweak bound-details.left-broken.text ##f
                        - \tweak bound-details.left.stencil-align-dir-y 0
                        - \tweak bound-details.right-broken.arrow ##f
                        - \tweak bound-details.right-broken.padding 0
                        - \tweak bound-details.right-broken.text ##f
                        - \tweak bound-details.right.padding 1.25
                        - \tweak bound-details.right.text \markup {
                            \draw-line
                                #'(0 . -1)
                            }
                        \startTextSpan
                        - \tweak staff-padding #6.5
                        - \tweak Y-extent ##f
                        - \tweak bound-details.left.text \markup {
                            \concat
                                {
                                    \whiteout
                                        \upright
                                            damp
                                    \hspace
                                        #0.5
                                }
                            }
                        - \tweak dash-fraction 0.25
                        - \tweak dash-period 1.5
                        - \tweak bound-details.left-broken.text ##f
                        - \tweak bound-details.left.stencil-align-dir-y 0
                        - \tweak bound-details.right-broken.arrow ##f
                        - \tweak bound-details.right-broken.padding 0
                        - \tweak bound-details.right-broken.text ##f
                        - \tweak bound-details.right.padding 1.25
                        - \tweak bound-details.right.text \markup {
                            \draw-line
                                #'(0 . -1)
                            }
                        \startTextSpanOne
                        
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
                        \stopTextSpan
                        [
                        
                        f'8
                        
                        e''8
                        
                        g'8
                        ]
                    }
                    {
                        
                        % [MusicVoice measure 4]                                         %! SM4
                        f''8
                        \stopTextSpanOne
                        [
                        
                        e'8
                        
                        d''8
                        ]
                        
                    }
                }
            }
        >>
    >>
}