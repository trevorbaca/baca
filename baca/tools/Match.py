import abjad


class Match(abjad.AbjadObject):
    r'''Match.

    Decorates match callables.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_description',
        '_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name: str,
        description: str = None,
        ):
        self._name = name
        self._description = description

    ### SPECIAL METHODS ###

    def __call__(self, match):
        r'''Calls match decorator on `match`.

        Returns `match` with metadata attached.
        '''
        match.name = self.name
        match.description = self.description
        return match

    ### PUBLIC PROPERTIES ###

    @property
    def description(self) -> str:
        r'''Gets description.
        '''
        return self._description

    @property
    def name(self) -> str:
        r'''Gets name.
        '''
        return self._name
