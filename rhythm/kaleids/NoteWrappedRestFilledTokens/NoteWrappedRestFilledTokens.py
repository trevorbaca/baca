from abjad.tools import mathtools
from baca.rhythm.kaleids._NoteInflectedRestFilledTokens import _NoteInflectedRestFilledTokens


class NoteWrappedRestFilledTokens(_NoteInflectedRestFilledTokens):
   '''Note-initiated rest-filled tokens.

   See the test file for examples.
   '''

   ## PRIVATE METHODS ##
      
   def _make_numeric_input(self, scaled_duration_pairs, scaled_numerators):
      numeric_input = [ ]
      for pair_index, (pair_numerator, pair_denominator) in enumerate(scaled_duration_pairs):
         initiation = scaled_numerators[2 * pair_index]
         termination = scaled_numerators[2 * pair_index + 1]
         ## initiation is really big
         if pair_numerator <= initiation:
            part = list(mathtools.partition_integer_into_canonic_parts(
               pair_numerator, direction = 'little-endian'))
         else:
            part = [initiation]
            space_for_termination = pair_numerator - initiation
            if space_for_termination <= termination:
               termination = mathtools.partition_integer_into_canonic_parts(
                  space_for_termination, direction = 'little-endian')
               part.extend(termination)
            else:
               middle = pair_numerator - initiation - termination
               middle = -abs(middle)
               part.append(middle)
               termination = mathtools.partition_integer_into_canonic_parts(
                  termination, direction = 'little-endian')
               part.extend(termination)
         numeric_input.append(part)
      return numeric_input
