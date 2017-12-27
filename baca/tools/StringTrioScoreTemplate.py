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
                        %%% GlobalSkips [measure 1] %%%
                        \time 4/8
                        \bar ""                                                            %%! EMPTY_START_BAR
                        s1 * 1/2
                        - \markup {                                                        %%! STAGE_NUMBER_MARKUP
                            \fontsize                                                      %%! STAGE_NUMBER_MARKUP
                                #-3                                                        %%! STAGE_NUMBER_MARKUP
                                \with-color                                                %%! STAGE_NUMBER_MARKUP
                                    #(x11-color 'DarkCyan)                                 %%! STAGE_NUMBER_MARKUP
                                    [1]                                                    %%! STAGE_NUMBER_MARKUP
                            }                                                              %%! STAGE_NUMBER_MARKUP
            <BLANKLINE>
                        %%% GlobalSkips [measure 2] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 3/8
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
                                %%% ViolinMusicVoice [measure 1] %%%
                                \set ViolinMusicStaff.instrumentName = \markup {           %%! TEMPLATE_INSTRUMENT
                                    \hcenter-in                                            %%! TEMPLATE_INSTRUMENT
                                        #10                                                %%! TEMPLATE_INSTRUMENT
                                        Violin                                             %%! TEMPLATE_INSTRUMENT
                                    }                                                      %%! TEMPLATE_INSTRUMENT
                                \set ViolinMusicStaff.shortInstrumentName = \markup {      %%! TEMPLATE_INSTRUMENT
                                    \hcenter-in                                            %%! TEMPLATE_INSTRUMENT
                                        #10                                                %%! TEMPLATE_INSTRUMENT
                                        Vn.                                                %%! TEMPLATE_INSTRUMENT
                                    }                                                      %%! TEMPLATE_INSTRUMENT
                                \set ViolinMusicStaff.forceClef = ##t                      %%! TEMPLATE_CLEF
                                \clef "treble"                                             %%! TEMPLATE_CLEF
                                \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %%! TEMPLATE_INSTRUMENT_COLOR
                                \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %%! TEMPLATE_CLEF_COLOR
                                %%% \override ViolinMusicStaff.Clef.color = ##f            %%! TEMPLATE_CLEF_UNCOLOR
                                R1 * 1/2
                                ^ \markup {
                                    \column
                                        {
                                            %%% \line                                      %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%     {                                      %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%         \vcenter                           %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%             (Violin                        %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%         \vcenter                           %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%             \hcenter-in                    %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                 #10                        %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                 Violin                     %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%         \concat                            %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%             {                              %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                 \vcenter                   %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                     \hcenter-in            %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                         #10                %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                         Vn.                %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                 \vcenter                   %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                     )                      %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%             }                              %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%     }                                      %%! TEMPLATE_INSTRUMENT_ALERT
                                            \line                                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                {                                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                    \with-color                            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                        #(x11-color 'DarkViolet)           %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                        {                                  %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                            \vcenter                       %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                (Violin                    %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                            \vcenter                       %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                \hcenter-in                %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                    #10                    %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                    Violin                 %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                            \concat                        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                {                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                    \vcenter               %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \hcenter-in        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                            #10            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                            Vn.            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                    \vcenter               %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                        )                  %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                }                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                        }                                  %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                }                                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                        }
                                    }
                                \set ViolinMusicStaff.instrumentName = \markup {           %%! TEMPLATE_REDRAW_INSTRUMENT
                                    \hcenter-in                                            %%! TEMPLATE_REDRAW_INSTRUMENT
                                        #10                                                %%! TEMPLATE_REDRAW_INSTRUMENT
                                        Violin                                             %%! TEMPLATE_REDRAW_INSTRUMENT
                                    }                                                      %%! TEMPLATE_REDRAW_INSTRUMENT
                                \set ViolinMusicStaff.shortInstrumentName = \markup {      %%! TEMPLATE_REDRAW_INSTRUMENT
                                    \hcenter-in                                            %%! TEMPLATE_REDRAW_INSTRUMENT
                                        #10                                                %%! TEMPLATE_REDRAW_INSTRUMENT
                                        Vn.                                                %%! TEMPLATE_REDRAW_INSTRUMENT
                                    }                                                      %%! TEMPLATE_REDRAW_INSTRUMENT
                                \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %%! TEMPLATE_REDRAW_INSTRUMENT_COLOR
                                \override ViolinMusicStaff.Clef.color = #(x11-color 'violet) %%! TEMPLATE_CLEF_COLOR_REDRAW
            <BLANKLINE>
                                %%% ViolinMusicVoice [measure 2] %%%
                                R1 * 3/8
            <BLANKLINE>
                                %%% ViolinMusicVoice [measure 3] %%%
                                R1 * 1/2
            <BLANKLINE>
                                %%% ViolinMusicVoice [measure 4] %%%
                                R1 * 3/8
                                \bar "|"
            <BLANKLINE>
                            }
                        }
                        \tag viola
                        \context ViolaMusicStaff = "ViolaMusicStaff" {
                            \context ViolaMusicVoice = "ViolaMusicVoice" {
            <BLANKLINE>
                                %%% ViolaMusicVoice [measure 1] %%%
                                \set ViolaMusicStaff.instrumentName = \markup {            %%! TEMPLATE_INSTRUMENT
                                    \hcenter-in                                            %%! TEMPLATE_INSTRUMENT
                                        #10                                                %%! TEMPLATE_INSTRUMENT
                                        Viola                                              %%! TEMPLATE_INSTRUMENT
                                    }                                                      %%! TEMPLATE_INSTRUMENT
                                \set ViolaMusicStaff.shortInstrumentName = \markup {       %%! TEMPLATE_INSTRUMENT
                                    \hcenter-in                                            %%! TEMPLATE_INSTRUMENT
                                        #10                                                %%! TEMPLATE_INSTRUMENT
                                        Va.                                                %%! TEMPLATE_INSTRUMENT
                                    }                                                      %%! TEMPLATE_INSTRUMENT
                                \set ViolaMusicStaff.forceClef = ##t                       %%! TEMPLATE_CLEF
                                \clef "alto"                                               %%! TEMPLATE_CLEF
                                \once \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %%! TEMPLATE_INSTRUMENT_COLOR
                                \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %%! TEMPLATE_CLEF_COLOR
                                %%% \override ViolaMusicStaff.Clef.color = ##f             %%! TEMPLATE_CLEF_UNCOLOR
                                R1 * 1/2
                                ^ \markup {
                                    \column
                                        {
                                            %%% \line                                      %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%     {                                      %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%         \vcenter                           %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%             (Viola                         %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%         \vcenter                           %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%             \hcenter-in                    %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                 #10                        %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                 Viola                      %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%         \concat                            %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%             {                              %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                 \vcenter                   %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                     \hcenter-in            %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                         #10                %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                         Va.                %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                 \vcenter                   %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                     )                      %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%             }                              %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%     }                                      %%! TEMPLATE_INSTRUMENT_ALERT
                                            \line                                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                {                                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                    \with-color                            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                        #(x11-color 'DarkViolet)           %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                        {                                  %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                            \vcenter                       %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                (Viola                     %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                            \vcenter                       %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                \hcenter-in                %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                    #10                    %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                    Viola                  %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                            \concat                        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                {                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                    \vcenter               %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \hcenter-in        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                            #10            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                            Va.            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                    \vcenter               %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                        )                  %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                }                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                        }                                  %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                }                                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                        }
                                    }
                                \set ViolaMusicStaff.instrumentName = \markup {            %%! TEMPLATE_REDRAW_INSTRUMENT
                                    \hcenter-in                                            %%! TEMPLATE_REDRAW_INSTRUMENT
                                        #10                                                %%! TEMPLATE_REDRAW_INSTRUMENT
                                        Viola                                              %%! TEMPLATE_REDRAW_INSTRUMENT
                                    }                                                      %%! TEMPLATE_REDRAW_INSTRUMENT
                                \set ViolaMusicStaff.shortInstrumentName = \markup {       %%! TEMPLATE_REDRAW_INSTRUMENT
                                    \hcenter-in                                            %%! TEMPLATE_REDRAW_INSTRUMENT
                                        #10                                                %%! TEMPLATE_REDRAW_INSTRUMENT
                                        Va.                                                %%! TEMPLATE_REDRAW_INSTRUMENT
                                    }                                                      %%! TEMPLATE_REDRAW_INSTRUMENT
                                \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'violet) %%! TEMPLATE_REDRAW_INSTRUMENT_COLOR
                                \override ViolaMusicStaff.Clef.color = #(x11-color 'violet) %%! TEMPLATE_CLEF_COLOR_REDRAW
            <BLANKLINE>
                                %%% ViolaMusicVoice [measure 2] %%%
                                R1 * 3/8
            <BLANKLINE>
                                %%% ViolaMusicVoice [measure 3] %%%
                                R1 * 1/2
            <BLANKLINE>
                                %%% ViolaMusicVoice [measure 4] %%%
                                R1 * 3/8
                                \bar "|"
            <BLANKLINE>
                            }
                        }
                        \tag cello
                        \context CelloMusicStaff = "CelloMusicStaff" {
                            \context CelloMusicVoice = "CelloMusicVoice" {
            <BLANKLINE>
                                %%% CelloMusicVoice [measure 1] %%%
                                \set CelloMusicStaff.instrumentName = \markup {            %%! TEMPLATE_INSTRUMENT
                                    \hcenter-in                                            %%! TEMPLATE_INSTRUMENT
                                        #10                                                %%! TEMPLATE_INSTRUMENT
                                        Cello                                              %%! TEMPLATE_INSTRUMENT
                                    }                                                      %%! TEMPLATE_INSTRUMENT
                                \set CelloMusicStaff.shortInstrumentName = \markup {       %%! TEMPLATE_INSTRUMENT
                                    \hcenter-in                                            %%! TEMPLATE_INSTRUMENT
                                        #10                                                %%! TEMPLATE_INSTRUMENT
                                        Vc.                                                %%! TEMPLATE_INSTRUMENT
                                    }                                                      %%! TEMPLATE_INSTRUMENT
                                \set CelloMusicStaff.forceClef = ##t                       %%! TEMPLATE_CLEF
                                \clef "bass"                                               %%! TEMPLATE_CLEF
                                \once \override CelloMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %%! TEMPLATE_INSTRUMENT_COLOR
                                \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %%! TEMPLATE_CLEF_COLOR
                                %%% \override CelloMusicStaff.Clef.color = ##f             %%! TEMPLATE_CLEF_UNCOLOR
                                R1 * 1/2
                                ^ \markup {
                                    \column
                                        {
                                            %%% \line                                      %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%     {                                      %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%         \vcenter                           %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%             (Cello                         %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%         \vcenter                           %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%             \hcenter-in                    %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                 #10                        %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                 Cello                      %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%         \concat                            %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%             {                              %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                 \vcenter                   %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                     \hcenter-in            %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                         #10                %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                         Vc.                %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                 \vcenter                   %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%                     )                      %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%             }                              %%! TEMPLATE_INSTRUMENT_ALERT
                                            %%%     }                                      %%! TEMPLATE_INSTRUMENT_ALERT
                                            \line                                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                {                                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                    \with-color                            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                        #(x11-color 'DarkViolet)           %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                        {                                  %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                            \vcenter                       %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                (Cello                     %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                            \vcenter                       %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                \hcenter-in                %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                    #10                    %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                    Cello                  %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                            \concat                        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                {                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                    \vcenter               %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \hcenter-in        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                            #10            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                            Vc.            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                    \vcenter               %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                        )                  %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                }                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                        }                                  %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                }                                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                        }
                                    }
                                \set CelloMusicStaff.instrumentName = \markup {            %%! TEMPLATE_REDRAW_INSTRUMENT
                                    \hcenter-in                                            %%! TEMPLATE_REDRAW_INSTRUMENT
                                        #10                                                %%! TEMPLATE_REDRAW_INSTRUMENT
                                        Cello                                              %%! TEMPLATE_REDRAW_INSTRUMENT
                                    }                                                      %%! TEMPLATE_REDRAW_INSTRUMENT
                                \set CelloMusicStaff.shortInstrumentName = \markup {       %%! TEMPLATE_REDRAW_INSTRUMENT
                                    \hcenter-in                                            %%! TEMPLATE_REDRAW_INSTRUMENT
                                        #10                                                %%! TEMPLATE_REDRAW_INSTRUMENT
                                        Vc.                                                %%! TEMPLATE_REDRAW_INSTRUMENT
                                    }                                                      %%! TEMPLATE_REDRAW_INSTRUMENT
                                \override CelloMusicStaff.InstrumentName.color = #(x11-color 'violet) %%! TEMPLATE_REDRAW_INSTRUMENT_COLOR
                                \override CelloMusicStaff.Clef.color = #(x11-color 'violet) %%! TEMPLATE_CLEF_COLOR_REDRAW
            <BLANKLINE>
                                %%% CelloMusicVoice [measure 2] %%%
                                R1 * 3/8
            <BLANKLINE>
                                %%% CelloMusicVoice [measure 3] %%%
                                R1 * 1/2
            <BLANKLINE>
                                %%% CelloMusicVoice [measure 4] %%%
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
