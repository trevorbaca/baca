from abjad.tools import durtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import seqtools
from baca.rhythm.kaleids._SignalAffixer import _SignalAffixer


class SignalAffixedChunksWithRestFilledTokens(_SignalAffixer):
   '''Signal-affixed chunks with rest-filled tokens.
   '''

   ## PRIVATE METHODS ##

   def _make_numeric_map(self,
      duration_pairs, prefix_signal, prefix_lengths, suffix_signal, suffix_lengths):
      numeric_map, prefix_signal_index, suffix_signal_index = [ ], 0, 0
      prefix_signal = seqtools.CyclicTuple(prefix_signal)
      suffix_signal = seqtools.CyclicTuple(suffix_signal)
      prefix_length, suffix_length = prefix_lengths[0], suffix_lengths[0]
      prefix = prefix_signal[prefix_signal_index:prefix_signal_index+prefix_length]
      suffix = suffix_signal[suffix_signal_index:suffix_signal_index+suffix_length]
      if len(duration_pairs) == 1:
         numeric_map_part = self._make_numeric_map_part(duration_pairs[0][0], prefix, suffix)
         numeric_map.append(numeric_map_part)
      else:
         numeric_map_part = self._make_numeric_map_part(duration_pairs[0][0], prefix, ( ))
         numeric_map.append(numeric_map_part)
         for duration_pair in duration_pairs[1:-1]:
            numeric_map_part = self._make_numeric_map_part(duration_pair[0], ( ), ( ))
            numeric_map.append(numeric_map_part)
         numeric_map_part = self._make_numeric_map_part(duration_pairs[-1][0], ( ), suffix)
         numeric_map.append(numeric_map_part)
      return numeric_map
