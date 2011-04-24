from abjad.tools import durtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import seqtools
from abjad.tools import tietools
from abjad.tools import tuplettools
from baca.rhythm.kaleids._RhythmicKaleid import _RhythmicKaleid
import types


class PartForcedPatternFilledTokens(_RhythmicKaleid):
   '''Part-forced pattern-filled tokens.
   '''

   def __init__(self, pattern, denominator, prolation_addenda = None, 
      lefts = None, middles = None, rights = None, left_lengths = None, right_lengths = None, 
      pattern_helper = None, prolation_addenda_helper = None,
      lefts_helper = None, middles_helper = None, rights_helper = None,
      left_lengths_helper = None, right_lengths_helper = None):
      _RhythmicKaleid.__init__(self)
      assert seqtools.all_are_integer_equivalent_numbers(pattern) 
      assert mathtools.is_positive_integer_equivalent_number(denominator)
      self._pattern = pattern
      self._denominator = denominator
      prolation_addenda = self._none_to_new_list(prolation_addenda)
      assert seqtools.all_are_nonnegative_integer_equivalent_numbers(prolation_addenda)
      self._prolation_addenda = prolation_addenda
      lefts = self._none_to_new_list(lefts)
      middles = self._none_to_new_list(middles)
      rights = self._none_to_new_list(rights)
      assert all([x in (-1, 0, 1) for x in lefts])
      assert all([x in (-1, 0, 1) for x in middles])
      assert all([x in (-1, 0, 1) for x in rights])
      self._lefts = lefts
      self._middles = middles
      self._rights = rights
      left_lengths = self._none_to_new_list(left_lengths)
      right_lengths = self._none_to_new_list(right_lengths)
      assert seqtools.all_are_nonnegative_integer_equivalent_numbers(left_lengths)
      assert seqtools.all_are_nonnegative_integer_equivalent_numbers(right_lengths)
      self._left_lengths = left_lengths
      self._right_lengths = right_lengths
      pattern_helper = self._none_to_trivial_helper(pattern_helper)
      assert isinstance(pattern_helper, (types.FunctionType, types.MethodType))
      self._pattern_helper = pattern_helper
      prolation_addenda_helper = self._none_to_trivial_helper(prolation_addenda_helper)
      assert isinstance(prolation_addenda_helper, (types.FunctionType, types.MethodType))
      self._prolation_addenda_helper = prolation_addenda_helper
      lefts_helper = self._none_to_trivial_helper(lefts_helper)
      middles_helper = self._none_to_trivial_helper(middles_helper)
      rights_helper = self._none_to_trivial_helper(rights_helper)
      assert isinstance(lefts_helper, (types.FunctionType, types.MethodType))
      assert isinstance(middles_helper, (types.FunctionType, types.MethodType))
      assert isinstance(rights_helper, (types.FunctionType, types.MethodType))
      self._lefts_helper = lefts_helper
      self._middles_helper = middles_helper
      self._rights_helper = rights_helper
      left_lengths_helper = self._none_to_trivial_helper(left_lengths_helper)
      right_lengths_helper = self._none_to_trivial_helper(right_lengths_helper)
      assert isinstance(left_lengths_helper, (types.FunctionType, types.MethodType))
      assert isinstance(right_lengths_helper, (types.FunctionType, types.MethodType))
      self._left_lengths_helper = left_lengths_helper
      self._right_lengths_helper = right_lengths_helper
      self._repr_signals.append(self._pattern)
      self._repr_signals.append(self._prolation_addenda)
      self._repr_signals.append(self._lefts)
      self._repr_signals.append(self._middles)
      self._repr_signals.append(self._rights)

   ## OVERLOADS ##

   def __call__(self, duration_tokens, seeds = None):
      duration_pairs, seeds = _RhythmicKaleid.__call__(self, duration_tokens, seeds)
      septuplet = self._prepare_input(seeds)
      pattern, prolation_addenda = septuplet[:2]
      pattern, lcd, prolation_addenda, duration_pairs = self._scale_input(
         pattern, prolation_addenda, duration_pairs)
      septuplet = (pattern, prolation_addenda) + septuplet[2:]
      #print septuplet
      numeric_map = self._make_numeric_map(duration_pairs, septuplet)
      leaf_lists = self._make_leaf_lists(numeric_map, lcd)
      if not prolation_addenda:
         return leaf_lists
      else:
         tuplets = self._make_tuplets(duration_pairs, leaf_lists)
         return tuplets

   ## PRIVATE METHODS ##

   def _make_leaf_lists(self, numeric_map, denominator):
      leaf_lists = [ ]
      for map_token in numeric_map:
         leaf_list = leaftools.make_leaves_from_note_value_signal(map_token, denominator)
         leaf_lists.append(leaf_list)
      tietools.remove_tie_spanners_from_components_in_expr(leaf_lists)
      return leaf_lists

   def _make_tuplets(self, duration_pairs, leaf_lists):
      assert len(duration_pairs) == len(leaf_lists)
      tuplets = [ ]
      for duration_pair, leaf_list in zip(duration_pairs, leaf_lists):
         tuplet = tuplettools.FixedDurationTuplet(duration_pair, leaf_list)
         tuplets.append(tuplet)
      return tuplets

   def _make_numeric_map(self, duration_pairs, septuplet):
      pattern, prolation_addenda, lefts, middles, rights, left_lengths, right_lengths = septuplet
      prolated_duration_pairs = self._make_prolated_duration_pairs(
         duration_pairs, prolation_addenda)
      #print duration_pairs, prolated_duration_pairs
      prolated_numerators = [pair[0] for pair in prolated_duration_pairs]
      map_tokens = seqtools.split_sequence_extended_to_weights_without_overhang(
         pattern, prolated_numerators)
      #print map_tokens
      quintuplet = (lefts, middles, rights, left_lengths, right_lengths)
      forced_map_tokens = self._force_token_parts(map_tokens, quintuplet)
      numeric_map = forced_map_tokens
      return numeric_map

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
      dummy_duration_pair = (1, self._denominator)
      duration_pairs = duration_pairs[:]
      duration_pairs.append(dummy_duration_pair)
      duration_pairs = durtools.duration_tokens_to_duration_pairs_with_least_common_denominator(
         duration_pairs)
      dummy_duration_pair = duration_pairs.pop( )
      lcd = dummy_duration_pair[1]
      pattern_multiplier = lcd / self._denominator
      pattern = seqtools.CyclicTuple([pattern_multiplier * n for n in pattern])
      prolation_addenda = seqtools.CyclicTuple([pattern_multiplier * n for n in prolation_addenda])
      return pattern, lcd, prolation_addenda, duration_pairs
