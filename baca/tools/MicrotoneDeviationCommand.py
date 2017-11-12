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
        ...     baca.scope('Music Voice', 1),
        ...     baca.pitches('E4'),
        ...     baca.make_even_runs(),
        ...     baca.deviation([0, 0.5, 0, -0.5]),
        ...     )

        >>> lilypond_file = maker.run(environment='docs')
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \context GlobalContext = "Global Context" <<
                    \context GlobalRests = "Global Rests" {
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
                    \context GlobalSkips = "Global Skips" {
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                        {
                            \time 4/8
                            s1 * 1/2
                        }
                        {
                            \time 3/8
                            s1 * 3/8
                        }
                    }
                >>
                \context MusicContext = "Music Context" <<
                    \context Staff = "Music Staff" {
                        \context Voice = "Music Voice" {
                            {
                                \clef "treble"
                                e'8 [
                                eqs'8
                                e'8
                                eqf'8 ]
                            }
                            {
                                e'8 [
                                eqs'8
                                e'8 ]
                            }
                            {
                                eqf'8 [
                                e'8
                                eqs'8
                                e'8 ]
                            }
                            {
                                eqf'8 [
                                e'8
                                eqs'8 ]
                                \bar "|"
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
