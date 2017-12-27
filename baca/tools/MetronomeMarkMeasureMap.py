import abjad


class MetronomeMarkMeasureMap(abjad.AbjadObject):
    r'''Metronome mark measure map.

    ..  container:: example

        >>> metronome_marks = abjad.MetronomeMarkDictionary()
        >>> metronome_marks['72'] = abjad.MetronomeMark((1, 4), 72)
        >>> metronome_marks['90'] = abjad.MetronomeMark((1, 4), 90)
        >>> maker = baca.SegmentMaker(
        ...     measures_per_stage=[2, 2],
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     metronome_mark_measure_map=baca.MetronomeMarkMeasureMap([
        ...         (1, metronome_marks['90']),
        ...         (2, metronome_marks['72']),
        ...         ]),
        ...     metronome_marks=metronome_marks,
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.pitches('E4 F4'),
        ...     baca.make_even_runs(),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=True)
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \time 4/8
                        \bar ""        %%! EMPTY_START_BAR:1
                        s1 * 1/2
                        ^ \markup {
                            \column
                                {
                                    \line                                          %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                        {                                          %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                            \with-color                            %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                                #(x11-color 'blue)                 %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                                {                                  %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                                    \fontsize                      %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                                        #-6                        %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                                        \general-align             %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                                            #Y                     %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                                            #DOWN                  %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                                            \note-by-number        %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                                                #2                 %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                                                #0                 %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                                                #1                 %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                                    \upright                       %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                                        {                          %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                                            =                      %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                                            90                     %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                                        }                          %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                                }                                  %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                        }                                          %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:3
                                    \line                     %%! CLOCK_TIME_MARKUP:5
                                        {                     %%! CLOCK_TIME_MARKUP:5
                                            \fontsize         %%! CLOCK_TIME_MARKUP:5
                                                #-2           %%! CLOCK_TIME_MARKUP:5
                                                0'00''        %%! CLOCK_TIME_MARKUP:5
                                        }                     %%! CLOCK_TIME_MARKUP:5
                                }
                            }
                        - \markup {                               %%! STAGE_NUMBER_MARKUP:2
                            \fontsize                             %%! STAGE_NUMBER_MARKUP:2
                                #-3                               %%! STAGE_NUMBER_MARKUP:2
                                \with-color                       %%! STAGE_NUMBER_MARKUP:2
                                    #(x11-color 'DarkCyan)        %%! STAGE_NUMBER_MARKUP:2
                                    [1]                           %%! STAGE_NUMBER_MARKUP:2
                            }                                     %%! STAGE_NUMBER_MARKUP:2
                        %%% ^ \markup {                        %%! EXPLICIT_METRONOME_MARK:4
                        %%%     \fontsize                      %%! EXPLICIT_METRONOME_MARK:4
                        %%%         #-6                        %%! EXPLICIT_METRONOME_MARK:4
                        %%%         \general-align             %%! EXPLICIT_METRONOME_MARK:4
                        %%%             #Y                     %%! EXPLICIT_METRONOME_MARK:4
                        %%%             #DOWN                  %%! EXPLICIT_METRONOME_MARK:4
                        %%%             \note-by-number        %%! EXPLICIT_METRONOME_MARK:4
                        %%%                 #2                 %%! EXPLICIT_METRONOME_MARK:4
                        %%%                 #0                 %%! EXPLICIT_METRONOME_MARK:4
                        %%%                 #1                 %%! EXPLICIT_METRONOME_MARK:4
                        %%%     \upright                       %%! EXPLICIT_METRONOME_MARK:4
                        %%%         {                          %%! EXPLICIT_METRONOME_MARK:4
                        %%%             =                      %%! EXPLICIT_METRONOME_MARK:4
                        %%%             90                     %%! EXPLICIT_METRONOME_MARK:4
                        %%%         }                          %%! EXPLICIT_METRONOME_MARK:4
                        %%%     }                              %%! EXPLICIT_METRONOME_MARK:4
            <BLANKLINE>
                        %%% GlobalSkips [measure 2] %%%
                        \time 3/8
                        s1 * 3/8
                        ^ \markup {           %%! CLOCK_TIME_MARKUP:1
                            \fontsize         %%! CLOCK_TIME_MARKUP:1
                                #-2           %%! CLOCK_TIME_MARKUP:1
                                0'01''        %%! CLOCK_TIME_MARKUP:1
                            }                 %%! CLOCK_TIME_MARKUP:1
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 4/8
                        s1 * 1/2
                        ^ \markup {
                            \column
                                {
                                    \line                                          %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                        {                                          %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                            \with-color                            %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                                #(x11-color 'blue)                 %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                                {                                  %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                                    \fontsize                      %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                                        #-6                        %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                                        \general-align             %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                                            #Y                     %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                                            #DOWN                  %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                                            \note-by-number        %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                                                #2                 %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                                                #0                 %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                                                #1                 %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                                    \upright                       %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                                        {                          %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                                            =                      %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                                            72                     %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                                        }                          %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                                }                                  %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                        }                                          %%! EXPLICIT_METRONOME_MARK_WITH_COLOR:2
                                    \line                     %%! CLOCK_TIME_MARKUP:4
                                        {                     %%! CLOCK_TIME_MARKUP:4
                                            \fontsize         %%! CLOCK_TIME_MARKUP:4
                                                #-2           %%! CLOCK_TIME_MARKUP:4
                                                0'02''        %%! CLOCK_TIME_MARKUP:4
                                        }                     %%! CLOCK_TIME_MARKUP:4
                                }
                            }
                        - \markup {                               %%! STAGE_NUMBER_MARKUP:1
                            \fontsize                             %%! STAGE_NUMBER_MARKUP:1
                                #-3                               %%! STAGE_NUMBER_MARKUP:1
                                \with-color                       %%! STAGE_NUMBER_MARKUP:1
                                    #(x11-color 'DarkCyan)        %%! STAGE_NUMBER_MARKUP:1
                                    [2]                           %%! STAGE_NUMBER_MARKUP:1
                            }                                     %%! STAGE_NUMBER_MARKUP:1
                        %%% ^ \markup {                        %%! EXPLICIT_METRONOME_MARK:3
                        %%%     \fontsize                      %%! EXPLICIT_METRONOME_MARK:3
                        %%%         #-6                        %%! EXPLICIT_METRONOME_MARK:3
                        %%%         \general-align             %%! EXPLICIT_METRONOME_MARK:3
                        %%%             #Y                     %%! EXPLICIT_METRONOME_MARK:3
                        %%%             #DOWN                  %%! EXPLICIT_METRONOME_MARK:3
                        %%%             \note-by-number        %%! EXPLICIT_METRONOME_MARK:3
                        %%%                 #2                 %%! EXPLICIT_METRONOME_MARK:3
                        %%%                 #0                 %%! EXPLICIT_METRONOME_MARK:3
                        %%%                 #1                 %%! EXPLICIT_METRONOME_MARK:3
                        %%%     \upright                       %%! EXPLICIT_METRONOME_MARK:3
                        %%%         {                          %%! EXPLICIT_METRONOME_MARK:3
                        %%%             =                      %%! EXPLICIT_METRONOME_MARK:3
                        %%%             72                     %%! EXPLICIT_METRONOME_MARK:3
                        %%%         }                          %%! EXPLICIT_METRONOME_MARK:3
                        %%%     }                              %%! EXPLICIT_METRONOME_MARK:3
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 3/8
                        s1 * 3/8
                        ^ \markup {           %%! CLOCK_TIME_MARKUP:1
                            \fontsize         %%! CLOCK_TIME_MARKUP:1
                                #-2           %%! CLOCK_TIME_MARKUP:1
                                0'04''        %%! CLOCK_TIME_MARKUP:1
                            }                 %%! CLOCK_TIME_MARKUP:1
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
                                e'8
                                [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e'8
            <BLANKLINE>
                                f'8
                                ]
                            }
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 2] %%%
                                e'8
                                [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e'8
                                ]
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
