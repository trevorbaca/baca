class Coat(object):
    r'''Coat.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utilities'

    __slots__ = (
        '_argument',
        )

    ### INITIALIZER ###

    def __init__(self, argument):
        self._argument = argument

    ### PUBLIC PROPERTIES ###

    @property
    def argument(self):
        r'''Gets argument.
        '''
        return self._argument
