import abjad
import baca
from .Command import Command


class OctaveDisplacementCommand(Command):
    r"""Octave displacement command.

    ..  container:: example

        Displaces octaves:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     baca.scope('MusicVoice', 1),
        ...     baca.make_even_runs(),
        ...     baca.suite([
        ...         baca.pitches('G4', repeats=True),
        ...         baca.displacement([0, 0, 1, 1, 0, 0, -1, -1, 2, 2]),
        ...         ]),
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
                                %@% \line                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %@%     {                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %@%         \fontsize                                                %! MEASURE_INDEX_MARKUP:SM31
                                %@%             #3                                                   %! MEASURE_INDEX_MARKUP:SM31
                                %@%             \with-color                                          %! MEASURE_INDEX_MARKUP:SM31
                                %@%                 #(x11-color 'DarkCyan)                           %! MEASURE_INDEX_MARKUP:SM31
                                %@%                 m0                                               %! MEASURE_INDEX_MARKUP:SM31
                                %@%     }                                                            %! MEASURE_INDEX_MARKUP:SM31
                                %@% \line                                                            %! STAGE_NUMBER_MARKUP:SM3
                                %@%     {                                                            %! STAGE_NUMBER_MARKUP:SM3
                                %@%         \fontsize                                                %! STAGE_NUMBER_MARKUP:SM3
                                %@%             #3                                                   %! STAGE_NUMBER_MARKUP:SM3
                                %@%             \with-color                                          %! STAGE_NUMBER_MARKUP:SM3
                                %@%                 #(x11-color 'DarkCyan)                           %! STAGE_NUMBER_MARKUP:SM3
                                %@%                 [1]                                              %! STAGE_NUMBER_MARKUP:SM3
                                %@%     }                                                            %! STAGE_NUMBER_MARKUP:SM3
                                }
                            }
            <BLANKLINE>
                        % GlobalSkips [measure 2]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             m1                                                               %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 3]                                                    %! SM4
                        \time 4/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 1/2
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             m2                                                               %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
            <BLANKLINE>
                        % GlobalSkips [measure 4]                                                    %! SM4
                        \time 3/8                                                                    %! EXPLICIT_TIME_SIGNATURE:SM8
                        \once \override Score.TimeSignature.color = #(x11-color 'blue)               %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                        s1 * 3/8
                        \stopTextSpan                                                                %! SM29
                    %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM31
                    %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM31
                    %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM31
                    %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM31
                    %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM31
                    %@%             m3                                                               %! MEASURE_INDEX_MARKUP:SM31
                    %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM31
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
                                g'8
                                [
            <BLANKLINE>
                                g'8
            <BLANKLINE>
                                g''8
            <BLANKLINE>
                                g''8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 2]                                             %! SM4
                                g'8
                                [
            <BLANKLINE>
                                g'8
            <BLANKLINE>
                                g8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 3]                                             %! SM4
                                g8
                                [
            <BLANKLINE>
                                g'''8
            <BLANKLINE>
                                g'''8
            <BLANKLINE>
                                g'8
                                ]
                            }
                            {
            <BLANKLINE>
                                % MusicVoice [measure 4]                                             %! SM4
                                g'8
                                [
            <BLANKLINE>
                                g''8
            <BLANKLINE>
                                g''8
                                ]
            <BLANKLINE>
                            }
                        }
                    }
                >>
            >>

    """

    ### CLASS VARIABLES ##

    __slots__ = (
        '_displacements',
        )

    ### INITIALIZER ###

    def __init__(self, displacements=None, selector='baca.plts()'):
        Command.__init__(self, selector=selector)
        if displacements is not None:
            displacements = tuple(displacements)
            assert self._is_octave_displacement_vector(displacements)
            displacements = abjad.CyclicTuple(displacements)
        self._displacements = displacements

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.displacements is None:
            return
        if self.selector:
            argument = self.selector(argument)
        for i, plt in enumerate(baca.select(argument).plts()):
            displacement = self.displacements[i]
            interval = abjad.NumberedInterval(12 * displacement)
            for pleaf in plt:
                if isinstance(pleaf, abjad.Note):
                    pitch = pleaf.written_pitch
                    pitch += interval
                    pleaf.written_pitch = pitch
                elif isinstance(pleaf, abjad.Chord):
                    pitches = [_ + interval for _ in pleaf.written_pitches]
                    pleaf.written_pitches = pitches
                else:
                    raise TypeError(pleaf)

    ### PRIVATE METHODS ###

    def _is_octave_displacement_vector(self, argument):
        if isinstance(argument, (tuple, list)):
            if all(isinstance(_, int) for _ in argument):
                return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def displacements(self):
        r'''Gets displacements.

        ..  container:: example

            >>> command = baca.displacement(
            ...     [0, 0, 0, 1, 1, 0, 0, 0, -1, 1, 1, 2, 2],
            ...     )
            >>> command.displacements
            CyclicTuple([0, 0, 0, 1, 1, 0, 0, 0, -1, 1, 1, 2, 2])

        Defaults to none.

        Set to integers or none.

        Returns cyclic tuple of integers, or none.
        '''
        return self._displacements
