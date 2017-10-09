import abjad
import baca


class CommandWrapper(abjad.AbjadObject):
    r'''Scoped command.

    ..  container:: example

        Wrapped pitch command:

        ::

            >>> command = baca.CommandWrapper(
            ...     baca.ScorePitchCommand(
            ...         source=[7, 1, 3, 4, 5, 11],
            ...         ),
            ...     baca.scope('Violin Music Voice', 1, 4),
            ...     )

        ::

            >>> f(command)
            baca.CommandWrapper(
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
                scope=baca.SimpleScope(
                    voice_name='Violin Music Voice',
                    stages=baca.StageSpecifier(
                        start=1,
                        stop=4,
                        ),
                    ),
                )

    ..  container:: example

        Pitch command wrapped with compound scope:

        ::

            >>> command = baca.CommandWrapper(
            ...     baca.ScorePitchCommand(
            ...         source=[7, 1, 3, 4, 5, 11],
            ...         ),
            ...     baca.compound([
            ...         baca.scope('Violin Music Voice', 1, 4),
            ...         baca.scope('Violin Music Voice', 8, 12),
            ...         ]),
            ...     )

        ::

            >>> f(command)
            baca.CommandWrapper(
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
                scope=baca.CompoundScope(
                    scopes=(
                        baca.SimpleScope(
                            voice_name='Violin Music Voice',
                            stages=baca.StageSpecifier(
                                start=1,
                                stop=4,
                                ),
                            ),
                        baca.SimpleScope(
                            voice_name='Violin Music Voice',
                            stages=baca.StageSpecifier(
                                start=8,
                                stop=12,
                                ),
                            ),
                        ),
                    ),
                )

    ..  container:: example

        Wrapped displacement command:

        ::

            >>> command = baca.CommandWrapper(
            ...     baca.OctaveDisplacementCommand(
            ...         displacements=[0, 0, 0, 0, 1, 1, 1, 1],
            ...         ),
            ...     baca.scope('Violin Music Voice', 1, 4),
            ...     )

        ::

            >>> f(command)
            baca.CommandWrapper(
                command=baca.OctaveDisplacementCommand(
                    displacements=abjad.CyclicTuple(
                        [0, 0, 0, 0, 1, 1, 1, 1]
                        ),
                    ),
                scope=baca.SimpleScope(
                    voice_name='Violin Music Voice',
                    stages=baca.StageSpecifier(
                        start=1,
                        stop=4,
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

    def __init__(self, command=None, scope=None):
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
                ...     baca.ScorePitchCommand(
                ...         source=[7, 1, 3, 4, 5, 11],
                ...         ),
                ...     baca.scope('Violin Music Voice', 1, 4),
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
                ...     baca.ScorePitchCommand(
                ...         source=[7, 1, 3, 4, 5, 11],
                ...         ),
                ...     baca.scope('Violin Music Voice', 1, 4),
                ...     )

            ::

                >>> f(command.scope)
                baca.SimpleScope(
                    voice_name='Violin Music Voice',
                    stages=baca.StageSpecifier(
                        start=1,
                        stop=4,
                        ),
                    )

        Defaults to none.

        Set to scope or none.

        Returns scope or none.
        '''
        return self._scope
