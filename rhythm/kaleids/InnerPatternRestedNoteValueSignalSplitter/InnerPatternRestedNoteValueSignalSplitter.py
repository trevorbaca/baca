from abjad.tools import mathtools
from abjad.tools import seqtools
from baca.rhythm.kaleids._PatternRestedNoteValueSignalSplitter import _PatternRestedNoteValueSignalSplitter
import types


class InnerPatternRestedNoteValueSignalSplitter(_PatternRestedNoteValueSignalSplitter):
   '''Inner-rested note-value signal splitter.

   See the test file for examples.

   Rest list of lists.

   Sublists contain untied notes and / or rest.
   '''

   ## PRIVATE METHODS ##

   def _rest_parts_of_note_value_signal(self, partitioned_note_value_signal):
      rested_note_value_signal = [ ]
      for part in partitioned_note_value_signal:
         rested_part = list(part)
         if 3 <= len(part):
            rested_part[1:-1] = [-abs(x) for x in rested_part[1:-1]]
         rested_note_value_signal.append(rested_part)
      rested_note_value_signal = seqtools.flatten_sequence(rested_note_value_signal)
      return rested_note_value_signal
