# -*- coding: utf-8 -*-
from abjad.tools import abctools


class ScopedSpecifier(abctools.AbjadObject):
    r'''Scoped specifier.

    ::

        >>> import baca

    ..  container:: example

        **Example 1.** Makes scoped pitch specifier:

        ::

            >>> specifier = baca.tools.ScopedSpecifier(
            ...     ('Violin Music Voice', (1, 4)),
            ...     baca.tools.PitchSpecifier(
            ...         source=[7, 1, 3, 4, 5, 11],
            ...         ),
            ...     )

        ::

            >>> print(format(specifier))
            baca.tools.ScopedSpecifier(
                scope=baca.tools.SimpleScope(
                    voice_name='Violin Music Voice',
                    stages=(1, 4),
                    ),
                specifier=baca.tools.PitchSpecifier(
                    source=datastructuretools.CyclicTuple(
                        [
                            pitchtools.NamedPitch("g'"),
                            pitchtools.NamedPitch("cs'"),
                            pitchtools.NamedPitch("ef'"),
                            pitchtools.NamedPitch("e'"),
                            pitchtools.NamedPitch("f'"),
                            pitchtools.NamedPitch("b'"),
                            ]
                        ),
                    ),
                )


    ..  container:: example

        **Example 2.** Makes pitch specifier with compound scope:

        ::

            >>> specifier = baca.tools.ScopedSpecifier(
            ...     baca.tools.CompoundScope([
            ...         baca.tools.SimpleScope('Violin Music Voice', (1, 4)),
            ...         baca.tools.SimpleScope('Violin Music Voice', (8, 12)),
            ...         ]),
            ...     baca.tools.PitchSpecifier(
            ...         source=[7, 1, 3, 4, 5, 11],
            ...         ),
            ...     )

        ::

            >>> print(format(specifier))
            baca.tools.ScopedSpecifier(
                scope=baca.tools.CompoundScope(
                    simple_scopes=(
                        baca.tools.SimpleScope(
                            voice_name='Violin Music Voice',
                            stages=(1, 4),
                            ),
                        baca.tools.SimpleScope(
                            voice_name='Violin Music Voice',
                            stages=(8, 12),
                            ),
                        ),
                    ),
                specifier=baca.tools.PitchSpecifier(
                    source=datastructuretools.CyclicTuple(
                        [
                            pitchtools.NamedPitch("g'"),
                            pitchtools.NamedPitch("cs'"),
                            pitchtools.NamedPitch("ef'"),
                            pitchtools.NamedPitch("e'"),
                            pitchtools.NamedPitch("f'"),
                            pitchtools.NamedPitch("b'"),
                            ]
                        ),
                    ),
                )


    ..  container:: example

        **Example 3.** Makes scoped displacement specifier:

        ::

            >>> specifier = baca.tools.ScopedSpecifier(
            ...     ('Violin Music Voice', (1, 4)),
            ...     baca.tools.OctaveDisplacementSpecifier(
            ...         displacements=[0, 0, 0, 0, 1, 1, 1, 1],
            ...         ),
            ...     )

        ::

            >>> print(format(specifier))
            baca.tools.ScopedSpecifier(
                scope=baca.tools.SimpleScope(
                    voice_name='Violin Music Voice',
                    stages=(1, 4),
                    ),
                specifier=baca.tools.OctaveDisplacementSpecifier(
                    displacements=datastructuretools.CyclicTuple(
                        [0, 0, 0, 0, 1, 1, 1, 1]
                        ),
                    ),
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Segment-maker components'

    __slots__ = (
        '_scope',
        '_specifier',
        )

    ### INITIALIZER ###

    def __init__(self, scope=None, specifier=None):
        import baca
        if isinstance(scope, tuple):
            scope = baca.tools.SimpleScope(*scope)
        prototype = (baca.tools.SimpleScope, baca.tools.CompoundScope)
        if scope is not None:
            assert isinstance(scope, prototype), repr(scope)
        self._scope = scope
        assert not isinstance(specifier, (tuple, list)), repr(specifier)
        self._specifier = specifier

    ### PUBLIC PROPERTIES ###

    @property
    def scope(self):
        r'''Gets scope.

        ..  container:: example

            **Example 1.** Gets scope:

            ::

                >>> specifier = baca.tools.ScopedSpecifier(
                ...     ('Violin Music Voice', (1, 4)),
                ...     baca.tools.PitchSpecifier(
                ...         source=[7, 1, 3, 4, 5, 11],
                ...         ),
                ...     )

            ::

                >>> print(format(specifier.scope))
                baca.tools.SimpleScope(
                    voice_name='Violin Music Voice',
                    stages=(1, 4),
                    )

        Defaults to none.

        Set to scope or none.

        Returns scope or none.
        '''
        return self._scope

    @property
    def specifier(self):
        r'''Gets specifier.

        ..  container:: example

            **Example 1.** Gets specifier:

            ::

                >>> specifier = baca.tools.ScopedSpecifier(
                ...     ('Violin Music Voice', (1, 4)),
                ...     baca.tools.PitchSpecifier(
                ...         source=[7, 1, 3, 4, 5, 11],
                ...         ),
                ...     )

            ::

                >>> print(format(specifier.specifier))
                baca.tools.PitchSpecifier(
                    source=datastructuretools.CyclicTuple(
                        [
                            pitchtools.NamedPitch("g'"),
                            pitchtools.NamedPitch("cs'"),
                            pitchtools.NamedPitch("ef'"),
                            pitchtools.NamedPitch("e'"),
                            pitchtools.NamedPitch("f'"),
                            pitchtools.NamedPitch("b'"),
                            ]
                        ),
                    )

        Defaults to none.

        Set to specifier or none.

        Returns specifier or none.
        '''
        return self._specifier