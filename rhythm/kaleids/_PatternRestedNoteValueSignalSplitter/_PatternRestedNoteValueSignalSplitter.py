from abjad.tools import mathtools
from abjad.tools import seqtools
from baca.rhythm.kaleids.NoteValueSignalSplitter import NoteValueSignalSplitter
import types


class _PatternRestedNoteValueSignalSplitter(NoteValueSignalSplitter):
   '''Left-rested note-value signal splitter.

   See the test file for examples.

   Rest list of lists.

   Sublists contain untied notes and / or rest.
   '''

   def __init__(self, note_value_signal, denominator, resting_signal,
      note_value_signal_preprocessor = None, resting_signal_preprocessor = None):
      NoteValueSignalSplitter.__init__(self, note_value_signal, denominator,
         note_value_signal_preprocessor = note_value_signal_preprocessor)
      assert seqtools.all_are_positive_integers(resting_signal)
      if resting_signal_preprocessor is None:
         resting_signal_preprocessor = self._trivial_signal_preprocessor
      assert isinstance(resting_signal_preprocessor, (types.FunctionType, types.MethodType))
      self._resting_signal = resting_signal
      self._resting_signal_preprocessor = resting_signal_preprocessor
      self._repr_signals.append(self._resting_signal)

   ## OVERLOADS ##

   def __call__(self, duration_tokens, seeds):
      rested_note_value_signal = self._rest_note_value_signal(seeds)
      leaf_lists = self._make_everything(rested_note_value_signal, duration_tokens, seeds)
      return leaf_lists

   ## PRIVATE METHODS ##

   def _rest_note_value_signal(self, seeds):
      resting_signal = self._resting_signal_preprocessor(self._resting_signal, seeds)
      note_value_signal = self._note_value_signal_preprocessor(self._note_value_signal, seeds)
      lcm = mathtools.least_common_multiple(len(note_value_signal), sum(resting_signal))
      note_value_signal = seqtools.repeat_sequence_to_length(note_value_signal, lcm)
      partitioned_note_value_signal = seqtools.partition_sequence_cyclically_by_counts_with_overhang(
         note_value_signal, resting_signal)
      rested_note_value_signal = self._rest_parts_of_note_value_signal(partitioned_note_value_signal)
      rested_note_value_signal = seqtools.flatten_sequence(rested_note_value_signal)
      return rested_note_value_signal
