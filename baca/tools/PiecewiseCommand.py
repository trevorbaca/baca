import abjad
import collections
from .Command import Command


class PiecewiseCommand(Command):
    r'''Piecewise command.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        '_commands',
        )

    ### INITIALIZER ###

    def __init__(self, commands):
        assert isinstance(commands, collections.Iterable), repr(commands)
        self._commands = commands

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if not self.commands:
            return
        if argument is None:
            return
        for command in self.commands:
            command(argument)

    ### PUBLIC PROPERTIES ###

    @property
    def commands(self):
        r'''Gets commands.
        '''
        return self._commands
