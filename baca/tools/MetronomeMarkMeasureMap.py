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
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        % [GlobalSkips measure 1]                                                    %! SM4
                    %@% \once \override TextSpanner.bound-details.left.text =                        %! EXPLICIT_METRONOME_MARK:SM27
                    %@% \markup {                                                                    %! EXPLICIT_METRONOME_MARK:SM27
                    %@%     \fontsize                                                                %! EXPLICIT_METRONOME_MARK:SM27
                    %@%         #-6                                                                  %! EXPLICIT_METRONOME_MARK:SM27
                    %@%         \general-align                                                       %! EXPLICIT_METRONOME_MARK:SM27
                    %@%             #Y                                                               %! EXPLICIT_METRONOME_MARK:SM27
                    %@%             #DOWN                                                            %! EXPLICIT_METRONOME_MARK:SM27
                    %@%             \note-by-number                                                  %! EXPLICIT_METRONOME_MARK:SM27
                    %@%                 #2                                                           %! EXPLICIT_METRONOME_MARK:SM27
                    %@%                 #0                                                           %! EXPLICIT_METRONOME_MARK:SM27
                    %@%                 #1.5                                                         %! EXPLICIT_METRONOME_MARK:SM27
                    %@%     \upright                                                                 %! EXPLICIT_METRONOME_MARK:SM27
                    %@%         {                                                                    %! EXPLICIT_METRONOME_MARK:SM27
                    %@%             =                                                                %! EXPLICIT_METRONOME_MARK:SM27
                    %@%             90                                                               %! EXPLICIT_METRONOME_MARK:SM27
                    %@%         }                                                                    %! EXPLICIT_METRONOME_MARK:SM27
                    %@%     \hspace                                                                  %! EXPLICIT_METRONOME_MARK:SM27
                    %@%         #1                                                                   %! EXPLICIT_METRONOME_MARK:SM27
                    %@%     }                                                                        %! EXPLICIT_METRONOME_MARK:SM27 %! SM29
                        \once \override TextSpanner.Y-extent = ##f                                   %! SM29
                        \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29
                        \once \override TextSpanner.bound-details.left-broken.text = \markup {
                            \null
                            }                                                                        %! SM29
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29
                        \once \override TextSpanner.bound-details.left.text =                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                        \markup {                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                            \with-color                                                              %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                #(x11-color 'blue)                                                   %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                {                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    \fontsize                                                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        #-6                                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        \general-align                                               %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            #Y                                                       %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            #DOWN                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            \note-by-number                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                #2                                                   %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                #0                                                   %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                #1.5                                                 %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    \upright                                                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        {                                                            %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            =                                                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            90                                                       %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        }                                                            %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    \hspace                                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        #1                                                           %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                }                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                            }                                                                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15 %! SM29
                        \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29
                        \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29
                        \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29
                        \once \override TextSpanner.dash-period = 0                                  %! SM29
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                        \startTextSpan                                                               %! SM29
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                    %@% \once \override TextSpanner.bound-details.left.text =                        %! EXPLICIT_METRONOME_MARK:SM27
                    %@% \markup {                                                                    %! EXPLICIT_METRONOME_MARK:SM27
                    %@%     \fontsize                                                                %! EXPLICIT_METRONOME_MARK:SM27
                    %@%         #-6                                                                  %! EXPLICIT_METRONOME_MARK:SM27
                    %@%         \general-align                                                       %! EXPLICIT_METRONOME_MARK:SM27
                    %@%             #Y                                                               %! EXPLICIT_METRONOME_MARK:SM27
                    %@%             #DOWN                                                            %! EXPLICIT_METRONOME_MARK:SM27
                    %@%             \note-by-number                                                  %! EXPLICIT_METRONOME_MARK:SM27
                    %@%                 #2                                                           %! EXPLICIT_METRONOME_MARK:SM27
                    %@%                 #0                                                           %! EXPLICIT_METRONOME_MARK:SM27
                    %@%                 #1.5                                                         %! EXPLICIT_METRONOME_MARK:SM27
                    %@%     \upright                                                                 %! EXPLICIT_METRONOME_MARK:SM27
                    %@%         {                                                                    %! EXPLICIT_METRONOME_MARK:SM27
                    %@%             =                                                                %! EXPLICIT_METRONOME_MARK:SM27
                    %@%             72                                                               %! EXPLICIT_METRONOME_MARK:SM27
                    %@%         }                                                                    %! EXPLICIT_METRONOME_MARK:SM27
                    %@%     \hspace                                                                  %! EXPLICIT_METRONOME_MARK:SM27
                    %@%         #1                                                                   %! EXPLICIT_METRONOME_MARK:SM27
                    %@%     }                                                                        %! EXPLICIT_METRONOME_MARK:SM27 %! SM29
                        \once \override TextSpanner.Y-extent = ##f                                   %! SM29
                        \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29
                        \once \override TextSpanner.bound-details.left-broken.text = \markup {
                            \null
                            }                                                                        %! SM29
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29
                        \once \override TextSpanner.bound-details.left.text =                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                        \markup {                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                            \with-color                                                              %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                #(x11-color 'blue)                                                   %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                {                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    \fontsize                                                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        #-6                                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        \general-align                                               %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            #Y                                                       %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            #DOWN                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            \note-by-number                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                #2                                                   %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                #0                                                   %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                                #1.5                                                 %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    \upright                                                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        {                                                            %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            =                                                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            72                                                       %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        }                                                            %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    \hspace                                                          %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        #1                                                           %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                }                                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                            }                                                                        %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15 %! SM29
                        \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29
                        \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29
                        \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29
                        \once \override TextSpanner.dash-period = 0                                  %! SM29
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                        \stopTextSpan                                                                %! SM29
                        \startTextSpan                                                               %! SM29
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                        \stopTextSpan                                                                %! SM29
                        \override Score.BarLine.transparent = ##f                                    %! SM5
                        \bar "|"                                                                     %! SM5
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
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
