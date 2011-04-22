from abjad.components import Note
from abjad.components import Rest
from abjad.tools import durtools


class _RhythmicKaleid(object):

   ## OVERLOADS ##

   def __repr__(self):
      return '%s( )' % (self.__class__.__name__)

   ## PRIVATE METHODS ##

   def _sequence_to_ellipsized_string(self, sequence):
      result = ', '.join([str(x) for x in sequence[:4]])
      if 4 < len(sequence):
         result += ', ...'
      result = '[%s]' % result
      return result

   def _trivial_signal_preprocessor(self, signal, seeds):
      return signal[:]
