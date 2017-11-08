import abjad


class LayoutMeasureMap(abjad.AbjadObject):
    r'''Layout measure map.

    ..  container:: example

        >>> segment_maker = baca.SegmentMaker(
        ...     score_template=baca.ViolinSoloScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     layout_measure_map=baca.LayoutMeasureMap([
        ...         baca.line_break(baca.components(abjad.Measure)[0]),
        ...         baca.page_break(baca.components(abjad.Measure)[1]),
        ...         ]),
        ...     )

        >>> segment_maker(
        ...     baca.scope('Violin Music Voice', 1),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches('E4', repeats=True),
        ...     )

        >>> result = segment_maker.run(is_doc_example=True)
        >>> lilypond_file, metadata = result
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
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
                    }
                    \context GlobalSkips = "Global Skips" {
                        {
                            \time 4/8
                            s1 * 1/2
                            \break
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                            \pageBreak
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            \set ViolinMusicStaff.instrumentName = \markup { Violin }
                            \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                            \clef "treble"
                            e'2
                            e'4.
                            e'2
                            e'4.
                            \bar "|"
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

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
            ...     baca.line_break(baca.logical_measure(0)),
            ...     baca.line_break(baca.logical_measure(1)),
            ...     baca.page_break(baca.logical_measure(2)),
            ...     ])

            >>> layout[1]
            IndicatorCommand(indicators=CyclicTuple([SystemBreak()]), selector=baca.logical_measure(1))

        Returns item.
        '''
        return self.items.__getitem__(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        r'''Gets items.

        ..  container:: example

            >>> layout = baca.LayoutMeasureMap([
            ...     baca.line_break(baca.logical_measure(0)),
            ...     baca.line_break(baca.logical_measure(1)),
            ...     baca.page_break(baca.logical_measure(2)),
            ...     ])

            >>> for item in layout.items:
            ...     item
            IndicatorCommand(indicators=CyclicTuple([SystemBreak()]), selector=baca.logical_measure(0))
            IndicatorCommand(indicators=CyclicTuple([SystemBreak()]), selector=baca.logical_measure(1))
            IndicatorCommand(indicators=CyclicTuple([PageBreak()]), selector=baca.logical_measure(2))

        Returns items.
        '''
        return self._items
