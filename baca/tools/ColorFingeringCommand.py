import abjad
import baca
from .Command import Command


class ColorFingeringCommand(Command):
    r'''Color fingering command.

    ..  container:: example

        With segment-maker:

        >>> maker = baca.SegmentMaker(
        ...     score_template=baca.SingleStaffScoreTemplate(),
        ...     time_signatures=[(4, 8), (3, 8), (4, 8), (3, 8)],
        ...     )

        >>> maker(
        ...     baca.scope('Music Voice', 1),
        ...     baca.pitches('E4', repeats=True),
        ...     baca.make_notes(repeat_ties=True),
        ...     baca.ColorFingeringCommand(numbers=[0, 1, 2, 1]),
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

    def __init__(self, numbers=None, selector='baca.pheads()'):
        Command.__init__(self, selector=selector)
        if numbers is not None:
            assert abjad.mathtools.all_are_nonnegative_integers(numbers)
            numbers = abjad.CyclicTuple(numbers)
        self._numbers = numbers

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if argument is None:
            return
        if not self.numbers:
            return
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        for i, phead in enumerate(baca.select(argument).pheads()):
            number = self.numbers[i]
            if number != 0:
                fingering = abjad.ColorFingering(number)
                abjad.attach(fingering, phead)

    ### PUBLIC PROPERTIES ###

    @property
    def numbers(self):
        r'''Gets numbers.

        ..  container:: example

            >>> command = baca.ColorFingeringCommand(numbers=[0, 1, 2, 1])
            >>> command.numbers
            CyclicTuple([0, 1, 2, 1])

        Set to nonnegative integers.
        '''
        return self._numbers
