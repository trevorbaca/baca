import abjad
import baca
import numbers
from .Command import Command


class MicrotoneDeviationCommand(Command):
    r'''Microtone deviation command.

    ..  container:: example

        With alternating up- and down-quatertones:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.pitches('E4'),
            ...     baca.even_runs(),
            ...     baca.microtone_deviation([[0, 0.5, 0, -0.5]]),
            ...     )

        ::

            >>> result = segment_maker.run(is_doc_example=True)
            >>> lilypond_file, metadata = result
            >>> show(lilypond_file) # doctest: +SKIP

        ..  docs::

            >>> f(lilypond_file[abjad.Score])
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

    def __init__(self, deviations=None, selector='baca.select().qruns()'):
        Command.__init__(self, selector=selector)
        if deviations is not None:
            if all(isinstance(_, numbers.Number) for _ in deviations):
                deviations = (list(deviations),)
            else:
                deviations = tuple([list(_) for _ in deviations])
        self._deviations = deviations

    ### SPECIAL METHODS ###

    def __call__(self, music=None):
        r'''Calls command on `music`.

        Returns none.
        '''
        selections = self._select(music)
        if not self.deviations:
            return
        lists, i = abjad.CyclicTuple(self.deviations), 0
        for selection in selections:
            if len(selection) == 1:
                continue
            deviations = abjad.CyclicTuple(lists[i])
            plts = baca.select().plts()(selection)
            for j, plt in enumerate(plts):
                deviation = deviations[j]
                self._adjust_pitch(plt, deviation)
            i += 1

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

            ::

                >>> command = baca.microtone_deviation([0, -0.5, 0, 0.5])
                >>> command.deviations
                ([0, -0.5, 0, 0.5],)

            ::

                >>> command = baca.microtone_deviation(
                ...     [[0, -0.5, 0, 0.5], [0, 0.5, 0, -0.5]],
                ...     )
                >>> command.deviations
                ([0, -0.5, 0, 0.5], [0, 0.5, 0, -0.5])

        Set to one or more lists of +/- 0.5, or none.

        Returns tuple of one or more lists of +/- 0.5, or none.
        '''
        return self._deviations
