import abjad
import baca


class LayoutMeasureMap(abjad.AbjadObject):
    r'''Layout measure map.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8), (4, 8)],
        ...     layout_measure_map=baca.LayoutMeasureMap([
        ...         baca.line_break(baca.skip(0)),
        ...         baca.lbsd(100, [30, 30], baca.skip(1)),
        ...         baca.line_break(baca.skip(1)),
        ...         ]),
        ...     )

        >>> maker(
        ...     baca.scope('ViolinMusicVoice', 1),
        ...     baca.make_even_runs(),
        ...     baca.pitches('E4', repeats=True),
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
                        \autoPageBreaksOff %! SEGMENT:LAYOUT:4
                        \noBreak %! SEGMENT:LAYOUT:5
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
                        \break %! SEGMENT:LAYOUT:3
            <BLANKLINE>
                        %%% GlobalSkips [measure 2] %%%
                        \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details #'((Y-offset . 100) (alignment-distances . (30 30))) %! SEGMENT:LAYOUT:1
                        \time 3/8
                        s1 * 3/8
                        \break %! SEGMENT:LAYOUT:2
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \noBreak %! SEGMENT:LAYOUT:1
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \noBreak %! SEGMENT:LAYOUT:1
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 5] %%%
                        \noBreak %! SEGMENT:LAYOUT:1
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context StringSectionStaffGroup = "String Section Staff Group" <<
                        \tag violin
                        \context ViolinMusicStaff = "ViolinMusicStaff" {
                            \context ViolinMusicVoice = "ViolinMusicVoice" {
                                {
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
                                    e'8
                                    [
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
                                    e'8
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
            <BLANKLINE>
                                    %%% ViolinMusicVoice [measure 2] %%%
                                    e'8
                                    [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
            <BLANKLINE>
                                    %%% ViolinMusicVoice [measure 3] %%%
                                    e'8
                                    [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
            <BLANKLINE>
                                    %%% ViolinMusicVoice [measure 4] %%%
                                    e'8
                                    [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
                                }
                                {
            <BLANKLINE>
                                    %%% ViolinMusicVoice [measure 5] %%%
                                    e'8
                                    [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
                                    ]
                                    \bar "|"
            <BLANKLINE>
                                }
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
            <BLANKLINE>
                                %%% ViolaMusicVoice [measure 5] %%%
                                R1 * 1/2
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
            <BLANKLINE>
                                %%% CelloMusicVoice [measure 5] %%%
                                R1 * 1/2
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

    __slots__ = (
        '_build',
        '_commands',
        '_tag',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, commands=None, build=None):
        self._build = build
        if build is None:
            tag = 'SEGMENT'
        else:
            tag = 'BUILD:' + build.upper()
        tag += ':LAYOUT'
        self._tag = tag
        if commands is not None:
            if tag is not None:
                commands_ = []
                for command in commands:
                    command_ = abjad.new(command, tag=tag)
                    commands_.append(command_)
                commands = commands_
            commands = tuple(commands)
        self._commands = commands

    ### SPECIAL METHODS ###

    def __call__(self, context=None):
        r'''Calls map on `context`.

        Returns none.
        '''
        if context is None:
            return
        for command in self.commands:
            command(context)
        skips = baca.select(context).skips()
        command = abjad.LilyPondCommand('autoPageBreaksOff', 'before')
        abjad.attach(command, skips[0], tag=self.tag)
        for skip in skips:
            if not abjad.inspect(skip).has_indicator(baca.LBSD):
                literal = abjad.LilyPondLiteral(r'\noBreak', 'before')
                abjad.attach(literal, skip, tag=self.tag)

    ### PUBLIC PROPERTIES ###

    @property
    def build(self):
        r'''Gets build.
        '''
        return self._build

    @property
    def commands(self):
        r'''Gets commands.

        ..  container:: example

            >>> layout = baca.LayoutMeasureMap([
            ...     baca.line_break(baca.skip(0)),
            ...     baca.page_break(baca.skip(1)),
            ...     ])

            >>> for command in layout.commands:
            ...     command
            ...
            IndicatorCommand(indicators=CyclicTuple([LineBreak(format_slot='closing')]), selector=baca.skip(0), tag='SEGMENT:LAYOUT')
            IndicatorCommand(indicators=CyclicTuple([PageBreak(format_slot='closing')]), selector=baca.skip(1), tag='SEGMENT:LAYOUT')

        Returns commands.
        '''
        return self._commands

    @property
    def tag(self):
        r'''Gets tag.
        '''
        return self._tag
