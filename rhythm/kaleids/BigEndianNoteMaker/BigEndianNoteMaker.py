from abjad.tools import notetools
from abjad.tools import tietools
from baca.rhythm.kaleids._NoteMaker import _NoteMaker


class BigEndianNoteMaker(_NoteMaker):
   '''Big-endian note maker.

   See the test file for examples.
   '''

   ## PRIVATE METHODS ##

   def _make_note_lists(self, duration_tokens):
      note_lists = [ ]
      for duration_token in duration_tokens:
         note_list = notetools.make_notes([0], [duration_token], direction = 'big-endian')
         note_lists.append(note_list)
      tietools.remove_tie_spanners_from_components_in_expr
      return note_lists
