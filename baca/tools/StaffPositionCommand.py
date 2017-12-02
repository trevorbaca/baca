import abjad
import baca
from .Command import Command


class StaffPositionCommand(Command):
    r'''Staff position command.

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> abjad.attach(abjad.Clef('treble'), staff[0])
        >>> command = baca.staff_positions([0, 2])
        >>> command(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff, strict=True)
            \new Staff {
                \clef "treble"
                b'4
                d''4
                b'4
                d''4
            }

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> abjad.attach(abjad.Clef('percussion'), staff[0])
        >>> command = baca.staff_positions([0, 2])
        >>> command(staff)
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff, strict=True)
            \new Staff {
                \clef "percussion"
                c'4
                e'4
                c'4
                e'4
            }

    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_numbers',
        '_repeats',
        )

    ### INITIALIZER ###

    def __init__(self, numbers, repeats=None, selector='baca.plts()'):
        Command.__init__(self, selector=selector)
        if numbers is not None:
            assert all(isinstance(_, int) for _ in numbers), repr(numbers)
            numbers = abjad.CyclicTuple(numbers)
        self._numbers = numbers
        if repeats is not None:
            repeats = bool(repeats)
        self._repeats = repeats

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
        for i, plt in enumerate(baca.select(argument).plts()):
            clef = abjad.inspect(plt.head).get_effective(abjad.Clef)
            number = self.numbers[i]
            position = abjad.StaffPosition(number)
            pitch = position.to_pitch(clef)
            baca.PitchCommand._set_lt_pitch(plt, pitch)
            if self.repeats:
                for pleaf in plt:
                    abjad.attach('repeat pitch allowed', pleaf)

    ### PUBLIC PROPERTIES ###

    @property
    def numbers(self):
        r'''Gets numbers.

        Defaults to none.

        Set to integers or none.

        Returns cyclic tuple of integers or none.
        '''
        return self._numbers

    @property
    def repeats(self):
        r'''Is true when repeat staff positions are allowed.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._repeats
