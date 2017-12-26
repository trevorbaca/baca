import abc
import abjad
import baca


class Command(abjad.AbjadObject):
    r'''Command.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(4) Commands'

    __slots__ = (
        '_manifests',
        '_selector',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, selector=None):
        self._manifests = None
        if isinstance(selector, str):
            selector = eval(selector)
        if selector is not None:
            prototype = (abjad.Expression, baca.MapCommand)
            assert isinstance(selector, prototype), repr(selector)
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
