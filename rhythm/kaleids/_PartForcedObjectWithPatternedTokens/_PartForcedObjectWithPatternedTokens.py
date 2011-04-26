from abjad.tools import durtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import seqtools
from baca.rhythm.kaleids._RhythmicKaleid import _RhythmicKaleid
import types


class _PartForcedObjectWithPatternedTokens(_RhythmicKaleid):
   '''Part-forced object with patterned tokens.
   '''

   def __init__(self, pattern, denominator, prolation_addenda = None,
      lefts = None, middles = None, rights = None, left_lengths = None, right_lengths = None,
      secondary_divisions = None,
      pattern_helper = None, prolation_addenda_helper = None,
      lefts_helper = None, middles_helper = None, rights_helper = None,
      left_lengths_helper = None, right_lengths_helper = None, secondary_divisions_helper = None):
      _RhythmicKaleid.__init__(self)
      prolation_addenda = self._none_to_new_list(prolation_addenda)
      lefts = self._none_to_new_list(lefts)
      middles = self._none_to_new_list(middles)
      rights = self._none_to_new_list(rights)
      left_lengths = self._none_to_new_list(left_lengths)
      right_lengths = self._none_to_new_list(right_lengths)
      secondary_divisions = self._none_to_new_list(secondary_divisions)
      pattern_helper = self._none_to_trivial_helper(pattern_helper)
      prolation_addenda_helper = self._none_to_trivial_helper(prolation_addenda_helper)
      lefts_helper = self._none_to_trivial_helper(lefts_helper)
      middles_helper = self._none_to_trivial_helper(middles_helper)
      rights_helper = self._none_to_trivial_helper(rights_helper)
      left_lengths_helper = self._none_to_trivial_helper(left_lengths_helper)
      right_lengths_helper = self._none_to_trivial_helper(right_lengths_helper)
      secondary_divisions_helper = self._none_to_trivial_helper(secondary_divisions_helper)
      assert seqtools.all_are_integer_equivalent_numbers(pattern)
      assert mathtools.is_positive_integer_equivalent_number(denominator)
      assert seqtools.all_are_nonnegative_integer_equivalent_numbers(prolation_addenda)
      assert all([x in (-1, 0, 1) for x in lefts])
      assert all([x in (-1, 0, 1) for x in middles])
      assert all([x in (-1, 0, 1) for x in rights])
      assert seqtools.all_are_nonnegative_integer_equivalent_numbers(left_lengths)
      assert seqtools.all_are_nonnegative_integer_equivalent_numbers(right_lengths)
      assert seqtools.all_are_nonnegative_integer_equivalent_numbers(secondary_divisions)
      assert isinstance(pattern_helper, (types.FunctionType, types.MethodType))
      assert isinstance(prolation_addenda_helper, (types.FunctionType, types.MethodType))
      assert isinstance(lefts_helper, (types.FunctionType, types.MethodType))
      assert isinstance(middles_helper, (types.FunctionType, types.MethodType))
      assert isinstance(rights_helper, (types.FunctionType, types.MethodType))
      assert isinstance(left_lengths_helper, (types.FunctionType, types.MethodType))
      assert isinstance(right_lengths_helper, (types.FunctionType, types.MethodType))
      self._pattern = pattern
      self._denominator = denominator
      self._prolation_addenda = prolation_addenda
      self._lefts = lefts
      self._middles = middles
      self._rights = rights
      self._left_lengths = left_lengths
      self._right_lengths = right_lengths
      self._secondary_divisions = secondary_divisions
      self._pattern_helper = pattern_helper
      self._prolation_addenda_helper = prolation_addenda_helper
      self._lefts_helper = lefts_helper
      self._middles_helper = middles_helper
      self._rights_helper = rights_helper
      self._left_lengths_helper = left_lengths_helper
      self._right_lengths_helper = right_lengths_helper
      self._secondary_divisions_helper = secondary_divisions_helper
      self._repr_signals.append(self._pattern)
      self._repr_signals.append(self._prolation_addenda)
      self._repr_signals.append(self._lefts)
      self._repr_signals.append(self._middles)
      self._repr_signals.append(self._rights)
      self._repr_signals.append(self._secondary_divisions)

   ## OVERLOADS ##

   def __call__(self, duration_tokens, seeds = None):
      duration_pairs, seeds = _RhythmicKaleid.__call__(self, duration_tokens, seeds)
      septuplet = self._prepare_input(seeds)
      pattern, prolation_addenda = septuplet[:2]
      pattern, lcd, prolation_addenda, duration_pairs = self._scale_input(
         pattern, prolation_addenda, duration_pairs)
      septuplet = (pattern, prolation_addenda) + septuplet[2:]
      numeric_map = self._make_numeric_map(duration_pairs, septuplet)
      leaf_lists = self._make_leaf_lists(numeric_map, lcd)
      if not prolation_addenda:
         return leaf_lists
      else:
         tuplets = self._make_tuplets(duration_pairs, leaf_lists)
         return tuplets

   ## PRIVATE METHODS ##

   def _force_token_part(self, token_part, indicator):
      assert len(token_part) == len(indicator)
      new_token_part = [ ]
      for number, i in zip(token_part, indicator):
         if i == -1:
            new_token_part.append(-abs(number))
         elif i == 0:
            new_token_part.append(number)
         elif i == 1:
            new_token_part.append(abs(number))
         else:
            raise ValueError
      new_token_part = type(token_part)(new_token_part)
      return new_token_part

   def _make_leaf_lists(self, numeric_map, denominator):
      leaf_lists = [ ]
      for map_token in numeric_map:
         leaf_list = leaftools.make_leaves_from_note_value_signal(map_token, denominator)
         leaf_lists.append(leaf_list)
      return leaf_lists

   def _make_numeric_map(self, duration_pairs, septuplet):
      pattern, prolation_addenda, lefts, middles, rights, left_lengths, right_lengths = septuplet
      prolated_duration_pairs = self._make_prolated_duration_pairs(
         duration_pairs, prolation_addenda)
      prolated_numerators = [pair[0] for pair in prolated_duration_pairs]
      map_tokens = seqtools.split_sequence_extended_to_weights_without_overhang(
         pattern, prolated_numerators)
      quintuplet = (lefts, middles, rights, left_lengths, right_lengths)
      forced_map_tokens = self._force_token_parts(map_tokens, quintuplet)
      numeric_map = forced_map_tokens
      return numeric_map

   def _make_prolated_duration_pairs(self, duration_pairs, prolation_addenda):
      prolated_duration_pairs = [ ]
      for i, duration_pair in enumerate(duration_pairs):
         if not prolation_addenda:
            prolated_duration_pairs.append(duration_pair)
         else:
            prolation_addendum = prolation_addenda[i]
            prolation_addendum %= duration_pair[0]
            prolated_duration_pair = (duration_pair[0] + prolation_addendum, duration_pair[1])
            prolated_duration_pairs.append(prolated_duration_pair)
      return prolated_duration_pairs

   def _prepare_input(self, seeds):
      pattern = seqtools.CyclicTuple(self._pattern_helper(self._pattern, seeds))
      prolation_addenda = self._prolation_addenda_helper(self._prolation_addenda, seeds)
      prolation_addenda = seqtools.CyclicTuple(prolation_addenda)
      lefts = seqtools.CyclicTuple(self._lefts_helper(self._lefts, seeds))
      middles = seqtools.CyclicTuple(self._middles_helper(self._middles, seeds))
      rights = seqtools.CyclicTuple(self._rights_helper(self._rights, seeds))
      left_lengths = seqtools.CyclicTuple(self._left_lengths_helper(self._left_lengths, seeds))
      right_lengths = seqtools.CyclicTuple(self._right_lengths_helper(self._right_lengths, seeds))
      return pattern, prolation_addenda, lefts, middles, rights, left_lengths, right_lengths

   def _scale_input(self, pattern, prolation_addenda, duration_pairs):
      duration_pairs = duration_pairs[:]
      dummy_duration_pair = (1, self._denominator)
      duration_pairs.append(dummy_duration_pair)
      duration_pairs = durtools.duration_tokens_to_duration_pairs_with_least_common_denominator(
         duration_pairs)
      dummy_duration_pair = duration_pairs.pop( )
      lcd = dummy_duration_pair[1]
      multiplier = lcd / self._denominator
      pattern = seqtools.CyclicTuple([multiplier * x for x in pattern])
      prolation_addenda = seqtools.CyclicTuple([multiplier * x for x in prolation_addenda])
      return pattern, lcd, prolation_addenda, duration_pairs
