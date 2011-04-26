from baca.rhythm.kaleids.SignalAffixedRestFilledTokens import SignalAffixedRestFilledTokens


class RestFilledTokens(SignalAffixedRestFilledTokens):
   '''Rest-filled tokens.

   See the test file for examples.
   '''

   def __init__(self):
      #SignalAffixedRestFilledTokens.__init__(self, [ ], 1, [0], [ ], 1, [0])
      SignalAffixedRestFilledTokens.__init__(self, [ ], [0], [ ], [0], 1)

   ## OVERLOADS ##

   def __repr__(self):
      return '%s( )' % self.__class__.__name__
