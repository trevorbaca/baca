import abjad
import baca
from .Command import Command


class ColorFingeringCommand(Command):
    r'''Color fingering command.

    ..  container:: example

        With segment-maker:

        ::

            >>> segment_maker = baca.SegmentMaker(
            ...     score_template=baca.ViolinSoloScoreTemplate(),
            ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
            ...     )

        ::

            >>> segment_maker(
            ...     baca.scope('Violin Music Voice', 1),
            ...     baca.pitches('E4', allow_repeat_pitches=True),
            ...     baca.messiaen_notes(),
            ...     baca.ColorFingeringCommand(numbers=[0, 1, 2, 1]),
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
                            \set ViolinMusicStaff.instrumentName = \markup { Violin }
                            \set ViolinMusicStaff.shortInstrumentName = \markup { Vn. }
                            \clef "treble"
                            e'2
                            e'4.
                                ^ \markup {
                                    \override
                                        #'(circle-padding . 0.25)
                                        \circle
                                            \finger
                                                1
                                    }
                            e'2
                                ^ \markup {
                                    \override
                                        #'(circle-padding . 0.25)
                                        \circle
                                            \finger
                                                2
                                    }
                            e'4.
                                ^ \markup {
                                    \override
                                        #'(circle-padding . 0.25)
                                        \circle
                                            \finger
                                                1
                                    }
                            \bar "|"
                        }
                    }
                >>
            >>

    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        '_numbers',
        )

    ### INITIALIZER ###

    def __init__(self, numbers=None, selector='baca.select().pheads().group()'):
        Command.__init__(self, selector=selector)
        if numbers is not None:
            assert abjad.mathtools.all_are_nonnegative_integers(numbers)
        self._numbers = numbers

    ### SPECIAL METHODS ###

    def __call__(self, music=None):
        r'''Calls command on `music`.

        Returns none.
        '''
        selections = self._select(music)
        if not self.numbers:
            return
        numbers = abjad.CyclicTuple(self.numbers)
        for selection in selections:
            pleaves = baca.select().pleaves()(selection)
            for i, pleaf in enumerate(pleaves):
                number = numbers[i]
                if number != 0:
                    fingering = abjad.ColorFingering(number)
                    abjad.attach(fingering, pleaf)
                abjad.attach({'color fingering': True}, pleaf)

    ### PUBLIC PROPERTIES ###

    @property
    def numbers(self):
        r'''Gets numbers.

        ..  container:: example

            ::

                >>> command = baca.ColorFingeringCommand(numbers=[0, 1, 2, 1])
                >>> command.numbers
                [0, 1, 2, 1]

        Set to nonnegative integers.
        '''
        return self._numbers
