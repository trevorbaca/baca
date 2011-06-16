from baca.rhythm.kaleids._SignalAffixedFilledTokens import _SignalAffixedFilledTokens


class SignalAffixedRestFilledTokens(_SignalAffixedFilledTokens):
    '''Signal-affixed rest-filled tokens.
    '''

    ## PRIVATE METHODS ##

    def _make_middle_of_numeric_map_part(self, middle):
        if 0 < middle:
            return (-abs(middle), )
        else:
            return ()
