from baca.rhythm.kaleids._NoteInflectedRestFilledTokens import _NoteInflectedRestFilledTokens


class NoteInitiatedRestFilledTokens(_NoteInflectedRestFilledTokens):
   '''Note-initiated rest-filled tokens.

   See the test file for examples.
   '''

   ## PRIVATE METHODS ##

   def _make_numeric_input(self, scaled_duration_pairs, scaled_numerators):
      numeric_input = [ ]
      for pair_index, (pair_numerator, pair_denominator) in enumerate(scaled_duration_pairs): 
         scaled_numerator = scaled_numerators[pair_index]
         if pair_numerator <= scaled_numerator:
            part = [pair_numerator]
         else:
            part = [scaled_numerator, -abs(pair_numerator - scaled_numerator)]
         numeric_input.append(part)
      return numeric_input
