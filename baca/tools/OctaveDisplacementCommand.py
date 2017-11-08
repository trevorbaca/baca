import abjad
import baca
from .Command import Command


class OctaveDisplacementCommand(Command):
    r"""Octave displacement command.

    ..  container:: example

        Displaces octaves:

        >>> segment_maker = baca.SegmentMaker(
        ...     score_template=baca.ViolinSoloScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> segment_maker(
        ...     baca.scope('Violin Music Voice', 1),
        ...     baca.even_runs(),
        ...     baca.suite([
        ...         baca.pitches('G4', repeats=True),
        ...         baca.displacement([0, 0, 1, 1, 0, 0, -1, -1, 2, 2]),
        ...         ]),
        ...     )

        >>> result = segment_maker.run(is_doc_example=True)
        >>> lilypond_file, metadata = result
        >>> abjad.show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(lilypond_file[abjad.Score])
            \context Score = "Score" <<
                \tag violin
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
                    \tag violin
                    \context ViolinMusicStaff = "Violin Music Staff" {
                        \context ViolinMusicVoice = "Violin Music Voice" {
                            {
                                \set ViolinMusicStaff.instrumentName = \markup { Violin }
                                \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                                \clef "treble"
                                g'8 [
                                g'8
                                g''8
                                g''8 ]
                            }
                            {
                                g'8 [
                                g'8
                                g8 ]
                            }
                            {
                                g8 [
                                g'''8
                                g'''8
                                g'8 ]
                            }
                            {
                                g'8 [
                                g''8
                                g''8 ]
                                \bar "|"
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
