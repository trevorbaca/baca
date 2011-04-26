from baca.rhythm.kaleids.PartForcedPatternedTokens import PartForcedPatternedTokens


class PatternedTokens(PartForcedPatternedTokens):
   '''Pattern-filled tokens.
   '''

   def __init__(self, pattern, denominator, prolation_addenda = None,
      pattern_helper = None, prolation_addenda_helper = None):
      lefts, middles, rights = [0], [0], [0]
      left_lengths, right_lengths = [0], [0]
      PartForcedPatternedTokens.__init__(self, pattern, denominator, prolation_addenda,
         lefts, middles, rights, left_lengths, right_lengths, 
         pattern_helper, prolation_addenda_helper)
