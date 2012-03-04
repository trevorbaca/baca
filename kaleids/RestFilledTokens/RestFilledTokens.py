from kaleids.SignalAffixedRestFilledTokens import SignalAffixedRestFilledTokens


class RestFilledTokens(SignalAffixedRestFilledTokens):
    '''Rest-filled tokens.

    See the test file for examples.
    '''

    ### CLASS ATTRIBUTES ###

    args = ()
    kwargs = ()

    def __init__(self):
        SignalAffixedRestFilledTokens.__init__(self, [], [0], [], [0], 1)

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % type(self).__name__
