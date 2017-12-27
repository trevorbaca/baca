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
        >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=79)
            \context Score = "Score" <<
                \tag violin
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
                    \tag violin
                    \context ViolinMusicStaff = "ViolinMusicStaff" {
                        \context ViolinMusicVoice = "ViolinMusicVoice" {
            <BLANKLINE>
                            %%% ViolinMusicVoice [measure 1] %%%
                            \set ViolinMusicStaff.instrumentName = \markup {               %%! TEMPLATE_INSTRUMENT
                                \hcenter-in                                                %%! TEMPLATE_INSTRUMENT
                                    #16                                                    %%! TEMPLATE_INSTRUMENT
                                    Violin                                                 %%! TEMPLATE_INSTRUMENT
                                }                                                          %%! TEMPLATE_INSTRUMENT
                            \set ViolinMusicStaff.shortInstrumentName = \markup {          %%! TEMPLATE_INSTRUMENT
                                \hcenter-in                                                %%! TEMPLATE_INSTRUMENT
                                    #10                                                    %%! TEMPLATE_INSTRUMENT
                                    Vn.                                                    %%! TEMPLATE_INSTRUMENT
                                }                                                          %%! TEMPLATE_INSTRUMENT
                            \set ViolinMusicStaff.forceClef = ##t                          %%! TEMPLATE_CLEF
                            \clef "treble"                                                 %%! TEMPLATE_CLEF
                            \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %%! TEMPLATE_INSTRUMENT_COLOR
                            \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %%! TEMPLATE_CLEF_COLOR
                            %%% \override ViolinMusicStaff.Clef.color = ##f                %%! TEMPLATE_CLEF_UNCOLOR
                            R1 * 1/2
                            ^ \markup {
                                \column
                                    {
                                        %%% \line                                          %%! TEMPLATE_INSTRUMENT_ALERT
                                        %%%     {                                          %%! TEMPLATE_INSTRUMENT_ALERT
                                        %%%         \vcenter                               %%! TEMPLATE_INSTRUMENT_ALERT
                                        %%%             (Violin                            %%! TEMPLATE_INSTRUMENT_ALERT
                                        %%%         \vcenter                               %%! TEMPLATE_INSTRUMENT_ALERT
                                        %%%             \hcenter-in                        %%! TEMPLATE_INSTRUMENT_ALERT
                                        %%%                 #16                            %%! TEMPLATE_INSTRUMENT_ALERT
                                        %%%                 Violin                         %%! TEMPLATE_INSTRUMENT_ALERT
                                        %%%         \concat                                %%! TEMPLATE_INSTRUMENT_ALERT
                                        %%%             {                                  %%! TEMPLATE_INSTRUMENT_ALERT
                                        %%%                 \vcenter                       %%! TEMPLATE_INSTRUMENT_ALERT
                                        %%%                     \hcenter-in                %%! TEMPLATE_INSTRUMENT_ALERT
                                        %%%                         #10                    %%! TEMPLATE_INSTRUMENT_ALERT
                                        %%%                         Vn.                    %%! TEMPLATE_INSTRUMENT_ALERT
                                        %%%                 \vcenter                       %%! TEMPLATE_INSTRUMENT_ALERT
                                        %%%                     )                          %%! TEMPLATE_INSTRUMENT_ALERT
                                        %%%             }                                  %%! TEMPLATE_INSTRUMENT_ALERT
                                        %%%     }                                          %%! TEMPLATE_INSTRUMENT_ALERT
                                        \line                                              %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                            {                                              %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                \with-color                                %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                    #(x11-color 'DarkViolet)               %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                    {                                      %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                        \vcenter                           %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                            (Violin                        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                        \vcenter                           %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                            \hcenter-in                    %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                #16                        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                Violin                     %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                        \concat                            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                            {                              %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                \vcenter                   %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                    \hcenter-in            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                        #10                %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                        Vn.                %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                \vcenter                   %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                    )                      %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                            }                              %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                    }                                      %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                            }                                              %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                    }
                                }
                            \set ViolinMusicStaff.instrumentName = \markup {               %%! TEMPLATE_REDRAW_INSTRUMENT
                                \hcenter-in                                                %%! TEMPLATE_REDRAW_INSTRUMENT
                                    #16                                                    %%! TEMPLATE_REDRAW_INSTRUMENT
                                    Violin                                                 %%! TEMPLATE_REDRAW_INSTRUMENT
                                }                                                          %%! TEMPLATE_REDRAW_INSTRUMENT
                            \set ViolinMusicStaff.shortInstrumentName = \markup {          %%! TEMPLATE_REDRAW_INSTRUMENT
                                \hcenter-in                                                %%! TEMPLATE_REDRAW_INSTRUMENT
                                    #10                                                    %%! TEMPLATE_REDRAW_INSTRUMENT
                                    Vn.                                                    %%! TEMPLATE_REDRAW_INSTRUMENT
                                }                                                          %%! TEMPLATE_REDRAW_INSTRUMENT
                            \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %%! TEMPLATE_REDRAW_INSTRUMENT_COLOR
                            \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)   %%! TEMPLATE_CLEF_COLOR_REDRAW
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
