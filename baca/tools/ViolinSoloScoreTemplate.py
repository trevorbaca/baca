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
                    \tag violin
                    \context ViolinMusicStaff = "ViolinMusicStaff" {
                        \context ViolinMusicVoice = "ViolinMusicVoice" {
            <BLANKLINE>
                            % ViolinMusicVoice [measure 1]                                 %! SM4
                            \set ViolinMusicStaff.instrumentName = \markup {               %! DEFAULT_INSTRUMENT
                                \hcenter-in                                                %! DEFAULT_INSTRUMENT
                                    #16                                                    %! DEFAULT_INSTRUMENT
                                    Violin                                                 %! DEFAULT_INSTRUMENT
                                }                                                          %! DEFAULT_INSTRUMENT
                            \set ViolinMusicStaff.shortInstrumentName = \markup {          %! DEFAULT_INSTRUMENT
                                \hcenter-in                                                %! DEFAULT_INSTRUMENT
                                    #10                                                    %! DEFAULT_INSTRUMENT
                                    Vn.                                                    %! DEFAULT_INSTRUMENT
                                }                                                          %! DEFAULT_INSTRUMENT
                            \set ViolinMusicStaff.forceClef = ##t                          %! DEFAULT_CLEF
                            \clef "treble"                                                 %! DEFAULT_CLEF
                            \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! DEFAULT_INSTRUMENT_COLOR
                            \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR
                            %%% \override ViolinMusicStaff.Clef.color = ##f                %! DEFAULT_CLEF_UNCOLOR
                            R1 * 1/2
                            ^ \markup {
                                \column
                                    {
                                        %%% \line                                          %! DEFAULT_INSTRUMENT_ALERT
                                        %%%     {                                          %! DEFAULT_INSTRUMENT_ALERT
                                        %%%         \vcenter                               %! DEFAULT_INSTRUMENT_ALERT
                                        %%%             (Violin                            %! DEFAULT_INSTRUMENT_ALERT
                                        %%%         \vcenter                               %! DEFAULT_INSTRUMENT_ALERT
                                        %%%             \hcenter-in                        %! DEFAULT_INSTRUMENT_ALERT
                                        %%%                 #16                            %! DEFAULT_INSTRUMENT_ALERT
                                        %%%                 Violin                         %! DEFAULT_INSTRUMENT_ALERT
                                        %%%         \concat                                %! DEFAULT_INSTRUMENT_ALERT
                                        %%%             {                                  %! DEFAULT_INSTRUMENT_ALERT
                                        %%%                 \vcenter                       %! DEFAULT_INSTRUMENT_ALERT
                                        %%%                     \hcenter-in                %! DEFAULT_INSTRUMENT_ALERT
                                        %%%                         #10                    %! DEFAULT_INSTRUMENT_ALERT
                                        %%%                         Vn.                    %! DEFAULT_INSTRUMENT_ALERT
                                        %%%                 \vcenter                       %! DEFAULT_INSTRUMENT_ALERT
                                        %%%                     )                          %! DEFAULT_INSTRUMENT_ALERT
                                        %%%             }                                  %! DEFAULT_INSTRUMENT_ALERT
                                        %%%     }                                          %! DEFAULT_INSTRUMENT_ALERT
                                        \line                                              %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                            {                                              %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                \with-color                                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                    #(x11-color 'DarkViolet)               %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                    {                                      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                        \vcenter                           %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            (Violin                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                        \vcenter                           %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            \hcenter-in                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                #16                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                Violin                     %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                        \concat                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            {                              %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                \vcenter                   %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    \hcenter-in            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        #10                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                        Vn.                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                \vcenter                   %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                                    )                      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                            }                              %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                                    }                                      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                            }                                              %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR
                                    }
                                }
                            \set ViolinMusicStaff.instrumentName = \markup {               %! DEFAULT_REDRAW_INSTRUMENT
                                \hcenter-in                                                %! DEFAULT_REDRAW_INSTRUMENT
                                    #16                                                    %! DEFAULT_REDRAW_INSTRUMENT
                                    Violin                                                 %! DEFAULT_REDRAW_INSTRUMENT
                                }                                                          %! DEFAULT_REDRAW_INSTRUMENT
                            \set ViolinMusicStaff.shortInstrumentName = \markup {          %! DEFAULT_REDRAW_INSTRUMENT
                                \hcenter-in                                                %! DEFAULT_REDRAW_INSTRUMENT
                                    #10                                                    %! DEFAULT_REDRAW_INSTRUMENT
                                    Vn.                                                    %! DEFAULT_REDRAW_INSTRUMENT
                                }                                                          %! DEFAULT_REDRAW_INSTRUMENT
                            \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %! DEFAULT_REDRAW_INSTRUMENT_COLOR
                            \override ViolinMusicStaff.Clef.color = #(x11-color 'violet)   %! DEFAULT_CLEF_COLOR_REDRAW
            <BLANKLINE>
                            % ViolinMusicVoice [measure 2]                                 %! SM4
                            R1 * 3/8
            <BLANKLINE>
                            % ViolinMusicVoice [measure 3]                                 %! SM4
                            R1 * 1/2
            <BLANKLINE>
                            % ViolinMusicVoice [measure 4]                                 %! SM4
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
