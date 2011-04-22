from abjad.tools import mathtools
from abjad.tools import seqtools
from baca.rhythm.kaleids._TokenRestedNoteValueSignalSplitter import _TokenRestedNoteValueSignalSplitter
import types


class LeftTokenRestedNoteValueSignalSplitter(_TokenRestedNoteValueSignalSplitter):
   '''Left token-rested note-value signal splitter.

   See the test file for examples.

   Rest list of lists.

   Sublists contain untied notes and / or rest.
   '''

   ## PRIVATE METHODS ##

   def _token_rest_split_and_scaled_note_value_signal(self, split_and_scaled_note_value_signal):
      split_and_rested_note_value_signal = [ ]
      for part in split_and_scaled_note_value_signal:
         rested_part = list(part)
         rested_part[0] = -abs(rested_part[0])
         split_and_rested_note_value_signal.append(rested_part)
      return split_and_rested_note_value_signal
