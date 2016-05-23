# -*- coding: utf-8 -*-
import abjad


class SpannerSpecifier(abjad.abctools.AbjadObject):
    r'''Spanner specifier.

    ::

        >>> import baca

    ..  container:: example

        **Example.**

        ::

            >>> baca.tools.SpannerSpecifier()
            SpannerSpecifier()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_selector',
        '_spanner',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        selector=None,
        spanner=None,
        ):
        if selector is not None:
            assert isinstance(selector, abjad.selectortools.Selector)
        self._selector = selector
        if spanner is not None:
            assert isinstance(spanner, abjad.spannertools.Spanner)
        self._spanner = spanner

    ### SPECIAL METHODS ###

    def __call__(self, selection):
        r'''Calls spanner figure specifier on `selection`.

        Returns none.
        '''
        if self.spanner is None:
            return
        selector = self._get_selector()
        #print(selector)
        #print(selection)
        selections = selector(selection)
        #print(selections)
        for index, selection in enumerate(selections):
            self._apply_payload(index, selection)
            
    ### PRIVATE METHODS ###

    def _apply_payload(self, index, selection):
        spanner = abjad.new(self.spanner)
        leaves = list(abjad.iterate(selection).by_leaf())
        if 1 < len(leaves):
            abjad.attach(spanner, leaves)

    def _get_selector(self):
        if self.selector is None:
            selector = abjad.select()
            selector = selector.by_leaf()
            return selector
        return self.selector

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
    def spanner(self):
        r'''Gets spanner.

        Defaults to none.

        Set to spanner or none.

        Returns spanner or none.
        '''
        return self._spanner