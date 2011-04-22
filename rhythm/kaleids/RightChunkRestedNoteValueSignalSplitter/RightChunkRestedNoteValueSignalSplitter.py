from baca.rhythm.kaleids._ChunkRestedNoteValueSignalSplitter import _ChunkRestedNoteValueSignalSplitter


class RightChunkRestedNoteValueSignalSplitter(_ChunkRestedNoteValueSignalSplitter):
   '''Right token-rested note-value signal splitter.

   See the test file for examples.

   Rest list of lists.

   Sublists contain untied notes and / or rest.
   '''

   ## PRIVATE METHODS ##

   def _chunk_rest_split_and_scaled_note_value_signal(self, split_and_scaled_note_value_signal):
      result = [list(part) for part in split_and_scaled_note_value_signal]
      result[-1][-1] = -abs(result[-1][-1])
      return result
