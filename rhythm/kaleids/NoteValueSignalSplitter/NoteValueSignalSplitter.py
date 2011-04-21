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

   Split corase signal::

      abjad> signal = [1]
      abjad> denominator_of_signal = 1
      abjad> def signal_preprocessor(signal, seeds):
      ...   voice_index, measure_index = seeds
      ...   result = seqtools.rotate_sequence(signal, -voice_index * len(signal) // 4)
      ...   result = seqtools.rotate_sequence(result, -measure_index * 4)
      ...   return type(signal)(result)

   ::

      abjad> splitter = baca.rhythm.kaleids.NoteValueSignalSplitter(signal, denominator_of_signal, signal_preprocessor)

   ::

      abjad> duration_pairs = [(2, 8), (5, 8)]
      abjad> leaf_lists = splitter(duration_pairs, [0, 0])

   ::
   
      abjad> leaf_lists
      [[Note("c'4")], [Note("c'2"), Note("c'8")]]

   ::

      abjad> leaves = seqtools.flatten_sequence(leaf_lists)
      abjad> staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_pairs))
      abjad> measuretools.replace_contents_of_measures_in_expr(staff, leaves)

   ::
      
      abjad> f(staff)
      \new Staff {
         {
            \time 2/8
            c'4
         }
         {
            \time 5/8
            c'2
            c'8
         }
      }

   Split fine signal::

      abjad> signal = [-1, 5]
      abjad> denominator_of_signal = 16
      abjad> def signal_preprocessor(signal, seeds):
      ...   voice_index, measure_index = seeds
      ...   result = seqtools.rotate_sequence(signal, -voice_index * len(signal) // 4)
      ...   result = seqtools.rotate_sequence(result, -measure_index * 4)
      ...   return type(signal)(result)

   ::

      abjad> splitter = baca.rhythm.kaleids.NoteValueSignalSplitter(signal, denominator_of_signal, signal_preprocessor)

   ::

      abjad> duration_pairs = [(2, 8), (5, 8)]
      abjad> leaf_lists = splitter(duration_pairs, [0, 0])

   ::
   
      abjad> leaf_lists
      [[Rest('r16'), Note("c'8.")], [Note("c'8"), Rest('r16'), Note("c'4"), Note("c'16"), Rest('r16'), Note("c'16")]]

   ::

      abjad> leaves = seqtools.flatten_sequence(leaf_lists)
      abjad> staff = Staff(measuretools.make_measures_with_full_measure_spacer_skips(duration_pairs))
      abjad> measuretools.replace_contents_of_measures_in_expr(staff, leaves)

   ::
      
      abjad> f(staff)
      \new Staff {
         {
            \time 2/8
            r16
            c'8.
         }
         {
            \time 5/8
            c'8
            r16
            c'4
            c'16
            r16
            c'16
         }
      }

   Return list of lists.
   
   Sublists contain untied notes and / or rests.
   '''

   def __init__(self, note_value_signal, denominator_of_signal, note_value_signal_preprocessor):
      assert mathtools.is_positive_integer(denominator_of_signal)
      assert seqtools.all_are_integer_equivalent_numbers(note_value_signal)
      assert isinstance(note_value_signal_preprocessor, types.FunctionType)
      self._denominator_of_signal = denominator_of_signal
      self._note_value_signal = seqtools.CyclicTuple(note_value_signal)
      self._note_value_signal_preprocessor = note_value_signal_preprocessor
      self._ellipsized_signal = self._sequence_to_ellipsized_string(self._note_value_signal)

   ## OVERLOADS ##

   def __call__(self, duration_tokens, seeds):
      '''Make rhythm from duration pairs.
      '''
      preprocessed_note_value_signal = self._note_value_signal_preprocessor(self._note_value_signal, seeds)
      scaled_note_value_signal, denominator_of_scaled_signal = self._scale_note_value_signal(
         preprocessed_note_value_signal, duration_tokens)
      split_and_scaled_note_value_signal = self._split_scaled_note_value_signal_extended_to_duration_tokens(
         scaled_note_value_signal, denominator_of_scaled_signal, duration_tokens)
      leaf_lists = self._make_leaf_lists(split_and_scaled_note_value_signal, denominator_of_scaled_signal)
      tietools.remove_tie_spanners_from_components_in_expr(leaf_lists)
      return leaf_lists

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._ellipsized_signal)

   ## PRIVATE METHODS ##

   def _make_leaf_lists(self, note_value_signal_lists, denominator_of_signal):
      result = [ ]
      for note_value_signal in note_value_signal_lists:
         leaves = leaftools.make_leaves_from_note_value_signal(note_value_signal, denominator_of_signal)
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
      scaled_note_value_signal = type(note_value_signal)([multiplier * x for x in note_value_signal])
      return scaled_note_value_signal, denominator_of_scaled_signal

   def _split_scaled_note_value_signal_extended_to_duration_tokens(
      self, scaled_note_value_signal, denominator_of_scaled_signal, duration_tokens):
      dummy_duration_token = Fraction(1, denominator_of_scaled_signal)
      duration_tokens.append(dummy_duration_token)
      duration_pairs = durtools.duration_tokens_to_duration_pairs_with_least_common_denominator(duration_tokens)
      duration_pairs = duration_pairs[:-1]
      weights = [duration_pair[0] for duration_pair in duration_pairs]
      split_and_scaled_note_value_signal = seqtools.split_sequence_extended_to_weights_without_overhang(
         scaled_note_value_signal, weights)
      return split_and_scaled_note_value_signal
