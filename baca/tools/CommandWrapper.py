import abjad
import baca


class CommandWrapper(abjad.AbjadObject):
    r'''Scoped command.

    ..  container:: example

        Scoped pitch command:

        ::

            >>> command = baca.CommandWrapper(
            ...     ('Violin Music Voice', (1, 4)),
            ...     baca.ScorePitchCommand(
            ...         source=[7, 1, 3, 4, 5, 11],
            ...         ),
            ...     )

        ::

            >>> f(command)
            baca.CommandWrapper(
                scope=baca.SimpleScope(
                    voice_name='Violin Music Voice',
                    stages=(1, 4),
                    ),
                command=baca.ScorePitchCommand(
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

        Scoped pitch command with compound scope:

        ::

            >>> command = baca.CommandWrapper(
            ...     baca.CompoundScope([
            ...         baca.SimpleScope('Violin Music Voice', (1, 4)),
            ...         baca.SimpleScope('Violin Music Voice', (8, 12)),
            ...         ]),
            ...     baca.ScorePitchCommand(
            ...         source=[7, 1, 3, 4, 5, 11],
            ...         ),
            ...     )

        ::

            >>> f(command)
            baca.CommandWrapper(
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
                command=baca.ScorePitchCommand(
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

        Scoped displacement command:

        ::

            >>> command = baca.CommandWrapper(
            ...     ('Violin Music Voice', (1, 4)),
            ...     baca.OctaveDisplacementCommand(
            ...         displacements=[0, 0, 0, 0, 1, 1, 1, 1],
            ...         ),
            ...     )

        ::

            >>> f(command)
            baca.CommandWrapper(
                scope=baca.SimpleScope(
                    voice_name='Violin Music Voice',
                    stages=(1, 4),
                    ),
                command=baca.OctaveDisplacementCommand(
                    displacements=abjad.CyclicTuple(
                        [0, 0, 0, 0, 1, 1, 1, 1]
                        ),
                    ),
                )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        '_command',
        '_scope',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, scope=None, command=None):
        if isinstance(scope, tuple):
            scope = baca.SimpleScope(*scope)
        prototype = (baca.SimpleScope, baca.CompoundScope)
        if scope is not None:
            assert isinstance(scope, prototype), repr(scope)
        self._scope = scope
        assert not isinstance(command, (tuple, list)), repr(command)
        classname = type(command).__name__
        if not classname.endswith('Command'):
            raise Exception(format(command))
        self._command = command

    ### PUBLIC PROPERTIES ###

    @property
    def command(self):
        r'''Gets command.

        ..  container:: example

            ::

                >>> command = baca.CommandWrapper(
                ...     ('Violin Music Voice', (1, 4)),
                ...     baca.ScorePitchCommand(
                ...         source=[7, 1, 3, 4, 5, 11],
                ...         ),
                ...     )

            ::

                >>> f(command.command)
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

        Set to command or none.

        Returns command or none.
        '''
        return self._command

    @property
    def scope(self):
        r'''Gets scope.

        ..  container:: example

            Gets scope:

            ::

                >>> command = baca.CommandWrapper(
                ...     ('Violin Music Voice', (1, 4)),
                ...     baca.ScorePitchCommand(
                ...         source=[7, 1, 3, 4, 5, 11],
                ...         ),
                ...     )

            ::

                >>> f(command.scope)
                baca.SimpleScope(
                    voice_name='Violin Music Voice',
                    stages=(1, 4),
                    )

        Defaults to none.

        Set to scope or none.

        Returns scope or none.
        '''
        return self._scope
