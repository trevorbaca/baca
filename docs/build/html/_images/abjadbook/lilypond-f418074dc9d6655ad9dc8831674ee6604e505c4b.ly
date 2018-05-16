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
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)         %! HSS1:SPACING
                \override TextSpanner.staff-padding = #4                                 %! OC1
                \autoPageBreaksOff                                                       %! BMM1:BREAK
                \noBreak                                                                 %! BMM2:BREAK
                \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details  %! IC:BREAK
                #'((Y-offset . 4) (alignment-distances . (8)))                           %! IC:BREAK
                \time 3/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \bar ""                                                                  %! SM2:+SEGMENT:EMPTY_START_BAR
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                \pageBreak                                                               %! IC:BREAK
                s1 * 3/8
                - \tweak Y-extent ##f                                                    %! SM29:METRONOME_MARK_SPANNER
            %@% - \tweak bound-details.left.text \markup {                               %! SM27:REAPPLIED_METRONOME_MARK:SM36
            %@%     \fontsize                                                            %! SM27:REAPPLIED_METRONOME_MARK:SM36
            %@%         #-6                                                              %! SM27:REAPPLIED_METRONOME_MARK:SM36
            %@%         \general-align                                                   %! SM27:REAPPLIED_METRONOME_MARK:SM36
            %@%             #Y                                                           %! SM27:REAPPLIED_METRONOME_MARK:SM36
            %@%             #DOWN                                                        %! SM27:REAPPLIED_METRONOME_MARK:SM36
            %@%             \note-by-number                                              %! SM27:REAPPLIED_METRONOME_MARK:SM36
            %@%                 #2                                                       %! SM27:REAPPLIED_METRONOME_MARK:SM36
            %@%                 #0                                                       %! SM27:REAPPLIED_METRONOME_MARK:SM36
            %@%                 #1                                                       %! SM27:REAPPLIED_METRONOME_MARK:SM36
            %@%     \upright                                                             %! SM27:REAPPLIED_METRONOME_MARK:SM36
            %@%         {                                                                %! SM27:REAPPLIED_METRONOME_MARK:SM36
            %@%             =                                                            %! SM27:REAPPLIED_METRONOME_MARK:SM36
            %@%             90                                                           %! SM27:REAPPLIED_METRONOME_MARK:SM36
            %@%         }                                                                %! SM27:REAPPLIED_METRONOME_MARK:SM36
            %@%     \hspace                                                              %! SM27:REAPPLIED_METRONOME_MARK:SM36
            %@%         #1                                                               %! SM27:REAPPLIED_METRONOME_MARK:SM36
            %@%     }                                                                    %! SM27:REAPPLIED_METRONOME_MARK:SM36 %! SM29:METRONOME_MARK_SPANNER
                - \tweak bound-details.left.text \markup {                               %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                    \with-color                                                          %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                        #(x11-color 'green4)                                             %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                        {                                                                %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                            \fontsize                                                    %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                #-6                                                      %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                \general-align                                           %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                    #Y                                                   %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                    #DOWN                                                %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                    \note-by-number                                      %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                        #2                                               %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                        #0                                               %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                        #1                                               %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                            \upright                                                     %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                {                                                        %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                    =                                                    %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                    90                                                   %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                }                                                        %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                            \hspace                                                      %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                                #1                                                       %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                        }                                                                %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36
                    }                                                                    %! SM15:REAPPLIED_METRONOME_MARK_WITH_COLOR:SM36 %! SM29:METRONOME_MARK_SPANNER
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
                \set Score.proportionalNotationDuration = #(ly:make-moment 1 24)         %! HSS1:SPACING
                \noBreak                                                                 %! BMM2:BREAK
                \once \override Score.TimeSignature.color = #(x11-color 'DeepPink1)      %! SM6:REDUNDANT_TIME_SIGNATURE_COLOR:SM1
                s1 * 3/8
                \stopTextSpan                                                            %! SM29:METRONOME_MARK_SPANNER
                \revert TextSpanner.staff-padding                                        %! OC2
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