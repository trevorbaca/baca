# -*- coding: utf-8 -*-
from abjad import *


class CompoundScope(abctools.AbjadObject):
    r'''Compound scope.

    ..  container:: example
    
        ::

            >>> import baca
            >>> scope = baca.makers.CompoundScope(
            ...     baca.makers.SimpleScope('Piano Music Voice', (5, 9)),
            ...     baca.makers.SimpleScope('Clarinet Music Voice', (7, 12)),
            ...     baca.makers.SimpleScope('Violin Music Voice', (8, 12)),
            ...     baca.makers.SimpleScope('Oboe Music Voice', (9, 12)),
            ...     )

        ::

            >>> print(format(scope, 'storage'))
            baca.makers.CompoundScope(
                baca.makers.SimpleScope(
                    context_name='Piano Music Voice',
                    stages=(5, 9),
                    ),
                baca.makers.SimpleScope(
                    context_name='Clarinet Music Voice',
                    stages=(7, 12),
                    ),
                baca.makers.SimpleScope(
                    context_name='Violin Music Voice',
                    stages=(8, 12),
                    ),
                baca.makers.SimpleScope(
                    context_name='Oboe Music Voice',
                    stages=(9, 12),
                    )
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context_names',
        '_simple_scopes',
        '_timespan_map',
        )

    ### INITIALIZER ###

    def __init__(self, *simple_scopes):
        from baca import makers
        for simple_scope in simple_scopes:
            assert isinstance(simple_scope, makers.SimpleScope), simple_scope
        self._context_names = []
        self._simple_scopes = tuple(simple_scopes)
        self._timespan_map = None

    ### SPECIAL METHODS ###

    def __contains__(self, component):
        if self._timespan_map is None:
            message = 'must construct timespan map first.'
            raise Exception(message)
        voice = inspect_(component).get_parentage().get_first(Voice)
        component_timespan = inspect_(component).get_timespan()
        for context_name, scope_timespan in self._timespan_map:
            if context_name == voice.name:
                if component_timespan.starts_during_timespan(scope_timespan):
                    return True
        return False

    ### PRIVATE PROPERTIES ###
    
    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = self.simple_scopes
        return systemtools.StorageFormatSpecification(
            self,
            positional_argument_values=positional_argument_values,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def simple_scopes(self):
        r'''Gets simple scopes that comprise compound scope.

        Set to simple scopes or none.
        '''
        return self._simple_scopes