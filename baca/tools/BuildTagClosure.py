import abjad


class BuildTagClosure(abjad.AbjadObject):
    r'''Build tag closure.

    ..  container:: example

        >>> baca.BuildTagClosure()
        BuildTagClosure()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_build_tag',
        '_command',
        )

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, build_tag=None, command=None):
        if build_tag is not None:
            build_tag = getattr(build_tag, 'name', build_tag)
            assert isinstance(build_tag, str), repr(build_tag)
        self._build_tag = build_tag
        if command is not None:
            assert isinstance(command, baca.Command), repr(command)
        self._command = command

    ### PUBLIC PROPERTIES ###

    @property
    def build_tag(self):
        r'''Gets build tag.

        Set to tag or string.

        Returns string.
        '''
        return self._build_tag

    @property
    def command(self):
        r'''Gets command.

        Set to comand or none.

        Returns command or none.
        '''
        return self._command
