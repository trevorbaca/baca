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
        >>> abjad.show(lilypond_file, strict=79) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score], strict=79)
            \context Score = "Score" <<
                \context GlobalContext = "GlobalContext" <<
                    \context GlobalSkips = "GlobalSkips" {
            <BLANKLINE>
                        %%% GlobalSkips [measure 1] %%%
                        \time 4/8
                        \bar ""                                                            %%! EMPTY_START_BAR
                        s1 * 1/2
                        - \markup {                                                        %%! STAGE_NUMBER_MARKUP
                            \fontsize                                                      %%! STAGE_NUMBER_MARKUP
                                #-3                                                        %%! STAGE_NUMBER_MARKUP
                                \with-color                                                %%! STAGE_NUMBER_MARKUP
                                    #(x11-color 'DarkCyan)                                 %%! STAGE_NUMBER_MARKUP
                                    [1]                                                    %%! STAGE_NUMBER_MARKUP
                            }                                                              %%! STAGE_NUMBER_MARKUP
            <BLANKLINE>
                        %%% GlobalSkips [measure 2] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                        %%% GlobalSkips [measure 3] %%%
                        \time 4/8
                        s1 * 1/2
            <BLANKLINE>
                        %%% GlobalSkips [measure 4] %%%
                        \time 3/8
                        s1 * 3/8
            <BLANKLINE>
                    }
                >>
                \context MusicContext = "MusicContext" <<
                    \context Staff = "MusicStaff" {
                        \context Voice = "MusicVoice" {
                            {
            <BLANKLINE>
                                %%% MusicVoice [measure 1] %%%
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
                                %%% MusicVoice [measure 2] %%%
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
                                %%% MusicVoice [measure 3] %%%
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
                                %%% MusicVoice [measure 4] %%%
                                g'8
                                [
            <BLANKLINE>
                                g''8
            <BLANKLINE>
                                g''8
                                ]
                                \bar "|"
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
