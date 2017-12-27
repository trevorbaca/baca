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
                        \autoPageBreaksOff                                                 %%! SEGMENT:LAYOUT:4
                        \noBreak                                                           %%! SEGMENT:LAYOUT:5
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
                        \break                                                             %%! SEGMENT:LAYOUT:3
            <BLANKLINE>
                        %%% GlobalSkips [measure 2] %%%
                        \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details #'((Y-offset . 100) (alignment-distances . (30 30))) %%! SEGMENT:LAYOUT:1
                        \time 3/8
                        s1 * 3/8
                        \break                                                             %%! SEGMENT:LAYOUT:2
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \noBreak                                                           %%! SEGMENT:LAYOUT:1
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \noBreak                                                           %%! SEGMENT:LAYOUT:1
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 5] %%%
                        \noBreak                                                           %%! SEGMENT:LAYOUT:1
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
                                    \set ViolinMusicStaff.instrumentName = \markup {       %%! TEMPLATE_INSTRUMENT:4
                                        \hcenter-in                                        %%! TEMPLATE_INSTRUMENT:4
                                            #10                                            %%! TEMPLATE_INSTRUMENT:4
                                            Violin                                         %%! TEMPLATE_INSTRUMENT:4
                                        }                                                  %%! TEMPLATE_INSTRUMENT:4
                                    \set ViolinMusicStaff.shortInstrumentName = \markup {  %%! TEMPLATE_INSTRUMENT:4
                                        \hcenter-in                                        %%! TEMPLATE_INSTRUMENT:4
                                            #10                                            %%! TEMPLATE_INSTRUMENT:4
                                            Vn.                                            %%! TEMPLATE_INSTRUMENT:4
                                        }                                                  %%! TEMPLATE_INSTRUMENT:4
                                    \set ViolinMusicStaff.forceClef = ##t                  %%! TEMPLATE_CLEF:9
                                    \clef "treble"                                         %%! TEMPLATE_CLEF:10
                                    \once \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %%! TEMPLATE_INSTRUMENT_COLOR:1
                                    \once \override ViolinMusicStaff.Clef.color = #(x11-color 'DarkViolet) %%! TEMPLATE_CLEF_COLOR:7
                                    %%% \override ViolinMusicStaff.Clef.color = ##f        %%! TEMPLATE_CLEF_UNCOLOR:8
                                    e'8
                                    [
                                    ^ \markup {
                                        \column
                                            {
                                                %%% \line                                  %%! TEMPLATE_INSTRUMENT_ALERT:2
                                                %%%     {                                  %%! TEMPLATE_INSTRUMENT_ALERT:2
                                                %%%         \vcenter                       %%! TEMPLATE_INSTRUMENT_ALERT:2
                                                %%%             (Violin                    %%! TEMPLATE_INSTRUMENT_ALERT:2
                                                %%%         \vcenter                       %%! TEMPLATE_INSTRUMENT_ALERT:2
                                                %%%             \hcenter-in                %%! TEMPLATE_INSTRUMENT_ALERT:2
                                                %%%                 #10                    %%! TEMPLATE_INSTRUMENT_ALERT:2
                                                %%%                 Violin                 %%! TEMPLATE_INSTRUMENT_ALERT:2
                                                %%%         \concat                        %%! TEMPLATE_INSTRUMENT_ALERT:2
                                                %%%             {                          %%! TEMPLATE_INSTRUMENT_ALERT:2
                                                %%%                 \vcenter               %%! TEMPLATE_INSTRUMENT_ALERT:2
                                                %%%                     \hcenter-in        %%! TEMPLATE_INSTRUMENT_ALERT:2
                                                %%%                         #10            %%! TEMPLATE_INSTRUMENT_ALERT:2
                                                %%%                         Vn.            %%! TEMPLATE_INSTRUMENT_ALERT:2
                                                %%%                 \vcenter               %%! TEMPLATE_INSTRUMENT_ALERT:2
                                                %%%                     )                  %%! TEMPLATE_INSTRUMENT_ALERT:2
                                                %%%             }                          %%! TEMPLATE_INSTRUMENT_ALERT:2
                                                %%%     }                                  %%! TEMPLATE_INSTRUMENT_ALERT:2
                                                \line                                      %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                    {                                      %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                        \with-color                        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                            #(x11-color 'DarkViolet)       %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                            {                              %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                \vcenter                   %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                    (Violin                %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                \vcenter                   %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                    \hcenter-in            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                        #10                %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                        Violin             %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                \concat                    %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                    {                      %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                        \vcenter           %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                            \hcenter-in    %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                                #10        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                                Vn.        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                        \vcenter           %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                            )              %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                    }                      %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                            }                              %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                    }                                      %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                            }
                                        }
                                    \set ViolinMusicStaff.instrumentName = \markup {       %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                        \hcenter-in                                        %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                            #10                                            %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                            Violin                                         %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                        }                                                  %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                    \set ViolinMusicStaff.shortInstrumentName = \markup {  %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                        \hcenter-in                                        %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                            #10                                            %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                            Vn.                                            %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                        }                                                  %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                    \override ViolinMusicStaff.InstrumentName.color = #(x11-color 'violet) %%! TEMPLATE_REDRAW_INSTRUMENT_COLOR:5
                                    \override ViolinMusicStaff.Clef.color = #(x11-color 'violet) %%! TEMPLATE_CLEF_COLOR_REDRAW:11
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
                                \set ViolaMusicStaff.instrumentName = \markup {            %%! TEMPLATE_INSTRUMENT:4
                                    \hcenter-in                                            %%! TEMPLATE_INSTRUMENT:4
                                        #10                                                %%! TEMPLATE_INSTRUMENT:4
                                        Viola                                              %%! TEMPLATE_INSTRUMENT:4
                                    }                                                      %%! TEMPLATE_INSTRUMENT:4
                                \set ViolaMusicStaff.shortInstrumentName = \markup {       %%! TEMPLATE_INSTRUMENT:4
                                    \hcenter-in                                            %%! TEMPLATE_INSTRUMENT:4
                                        #10                                                %%! TEMPLATE_INSTRUMENT:4
                                        Va.                                                %%! TEMPLATE_INSTRUMENT:4
                                    }                                                      %%! TEMPLATE_INSTRUMENT:4
                                \set ViolaMusicStaff.forceClef = ##t                       %%! TEMPLATE_CLEF:9
                                \clef "alto"                                               %%! TEMPLATE_CLEF:10
                                \once \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %%! TEMPLATE_INSTRUMENT_COLOR:1
                                \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %%! TEMPLATE_CLEF_COLOR:7
                                %%% \override ViolaMusicStaff.Clef.color = ##f             %%! TEMPLATE_CLEF_UNCOLOR:8
                                R1 * 1/2
                                ^ \markup {
                                    \column
                                        {
                                            %%% \line                                      %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%     {                                      %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%         \vcenter                           %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%             (Viola                         %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%         \vcenter                           %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%             \hcenter-in                    %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%                 #10                        %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%                 Viola                      %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%         \concat                            %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%             {                              %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%                 \vcenter                   %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%                     \hcenter-in            %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%                         #10                %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%                         Va.                %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%                 \vcenter                   %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%                     )                      %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%             }                              %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%     }                                      %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            \line                                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                {                                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                    \with-color                            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                        #(x11-color 'DarkViolet)           %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                        {                                  %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                            \vcenter                       %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                (Viola                     %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                            \vcenter                       %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                \hcenter-in                %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                    #10                    %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                    Viola                  %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                            \concat                        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                {                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                    \vcenter               %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                        \hcenter-in        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                            #10            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                            Va.            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                    \vcenter               %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                        )                  %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                }                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                        }                                  %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                }                                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                        }
                                    }
                                \set ViolaMusicStaff.instrumentName = \markup {            %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                    \hcenter-in                                            %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                        #10                                                %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                        Viola                                              %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                    }                                                      %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                \set ViolaMusicStaff.shortInstrumentName = \markup {       %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                    \hcenter-in                                            %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                        #10                                                %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                        Va.                                                %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                    }                                                      %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                \override ViolaMusicStaff.InstrumentName.color = #(x11-color 'violet) %%! TEMPLATE_REDRAW_INSTRUMENT_COLOR:5
                                \override ViolaMusicStaff.Clef.color = #(x11-color 'violet) %%! TEMPLATE_CLEF_COLOR_REDRAW:11
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
                                \set CelloMusicStaff.instrumentName = \markup {            %%! TEMPLATE_INSTRUMENT:4
                                    \hcenter-in                                            %%! TEMPLATE_INSTRUMENT:4
                                        #10                                                %%! TEMPLATE_INSTRUMENT:4
                                        Cello                                              %%! TEMPLATE_INSTRUMENT:4
                                    }                                                      %%! TEMPLATE_INSTRUMENT:4
                                \set CelloMusicStaff.shortInstrumentName = \markup {       %%! TEMPLATE_INSTRUMENT:4
                                    \hcenter-in                                            %%! TEMPLATE_INSTRUMENT:4
                                        #10                                                %%! TEMPLATE_INSTRUMENT:4
                                        Vc.                                                %%! TEMPLATE_INSTRUMENT:4
                                    }                                                      %%! TEMPLATE_INSTRUMENT:4
                                \set CelloMusicStaff.forceClef = ##t                       %%! TEMPLATE_CLEF:9
                                \clef "bass"                                               %%! TEMPLATE_CLEF:10
                                \once \override CelloMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %%! TEMPLATE_INSTRUMENT_COLOR:1
                                \once \override CelloMusicStaff.Clef.color = #(x11-color 'DarkViolet) %%! TEMPLATE_CLEF_COLOR:7
                                %%% \override CelloMusicStaff.Clef.color = ##f             %%! TEMPLATE_CLEF_UNCOLOR:8
                                R1 * 1/2
                                ^ \markup {
                                    \column
                                        {
                                            %%% \line                                      %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%     {                                      %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%         \vcenter                           %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%             (Cello                         %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%         \vcenter                           %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%             \hcenter-in                    %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%                 #10                        %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%                 Cello                      %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%         \concat                            %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%             {                              %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%                 \vcenter                   %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%                     \hcenter-in            %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%                         #10                %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%                         Vc.                %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%                 \vcenter                   %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%                     )                      %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%             }                              %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            %%%     }                                      %%! TEMPLATE_INSTRUMENT_ALERT:2
                                            \line                                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                {                                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                    \with-color                            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                        #(x11-color 'DarkViolet)           %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                        {                                  %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                            \vcenter                       %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                (Cello                     %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                            \vcenter                       %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                \hcenter-in                %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                    #10                    %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                    Cello                  %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                            \concat                        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                {                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                    \vcenter               %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                        \hcenter-in        %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                            #10            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                            Vc.            %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                    \vcenter               %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                        )                  %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                                }                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                        }                                  %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                                }                                          %%! TEMPLATE_INSTRUMENT_ALERT_WITH_COLOR:3
                                        }
                                    }
                                \set CelloMusicStaff.instrumentName = \markup {            %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                    \hcenter-in                                            %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                        #10                                                %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                        Cello                                              %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                    }                                                      %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                \set CelloMusicStaff.shortInstrumentName = \markup {       %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                    \hcenter-in                                            %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                        #10                                                %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                        Vc.                                                %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                    }                                                      %%! TEMPLATE_REDRAW_INSTRUMENT:6
                                \override CelloMusicStaff.InstrumentName.color = #(x11-color 'violet) %%! TEMPLATE_REDRAW_INSTRUMENT_COLOR:5
                                \override CelloMusicStaff.Clef.color = #(x11-color 'violet) %%! TEMPLATE_CLEF_COLOR_REDRAW:11
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
