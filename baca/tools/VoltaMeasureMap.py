import abjad


class VoltaMeasureMap(abjad.AbjadObject):
    r'''Volta measure map.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     volta_measure_map=baca.VoltaMeasureMap([
        ...         baca.MeasureSpecifier(1, 3),
        ...         ]),
        ...     )

        >>> maker(
        ...     baca.scope('Music Voice', 1),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.pitches('E4', repeats=True),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \context GlobalContext = "Global Context" <<
                    \context GlobalSkips = "Global Skips" {
                        \time 4/8
                        s1 * 1/2
                        \repeat volta 2
                        {
                                \time 3/8
                                s1 * 3/8
                                \time 4/8
                                s1 * 1/2
                        }
                        \time 3/8
                        s1 * 3/8
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \context Staff = "Music Staff" {
                        \context Voice = "Music Voice" {
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

    def __getitem__(self, argument):
        r'''Gets `argument`.

        ..  container:: example

            >>> voltas = baca.VoltaMeasureMap([
            ...     baca.MeasureSpecifier(2, 4),
            ...     baca.MeasureSpecifier(16, 18),
            ...     ])

            >>> voltas[1]
            MeasureSpecifier(start=16, stop=18)

        Returns item.
        '''
        return self.items.__getitem__(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        r'''Gets items.

        ..  container:: example

            >>> voltas = baca.VoltaMeasureMap([
            ...     baca.MeasureSpecifier(2, 4),
            ...     baca.MeasureSpecifier(16, 18),
            ...     ])

            >>> for item in voltas.items:
            ...     item
            MeasureSpecifier(start=2, stop=4)
            MeasureSpecifier(start=16, stop=18)

        Returns items.
        '''
        return self._items
