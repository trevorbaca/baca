from baca.rhythm.kaleids._SignalAffixedObjectWithFilledTokens import _SignalAffixedObjectWithFilledTokens


class _SignalAffixedFilledTokens(_SignalAffixedObjectWithFilledTokens):
   '''Signal-affixed rest-filled tokens.
   '''

   ## PRIVATE METHODS ##

   def _make_numeric_map(self, duration_pairs, 
      prefix_signal, prefix_lengths, suffix_signal, suffix_lengths, prolation_addenda):
      numeric_map, prefix_signal_index, suffix_signal_index = [ ], 0, 0
      for pair_index, duration_pair in enumerate(duration_pairs):
         prefix_length, suffix_length = prefix_lengths[pair_index], suffix_lengths[pair_index]
         prefix = prefix_signal[prefix_signal_index:prefix_signal_index+prefix_length]
         suffix = suffix_signal[suffix_signal_index:suffix_signal_index+suffix_length]
         prefix_signal_index += prefix_length
         suffix_signal_index += suffix_length
         prolation_addendum = prolation_addenda[pair_index]
         numerator = duration_pair[0] + (prolation_addendum % duration_pair[0])
         numeric_map_part = self._make_numeric_map_part(numerator, prefix, suffix)
         numeric_map.append(numeric_map_part)
      return numeric_map
