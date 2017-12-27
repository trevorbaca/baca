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
        >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=79)
            \context Score = "Score" <<
                \tag violin.viola.cello
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \autoPageBreaksOff                                                 %%! SEGMENT:LAYOUT
                        \noBreak                                                           %%! SEGMENT:LAYOUT
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
                        \break                                                             %%! SEGMENT:LAYOUT
            <BLANKLINE>
                        %%% GlobalSkips [measure 2] %%%
                        \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details #'((Y-offset . 100) (alignment-distances . (30 30))) %%! SEGMENT:LAYOUT
                        \time 3/8
                        s1 * 3/8
                        \break                                                             %%! SEGMENT:LAYOUT
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \noBreak                                                           %%! SEGMENT:LAYOUT
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \noBreak                                                           %%! SEGMENT:LAYOUT
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 5] %%%
                        \noBreak                                                           %%! SEGMENT:LAYOUT
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
                                    \set ViolinMusicStaff.instrumentName = \markup {       %%! TEMPLATE_INSTRUMENT
                                        \hcenter-in                                        %%! TEMPLATE_INSTRUMENT
                                            #10                                            %%! TEMPLATE_INSTRUMENT
                                            Violin                                         %%! TEMPLATE_INSTRUMENT
                                        }                                                  %%! TEMPLATE_INSTRUMENT
                                    \set ViolinMusicStaff.shortInstrumentName = \markup {  %%! TEMPLATE_INSTRUMENT
                                        \hcenter-in                                        %%! TEMPLATE_INSTRUMENT
                                            #10                                            %%! TEMPLATE_INSTRUMENT
                                            Vn.                                            %%! TEMPLATE_INSTRUMENT
                                        }                                                  %%! TEMPLATE_INSTRUMENT
                                    \set ViolinMusicStaff.forceClef = ##t                  %%! TEMPLATE_CLEF
                                    \clef "treble"                                         %%! TEMPLATE_CLEF
                                    \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %%! TEMPLATE_INSTRUMENT_COLOR
                                    \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %%! TEMPLATE_CLEF_COLOR
                                    %%% \override ViolinMusicStaff.Clef.color = ##f        %%! TEMPLATE_CLEF_UNCOLOR
                                    e'8
                                    [
                                    ^ \markup {
                                        \column
                                            {
                                                %%% \line                                  %%! TEMPLATE_INSTRUMENT_ALERT
                                                %%%     {                                  %%! TEMPLATE_INSTRUMENT_ALERT
                                                %%%         \vcenter                       %%! TEMPLATE_INSTRUMENT_ALERT
                                                %%%             (Violin                    %%! TEMPLATE_INSTRUMENT_ALERT
                                                %%%         \vcenter                       %%! TEMPLATE_INSTRUMENT_ALERT
                                                %%%             \hcenter-in                %%! TEMPLATE_INSTRUMENT_ALERT
                                                %%%                 #10                    %%! TEMPLATE_INSTRUMENT_ALERT
                                                %%%                 Violin                 %%! TEMPLATE_INSTRUMENT_ALERT
                                                %%%         \concat                        %%! TEMPLATE_INSTRUMENT_ALERT
                                                %%%             {                          %%! TEMPLATE_INSTRUMENT_ALERT
                                                %%%                 \vcenter               %%! TEMPLATE_INSTRUMENT_ALERT
                                                %%%                     \hcenter-in        %%! TEMPLATE_INSTRUMENT_ALERT
                                                %%%                         #10            %%! TEMPLATE_INSTRUMENT_ALERT
                                                %%%                         Vn.            %%! TEMPLATE_INSTRUMENT_ALERT
                                                %%%                 \vcenter               %%! TEMPLATE_INSTRUMENT_ALERT
                                                %%%                     )                  %%! TEMPLATE_INSTRUMENT_ALERT
                                                %%%             }                          %%! TEMPLATE_INSTRUMENT_ALERT
                                                %%%     }                                  %%! TEMPLATE_INSTRUMENT_ALERT
                                                \line                                      %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                    {                                      %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                        \with-color                        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                            #(x11-color 'DarkViolet)       %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                            {                              %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                \vcenter                   %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                    (Violin                %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                \vcenter                   %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                    \hcenter-in            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                        #10                %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                        Violin             %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                \concat                    %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                    {                      %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \vcenter           %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                            \hcenter-in    %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                                #10        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                                Vn.        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                        \vcenter           %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                            )              %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                                    }                      %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                            }                              %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                                    }                                      %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR
                                            }
                                        }
                                    \set ViolinMusicStaff.instrumentName = \markup {       %%! TEMPLATE_REDRAW_INSTRUMENT
                                        \hcenter-in                                        %%! TEMPLATE_REDRAW_INSTRUMENT
                                            #10                                            %%! TEMPLATE_REDRAW_INSTRUMENT
                                            Violin                                         %%! TEMPLATE_REDRAW_INSTRUMENT
                                        }                                                  %%! TEMPLATE_REDRAW_INSTRUMENT
                                    \set ViolinMusicStaff.shortInstrumentName = \markup {  %%! TEMPLATE_REDRAW_INSTRUMENT
                                        \hcenter-in                                        %%! TEMPLATE_REDRAW_INSTRUMENT
                                            #10                                            %%! TEMPLATE_REDRAW_INSTRUMENT
                                            Vn.                                            %%! TEMPLATE_REDRAW_INSTRUMENT
                                        }                                                  %%! TEMPLATE_REDRAW_INSTRUMENT
                                    \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %%! TEMPLATE_REDRAW_INSTRUMENT_COLOR
                                    \override ViolinMusicStaff.Clef.color = #(x11-color 'violet) %%! TEMPLATE_CLEF_COLOR_REDRAW
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
