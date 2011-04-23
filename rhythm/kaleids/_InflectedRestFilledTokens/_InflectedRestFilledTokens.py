from abjad.tools import mathtools
from abjad.tools import seqtools
from baca.rhythm.kaleids._RhythmicKaleid import _RhythmicKaleid


class _InflectedRestFilledTokens(_RhythmicKaleid):
   '''Note- or rest-inflected rest-filled tokens.
   '''

   def __init__(self, written_duration_numerators, written_duration_denominator,
      written_duration_numerators_preprocessor = None):
      assert seqtools.all_are_integer_equivalent_numbers(written_duration_numerators)
      assert mathtools.is_positive_integer_equivalent_number(written_duration_denominator)
      self._written_duration_numerators = written_duration_numerators
      self._written_duration_denominator = written_duration_denominator
      preprocessor = self._handle_none_preprocessor(written_duration_numerators_preprocessor)
      self._written_duration_numerators_preprocessor = preprocessor

   ## OVERLOADS ##

   def __call__(self, duration_tokens, seeds = None):
      duration_pairs, seeds = _RhythmicKaleid.__call__(self, duration_tokens, seeds)
      leaf_lists = self._make_leaf_lists(duration_pairs, seeds)
      return leaf_lists
