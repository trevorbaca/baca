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

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score"
            <<
                \context GlobalContext = "GlobalContext"
                <<
                    \context GlobalSkips = "GlobalSkips"
                    {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                    %@% \once \override TextSpanner.bound-details.left.text =                        %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@% \markup {                                                                    %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%     \fontsize                                                                %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%         #-6                                                                  %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%         \general-align                                                       %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%             #Y                                                               %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%             #DOWN                                                            %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%             \note-by-number                                                  %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%                 #2                                                           %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%                 #0                                                           %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%                 #1.5                                                         %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%     \upright                                                                 %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%         {                                                                    %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%             =                                                                %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%             90                                                               %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%         }                                                                    %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%     \hspace                                                                  %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%         #1                                                                   %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%     }                                                                        %! SM27:EXPLICIT_METRONOME_MARK:SM30 %! SM29:METRONOME_MARK_SPANNER
                        \once \override TextSpanner.Y-extent = ##f                                   %! SM29:METRONOME_MARK_SPANNER
                        \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29:METRONOME_MARK_SPANNER
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                        \once \override TextSpanner.bound-details.left.text =                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                        \markup {                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                            \with-color                                                              %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                #(x11-color 'blue)                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                {                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                    \fontsize                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                        #-6                                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                        \general-align                                               %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                            #Y                                                       %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                            #DOWN                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                            \note-by-number                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                                #2                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                                #0                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                                #1.5                                                 %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                    \upright                                                         %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                        {                                                            %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                            =                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                            90                                                       %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                        }                                                            %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                    \hspace                                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                        #1                                                           %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                }                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                            }                                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30 %! SM29:METRONOME_MARK_SPANNER
                        \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29:METRONOME_MARK_SPANNER
                        \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29:METRONOME_MARK_SPANNER
                        \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29:METRONOME_MARK_SPANNER
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                        \once \override TextSpanner.dash-period = 0                                  %! SM29:METRONOME_MARK_SPANNER
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
                        \startTextSpan                                                               %! SM29:METRONOME_MARK_SPANNER
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                    %@% \once \override TextSpanner.bound-details.left.text =                        %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@% \markup {                                                                    %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%     \fontsize                                                                %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%         #-6                                                                  %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%         \general-align                                                       %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%             #Y                                                               %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%             #DOWN                                                            %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%             \note-by-number                                                  %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%                 #2                                                           %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%                 #0                                                           %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%                 #1.5                                                         %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%     \upright                                                                 %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%         {                                                                    %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%             =                                                                %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%             72                                                               %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%         }                                                                    %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%     \hspace                                                                  %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%         #1                                                                   %! SM27:EXPLICIT_METRONOME_MARK:SM30
                    %@%     }                                                                        %! SM27:EXPLICIT_METRONOME_MARK:SM30 %! SM29:METRONOME_MARK_SPANNER
                        \once \override TextSpanner.Y-extent = ##f                                   %! SM29:METRONOME_MARK_SPANNER
                        \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29:METRONOME_MARK_SPANNER
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                        \once \override TextSpanner.bound-details.left.text =                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                        \markup {                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                            \with-color                                                              %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                #(x11-color 'blue)                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                {                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                    \fontsize                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                        #-6                                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                        \general-align                                               %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                            #Y                                                       %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                            #DOWN                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                            \note-by-number                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                                #2                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                                #0                                                   %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                                #1.5                                                 %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                    \upright                                                         %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                        {                                                            %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                            =                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                            72                                                       %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                        }                                                            %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                    \hspace                                                          %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                        #1                                                           %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                                }                                                                    %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30
                            }                                                                        %! SM15:EXPLICIT_METRONOME_MARK_WITH_COLOR:SM30 %! SM29:METRONOME_MARK_SPANNER
                        \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29:METRONOME_MARK_SPANNER
                        \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29:METRONOME_MARK_SPANNER
                        \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29:METRONOME_MARK_SPANNER
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29:METRONOME_MARK_SPANNER
                        \once \override TextSpanner.dash-period = 0                                  %! SM29:METRONOME_MARK_SPANNER
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
                        \stopTextSpan                                                                %! SM29:METRONOME_MARK_SPANNER
                        \startTextSpan                                                               %! SM29:METRONOME_MARK_SPANNER
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \stopTextSpan                                                                %! SM29:METRONOME_MARK_SPANNER
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext"
                <<
                    \context Staff = "MusicStaff"
                    {
                        \context Voice = "MusicVoice"
                        {
                            {
            <BLANKLINE>
                                % [MusicVoice measure 1]                                             %! SM4
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
                                % [MusicVoice measure 2]                                             %! SM4
                                e'8
                                [
            <BLANKLINE>
                                f'8
            <BLANKLINE>
                                e'8
                                ]
                            }
            <BLANKLINE>
                            % [MusicVoice measure 3]                                                 %! SM4
                            R1 * 1/2
            <BLANKLINE>
                            % [MusicVoice measure 4]                                                 %! SM4
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
