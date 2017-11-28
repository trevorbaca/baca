import abjad


class PageSpecifier(abjad.AbjadObject):
    r'''Page specifier.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = '(5) Utilities'

    __slots__ = (
        '_items',
        )

    ### INITIALIZER ###

    def __init__(self, items=None):
        self._items = items

    ### PUBLIC PROPERTIES ###

    @property
    def items(self):
        r'''Gets items.
        '''
        return self._items
