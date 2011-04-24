from baca.rhythm.kaleids.SignalAffixedNoteFilledTokens import SignalAffixedNoteFilledTokens


class NoteFilledTokens(SignalAffixedNoteFilledTokens):
   '''Note-filled tokens.

   See the test file for examples.
   '''

   def __init__(self):
      SignalAffixedNoteFilledTokens.__init__(self, [ ], 1, [0], [ ], 1, [0])
