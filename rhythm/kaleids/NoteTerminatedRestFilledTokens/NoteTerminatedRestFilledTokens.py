from abjad.tools import mathtools
from baca.rhythm.kaleids._NoteInflectedRestFilledTokens import _NoteInflectedRestFilledTokens


class NoteTerminatedRestFilledTokens(_NoteInflectedRestFilledTokens):
   '''Note-initiated rest-filled tokens.

   See the test file for examples.
   '''

   ## PRIVATE METHODS ##
      
   def _make_numeric_input(self, scaled_duration_pairs, scaled_numerators):
      numeric_input = [ ]
      for pair_index, (pair_numerator, pair_denominator) in enumerate(scaled_duration_pairs):
         scaled_numerator = scaled_numerators[pair_index]
         if pair_numerator <= scaled_numerator:
            part = list(mathtools.partition_integer_into_canonic_parts(
               pair_numerator, direction = 'little-endian'))
         else:
            part = [-abs(pair_numerator - scaled_numerator)]
            termination = mathtools.partition_integer_into_canonic_parts(
               scaled_numerator, direction = 'little-endian')
            part.extend(termination)
         numeric_input.append(part)
      return numeric_input
