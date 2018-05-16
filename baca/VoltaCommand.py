import abjad
import baca
from .Command import Command


class VoltaCommand(Command):
    """
    Volta command.

    ..  container:: example

        >>> baca.VoltaCommand()
        VoltaCommand()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Applies command to result of selector called on ``argument``.
        """
        if argument is None:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        leaves = baca.select(argument).leaves()
        container = abjad.Container()
        abjad.mutate(leaves).wrap(container)
        abjad.attach(abjad.Repeat(), container)
