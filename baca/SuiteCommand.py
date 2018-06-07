import baca
import collections
import typing
from .Command import Command
from .Typing import Selector


class SuiteCommand(Command):
    """
    Suite command.

    ..  container:: example

        >>> baca.SuiteCommand()
        SuiteCommand()

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_commands',
        '_selector',
        )

    ### INITIALIZER ###

    # TODO: remove selector?
    def __init__(
        self,
        *commands: Command,
        selector: Selector = None,
        ) -> None:
        Command.__init__(self, selector=selector)
        command_list: typing.List[Command] = []
        for command in commands:
            if not isinstance(command, Command):
                message = '\n  Commands must contain only commands.'
                message += f'\n  Not {type(command).__name__}: {command!r}.'
                raise Exception(message)
            command_list.append(command)
        self._commands = tuple(command_list)

    ### SPECIAL METHODS ###

    def __call__(self, argument=None) -> None:
        """
        Applies commands to result of selector called on ``argument``.
        """
        if argument is None:
            return
        if not self.commands:
            return
        if self.selector is not None:
            argument = self.selector(argument)
        for command in self.commands:
            command(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def commands(self) -> typing.Tuple[Command, ...]:
        """
        Gets commands.
        """
        return self._commands
