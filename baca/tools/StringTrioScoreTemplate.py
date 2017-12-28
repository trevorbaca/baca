import abjad
import baca
from .ScoreTemplate import ScoreTemplate


class StringTrioScoreTemplate(ScoreTemplate):
    r'''String trio score template.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=79)
            \context Score = "Score" <<
                \tag violin.viola.cello
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        % GlobalSkips [measure 1]                                          %! SM4
                        \time 4/8                                                          %! SM1
                        \bar ""                                                            %! EMPTY_START_BAR:SM2
                        s1 * 1/2
                        ^ \markup {                                                        %! STAGE_NUMBER_MARKUP:SM3
                            \fontsize                                                      %! STAGE_NUMBER_MARKUP:SM3
                                #-3                                                        %! STAGE_NUMBER_MARKUP:SM3
                                \with-color                                                %! STAGE_NUMBER_MARKUP:SM3
                                    #(x11-color 'DarkCyan)                                 %! STAGE_NUMBER_MARKUP:SM3
                                    [1]                                                    %! STAGE_NUMBER_MARKUP:SM3
                            }                                                              %! STAGE_NUMBER_MARKUP:SM3
            <BLANKLINE>
                        % GlobalSkips [measure 2]                                          %! SM4
                        \time 3/8                                                          %! SM1
                        s1 * 3/8
            <BLANKLINE>
                        % GlobalSkips [measure 3]                                          %! SM4
                        \time 4/8                                                          %! SM1
                        s1 * 1/2
            <BLANKLINE>
                        % GlobalSkips [measure 4]                                          %! SM4
                        \time 3/8                                                          %! SM1
                        s1 * 3/8
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context StringSectionStaffGroup = "String Section Staff Group" <<
                        \tag violin
                        \context ViolinMusicStaff = "ViolinMusicStaff" {
                            \context ViolinMusicVoice = "ViolinMusicVoice" {
            <BLANKLINE>
                                % ViolinMusicVoice [measure 1]                             %! SM4
                                \set ViolinMusicStaff.instrumentName = \markup {           %! DEFAULT_INSTRUMENT
                                    \hcenter-in                                            %! DEFAULT_INSTRUMENT
                                        #10                                                %! DEFAULT_INSTRUMENT
                                        Violin                                             %! DEFAULT_INSTRUMENT
                                    }                                                      %! DEFAULT_INSTRUMENT
                                \set ViolinMusicStaff.shortInstrumentName = \markup {      %! DEFAULT_INSTRUMENT
                                    \hcenter-in                                            %! DEFAULT_INSTRUMENT
                                        #10                                                %! DEFAULT_INSTRUMENT
                                        Vn.                                                %! DEFAULT_INSTRUMENT
                                    }                                                      %! DEFAULT_INSTRUMENT
                                \set ViolinMusicStaff.forceClef = ##t                      %! DEFAULT_CLEF
                                \clef "treble"                                             %! DEFAULT_CLEF
                                \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! DEFAULT_INSTRUMENT_COLOR
                                \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR
                                %%% \override ViolinMusicStaff.Clef.color = ##f            %! DEFAULT_CLEF_UNCOLOR
                                R1 * 1/2
                                ^ \markup {
                                    \column
                                        {
                                            %%% \line                                      %! DEFAULT_INSTRUMENT_ALERT
                                            %%%     {                                      %! DEFAULT_INSTRUMENT_ALERT
                                            %%%         \vcenter                           %! DEFAULT_INSTRUMENT_ALERT
                                            %%%             (Violin                        %! DEFAULT_INSTRUMENT_ALERT
                                            %%%         \vcenter                           %! DEFAULT_INSTRUMENT_ALERT
                                            %%%             \hcenter-in                    %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                 #10                        %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                 Violin                     %! DEFAULT_INSTRUMENT_ALERT
                                            %%%         \concat                            %! DEFAULT_INSTRUMENT_ALERT
                                            %%%             {                              %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                 \vcenter                   %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                     \hcenter-in            %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                         #10                %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                         Vn.                %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                 \vcenter                   %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                     )                      %! DEFAULT_INSTRUMENT_ALERT
                                            %%%             }                              %! DEFAULT_INSTRUMENT_ALERT
                                            %%%     }                                      %! DEFAULT_INSTRUMENT_ALERT
                                            \line                                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                {                                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                    \with-color                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                        #(x11-color 'DarkViolet)           %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                        {                                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            \vcenter                       %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                (Violin                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            \vcenter                       %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                \hcenter-in                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    #10                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    Violin                 %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            \concat                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                {                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    \vcenter               %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \hcenter-in        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            #10            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            Vn.            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    \vcenter               %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        )                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                }                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                        }                                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                }                                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                        }
                                    }
                                \set ViolinMusicStaff.instrumentName = \markup {           %! DEFAULT_REDRAW_INSTRUMENT
                                    \hcenter-in                                            %! DEFAULT_REDRAW_INSTRUMENT
                                        #10                                                %! DEFAULT_REDRAW_INSTRUMENT
                                        Violin                                             %! DEFAULT_REDRAW_INSTRUMENT
                                    }                                                      %! DEFAULT_REDRAW_INSTRUMENT
                                \set ViolinMusicStaff.shortInstrumentName = \markup {      %! DEFAULT_REDRAW_INSTRUMENT
                                    \hcenter-in                                            %! DEFAULT_REDRAW_INSTRUMENT
                                        #10                                                %! DEFAULT_REDRAW_INSTRUMENT
                                        Vn.                                                %! DEFAULT_REDRAW_INSTRUMENT
                                    }                                                      %! DEFAULT_REDRAW_INSTRUMENT
                                \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %! DEFAULT_REDRAW_INSTRUMENT_COLOR
                                \override ViolinMusicStaff.Clef.color = #(x11-color 'violet) %! DEFAULT_CLEF_COLOR_REDRAW
            <BLANKLINE>
                                % ViolinMusicVoice [measure 2]                             %! SM4
                                R1 * 3/8
            <BLANKLINE>
                                % ViolinMusicVoice [measure 3]                             %! SM4
                                R1 * 1/2
            <BLANKLINE>
                                % ViolinMusicVoice [measure 4]                             %! SM4
                                R1 * 3/8
                                \bar "|"
            <BLANKLINE>
                            }
                        }
                        \tag viola
                        \context ViolaMusicStaff = "ViolaMusicStaff" {
                            \context ViolaMusicVoice = "ViolaMusicVoice" {
            <BLANKLINE>
                                % ViolaMusicVoice [measure 1]                              %! SM4
                                \set ViolaMusicStaff.instrumentName = \markup {            %! DEFAULT_INSTRUMENT
                                    \hcenter-in                                            %! DEFAULT_INSTRUMENT
                                        #10                                                %! DEFAULT_INSTRUMENT
                                        Viola                                              %! DEFAULT_INSTRUMENT
                                    }                                                      %! DEFAULT_INSTRUMENT
                                \set ViolaMusicStaff.shortInstrumentName = \markup {       %! DEFAULT_INSTRUMENT
                                    \hcenter-in                                            %! DEFAULT_INSTRUMENT
                                        #10                                                %! DEFAULT_INSTRUMENT
                                        Va.                                                %! DEFAULT_INSTRUMENT
                                    }                                                      %! DEFAULT_INSTRUMENT
                                \set ViolaMusicStaff.forceClef = ##t                       %! DEFAULT_CLEF
                                \clef "alto"                                               %! DEFAULT_CLEF
                                \once \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! DEFAULT_INSTRUMENT_COLOR
                                \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR
                                %%% \override ViolaMusicStaff.Clef.color = ##f             %! DEFAULT_CLEF_UNCOLOR
                                R1 * 1/2
                                ^ \markup {
                                    \column
                                        {
                                            %%% \line                                      %! DEFAULT_INSTRUMENT_ALERT
                                            %%%     {                                      %! DEFAULT_INSTRUMENT_ALERT
                                            %%%         \vcenter                           %! DEFAULT_INSTRUMENT_ALERT
                                            %%%             (Viola                         %! DEFAULT_INSTRUMENT_ALERT
                                            %%%         \vcenter                           %! DEFAULT_INSTRUMENT_ALERT
                                            %%%             \hcenter-in                    %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                 #10                        %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                 Viola                      %! DEFAULT_INSTRUMENT_ALERT
                                            %%%         \concat                            %! DEFAULT_INSTRUMENT_ALERT
                                            %%%             {                              %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                 \vcenter                   %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                     \hcenter-in            %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                         #10                %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                         Va.                %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                 \vcenter                   %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                     )                      %! DEFAULT_INSTRUMENT_ALERT
                                            %%%             }                              %! DEFAULT_INSTRUMENT_ALERT
                                            %%%     }                                      %! DEFAULT_INSTRUMENT_ALERT
                                            \line                                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                {                                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                    \with-color                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                        #(x11-color 'DarkViolet)           %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                        {                                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            \vcenter                       %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                (Viola                     %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            \vcenter                       %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                \hcenter-in                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    #10                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    Viola                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            \concat                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                {                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    \vcenter               %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \hcenter-in        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            #10            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            Va.            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    \vcenter               %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        )                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                }                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                        }                                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                }                                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                        }
                                    }
                                \set ViolaMusicStaff.instrumentName = \markup {            %! DEFAULT_REDRAW_INSTRUMENT
                                    \hcenter-in                                            %! DEFAULT_REDRAW_INSTRUMENT
                                        #10                                                %! DEFAULT_REDRAW_INSTRUMENT
                                        Viola                                              %! DEFAULT_REDRAW_INSTRUMENT
                                    }                                                      %! DEFAULT_REDRAW_INSTRUMENT
                                \set ViolaMusicStaff.shortInstrumentName = \markup {       %! DEFAULT_REDRAW_INSTRUMENT
                                    \hcenter-in                                            %! DEFAULT_REDRAW_INSTRUMENT
                                        #10                                                %! DEFAULT_REDRAW_INSTRUMENT
                                        Va.                                                %! DEFAULT_REDRAW_INSTRUMENT
                                    }                                                      %! DEFAULT_REDRAW_INSTRUMENT
                                \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'violet) %! DEFAULT_REDRAW_INSTRUMENT_COLOR
                                \override ViolaMusicStaff.Clef.color = #(x11-color 'violet) %! DEFAULT_CLEF_COLOR_REDRAW
            <BLANKLINE>
                                % ViolaMusicVoice [measure 2]                              %! SM4
                                R1 * 3/8
            <BLANKLINE>
                                % ViolaMusicVoice [measure 3]                              %! SM4
                                R1 * 1/2
            <BLANKLINE>
                                % ViolaMusicVoice [measure 4]                              %! SM4
                                R1 * 3/8
                                \bar "|"
            <BLANKLINE>
                            }
                        }
                        \tag cello
                        \context CelloMusicStaff = "CelloMusicStaff" {
                            \context CelloMusicVoice = "CelloMusicVoice" {
            <BLANKLINE>
                                % CelloMusicVoice [measure 1]                              %! SM4
                                \set CelloMusicStaff.instrumentName = \markup {            %! DEFAULT_INSTRUMENT
                                    \hcenter-in                                            %! DEFAULT_INSTRUMENT
                                        #10                                                %! DEFAULT_INSTRUMENT
                                        Cello                                              %! DEFAULT_INSTRUMENT
                                    }                                                      %! DEFAULT_INSTRUMENT
                                \set CelloMusicStaff.shortInstrumentName = \markup {       %! DEFAULT_INSTRUMENT
                                    \hcenter-in                                            %! DEFAULT_INSTRUMENT
                                        #10                                                %! DEFAULT_INSTRUMENT
                                        Vc.                                                %! DEFAULT_INSTRUMENT
                                    }                                                      %! DEFAULT_INSTRUMENT
                                \set CelloMusicStaff.forceClef = ##t                       %! DEFAULT_CLEF
                                \clef "bass"                                               %! DEFAULT_CLEF
                                \once \override CelloMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! DEFAULT_INSTRUMENT_COLOR
                                \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR
                                %%% \override CelloMusicStaff.Clef.color = ##f             %! DEFAULT_CLEF_UNCOLOR
                                R1 * 1/2
                                ^ \markup {
                                    \column
                                        {
                                            %%% \line                                      %! DEFAULT_INSTRUMENT_ALERT
                                            %%%     {                                      %! DEFAULT_INSTRUMENT_ALERT
                                            %%%         \vcenter                           %! DEFAULT_INSTRUMENT_ALERT
                                            %%%             (Cello                         %! DEFAULT_INSTRUMENT_ALERT
                                            %%%         \vcenter                           %! DEFAULT_INSTRUMENT_ALERT
                                            %%%             \hcenter-in                    %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                 #10                        %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                 Cello                      %! DEFAULT_INSTRUMENT_ALERT
                                            %%%         \concat                            %! DEFAULT_INSTRUMENT_ALERT
                                            %%%             {                              %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                 \vcenter                   %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                     \hcenter-in            %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                         #10                %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                         Vc.                %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                 \vcenter                   %! DEFAULT_INSTRUMENT_ALERT
                                            %%%                     )                      %! DEFAULT_INSTRUMENT_ALERT
                                            %%%             }                              %! DEFAULT_INSTRUMENT_ALERT
                                            %%%     }                                      %! DEFAULT_INSTRUMENT_ALERT
                                            \line                                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                {                                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                    \with-color                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                        #(x11-color 'DarkViolet)           %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                        {                                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            \vcenter                       %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                (Cello                     %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            \vcenter                       %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                \hcenter-in                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    #10                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    Cello                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            \concat                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                {                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    \vcenter               %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \hcenter-in        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            #10            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                            Vc.            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    \vcenter               %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        )                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                }                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                        }                                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                }                                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                        }
                                    }
                                \set CelloMusicStaff.instrumentName = \markup {            %! DEFAULT_REDRAW_INSTRUMENT
                                    \hcenter-in                                            %! DEFAULT_REDRAW_INSTRUMENT
                                        #10                                                %! DEFAULT_REDRAW_INSTRUMENT
                                        Cello                                              %! DEFAULT_REDRAW_INSTRUMENT
                                    }                                                      %! DEFAULT_REDRAW_INSTRUMENT
                                \set CelloMusicStaff.shortInstrumentName = \markup {       %! DEFAULT_REDRAW_INSTRUMENT
                                    \hcenter-in                                            %! DEFAULT_REDRAW_INSTRUMENT
                                        #10                                                %! DEFAULT_REDRAW_INSTRUMENT
                                        Vc.                                                %! DEFAULT_REDRAW_INSTRUMENT
                                    }                                                      %! DEFAULT_REDRAW_INSTRUMENT
                                \override CelloMusicStaff.InstrumentName.color = #(x11-color 'violet) %! DEFAULT_REDRAW_INSTRUMENT_COLOR
                                \override CelloMusicStaff.Clef.color = #(x11-color 'violet) %! DEFAULT_CLEF_COLOR_REDRAW
            <BLANKLINE>
                                % CelloMusicVoice [measure 2]                              %! SM4
                                R1 * 3/8
            <BLANKLINE>
                                % CelloMusicVoice [measure 3]                              %! SM4
                                R1 * 1/2
            <BLANKLINE>
                                % CelloMusicVoice [measure 4]                              %! SM4
                                R1 * 3/8
                                \bar "|"
            <BLANKLINE>
                            }
                        }
                    >>
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls string trio score template.

        Returns score.
        '''
        global_context = self._make_global_context()
        instrument_tags = (
            'violin',
            'viola',
            'cello',
            )
        tag_string = '.'.join(instrument_tags)
        tag_string = f'tag {tag_string}'
        tag_command = abjad.LilyPondCommand(
            tag_string,
            'before',
            )
        abjad.attach(tag_command, global_context)

        # VIOLIN
        violin_music_voice = abjad.Voice(
            [],
            context_name='ViolinMusicVoice',
            name='ViolinMusicVoice',
            )
        violin_music_staff = abjad.Staff(
            [violin_music_voice],
            context_name='ViolinMusicStaff',
            name='ViolinMusicStaff',
            )
        violin = abjad.Violin(
            markup=baca.markup.instrument('Violin', hcenter_in=10),
            short_markup=baca.markup.short_instrument(
                'Vn.',
                hcenter_in=10,
                ),
            )
        abjad.annotate(
            violin_music_staff,
            'default_instrument',
            violin,
            )
        abjad.annotate(
            violin_music_staff,
            'default_clef',
            abjad.Clef('treble'),
            )
        self._attach_tag('violin', violin_music_staff)

        # VIOLA
        viola_music_voice = abjad.Voice(
            [],
            context_name='ViolaMusicVoice',
            name='ViolaMusicVoice',
            )
        viola_music_staff = abjad.Staff(
            [viola_music_voice],
            context_name='ViolaMusicStaff',
            name='ViolaMusicStaff',
            )
        abjad.annotate(
            viola_music_staff,
            'default_instrument',
            abjad.Viola(
                markup=baca.markup.instrument('Viola', hcenter_in=10),
                short_markup=baca.markup.short_instrument(
                    'Va.',
                    hcenter_in=10,
                    ),
                ),
            )
        abjad.annotate(
            viola_music_staff,
            'default_clef',
            abjad.Clef('alto'),
            )
        self._attach_tag('viola', viola_music_staff)

        # CELLO
        cello_music_voice = abjad.Voice(
            [],
            context_name='CelloMusicVoice',
            name='CelloMusicVoice',
            )
        cello_music_staff = abjad.Staff(
            [cello_music_voice],
            context_name='CelloMusicStaff',
            name='CelloMusicStaff',
            )
        abjad.annotate(
            cello_music_staff,
            'default_instrument',
            abjad.Cello(
                markup=baca.markup.instrument('Cello', hcenter_in=10),
                short_markup=baca.markup.short_instrument(
                    'Vc.',
                    hcenter_in=10,
                    ),
                ),
            )
        abjad.annotate(
            cello_music_staff,
            'default_clef',
            abjad.Clef('bass'),
            )
        self._attach_tag('cello', cello_music_staff)

        # SCORE
        string_section_staff_group = abjad.StaffGroup(
            [
                violin_music_staff,
                viola_music_staff,
                cello_music_staff,
                ],
            context_name='StringSectionStaffGroup',
            name='String Section Staff Group',
            )
        music_context = abjad.Context(
            [
                string_section_staff_group,
                ],
            context_name='MusicContext',
            is_simultaneous=True,
            name='MusicContext',
            )
        score = abjad.Score(
            [
                global_context,
                music_context,
                ],
            name='Score',
            )
        return score
