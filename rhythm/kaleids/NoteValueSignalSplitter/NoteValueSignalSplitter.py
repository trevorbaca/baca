from abjad.tools import durtools
from abjad.tools import mathtools
from abjad.tools import seqtools
from baca.rhythm.kaleids._RhythmicKaleid import _RhythmicKaleid
import types


class NoteValueSignalSplitter(_RhythmicKaleid):
   '''Split note-value signal.

   Return list of zero or more untied notes and / or rests.
   '''

   def __init__(self, note_value_signal, unit_of_signal, note_value_signal_preprocessor):
      assert durtools.is_duration_token(unit_of_signal)
      assert seqtools.all_are_integer_equivalent_numbers(note_value_signal)
      assert isinstance(note_value_signal_preprocessor, types.FunctionType)
      self._unit_of_signal = durtools.duration_token_to_rational(unit_of_signal)
      self._note_value_signal = seqtools.CyclicTuple(note_value_signal)
      self._note_value_signal_preprocessor = note_value_signal_preprocessor
      ellipsized_signal = self._sequence_to_ellipsized_string(self._note_value_signal)
      self._ellipsized_signal = ellipsized_signal

   ## OVERLOADS ##

   def __call__(self, duration_tokens, seeds):
      '''Make rhythm from duration pairs.
      '''
      assert seqtools.all_are_integer_equivalent_numbers(seeds)
      note_value_signal = self._note_value_signal_preprocessor(self._note_value_signal, seeds)
      note_value_signal = self._scale_note_value_signal(note_value_signal, duration_tokens)
      #duration_pairs = self._duration_tokens_to_duration_pairs(duration_tokens)
      return [ ]

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._ellipsized_signal)

   ## PRIVATE METHODS ##

   def _scale_note_value_signal(self, note_value_signal, duration_tokens):
      signal_denominator = self._unit_of_signal.denominator
      lcd = durtools.duration_tokens_to_least_common_denominator(duration_tokens) 
      if signal_denominator < lcd:
         assert signal_denominator in mathtools.divisors(lcd)
         multiplier = int(lcd / signal_denominator)
         note_value_signal = type(note_value_signal)([
            multiplier * x for x in note_value_signal])
      return note_value_signal
