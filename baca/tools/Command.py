import abc
import abjad
import baca


class Command(abjad.AbjadObject):
    r'''Command.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Commands'

    __slots__ = (
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(self, selector=None):
        if isinstance(selector, str):
            selector = eval(selector)
        if selector is not None:
            assert isinstance(selector, abjad.Expression), repr(selector)
        self._selector = selector

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, argument=None):
        r'''Calls command on `argument`.

        Returns none.
        '''
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def selector(self):
        r'''Gets selector.

        Defaults to none.

        Set to selector or none.

        Returns selector or none.
        '''
        return self._selector
