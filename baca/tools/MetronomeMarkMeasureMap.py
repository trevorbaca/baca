import abjad


class MetronomeMarkMeasureMap(abjad.AbjadObject):
    r'''Metronome mark measure map.

    ..  container:: example

        >>> maker = baca.SegmentMaker(
        ...     measures_per_stage=[2, 2],
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     metronome_mark_measure_map=baca.MetronomeMarkMeasureMap([
        ...         (1, abjad.MetronomeMark((1, 4), 90)),
        ...         (2, abjad.MetronomeMark((1, 4), 72)),
        ...         ]),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.pitches('E4 F4'),
        ...     baca.make_even_runs(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \time 4/8
                        \bar "" % SEGMENT:EMPTY-BAR:1
                        s1 * 1/2
                            ^ \markup { % CLOCK-TIME:3
                                \fontsize % CLOCK-TIME:3
                                    #-2 % CLOCK-TIME:3
                                    0'00'' % CLOCK-TIME:3
                                } % CLOCK-TIME:3
                            - \markup { % STAGE-NUMBER:2
                                \fontsize % STAGE-NUMBER:2
                                    #-3 % STAGE-NUMBER:2
                                    \with-color % STAGE-NUMBER:2
                                        #(x11-color 'DarkCyan) % STAGE-NUMBER:2
                                        [1] % STAGE-NUMBER:2
                                } % STAGE-NUMBER:2
                            ^ \markup {
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
            <BLANKLINE>
                        %%% GlobalSkips [measure 2] %%%
                        \time 3/8
                        s1 * 3/8
                            ^ \markup { % CLOCK-TIME:1
                                \fontsize % CLOCK-TIME:1
                                    #-2 % CLOCK-TIME:1
                                    0'01'' % CLOCK-TIME:1
                                } % CLOCK-TIME:1
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 4/8
                        s1 * 1/2
                            ^ \markup { % CLOCK-TIME:2
                                \fontsize % CLOCK-TIME:2
                                    #-2 % CLOCK-TIME:2
                                    0'02'' % CLOCK-TIME:2
                                } % CLOCK-TIME:2
                            - \markup { % STAGE-NUMBER:1
                                \fontsize % STAGE-NUMBER:1
                                    #-3 % STAGE-NUMBER:1
                                    \with-color % STAGE-NUMBER:1
                                        #(x11-color 'DarkCyan) % STAGE-NUMBER:1
                                        [2] % STAGE-NUMBER:1
                                } % STAGE-NUMBER:1
                            ^ \markup {
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
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 3/8
                        s1 * 3/8
                            ^ \markup { % CLOCK-TIME:1
                                \fontsize % CLOCK-TIME:1
                                    #-2 % CLOCK-TIME:1
                                    0'04'' % CLOCK-TIME:1
                                } % CLOCK-TIME:1
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                \clef "treble" % SEGMENT:EXPLICIT-CLEF:2
                                \override Staff.Clef.color = #(x11-color 'black) % SEGMENT:EXPLICIT-CLEF:COLOR:1
                                e'8 [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e'8
            <BLANKLINE>
                                f'8 ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                e'8 [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e'8 ]
                            }
            <BLANKLINE>
                            %%% MusicVoice [measure 3] %%%
                            R1 * 1/2
            <BLANKLINE>
                            %%% MusicVoice [measure 4] %%%
                            R1 * 3/8
                            \bar "|"
            <BLANKLINE>
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

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

            >>> marks = baca.MetronomeMarkMeasureMap([
            ...     (1, abjad.MetronomeMark((1, 4), 90)),
            ...     (1, abjad.Accelerando()),
            ...     (4, abjad.MetronomeMark((1, 4), 120)),
            ...     ])

            >>> marks[1]
            (1, Accelerando())

        Returns item.
        '''
        return self.items.__getitem__(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        r'''Gets items.

        ..  container:: example

            >>> marks = baca.MetronomeMarkMeasureMap([
            ...     (1, abjad.MetronomeMark((1, 4), 90)),
            ...     (1, abjad.Accelerando()),
            ...     (4, abjad.MetronomeMark((1, 4), 120)),
            ...     ])

            >>> for item in marks.items:
            ...     item
            (1, MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=90))
            (1, Accelerando())
            (4, MetronomeMark(reference_duration=Duration(1, 4), units_per_minute=120))

        Defaults to none.

        Set to tuple or none.

        Returns tuple or none.
        '''
        return self._items
