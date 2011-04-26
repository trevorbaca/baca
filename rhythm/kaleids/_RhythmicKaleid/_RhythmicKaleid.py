from abjad.components import Note
from abjad.components import Rest
from abjad.tools import durtools
from abjad.tools import seqtools
from abjad.tools import tuplettools
import copy


class _RhythmicKaleid(object):

   def __init__(self):
      self._repr_signals = [ ]

   ## OVERLOADS ##

   def __call__(self, duration_tokens, seeds = None):
      duration_pairs = durtools.duration_tokens_to_duration_pairs(duration_tokens)
      seeds = self._none_to_new_list(seeds)
      return duration_pairs, seeds

   def __repr__(self):
      repr_signals = [self._sequence_to_ellipsized_string(x) for x in self._repr_signals]
      repr_signals = ', '.join(repr_signals)
      return '%s(%s)' % (self.__class__.__name__, repr_signals)

   ## PRIVATE METHODS ##

   def _make_tuplets(self, duration_pairs, leaf_lists):
      assert len(duration_pairs) == len(leaf_lists)
      tuplets = [ ]
      for duration_pair, leaf_list in zip(duration_pairs, leaf_lists):
         tuplet = tuplettools.FixedDurationTuplet(duration_pair, leaf_list)
         tuplets.append(tuplet)
      return tuplets

   def _none_to_new_list(self, expr):
      if expr is None:
         return [ ]
      return expr

   def _none_to_trivial_helper(self, expr):
      if expr is None:
         return self._trivial_helper
      return expr

   def _scale_signals(self, duration_pairs, denominator, signals):
      dummy_duration_pair = (1, denominator)
      duration_pairs.append(dummy_duration_pair)
      duration_pairs = durtools.duration_tokens_to_duration_pairs_with_least_common_denominator(
         duration_pairs)
      dummy_duration_pair = duration_pairs.pop( )
      lcd = dummy_duration_pair[1]
      multiplier = lcd / denominator
      scaled_signals = [ ]
      for signal in signals:
         signal = seqtools.CyclicTuple([multiplier * x for x in signal])
         scaled_signals.append(signal)
      result = [duration_pairs, lcd]
      result.extend(scaled_signals)
      return tuple(result)
         
   def _sequence_to_ellipsized_string(self, sequence):
      if not sequence:
         return '[ ]'
      if len(sequence) <= 4:
         result = ', '.join([str(x) for x in sequence])
      else:
         result = ', '.join([str(x) for x in sequence[:4]])
         result += ', ...'
      result = '[$%s$]' % result
      return result

   def _trivial_helper(self, signal, seeds):
      return signal
