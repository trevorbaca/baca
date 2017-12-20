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
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=True)
            \context Score = "Score" <<
                \tag violin.viola.cello
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \time 4/8
                        \bar "" %! EMPTY_START_BAR:1
                        s1 * 1/2
                        - \markup { %! STAGE_NUMBER_MARKUP:2
                            \fontsize %! STAGE_NUMBER_MARKUP:2
                                #-3 %! STAGE_NUMBER_MARKUP:2
                                \with-color %! STAGE_NUMBER_MARKUP:2
                                    #(x11-color 'DarkCyan) %! STAGE_NUMBER_MARKUP:2
                                    [1] %! STAGE_NUMBER_MARKUP:2
                            } %! STAGE_NUMBER_MARKUP:2
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
                                \set ViolinMusicStaff.instrumentName = \markup { %! EXPLICIT_INSTRUMENT:9
                                    \hcenter-in %! EXPLICIT_INSTRUMENT:9
                                        #10 %! EXPLICIT_INSTRUMENT:9
                                        Violin %! EXPLICIT_INSTRUMENT:9
                                    } %! EXPLICIT_INSTRUMENT:9
                                \set ViolinMusicStaff.shortInstrumentName = \markup { %! EXPLICIT_INSTRUMENT:9
                                    \hcenter-in %! EXPLICIT_INSTRUMENT:9
                                        #10 %! EXPLICIT_INSTRUMENT:9
                                        Vn. %! EXPLICIT_INSTRUMENT:9
                                    } %! EXPLICIT_INSTRUMENT:9
                                \clef "treble" %! EXPLICIT_CLEF:4
                                \once \override ViolinMusicStaff.Clef.color = #(x11-color 'blue) %! EXPLICIT_CLEF_COLOR:1
                                %%% \override ViolinMusicStaff.Clef.color = ##f %! EXPLICIT_CLEF_UNCOLOR:2
                                \set ViolinMusicStaff.forceClef = ##t %! EXPLICIT_CLEF:3
                                \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_INSTRUMENT_COLOR:6
                                R1 * 1/2
                                ^ \markup {
                                    \column
                                        {
                                            %%% \line %! EXPLICIT_INSTRUMENT_ALERT:7
                                            %%%     { %! EXPLICIT_INSTRUMENT_ALERT:7
                                            %%%         [[violin]] %! EXPLICIT_INSTRUMENT_ALERT:7
                                            %%%     } %! EXPLICIT_INSTRUMENT_ALERT:7
                                            \line %! EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR:8
                                                { %! EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR:8
                                                    \with-color %! EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR:8
                                                        #(x11-color 'blue) %! EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR:8
                                                        [[violin]] %! EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR:8
                                                } %! EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR:8
                                        }
                                    }
                                \set ViolinMusicStaff.instrumentName = \markup { %! EXPLICIT_REDRAW_INSTRUMENT:11
                                    \hcenter-in %! EXPLICIT_REDRAW_INSTRUMENT:11
                                        #10 %! EXPLICIT_REDRAW_INSTRUMENT:11
                                        Violin %! EXPLICIT_REDRAW_INSTRUMENT:11
                                    } %! EXPLICIT_REDRAW_INSTRUMENT:11
                                \set ViolinMusicStaff.shortInstrumentName = \markup { %! EXPLICIT_REDRAW_INSTRUMENT:11
                                    \hcenter-in %! EXPLICIT_REDRAW_INSTRUMENT:11
                                        #10 %! EXPLICIT_REDRAW_INSTRUMENT:11
                                        Vn. %! EXPLICIT_REDRAW_INSTRUMENT:11
                                    } %! EXPLICIT_REDRAW_INSTRUMENT:11
                                \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkCyan) %! EXPLICIT_CLEF_COLOR_REDRAW:5
                                \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkCyan) %! EXPLICIT_REDRAW_INSTRUMENT_COLOR:10
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
                                \set ViolaMusicStaff.instrumentName = \markup { %! EXPLICIT_INSTRUMENT:9
                                    \hcenter-in %! EXPLICIT_INSTRUMENT:9
                                        #10 %! EXPLICIT_INSTRUMENT:9
                                        Viola %! EXPLICIT_INSTRUMENT:9
                                    } %! EXPLICIT_INSTRUMENT:9
                                \set ViolaMusicStaff.shortInstrumentName = \markup { %! EXPLICIT_INSTRUMENT:9
                                    \hcenter-in %! EXPLICIT_INSTRUMENT:9
                                        #10 %! EXPLICIT_INSTRUMENT:9
                                        Va. %! EXPLICIT_INSTRUMENT:9
                                    } %! EXPLICIT_INSTRUMENT:9
                                \clef "alto" %! EXPLICIT_CLEF:4
                                \once \override ViolaMusicStaff.Clef.color = #(x11-color 'blue) %! EXPLICIT_CLEF_COLOR:1
                                %%% \override ViolaMusicStaff.Clef.color = ##f %! EXPLICIT_CLEF_UNCOLOR:2
                                \set ViolaMusicStaff.forceClef = ##t %! EXPLICIT_CLEF:3
                                \once \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_INSTRUMENT_COLOR:6
                                R1 * 1/2
                                ^ \markup {
                                    \column
                                        {
                                            %%% \line %! EXPLICIT_INSTRUMENT_ALERT:7
                                            %%%     { %! EXPLICIT_INSTRUMENT_ALERT:7
                                            %%%         [[viola]] %! EXPLICIT_INSTRUMENT_ALERT:7
                                            %%%     } %! EXPLICIT_INSTRUMENT_ALERT:7
                                            \line %! EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR:8
                                                { %! EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR:8
                                                    \with-color %! EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR:8
                                                        #(x11-color 'blue) %! EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR:8
                                                        [[viola]] %! EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR:8
                                                } %! EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR:8
                                        }
                                    }
                                \set ViolaMusicStaff.instrumentName = \markup { %! EXPLICIT_REDRAW_INSTRUMENT:11
                                    \hcenter-in %! EXPLICIT_REDRAW_INSTRUMENT:11
                                        #10 %! EXPLICIT_REDRAW_INSTRUMENT:11
                                        Viola %! EXPLICIT_REDRAW_INSTRUMENT:11
                                    } %! EXPLICIT_REDRAW_INSTRUMENT:11
                                \set ViolaMusicStaff.shortInstrumentName = \markup { %! EXPLICIT_REDRAW_INSTRUMENT:11
                                    \hcenter-in %! EXPLICIT_REDRAW_INSTRUMENT:11
                                        #10 %! EXPLICIT_REDRAW_INSTRUMENT:11
                                        Va. %! EXPLICIT_REDRAW_INSTRUMENT:11
                                    } %! EXPLICIT_REDRAW_INSTRUMENT:11
                                \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkCyan) %! EXPLICIT_CLEF_COLOR_REDRAW:5
                                \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'DarkCyan) %! EXPLICIT_REDRAW_INSTRUMENT_COLOR:10
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
                                \set CelloMusicStaff.instrumentName = \markup { %! EXPLICIT_INSTRUMENT:9
                                    \hcenter-in %! EXPLICIT_INSTRUMENT:9
                                        #10 %! EXPLICIT_INSTRUMENT:9
                                        Cello %! EXPLICIT_INSTRUMENT:9
                                    } %! EXPLICIT_INSTRUMENT:9
                                \set CelloMusicStaff.shortInstrumentName = \markup { %! EXPLICIT_INSTRUMENT:9
                                    \hcenter-in %! EXPLICIT_INSTRUMENT:9
                                        #10 %! EXPLICIT_INSTRUMENT:9
                                        Vc. %! EXPLICIT_INSTRUMENT:9
                                    } %! EXPLICIT_INSTRUMENT:9
                                \clef "bass" %! EXPLICIT_CLEF:4
                                \once \override CelloMusicStaff.Clef.color = #(x11-color 'blue) %! EXPLICIT_CLEF_COLOR:1
                                %%% \override CelloMusicStaff.Clef.color = ##f %! EXPLICIT_CLEF_UNCOLOR:2
                                \set CelloMusicStaff.forceClef = ##t %! EXPLICIT_CLEF:3
                                \once \override CelloMusicStaff.InstrumentName.color = #(x11-color 'blue) %! EXPLICIT_INSTRUMENT_COLOR:6
                                R1 * 1/2
                                ^ \markup {
                                    \column
                                        {
                                            %%% \line %! EXPLICIT_INSTRUMENT_ALERT:7
                                            %%%     { %! EXPLICIT_INSTRUMENT_ALERT:7
                                            %%%         [[cello]] %! EXPLICIT_INSTRUMENT_ALERT:7
                                            %%%     } %! EXPLICIT_INSTRUMENT_ALERT:7
                                            \line %! EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR:8
                                                { %! EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR:8
                                                    \with-color %! EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR:8
                                                        #(x11-color 'blue) %! EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR:8
                                                        [[cello]] %! EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR:8
                                                } %! EXPLICIT_INSTRUMENT_ALERT_WITH_COLOR:8
                                        }
                                    }
                                \set CelloMusicStaff.instrumentName = \markup { %! EXPLICIT_REDRAW_INSTRUMENT:11
                                    \hcenter-in %! EXPLICIT_REDRAW_INSTRUMENT:11
                                        #10 %! EXPLICIT_REDRAW_INSTRUMENT:11
                                        Cello %! EXPLICIT_REDRAW_INSTRUMENT:11
                                    } %! EXPLICIT_REDRAW_INSTRUMENT:11
                                \set CelloMusicStaff.shortInstrumentName = \markup { %! EXPLICIT_REDRAW_INSTRUMENT:11
                                    \hcenter-in %! EXPLICIT_REDRAW_INSTRUMENT:11
                                        #10 %! EXPLICIT_REDRAW_INSTRUMENT:11
                                        Vc. %! EXPLICIT_REDRAW_INSTRUMENT:11
                                    } %! EXPLICIT_REDRAW_INSTRUMENT:11
                                \override CelloMusicStaff.Clef.color = #(x11-color 'DarkCyan) %! EXPLICIT_CLEF_COLOR_REDRAW:5
                                \override CelloMusicStaff.InstrumentName.color = #(x11-color 'DarkCyan) %! EXPLICIT_REDRAW_INSTRUMENT_COLOR:10
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
            name_markup=baca.markup.instrument('Violin', hcenter_in=10),
            short_name_markup=baca.markup.short_instrument(
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
                name_markup=baca.markup.instrument('Viola', hcenter_in=10),
                short_name_markup=baca.markup.short_instrument(
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
                name_markup=baca.markup.instrument('Cello', hcenter_in=10),
                short_name_markup=baca.markup.short_instrument(
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
