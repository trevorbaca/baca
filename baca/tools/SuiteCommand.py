import baca
import collections
from .Command import Command


class SuiteCommand(Command):
    r'''Suite command.

    ..  container:: example

        >>> baca.SuiteCommand()
        SuiteCommand()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_commands',
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(self, commands=None, selector=None):
        Command.__init__(self, selector=selector)
        if isinstance(commands, baca.Command):
            commands = (commands,)
        elif isinstance(commands, collections.Iterable):
            commands = tuple(commands)
        self._commands = commands

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Applies commands to result of selector called on `argument`.

        Returns none.
        '''
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
    def commands(self):
        r'''Gets commands.

        Returns tuple or none.
        '''
        return self._commands
