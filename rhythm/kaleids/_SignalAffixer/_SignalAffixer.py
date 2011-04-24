from abjad.tools import durtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import seqtools
from baca.rhythm.kaleids._RhythmicKaleid import _RhythmicKaleid


class _SignalAffixer(_RhythmicKaleid):
   '''Signal-affixer.
   '''

   def __init__(self, prefix_signal, prefix_denominator, prefix_lengths,
      suffix_signal, suffix_denominator, suffix_lengths,
      prefix_signal_helper = None, prefix_lengths_helper = None,
      suffix_signal_helper = None, suffix_lengths_helper = None):
      _RhythmicKaleid.__init__(self)
      assert seqtools.all_are_integer_equivalent_numbers(prefix_signal)
      assert mathtools.is_positive_integer(prefix_denominator)
      assert seqtools.all_are_nonnegative_integer_equivalent_numbers(prefix_lengths)
      assert seqtools.all_are_integer_equivalent_numbers(suffix_signal)
      assert mathtools.is_positive_integer(suffix_denominator)
      assert seqtools.all_are_nonnegative_integer_equivalent_numbers(suffix_lengths)
      self._prefix_signal = prefix_signal
      self._prefix_denominator = prefix_denominator
      self._prefix_lengths = prefix_lengths
      self._suffix_signal = suffix_signal
      self._suffix_denominator = suffix_denominator
      self._suffix_lengths = suffix_lengths
      self._repr_signals.append(prefix_signal)
      self._repr_signals.append(prefix_lengths)
      self._repr_signals.append(suffix_signal)
      self._repr_signals.append(suffix_lengths)
      self._prefix_signal_helper = self._handle_none_preprocessor(prefix_signal_helper)
      self._prefix_lengths_helper = self._handle_none_preprocessor(prefix_lengths_helper)
      self._suffix_signal_helper = self._handle_none_preprocessor(suffix_signal_helper)
      self._suffix_lengths_helper = self._handle_none_preprocessor(suffix_lengths_helper)

   ## OVERLOADS ##

   def __call__(self, duration_tokens, seeds = None):
      return _RhythmicKaleid.__call__(self, duration_tokens, seeds)

   ## PRIVATE METHODS ##

   def _numeric_map_and_denominator_to_leaf_lists(self, numeric_map, denominator):
      leaf_lists = [ ]
      for numeric_map_part in numeric_map:
         leaf_list = leaftools.make_leaves_from_note_value_signal(numeric_map_part, denominator)
         leaf_lists.append(leaf_list)
      return leaf_lists

   def _scale_signal_denominator_and_duration_pairs(self, duration_pairs, seeds):
      prefix_signal = self._prefix_signal_helper(self._prefix_signal, seeds)
      suffix_signal = self._suffix_signal_helper(self._suffix_signal, seeds)
      duration_pairs = duration_pairs[:]
      dummy_prefix_duration_pair = (1, self._prefix_denominator)
      dummy_suffix_duration_pair = (1, self._suffix_denominator)
      duration_pairs.append(dummy_prefix_duration_pair)
      duration_pairs.append(dummy_suffix_duration_pair)
      duration_pairs = durtools.duration_tokens_to_duration_pairs_with_least_common_denominator(
         duration_pairs)
      dummy_suffix_duration_pair = duration_pairs.pop( )
      dummy_prefix_duration_pair = duration_pairs.pop( )
      denominator = duration_pairs[0][1]
      prefix_signal_multiplier = denominator / self._prefix_denominator
      prefix_signal = [prefix_signal_multiplier * x for x in prefix_signal]
      suffix_signal_multiplier = denominator / self._suffix_denominator
      suffix_signal = [suffix_signal_multiplier * x for x in suffix_signal]
      return prefix_signal, suffix_signal, denominator, duration_pairs
