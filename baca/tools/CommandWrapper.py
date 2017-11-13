import abjad
import baca


class CommandWrapper(abjad.AbjadObject):
    r'''Command wrapper.

    ..  container:: example

        Pitch command wrapped with simple scope:

        >>> command = baca.CommandWrapper(
        ...     baca.pitches([7, 1, 3, 4, 5, 11]),
        ...     baca.scope('Violin Music Voice', 1, 4),
        ...     )

        >>> abjad.f(command)
        baca.CommandWrapper(
            command=baca.PitchCommand(
                cyclic=True,
                pitches=abjad.CyclicTuple(
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
            scope=baca.Scope(
                voice_name='Violin Music Voice',
                stages=(1, 4),
                ),
            )

    ..  container:: example

        Pitch command wrapped with timeline scope:

        >>> command = baca.CommandWrapper(
        ...     baca.pitches([7, 1, 3, 4, 5, 11]),
        ...     baca.timeline([
        ...         ('Violin Music Voice', 1, 4),
        ...         ('Viola Music Voice', 1, 4),
        ...         ]),
        ...     )

        >>> abjad.f(command)
        baca.CommandWrapper(
            command=baca.PitchCommand(
                cyclic=True,
                pitches=abjad.CyclicTuple(
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
            scope=baca.TimelineScope(
                scopes=(
                    baca.Scope(
                        voice_name='Violin Music Voice',
                        stages=(1, 4),
                        ),
                    baca.Scope(
                        voice_name='Viola Music Voice',
                        stages=(1, 4),
                        ),
                    ),
                ),
            )

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(6) Utilities'

    __slots__ = (
        '_command',
        '_scope',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, command=None, scope=None):
        if scope is not None:
            prototype = (baca.Scope, baca.TimelineScope)
            assert isinstance(scope, prototype), format(scope)
        self._scope = scope
        if command is not None:
            prototype = (baca.Builder, baca.Command)
            assert isinstance(command, prototype), format(command)
        self._command = command

    ### PUBLIC PROPERTIES ###

    @property
    def command(self):
        r'''Gets command.

        ..  container:: example

            >>> command = baca.CommandWrapper(
            ...     baca.pitches([7, 1, 3, 4, 5, 11]),
            ...     baca.scope('Violin Music Voice', 1, 4),
            ...     )

            >>> abjad.f(command.command)
            baca.PitchCommand(
                cyclic=True,
                pitches=abjad.CyclicTuple(
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

            >>> command = baca.CommandWrapper(
            ...     baca.pitches([7, 1, 3, 4, 5, 11]),
            ...     baca.scope('Violin Music Voice', 1, 4),
            ...     )

            >>> abjad.f(command.scope)
            baca.Scope(
                voice_name='Violin Music Voice',
                stages=(1, 4),
                )

        Defaults to none.

        Set to scope or none.

        Returns scope or none.
        '''
        return self._scope
