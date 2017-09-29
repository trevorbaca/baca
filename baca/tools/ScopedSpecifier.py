import abjad
import baca


class ScopedSpecifier(abjad.AbjadObject):
    r'''Scoped specifier.

    ..  container:: example

        Makes scoped pitch specifier:

        ::

            >>> specifier = baca.ScopedSpecifier(
            ...     ('Violin Music Voice', (1, 4)),
            ...     baca.ScorePitchCommand(
            ...         source=[7, 1, 3, 4, 5, 11],
            ...         ),
            ...     )

        ::

            >>> f(specifier)
            baca.ScopedSpecifier(
                scope=baca.SimpleScope(
                    voice_name='Violin Music Voice',
                    stages=(1, 4),
                    ),
                specifier=baca.ScorePitchCommand(
                    source=abjad.CyclicTuple(
                        [
                            abjad.NamedPitch("g'"),
                            abjad.NamedPitch("cs'"),
                            abjad.NamedPitch("ef'"),
                            abjad.NamedPitch("e'"),
                            abjad.NamedPitch("f'"),
                            abjad.NamedPitch("b'"),
                            ]
                        ),
                    ),
                )

    ..  container:: example

        Makes pitch specifier with compound scope:

        ::

            >>> specifier = baca.ScopedSpecifier(
            ...     baca.CompoundScope([
            ...         baca.SimpleScope('Violin Music Voice', (1, 4)),
            ...         baca.SimpleScope('Violin Music Voice', (8, 12)),
            ...         ]),
            ...     baca.ScorePitchCommand(
            ...         source=[7, 1, 3, 4, 5, 11],
            ...         ),
            ...     )

        ::

            >>> f(specifier)
            baca.ScopedSpecifier(
                scope=baca.CompoundScope(
                    simple_scopes=(
                        baca.SimpleScope(
                            voice_name='Violin Music Voice',
                            stages=(1, 4),
                            ),
                        baca.SimpleScope(
                            voice_name='Violin Music Voice',
                            stages=(8, 12),
                            ),
                        ),
                    ),
                specifier=baca.ScorePitchCommand(
                    source=abjad.CyclicTuple(
                        [
                            abjad.NamedPitch("g'"),
                            abjad.NamedPitch("cs'"),
                            abjad.NamedPitch("ef'"),
                            abjad.NamedPitch("e'"),
                            abjad.NamedPitch("f'"),
                            abjad.NamedPitch("b'"),
                            ]
                        ),
                    ),
                )

    ..  container:: example

        Makes scoped displacement specifier:

        ::

            >>> specifier = baca.ScopedSpecifier(
            ...     ('Violin Music Voice', (1, 4)),
            ...     baca.OctaveDisplacementCommand(
            ...         displacements=[0, 0, 0, 0, 1, 1, 1, 1],
            ...         ),
            ...     )

        ::

            >>> f(specifier)
            baca.ScopedSpecifier(
                scope=baca.SimpleScope(
                    voice_name='Violin Music Voice',
                    stages=(1, 4),
                    ),
                specifier=baca.OctaveDisplacementCommand(
                    displacements=abjad.CyclicTuple(
                        [0, 0, 0, 0, 1, 1, 1, 1]
                        ),
                    ),
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Segments'

    __slots__ = (
        '_scope',
        '_specifier',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, scope=None, specifier=None):
        if isinstance(scope, tuple):
            scope = baca.SimpleScope(*scope)
        prototype = (baca.SimpleScope, baca.CompoundScope)
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

            Gets scope:

            ::

                >>> specifier = baca.ScopedSpecifier(
                ...     ('Violin Music Voice', (1, 4)),
                ...     baca.ScorePitchCommand(
                ...         source=[7, 1, 3, 4, 5, 11],
                ...         ),
                ...     )

            ::

                >>> f(specifier.scope)
                baca.SimpleScope(
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

            Gets specifier:

            ::

                >>> specifier = baca.ScopedSpecifier(
                ...     ('Violin Music Voice', (1, 4)),
                ...     baca.ScorePitchCommand(
                ...         source=[7, 1, 3, 4, 5, 11],
                ...         ),
                ...     )

            ::

                >>> f(specifier.specifier)
                baca.ScorePitchCommand(
                    source=abjad.CyclicTuple(
                        [
                            abjad.NamedPitch("g'"),
                            abjad.NamedPitch("cs'"),
                            abjad.NamedPitch("ef'"),
                            abjad.NamedPitch("e'"),
                            abjad.NamedPitch("f'"),
                            abjad.NamedPitch("b'"),
                            ]
                        ),
                    )

        Defaults to none.

        Set to specifier or none.

        Returns specifier or none.
        '''
        return self._specifier
