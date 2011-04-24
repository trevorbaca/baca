from abjad.tools import durtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import seqtools
from baca.rhythm.kaleids._SignalAffixer import _SignalAffixer


class _SignalAffixedFilledTokens(_SignalAffixer):
   '''Signal-affixed rest-filled tokens.
   '''

   ## PRIVATE METHODS ##

   def _make_numeric_map(self,
      duration_pairs, prefix_signal, prefix_lengths, suffix_signal, suffix_lengths):
      numeric_map, prefix_signal_index, suffix_signal_index = [ ], 0, 0
      prefix_signal = seqtools.CyclicTuple(prefix_signal)
      suffix_signal = seqtools.CyclicTuple(suffix_signal)
      prefix_lengths = seqtools.CyclicTuple(prefix_lengths)
      suffix_lengths = seqtools.CyclicTuple(suffix_lengths)
      for pair_index, duration_pair in enumerate(duration_pairs):
         prefix_length, suffix_length = prefix_lengths[pair_index], suffix_lengths[pair_index]
         prefix = prefix_signal[prefix_signal_index:prefix_signal_index+prefix_length]
         suffix = suffix_signal[suffix_signal_index:suffix_signal_index+suffix_length]
         prefix_signal_index += prefix_length
         suffix_signal_index += suffix_length
         numeric_map_part = self._make_numeric_map_part(duration_pair[0], prefix, suffix)
         numeric_map.append(numeric_map_part)
      return numeric_map
