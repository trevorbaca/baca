import abjad
import baca
import collections
import numbers
from .Command import Command


class MicrotoneDeviationCommand(Command):
    r'''Microtone deviation command.

    ..  container:: example

        With alternating up- and down-quatertones:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.pitches('E4'),
        ...     baca.make_even_runs(),
        ...     baca.deviation([0, 0.5, 0, -0.5]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=89)
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        % GlobalSkips [measure 1]                                                    %! SM4
                        \once \override TextSpanner.Y-extent = ##f                                   %! SM29
                        \once \override TextSpanner.bound-details.left-broken.text = ##f             %! SM29
                        \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29
                        \once \override TextSpanner.bound-details.right-broken.padding = 0           %! SM29
                        \once \override TextSpanner.bound-details.right-broken.text = ##f            %! SM29
                        \once \override TextSpanner.bound-details.right.padding = 0                  %! SM29
                        \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29
                        \once \override TextSpanner.dash-period = 0                                  %! SM29
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                        \startTextSpan                                                               %! SM29
                        ^ \markup {
                            \column
                                {
                                %F% \line                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %F%     {                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %F%         \fontsize                                                %! MEASURE_INDEX_MARKUP:SM31
                                %F%             #3                                                   %! MEASURE_INDEX_MARKUP:SM31
                                %F%             \with-color                                          %! MEASURE_INDEX_MARKUP:SM31
                                %F%                 #(x11-color 'DarkCyan)                           %! MEASURE_INDEX_MARKUP:SM31
                                %F%                 m0                                               %! MEASURE_INDEX_MARKUP:SM31
                                %F%     }                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %F% \line                                                            %! STAGE_NUMBER_MARKUP:SM3
                                %F%     {                                                            %! STAGE_NUMBER_MARKUP:SM3
                                %F%         \fontsize                                                %! STAGE_NUMBER_MARKUP:SM3
                                %F%             #3                                                   %! STAGE_NUMBER_MARKUP:SM3
                                %F%             \with-color                                          %! STAGE_NUMBER_MARKUP:SM3
                                %F%                 #(x11-color 'DarkCyan)                           %! STAGE_NUMBER_MARKUP:SM3
                                %F%                 [1]                                              %! STAGE_NUMBER_MARKUP:SM3
                                %F%     }                                                            %! STAGE_NUMBER_MARKUP:SM3
                                }
                            }
            <BLANKLINE>
                        % GlobalSkips [measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                    %F% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %F%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %F%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %F%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %F%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %F%             m1                                                               %! MEASURE_INDEX_MARKUP:SM31
                    %F%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                    %F% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %F%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %F%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %F%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %F%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %F%             m2                                                               %! MEASURE_INDEX_MARKUP:SM31
                    %F%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                        \stopTextSpan                                                                %! SM29
                    %F% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %F%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %F%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %F%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %F%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %F%             m3                                                               %! MEASURE_INDEX_MARKUP:SM31
                    %F%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
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
                                % MusicVoice [measure 1]                                             %! SM4
                                e'8
                                [
            <BLANKLINE>
                                eqs'8
            <BLANKLINE>
                                e'8
            <BLANKLINE>
                                eqf'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 2]                                             %! SM4
                                e'8
                                [
            <BLANKLINE>
                                eqs'8
            <BLANKLINE>
                                e'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 3]                                             %! SM4
                                eqf'8
                                [
            <BLANKLINE>
                                e'8
            <BLANKLINE>
                                eqs'8
            <BLANKLINE>
                                e'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 4]                                             %! SM4
                                eqf'8
                                [
            <BLANKLINE>
                                e'8
            <BLANKLINE>
                                eqs'8
                                ]
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_deviations',
        )

    ### INITIALIZER ###

    def __init__(self, deviations=None, selector='baca.plts()'):
        Command.__init__(self)
        if deviations is not None:
            assert isinstance(deviations, collections.Iterable)
            assert all(isinstance(_, numbers.Number) for _ in deviations)
        self._deviations = abjad.CyclicTuple(deviations)

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Cyclically applies deviations to plts in `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if not self.deviations:
            return
        if self.selector:
            argument = self.selector(argument)
        for i, plt in enumerate(baca.select(argument).plts()):
            deviation = self.deviations[i]
            self._adjust_pitch(plt, deviation)
            
    ### PRIVATE METHODS ###

    def _adjust_pitch(self, plt, deviation):
        assert deviation in (0.5, 0, -0.5)
        if deviation == 0:
            return
        for pleaf in plt:
            pitch = pleaf.written_pitch
            pitch = pitch.transpose_staff_position(0, deviation)
            pleaf.written_pitch = pitch
            annotation = {'color microtone': True}
            abjad.attach(annotation, pleaf)

    ### PUBLIC PROPERTIES ###

    @property
    def deviations(self):
        r'''Gets deviations.

        ..  container:: example

            >>> command = baca.deviation([0, -0.5, 0, 0.5])
            >>> command.deviations
            CyclicTuple([0, -0.5, 0, 0.5])

        Set to iterable of items (each -0.5, 0 or 0.5).

        Returns cyclic tuple or none.
        '''
        return self._deviations
