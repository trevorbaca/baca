from baca.rhythm.kaleids.PartForcedPatternFilledTokens import PartForcedPatternFilledTokens


class PatternFilledTokens(PartForcedPatternFilledTokens):
   '''Pattern-filled tokens.
   '''

   def __init__(self, pattern, denominator, prolation_addenda = None,
      pattern_helper = None, prolation_addenda_helper = None):
      lefts, middles, rights = [0], [0], [0]
      left_lengths, right_lengths = [0], [0]
      PartForcedPatternFilledTokens.__init__(self, pattern, denominator, prolation_addenda,
         lefts, middles, rights, left_lengths, right_lengths, 
         pattern_helper, prolation_addenda_helper)
