# -*- coding: utf-8 -*-
from abjad import *


class PitchHandler(abctools.AbjadObject):
    r'''ensemble pitch-handler.

    ..  container:: example

        ::

            >>> import baca
            >>> handler = baca.makers.PitchHandler(
            ...     scope=(['Flute Music Voice', 'Piano Music Voice'], (1, 4)),
            ...     )

        ::

            >>> print(format(handler))
            baca.makers.PitchHandler(
                scope=baca.makers.CompoundScope(
                    baca.makers.SimpleScope(
                        context_name='Flute Music Voice',
                        stages=(1, 4),
                        ),
                    baca.makers.SimpleScope(
                        context_name='Piano Music Voice',
                        stages=(1, 4),
                        )
                    ),
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_scope',
        '_specifiers',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        scope=None,
        specifiers=None,
        ):
        import baca
        parser = baca.makers.ScopeTokenParser()
        scope = parser._to_compound_scope(scope)
        assert isinstance(scope, baca.makers.CompoundScope), repr(scope)
        self._scope = scope
        if specifiers is not None:
            specifiers = tuple(specifiers)
        self._specifiers = specifiers

    ### PUBLIC PROPERTIES ###

    @property
    def scope(self):
        r'''Gets scope of pitch-handler.

        ..  container:: example

            ::

                >>> print(format(handler.scope))
                baca.makers.CompoundScope(
                    baca.makers.SimpleScope(
                        context_name='Flute Music Voice',
                        stages=(1, 4),
                        ),
                    baca.makers.SimpleScope(
                        context_name='Piano Music Voice',
                        stages=(1, 4),
                        )
                    )

        Set to compound scope.
        '''
        return self._scope

    @property
    def specifiers(self):
        r'''Gets specifiers of pitch-handler.

        ..  container:: example

            ::

                >>> handler.specifiers is None
                True

        Set to specifiers or none.
        '''
        return self._specifiers