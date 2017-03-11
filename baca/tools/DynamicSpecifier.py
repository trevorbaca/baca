# -*- coding: utf-8 -*-
import abjad
import baca


class DynamicSpecifier(abjad.abctools.AbjadObject):
    r'''Dynamic specifier.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

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
            prototype = (str, abjad.Dynamic, abjad.Hairpin)
            assert isinstance(dynamic, prototype), repr(dynamic)
        self._dynamic = dynamic
        if selector is not None:
            assert isinstance(selector, abjad.Selector)
        self._selector = selector

    ### SPECIAL METHODS ###

    def __call__(self, argument=None):
        r'''Calls specifier on `argument`.

        Returns none.
        '''
        if not argument:
            return
        if self.dynamic is None:
            return
        selector = self.selector or baca.select_leaves()
        selections = selector(argument)
        selections = baca.MusicMaker._normalize_selections(selections)
        for selection in selections:
            if isinstance(self.dynamic, abjad.Hairpin):
                hairpin = abjad.new(self.dynamic)
                leaves = list(abjad.iterate(selection).by_leaf())
                if hairpin._attachment_test_all(leaves):
                    abjad.attach(hairpin, leaves)
            elif isinstance(self.dynamic, (str, abjad.Dynamic)):
                dynamic = abjad.Dynamic(self.dynamic)
                abjad.attach(dynamic, selection[0])
            else:
                message = 'invalid dynamic: {!r}.'
                message = message.format(self.dynamic)
                raise Exception(message)
            
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
