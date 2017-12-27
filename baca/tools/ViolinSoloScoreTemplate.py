import abjad
import baca
from .ScoreTemplate import ScoreTemplate


class ViolinSoloScoreTemplate(ScoreTemplate):
    r'''Violin solo score template.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.ViolinSoloScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=79)
            \context Score = "Score" <<
                \tag violin
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \time 4/8
                        \bar ""                                                            %%! EMPTY_START_BAR:1
                        s1 * 1/2
                        - \markup {                                                        %%! STAGE_NUMBER_MARKUP:2
                            \fontsize                                                      %%! STAGE_NUMBER_MARKUP:2
                                #-3                                                        %%! STAGE_NUMBER_MARKUP:2
                                \with-color                                                %%! STAGE_NUMBER_MARKUP:2
                                    #(x11-color 'DarkCyan)                                 %%! STAGE_NUMBER_MARKUP:2
                                    [1]                                                    %%! STAGE_NUMBER_MARKUP:2
                            }                                                              %%! STAGE_NUMBER_MARKUP:2
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
                    \tag violin
                    \context ViolinMusicStaff = "ViolinMusicStaff" {
                        \context ViolinMusicVoice = "ViolinMusicVoice" {
            <BLANKLINE>
                            %%% ViolinMusicVoice [measure 1] %%%
                            \set ViolinMusicStaff.instrumentName = \markup {               %%! TEMPLATE_INSTRUMENT:4
                                \hcenter-in                                                %%! TEMPLATE_INSTRUMENT:4
                                    #16                                                    %%! TEMPLATE_INSTRUMENT:4
                                    Violin                                                 %%! TEMPLATE_INSTRUMENT:4
                                }                                                          %%! TEMPLATE_INSTRUMENT:4
                            \set ViolinMusicStaff.shortInstrumentName = \markup {          %%! TEMPLATE_INSTRUMENT:4
                                \hcenter-in                                                %%! TEMPLATE_INSTRUMENT:4
                                    #10                                                    %%! TEMPLATE_INSTRUMENT:4
                                    Vn.                                                    %%! TEMPLATE_INSTRUMENT:4
                                }                                                          %%! TEMPLATE_INSTRUMENT:4
                            \set ViolinMusicStaff.forceClef = ##t                          %%! TEMPLATE_CLEF:9
                            \clef "treble"                                                 %%! TEMPLATE_CLEF:10
                            \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %%! TEMPLATE_INSTRUMENT_COLOR:1
                            \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %%! TEMPLATE_CLEF_COLOR:7
                            %%% \override ViolinMusicStaff.Clef.color = ##f                %%! TEMPLATE_CLEF_UNCOLOR:8
                            R1 * 1/2
                            ^ \markup {
                                \column
                                    {
                                        %%% \line                                          %%! TEMPLATE_INSTRUMENT_ALERT:2
                                        %%%     {                                          %%! TEMPLATE_INSTRUMENT_ALERT:2
                                        %%%         \vcenter                               %%! TEMPLATE_INSTRUMENT_ALERT:2
                                        %%%             (Violin                            %%! TEMPLATE_INSTRUMENT_ALERT:2
                                        %%%         \vcenter                               %%! TEMPLATE_INSTRUMENT_ALERT:2
                                        %%%             \hcenter-in                        %%! TEMPLATE_INSTRUMENT_ALERT:2
                                        %%%                 #16                            %%! TEMPLATE_INSTRUMENT_ALERT:2
                                        %%%                 Violin                         %%! TEMPLATE_INSTRUMENT_ALERT:2
                                        %%%         \concat                                %%! TEMPLATE_INSTRUMENT_ALERT:2
                                        %%%             {                                  %%! TEMPLATE_INSTRUMENT_ALERT:2
                                        %%%                 \vcenter                       %%! TEMPLATE_INSTRUMENT_ALERT:2
                                        %%%                     \hcenter-in                %%! TEMPLATE_INSTRUMENT_ALERT:2
                                        %%%                         #10                    %%! TEMPLATE_INSTRUMENT_ALERT:2
                                        %%%                         Vn.                    %%! TEMPLATE_INSTRUMENT_ALERT:2
                                        %%%                 \vcenter                       %%! TEMPLATE_INSTRUMENT_ALERT:2
                                        %%%                     )                          %%! TEMPLATE_INSTRUMENT_ALERT:2
                                        %%%             }                                  %%! TEMPLATE_INSTRUMENT_ALERT:2
                                        %%%     }                                          %%! TEMPLATE_INSTRUMENT_ALERT:2
                                        \line                                              %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                            {                                              %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                \with-color                                %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                    #(x11-color 'DarkViolet)               %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                    {                                      %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                        \vcenter                           %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                            (Violin                        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                        \vcenter                           %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                            \hcenter-in                    %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                #16                        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                Violin                     %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                        \concat                            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                            {                              %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                \vcenter                   %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                    \hcenter-in            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                        #10                %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                        Vn.                %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                \vcenter                   %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                    )                      %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                            }                              %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                    }                                      %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                            }                                              %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                    }
                                }
                            \set ViolinMusicStaff.instrumentName = \markup {               %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                \hcenter-in                                                %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                    #16                                                    %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                    Violin                                                 %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                }                                                          %%! TEMPLATE_REDRAW_INSTRUMENT:6
                            \set ViolinMusicStaff.shortInstrumentName = \markup {          %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                \hcenter-in                                                %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                    #10                                                    %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                    Vn.                                                    %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                }                                                          %%! TEMPLATE_REDRAW_INSTRUMENT:6
                            \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %%! TEMPLATE_REDRAW_INSTRUMENT_COLOR:5
                            \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)   %%! TEMPLATE_CLEF_COLOR_REDRAW:11
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
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls violin solo score template.

        Returns score.
        '''
        global_context = self._make_global_context()
        instrument_tags = (
            'violin',
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
            markup=baca.markup.instrument('Violin'),
            short_markup=baca.markup.short_instrument('Vn.'),
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
        # SCORE
        music_context = abjad.Context(
            [
                violin_music_staff,
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
