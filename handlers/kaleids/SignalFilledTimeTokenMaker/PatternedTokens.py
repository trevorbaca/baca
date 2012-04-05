from handlers.kaleids.TokenBurnishedSignalFilledTimeTokenMaker import TokenBurnishedSignalFilledTimeTokenMaker


class SignalFilledTimeTokenMaker(TokenBurnishedSignalFilledTimeTokenMaker):
    '''Pattern-filled tokens.
    '''

    def __init__(self, pattern, denominator, prolation_addenda=None, secondary_divisions=None,
        pattern_helper=None, prolation_addenda_helper=None, secondary_divisions_helper=None):
        lefts, middles, rights = [0], [0], [0]
        left_lengths, right_lengths = [0], [0]
        TokenBurnishedSignalFilledTimeTokenMaker.__init__(self, pattern, denominator, prolation_addenda,
            lefts, middles, rights, left_lengths, right_lengths, secondary_divisions,
            pattern_helper=pattern_helper, prolation_addenda_helper=prolation_addenda_helper,
            secondary_divisions_helper=secondary_divisions_helper)

    ### CLASS ATTRIBUTES ###

    kwargs = (
        'prolation_addenda',
        'secondary_divisions',
        #'pattern_helper',
        #'prolation_addenda_helper',
        #'secondary_divisions_helper',
        )
