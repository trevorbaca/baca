import abjad
import baca
from .Command import Command
from .Typing import Optional
from .Typing import Selector


class StaffPositionCommand(Command):
    r'''Staff position command.

    ..  container:: example

        >>> staff = abjad.Staff("c' d' e' f'")
        >>> abjad.attach(abjad.Clef('treble'), staff[0])
        >>> command = baca.staff_positions([0, 2])
        >>> command(staff)
        >>> abjad.show(staff, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff, strict=89)
            \new Staff
            {
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
        >>> abjad.show(staff, strict=89) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff, strict=89)
            \new Staff
            {
                \clef "percussion"
                c'4
                e'4
                c'4
                e'4
            }

    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_exact',
        '_numbers',
        '_repeats',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        numbers,
        exact: bool = None, 
        repeats: bool = None,
        selector: Selector = 'baca.plts()',
        ) -> None:
        Command.__init__(self, selector=selector)
        if exact is not None:
            exact = bool(exact)
        self._exact = exact
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
        plt_count = 0
        for i, plt in enumerate(baca.select(argument).plts()):
            clef = abjad.inspect(plt.head).get_effective(
                abjad.Clef,
                default=abjad.Clef('treble'),
                )
            number = self.numbers[i]
            position = abjad.StaffPosition(number)
            pitch = position.to_pitch(clef)
            baca.PitchCommand._set_lt_pitch(plt, pitch)
            plt_count += 1
            if self.repeats:
                for pleaf in plt:
                    abjad.attach(abjad.tags.ALLOW_REPEAT_PITCH, pleaf)
                    abjad.attach(abjad.tags.DO_NOT_TRANSPOSE, pleaf)
        if self.exact and plt_count != len(self.numbers):
            message = f'PLT count ({plt_count}) does not match'
            message += f' staff position count ({len(self.numbers)}).'
            raise Exception(message)

    ### PUBLIC PROPERTIES ###

    @property
    def exact(self) -> Optional[bool]:
        r'''Is true when number of staff positions must match number of leaves
        exactly.
        '''
        return self._exact

    @property
    def numbers(self) -> Optional[abjad.CyclicTuple]:
        r'''Gets numbers.
        '''
        return self._numbers

    @property
    def repeats(self) -> Optional[bool]:
        r'''Is true when repeat staff positions are allowed.
        '''
        return self._repeats
