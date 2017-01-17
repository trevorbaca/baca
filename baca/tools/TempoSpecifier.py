# -*- coding: utf-8 -*-
import abjad


class TempoSpecifier(abjad.abctools.AbjadObject):
    r'''Tempo specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        ::

            >>> segment_maker = baca.tools.SegmentMaker(
            ...     measures_per_stage=[2, 2],
            ...     score_template=baca.tools.ViolinSoloScoreTemplate(),
            ...     tempo_specifier=baca.tools.TempoSpecifier([
            ...         (1, Tempo(Duration(1, 4), 90)),
            ...         (2, Tempo(Duration(1, 4), 72)),
            ...         ]),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.append_specifiers(
            ...     ('vn', baca.select.stages(1)),
            ...     [
            ...         baca.pitch.pitches('E4 F4'),
            ...         baca.rhythm.make_even_run_rhythm_specifier(),
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
                        \clef "treble"
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
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
        r'''Gets item.

        ..  container:: example

            Gets item 1:

            ::

                >>> tempo_specifier = baca.tools.TempoSpecifier([
                ...     (1, Tempo(Duration(1, 4), 90)),
                ...     (1, Accelerando()),
                ...     (4, Tempo(Duration(1, 4), 120)),
                ...     ])

            ::

                >>> tempo_specifier[1]
                (1, Accelerando())

        Returns item.
        '''
        return self.items.__getitem__(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        r'''Gets items.

        ..  container:: example

            Gets items:

            ::

                >>> tempo_specifier = baca.tools.TempoSpecifier([
                ...     (1, Tempo(Duration(1, 4), 90)),
                ...     (1, Accelerando()),
                ...     (4, Tempo(Duration(1, 4), 120)),
                ...     ])

            ::

                >>> for item in tempo_specifier.items:
                ...     item
                (1, Tempo(reference_duration=Duration(1, 4), units_per_minute=90))
                (1, Accelerando())
                (4, Tempo(reference_duration=Duration(1, 4), units_per_minute=120))

        Defaults to none.

        Set to tuple or none.

        Returns tuple or none.
        '''
        return self._items
