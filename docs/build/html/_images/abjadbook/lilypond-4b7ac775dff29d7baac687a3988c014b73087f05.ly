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
                \time 4/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 1/2
                - \tweak Y-extent ##f                                                    %! SM29:METRONOME_MARK_SPANNER
            %@% - \tweak bound-details.left.text \markup {                               %! SM27:EXPLICIT_METRONOME_MARK:SM30
            %@%     \fontsize                                                            %! SM27:EXPLICIT_METRONOME_MARK:SM30
            %@%         #-6                                                              %! SM27:EXPLICIT_METRONOME_MARK:SM30
            %@%         \general-align                                                   %! SM27:EXPLICIT_METRONOME_MARK:SM30
            %@%             #Y                                                           %! SM27:EXPLICIT_METRONOME_MARK:SM30
            %@%             #DOWN                                                        %! SM27:EXPLICIT_METRONOME_MARK:SM30
            %@%             \note-by-number                                              %! SM27:EXPLICIT_METRONOME_MARK:SM30
            %@%                 #2                                                       %! SM27:EXPLICIT_METRONOME_MARK:SM30
            %@%                 #0                                                       %! SM27:EXPLICIT_METRONOME_MARK:SM30
            %@%                 #1                                                       %! SM27:EXPLICIT_METRONOME_MARK:SM30
            %@%     \upright                                                             %! SM27:EXPLICIT_METRONOME_MARK:SM30
            %@%         {                                                                %! SM27:EXPLICIT_METRONOME_MARK:SM30
            %@%             =                                                            %! SM27:EXPLICIT_METRONOME_MARK:SM30
            %@%             90                                                           %! SM27:EXPLICIT_METRONOME_MARK:SM30
            %@%         }                                                                %! SM27:EXPLICIT_METRONOME_MARK:SM30
            %@%     \hspace                                                              %! SM27:EXPLICIT_METRONOME_MARK:SM30
            %@%         #1                                                               %! SM27:EXPLICIT_METRONOME_MARK:SM30
            %@%     }                                                                    %! SM27:EXPLICIT_METRONOME_MARK:SM30 %! SM29:METRONOME_MARK_SPANNER
                - \tweak bound-details.left.text \markup {                               %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                    \with-color                                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                        #(x11-color 'blue)                                               %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                        {                                                                %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                            \fontsize                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                #-6                                                      %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                \general-align                                           %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                    #Y                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                    #DOWN                                                %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                    \note-by-number                                      %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                        #2                                               %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                        #0                                               %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                        #1                                               %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                            \upright                                                     %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                {                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                    =                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                    90                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                }                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                            \hspace                                                      %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                #1                                                       %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                        }                                                                %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                    }                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30 %! SM29:METRONOME_MARK_SPANNER
                - \tweak dash-period 0                                                   %! SM29:METRONOME_MARK_SPANNER
                - \tweak bound-details.left.stencil-align-dir-y #center                  %! SM29:METRONOME_MARK_SPANNER
                - \tweak bound-details.right-broken.padding 0                            %! SM29:METRONOME_MARK_SPANNER
                - \tweak bound-details.right-broken.text ##f                             %! SM29:METRONOME_MARK_SPANNER
                - \tweak bound-details.right.padding 0                                   %! SM29:METRONOME_MARK_SPANNER
                - \tweak bound-details.right.stencil-align-dir-y #center                 %! SM29:METRONOME_MARK_SPANNER
                - \tweak bound-details.left-broken.text ##f                              %! SM29:METRONOME_MARK_SPANNER
                \startTextSpan                                                           %! SM29:METRONOME_MARK_SPANNER
                
                % [GlobalSkips measure 2]                                                %! SM4
                \time 3/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 3/8
                
                % [GlobalSkips measure 3]                                                %! SM4
                \time 4/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                s1 * 1/2
                
                % [GlobalSkips measure 4]                                                %! SM4
                \time 3/8                                                                %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                \once \override Score.TimeSignature.color = #(x11-color 'blue)           %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
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
                    {
                        
                        % [MusicVoice measure 1]                                         %! SM4
                        c'8
                        [
                        
                        c'8
                        
                        c'8
                        
                        c'8
                        ]
                    }
                    {
                        
                        % [MusicVoice measure 2]                                         %! SM4
                        c'8
                        [
                        
                        c'8
                        
                        c'8
                        ]
                    }
                    {
                        
                        % [MusicVoice measure 3]                                         %! SM4
                        c'8
                        [
                        
                        c'8
                        
                        c'8
                        
                        c'8
                        ]
                    }
                    {
                        
                        % [MusicVoice measure 4]                                         %! SM4
                        c'8
                        [
                        
                        c'8
                        
                        c'8
                        ]
                        
                    }
                }
            }
        >>
    >>
}