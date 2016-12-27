# -*- coding: utf-8 -*-
import abjad


class VoltaSpecifier(abjad.abctools.AbjadObject):
    r'''Volta specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     volta_specifier=baca.tools.VoltaSpecifier([
            ...         baca.tools.MeasureExpression(1, 3),
            ...         ]),
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.select.stages(1)),
            ...     [
            ...         baca.pitch.pitches('E4', allow_repeated_pitches=True),
            ...         baca.rhythm.make_messiaen_note_rhythm_specifier(),
            ...         ],
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
            >>> lilypond_file, segment_metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  doctest::

            >>> f(lilypond_file[Score])
            \context Score = "Score" <<
                \tag violin
                \context TimeSignatureContext = "Time Signature Context" <<
                    \context TimeSignatureContextMultimeasureRests = "Time Signature Context Multimeasure Rests" {
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
                    \context TimeSignatureContextSkips = "Time Signature Context Skips" {
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
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
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

    def __getitem__(self, expr):
        r'''Gets item.

        ..  container:: example

            Gets items:

            ::

                >>> volta_specifier = baca.tools.VoltaSpecifier([
                ...     baca.tools.MeasureExpression(2, 4),
                ...     baca.tools.MeasureExpression(16, 18),
                ...     ])

            ::

                >>> volta_specifier[1]
                MeasureExpression(start_number=16, stop_number=18)

        Returns item.
        '''
        return self.items.__getitem__(expr)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        r'''Gets items.

        ..  container:: example

            Gets items:

            ::

                >>> volta_specifier = baca.tools.VoltaSpecifier([
                ...     baca.tools.MeasureExpression(2, 4),
                ...     baca.tools.MeasureExpression(16, 18),
                ...     ])

            ::

                >>> for item in volta_specifier.items:
                ...     item
                MeasureExpression(start_number=2, stop_number=4)
                MeasureExpression(start_number=16, stop_number=18)

        Defaults to none.

        Set to tuple or none.

        Returns tuple or none.
        '''
        return self._items
