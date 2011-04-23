from abjad.tools import mathtools
from abjad.tools import seqtools
from baca.rhythm.kaleids._RhythmicKaleid import _RhythmicKaleid


class _NoteInflectedRestFilledTokens(_RhythmicKaleid):
   '''Note- or rest-inflected rest-filled tokens.
   '''

   def _make_leaf_lists(duration_pairs, seeds):
      scaled_duration_pairs, scaled_numerators, scaled_denominator = self._scale_input(
         duration_pairs, seeds)
      numeric_input = self._make_numeric_input(scaled_duration_pairs, scaled_numerators)
      leaf_lists = self._make_leaf_lists_from_numeric_input(numeric_input, scaled_denominator)
      return leaf_lists

   def _make_leaf_lists_from_numeric_input(self, numeric_input, scaled_denominator):
      leaf_lists = [ ]
      for part in numeric_input:
         leaf_list = leaftools.make_leaves_from_note_value_signal(part, scaled_denominator)
         leaf_lists.append(leaf_list)
      return leaf_lists

   def _scale_input(self, duration_pairs, seeds):
      dummy_duration_pair = (1, self._written_duration_denominator)
      duration_pairs = duration_pairs[:]
      duration_pairs.append(dummy_duration_pair)
      duration_pairs = durtools.duration_tokens_to_duration_pairs_with_least_common_denominator(
         duration_pairs)
      scaled_duration_pairs = duration_pairs[0:-1]
      dummy_duration_pair = duration_pairs.pop( )
      scaled_denominator = dummy_duration_pair[1]
      numerator_multiplier = scaled_denominator / self._written_duration_denominator
      numerators = self._written_duration_numerators_preprocessor(
         self._written_duration_numerators, seeds)
      scaled_numerators = [numerator_multiplier * numerator for numerator in numerators]
      scaled_numerators = seqtools.CyclicTuple(scaled_numerators)
      return scaled_duration_pairs, scaled_numerators, scaled_denominator
