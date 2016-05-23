# -*- coding: utf-8 -*-
import abjad


class ArticulationSpecifier(abjad.abctools.AbjadObject):
    r'''Articulation specifier.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_articulations',
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        articulations=None,
        selector=None,
        ):
        if articulations is not None:
            prototype = (abjad.indicatortools.Articulation, str)
            assert all(isinstance(_, prototype) for _ in articulations)
        self._articulations = articulations
        if selector is not None:
            assert isinstance(selector, abjad.selectortools.Selector)
        self._selector = selector

    ### SPECIAL METHODS ###

    def __call__(self, selection):
        r'''Calls articulation specifier on `selection`.

        Returns none.
        '''
        if self.articulations is None:
            return
        selector = self._get_selector()
        #print(selector)
        selections = selector(selection)
        #print(selections)
        for index, selection in enumerate(selections):
            self._apply_payload(index, selection)

    ### PRIVATE METHODS ###

    def _apply_payload(self, index, selection):
        for component in selection:
            for articulation in self.articulations:
                articulation = abjad.indicatortools.Articulation(articulation)
                abjad.attach(articulation, component)

    def _get_selector(self):
        if self.selector is None:
            selector = abjad.selectortools.Selector()
            selector = selector.by_leaf()
            return selector
        return self.selector

    ### PUBLIC PROPERTIES ###

    @property
    def articulations(self):
        r'''Gets articulations.

        Defaults to none.

        Set to articulations or none.

        Returns articulations or none.
        '''
        return self._articulations

    @property
    def selector(self):
        r'''Gets selector.

        Defaults to none.

        Set to selector or none.

        Returns selector or none.
        '''
        return self._selector