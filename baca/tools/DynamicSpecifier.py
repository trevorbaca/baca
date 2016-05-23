# -*- coding: utf-8 -*-
import abjad


class DynamicSpecifier(abjad.abctools.AbjadObject):
    r'''Dynamic specifier.

    ::

        >>> import baca

    ..  container:: example

        **Example.**

        ::

            >>> baca.tools.DynamicSpecifier()
            DynamicSpecifier()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_dynamic',
        '_selector',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        dynamic=None,
        selector=None,
        ):
        if dynamic is not None:
            prototype = (
                str,
                abjad.indicatortools.Dynamic,
                abjad.spannertools.Hairpin,
                )
            assert isinstance(dynamic, prototype), repr(dynamic)
        self._dynamic = dynamic
        if selector is not None:
            assert isinstance(selector, abjad.selectortools.Selector)
        self._selector = selector

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        r'''Calls specifier on `expr`.

        Returns none.
        '''
        if self.dynamic is None:
            return
        #print(expr)
        selector = self._get_selector()
        #print(selector)
        selections = selector(expr)
        #print(selections)
        for selection in selections:
            if isinstance(self.dynamic, abjad.spannertools.Hairpin):
                hairpin = abjad.new(self.dynamic)
                leaves = list(abjad.iterate(selection).by_leaf())
                if hairpin._attachment_test_all(leaves):
                    abjad.attach(hairpin, leaves)
            elif isinstance(self.dynamic, (str, abjad.indicatortools.Dynamic)):
                dynamic = abjad.indicatortools.Dynamic(self.dynamic)
                abjad.attach(dynamic, selection[0])
            else:
                message = 'invalid dynamic: {!r}.'
                message = message.format(self.dynamic)
                raise Exception(message)
            
    ### PRIVATE METHODS ###

    def _get_selector(self):
        if self.selector is None:
            selector = abjad.selectortools.Selector()
            selector = selector.by_leaf()
            return selector
        return self.selector

    ### PUBLIC PROPERTIES ###

    @property
    def dynamic(self):
        r'''Gets dynamic.

        Defaults to none.

        Set to dynamic, hairpin or none.

        Returns dynamic, hairpin or none.
        '''
        return self._dynamic

    @property
    def selector(self):
        r'''Gets selector.

        Defaults to leaves.

        Set to selector or none.

        Returns selector or none.
        '''
        return self._selector