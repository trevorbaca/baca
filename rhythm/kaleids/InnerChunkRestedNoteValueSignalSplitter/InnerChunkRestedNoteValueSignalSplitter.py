from abjad.tools import seqtools
from baca.rhythm.kaleids._ChunkRestedNoteValueSignalSplitter import _ChunkRestedNoteValueSignalSplitter


class InnerChunkRestedNoteValueSignalSplitter(_ChunkRestedNoteValueSignalSplitter):
   '''Inner token-rested note-value signal splitter.

   See the test file for examples.

   Rest list of lists.

   Sublists contain untied notes and / or rest.
   '''

   ## PRIVATE METHODS ##

   def _chunk_rest_split_and_scaled_note_value_signal(self, split_and_scaled_note_value_signal):
      lengths = [len(part) for part in split_and_scaled_note_value_signal]
      result = seqtools.flatten_sequence(split_and_scaled_note_value_signal)
      if 3 <= len(result):
         result[1:-1] = [-abs(x) for x in result[1:-1]]
      result = seqtools.partition_sequence_once_by_counts_without_overhang(result, lengths)
      return result
