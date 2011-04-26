from abjad.tools import durtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import seqtools
from baca.rhythm.kaleids._RhythmicKaleid import _RhythmicKaleid


class _SignalAffixedObjectWithFilledTokens(_RhythmicKaleid):
   '''Signal-affixed object with filled tokens.
   '''

   def __init__(self, prefix_signal, prefix_lengths, suffix_signal, suffix_lengths, denominator,
      prolation_addenda = None,
      prefix_signal_helper = None, prefix_lengths_helper = None,
      suffix_signal_helper = None, suffix_lengths_helper = None,
      prolation_addenda_helper = None):
      _RhythmicKaleid.__init__(self)
      assert seqtools.all_are_integer_equivalent_numbers(prefix_signal)
      assert seqtools.all_are_nonnegative_integer_equivalent_numbers(prefix_lengths)
      assert seqtools.all_are_integer_equivalent_numbers(suffix_signal)
      assert seqtools.all_are_nonnegative_integer_equivalent_numbers(suffix_lengths)
      prolation_addenda = self._none_to_new_list(prolation_addenda)
      assert seqtools.all_are_nonnegative_integer_equivalent_numbers(prolation_addenda)
      self._prefix_signal = prefix_signal
      self._prefix_lengths = prefix_lengths
      self._suffix_signal = suffix_signal
      self._suffix_lengths = suffix_lengths
      self._prolation_addenda = prolation_addenda
      assert mathtools.is_positive_integer_equivalent_number(denominator)
      self._denominator = denominator
      self._repr_signals.append(prefix_signal)
      self._repr_signals.append(suffix_signal)
      self._prefix_signal_helper = self._none_to_trivial_helper(prefix_signal_helper)
      self._prefix_lengths_helper = self._none_to_trivial_helper(prefix_lengths_helper)
      self._suffix_signal_helper = self._none_to_trivial_helper(suffix_signal_helper)
      self._suffix_lengths_helper = self._none_to_trivial_helper(suffix_lengths_helper)
      self._prolation_addenda_helper = self._none_to_trivial_helper(prolation_addenda_helper)

   ## OVERLOADS ##

   def __call__(self, duration_tokens, seeds = None):
      duration_pairs, seeds = _RhythmicKaleid.__call__(self, duration_tokens, seeds)
      prefix_signal, suffix_signal, lcd, prolation_addenda, duration_pairs = \
         self._scale_signal_denominator_and_duration_pairs(duration_pairs, seeds)
      prefix_lengths = self._prefix_lengths_helper(self._prefix_lengths, seeds)
      suffix_lengths = self._suffix_lengths_helper(self._suffix_lengths, seeds)
      numeric_map = self._make_numeric_map(duration_pairs, 
         prefix_signal, prefix_lengths, suffix_signal, suffix_lengths, prolation_addenda)
      leaf_lists = self._numeric_map_and_denominator_to_leaf_lists(numeric_map, lcd)
      if not prolation_addenda:
         return leaf_lists
      else:
         tuplets = self._make_tuplets(duration_pairs, leaf_lists)
         return tuplets

   ## PRIVATE METHODS ##

   def _make_numeric_map_part(self, numerator, prefix, suffix, is_note_filled = True):
      prefix_weight = mathtools.weight(prefix)
      suffix_weight = mathtools.weight(suffix)
      middle = numerator - prefix_weight - suffix_weight
      if numerator <prefix_weight:
         weights = [numerator]
         prefix = seqtools.split_sequence_once_by_weights_without_overhang(prefix, weights)[0]
      middle = self._make_middle_of_numeric_map_part(middle)
      suffix_space = numerator - prefix_weight
      if suffix_space <= 0:
         suffix = ( )
      elif suffix_space < suffix_weight:
         weights = [suffix_space]
         suffix = seqtools.split_sequence_once_by_weights_without_overhang(suffix, weights)[0]
      numeric_map_part = prefix + middle + suffix
      return numeric_map_part

   def _numeric_map_and_denominator_to_leaf_lists(self, numeric_map, lcd):
      leaf_lists = [ ]
      for numeric_map_part in numeric_map:
         leaf_list = leaftools.make_leaves_from_note_value_signal(numeric_map_part, lcd)
         leaf_lists.append(leaf_list)
      return leaf_lists

   def _scale_signal_denominator_and_duration_pairs(self, duration_pairs, seeds):
      prefix_signal = self._prefix_signal_helper(self._prefix_signal, seeds)
      suffix_signal = self._suffix_signal_helper(self._suffix_signal, seeds)
      prolation_addenda = self._prolation_addenda_helper(self._prolation_addenda, seeds)
      duration_pairs = duration_pairs[:]
      dummy_duration_pair = (1, self._denominator)
      duration_pairs.append(dummy_duration_pair)
      duration_pairs = durtools.duration_tokens_to_duration_pairs_with_least_common_denominator(
         duration_pairs)
      dummy_duration_pair = duration_pairs.pop( )
      lcd = dummy_duration_pair[1]
      multiplier = lcd / self._denominator
      prefix_signal = [multiplier * x for x in prefix_signal]
      suffix_signal = [multiplier * x for x in suffix_signal]
      prolation_addenda = [multiplier * x for x in prolation_addenda]
      return prefix_signal, suffix_signal, lcd, prolation_addenda, duration_pairs
