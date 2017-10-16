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

    ### PRIVATE METHODS ###

    def _preprocess(self, argument):
        selections = self._to_selection_list(argument)
        if self.selector is not None:
            selections = [self.selector(_) for _ in selections]
            selections = self._to_selection_list(selections)
        if self.target is not None:
            selections = [self.target(_) for _ in selections]
            selections = self._to_selection_list(selections)
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

    @property
    def target(self):
        r'''Gets target.

        Defaults to none.

        Set to target or none.

        Returns target or none.
        '''
        return self._target

    ### PUBLIC METHODS ###

    def normalize(self, argument):
        r'''Normalizes `argument` for iteration.
        
        Returns `argument` wrapped in list when target selector returns item.

        Returns `argument` as-is when target selector does not return item.
        '''
        import abjad
        targets = self.target(argument)
        if isinstance(self.target.callbacks[-1], abjad.ItemSelectorCallback):
            targets = [targets]
        return targets
