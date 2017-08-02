# -*- coding: utf-8 -*-
import abjad


class SpecifierWrapper(abjad.AbjadObject):
    r'''Specifier wrapper.

    ::

        >>> import abjad
        >>> import baca

    ..  container:: example

        Dynamic placed on first leaf that starts in stage (rather than on first
        tie chain that starts in stage):

        ::

            >>> specifier_wrapper = baca.SpecifierWrapper(
            ...     specifier=abjad.Dynamic('p'),
            ...     )

        ::
            
            >>> f(specifier_wrapper)
            baca.tools.SpecifierWrapper(
                specifier=abjad.Dynamic('p'),
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Segments'

    __slots__ = (
        '_prototype',
        '_specifier',
        '_start_index',
        '_stop_index',
        '_with_next_leaf',
        '_with_previous_leaf',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(
        self,
        prototype=None,
        specifier=None,
        start_index=None,
        stop_index=None,
        with_next_leaf=None,
        with_previous_leaf=None,
        ):
        self._prototype = prototype
        assert specifier is not None, repr(specifier)
        self._specifier = specifier
        self._start_index = start_index
        self._stop_index = stop_index
        self._with_next_leaf = with_next_leaf
        self._with_previous_leaf = with_previous_leaf

    ### PUBLIC PROPERTIES ###

    @property
    def prototype(self):
        r'''Gets prototype to filter on.

        Set to class, list of classes or none.

        Returns prototype, list of classes or none.
        '''
        return self._prototype

    @property
    def specifier(self):
        r'''Gets specifier.

        Set to specifier.

        Returns specifier.
        '''
        return self._specifier

    @property
    def start_index(self):
        r'''Gets start index.

        Set to integer or none.

        Returns integer or none.
        '''
        return self._start_index

    @property
    def stop_index(self):
        r'''Gets stop index.

        Set to integer or none.

        Returns integer or none.
        '''
        return self._stop_index

    @property
    def with_next_leaf(self):
        r'''Is true when specifier includes next leaf (after last leaf).
        Otherwise false.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._with_next_leaf

    @property
    def with_previous_leaf(self):
        r'''Is true when specifier includes previous leaf (before first leaf).
        Otherwise false.

        Set to true, false or none.

        Returns true, false or none.
        '''
        return self._with_previous_leaf
