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
            command=baca.ScorePitchCommand(
                allow_repeat_pitches=True,
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
            scope=baca.Scope(
                voice_name='Violin Music Voice',
                stages=baca.StageSpecifier(
                    start=1,
                    stop=4,
                    ),
                ),
            )

    ..  container:: example

        Pitch command wrapped with compound scope:

        >>> command = baca.CommandWrapper(
        ...     baca.pitches([7, 1, 3, 4, 5, 11]),
        ...     baca.compound([
        ...         baca.scope('Violin Music Voice', 1, 4),
        ...         baca.scope('Violin Music Voice', 8, 12),
        ...         ]),
        ...     )

        >>> abjad.f(command)
        baca.CommandWrapper(
            command=baca.ScorePitchCommand(
                allow_repeat_pitches=True,
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
                    baca.Scope(
                        voice_name='Violin Music Voice',
                        stages=baca.StageSpecifier(
                            start=1,
                            stop=4,
                            ),
                        ),
                    baca.Scope(
                        voice_name='Violin Music Voice',
                        stages=baca.StageSpecifier(
                            start=8,
                            stop=12,
                            ),
                        ),
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
        if scope is not None:
            prototype = (baca.Scope, baca.CompoundScope)
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
            baca.ScorePitchCommand(
                allow_repeat_pitches=True,
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

            >>> command = baca.CommandWrapper(
            ...     baca.pitches([7, 1, 3, 4, 5, 11]),
            ...     baca.scope('Violin Music Voice', 1, 4),
            ...     )

            >>> abjad.f(command.scope)
            baca.Scope(
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
