import abjad
import baca


class Command(abjad.AbjadObject):
    r'''Command.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Commands'

    __slots__ = (
        '_selector',
        '_target',
        )

    ### INITIALIZER ###

    def __init__(self, selector=None, target=None):
        if isinstance(selector, str):
            selector = eval(selector)
        if selector is not None:
            assert isinstance(selector, abjad.Selector), repr(selector)
        self._selector = selector
        if isinstance(target, str):
            target = eval(target)
        if target is not None:
            assert isinstance(target, abjad.Selector), repr(target)
        self._target = target

    ### SPECIAL METHODS ###

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

    @property
    def target(self):
        r'''Gets target.

        Defaults to none.

        Set to target or none.

        Returns target or none.
        '''
        return self._target
