\version "2.19.0"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "../../../../source/_stylesheets/string-trio-stylesheet.ily"

\layout {
    indent = #0
}

\score {
    \context Score = "Score"
    <<
        \context GlobalContext = "GlobalContext"
        <<
            \context GlobalSkips = "GlobalSkips"
            {
                
                % [GlobalSkips measure 1]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 25)         %! HSS1:SPACING
                \autoPageBreaksOff                                                       %! BMM1:BREAK
                \noBreak                                                                 %! BMM2:BREAK
                \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details  %! IC:BREAK
                #'((Y-offset . 4) (alignment-distances . (8)))                           %! IC:BREAK
                \time 3/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                \pageBreak                                                               %! IC:BREAK
                s1 * 3/8
                - \tweak Y-extent ##f                                                    %! SM29:METRONOME_MARK_SPANNER
            %@% - \tweak bound-details.left.text \markup {                               %! SM27:EXPLICIT_METRONOME_MARK
            %@%     \fontsize                                                            %! SM27:EXPLICIT_METRONOME_MARK
            %@%         #-6                                                              %! SM27:EXPLICIT_METRONOME_MARK
            %@%         \general-align                                                   %! SM27:EXPLICIT_METRONOME_MARK
            %@%             #Y                                                           %! SM27:EXPLICIT_METRONOME_MARK
            %@%             #DOWN                                                        %! SM27:EXPLICIT_METRONOME_MARK
            %@%             \note-by-number                                              %! SM27:EXPLICIT_METRONOME_MARK
            %@%                 #2                                                       %! SM27:EXPLICIT_METRONOME_MARK
            %@%                 #0                                                       %! SM27:EXPLICIT_METRONOME_MARK
            %@%                 #1                                                       %! SM27:EXPLICIT_METRONOME_MARK
            %@%     \upright                                                             %! SM27:EXPLICIT_METRONOME_MARK
            %@%         {                                                                %! SM27:EXPLICIT_METRONOME_MARK
            %@%             =                                                            %! SM27:EXPLICIT_METRONOME_MARK
            %@%             112                                                          %! SM27:EXPLICIT_METRONOME_MARK
            %@%         }                                                                %! SM27:EXPLICIT_METRONOME_MARK
            %@%     \hspace                                                              %! SM27:EXPLICIT_METRONOME_MARK
            %@%         #1                                                               %! SM27:EXPLICIT_METRONOME_MARK
            %@%     }                                                                    %! SM27:EXPLICIT_METRONOME_MARK %! SM29:METRONOME_MARK_SPANNER
                - \tweak bound-details.left.text \markup {                               %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                    \with-color                                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                        #(x11-color 'blue)                                               %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                        {                                                                %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                            \fontsize                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                #-6                                                      %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                \general-align                                           %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                    #Y                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                    #DOWN                                                %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                    \note-by-number                                      %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                        #2                                               %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                        #0                                               %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                        #1                                               %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                            \upright                                                     %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                {                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                    =                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                    112                                                  %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                }                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                            \hspace                                                      %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                                #1                                                       %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                        }                                                                %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR
                    }                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR %! SM29:METRONOME_MARK_SPANNER
                - \tweak dash-period 0                                                   %! SM29:METRONOME_MARK_SPANNER
                - \tweak bound-details.left.stencil-align-dir-y #center                  %! SM29:METRONOME_MARK_SPANNER
                - \tweak bound-details.right-broken.padding 0                            %! SM29:METRONOME_MARK_SPANNER
                - \tweak bound-details.right-broken.text ##f                             %! SM29:METRONOME_MARK_SPANNER
                - \tweak bound-details.right.padding 0                                   %! SM29:METRONOME_MARK_SPANNER
                - \tweak bound-details.right.stencil-align-dir-y #center                 %! SM29:METRONOME_MARK_SPANNER
                - \tweak bound-details.left-broken.text ##f                              %! SM29:METRONOME_MARK_SPANNER
                \startTextSpan                                                           %! SM29:METRONOME_MARK_SPANNER
                
                % [GlobalSkips measure 2]                                                %! SM4
                \newSpacingSection                                                       %! HSS1:SPACING
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 25)         %! HSS1:SPACING
                \noBreak                                                                 %! BMM2:BREAK
                \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)      %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                s1 * 3/8
                \stopTextSpan                                                            %! SM29:METRONOME_MARK_SPANNER
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
                    
                    % [MusicVoice measure 1]                                             %! SM4
                    c'4.
                    
                    % [MusicVoice measure 2]                                             %! SM4
                    c'4.
                    
                }
            }
        >>
    >>
}