from baca.rhythm.kaleids._SignalAffixedChunkWithFilledTokens import _SignalAffixedChunkWithFilledTokens


class SignalAffixedChunkWithNoteFilledTokens(_SignalAffixedChunkWithFilledTokens):
    '''Signal-affixed chunks with rest-filled tokens.
    '''

    ## PRIVATE METHODS ##

    def _make_middle_of_numeric_map_part(self, middle):
        if 0 < middle:
            return (middle, )
        else:
            return ()
