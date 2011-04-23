from abjad.tools import durtools
from abjad.tools import mathtools
from abjad.tools import seqtools
from baca.rhythm.kaleids._RhythmicKaleid import _RhythmicKaleid


class SignalAffixedRestFilledTokens(_RhythmicKaleid):
   '''Signal-affixed rest-filled tokens.
   '''

   def __init__(self, signal, denominator, prefix_lengths, suffix_lengths,
      signal_helper = None, prefix_helper = None, suffix_helper = None):
      _RhythmicKaleid.__init__(self)
      assert seqtools.all_are_integer_equivalent_numbers(signal)
      assert mathtools.is_positive_integer(denominator)
      assert seqtools.all_are_nonnegative_integer_equivalent_numbers(prefix_lengths)
      assert seqtools.all_are_nonnegative_integer_equivalent_numbers(suffix_lengths)
      self._signal = signal
      self._denominator = denominator
      self._prefix_lengths = prefix_lengths
      self._suffix_lengths = suffix_lengths
      self._repr_signals.append(signal)
      self._repr_signals.append(prefix_lengths)
      self._repr_signals.append(suffix_lengths)
      self._signal_helper = self._handle_none_preprocessor(signal_helper)
      self._prefix_helper = self._handle_none_preprocessor(prefix_helper)
      self._suffix_helper = self._handle_none_preprocessor(suffix_helper)

   ## OVERLOADS ##

   def __call__(self, duration_tokens, seeds = None):
      duration_pairs, seeds = _RhythmicKaleid.__call__(self, duration_tokens, seeds)
      seeds = self._handle_none_seeds(seeds)
      signal, denominator, duration_pairs = self._scale_signal_denominator_and_duration_pairs(
         duration_pairs, seeds)
      print signal, denominator, duration_pairs
      prefix_lengths = self._prefix_helper(self._prefix_lengths, seeds)
      suffix_lengths = self._suffix_helper(self._suffix_lengths, seeds)
      numeric_map = self._make_numeric_map(duration_pairs, signal, prefix_lengths, suffix_lengths)
      leaf_lists = self._numeric_map_and_denominator_to_leaf_lists(numeric_map, denominator)
      return leaf_lists

   ## PRIVATE METHODS ##

   ## TODO: RESUME WORK HERE ON THIS METHOD
   def _make_numeric_map(self, duration_pairs, signal, prefix_lengths, suffix_lengths):
      numeric_map = [ ]
      signal_index = 0
      signal = seqtools.CyclicTuple(signal)
      prefix_lengths = seqtools.CyclicTuple(prefix_lengths)
      suffix_lengths = seqtools.CyclicTuple(suffix_lengths)
      for pair_index, duration_pair in enumerate(duration_pairs):
         numeric_map_part = [ ]
         prefix_length = prefix_lengths[pair_index]
         suffix_length = suffix_lengths[pair_index]
      
   def _numeric_map_and_denominator_to_leaf_lists(self, numeric_map, denominator):
      pass

   def _scale_signal_denominator_and_duration_pairs(self, duration_pairs, seeds):
      signal = self._signal_helper(self._signal, seeds)
      duration_pairs = duration_pairs[:]
      dummy_duration_pair = (1, self._denominator)
      duration_pairs.append(dummy_duration_pair)
      duration_pairs = durtools.duration_tokens_to_duration_pairs_with_least_common_denominator(
         duration_pairs)
      dummy_duration_pair = duration_pairs.pop( )
      denominator = dummy_duration_pair[1]
      signal_multiplier = denominator / self._denominator
      signal = [signal_multiplier * x for x in signal]
      return signal, denominator, duration_pairs
