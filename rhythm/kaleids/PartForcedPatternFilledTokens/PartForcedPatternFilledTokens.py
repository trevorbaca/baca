from abjad.tools import mathtools
from abjad.tools import seqtools
from baca.rhythm.kaleids._PartForcedObjectWithPatternFilledTokens import _PartForcedObjectWithPatternFilledTokens


class PartForcedPatternFilledTokens(_PartForcedObjectWithPatternFilledTokens):
   '''Part-forced pattern-filled tokens.
   '''

   ## PRIVATE METHODS ##

   def _force_token_parts(self, map_tokens, quintuplet):
      lefts, middles, rights, left_lengths, right_lengths = quintuplet
      lefts_index, rights_index = 0, 0
      forced_map_tokens = [ ]
      for token_index, map_token in enumerate(map_tokens):
         left_length = left_lengths[token_index]
         left = lefts[lefts_index:lefts_index+left_length]
         lefts_index += left_length
         right_length = right_lengths[token_index]
         right = rights[rights_index:rights_index+right_length]
         rights_index += right_length
         #print left, right, left_length, right_length
         available_left_length = len(map_token)
         left_length = min([left_length, available_left_length])
         available_right_length = len(map_token) - left_length
         right_length = min([right_length, available_right_length])
         middle_length = len(map_token) - left_length - right_length
         #print left_length, middle_length, right_length
         left = left[:left_length]
         middle = middle_length * [middles[token_index]]
         right = right[:right_length]
         #print left, middle, right
         left_part, middle_part, right_part = \
            seqtools.partition_sequence_once_by_counts_without_overhang(
            map_token, [left_length, middle_length, right_length])
         #print left_part, middle_part, right_part
         left_part = self._force_token_part(left_part, left)
         middle_part = self._force_token_part(middle_part, middle)
         right_part = self._force_token_part(right_part, right)
         #print left_part, middle_part, right_part
         forced_map_token = left_part + middle_part + right_part
         #print forced_map_token
         forced_map_tokens.append(forced_map_token)
      unforced_weights = [mathtools.weight(x) for x in map_tokens]
      forced_weights = [mathtools.weight(x) for x in forced_map_tokens]
      assert forced_weights == unforced_weights
      return forced_map_tokens
