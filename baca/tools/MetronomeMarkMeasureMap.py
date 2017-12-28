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

            >>> abjad.f(lilypond_file[abjad.Score], strict=79)
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        % GlobalSkips [measure 1]                                          %! SM4
                        \time 4/8                                                          %! SM1
                        \bar ""                                                            %! EMPTY_START_BAR:SM2
                        s1 * 1/2
                        ^ \markup {
                            \column
                                {
                                    \line                                                  %! STAGE_NUMBER_MARKUP:SM3
                                        {                                                  %! STAGE_NUMBER_MARKUP:SM3
                                            \fontsize                                      %! STAGE_NUMBER_MARKUP:SM3
                                                #-3                                        %! STAGE_NUMBER_MARKUP:SM3
                                                \with-color                                %! STAGE_NUMBER_MARKUP:SM3
                                                    #(x11-color 'DarkCyan)                 %! STAGE_NUMBER_MARKUP:SM3
                                                    [1]                                    %! STAGE_NUMBER_MARKUP:SM3
                                        }                                                  %! STAGE_NUMBER_MARKUP:SM3
                                    \line                                                  %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                        {                                                  %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                            \with-color                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                #(x11-color 'blue)                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                {                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                    \fontsize                              %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                        #-6                                %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                        \general-align                     %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                            #Y                             %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                            #DOWN                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                            \note-by-number                %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                                #2                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                                #0                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                                #1                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                    \upright                               %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                        {                                  %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                            =                              %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                            90                             %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                        }                                  %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                }                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                        }                                                  %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                    \line                                                  %! CLOCK_TIME_MARKUP
                                        {                                                  %! CLOCK_TIME_MARKUP
                                            \fontsize                                      %! CLOCK_TIME_MARKUP
                                                #-2                                        %! CLOCK_TIME_MARKUP
                                                0'00''                                     %! CLOCK_TIME_MARKUP
                                        }                                                  %! CLOCK_TIME_MARKUP
                                }
                            }
                        %%% ^ \markup {                                                    %! EXPLICIT_METRONOME_MARK
                        %%%     \fontsize                                                  %! EXPLICIT_METRONOME_MARK
                        %%%         #-6                                                    %! EXPLICIT_METRONOME_MARK
                        %%%         \general-align                                         %! EXPLICIT_METRONOME_MARK
                        %%%             #Y                                                 %! EXPLICIT_METRONOME_MARK
                        %%%             #DOWN                                              %! EXPLICIT_METRONOME_MARK
                        %%%             \note-by-number                                    %! EXPLICIT_METRONOME_MARK
                        %%%                 #2                                             %! EXPLICIT_METRONOME_MARK
                        %%%                 #0                                             %! EXPLICIT_METRONOME_MARK
                        %%%                 #1                                             %! EXPLICIT_METRONOME_MARK
                        %%%     \upright                                                   %! EXPLICIT_METRONOME_MARK
                        %%%         {                                                      %! EXPLICIT_METRONOME_MARK
                        %%%             =                                                  %! EXPLICIT_METRONOME_MARK
                        %%%             90                                                 %! EXPLICIT_METRONOME_MARK
                        %%%         }                                                      %! EXPLICIT_METRONOME_MARK
                        %%%     }                                                          %! EXPLICIT_METRONOME_MARK
            <BLANKLINE>
                        % GlobalSkips [measure 2]                                          %! SM4
                        \time 3/8                                                          %! SM1
                        s1 * 3/8
                        ^ \markup {                                                        %! CLOCK_TIME_MARKUP
                            \fontsize                                                      %! CLOCK_TIME_MARKUP
                                #-2                                                        %! CLOCK_TIME_MARKUP
                                0'01''                                                     %! CLOCK_TIME_MARKUP
                            }                                                              %! CLOCK_TIME_MARKUP
            <BLANKLINE>
                        % GlobalSkips [measure 3]                                          %! SM4
                        \time 4/8                                                          %! SM1
                        s1 * 1/2
                        ^ \markup {
                            \column
                                {
                                    \line                                                  %! STAGE_NUMBER_MARKUP:SM3
                                        {                                                  %! STAGE_NUMBER_MARKUP:SM3
                                            \fontsize                                      %! STAGE_NUMBER_MARKUP:SM3
                                                #-3                                        %! STAGE_NUMBER_MARKUP:SM3
                                                \with-color                                %! STAGE_NUMBER_MARKUP:SM3
                                                    #(x11-color 'DarkCyan)                 %! STAGE_NUMBER_MARKUP:SM3
                                                    [2]                                    %! STAGE_NUMBER_MARKUP:SM3
                                        }                                                  %! STAGE_NUMBER_MARKUP:SM3
                                    \line                                                  %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                        {                                                  %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                            \with-color                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                #(x11-color 'blue)                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                {                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                    \fontsize                              %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                        #-6                                %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                        \general-align                     %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                            #Y                             %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                            #DOWN                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                            \note-by-number                %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                                #2                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                                #0                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                                #1                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                    \upright                               %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                        {                                  %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                            =                              %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                            72                             %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                        }                                  %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                                }                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                        }                                                  %! EXPLICIT_METRONOME_MARK_WITH_COLOR
                                    \line                                                  %! CLOCK_TIME_MARKUP
                                        {                                                  %! CLOCK_TIME_MARKUP
                                            \fontsize                                      %! CLOCK_TIME_MARKUP
                                                #-2                                        %! CLOCK_TIME_MARKUP
                                                0'02''                                     %! CLOCK_TIME_MARKUP
                                        }                                                  %! CLOCK_TIME_MARKUP
                                }
                            }
                        %%% ^ \markup {                                                    %! EXPLICIT_METRONOME_MARK
                        %%%     \fontsize                                                  %! EXPLICIT_METRONOME_MARK
                        %%%         #-6                                                    %! EXPLICIT_METRONOME_MARK
                        %%%         \general-align                                         %! EXPLICIT_METRONOME_MARK
                        %%%             #Y                                                 %! EXPLICIT_METRONOME_MARK
                        %%%             #DOWN                                              %! EXPLICIT_METRONOME_MARK
                        %%%             \note-by-number                                    %! EXPLICIT_METRONOME_MARK
                        %%%                 #2                                             %! EXPLICIT_METRONOME_MARK
                        %%%                 #0                                             %! EXPLICIT_METRONOME_MARK
                        %%%                 #1                                             %! EXPLICIT_METRONOME_MARK
                        %%%     \upright                                                   %! EXPLICIT_METRONOME_MARK
                        %%%         {                                                      %! EXPLICIT_METRONOME_MARK
                        %%%             =                                                  %! EXPLICIT_METRONOME_MARK
                        %%%             72                                                 %! EXPLICIT_METRONOME_MARK
                        %%%         }                                                      %! EXPLICIT_METRONOME_MARK
                        %%%     }                                                          %! EXPLICIT_METRONOME_MARK
            <BLANKLINE>
                        % GlobalSkips [measure 4]                                          %! SM4
                        \time 3/8                                                          %! SM1
                        s1 * 3/8
                        ^ \markup {                                                        %! CLOCK_TIME_MARKUP
                            \fontsize                                                      %! CLOCK_TIME_MARKUP
                                #-2                                                        %! CLOCK_TIME_MARKUP
                                0'04''                                                     %! CLOCK_TIME_MARKUP
                            }                                                              %! CLOCK_TIME_MARKUP
                        \override Score.BarLine.transparent = ##f                          %! SM5
                        \bar "|"                                                           %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                % MusicVoice [measure 1]                                   %! SM4
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
                                % MusicVoice [measure 2]                                   %! SM4
                                e'8
                                [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e'8
                                ]
                            }
            <BLANKLINE>
                            % MusicVoice [measure 3]                                       %! SM4
                            R1 * 1/2
            <BLANKLINE>
                            % MusicVoice [measure 4]                                       %! SM4
                            R1 * 3/8
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
