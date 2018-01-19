import abjad


class Match(abjad.AbjadObject):
    r'''Match.

    ..  container:: example

        >>> match = baca.Match(match_any=['BREAK', 'SHIFTED_CLEF'])

        >>> match('       %! BREAK')
        True

        >>> match('       %! SHIFTED_CLEF')
        True

        >>> match('       %! FOO')
        False

        >>> match('       %! BAR')
        False

        >>> match('       %! BREAK:SHIFTED_CLEF')
        True

        >>> match('       %! BREAK:FOO')
        True

        >>> match('       %! BREAK:BAR')
        True

        >>> match('       %! SHIFTED_CLEF:FOO')
        True

        >>> match('       %! SHIFTED_CLEF:BAR')
        True

        >>> match('       %! FOO:BAR')
        False

        >>> match('       %! BREAK:SHIFTED_CLEF:FOO')
        True

        >>> match('       %! BREAK:SHIFTED_CLEF:BAR')
        True

        >>> match('       %! BREAK:FOO:BAR')
        True

        >>> match('       %! SHIFTED_CLEF:FOO:BAR')
        True

    ..  container:: example

        >>> match = baca.Match(
        ...     match_any=['BREAK', 'SHIFTED_CLEF'],
        ...     forbid_any=['FOO', 'BAR'],
        ...     )

        >>> match('       %! BREAK')
        True

        >>> match('       %! SHIFTED_CLEF')
        True

        >>> match('       %! FOO')
        False

        >>> match('       %! BAR')
        False

        >>> match('       %! BREAK:SHIFTED_CLEF')
        True

        >>> match('       %! BREAK:FOO')
        False

        >>> match('       %! BREAK:BAR')
        False

        >>> match('       %! SHIFTED_CLEF:FOO')
        False

        >>> match('       %! SHIFTED_CLEF:BAR')
        False

        >>> match('       %! FOO:BAR')
        False

        >>> match('       %! BREAK:SHIFTED_CLEF:FOO')
        False

        >>> match('       %! BREAK:SHIFTED_CLEF:BAR')
        False

        >>> match('       %! BREAK:FOO:BAR')
        False

        >>> match('       %! SHIFTED_CLEF:FOO:BAR')
        False

    ..  container:: example

        >>> match = baca.Match(
        ...     match_any=['BREAK', 'SHIFTED_CLEF'],
        ...     forbid_all=['FOO', 'BAR'],
        ...     )

        >>> match('       %! BREAK')
        True

        >>> match('       %! SHIFTED_CLEF')
        True

        >>> match('       %! FOO')
        False

        >>> match('       %! BAR')
        False

        >>> match('       %! BREAK:SHIFTED_CLEF')
        True

        >>> match('       %! BREAK:FOO')
        True

        >>> match('       %! BREAK:BAR')
        True

        >>> match('       %! SHIFTED_CLEF:FOO')
        True

        >>> match('       %! SHIFTED_CLEF:BAR')
        True

        >>> match('       %! FOO:BAR')
        False

        >>> match('       %! BREAK:SHIFTED_CLEF:FOO')
        True

        >>> match('       %! BREAK:SHIFTED_CLEF:BAR')
        True

        >>> match('       %! BREAK:FOO:BAR')
        False

        >>> match('       %! SHIFTED_CLEF:FOO:BAR')
        False

    ..  container:: example

        >>> match = baca.Match(match_all=['BREAK', 'SHIFTED_CLEF'])

        >>> match('       %! BREAK')
        False

        >>> match('       %! SHIFTED_CLEF')
        False

        >>> match('       %! FOO')
        False

        >>> match('       %! BAR')
        False

        >>> match('       %! BREAK:SHIFTED_CLEF')
        True

        >>> match('       %! BREAK:FOO')
        False

        >>> match('       %! BREAK:BAR')
        False

        >>> match('       %! SHIFTED_CLEF:FOO')
        False

        >>> match('       %! SHIFTED_CLEF:BAR')
        False

        >>> match('       %! FOO:BAR')
        False

        >>> match('       %! BREAK:SHIFTED_CLEF:FOO')
        True

        >>> match('       %! BREAK:SHIFTED_CLEF:BAR')
        True

        >>> match('       %! BREAK:FOO:BAR')
        False

        >>> match('       %! SHIFTED_CLEF:FOO:BAR')
        False

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_forbid_all',
        '_forbid_any',
        '_match_all',
        '_match_any',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        forbid_all=None,
        forbid_any=None,
        match_all=None,
        match_any=None,
        ):
        self._forbid_all = forbid_all
        self._forbid_any = forbid_any
        self._match_all = match_all
        self._match_any = match_any

    ### SPECIAL METHODS ###

    def __call__(self, line):
        assert isinstance(line, str), repr(line)
        if ' %! ' not in line:
            return False
        index = line.find('%! ')
        line = line[index+2:].strip()
        parts = line.split()
        tags = parts[0]
        tags = tags.split(':')
        if self.forbid_any and any(_ in tags for _ in self.forbid_any):
            return False
        if self.forbid_all and all(_ in tags for _ in self.forbid_all):
            return False
        if self.match_all and not all(_ in tags for _ in self.match_all):
            return False
        if self.match_any and not any(_ in tags for _ in self.match_any):
            return False
        return True

    ### PUBLIC PROPERTIES ###

    @property
    def forbid_all(self):
        r'''Gets forbid-all tags.

        Returns list.
        '''
        return self._forbid_all

    @property
    def forbid_any(self):
        r'''Gets forbid-any tags.

        Returns list.
        '''
        return self._forbid_any

    @property
    def match_all(self):
        r'''Gets match-all tags.

        Returns list.
        '''
        return self._match_all

    @property
    def match_any(self):
        r'''Gets match-any tags.

        Returns list.
        '''
        return self._match_any
