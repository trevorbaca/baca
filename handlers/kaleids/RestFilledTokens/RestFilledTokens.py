from handlers.kaleids.TokenIncisedRestFilledTimeTokenMaker import TokenIncisedRestFilledTimeTokenMaker


class RestFilledTokens(TokenIncisedRestFilledTimeTokenMaker):
    '''Rest-filled tokens.

    See the test file for examples.
    '''

    ### CLASS ATTRIBUTES ###

    args = ()
    kwargs = ()

    def __init__(self):
        TokenIncisedRestFilledTimeTokenMaker.__init__(self, [], [0], [], [0], 1)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '%s()' % type(self).__name__
