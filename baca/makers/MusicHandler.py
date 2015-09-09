# -*- coding: utf-8 -*-
from abjad import *


class MusicHandler(abctools.AbjadObject):
    r'''Ensemble music-handler.

    ..  container:: example

        ::

            >>> import baca
            >>> handler = baca.makers.MusicHandler(
            ...     scope=('Violin Music Voice', (1, 4)),
            ...     specifiers=[
            ...         baca.makers.DisplacementSpecifier(
            ...             displacements=[0, 0, 0, 0, 1, 1, 1, 1],
            ...             ),
            ...         ],
            ...     )

        ::

            >>> print(format(handler))
            baca.makers.MusicHandler(
                scope=baca.makers.SimpleScope(
                    context_name='Violin Music Voice',
                    stages=(1, 4),
                    ),
                specifiers=[
                    baca.makers.DisplacementSpecifier(
                        displacements=datastructuretools.CyclicTuple(
                            [0, 0, 0, 0, 1, 1, 1, 1]
                            ),
                        ),
                    ],
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
        if isinstance(scope, tuple):
            scope = baca.makers.SimpleScope(*scope)
        if scope is not None:
            assert isinstance(scope, baca.makers.SimpleScope), repr(scope)
        self._scope = scope
        assert isinstance(specifiers, list), repr(specifiers)
        self._specifiers = specifiers

    ### PUBLIC PROPERTIES ###

    @property
    def scope(self):
        r'''Gets scope of music-handler.

        ..  container:: example

            ::

                >>> print(format(handler.scope))
                baca.makers.SimpleScope(
                    context_name='Violin Music Voice',
                    stages=(1, 4),
                    )

        Set to scope or none.
        '''
        return self._scope

    @property
    def specifiers(self):
        r'''Gets specifiers of music-handler.

        ..  container:: example

            ::

                >>> print(format(handler.specifiers))
                [DisplacementSpecifier(displacements=CyclicTuple([0, 0, 0, 0, 1, 1, 1, 1]))]

        Set to list of specifiers or none.
        '''
        return self._specifiers