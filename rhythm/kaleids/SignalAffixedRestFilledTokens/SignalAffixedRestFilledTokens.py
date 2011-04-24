from abjad.tools import durtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import seqtools
from baca.rhythm.kaleids._SignalAffixer import _SignalAffixer


class SignalAffixedRestFilledTokens(_SignalAffixer):
   '''Signal-affixed rest-filled tokens.
   '''

   ## OVERLOADS ##

   def __call__(self, duration_tokens, seeds = None):
      duration_pairs, seeds = _SignalAffixer.__call__(self, duration_tokens, seeds)
      seeds = self._handle_none_seeds(seeds)
      prefix_signal, suffix_signal, denominator, duration_pairs = \
         self._scale_signal_denominator_and_duration_pairs(duration_pairs, seeds)
      prefix_lengths = self._prefix_lengths_helper(self._prefix_lengths, seeds)
      suffix_lengths = self._suffix_lengths_helper(self._suffix_lengths, seeds)
      numeric_map = self._make_numeric_map(
         duration_pairs, prefix_signal, prefix_lengths, suffix_signal, suffix_lengths)
      leaf_lists = self._numeric_map_and_denominator_to_leaf_lists(numeric_map, denominator)
      return leaf_lists

   ## PRIVATE METHODS ##

   def _make_numeric_map(self, 
      duration_pairs, prefix_signal, prefix_lengths, suffix_signal, suffix_lengths):
      numeric_map, prefix_signal_index, suffix_signal_index = [ ], 0, 0
      prefix_signal = seqtools.CyclicTuple(prefix_signal)
      suffix_signal = seqtools.CyclicTuple(suffix_signal)
      prefix_lengths = seqtools.CyclicTuple(prefix_lengths)
      suffix_lengths = seqtools.CyclicTuple(suffix_lengths)
      for pair_index, duration_pair in enumerate(duration_pairs):
         numeric_map_part = [ ]
         prefix_length = prefix_lengths[pair_index]
         suffix_length = suffix_lengths[pair_index]
         prefix = prefix_signal[prefix_signal_index:prefix_signal_index+prefix_length]
         suffix = suffix_signal[suffix_signal_index:suffix_signal_index+suffix_length]
         prefix_signal_index += prefix_length
         suffix_signal_index += suffix_length
         numerator = duration_pair[0]
         prefix_weight = mathtools.weight(prefix)
         suffix_weight = mathtools.weight(suffix)
         middle = numerator - prefix_weight - suffix_weight
         if numerator <prefix_weight:
            weights = [numerator]
            prefix = seqtools.split_sequence_once_by_weights_without_overhang(prefix, weights)[0]
         if 0 < middle:
            middle = (-abs(middle), )
         else:
            middle = ( )
         suffix_space = numerator - prefix_weight
         if suffix_space <= 0:
            suffix = ( )
         elif suffix_space < suffix_weight:
            weights = [suffix_space]
            suffix = seqtools.split_sequence_once_by_weights_without_overhang(suffix, weights)[0]
         numeric_map_part = prefix + middle + suffix
         numeric_map.append(numeric_map_part)
      return numeric_map
