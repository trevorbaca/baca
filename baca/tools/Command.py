import abjad
import baca
import collections


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

    def __call__(self, music=None):
        r'''Calls command on `music`.

        Returns none.
        '''
        pass

    ### PRIVATE METHODS ###

    def _debug_selections(self, argument, selections):
        print(format(self))
        print(format(self.selector))
        print(argument)
        print(selections)
        print()
        
    def _select(self, argument):
        if argument is None:
            return
        if self.selector is not None:
            selections = self.selector(argument)
            if self.selector._is_singular_get_item():
                selections = [selections]
        else:
            selections = argument
        if not isinstance(selections, collections.Iterable):
            selections = [selections]
        return selections

    def _to_selection_list(self, argument):
        if not argument:
            selections = []
        elif isinstance(argument, abjad.Component):
            selections = [abjad.select(argument)]
        elif isinstance(argument, abjad.Selection):
            selections = [argument]
        # TODO: maybe remove this branch in favor of the next?
        elif (isinstance(argument, collections.Iterable) and
            all(type(_).__name__ == 'Selection' for _ in argument)):
            selections = list(argument)
        elif isinstance(argument, collections.Iterable):
            selections = []
            for item in argument:
                selections_ = self._to_selection_list(item)
                selections.extend(selections_)
        else:
            raise TypeError(f'unrecognized argument: {argument!r}.')
        assert isinstance(selections, list), repr(selections)
        assert all(isinstance(_, abjad.Selection) for _ in selections)
        return selections

    ### PUBLIC PROPERTIES ###

    @property
    def selector(self):
        r'''Gets selector.

        Defaults to none.

        Set to selector or none.

        Returns selector or none.
        '''
        return self._selector
