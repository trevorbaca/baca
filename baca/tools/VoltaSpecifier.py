import abjad


class VoltaSpecifier(abjad.AbjadObject):
    r'''Volta specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     volta_specifier=baca.VoltaSpecifier([
            ...         baca.MeasureExpression(1, 3),
            ...         ]),
            ...     )

        ::

            >>> specifiers = segment_maker.append_commands(
            ...     'vn',
            ...     baca.select_stages(1),
            ...     baca.pitches('E4', allow_repeat_pitches=True),
            ...     baca.messiaen_notes(),
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
                            s1 * 1/2
                        }
                        \repeat volta 2
                        {
                            {
                                \time 3/8
                                s1 * 3/8
                            }
                            {
                                \time 4/8
                                s1 * 1/2
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
                            \set Staff.instrumentName = \markup { Violin }
                            \set Staff.shortInstrumentName = \markup { Vn. }
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
        r'''Gets measure expression or slice of measure expressions
        identified by `argument`.

        ..  container:: example

            Gets measure expression:

            ::

                >>> volta_specifier = baca.VoltaSpecifier([
                ...     baca.MeasureExpression(2, 4),
                ...     baca.MeasureExpression(16, 18),
                ...     ])

            ::

                >>> volta_specifier[1]
                MeasureExpression(start=16, stop=18)

        Returns measure expression or slice of measure expression.
        '''
        return self.items.__getitem__(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        r'''Gets items.

        ..  container:: example

            Gets items:

            ::

                >>> volta_specifier = baca.VoltaSpecifier([
                ...     baca.MeasureExpression(2, 4),
                ...     baca.MeasureExpression(16, 18),
                ...     ])

            ::

                >>> for item in volta_specifier.items:
                ...     item
                MeasureExpression(start=2, stop=4)
                MeasureExpression(start=16, stop=18)

        Defaults to none.

        Set to tuple or none.

        Returns tuple or none.
        '''
        return self._items
