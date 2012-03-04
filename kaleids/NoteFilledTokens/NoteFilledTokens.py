from kaleids.SignalAffixedNoteFilledTokens import SignalAffixedNoteFilledTokens


class NoteFilledTokens(SignalAffixedNoteFilledTokens):
    '''Note-filled tokens.

    See the test file for examples.
    '''

    ### CLASS ATTRIBUTES ###

    args = ()
    kwargs = ()

    def __init__(self):
        SignalAffixedNoteFilledTokens.__init__(self, [], [0], [], [0], 1)

    ### OVERLOADS ###

    def __repr__(self):
        return '%s()' % type(self).__name__
