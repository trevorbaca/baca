from abjad.tools import durtools
from abjad.tools import mathtools
from abjad.tools import seqtools
from abjad.tools import tuplettools
from baca.rhythm.kaleids.NoteValueSignalSplitter import NoteValueSignalSplitter
import types


class ProlatedNoteValueSignalSplitter(NoteValueSignalSplitter):
   '''Proalted note-value signal splitter.

   See the test file for examples.

   Return list of tuplets.
   '''

   def __init__(self, note_value_signal, denominator_of_signal, note_value_signal_preprocessor,
      prolation_addenda_signal, prolation_addenda_signal_preprocessor):
      NoteValueSignalSplitter.__init__(self, note_value_signal, denominator_of_signal, note_value_signal_preprocessor)
      assert all([mathtools.is_integer_equivalent_number(x) for x in prolation_addenda_signal])
      assert isinstance(prolation_addenda_signal_preprocessor, types.FunctionType)
      self._prolation_addenda_signal = prolation_addenda_signal
      self._prolation_addenda_signal_preprocessor = prolation_addenda_signal_preprocessor
      self._ellipsized_prolation_addenda_signal = self._sequence_to_ellipsized_string(self._prolation_addenda_signal)
      
   ## OVERLOADS ##

   def __call__(self, duration_tokens, seeds):
      duration_pairs = durtools.duration_tokens_to_duration_pairs(duration_tokens)
      prolation_addenda = self._calculate_prolation_addenda(duration_pairs, seeds)
      prolated_duration_pairs = self._make_prolated_duration_pairs(duration_pairs, prolation_addenda)
      leaf_lists = self._make_everything(prolated_duration_pairs, seeds)
      tuplets = self._make_tuplets(duration_pairs, leaf_lists)
      return tuplets

   def __repr__(self):
      return '%s(%s, %s)' % (
         self.__class__.__name__, self._ellipsized_note_value_signal, self._ellipsized_prolation_addenda_signal)

   ## PRIVATE METHODS ##

   def _calculate_prolation_addenda(self, duration_pairs, seeds):
      prolation_addenda = self._prolation_addenda_signal_preprocessor(self._prolation_addenda_signal, seeds)
      prolation_addenda = seqtools.partition_sequence_extended_to_counts_without_overhang(
         prolation_addenda, [len(duration_pairs)])
      prolation_addenda = prolation_addenda[0]
      numerators = [duration_pair[0] for duration_pair in duration_pairs]
      pairs = zip(prolation_addenda, numerators)
      prolation_addenda = [prolation_addendum % numerator for (prolation_addendum, numerator) in pairs]
      return prolation_addenda

   def _make_prolated_duration_pairs(self, duration_pairs, prolation_addenda):
      pairs = zip(duration_pairs, prolation_addenda)
      prolated_duration_pairs = [
         (duration_pair[0] + prolation_addendum, duration_pair[1]) for (duration_pair, prolation_addendum) in pairs]
      return prolated_duration_pairs

   def _make_tuplets(self, duration_pairs, leaf_lists):
      tuplets = [ ]
      for duration_pair, leaf_list in zip(duration_pairs, leaf_lists):
         tuplet = tuplettools.FixedDurationTuplet(duration_pair, leaf_list)
         tuplets.append(tuplet)
      return tuplets
