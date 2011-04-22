from abjad.components import Note
from abjad.components import Rest
from abjad.tools import durtools


class _RhythmicKaleid(object):

   def __init__(self):
      self._repr_signals = [ ]

   ## OVERLOADS ##

   def __repr__(self):
      repr_signals = [self._sequence_to_ellipsized_string(x) for x in self._repr_signals]
      repr_signals = ', '.join(repr_signals)
      return '%s(%s)' % (self.__class__.__name__, repr_signals)

   ## PRIVATE METHODS ##

   def _sequence_to_ellipsized_string(self, sequence):
      result = ', '.join([str(x) for x in sequence[:4]])
      result += ', ...'
      result = '[%s]' % result
      return result

   def _trivial_signal_preprocessor(self, signal, seeds):
      return signal[:]
