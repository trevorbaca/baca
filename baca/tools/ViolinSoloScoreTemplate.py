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

            >>> abjad.f(lilypond_file[abjad.Score], strict=True)
            \context Score = "Score" <<
                \tag violin
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
                    \tag violin
                    \context ViolinMusicStaff = "ViolinMusicStaff" {
                        \context ViolinMusicVoice = "ViolinMusicVoice" {
            <BLANKLINE>
                            %%% ViolinMusicVoice [measure 1] %%%
                            \set ViolinMusicStaff.instrumentName = \markup { %! EXPLICIT_INSTRUMENT:9
                                \hcenter-in %! EXPLICIT_INSTRUMENT:9
                                    #16 %! EXPLICIT_INSTRUMENT:9
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
                                    #16 %! EXPLICIT_REDRAW_INSTRUMENT:11
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
            name_markup=baca.markup.instrument('Violin'),
            short_name_markup=baca.markup.short_instrument('Vn.'),
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
