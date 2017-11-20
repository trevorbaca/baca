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
        ...         ],
        ...         tag='SEGMENT',
        ...         ),
        ...     )

        >>> maker(
        ...     baca.scope('ViolinMusicVoice', 1),
        ...     baca.make_even_runs(),
        ...     baca.pitches('E4', repeats=True),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin.viola.cello
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \time 4/8
                        s1 * 1/2
                        \break % SEGMENT
            <BLANKLINE>
                        %%% GlobalSkips [measure 2] %%%
                        \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details #'((Y-offset . 100) (alignment-distances . (30 30))) % SEGMENT
                        \time 3/8
                        s1 * 3/8
                        \break % SEGMENT
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 5] %%%
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
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
                                    e'8 [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8 ]
                                }
                                {
            <BLANKLINE>
                                    %%% ViolinMusicVoice [measure 2] %%%
                                    e'8 [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8 ]
                                }
                                {
            <BLANKLINE>
                                    %%% ViolinMusicVoice [measure 3] %%%
                                    e'8 [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8 ]
                                }
                                {
            <BLANKLINE>
                                    %%% ViolinMusicVoice [measure 4] %%%
                                    e'8 [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8 ]
                                }
                                {
            <BLANKLINE>
                                    %%% ViolinMusicVoice [measure 5] %%%
                                    e'8 [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8 ]
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
                                \set ViolaMusicStaff.instrumentName = \markup { Viola }
                                \set ViolaMusicStaff.shortInstrumentName = \markup { Va. }
                                \clef "alto"
                                R1 * 1/2
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
                                \set CelloMusicStaff.instrumentName = \markup { Cello }
                                \set CelloMusicStaff.shortInstrumentName = \markup { Vc. }
                                \clef "bass"
                                R1 * 1/2
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
        '_commands',
        '_tag',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, commands=None, tag=None):
        if tag is not None:
            assert isinstance(tag, str), repr(tag)
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

    def __getitem__(self, argument):
        r'''Gets `argument`.

        ..  container:: example

            >>> layout = baca.LayoutMeasureMap([
            ...     baca.line_break(baca.skip(0)),
            ...     baca.page_break(baca.skip(1)),
            ...     ])

            >>> abjad.f(layout[1])
            baca.IndicatorCommand(
                indicators=abjad.CyclicTuple(
                    [
                        abjad.PageBreak(
                            format_slot='closing',
                            ),
                        ]
                    ),
                selector=baca.skip(1),
                )

        Returns item.
        '''
        return self.commands.__getitem__(argument)

    ### PUBLIC PROPERTIES ###

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
            IndicatorCommand(indicators=CyclicTuple([LineBreak(format_slot='closing')]), selector=baca.skip(0))
            IndicatorCommand(indicators=CyclicTuple([PageBreak(format_slot='closing')]), selector=baca.skip(1))

        Returns commands.
        '''
        return self._commands

    @property
    def tag(self):
        r'''Gets tag.
        '''
        return self._tag
