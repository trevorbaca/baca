# -*- coding: utf-8 -*-
from abjad import *


class PitchHandler(abctools.AbjadObject):
    r'''Pitch handler.

    ..  container:: example

        **Example 1.** Makes pitch handler with no specifier:

        ::

            >>> import baca

        ::

            >>> handler = baca.tools.PitchHandler(
            ...     scope=(['Flute Music Voice', 'Piano Music Voice'], (1, 4)),
            ...     specifier=baca.tools.PitchSpecifier(
            ...         source=[-6, -5, -1, -2, 2],
            ...         ),
            ...     )

        ::

            >>> print(format(handler))
            baca.tools.PitchHandler(
                baca.tools.CompoundScope(
                    simple_scopes=(
                        baca.tools.SimpleScope(
                            voice_name='Flute Music Voice',
                            stages=(1, 4),
                            ),
                        baca.tools.SimpleScope(
                            voice_name='Piano Music Voice',
                            stages=(1, 4),
                            ),
                        ),
                    ),
                specifier=baca.tools.PitchSpecifier(
                    source=datastructuretools.CyclicTuple(
                        [
                            pitchtools.NamedPitch('fs'),
                            pitchtools.NamedPitch('g'),
                            pitchtools.NamedPitch('b'),
                            pitchtools.NamedPitch('bf'),
                            pitchtools.NamedPitch("d'"),
                            ]
                        ),
                    ),
                )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_scope',
        '_specifier',
        )

    ### INITIALIZER ###

    def __init__(self, scope, specifier=None):
        import baca
        scope = baca.tools.CompoundScope.from_token(scope)
        assert isinstance(scope, baca.tools.CompoundScope), repr(scope)
        self._scope = scope
        if specifier is not None:
            assert isinstance(specifier, baca.tools.PitchSpecifier)
        self._specifier = specifier

    ### PUBLIC PROPERTIES ###

    @property
    def scope(self):
        r'''Gets scope.

        ..  container:: example

            **Example 1.** Gets scope:

            ::

                >>> print(format(handler.scope))
                baca.tools.CompoundScope(
                    simple_scopes=(
                        baca.tools.SimpleScope(
                            voice_name='Flute Music Voice',
                            stages=(1, 4),
                            ),
                        baca.tools.SimpleScope(
                            voice_name='Piano Music Voice',
                            stages=(1, 4),
                            ),
                        ),
                    )

        Set to compound scope.

        Returns compound scope.
        '''
        return self._scope

    @property
    def specifier(self):
        r'''Gets specifier.

        ..  container:: example

            **Example 1.** Gets specifier:

            ::

                >>> handler = baca.tools.PitchHandler(
                ...     scope=(['Flute Music Voice', 'Piano Music Voice'], (1, 4)),
                ...     specifier=baca.tools.PitchSpecifier(
                ...         source=[-6, -5, -1, -2, 2],
                ...         ),
                ...     )

            ::

                >>> print(format(handler.specifier))
                baca.tools.PitchSpecifier(
                    source=datastructuretools.CyclicTuple(
                        [
                            pitchtools.NamedPitch('fs'),
                            pitchtools.NamedPitch('g'),
                            pitchtools.NamedPitch('b'),
                            pitchtools.NamedPitch('bf'),
                            pitchtools.NamedPitch("d'"),
                            ]
                        ),
                    )

        Set to specifier or none.

        Returns specifier or none.
        '''
        return self._specifier