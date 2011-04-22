from abjad.tools import durtools
from abjad.tools import leaftools
from abjad.tools import mathtools
from abjad.tools import seqtools
from abjad.tools import tietools
from baca.rhythm.kaleids._RhythmicKaleid import _RhythmicKaleid
from fractions import Fraction
import types


class NoteValueSignalSplitter(_RhythmicKaleid):
   r'''Note-value signal-splitter.

   See the test file for examples.

   Return list of lists.
   
   Sublists contain untied notes and / or rests.
   '''

   def __init__(self, note_value_signal, denominator_of_signal, 
      note_value_signal_preprocessor = None):
      _RhythmicKaleid.__init__(self)
      assert mathtools.is_positive_integer(denominator_of_signal)
      assert seqtools.all_are_integer_equivalent_numbers(note_value_signal)
      if note_value_signal_preprocessor is None:
         note_value_signal_preprocessor = self._trivial_signal_preprocessor
      assert isinstance(note_value_signal_preprocessor, (types.FunctionType, types.MethodType))
      self._denominator_of_signal = denominator_of_signal
      self._note_value_signal = seqtools.CyclicTuple(note_value_signal)
      self._note_value_signal_preprocessor = note_value_signal_preprocessor
      self._repr_signals.append(self._note_value_signal)

   ## OVERLOADS ##

   def __call__(self, duration_tokens, seeds):
      note_value_signal = self._note_value_signal_preprocessor(self._note_value_signal, seeds)
      leaf_lists = self._make_everything(note_value_signal, duration_tokens, seeds)
      return leaf_lists

   ## PRIVATE METHODS ##

   ## TODO: rename function to show that it is a wrapper around other high-level method calls
   def _make_everything(self, note_value_signal, duration_tokens, seeds):
      scaled_note_value_signal, denominator_of_scaled_signal = self._scale_note_value_signal(
         note_value_signal, duration_tokens)
      split_and_scaled_note_value_signal = \
         self._split_scaled_note_value_signal_extended_to_duration_tokens(
         scaled_note_value_signal, denominator_of_scaled_signal, duration_tokens)
      leaf_lists = self._make_leaf_lists(
         split_and_scaled_note_value_signal, denominator_of_scaled_signal)
      tietools.remove_tie_spanners_from_components_in_expr(leaf_lists)
      return leaf_lists

   def _make_leaf_lists(self, note_value_signal_lists, denominator_of_signal):
      result = [ ]
      for note_value_signal in note_value_signal_lists:
         leaves = leaftools.make_leaves_from_note_value_signal(
            note_value_signal, denominator_of_signal)
         result.append(leaves)
      return result

   def _scale_note_value_signal(self, note_value_signal, duration_tokens):
      lcd = durtools.duration_tokens_to_least_common_denominator(duration_tokens) 
      ## if signal is coarse relative to duration tokens
      if self._denominator_of_signal < lcd:
         assert self._denominator_of_signal in mathtools.divisors(lcd)
         multiplier = int(lcd / self._denominator_of_signal)
      ## if signal is fine relative to duration tokens
      else:
         multiplier = 1
      denominator_of_scaled_signal = multiplier * self._denominator_of_signal
      scaled_note_value_signal = type(note_value_signal)([
         multiplier * x for x in note_value_signal])
      return scaled_note_value_signal, denominator_of_scaled_signal

   def _split_scaled_note_value_signal_extended_to_duration_tokens(
      self, scaled_note_value_signal, denominator_of_scaled_signal, duration_tokens):
      duration_tokens = duration_tokens[:]
      dummy_duration_token = Fraction(1, denominator_of_scaled_signal)
      duration_tokens.append(dummy_duration_token)
      duration_pairs = durtools.duration_tokens_to_duration_pairs_with_least_common_denominator(
         duration_tokens)
      duration_pairs = duration_pairs[:-1]
      weights = [duration_pair[0] for duration_pair in duration_pairs]
      split_and_scaled_note_value_signal = \
         seqtools.split_sequence_extended_to_weights_without_overhang(
         scaled_note_value_signal, weights)
      return split_and_scaled_note_value_signal
