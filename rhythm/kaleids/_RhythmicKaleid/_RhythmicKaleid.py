from abjad.components import Note
from abjad.components import Rest
from abjad.tools import durtools
from abjad.tools import seqtools
import copy


class _RhythmicKaleid(object):

   def __init__(self):
      self._repr_signals = [ ]

   ## OVERLOADS ##

   def __call__(self, duration_tokens, seeds = None):
      duration_pairs = durtools.duration_tokens_to_duration_pairs(duration_tokens)
      seeds = self._handle_none_seeds(seeds)
      return duration_pairs, seeds

   def __repr__(self):
      repr_signals = [self._sequence_to_ellipsized_string(x) for x in self._repr_signals]
      repr_signals = ', '.join(repr_signals)
      return '%s(%s)' % (self.__class__.__name__, repr_signals)

   ## PRIVATE METHODS ##

   def _handle_none_preprocessor(self, preprocessor):
      if preprocessor is None:
         return self._trivial_signal_preprocessor
      return preprocessor
         
   def _handle_none_seeds(self, seeds):
      if seeds is None:
         return [ ]
      return seeds
         
   def _sequence_to_ellipsized_string(self, sequence):
      sequence = seqtools.repeat_sequence_to_length(sequence, 4)
      result = ', '.join([str(x) for x in sequence[:4]])
      result += ', ...'
      result = '[%s]' % result
      return result

   def _trivial_signal_preprocessor(self, signal, seeds):
      return signal
