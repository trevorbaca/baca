import abjad


class MetronomeMarkMeasureMap(abjad.AbjadObject):
    r"""
    Metronome mark measure map.

    ..  container:: example

        >>> metronome_marks = abjad.OrderedDict()
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
        ...     ('MusicVoice', 1),
        ...     baca.pitches('E4 F4'),
        ...     baca.make_even_divisions(),
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
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
                        \stopTextSpan                                                                %! MMI1
                    %@% - \abjad_invisible_line                                                      %! MMI2
                    %@% - \tweak bound-details.left.text \markup {                                   %! MMI2
                    %@%     \concat                                                                  %! MMI2
                    %@%         {                                                                    %! MMI2
                    %@%             \abjad-metronome-mark-markup #2 #0 #1 #"90"                      %! MMI2
                    %@%             \hspace                                                          %! MMI2
                    %@%                 #0.5                                                         %! MMI2
                    %@%         }                                                                    %! MMI2
                    %@%     }                                                                        %! MMI2
                    %@% - \tweak bound-details.left-broken.text ##f                                  %! MMI2
                    %@% \startTextSpan                                                               %! MMI2
                        - \abjad_invisible_line                                                      %! MMI3
                        - \tweak bound-details.left.text \markup {                                   %! MMI3
                            \concat                                                                  %! MMI3
                                {                                                                    %! MMI3
                                    \with-color                                                      %! MMI3
                                        #(x11-color 'blue)                                           %! MMI3
                                        \abjad-metronome-mark-markup #2 #0 #1 #"90"                  %! MMI3
                                    \hspace                                                          %! MMI3
                                        #0.5                                                         %! MMI3
                                }                                                                    %! MMI3
                            }                                                                        %! MMI3
                        - \tweak bound-details.left-broken.text ##f                                  %! MMI3
                        \startTextSpan                                                               %! MMI3
            <BLANKLINE>
                        % [GlobalSkips measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
            <BLANKLINE>
                        % [GlobalSkips measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 1/2
                        \stopTextSpan                                                                %! MMI1
                    %@% - \abjad_invisible_line                                                      %! MMI2
                    %@% - \tweak bound-details.left.text \markup {                                   %! MMI2
                    %@%     \concat                                                                  %! MMI2
                    %@%         {                                                                    %! MMI2
                    %@%             \abjad-metronome-mark-markup #2 #0 #1 #"72"                      %! MMI2
                    %@%             \hspace                                                          %! MMI2
                    %@%                 #0.5                                                         %! MMI2
                    %@%         }                                                                    %! MMI2
                    %@%     }                                                                        %! MMI2
                    %@% - \tweak bound-details.left-broken.text ##f                                  %! MMI2
                    %@% \startTextSpan                                                               %! MMI2
                        - \abjad_invisible_line                                                      %! MMI3
                        - \tweak bound-details.left.text \markup {                                   %! MMI3
                            \concat                                                                  %! MMI3
                                {                                                                    %! MMI3
                                    \with-color                                                      %! MMI3
                                        #(x11-color 'blue)                                           %! MMI3
                                        \abjad-metronome-mark-markup #2 #0 #1 #"72"                  %! MMI3
                                    \hspace                                                          %! MMI3
                                        #0.5                                                         %! MMI3
                                }                                                                    %! MMI3
                            }                                                                        %! MMI3
                        - \tweak bound-details.left-broken.text ##f                                  %! MMI3
                        \startTextSpan                                                               %! MMI3
            <BLANKLINE>
                        % [GlobalSkips measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! SM8:EXPLICIT_TIME_SIGNATURE:SM1
                        \baca_time_signature_color #'blue                                            %! SM6:EXPLICIT_TIME_SIGNATURE_COLOR:SM1
                        s1 * 3/8
                        \stopTextSpan                                                                %! MMI4
                        \baca_bar_line_visible                                                       %! SM5
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
            <BLANKLINE>
                            % [MusicVoice measure 1]                                                 %! SM4
                            e'8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e'8
            <BLANKLINE>
                            f'8
                            ]
            <BLANKLINE>
                            % [MusicVoice measure 2]                                                 %! SM4
                            e'8
                            [
            <BLANKLINE>
                            f'8
            <BLANKLINE>
                            e'8
                            ]
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

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_items',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        items=None,
        ):
        if items is not None:
            items = tuple(items)
        self._items = items

    ### SPECIAL METHODS ###

    def __getitem__(self, argument):
        """
        Gets ``argument``.

        ..  container:: example

            >>> marks = baca.MetronomeMarkMeasureMap([
            ...     (1, abjad.MetronomeMark((1, 4), 90)),
            ...     (1, baca.Accelerando()),
            ...     (4, abjad.MetronomeMark((1, 4), 120)),
            ...     ])

            >>> marks[1]
            (1, Accelerando())

        Returns item.
        """
        return self.items.__getitem__(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        """
        Gets items.

        ..  container:: example

            >>> marks = baca.MetronomeMarkMeasureMap([
            ...     (1, abjad.MetronomeMark((1, 4), 90)),
            ...     (1, baca.Accelerando()),
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
        """
        return self._items
