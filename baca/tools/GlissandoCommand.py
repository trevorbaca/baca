import abjad
import baca
import collections
from .Command import Command


class GlissandoCommand(Command):
    r'''Glissando command.
    '''

    ### CLASS VARIABLES ##

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, selector='baca.select().leaves()'):
        Command.__init__(self, selector=selector)

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        if self.selector:
            argument = self.selector(argument)
        if not argument:
            return
        leaves = abjad.select(argument).leaves()
        if 1 < len(leaves):
            abjad.attach(abjad.Glissando(), leaves)
