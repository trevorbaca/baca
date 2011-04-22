from abjad.tools import mathtools
from abjad.tools import seqtools
from abjad.tools import tietools
from baca.rhythm.kaleids.NoteValueSignalSplitter import NoteValueSignalSplitter
import types


class _ChunkRestedNoteValueSignalSplitter(NoteValueSignalSplitter):
   '''Chunk-rested note-value signal splitter.

   Rest list of lists.

   Sublists contain untied notes and / or rest.
   '''

   ## OVERLOADS ##

   def __call__(self, duration_tokens, seeds = None):
      if seeds is None:
         seeds = [ ]
      note_value_signal = self._note_value_signal_preprocessor(self._note_value_signal, seeds)
      split_and_scaled_note_value_signal, denominator = self._scale_and_split_note_value_signal(
         note_value_signal, duration_tokens, seeds)
      split_and_rested_note_value_signal = self._chunk_rest_split_and_scaled_note_value_signal(
         split_and_scaled_note_value_signal)
      leaf_lists = self._make_leaf_lists(split_and_rested_note_value_signal, denominator)
      tietools.remove_tie_spanners_from_components_in_expr(leaf_lists)
      return leaf_lists
