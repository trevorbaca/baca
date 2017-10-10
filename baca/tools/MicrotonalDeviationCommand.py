import abjad
import itertools
from .Command import Command


class MicrotonalDeviationCommand(Command):
    r'''Microtonal deviation command.

    ..  container:: example

        With alternating up- and down-quatertones:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> specifiers = segment_maker.scope(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.pitches('E4'),
            ...     baca.even_runs(),
            ...     baca.MicrotonalDeviationCommand(
            ...         number_lists=([0, 0.5, 0, -0.5],),
            ...         ),
            ...     )

        ::

            >>> result = segment_maker(is_doc_example=True)
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

    __documentation_section__ = 'Commands'

    __slots__ = (
        '_deposit_annotations',
        '_number_lists',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        deposit_annotations=None,
        number_lists=None,
        ):
        if deposit_annotations is not None:
            deposit_annotations = tuple(deposit_annotations)
        self._deposit_annotations = deposit_annotations
        if number_lists is not None:
            number_lists = tuple(number_lists)
            for number_list in number_lists:
                assert isinstance(number_list, (list, tuple)), number_list
        self._number_lists = number_lists

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if self.number_lists is None:
            return
        number_lists = abjad.CyclicTuple(self.number_lists)
        number_list_index = 0
        logical_ties = argument
        pairs = itertools.groupby(
            logical_ties,
            lambda _: _.head.written_pitch,
            )
        for key, values in pairs:
            values = list(values)
            if len(values) == 1:
                continue
            number_list = number_lists[number_list_index]
            number_list = abjad.CyclicTuple(number_list)
            for i, logical_tie in enumerate(values):
                number = number_list[i]
                for note in logical_tie:
                    self._adjust_pitch(note, number)
                    self._attach_deposit_annotations(note)
            number_list_index += 1

    ### PRIVATE METHODS ###

    def _adjust_pitch(self, note, number):
        assert number in (0.5, 0, -0.5)
        if number == 0:
            return
        written_pitch = note.written_pitch
        written_pitch = written_pitch.transpose_staff_position(0, number)
        note.written_pitch = written_pitch

    def _attach_deposit_annotations(self, note):
        if not self.deposit_annotations:
            return
        for annotation_name in self.deposit_annotations:
            annotation = {annotation_name: True}
            abjad.attach(annotation, note)

    ### PUBLIC PROPERTIES ###

    @property
    def deposit_annotations(self):
        r'''Gets deposit annotations of command.

        These will be attached to every note affected at call time.

        Set to annotations or none.
        '''
        return self._deposit_annotations

    @property
    def number_lists(self):
        r'''Gets number lists.

        ..  container:: example

            ::

                >>> command = baca.MicrotonalDeviationCommand(
                ...     number_lists=(
                ...         [0, 1, 2, 1],
                ...         ),
                ...     )

            ::

                >>> command.number_lists
                ([0, 1, 2, 1],)

        Set to number lists or none.

        Returns tuple of number lists or none.
        '''
        return self._number_lists
