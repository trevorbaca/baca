import abjad


class TempoSpecifier(abjad.AbjadObject):
    r'''MetronomeMark specifier.

    ::

        >>> import baca

    ..  container:: example

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     measures_per_stage=[2, 2],
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     tempo_specifier=baca.TempoSpecifier([
            ...         (1, abjad.MetronomeMark((1, 4), 90)),
            ...         (2, abjad.MetronomeMark((1, 4), 72)),
            ...         ]),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_commands(
            ...     'vn',
            ...     baca.select_stages(1),
            ...     baca.pitches('E4 F4'),
            ...     baca.even_runs(),
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Score])
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
                            s1 * 1/2 ^ \markup {
                                \fontsize
                                    #-6
                                    \general-align
                                        #Y
                                        #DOWN
                                        \note-by-number
                                            #2
                                            #0
                                            #1
                                \upright
                                    {
                                        =
                                        90
                                    }
                                }
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 4/8
                            s1 * 1/2 ^ \markup {
                                \fontsize
                                    #-6
                                    \general-align
                                        #Y
                                        #DOWN
                                        \note-by-number
                                            #2
                                            #0
                                            #1
                                \upright
                                    {
                                        =
                                        72
                                    }
                                }
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
                            {
                                \set Staff.instrumentName = \markup { Violin }
                                \set Staff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
                                e'8 [
                                f'8
                                e'8
                                f'8 ]
                            }
                            {
                                e'8 [
                                f'8
                                e'8 ]
                            }
                            s1 * 7/8
                            \bar "|"
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

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
        r'''Gets pair or pair slice identified by `argument`.

        ..  container:: example

            Gets pair 1:

            ::

                >>> tempo_specifier = baca.TempoSpecifier([
                ...     (1, abjad.MetronomeMark((1, 4), 90)),
                ...     (1, abjad.Accelerando()),
                ...     (4, abjad.MetronomeMark((1, 4), 120)),
                ...     ])

            ::

                >>> tempo_specifier[1]
                (1, Accelerando())

        Returns pair or slice of pairs.
        '''
        return self.items.__getitem__(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        r'''Gets items.

        ..  container:: example

            Gets items:

            ::

                >>> tempo_specifier = baca.TempoSpecifier([
                ...     (1, abjad.MetronomeMark((1, 4), 90)),
                ...     (1, abjad.Accelerando()),
                ...     (4, abjad.MetronomeMark((1, 4), 120)),
                ...     ])

            ::

                >>> for item in tempo_specifier.items:
                ...     item
                (1, MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=90))
                (1, Accelerando())
                (4, MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=120))

        Defaults to none.

        Set to tuple or none.

        Returns tuple or none.
        '''
        return self._items
