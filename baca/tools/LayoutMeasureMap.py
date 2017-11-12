import abjad


class LayoutMeasureMap(abjad.AbjadObject):
    r'''Layout measure map.

    ..  container:: example

        >>> measures = baca.components
        >>> segment_maker = baca.SegmentMaker(
        ...     score_template=baca.StringTrioScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8), (4, 8)],
        ...     layout_measure_map=baca.LayoutMeasureMap([
        ...         baca.line_break(baca.measure(0)),
        ...         baca.lbsd(100, [30, 30], baca.measure(1)),
        ...         baca.line_break(baca.measure(1)),
        ...         ]),
        ...     )

        >>> segment_maker(
        ...     baca.scope('Violin Music Voice', 1),
        ...     baca.make_even_runs(),
        ...     baca.pitches('E4', repeats=True),
        ...     )

        >>> result = segment_maker.run(environment='docs')
        >>> lilypond_file, metadata = result
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin.viola.cello
                \context GlobalContext = "Global Context" <<
                    \context GlobalRests = "Global Rests" {
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                        {
                            \time 3/8
                            R1 * 3/8
                        }
                        {
                            \time 4/8
                            R1 * 1/2
                        }
                    }
                    \context GlobalSkips = "Global Skips" {
                        {
                            s1 * 1/2
                            \break
                        }
                        {
                            \time 3/8
                            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details
                            #'((Y-offset . 100) (alignment-distances . (30 30)))
                            s1 * 3/8
                            \break
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \context StringSectionStaffGroup = "String Section Staff Group" <<
                        \tag violin
                        \context ViolinMusicStaff = "Violin Music Staff" {
                            \context ViolinMusicVoice = "Violin Music Voice" {
                                {
                                    \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                    \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                    \clef "treble"
                                    e'8 [
                                    e'8
                                    e'8
                                    e'8 ]
                                }
                                {
                                    e'8 [
                                    e'8
                                    e'8 ]
                                }
                                {
                                    e'8 [
                                    e'8
                                    e'8
                                    e'8 ]
                                }
                                {
                                    e'8 [
                                    e'8
                                    e'8 ]
                                }
                                {
                                    e'8 [
                                    e'8
                                    e'8
                                    e'8 ]
                                    \bar "|"
                                }
                            }
                        }
                        \tag viola
                        \context ViolaMusicStaff = "Viola Music Staff" {
                            \context ViolaMusicVoice = "Viola Music Voice" {
                                \set ViolaMusicStaff.instrumentName = \markup { Viola }
                                \set ViolaMusicStaff.shortInstrumentName = \markup { Va. }
                                \clef "alto"
                                R1 * 1/2
                                R1 * 3/8
                                R1 * 1/2
                                R1 * 3/8
                                R1 * 1/2
                                \bar "|"
                            }
                        }
                        \tag cello
                        \context CelloMusicStaff = "Cello Music Staff" {
                            \context CelloMusicVoice = "Cello Music Voice" {
                                \set CelloMusicStaff.instrumentName = \markup { Cello }
                                \set CelloMusicStaff.shortInstrumentName = \markup { Vc. }
                                \clef "bass"
                                R1 * 1/2
                                R1 * 3/8
                                R1 * 1/2
                                R1 * 3/8
                                R1 * 1/2
                                \bar "|"
                            }
                        }
                    >>
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(6) Utilities'

    __slots__ = (
        '_items',
        )

    ### INITIALIZER ###

    def __init__(self, items=None):
        if items is not None:
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
            ...     baca.line_break(baca.measure(0)),
            ...     baca.page_break(baca.measure(1)),
            ...     ])

            >>> layout[1]
            IndicatorCommand(indicators=CyclicTuple([PageBreak()]), selector=baca.measure(1))

        Returns item.
        '''
        return self.items.__getitem__(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        r'''Gets items.

        ..  container:: example

            >>> layout = baca.LayoutMeasureMap([
            ...     baca.line_break(baca.measure(0)),
            ...     baca.page_break(baca.measure(1)),
            ...     ])

            >>> for item in layout.items:
            ...     item
            IndicatorCommand(indicators=CyclicTuple([SystemBreak()]), selector=baca.measure(0))
            IndicatorCommand(indicators=CyclicTuple([PageBreak()]), selector=baca.measure(1))

        Returns items.
        '''
        return self._items
