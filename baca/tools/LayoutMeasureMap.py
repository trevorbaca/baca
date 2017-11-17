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
        ...     baca.scope('Violin Music Voice', 1),
        ...     baca.make_even_runs(),
        ...     baca.pitches('E4', repeats=True),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin.viola.cello
                \context GlobalContext = "Global Context" <<
                    \context GlobalSkips = "Global Skips" {
            <BLANKLINE>
                        %%% Global Skips [measure 1] %%%
                        \time 4/8
                        s1 * 1/2
                        \break
            <BLANKLINE>
                        %%% Global Skips [measure 2] %%%
                        \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details
                        #'((Y-offset . 100) (alignment-distances . (30 30)))
                        \time 3/8
                        s1 * 3/8
                        \break
            <BLANKLINE>
                        %%% Global Skips [measure 3] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% Global Skips [measure 4] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% Global Skips [measure 5] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \context StringSectionStaffGroup = "String Section Staff Group" <<
                        \tag violin
                        \context ViolinMusicStaff = "Violin Music Staff" {
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
            <BLANKLINE>
                                    %%% Violin Music Voice [measure 1] %%%
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
                                    %%% Violin Music Voice [measure 2] %%%
                                    e'8 [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8 ]
                                }
                                {
            <BLANKLINE>
                                    %%% Violin Music Voice [measure 3] %%%
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
                                    %%% Violin Music Voice [measure 4] %%%
                                    e'8 [
            <BLANKLINE>
                                    e'8
            <BLANKLINE>
                                    e'8 ]
                                }
                                {
            <BLANKLINE>
                                    %%% Violin Music Voice [measure 5] %%%
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
                        \context ViolaMusicStaff = "Viola Music Staff" {
                            \context ViolaMusicVoice = "Viola Music Voice" {
            <BLANKLINE>
                                %%% Viola Music Voice [measure 1] %%%
                                \set ViolaMusicStaff.instrumentName = \markup { Viola }
                                \set ViolaMusicStaff.shortInstrumentName = \markup { Va. }
                                \clef "alto"
                                R1 * 1/2
            <BLANKLINE>
                                %%% Viola Music Voice [measure 2] %%%
                                R1 * 3/8
            <BLANKLINE>
                                %%% Viola Music Voice [measure 3] %%%
                                R1 * 1/2
            <BLANKLINE>
                                %%% Viola Music Voice [measure 4] %%%
                                R1 * 3/8
            <BLANKLINE>
                                %%% Viola Music Voice [measure 5] %%%
                                R1 * 1/2
                                \bar "|"
            <BLANKLINE>
                            }
                        }
                        \tag cello
                        \context CelloMusicStaff = "Cello Music Staff" {
                            \context CelloMusicVoice = "Cello Music Voice" {
            <BLANKLINE>
                                %%% Cello Music Voice [measure 1] %%%
                                \set CelloMusicStaff.instrumentName = \markup { Cello }
                                \set CelloMusicStaff.shortInstrumentName = \markup { Vc. }
                                \clef "bass"
                                R1 * 1/2
            <BLANKLINE>
                                %%% Cello Music Voice [measure 2] %%%
                                R1 * 3/8
            <BLANKLINE>
                                %%% Cello Music Voice [measure 3] %%%
                                R1 * 1/2
            <BLANKLINE>
                                %%% Cello Music Voice [measure 4] %%%
                                R1 * 3/8
            <BLANKLINE>
                                %%% Cello Music Voice [measure 5] %%%
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
        '_items',
        '_tag',
        )

    ### INITIALIZER ###

    def __init__(self, items=None, tag=None):
        if tag is not None:
            assert isinstance(tag, str), repr(tag)
        self._tag = tag
        if items is not None:
            if tag is not None:
                items_ = []
                for item in items:
                    lbsd = item.indicators[0]
                    lbsd = abjad.new(lbsd, tag=tag)
                    item_ = baca.IndicatorCommand(
                        indicators=[lbsd],
                        selector=item.selector,
                        )
                    items_.append(item_)
                items = items_
            items = tuple(items)
        self._items = items

    ### SPECIAL METHODS ###

    def __call__(self, context=None):
        r'''Calls map on `context`.

        Returns none.
        '''
        if context is None:
            return
        for indicator in self.items:
            indicator(context)

    def __getitem__(self, argument):
        r'''Gets `argument`.

        ..  container:: example

            >>> layout = baca.LayoutMeasureMap([
            ...     baca.line_break(baca.skip(0)),
            ...     baca.page_break(baca.skip(1)),
            ...     ])

            >>> layout[1]
            IndicatorCommand(indicators=CyclicTuple([PageBreak()]), selector=baca.skip(1))

        Returns item.
        '''
        return self.items.__getitem__(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        r'''Gets items.

        ..  container:: example

            >>> layout = baca.LayoutMeasureMap([
            ...     baca.line_break(baca.skip(0)),
            ...     baca.page_break(baca.skip(1)),
            ...     ])

            >>> for item in layout.items:
            ...     item
            IndicatorCommand(indicators=CyclicTuple([SystemBreak()]), selector=baca.skip(0))
            IndicatorCommand(indicators=CyclicTuple([PageBreak()]), selector=baca.skip(1))

        Returns items.
        '''
        return self._items

    @property
    def tag(self):
        r'''Gets tag.
        '''
        return self._tag
