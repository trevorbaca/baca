from baca.rhythm.kaleids.SignalAffixedRestFilledTokens import SignalAffixedRestFilledTokens


class RestFilledTokens(SignalAffixedRestFilledTokens):
   '''Rest-filled tokens.

   See the test file for examples.
   '''

   def __init__(self):
      SignalAffixedRestFilledTokens.__init__(self, [ ], 1, [0], [ ], 1, [0])
