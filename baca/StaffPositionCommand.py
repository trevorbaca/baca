import abjad
import baca
import typing
from .Command import Command
from .PitchCommand import PitchCommand
from .Typing import Selector


class StaffPositionCommand(Command):
    r"""
    Staff position command.

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

    """

    ### CLASS ATTRIBUTES ###

    __slots__ = (
        '_allow_repeats',
        '_exact',
        '_numbers',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        numbers,
        allow_repeats: bool = None,
        exact: bool = None, 
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
        if allow_repeats is not None:
            allow_repeats = bool(allow_repeats)
        self._allow_repeats = allow_repeats

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Calls command on ``argument``.
        """
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
            PitchCommand._set_lt_pitch(plt, pitch)
            plt_count += 1
            for pleaf in plt:
                abjad.attach(abjad.tags.STAFF_POSITION, pleaf)
                if self.allow_repeats:
                    abjad.attach(abjad.tags.ALLOW_REPEAT_PITCH, pleaf)
                    abjad.attach(abjad.tags.DO_NOT_TRANSPOSE, pleaf)
        if self.exact and plt_count != len(self.numbers):
            message = f'PLT count ({plt_count}) does not match'
            message += f' staff position count ({len(self.numbers)}).'
            raise Exception(message)

    ### PUBLIC PROPERTIES ###

    @property
    def allow_repeats(self) -> typing.Optional[bool]:
        """
        Is true when repeat staff positions are allowed.
        """
        return self._allow_repeats

    @property
    def exact(self) -> typing.Optional[bool]:
        """
        Is true when number of staff positions must match number of leaves
        exactly.
        """
        return self._exact

    @property
    def numbers(self) -> typing.Optional[abjad.CyclicTuple]:
        """
        Gets numbers.
        """
        return self._numbers
